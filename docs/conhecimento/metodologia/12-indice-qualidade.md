# 12. Índice de Qualidade (IQ): titulares ÷ lançadores

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - Zé da Silva, "O índice de qualidade na venda de opções", Clube do Pai Rico, 07/08/2015 (atualizado em 15/02/2023). Diz: "a divisão do titular pelo lançador"; "Acima de 1 é pó, abaixo, exercício"; dado do "relatório de opções divulgado diariamente pela Bovespa"; exemplos PETRH10 (IQ 0,47) e PETRI8 (375 titulares / 506 lançadores). <https://www.clubedopairico.com.br/o-indice-de-qualidade-na-venda-de-opcoes/22810>
  - Clube do Pai Rico, "Distorções no IQ": <https://www.clubedopairico.com.br/distorcoes-no-indice-de-qualidade-das-opcoes-o-que-isso-significa/39249> (citado na pesquisa anterior; não reaberto hoje).
  - Jumba: IQ de calls e IQ de puts **separados**, em linhas ao longo do tempo com o preço; "Relação Titulares/Lançadores"; "IQ Global dos Papéis". Critério de barreira: "volume descoberto acima de 5 milhões e índice de qualidade (IQ) acima de 1,2" (Telegram 1597). Ver `../jumba-publico/glossario-jumba.md` e `telegram-busca-iq.md`.
  - B3 DerivativesOpenPosition: `BrrwrQty` ("quantidade de tomadores") e `LndrQty` ("quantidade de doadores") são contagens de **clientes** e as candidatas a titulares e lançadores [S]. Ver `../b3-opcoes/02-posicoes-em-aberto.md`.

## 1. Por série [C, fórmula de fonte externa]

$$\text{IQ}_i=\frac{H_i}{W_i}$$

- $H_i$ = número de **titulares** (clientes comprados) da série $i$.
- $W_i$ = número de **lançadores** (clientes vendidos).

**Leitura do autor:**
- $\text{IQ}>1$: muitos titulares pequenos contra poucos lançadores; a opção "tende a virar pó".
- $\text{IQ}<1$: "tende a exercício".
- O próprio autor diz que o índice não é "100 % exato" e deve ser lido junto com a venda descoberta do strike.

**Atenção à unidade:** $H$ e $W$ são **pessoas** (contagens), não quantidade de opções. Por isso o IQ não tem relação direta com o OI.

## 2. Agregações (a da Jumba não é pública)

| Nome | Fórmula | Observação |
|---|---|---|
| IQ do ativo por tipo, razão de somas [P padrão] | $\text{IQ}^{call}_{ativo}=\dfrac{\sum_{i\in calls}H_i}{\sum_{i\in calls}W_i}$ (idem para puts) | um cliente com posição em várias séries é contado várias vezes [I]. É o que bate com "IQ das CALLs" e "IQ das PUTs" separados [C Telegram 563] |
| IQ ponderado por OI | $\dfrac{\sum_iOI_i\,\text{IQ}_i}{\sum_iOI_i}$ | dá peso às séries grandes; sensível a séries com $W_i$ pequeno |
| IQ ponderado por descoberto | $\dfrac{\sum_iUcvrdQty_i\,\text{IQ}_i}{\sum_iUcvrdQty_i}$ | foca no que pode gerar exercício |
| IQ Global dos Papéis | razão de somas sobre todos os ativos do universo, por tipo | [I] só o nome é público |

**Filtros [P]:** vencimento (próximo ou todos) e faixa de strike ($|K/S-1|\le h$). Séries com $W_i=0$ ficam fora e recebem a flag `SEM_LANCADOR`.

## 3. Barreiras do Mapa (usa o IQ)

Critério observado na Jumba [C, um exemplo]: strike com $UcvrdQty>5\times10^6$ e $\text{IQ}>1{,}2$.

Proposta para o scanner [P]:

$$\mathcal B=\{i:\ UcvrdQty_i\ge Q_{\min},\ \text{IQ}_i\ge\text{IQ}_{\min},\ |K_i/S-1|\le h\}$$

Padrões: $Q_{\min}$ = 5 milhões (ou um percentil do ativo), $\text{IQ}_{\min}$ = 1,2 e $h$ = 10 %.

## 4. Dependência de dado (bloqueante)

- O IQ só existe se a B3 publicar as **contagens** de titulares e lançadores por série.
- O teste está em `../b3-opcoes/00-indice.md` (passo 2): numa linha de opção de PETR4, conferir se `BrrwrQty` e `LndrQty` vêm preenchidos e são muito menores que `OpnIntrst`.
- Se não vierem, o IQ fica **sem fonte**. A ProfitDLL não traz essas contagens.
