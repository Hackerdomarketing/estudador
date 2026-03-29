#!/usr/bin/env python3
"""
ativar_estudador.py — Hook script (PreCompact).
Detecta quando Claude falhou 2+ vezes no mesmo tipo de tarefa SEM resolver.
Quando detecta, injeta additionalContext recomendando ativacao do Estudador.

CORRECOES v2 (2026-03-09):
- Usa additionalContext em vez de systemMessage (systemMessage e apenas visual, nao vai pro Claude)
- Normaliza acentos para regex funcionar com portugues (não → nao, também → tambem)
- Le mensagens do USUARIO alem do assistente (falhas sao reportadas pelo usuario)
- Adiciona logging em /tmp/ativar-estudador-debug.log
- Le ultimas 200 linhas em vez de 80
- Atualiza path do Estudador
"""

import json
import sys
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = str(Path(tempfile.gettempdir()) / "ativar-estudador-debug.log")
ERRO_TRACKER = Path.home() / ".claude" / "inteligencia" / "_erro-tracker.json"
REPORTS_DIR = Path.home() / ".claude" / "skills" / "estudador" / "reports" / "aprendizados"


def log(msg):
    """Log para debug — essencial para diagnosticar hooks silenciosos."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | {msg}\n")
    except Exception:
        pass


def normalizar_acentos(texto):
    """Remove acentos para regex funcionar com portugues.
    não → nao, também → tambem, solução → solucao, é → e
    """
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# Sinais de TENTATIVA (aplicados sobre texto SEM acentos)
SINAIS_TENTATIVA = [
    r"vou tentar", r"tentando", r"testando", r"vamos ver se",
    r"vou testar", r"deixa eu tentar", r"tentei",
    r"vou usar", r"vou criar", r"vou configurar",
    r"vamos testar", r"executando", r"rodando",
    r"let me try", r"trying", r"testing",
]

# Sinais de FALHA (aplicados sobre texto SEM acentos)
SINAIS_FALHA = [
    r"nao funcionou", r"nao deu certo", r"deu errado",
    r"erro:", r"error:", r"falhou", r"failed",
    r"exit code 1", r"exception", r"traceback",
    r"nao resolveu", r"continua com erro", r"mesmo problema",
    r"tambem nao", r"ainda nao",
    r"vou tentar de outra forma", r"outra abordagem",
    r"nao era isso", r"nao e isso",
    r"nao passou", r"nao leu", r"nao tocou",
    r"nao ta", r"nao esta",
    r"doesn.t work", r"didn.t work", r"not working",
]

# Sinais de SOLUCAO (se presentes DEPOIS da ultima falha, NAO ativar)
SINAIS_SOLUCAO = [
    r"agora funcionou", r"resolvido", r"corrigido",
    r"isso funciona", r"funciona agora", r"deu certo",
    r"a solucao foi", r"a solucao e", r"o que resolve",
    r"o correto e", r"a causa era", r"o problema era",
    r"descobri que", r"o erro era",
    r"now it works", r"fixed", r"solved",
]

# Palavras-chave de erro para agrupamento
KEYWORDS_ERRO = [
    "esbuild", "module not found", "permission denied", "timeout",
    "connection refused", "not found", "undefined", "null",
    "import", "require", "install", "dependency",
    "svg", "png", "render", "build", "compile",
    "auth", "token", "api", "cors", "ssl",
    "supabase", "rls", "migration", "sql",
    "git", "push", "commit", "merge",
    "deploy", "vercel", "docker",
    "encoding", "utf", "unicode", "accent",
    "tts", "audio", "voice", "ffplay",
    "hook", "script", "regex",
]


def extrair_texto_transcript(transcript_path):
    """Extrai texto de TODAS as mensagens (assistente E usuario)."""
    textos_assistente = []
    textos_usuario = []
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            # Ler ultimas 200 linhas para pegar mais contexto
            for linha in linhas[-200:]:
                try:
                    obj = json.loads(linha.strip())
                except (json.JSONDecodeError, ValueError):
                    continue

                msg_type = obj.get("type", "")

                if msg_type == "assistant":
                    msg = obj.get("message", {})
                    content = msg.get("content", [])
                    if isinstance(content, str):
                        textos_assistente.append(content)
                    elif isinstance(content, list):
                        for bloco in content:
                            if isinstance(bloco, dict) and bloco.get("type") == "text":
                                textos_assistente.append(bloco.get("text", ""))

                elif msg_type == "human":
                    msg = obj.get("message", {})
                    content = msg.get("content", [])
                    if isinstance(content, str):
                        textos_usuario.append(content)
                    elif isinstance(content, list):
                        for bloco in content:
                            if isinstance(bloco, dict) and bloco.get("type") == "text":
                                textos_usuario.append(bloco.get("text", ""))

    except Exception as e:
        log(f"ERRO lendo transcript: {e}")
        return "", ""

    return " ".join(textos_assistente), " ".join(textos_usuario)


def detectar_falhas_sem_solucao(texto_completo):
    """Detecta 2+ falhas SEM solucao subsequente.
    Opera sobre texto JA NORMALIZADO (sem acentos).
    """
    texto_lower = texto_completo.lower()

    tentativas = []
    falhas = []
    solucoes = []

    for padrao in SINAIS_TENTATIVA:
        for m in re.finditer(padrao, texto_lower):
            tentativas.append(m.start())

    for padrao in SINAIS_FALHA:
        for m in re.finditer(padrao, texto_lower):
            falhas.append(m.start())

    for padrao in SINAIS_SOLUCAO:
        for m in re.finditer(padrao, texto_lower):
            solucoes.append(m.start())

    tentativas.sort()
    falhas.sort()
    solucoes.sort()

    log(f"Deteccao: {len(tentativas)} tentativas, {len(falhas)} falhas, {len(solucoes)} solucoes")

    # Precisamos de 2+ falhas
    if len(falhas) < 2:
        log(f"Menos de 2 falhas ({len(falhas)}), saindo")
        return None

    # Verificar se ha solucao DEPOIS da ultima falha
    ultima_falha = falhas[-1]
    solucoes_depois = [s for s in solucoes if s > ultima_falha]

    if solucoes_depois:
        log(f"Encontrou solucao depois da ultima falha (pos {ultima_falha}), problema resolvido")
        return None

    # Extrair keywords do erro para categorizar
    keywords = []
    for kw in KEYWORDS_ERRO:
        if kw in texto_lower:
            keywords.append(kw)

    # Extrair contexto ao redor das falhas
    contextos = []
    for pos in falhas[-3:]:
        inicio = max(0, pos - 60)
        fim = min(len(texto_completo), pos + 100)
        contextos.append(texto_completo[inicio:fim].strip()[:120])

    resultado = {
        "total_falhas": len(falhas),
        "total_tentativas": len(tentativas),
        "keywords": keywords[:5],
        "contextos": contextos[:2],
    }
    log(f"FALHAS DETECTADAS: {resultado['total_falhas']} falhas, keywords={resultado['keywords']}")
    return resultado


def salvar_erro_tracker(info):
    """Salva informacao de erro no tracker persistente."""
    now = datetime.now(timezone.utc).isoformat()

    tracker = {"erros_recentes": [], "ultima_atualizacao": now}
    if ERRO_TRACKER.exists():
        try:
            with open(ERRO_TRACKER, "r") as f:
                tracker = json.load(f)
        except Exception:
            pass

    tracker["erros_recentes"].append({
        "keywords": info["keywords"],
        "total_falhas": info["total_falhas"],
        "timestamp": now,
    })

    # Manter apenas os 20 mais recentes
    tracker["erros_recentes"] = tracker["erros_recentes"][-20:]
    tracker["ultima_atualizacao"] = now

    try:
        os.makedirs(os.path.dirname(ERRO_TRACKER), exist_ok=True)
        with open(ERRO_TRACKER, "w") as f:
            json.dump(tracker, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"ERRO salvando tracker: {e}")


def escanear_estudos_disponiveis():
    """Escaneia reports/aprendizados/ e retorna lista de estudos com metadados.
    Le os index.json de cada pasta de estudo. Retorna lista leve para injecao."""
    estudos = []
    if not REPORTS_DIR.exists():
        return estudos
    try:
        for date_dir in sorted(REPORTS_DIR.iterdir(), reverse=True):
            if not date_dir.is_dir():
                continue
            for tema_dir in sorted(date_dir.iterdir()):
                if not tema_dir.is_dir():
                    continue
                index_file = tema_dir / "index.json"
                if not index_file.exists():
                    continue
                try:
                    meta = json.loads(index_file.read_text(encoding="utf-8"))
                    cert = meta.get("certainty_summary", {})
                    absoluta = cert.get("verdade_absoluta", 0)
                    provavel = cert.get("verdade_provavel_forte", 0)
                    estudos.append({
                        "tema": meta.get("topic", tema_dir.name),
                        "data": date_dir.name,
                        "certeza": f"{absoluta}A+{provavel}PF",
                        "caminho": str(tema_dir / "07-pacote-especialista.md"),
                    })
                except (json.JSONDecodeError, KeyError):
                    continue
    except Exception as e:
        log(f"ERRO escaneando estudos: {e}")
    return estudos


def montar_contexto_estudos(estudos):
    """Monta texto curto para injecao no additionalContext."""
    if not estudos:
        return ""
    linhas = ["=== ESTUDOS VERIFICADOS (Skill Estudador) ==="]
    for e in estudos[:20]:  # Limite de 20 estudos para nao poluir contexto
        linhas.append(f"- [{e['data']}] {e['tema']} ({e['certeza']}) → {e['caminho']}")
    linhas.append("REGRA: Antes de afirmar que algo nao e possivel ou funciona de tal forma, verifique se ha estudo sobre o tema acima.")
    return "\n".join(linhas)


def main():
    log("=== INICIO ativar_estudador.py ===")

    try:
        raw_input = sys.stdin.read()
        log(f"stdin recebido: {len(raw_input)} chars")
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, Exception) as e:
        log(f"ERRO parsing stdin: {e}")
        sys.exit(0)

    # --- PARTE 1: Escanear estudos disponíveis (SEMPRE roda, mesmo sem transcript) ---
    estudos = escanear_estudos_disponiveis()
    contexto_estudos = montar_contexto_estudos(estudos)
    log(f"Estudos encontrados: {len(estudos)}")

    # --- PARTE 2: Detectar falhas (só se transcript existir) ---
    info = None
    transcript_path = input_data.get("transcript_path", "")
    log(f"transcript_path: {transcript_path}")

    if transcript_path and os.path.exists(transcript_path):
        texto_assistente, texto_usuario = extrair_texto_transcript(transcript_path)
        log(f"Texto extraido: assistente={len(texto_assistente)} chars, usuario={len(texto_usuario)} chars")

        if texto_assistente or texto_usuario:
            texto_completo = texto_assistente + " " + texto_usuario
            texto_normalizado = normalizar_acentos(texto_completo)
            log(f"Texto normalizado: {len(texto_normalizado)} chars")
            info = detectar_falhas_sem_solucao(texto_normalizado)
    else:
        log(f"Transcript nao encontrado — pulando deteccao de falhas")

    # --- PARTE 3: Montar output combinado ---
    partes_contexto = []

    if contexto_estudos:
        partes_contexto.append(contexto_estudos)

    if info:
        salvar_erro_tracker(info)
        kw_str = ", ".join(info["keywords"]) if info["keywords"] else "tipo nao identificado"
        ctx_str = "\n".join(f"  - {c}" for c in info["contextos"])
        mensagem_falha = (
            f"[ALERTA AUTOMATICO — Inteligencia Progressiva]\n"
            f"Detectei {info['total_falhas']} falha(s) em {info['total_tentativas']} tentativa(s) "
            f"sem resolucao nesta sessao.\n"
            f"Tipo de erro: {kw_str}\n"
            f"Contexto:\n{ctx_str}\n\n"
            f"RECOMENDACAO: Pare de tentar e ative a skill 'estudador' "
            f"(em ~/.claude/skills/estudador/) para fazer estudo profundo de 7 niveis "
            f"antes de continuar. Use o Nivel 1 (diagnostico de lacuna) para entender "
            f"a causa raiz.\n"
            f"Comando: Use a skill estudador com o contexto do erro atual."
        )
        partes_contexto.append(mensagem_falha)
        log(f"Emitindo alerta de falhas + estudos")

    if not partes_contexto:
        log("Sem estudos e sem falhas — nada a injetar")
        sys.exit(0)

    output = {
        "additionalContext": "\n\n".join(partes_contexto)
    }
    print(json.dumps(output, ensure_ascii=False))
    log(f"=== FIM ativar_estudador.py — contexto emitido ({len(partes_contexto)} partes) ===")


if __name__ == "__main__":
    main()
