# Estudador — Arquiteto de Certezas Universal 7.0

Agente estudador de elite para Claude Code. Constroi conhecimento confiavel com escavacao em 7 niveis, triangulacao de fontes, modo de contradicao, busca por ausencia de evidencia e sintese operacional orientada a output.

## Quando usar

- Uma IA errou a mesma coisa 2+ vezes
- Precisa de alta confiabilidade antes de decidir
- Existe divergencia entre fontes
- Documentacao oficial nao foi lida por completo
- Precisa de estudo profundo com grau de certeza auditavel
- Precisa comparar performance de agentes/skills em tarefa real

## Instalacao

### Passo 1 — Clonar na pasta de skills do Claude Code

```bash
git clone https://github.com/Hackerdomarketing/estudador.git ~/.claude/skills/estudador
```

Pronto. O Claude Code descobre a skill automaticamente.

### Passo 2 (opcional) — Adicionar triggers explicitos

Para garantir ativacao com 100% de certeza, adicione ao seu `~/.claude/CLAUDE.md`:

```markdown
### ESTUDADOR

Quando o usuario usar qualquer uma destas frases, ative a skill `estudador`:

**Triggers de estudo e pesquisa:**
- "use o estudador", "com o estudador", "pesquise com o estudador", "ative o estudador"
- "estudo profundo", "pesquise isso", "investigue isso", "valide isso"
- "preciso ter certeza", "confirme isso", "verifique isso com rigor"
- "triangule as fontes", "busque evidencia", "escavacao profunda"

**Acao:** Usar a skill `estudador` que carrega o protocolo completo do Arquiteto de Certezas Universal em `~/.claude/skills/estudador/`.

**REGRA CRITICA:** Quando o usuario mencionar "estudador" por nome, SEMPRE ativar a skill. NUNCA substituir por pesquisa manual.
```

## Como usar

Abra o Claude Code e diga qualquer uma destas frases:

| Frase | O que acontece |
|-------|---------------|
| "use o estudador" | Ativa o protocolo completo de 7 niveis |
| "pesquise com o estudador" | Igual acima |
| "estudo profundo sobre X" | Escavacao completa do tema X |
| "preciso ter certeza sobre X" | Validacao rigorosa com triangulacao |
| "triangule as fontes" | Modo de contradicao ativado |

## Pipeline de 7 Niveis

```
Nivel 1: Diagnostico de Lacuna
Nivel 2: Hierarquia de Autoridade Epistemica (Ouro > Prata > Bronze > Ferro > Chumbo)
Nivel 3: Triangulacao com Modo de Contradicao
Nivel 4: Escavacao Sistemica e Contextual
Nivel 5: Busca por Ausencia de Evidencia
Nivel 6: Sintese e Transformacao Competencial
Nivel 7: Atualizacao Continua e Monitoramento
```

## Escala de Certeza

| Nivel | Significado |
|-------|-------------|
| Verdade Absoluta | Ancorada em fonte Ouro (documentacao oficial, codigo-fonte) |
| Verdade Provavel Forte | 3+ fontes independentes Prata/Bronze com alta convergencia |
| Verdade Provavel Fraca | Evidencia parcial ou divergente |
| Verdade Popular sem Validacao | Repeticao sem lastro Ouro/Prata |
| Indeterminado | Evidencia insuficiente |

## Estrutura

```
estudador/
├── SKILL.md                    # Protocolo completo (Arquiteto de Certezas 7.0)
├── AgenteAprendedor.skill      # Pacote distribuivel
├── agents/                     # Agentes de interface
│   └── openai.yaml
├── assets/                     # Templates de entrega
│   ├── template-mapa-conhecimento.md
│   ├── template-manual-boas-praticas.md
│   └── template-alerta-atualizacao.md
├── evals/                      # Testes de qualidade
│   ├── evals-social-media.json
│   └── assertions-social-media.md
├── references/                 # Documentacao de referencia
│   ├── operacao-universal.md
│   ├── matriz-fontes.md
│   ├── modelo-controversia.md
│   ├── checklist-gate-qualidade.md
│   ├── protocolo-monitoramento.md
│   └── persistencia-conhecimento.md
└── scripts/                    # Ferramentas de automacao
    ├── normalize_sources.py
    ├── save_study_bundle.py
    ├── score_plan.py
    ├── simulate_output_score.py
    └── pack_results.py
```

## Licenca

MIT
