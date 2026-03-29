#!/usr/bin/env python3
"""Cria estrutura padrao de persistencia para estudos do AgenteAprendedor."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


FILES = [
    "00-contexto.md",
    "01-matriz-afirmacoes.csv",
    "02-fontes.json",
    "03-controversias.md",
    "04-ausencias-alertas.md",
    "05-mapa-conhecimento.md",
    "06-manual-operacional.md",
    "07-pacote-especialista.md",
    "08-monitoramento.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic-slug", required=True, help="Slug do tema do estudo")
    parser.add_argument(
        "--base-dir",
        default="reports/aprendizados",
        help="Diretorio base de persistencia (padrao: reports/aprendizados)",
    )
    parser.add_argument(
        "--agent-name",
        default="agente-aprendedor",
        help="Nome do agente/modelo para index.json",
    )
    return parser.parse_args()


def calcular_memory_md_path() -> Path | None:
    """Calcula o caminho do MEMORY.md da Anthropic para o diretorio atual.
    Converte o CWD em project key: /Users/alfa → -Users-alfa"""
    cwd = Path.cwd()
    project_key = str(cwd).replace("/", "-")
    memory_dir = Path.home() / ".claude" / "projects" / project_key / "memory"
    return memory_dir / "MEMORY.md"


def escrever_ponteiro_memory_md(topic_slug: str, study_path: Path, date_str: str) -> None:
    """Escreve ponteiro do estudo no MEMORY.md do projeto atual."""
    memory_path = calcular_memory_md_path()
    if memory_path is None:
        return

    memory_path.parent.mkdir(parents=True, exist_ok=True)
    ponteiro = f"- [Estudo: {topic_slug}]({study_path / '07-pacote-especialista.md'}) — {date_str}\n"

    if memory_path.exists():
        conteudo = memory_path.read_text(encoding="utf-8")
        # Verificar se ja tem secao de estudos
        if "## Estudos Verificados" in conteudo:
            # Verificar duplicata
            if topic_slug in conteudo and date_str in conteudo:
                return
            # Adicionar abaixo da secao existente
            conteudo = conteudo.replace(
                "## Estudos Verificados (Skill Estudador)\n",
                f"## Estudos Verificados (Skill Estudador)\n{ponteiro}",
            )
        else:
            conteudo += f"\n## Estudos Verificados (Skill Estudador)\n{ponteiro}"
        memory_path.write_text(conteudo, encoding="utf-8")
    else:
        memory_path.write_text(
            f"# Memoria do Projeto\n\n## Estudos Verificados (Skill Estudador)\n{ponteiro}",
            encoding="utf-8",
        )


def main() -> int:
    args = parse_args()
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(args.base_dir) / date_str / args.topic_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    for fname in FILES:
        path = out_dir / fname
        if not path.exists():
            path.write_text("", encoding="utf-8")

    index = {
        "topic": args.topic_slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_or_agent": args.agent_name,
        "method_version": "7.0",
        "certainty_summary": {
            "verdade_absoluta": 0,
            "verdade_provavel_forte": 0,
            "verdade_provavel_fraca": 0,
            "verdade_popular_sem_validacao": 0,
            "indeterminado": 0,
        },
        "files": FILES,
    }
    (out_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Escrever ponteiro no MEMORY.md do projeto atual
    escrever_ponteiro_memory_md(args.topic_slug, out_dir, date_str)

    print(str(out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
