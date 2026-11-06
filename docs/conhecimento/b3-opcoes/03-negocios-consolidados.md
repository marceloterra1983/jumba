# 03. Negócios consolidados (OHLC, volume, nº de negócios por série)

Acesso: 2026-11-04. Legenda: **[C]** documento da B3; **[T]** código de terceiros; **[S]** suposição a testar.

| Forma | URL ou padrão | Formato | Histórico |
|---|---|---|---|
| A. TradeInformationConsolidated (V3) | Antes: Dados Públicos (`TradeInformationConsolidated_AAAAMMDD`). Hoje: BDI "Negócios consolidados do pregão" | ZIP com CSV [C] | BDI: cerca de 21 pregões [T] |
| B. BDI, rota `ConsolidatedTradesDerivatives` | `POST https://arquivos.b3.com.br/bdi/table/ConsolidatedTradesDerivatives/{d}/{d}/{pág}/{tam}`, ou exportação CSV (nota 07) | JSON ou CSV | cerca de 21 pregões |
| C. **BVBG.086.01 Pricing Report** | `https://www.b3.com.br/pesquisapregao/download?filelist=PR{aammdd}.zip` [T: rb3 `b3-bvbg-086.yaml`] | ZIP com XML. Pode trazer mais de um arquivo: use o mais novo | Pesquisa por pregão; o rb3 indica este arquivo para "dados mais antigos" que os 21 pregões do BDI [T] |

## A. TradeInformationConsolidatedFile V3

- Fonte: [TradeInformationConsolidatedFileV3_PT.pdf](https://www.b3.com.br/data/files/F8/42/7A/61/FEC4A8103234E0A8AC094EA8/TradeInformationConsolidatedFileV3_PT.pdf), v3 de 15/05/2023 [C]. Mudanças: v2 (out/2022) incluiu OscnPctg e NtlFinVol; v3 (mai/2023) mudou o layout.
- Publicação: "todos os dias pela noite" [C]. Cobre só a Sessão Regular. Há um arquivo separado para after-market.
- Séries sem negócio: o glossário não diz [C]. Pela natureza do arquivo, devem vir só as que negociaram [S]. Por isso a vol implícita de séries sem negócio vem do Prêmio de Referência (nota 05).

| # | Tag | Tipo | Significado |
|---|---|---|---|
| 1 | RptDt | data DD/MM/AAAA | Data de referência |
| 2 | **TckrSymb** | texto | Ticker (**chave**) |
| 3 | ISIN | texto | ISIN |
| 4 | SgmtNm | texto | Segmento |
| 5 | MinPric | número | Mínimo |
| 6 | MaxPric | número | Máximo |
| 7 | TradAvrgPric | número | Preço médio |
| 8 | LastPric | número | Fechamento (último) |
| 9 | OscnPctg | número | Oscilação % |
| 10 | AdjstdQt | número | Ajuste (futuros e opções com ajuste) |
| 11 | AdjstdQtTax | número | Ajuste em taxa |
| 12 | RefPric | número | Preço de referência |
| 13 | TradQty | número | **Nº de negócios** |
| 14 | FinInstrmQty | número | **Contratos negociados** |
| 15 | NtlFinVol | número (R$) | Volume financeiro |

**Não tem abertura (`FrstPric`) nem melhor oferta.** O BVBG.086 tem as duas.

## B. BDI `ConsolidatedTradesDerivatives`

- Exportação CSV (rb3, `raw/rb3-github/downloaders.R`):
  - `POST https://arquivos.b3.com.br/bdi/table/export/csv?lang=en-us`
  - corpo JSON: `{"Name":"ConsolidatedTradesDerivatives","Date":"AAAA-MM-DD","FinalDate":"AAAA-MM-DD"}` [T]
- O CSV em inglês tem linhas de preâmbulo. O cabeçalho começa em `Ticker symbol`, com separador `;` e `-` como vazio. Colunas citadas: `Adjusted quote`, `Previous adjusted quote tax` (rótulo trocado: guarda o ajuste anterior), `Variation` e `Settlement value per contract (R$)` [T: `raw/rb3-github/readers.R`].
- Farol: `ConsolidatedTradesDerivatives@true`, cerca de 780 KB, limiar de 50.000 bytes.
- **Em aberto [S]:** se a rota inclui opções de ações ou só derivativos BM&F. Deve existir uma rota irmã para ações; o nome não foi confirmado.

## C. BVBG.086.01 Pricing Report (campos do rb3)

Fonte: `raw/rb3-github/b3-bvbg-086.yaml` [T]. A descrição consta na [descrição dos arquivos](https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/descricao-dos-arquivos/) [C].

| Tag XML | Significado |
|---|---|
| Dt | Data |
| **TckrSymb** | Ticker (**chave**) |
| Id / Prtry / MktIdrCd | SecurityID / 8 / BVMF (`FinInstrmId`) |
| NtlFinVol | Volume financeiro |
| **OpnIntrst** | **Posições em aberto** (total, sem quebra) |
| FinInstrmQty | Contratos negociados |
| BestAskPric / BestBidPric | Melhor venda / melhor compra no fechamento |
| FrstPric / MinPric / MaxPric / LastPric / TradAvrgPric | Abertura, mínimo, máximo, fechamento e médio |
| RglrTxsQty / RglrTraddCtrcts / NtlRglrVol | Negócios, contratos e volume no horário regular |
| NonRglrTxsQty / NonRglrTraddCtrcts / NtlNonRglrVol | O mesmo fora do horário regular |
| OscnPctg | Oscilação |
| AdjstdQt / AdjstdQtTax / PrvsAdjstdQt / PrvsAdjstdQtTax | Ajuste atual e anterior (futuros) |
| VartnPts / AdjstdValCtrct | Variação em pontos / valor do ajuste |
| DaysToSttlm / TradQty | Dias para liquidação / quantidade negociada |

- Liga-se ao BVBG.028 pelo `FinInstrmId/OthrId/Id` (SecurityID) ou pelo `TckrSymb`.
- Se `OpnIntrst` vem preenchido para **opções de ações** não está confirmado [S].

## Traz?

| Strike | Vencimento | Tipo | Estilo | Coberto/travado/descoberto | Titulares/lançadores |
|---|---|---|---|---|---|
| não | não | não | não | não | não |

Todos se ligam ao cadastro pelo `TckrSymb`.
