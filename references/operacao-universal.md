# Operacao Universal 7 Niveis

## 1) Matriz de Afirmacoes Criticas

Usar uma linha por afirmacao.

| claim_id | afirmacao | impacto | evidencia_esperada | fontes_coletadas | grau_certeza | risco_erro | status |
|---|---|---|---|---|---|---|---|
| C1 | ... | alto | Ouro oficial | Ouro:..., Prata:..., Bronze:... | ... | ... | pendente |

Regras:
- Impacto alto exige Ouro ou Relatorio de Controversia completo.
- Sem suporte minimo, classificar como `Indeterminado`.

## 2) Relatorio de Controversia (Formato Obrigatorio)

```text
RELATORIO DE CONTROVERSIA
Tema:
Pergunta critica:

Fonte A:
- Identificacao:
- Data:
- Nivel:
- Metodo/dados:
- Posicao:

Fonte B:
- Identificacao:
- Data:
- Nivel:
- Metodo/dados:
- Posicao:

Origem da divergencia:
Consenso atual e forca do consenso:
Razao da indefinicao (se houver):
Risco de decisao errada:
Recomendacao operacional sob incerteza:
```

## 3) Alerta de Verdade Popular sem Validacao Primaria

```text
ALERTA: VERDADE POPULAR SEM VALIDACAO PRIMARIA
Afirmacao:
Popularidade observada (Ferro/Chumbo):
Local esperado da evidencia primaria:
Resultado da verificacao de ausencia:
Impacto se adotada sem validacao:
Acao recomendada:
```

## 4) Alerta de Atualizacao Critica

```text
ATUALIZACAO CRITICA DETECTADA
Topico:
Fonte nova:
Data:
Entendimento anterior:
Entendimento atualizado:
Praticas que devem ser revisadas:
Prioridade:
```

## 5) Mapa de Conhecimento Vivo (Estrutura Minima)

- Escopo do dominio
- Grafo de entidades e relacoes
- Casos validados
- Casos onde nao se aplica
- Limitacoes conhecidas
- Dependencias e pre-requisitos
- Padroes de erro recorrentes e solucoes
- Controversias ativas
- Alertas de ausencia

## 6) Manual de Boas Praticas Validadas (Estrutura Minima)

- Objetivo operacional
- Passo a passo executavel
- Variacoes por contexto
- Falhas frequentes e mitigacao
- Fontes primarias por etapa critica
- Condicoes de parada e criterio de sucesso

## 7) Pacote de Especializacao Reutilizavel

Entregar bloco reutilizavel com:
- Decisoes validadas
- Anti-padroes
- Checklists de execucao
- Fontes de manutencao (Ouro/Prata)
- Gatilhos de revisao futura

Persistencia obrigatoria (sempre que houver escrita de arquivo):
- Salvar em `reports/aprendizados/<YYYY-MM-DD>/<tema-slug>/`
- Gerar `index.json` com:
  - `topic`
  - `generated_at`
  - `model_or_agent`
  - `certainty_summary`
  - `files`

Se escrita de arquivo estiver indisponivel:
- Marcar `PERSISTENCIA BLOQUEADA`
- Entregar os artefatos completos inline
- Tentar gravar assim que escrita estiver disponivel

## 8) Checklist Final (Pass/Fail)

Marcar `SIM` ou `NAO` para cada item:
- Diagnostico do erro foi especifico?
- Busca ocorreu em 3 niveis ou mais?
- Cada afirmacao critica tem Ouro ou 3 fontes independentes Prata/Bronze?
- Todas as contradicoes foram documentadas?
- Busca por ausencia foi executada?
- Grafo de conhecimento foi construido?
- 3 produtos do Nivel 6 foram entregues?
- Grau de certeza foi informado por afirmacao?
- Estilo escolhido afetou so a forma?
- Pacote de persistencia foi salvo no caminho padrao?
