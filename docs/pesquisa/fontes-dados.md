# Fontes de dados para a réplica do Jumba

## 0. O que muda o plano

1. **A B3 proíbe coleta automatizada.** O Hub de Dados Públicos diz, literalmente: *"é expressamente vedada a coleta automatizada, inclusive por meio de ferramentas de inteligência artificial, para quaisquer finalidades, comerciais ou não, próprias ou de terceiros"* ([hub](https://www.b3.com.br/pt_br/dados/hub-de-dados-publicos/)). A página de dividendos traz o mesmo aviso. O Farol já baixa o BDI por robô (`/home/claude/Farol/Python/b3_scraper_linux.py`, linhas 73–84 e 1565–1593). Fica para o Marcelo decidir. As alternativas licenciadas são a ProfitDLL (a Nelogica compra os dados da B3 e revende) e o UP2DATA (pago).
2. **A página "Dados Públicos" saiu do ar em 31/03/2026.** Os arquivos foram para o Boletim Diário do Mercado ([CE 001-2026](https://www.b3.com.br/data/files/24/92/1D/71/773CB9109B5E99B9AC094EA8/CE%20001-2026-VTEC_NOVA%20DATA%20PARA%20DESCONTINUACAO%20DA%20PAGINA%20DE%20DADOS%20PUBLICOS_PT.pdf), [CE 007-2025](https://www.b3.com.br/data/files/28/C7/3A/11/33F7A9105B12E5A9AC094EA8/CE%20007-2025-VTEC%20MELHORIAS%20NO%20ACESSO%20AOS%20DADOS%20NO%20SITE%20B3_PT.pdf)). A página "Ajustes do pregão" acabou em dez/2025. Segundo o manual do pacote rb3, o boletim guarda cerca de 21 pregões ([rb3 manual](https://packages.ropensci.org/rb3/doc/manual.html)).
3. **A ProfitDLL só devolve 30 dias de negócios.** O histórico de negócios é recusado se a data inicial passar de 30 dias (`NL_HISTORY_PERIOD_LIMIT`). Para WIN e WDO, cada janela tem de ser menor que 10 dias (`/home/claude/Farol/SDK/Manual/Manual - ProfitDLL pt_br.pdf`, v4.0.0.42, seção GetHistoryTrades).

**Consequência:** o histórico próprio (OI, Max Pain History, histórico de vol implícita, Trader Flow) só existe se o sistema **gravar uma foto por dia desde já**. Antes disso, a única fonte é COTAHIST (preços, sem OI) ou UP2DATA (pago).

---

## A) B3 pública

| Dado | Onde (URL) | Formato / campos | Frequência | Custo / limites |
|---|---|---|---|---|
| **Posições em aberto (OI) por série** | Boletim: [boletim-diario-do-mercado](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/boletim-diario-do-mercado/). Por API: POST `https://arquivos.b3.com.br/bdi/table/OpenPositionsEquities/{data}/{data}/{pág}/{tam}`, rota usada no Farol (`b3_scraper_linux.py:80,1578`). Consulta em tela: [opções › posições em aberto](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/opcoes/posicoes-em-aberto/) | CSV ([glossário](https://b3.com.br/data/files/1E/D1/BA/58/C841B810E9C1AAA8AC094EA8/DerivativesOpenPositionFile%202023.pdf)): TckrSymb, ISIN, Asst, XprtnCd, OpnIntrst, VartnOpnIntrst, CvrdQty (coberto), UcvrdQty (descoberto), TtlBlckdPos (travado), TtlPos. **Não tem strike.** | Diário, depois do pregão | Gratuito. Cerca de 21 pregões retidos. Coleta automatizada vedada |
| **Cadastro de instrumentos / séries** | Mesma API, rota `InstrumentsDerivatives` (Farol `:82`). Consulta em tela: [séries autorizadas](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/opcoes/series-autorizadas/) | CSV ([glossário 2024](https://b3.com.br/data/files/52/74/1E/14/4BA6D8103152D4C8AC094EA8/Glossario%20InstrumentsConsolidatedFile%202024.pdf)): ExrcPric (strike), XprtnDt, OptnTp (call/put), OptnStyle (americana/europeia), MktNm, UndrlygTckrSymb1 | De manhã, antes da abertura, e à noite | Gratuito. Liga-se ao OI pelo TckrSymb |
| **Negócios consolidados** (OHLC, volume, nº de negócios por série) | Rota `ConsolidatedTradesDerivatives` (Farol `:81`), [glossário](https://www.b3.com.br/data/files/F8/42/7A/61/FEC4A8103234E0A8AC094EA8/TradeInformationConsolidatedFileV3_PT.pdf) | CSV | Diário | Gratuito, cerca de 21 pregões |
| **COTAHIST** | [cotações históricas](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/), [layout](https://www.b3.com.br/data/files/65/50/AD/26/29C8B51095EE46B5790D8AA8/HistoricalQuotations_B3.pdf) | TXT posicional de 245 bytes. Opções: TPMERC 070 (call) e 080 (put), PREEXE (strike), DATVEN (vencimento), CODISI | Anual (o rb3 também cita mensal e diário) | Gratuito, anos de histórico. **Não tem OI.** Traz só o fechamento, sem casamento de horário com o ativo-objeto |
| **Aluguel (BTB): taxas** | "Negócio a negócio – Empréstimo de ativos" ([glossário](https://www.b3.com.br/data/files/A6/C3/43/9D/3941B810E9C1AAA8AC094EA8/Negocio%20a%20Negocio%20-%20Emprestimos%20de%20Ativos%20-%20btb%202023.pdf)) | ZIP `DD-MM-AAAA_NEGOCIOSBTB.zip` com CSV: Simbolo, TaxaDeJurosDoTermoDoNegocio, QuantidadeNegociada, HoraEntrada | No mesmo dia, depois do fechamento | Gratuito. Renovações não entram |
| **Aluguel: posição em aberto** | [glossário](https://b3.com.br/data/files/BF/F1/58/15/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Posicao_Em_Aberto.pdf) | CSV: Ticker, Mercado, saldo em quantidade, preço médio, saldo em R$. **Sem taxa.** | D-1, publicado na abertura | Gratuito |
| **Proventos e eventos corporativos** | [dividendos e eventos](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/acoes/consultas/dividendos-e-outros-eventos-corporativos/), que aponta para `sistemaswebb3-listados.b3.com.br/dividensOtherCorpActPage` | Tela (não confirmei se há download) | Por evento | Gratuito, coleta automatizada vedada |
| **Ajustes de strike** | Não achei arquivo próprio. **Suposição:** dá para obter comparando o ExrcPric do cadastro de um dia para o outro, série a série | — | Diário | — |
| **Participação por tipo de investidor** | PDF do BDI, seção "Participação dos Investidores" ([exemplo](https://arquivos.b3.com.br/bdi/download/bdi/2024-03-21/BDI_02_20240321.pdf)) | Estrangeiro, institucional, instituição financeira, pessoa física e outros. Acumulado no mês e quebra mensal por mercado (vista, termo, opções, exercício, blocos) | Diário (valor acumulado) | Gratuito. **Não há série diária gratuita por tipo de investidor em IND/WIN.** O Farol já chegou a essa conclusão: `/home/claude/Farol/docs/specs/0021-players-indfut/revplayers.txt:32` e `SPEC.md:83`. Há uma amostra paga de 1 dia (`Investor_Category.zip`) |
| **Ajustes de futuros / curva DI** | Ajuste histórico: Pricing Report BVBG.086 em "Pesquisa por pregão". Curva: arquivo "Taxas de Mercado para Swaps" `TS<aammdd>.ex_`, que substituiu a página de Taxas Referenciais (ambos segundo o [rb3](https://packages.ropensci.org/rb3/doc/manual.html)). [Pesquisa por pregão](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/pesquisa-por-pregao/) | `.ex_` autoextraível e XML | Diário | Gratuito. Não consegui confirmar quanto histórico existe (a página devolveu erro ao acesso) |
| **Volatilidade / prêmio** | [descrição dos arquivos](https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/descricao-dos-arquivos/): "Premio" (prêmio de referência de todas as opções), "SupVol" (superfície por delta, para opções flexíveis), "Deltas". Superfície de dólar já coletada pelo Farol (`b3_scraper_linux.py:69`) | Arquivos de pregão | Diário | Gratuito. Para opções de ações **não há vol implícita pronta**: é preciso calcular |
| **UP2DATA (pago)** | [UP2DATA](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/up2data/), [On Demand](https://www.b3.com.br/pt_br/noticias/up2data-on-demand-8AA8D0CC963AC85801963E19F1E219E6.htm), [Política Comercial 2.4.5](https://www.b3.com.br/data/files/44/20/90/B2/E7D5F910CEC024F9AC094EA8/UP2DATA_Politica_Comercial_2.4.5.pdf) | Histórico de fechamento, preço de referência, ajuste, cadastro, intradiário e **open interest** | Sob demanda ou assinatura | Pago, com contrato. Preço não verificado (página de preços inacessível). É o único caminho licenciado para histórico de OI com mais de 21 dias |

---

## B) ProfitDLL (Nelogica)

Evidência: o manual oficial está no repositório, em `/home/claude/Farol/SDK/Manual/Manual - ProfitDLL pt_br.pdf` (v4.0.0.42, 2026-09-04), e a lista de exports em `/home/claude/Farol/Host.Tests/Fixtures/ProfitDLL-4.0.0.42.exports.json`.

| Recurso | Função / callback | Observação |
|---|---|---|
| Negócios em tempo real | `SubscribeTicker` → `TNewTradeCallback` (preço, volume, quantidade, **nBuyAgent, nSellAgent**, nTradeType, bEdit) | nTradeType indica o agressor: 2 = compra agressão, 3 = venda agressão, 4 = leilão, 7 = exercício, 11 = BTC, 13 = RLP. É a base do Trader Flow |
| Nome da corretora | `GetAgentNameLength` + `GetAgentName` (nome completo ou abreviado) | `GetAgentNameByID` está depreciada |
| Histórico de negócios | `GetHistoryTrades(ticker, bolsa, início, fim)` → `THistoryTradeCallback`, que também traz os agentes | **No máximo 30 dias para trás.** WIN/WDO em janelas menores que 10 dias. O [profitdll-wrapper](https://pypi.org/project/profitdll-wrapper/) confirma o limite |
| Book de ofertas | `SubscribeOfferBook` → `TOfferBookCallback`/`V2`, com nAgent por oferta | — |
| Book por preço | `SubscribePriceBook` → `TPriceBookCallback`/`V2` | — |
| Resumo diário | `TNewDailyCallback`: OHLC, **dAjuste**, limites de preço, volume de compradores e vendedores, **nContratosOpen** | **Suposição a testar:** se nContratosOpen vem preenchido por série de opção, a DLL pode substituir o OI da B3 |
| Lista de séries | `SetAssetListInfoCallbackV2`: stSecurityType (6 stOption, 2 stSpotOption, 3 stFutureOption, 17 stOptionOnIndex, 16 stSecurityLoan), strValidDate (vencimento), ISIN, multiplicador, lote | **Não traz campo de strike.** O strike tem de vir do cadastro da B3 (ou de interpretar a descrição, o que é suposição) |
| Ajustes e proventos | `SubscribeAdjustHistory` → `TAdjustHistoryCallbackV2`: valor, tipo, observação, data do ajuste, data da deliberação, data de pagamento, fator multiplicador | Fonte estruturada para "Eventos Corporativos" |
| Preço teórico | `GetTheoreticalValues` e `SetTheoreticalPriceCallback` | É o **preço teórico de leilão**, não grega |
| Gregas / vol implícita | — | **Não existem na DLL.** Cálculo nosso |
| Licença | Erros `NL_NO_LICENSE` e `NL_LICENSE_NOT_ALLOWED` ("Recurso não liberado na licença") | Os recursos dependem do plano. Preço não é público (o [texto da Nelogica no Money Times](https://www.moneytimes.com.br/conteudo-de-marca/a-importancia-de-ter-dados-da-b3-conheca-o-datafeed/) é publicidade e não traz valores). O wrapper avisa que é preciso um processo por sessão: depois de desconectar, não dá para reconectar no mesmo processo |

---

## C) Outras fontes

- **ANBIMA ETTJ:** curva prefixada, IPCA e inflação implícita, parâmetros Svensson, em XLS, CSV, TXT ou XML ([CZ.asp](https://www.anbima.com.br/informacoes/est-termo/CZ.asp)). Há também a versão intradiária das 12h ([curvas intradiárias](https://www.anbima.com.br/informacoes/curvas-intradiarias/default.asp)). A página não traz termos de uso visíveis, e não verifiquei se é gratuita.
- **Tesouro Transparente:** taxas e preços do Tesouro Direto em CSV por CKAN ([metadados](https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/1a8eb2e3-4902-4a38-a1eb-6410f23d90de/download/Taxa.pdf)). Gratuito.
- **CVM dados abertos, IPE:** ZIP anual com índice de Fatos Relevantes e Avisos aos Acionistas, atualizado toda semana, licença ODbL, histórico desde 2003 ([dataset](https://dados.cvm.gov.br/dataset/cia_aberta-doc-ipe)). Serve para conferir proventos. Os documentos não são estruturados.
- **Terceiros com OI:** a [brapi](https://brapi.dev/blog/api-open-interest-opcoes-b3-posicoes-em-aberto) tem OI coberto, descoberto e travado e histórico em JSON (`/api/v2/options/positions`, mas não diz de onde tira os dados). Há também um scraper no Apify ([link](https://apify.com/serj_henrique/b3-boletim-diario-derivativos-posicoes-em-aberto/api)). Ambos servem só como contingência e a licença não é clara.
- **Ferramenta:** o pacote R rb3 ([docs](https://docs.ropensci.org/rb3/articles/Getting-started.html)) é uma boa referência de parsers para COTAHIST, BVBG.086 e TS.

---

## D) Fonte que eu usaria primeiro em cada tipo de tela

| Tela-tipo | 1ª fonte | Complemento / histórico |
|---|---|---|
| Mapa de Opções, Market Gamma, Jumba Walls, Market Exposure, Gamma Bands (Pro e IND/DOL) | OI de D-1 da B3 (`OpenPositionsEquities`) cruzado com o cadastro (strike, tipo, vencimento, estilo). Preços do ativo e das opções **em tempo real pela ProfitDLL**. Gregas calculadas por nós (BSM; Black-76 para IND/DOL) | Teste: nContratosOpen da DLL. Histórico = foto diária gravada no Farol. Para IND/DOL, o OI de opções sobre futuro vem do mesmo arquivo (suposição: segmento de derivativos) |
| Max Pain e Max Pain History | Mesmo par OI + cadastro | O histórico só existe a partir das fotos diárias, ou com UP2DATA |
| PCR | OI de calls e puts (B3) e volume (negócios da ProfitDLL ou consolidado da B3) | COTAHIST para o PCR de volume em anos anteriores (sem OI) |
| Volatilidade e Histórico de Vol Implícita | Cálculo próprio com o meio do book da ProfitDLL, o ativo-objeto e a curva DI | Recuperação do passado com o fechamento do COTAHIST e o arquivo TS (menos preciso, porque os horários não casam). O arquivo "Premio" da B3 serve de conferência |
| Mercados de Aluguel | Negócio a negócio do BTB (taxas) e posição em aberto do BTB (D-1) | ProfitDLL com tradeType 11 ou stSecurityLoan (**suposição**: não sei se a licença inclui o BTB) |
| Eventos Corporativos e Histórico de Ajustes de Strikes | `SubscribeAdjustHistory` da ProfitDLL, mais a comparação diária do ExrcPric no cadastro da B3 | CVM IPE (Avisos aos Acionistas) |
| Fluxo de Investimentos | Seção "Participação dos Investidores" do BDI (acumulado no mês; o fluxo diário sai da diferença entre dias, o que é inferência) | Por tipo de investidor em derivativos, só com fonte paga. Aproximação pelas corretoras via ProfitDLL (Farol spec 0021) |
| Curva de Juros | DI1 em tempo real pela ProfitDLL (último preço e dAjuste) para a curva intradiária | Arquivo TS da B3 ou BVBG.086 para o fechamento oficial. ANBIMA ETTJ para conferir |
| Trader Flow (IND/DOL, TradingView, Beta) | `TNewTradeCallback` com nBuyAgent e nSellAgent, mais o lado agressor; book via Offer/PriceBook | Gravar tudo todo dia: a DLL só volta 30 dias |
| Shark Map e Shark Positions | **Suposição** sobre o que mostram: VartnOpnIntrst por série (B3) mais negócios grandes por corretora (ProfitDLL) | — |
| Gamma Score, IQ, BGT Bands | Metodologias próprias do Jumba, derivadas das bases acima (**suposição**: precisa olhar as telas para definir) | — |
| Find Your Trade (calculadoras, payoff, BSM, Box 3 e 4 pontas, Collar, Venda Coberta, Cash Put) | Cadastro (strike, vencimento, estilo, lote) mais preços da ProfitDLL e taxa DI | Não precisa de outra fonte |

---

## E) Pendências

- Não consegui abrir as páginas de preço do UP2DATA, a "Pesquisa por pregão" (histórico do TS e do BVBG.086), os Termos de Uso da B3 nem `arquivos.b3.com.br/bdi/tabelas`: todas devolveram erro ao acesso. Preços e prazos de retenção ainda estão por confirmar.
- Teste na conta do Marcelo: se nContratosOpen vem preenchido em opções, se a licença libera BTB e opções sobre futuro, e se a lista de ativos inclui todas as séries de opções.
- Decisão do Marcelo: manter o robô de coleta da B3, que conflita com o aviso dela, ou passar a usar só ProfitDLL e UP2DATA.