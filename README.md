# Estudador — Arquiteto de Certezas 7.0

Skill para Claude Code e Claude.ai que transforma "achar uma resposta" em
"ter certeza do que é verdade".

Em vez de pesquisar e devolver o primeiro resultado plausível, o Estudador
escava em 7 níveis, classifica cada fonte por autoridade, trata contradições
como trabalho a ser feito (não como detalhe a ser ignorado) e te entrega o
grau de certeza de cada afirmação — para você saber onde pode pisar firme e
onde o chão é falso.

---

## Sobre este repositório

**Este repositório é público, de propósito.** Ele existe para os clientes e
seguidores do Rafa (Hacker do Marketing) poderem instalar, atualizar e
estudar a skill livremente.

O que está aqui é a **metodologia**: o protocolo dos 7 níveis, os templates,
as referências, os scripts e os instaladores.

O que **não** está aqui são os estudos reais gerados pelo uso da skill. Eles
contêm temas, clientes e decisões de negócio, ficam apenas na máquina de
quem roda a skill (em `reports/aprendizados/`) e estão no `.gitignore`.
Metodologia é pública; conteúdo investigado é privado.

---

## O problema que isso resolve

Toda IA tem o mesmo vício: ela responde com confiança igual quando sabe e
quando está chutando. Você não tem como distinguir as duas coisas olhando a
resposta — as duas soam seguras.

Isso custa caro quando a resposta vira decisão: você escolhe uma ferramenta
que não faz o que prometeram, monta uma operação sobre uma regra que mudou
no ano passado, ou repete uma "verdade" que todo mundo repete e ninguém nunca
verificou na fonte.

O Estudador ataca isso de frente:

- **Hierarquia de fontes** — documentação oficial e dado primário valem mais
  que blog e opinião de fórum, e a skill nunca trata os dois como iguais.
- **Modo de Contradição** — quando duas fontes boas discordam, ela não escolhe
  a mais conveniente: rastreia a origem de cada posição e te mostra por que
  divergem.
- **Busca por ausência de evidência** — pergunta "se isso fosse verdade e
  importante, onde deveria estar escrito?", vai ao lugar esperado e sinaliza
  quando a evidência simplesmente não existe.
- **Grau de certeza por afirmação** — de Verdade Absoluta (fonte primária) até
  Indeterminado (evidência insuficiente), explícito em cada achado.

---

## Como instalar

### No Claude Code (terminal)

Cole esta linha no Terminal e aperte Enter:

```bash
git clone https://github.com/Hackerdomarketing/estudador.git /tmp/estudador && cd /tmp/estudador && chmod +x instalar.sh && ./instalar.sh
```

O instalador faz tudo sozinho: copia a skill para o lugar certo, configura o
gatilho automático, prepara a pasta de memória e confere no final se deu tudo
certo. Ele não apaga nenhuma configuração que você já tenha.

Depois, reinicie o Claude Code.

### Para atualizar depois

```bash
bash <(curl -sL https://raw.githubusercontent.com/Hackerdomarketing/estudador/main/atualizar.sh)
```

### No Claude.ai (navegador ou celular)

Baixe o arquivo `AgenteAprendedor.skill` deste repositório e suba nas
configurações de Skills do Claude.ai. Não precisa de terminal.

---

## Como usar

Diga qualquer uma destas frases no Claude:

```
use o estudador
pesquisa pra mim sobre <tema>
investiga isso
valida isso, preciso ter certeza
me explica com certeza
estudo profundo sobre <tema>
```

**Ativação automática:** se o Claude errar a mesma coisa 2 vezes ou mais na
mesma conversa, um gatilho detecta e recomenda ativar o Estudador — antes de
você perder mais tempo tentando o mesmo caminho.

Você não precisa escolher modo, estilo nem configuração. A skill detecta
sozinha se você quer executar algo, decidir algo, entender um erro ou
aprender um conceito novo, e ajusta a entrega.

---

## O que você recebe

A skill entrega em **dois canais**, e isso é parte do método:

**No chat** — a Síntese de Descobertas, sempre. Seis blocos: o que foi
investigado, o que foi descoberto (cada achado com seu grau de certeza), o
que foi derrubado, o que continua incerto, o que fazer com isso e onde está
o estudo completo. Você termina de ler sabendo o que foi descoberto, sem
precisar abrir arquivo nenhum.

**Em arquivos** (no Claude Code) — o pacote completo com 10 artefatos: matriz
de afirmações, fontes classificadas, relatórios de controvérsia, alertas de
ausência de evidência, mapa de conhecimento, manual operacional e plano de
monitoramento. No Claude.ai, onde não há onde gravar, esse pacote vem no
chat logo abaixo da síntese.

O estudo salvo é reutilizável: na próxima vez que o tema voltar, o
conhecimento já está lá, com data e grau de certeza.

---

## Os 7 níveis, em resumo

1. **Diagnóstico de lacuna** — o erro é de fato, de contexto, de profundidade,
   de ferramenta ou de lógica? Cada um pede um caminho diferente.
2. **Hierarquia de autoridade** — Ouro (fonte primária), Prata, Bronze, Ferro,
   Chumbo. Começa sempre pelo Ouro quando ele existe.
3. **Triangulação com Modo de Contradição** — sem fonte primária, exige no
   mínimo 3 fontes independentes convergentes.
4. **Escavação sistêmica** — documentação integral, changelogs, experiência
   real de quem usou, dependências e condições de contorno.
5. **Busca por ausência de evidência** — caça a "verdade popular" que ninguém
   nunca validou na fonte.
6. **Síntese operacional** — mapa de conhecimento, manual de boas práticas e
   pacote reutilizável.
7. **Monitoramento contínuo** — quais fontes vigiar e o que dispara reabrir
   o caso.

Existe um portão de qualidade no fim: se qualquer item falhar, a skill volta
ao nível correspondente em vez de entregar incompleto.

---

## Onde funciona

| Ambiente | Estudo completo | Arquivos salvos | Scripts |
|---|---|---|---|
| Claude Code (terminal) | sim | sim | sim |
| Claude.ai (web e celular) | sim | entregues no chat | não |

O rigor da investigação e a síntese no chat são **idênticos** nos dois. O que
muda é apenas onde o pacote completo é gravado.

---

## Licença e uso

Livre para usar, estudar, adaptar e instalar quantas vezes quiser.

Se a skill te ajudou a tomar uma decisão melhor, conta pro Rafa — é o
feedback que faz a próxima versão nascer.
