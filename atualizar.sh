#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# ESTUDADOR — Script de Atualizacao
# ═══════════════════════════════════════════════════════════════
#
# Atualiza o Estudador para a versao mais recente do GitHub.
# Funciona em qualquer versao instalada anteriormente.
#
# Como usar:
#   bash <(curl -sL https://raw.githubusercontent.com/Hackerdomarketing/estudador/main/atualizar.sh)
#
# ═══════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SKILL_DIR="$HOME/.claude/skills/estudador"
SETTINGS_FILE="$HOME/.claude/settings.json"
REPO_RAW="https://raw.githubusercontent.com/Hackerdomarketing/estudador/main"
HOOK_COMMAND="python3 $SKILL_DIR/scripts/ativar_estudador.py"

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}        ESTUDADOR — Atualizacao${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo ""

# ─── PASSO 1: Baixar arquivos atualizados ──────────────────────

echo -e "${YELLOW}[1/3]${NC} Baixando arquivos atualizados do GitHub..."

mkdir -p "$SKILL_DIR/scripts"

curl -sL "$REPO_RAW/scripts/ativar_estudador.py" -o "$SKILL_DIR/scripts/ativar_estudador.py"
curl -sL "$REPO_RAW/instalar.sh" -o "$SKILL_DIR/instalar.sh"
curl -sL "$REPO_RAW/atualizar.sh" -o "$SKILL_DIR/atualizar.sh"
chmod +x "$SKILL_DIR/instalar.sh" "$SKILL_DIR/atualizar.sh"

echo -e "  ${GREEN}✓${NC} Arquivos atualizados"
echo ""

# ─── PASSO 2: Corrigir settings.json ──────────────────────────

echo -e "${YELLOW}[2/3]${NC} Corrigindo configuracao do hook..."

if [ ! -f "$SETTINGS_FILE" ]; then
    echo -e "  ${YELLOW}⚠${NC} settings.json nao encontrado — nada a corrigir"
else
    RESULTADO=$(python3 - << 'PYEOF'
import json
from pathlib import Path

f = Path.home() / '.claude' / 'settings.json'
data = json.loads(f.read_text())
hooks = data.setdefault('hooks', {})
pre = hooks.get('PreCompact', [])
user_prompt = hooks.setdefault('UserPromptSubmit', [])

# Verificar se ja existe em UserPromptSubmit (evitar duplicata)
ja_existe = any(
    'ativar_estudador' in h.get('command', '')
    for group in user_prompt
    for h in group.get('hooks', [])
)

if ja_existe:
    print('ok')
else:
    # Migrar do PreCompact se existir la
    new_pre, moved = [], False
    for group in pre:
        estudador = [h for h in group.get('hooks', []) if 'ativar_estudador' in h.get('command', '')]
        outros = [h for h in group.get('hooks', []) if 'ativar_estudador' not in h.get('command', '')]
        if estudador:
            user_prompt.append({'matcher': '*', 'hooks': estudador})
            moved = True
        if outros:
            new_pre.append({**group, 'hooks': outros})

    if moved:
        hooks['PreCompact'] = new_pre if new_pre else hooks.pop('PreCompact', None) and None
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        print('migrado')
    else:
        # Nao estava em lugar nenhum — adicionar novo
        hook_cmd = str(Path.home() / '.claude' / 'skills' / 'estudador' / 'scripts' / 'ativar_estudador.py')
        user_prompt.append({'matcher': '*', 'hooks': [{'type': 'command', 'command': f'python3 {hook_cmd}', 'timeout': 5000}]})
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        print('adicionado')
PYEOF
)

    if [ "$RESULTADO" = "migrado" ]; then
        echo -e "  ${GREEN}✓${NC} Hook migrado de PreCompact para UserPromptSubmit"
    elif [ "$RESULTADO" = "adicionado" ]; then
        echo -e "  ${GREEN}✓${NC} Hook adicionado ao UserPromptSubmit"
    else
        echo -e "  ${GREEN}✓${NC} Hook ja estava correto"
    fi
fi

echo ""

# ─── PASSO 3: Confirmacao ──────────────────────────────────────

echo -e "${YELLOW}[3/3]${NC} Verificando..."

if [ -f "$SKILL_DIR/scripts/ativar_estudador.py" ]; then
    echo -e "  ${GREEN}✓${NC} Script atualizado"
else
    echo -e "  ${RED}✗${NC} Script nao encontrado"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  ✓ ATUALIZACAO COMPLETA${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${BOLD}Reinicie o Claude Code para ativar as mudancas.${NC}"
echo ""
echo -e "  O que mudou:"
echo -e "  • Hook agora roda em TODA mensagem (antes: so em sessoes longas)"
echo -e "  • Deteccao de falhas mais precisa (menos falsos positivos)"
echo -e "  • Compativel com Mac, Linux e Windows"
echo ""
