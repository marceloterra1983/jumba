# 03. Empréstimo de ativos (BTB): taxas doadora e tomadora, negócios e posições

Acesso: 2026-11-04. Legenda: [C] B3 lido; [T] terceiros; [S] suposição.

**Novidade:** o critic.md dizia que nenhuma fonte trazia as taxas doadora e tomadora. Elas estão no arquivo **"Empréstimos registrados"** do BDI.

## A. Empréstimos registrados: taxas doadora e tomadora (fonte principal)

| Item | Valor |
|---|---|
| Glossário | [Glossario _ Emprestimos_Registrados.pdf](https://b3.com.br/data/files/32/02/C0/25/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Emprestimos_Registrados.pdf): v1 de 05/09/2023, v2 de 22/02/2024 [C] |
| Onde | Boletim Diário do Mercado (BDI), seção **Clearing**, tabela "Empréstimos registrados". Arquivo "Empréstimos de Ativos – Empréstimos Registrados-DD-MM-AAAA" [C]. Também no Secure Client (ARQ.SI.002) e no UP2DATA ([CE 068/2024-VNC](https://b3.com.br/data/files/83/F5/96/95/522239106EEC8429AC094EA8/CE%20068-2024-VNC%20Metodologia_taxaBTB_PT.pdf)) [C] |
| Formato | CSV [C] |
| Horário | Diário, **na abertura, com dado de D-1** [C] |
| Histórico | O BDI aceita consulta por período (aparece a coluna `Data`) [C]. A retenção não foi medida. O BDI em geral guarda cerca de 21 pregões [T] |
| Cobertura | Mercados Registro, Neg. Eletrônica D+0, Neg. Eletrônica D+1 e ETF de Renda Fixa. **Inclui renovações manuais** [C] |
| Taxa média | Desde 18/11/2024, "ponderação de todos os negócios e renovações do dia", **sem filtro de outliers** (CE 068/2024). O glossário ainda fala em MTO [C] |
| Rota BDI | Não confirmada [S]. Achar em `#selectTabelas` |

**Campos (PT / EN):**

| Campo (PT) | Campo (EN) |
|---|---|
| Data | Date (só em consulta por período) |
| Ticker | Ticker |
| ISIN | ISIN |
| Empresa ou Fundo | Company or Fund |
| Mercado | Market |
| Número de Contratos | Number of Contracts |
| Quantidade de Ativos | Asset Amount |
| Valor em R$ | Value in BRL |
| **Taxa Mínima doador** | Minimum Rate Donor |
| **Taxa Média ponderada doador** | Average Rate Donor |
| **Taxa Máxima doador** | Maximum Rate Donor |
| **Taxa Mínima tomador** | Minimum Rate Taker |
| **Taxa Média ponderada tomador** | Average Rate Taker |
| **Taxa Máxima tomador** | Maximum Rate Taker |

É o equivalente da antiga `LoanBalance` (`DnrMinRate`… `TakrMaxRate`), que saiu do ar com a página Dados Públicos em 31/03/2026 [T: `../b3-opcoes/raw/b3-open-data-1.0.4/meta.py`].

## B. Negócio a negócio do BTB

| Item | Valor |
|---|---|
| Glossário | [Negocio a Negocio - Emprestimos de Ativos - btb 2023.pdf](https://b3.com.br/data/files/A6/C3/43/9D/3941B810E9C1AAA8AC094EA8/Negocio%20a%20Negocio%20-%20Emprestimos%20de%20Ativos%20-%20btb%202023.pdf): v2.1 de out/2023 [C] |
| Arquivo | `DD-MM-AAAA_NEGOCIOSBTB.zip` (BTBTradeIntradayFile), com CSV dentro [C] |
| Horário | No próprio dia, ao final [C] |
| Limitação | **Não inclui renovações** [C] |

**Campos:**

| # | Campo | Conteúdo |
|---|---|---|
| 1 | ReportDate | Data do relatório |
| 2 | TickerSymbol | Código do ativo |
| 3 | UpdateAction | 0 = novo, 2 = cancelado |
| 4 | InterestRateTermTrade | Taxa do negócio, **em decimal** (1% = 0,01) |
| 5 | TradeQuantity | Quantidade |
| 6 | EntryTime | Hora, `HHMMSSNNN`, UTC-3 |
| 7 | TradeIdentification | Número do negócio |
| 8 | TradeDate | Data do pregão |
| 9 | TradingSessionIdentification | 1 = sessão regular, 6 = after-hours |
| 10 | Market | 10 = vista, 30 = termo, 70 = opção de compra, 80 = opção de venda… |
| 11 | LenderParticipantCode | Código do participante doador |
| 12 | BorrowerParticipantCode | Código do participante tomador |

**Uso:** distribuição intradiária das taxas e quais corretoras doam e tomam. As taxas deste arquivo não vêm separadas em doadora e tomadora: a taxa é do negócio.

## C. Posição em aberto do BTB

- **Glossário:** [Glossario _ Posicao_Em_Aberto.pdf](https://b3.com.br/data/files/BF/F1/58/15/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Posicao_Em_Aberto.pdf), v1 de 05/09/2023 [C, lido pela nota irmã `../b3-opcoes/02-posicoes-em-aberto.md`].
- **Arquivo:** "Empréstimos de Ativos – Posição em Aberto-DD-MM-AAAA", CSV, na abertura, com D-1.
- **Campos:** Data, Ticker, ISIN, Empresa ou Fundo, Tipo, Mercado, Saldo em quantidade, Preço Médio, Saldo em R$. **Não traz taxa.**
- **Rota BDI:** `BTBLendingOpenPosition` [T: filings-b3].

## Montagem da tela "Mercados de Aluguel"

| Tela | Fonte |
|---|---|
| Taxa doadora e tomadora do dia (mín./média/máx.) | A |
| Volume alugado no dia | A (contratos, quantidade, R$) |
| Saldo alugado (estoque) | C |
| Saldo em % do free float | C ÷ free float. O free float vem de "Ações › capital social" no Hub [S] |
| Histórico | Gravar A e C todo dia. O BDI guarda pouco [T] |
| Taxa intradiária e contrapartes | B |

## Limitações

- Nenhum CSV foi baixado: o proxy bloqueia a B3.
- Retenção e nome da rota do BDI não confirmados.
- Termos da B3 vedam coleta automatizada. O Marcelo decidiu seguir com o scraper.
