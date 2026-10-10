# Sintese de Descobertas no Chat (Canal 2)

## Por que esta regra existe

Sintoma real relatado pelo usuario: o Estudador fazia o estudo inteiro, salvava os 10
artefatos, e respondia no chat apenas "estudo concluido, pacote salvo em reports/...".
O usuario ficava com a confirmacao e sem o aprendizado. No claude.ai era pior, porque lá
nao ha arquivo nenhum para abrir depois.

Causa-raiz: a skill especificava os ARQUIVOS em detalhe obsessivo e nunca especificava a
MENSAGEM. Onde nao ha regra, o modelo usa o padrao dele — que e resumir que trabalhou.

## Os 6 blocos obrigatorios

```text
1. O QUE EU INVESTIGUEI      -> uma frase com a pergunta real
2. O QUE EU DESCOBRI         -> 3 a 5 achados concretos + grau de certeza em cada
3. O QUE EU DERRUBEI         -> crencas comuns que nao se sustentaram
4. O QUE CONTINUA INCERTO    -> controversias e Indeterminado + risco de decidir sem isso
5. O QUE FAZER COM ISSO      -> 1 a 3 acoes concretas
6. ONDE ESTA O ESTUDO        -> caminho do pacote, ou PERSISTENCIA BLOQUEADA
```

## Exemplo correto (tema: parcelamento em checkout proprio no Brasil)

```text
1. O QUE EU INVESTIGUEI
Se da para montar checkout proprio com parcelamento e upsell no Brasil, e com qual gateway.

2. O QUE EU DESCOBRI
- Stripe nao oferece parcelamento em BRL para conta brasileira — confirmado na doc oficial de
  metodos de pagamento [Verdade Absoluta]
- Pagar.me, Asaas e Efi suportam parcelado em cartao com repasse de juros configuravel
  [Verdade Provavel Forte — 3 docs oficiais convergentes]
- Order bump no checkout proprio exige tokenizacao do cartao antes do upsell, senao o cliente
  digita o cartao duas vezes e a conversao cai [Verdade Provavel Forte]
- Guru e Doppus resolvem parcelado + upsell sem desenvolvimento, com custo maior por transacao
  [Verdade Provavel Forte]

3. O QUE EU DERRUBEI
"Stripe parcela no Brasil" circula muito em blogs e grupos, mas nao tem lastro na documentacao
oficial. E Verdade Popular sem Validacao Primaria — provavelmente confusao com Stripe Mexico,
onde parcelamento existe de fato.

4. O QUE CONTINUA INCERTO
Taxa efetiva do Pagar.me em volume alto: a tabela publica nao cobre negociacao acima de certo
faturamento. Decidir o gateway so pela taxa de tabela pode custar caro — pedir proposta antes.

5. O QUE FAZER COM ISSO
- Se prioridade e velocidade: Guru ou Doppus, sobe essa semana.
- Se prioridade e margem no longo prazo: Pagar.me ou Asaas, com proposta negociada.
- Em qualquer rota: tokenizar o cartao antes do upsell.

6. ONDE ESTA O ESTUDO COMPLETO
~/.claude/skills/estudador/reports/aprendizados/2026-10-03/checkout-proprio-parcelado-upsell-brasil/
```

## Exemplo ERRADO (nunca fazer)

```text
Estudo concluido com sucesso.

Executei os 7 niveis do protocolo, consultei 14 fontes (3 Ouro, 6 Prata, 5 Bronze),
documentei 2 controversias e executei a busca por ausencia de evidencia.

Pacote salvo em reports/aprendizados/2026-10-03/checkout-proprio/
10 arquivos gerados. Gate de qualidade: 11/11 SIM.
```

Por que esta errado:
- Narra o processo, nao os achados.
- O usuario nao sabe NADA sobre checkout depois de ler isso.
- Conta fontes em vez de dizer o que as fontes disseram.
- Exige abrir arquivo para obter o valor do trabalho.
- No claude.ai esse caminho de arquivo nem existe.

## Erros frequentes de calibragem

| Erro | Correcao |
|---|---|
| Achado vago ("a ferramenta tem limitacoes") | Nomear a limitacao exata e a consequencia |
| Grau de certeza ausente | Todo achado carrega o seu, sem excecao |
| Remeter ao arquivo ("detalhes no 05-mapa") | O chat tem que bastar sozinho |
| Despejar os 10 artefatos no chat | Sintese primeiro, artefatos depois e separados |
| Encurtar por "estilo Executivo" | Estilo muda o tom, nunca remove bloco |
| Mais de 5 achados no bloco 2 | Escolher os 5 de maior impacto e dizer quantos ficaram no arquivo |
