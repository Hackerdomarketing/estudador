#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# ESTUDADOR — Script de Instalacao
# ═══════════════════════════════════════════════════════════════
#
# O que este script faz:
# 1. Copia a skill Estudador para ~/.claude/skills/estudador/
# 2. Configura o hook automatico no settings.json
#    (detecta 2+ falhas sem solucao e recomenda ativar o Estudador)
#
# Como usar:
#   chmod +x instalar.sh && ./instalar.sh
#
# ═══════════════════════════════════════════════════════════════

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SKILL_DIR="$HOME/.claude/skills/estudador"
SETTINGS_FILE="$HOME/.claude/settings.json"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}        ESTUDADOR — Instalacao${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo ""

# ─── PASSO 1: Copiar arquivos da skill ─────────────────────────

echo -e "${YELLOW}[1/4]${NC} Copiando arquivos da skill..."

mkdir -p "$SKILL_DIR"

# Copiar tudo exceto .git, instalar.sh e README.md
rsync -a --exclude='.git' --exclude='instalar.sh' --exclude='README.md' "$SCRIPT_DIR/" "$SKILL_DIR/"

echo -e "  ${GREEN}✓${NC} Skill copiada para $SKILL_DIR"
echo ""

# ─── PASSO 2: Configurar hook no settings.json ────────────────

echo -e "${YELLOW}[2/4]${NC} Configurando hook automatico..."

HOOK_COMMAND="python3 $SKILL_DIR/scripts/ativar_estudador.py"

# Verificar se o hook ja existe
if [ -f "$SETTINGS_FILE" ]; then
    if grep -q "ativar_estudador" "$SETTINGS_FILE" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Hook ja configurado (nada a fazer)"
    else
        # settings.json existe mas sem o hook — adicionar
        if command -v jq &> /dev/null; then
            # Usar jq para merge seguro
            TMP_SETTINGS=$(mktemp)
            jq --arg cmd "$HOOK_COMMAND" '
                .hooks = (.hooks // {}) |
                .hooks.UserPromptSubmit = (.hooks.UserPromptSubmit // []) + [{
                    "matcher": "*",
                    "hooks": [{
                        "type": "command",
                        "command": $cmd,
                        "timeout": 5000
                    }]
                }]
            ' "$SETTINGS_FILE" > "$TMP_SETTINGS" && mv "$TMP_SETTINGS" "$SETTINGS_FILE"
            echo -e "  ${GREEN}✓${NC} Hook adicionado ao settings.json existente"
        else
            echo -e "  ${YELLOW}⚠${NC} jq nao encontrado — nao foi possivel adicionar hook automaticamente"
            echo ""
            echo -e "  ${BOLD}Adicione manualmente ao seu ~/.claude/settings.json:${NC}"
            echo ""
            echo '  "hooks": {'
            echo '    "UserPromptSubmit": [{'
            echo '      "matcher": "*",'
            echo '      "hooks": [{'
            echo '        "type": "command",'
            echo "        \"command\": \"$HOOK_COMMAND\","
            echo '        "timeout": 5000'
            echo '      }]'
            echo '    }]'
            echo '  }'
            echo ""
        fi
    fi
else
    # settings.json nao existe — criar
    mkdir -p "$(dirname "$SETTINGS_FILE")"
    cat > "$SETTINGS_FILE" << EOFJSON
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$HOOK_COMMAND",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
EOFJSON
    echo -e "  ${GREEN}✓${NC} settings.json criado com hook configurado"
fi

echo ""

# ─── PASSO 3: Configurar estrutura de memoria ───────────────────

echo -e "${YELLOW}[3/5]${NC} Configurando estrutura de memoria..."

# Calcular caminho do MEMORY.md global (auto-memory da Anthropic)
# Converte $HOME em project key: /Users/alfa → -Users-alfa
HOME_KEY=$(echo "$HOME" | tr '/' '-')
MEMORY_DIR="$HOME/.claude/projects/$HOME_KEY/memory"
MEMORY_FILE="$MEMORY_DIR/MEMORY.md"

mkdir -p "$MEMORY_DIR"

if [ -f "$MEMORY_FILE" ]; then
    if grep -q "Estudos Verificados (Skill Estudador)" "$MEMORY_FILE" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Secao do Estudador ja existe no MEMORY.md"
    else
        # MEMORY.md existe mas sem secao do estudador — adicionar
        printf '\n## Estudos Verificados (Skill Estudador)\n' >> "$MEMORY_FILE"
        echo -e "  ${GREEN}✓${NC} Secao do Estudador adicionada ao MEMORY.md existente"
    fi
else
    # MEMORY.md nao existe — criar com secao basica
    cat > "$MEMORY_FILE" << 'MEMEOF'
# Memoria do Projeto

## Estudos Verificados (Skill Estudador)
MEMEOF
    echo -e "  ${GREEN}✓${NC} MEMORY.md criado com secao do Estudador"
fi

echo ""

# ─── PASSO 4: Configurar triggers no CLAUDE.md global ─────────

echo -e "${YELLOW}[4/5]${NC} Configurando triggers no CLAUDE.md global..."

CLAUDE_MD="$HOME/.claude/CLAUDE.md"

if [ ! -f "$CLAUDE_MD" ]; then
    touch "$CLAUDE_MD"
fi

if ! grep -q "## ESTUDADOR" "$CLAUDE_MD" 2>/dev/null; then
    cat >> "$CLAUDE_MD" << 'TRIGGER_BLOCK'


## ESTUDADOR

Quando o usuario usar qualquer uma destas frases, ative a skill `estudador`:

**Triggers de ativacao:**
- "use o estudador", "com o estudador", "pesquise com o estudador", "ative o estudador"
- "estudo profundo", "investigue isso", "valide isso", "preciso ter certeza"
- "triangule as fontes", "escavacao profunda"
- "descubra na internet", "busque na internet", "pesquise sobre"
- "me explica com certeza"

**Ativacao automatica:** O hook no settings.json detecta quando o Claude erra 2+ vezes na mesma tarefa e recomenda ativar o Estudador automaticamente.

**REGRA CRITICA:** Quando o usuario mencionar "estudador" por nome, SEMPRE ativar a skill.
TRIGGER_BLOCK
    echo -e "  ${GREEN}✓${NC} Triggers configurados no CLAUDE.md"
else
    echo -e "  ${GREEN}✓${NC} Triggers ja estavam configurados"
fi

echo ""

# ─── PASSO 4: Verificar instalacao ────────────────────────────

echo -e "${YELLOW}[5/5]${NC} Verificando instalacao..."

ERROS=0

if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo -e "  ${GREEN}✓${NC} SKILL.md encontrado"
else
    echo -e "  ${RED}✗${NC} SKILL.md nao encontrado"
    ERROS=$((ERROS + 1))
fi

if [ -f "$SKILL_DIR/scripts/ativar_estudador.py" ]; then
    echo -e "  ${GREEN}✓${NC} Script de ativacao encontrado"
else
    echo -e "  ${RED}✗${NC} Script de ativacao nao encontrado"
    ERROS=$((ERROS + 1))
fi

if grep -q "ativar_estudador" "$SETTINGS_FILE" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Hook configurado no settings.json"
else
    echo -e "  ${YELLOW}⚠${NC} Hook nao configurado (adicione manualmente)"
fi

if [ -f "$MEMORY_FILE" ] && grep -q "Estudos Verificados" "$MEMORY_FILE" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} MEMORY.md configurado com secao do Estudador"
else
    echo -e "  ${YELLOW}⚠${NC} MEMORY.md nao configurado"
fi

echo ""

if [ $ERROS -eq 0 ]; then
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}  ✓ INSTALACAO COMPLETA${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${BOLD}Como usar:${NC}"
    echo -e "  • Manualmente: abra o Claude Code e diga ${CYAN}use o estudador${NC}"
    echo -e "  • Automatico: quando o Claude falhar 2+ vezes na mesma"
    echo -e "    tarefa, o hook detecta e recomenda ativar o Estudador"
    echo ""
    echo -e "  ${BOLD}O que o hook faz:${NC}"
    echo -e "  Antes de compactar o contexto, analisa a conversa."
    echo -e "  Se encontrar 2+ tentativas com falha sem resolucao,"
    echo -e "  injeta um alerta recomendando parar e usar o Estudador."
    echo ""
else
    echo -e "${RED}  ✗ Instalacao com erros. Verifique os itens acima.${NC}"
    echo ""
fi
