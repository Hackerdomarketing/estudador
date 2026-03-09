# Persistencia de Conhecimento - Padrao Obrigatorio

## Objetivo

Garantir que todo estudo gere memoria reutilizavel para futuras execucoes, treinamentos e transferencia para outras skills/agentes.

## Caminho padrao

`reports/aprendizados/<YYYY-MM-DD>/<tema-slug>/`

Exemplo:
`reports/aprendizados/2026-03-08/social-media-alcance-massivo/`

## Estrutura minima obrigatoria

1. `00-contexto.md`
2. `01-matriz-afirmacoes.csv`
3. `02-fontes.json`
4. `03-controversias.md`
5. `04-ausencias-alertas.md`
6. `05-mapa-conhecimento.md`
7. `06-manual-operacional.md`
8. `07-pacote-especialista.md`
9. `08-monitoramento.md`
10. `index.json`

## Schema minimo do index.json

```json
{
  "topic": "tema-principal",
  "generated_at": "2026-03-08T10:00:00Z",
  "model_or_agent": "nome-do-agente",
  "method_version": "7.0",
  "certainty_summary": {
    "verdade_absoluta": 0,
    "verdade_provavel_forte": 0,
    "verdade_provavel_fraca": 0,
    "verdade_popular_sem_validacao": 0,
    "indeterminado": 0
  },
  "files": [
    "00-contexto.md",
    "01-matriz-afirmacoes.csv",
    "02-fontes.json",
    "03-controversias.md",
    "04-ausencias-alertas.md",
    "05-mapa-conhecimento.md",
    "06-manual-operacional.md",
    "07-pacote-especialista.md",
    "08-monitoramento.md"
  ]
}
```

## Regra de versionamento

- Novo estudo no mesmo tema no mesmo dia: usar `v2`, `v3`, ...
- Nao sobrescrever estudo anterior sem registro de versao.
- Sempre manter historico de controversias e mudancas de entendimento.
