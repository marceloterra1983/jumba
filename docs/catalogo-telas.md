# Catálogo das telas do sistema de opções da B3

- **Data:** 05/11/2026. Revisado no mesmo dia; as mudanças e os pontos em que a revisão se afastou das propostas estão em "Notas da revisão", no fim.
- **Branch lido:** `claude/project-thread-ugulea` no commit `5fecc33`, comparado com `origin/main` em `827a577`.
- **Motor:** `src/Web/Farol.Portal/Modules/Options/` (namespace `Farol.Portal.Options`, SPEC-0524).
- **Base diária:** esquema `b3_daily_v1` da História, escrito só pelo DataHub (SPEC-0523).
- **Vetores:** `tests/fixtures/opcoes/` (`precificacao.json`, `agregados.json`, `feriados-b3-2026-2028.json`).

Este catálogo é nosso. O menu, os nomes de tela e os critérios próprios foram escritos aqui, e a revisão de 05/11/2026 tirou os nomes, os conceitos e a divisão de telas que ainda seguiam notas de metodologia marcadas [Q]. As fórmulas vêm de fontes públicas aceitas (B3, ANBIMA, Hull, Haug, artigos acadêmicos e documentação oficial de bolsa), citadas em cada tela pela chave da seção Referências. Nenhum material em quarentena foi aberto, e os trechos marcados [Q] nas notas de metodologia não servem de fonte. Onde não há fonte aceita, o critério é declarado como nosso.

## Resumo

1. O catálogo descreve 37 telas próprias em 6 temas, cada uma com definição, fórmula, referência pública, dado de entrada, arquivo da B3, função do motor, escolhas em aberto e status. O objeto (ação ou ETF, Ibovespa, dólar) é um seletor comum a todas as telas, e o modelo de cada objeto sai da regra da §7.
2. O branch já traz a importação offline da base diária pública (cadastro, posições, prêmios, negócios e taxas) e o motor de calendário, curva DI, BSM-Merton, Black-76, gregas, vol implícita e SVI. Nenhuma tela existe ainda. O branch também não liga a opção ao objeto: o cadastro guarda o SecurityID do objeto, mas esse id não aponta para nenhum registro da base, e o preço do objeto não sai dela.
3. Só a calculadora de opção (ES-01), com entradas digitadas, tem motor pronto e espera apenas a página, e isso vale para BSM e Black-76: o Garman-Kohlhagen ainda não tem o rho estrangeiro nem a conversão do cupom. A grade de séries, a conferência com o prêmio da B3 e a curva pré DI dependem também da leitura da base pelo Portal (A5), e a grade e a conferência dependem ainda da ligação opção → objeto.
4. As demais esperam o motor de agregados e exposições (backlog B2), a leitura da base pelo Portal (A5), a ligação opção → objeto, o book executável ou dado que a B3 não publica. Os históricos só existem com a gravação diária, porque o BDI guarda cerca de 21 pregões, e essa gravação (A2 e A3) está parada: a B3 veda coleta automatizada, e a escolha da fonte depende do cartão de 05/11, que segue aberto.
5. As convenções que mudam números ficam como parâmetro, com um padrão proposto, e estão listadas no fim para decisão do Marcelo.

## Índice

| Tema | Código | Tela | Status |
|---|---|---|---|
| Cadeia e posição em aberto | OP-01 | Grade de séries | Dado pronto no branch, mas falta ligação opção → objeto; motor pronto; falta tela |
| Cadeia e posição em aberto | OP-09 | Histórico de uma série | Bloqueada por decisão pendente da fonte (base acumulada); falta motor; falta tela |
| Cadeia e posição em aberto | OP-10 | Atividade do dia | Dado pronto no branch para as séries (variação e razão volume/OI em duas datas; por objeto, falta ligação opção → objeto); falta motor; falta tela |
| Cadeia e posição em aberto | OP-02 | Posição por strike | Dado pronto no branch (o filtro perto do preço depende da ligação opção → objeto); falta motor; falta tela |
| Cadeia e posição em aberto | OP-03 | Resumo por vencimento | Dado pronto no branch (vol ATM, GEX e intervalo implícito dependem da ligação opção → objeto); falta motor; falta tela |
| Cadeia e posição em aberto | OP-05 | Razão put/call | Dado pronto no branch; falta motor; falta tela |
| Cadeia e posição em aberto | OP-06 | Dor máxima do vencimento | Dado pronto no branch; falta motor; falta tela |
| Cadeia e posição em aberto | OP-07 | Dor máxima no tempo | Bloqueada por decisão pendente da fonte (base acumulada); falta motor; falta tela |
| Cadeia e posição em aberto | OP-08 | Índice titulares/lançadores | Dado pronto no branch (leitura dos campos a confirmar); falta motor; falta tela |
| Gamma e exposição | GX-01 | Exposição gamma por strike | Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela |
| Gamma e exposição | GX-02 | Preço de gamma zero | Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela |
| Gamma e exposição | GX-05 | Exposição delta por strike | Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela |
| Gamma e exposição | GX-06 | Exposição perto do dinheiro no tempo | Bloqueada por decisão pendente da fonte (base acumulada); falta motor; falta tela |
| Gamma e exposição | GX-07 | Exposição de vanna e charm | Dado pronto no branch, mas falta ligação opção → objeto; falta motor (gregas de 2ª ordem); falta tela |
| Volatilidade | VL-01 | Sorriso por vencimento | Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela |
| Volatilidade | VL-06 | Densidade neutra ao risco (aba da VL-01) | Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela |
| Volatilidade | VL-02 | Superfície e estrutura a termo | Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela |
| Volatilidade | VL-05 | Intervalo implícito até o vencimento | Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela |
| Volatilidade | VL-03 | Vol implícita no tempo | Bloqueada por decisão pendente da fonte (histórico); falta leitor do COTAHIST anual; falta motor; falta tela |
| Volatilidade | VL-07 | Vol implícita entre objetos | Bloqueada por decisão pendente da fonte (histórico); falta ligação opção → objeto; falta motor; falta tela |
| Volatilidade | VL-08 | Cone de volatilidade | Falta dado (leitor do COTAHIST anual); falta motor; falta tela |
| Volatilidade | VL-04 | Conferência com o prêmio de referência da B3 | Dado pronto no branch, mas falta ligação opção → objeto; motor pronto; falta tela |
| Fluxo | FL-01 | Variação da posição em aberto | Bloqueada por decisão pendente da fonte (duas datas seguidas); falta motor; falta tela |
| Fluxo | FL-02 | Fluxo por grupo de corretoras | Dado pronto na main para objeto e futuros; dado parcial de opções na main (SPEC-0078, só séries dos Sinais), falta ampliar o universo; falta motor; falta tela |
| Fluxo | FL-03 | Negócios grandes | Dado pronto na main para objeto e futuros; dado parcial de opções na main (SPEC-0078, só séries dos Sinais), falta ampliar o universo; falta motor; falta tela |
| Fluxo | FL-05 | Participação por tipo de investidor | Falta dado; falta motor; falta tela |
| Juros e eventos | JE-01 | Curva pré DI | Dado pronto no branch (duas datas para a comparação com o pregão anterior); motor pronto; falta tela |
| Juros e eventos | JE-02 | Calendário de pregões e vencimentos | Motor pronto no branch; falta dado (calendário como configuração; `WrkgDays` e `WdrwlDays` não importados); falta tela |
| Juros e eventos | JE-03 | Proventos e eventos corporativos | Falta dado; falta motor; falta tela |
| Juros e eventos | JE-04 | Ajustes de strike por série | Bloqueada por decisão pendente da fonte (duas datas seguidas); falta motor; falta tela |
| Juros e eventos | JE-05 | Aluguel de ações | Falta dado; falta motor; falta tela |
| Estruturas | ES-01 | Calculadora de opção | Dado digitado; motor pronto no branch para BSM e Black-76, parcial para Garman-Kohlhagen; falta tela |
| Estruturas | ES-02 | Payoff de uma posição | Dado digitado ou da grade (OP-01); motor parcial; falta tela |
| Estruturas | ES-03 | Payoff de estruturas | Dado da grade (OP-01); motor parcial; falta tela |
| Estruturas | ES-04 | Gregas da estrutura (delta estrutural) | Dado digitado ou da grade (OP-01); motor parcial; falta tela |
| Estruturas | ES-05 | Buscador de estruturas de renda | Falta dado (bid/ask); falta motor; falta tela |
| Estruturas | ES-10 | Estruturas salvas | Dado do próprio usuário; falta motor (armazenamento); falta tela |

Total: 37 telas (Cadeia e posição em aberto 9, Gamma e exposição 5, Volatilidade 8, Fluxo 4, Juros e eventos 5, Estruturas 6). A ordem do índice segue a dependência entre as telas, e não o número. Os códigos não foram renumerados, para não quebrar as referências: OP-04 virou filtro da OP-02; GX-03 e GX-04 viraram camada e coluna da GX-01; FL-04 virou JE-05; ES-06 a ES-09 entraram na ES-05; ID-01 a ID-04 viraram a regra do objeto da §7. Os códigos novos são OP-09, OP-10, VL-05 a VL-08 e JE-05.

## Como ler o status

- Cada tela tem três camadas. **Dado:** o arquivo público chega e o DataHub o importa. **Motor:** a função pura existe em `Modules/Options/`. **Tela:** a página existe no Portal.
- "Pronto no branch" quer dizer que a camada existe no branch. "Falta dado", "falta motor" e "falta tela" querem dizer que ela não existe.
- Nenhuma tela existe no branch, porque a SPEC-0524 deixou interface e rotas HTTP fora do escopo. Por isso toda linha diz "falta tela".
- "Dado pronto no branch" quer dizer que a importação offline da SPEC-0523 cobre o arquivo. Três peças faltam para todas essas telas e não se repetem em cada linha: a leitura da base pelo Portal, por data e objeto (backlog A5); a ligação opção → objeto, descrita logo abaixo; e a coleta diária automática (A3), parada até a decisão da fonte.
- **Ligação opção → objeto.** O IN traz o objeto como SecurityID (`UndrlygInstrmId`), mas `B3InstrumentFile.Parse` só lê os blocos `OptnOnEqtsInf`, `OptnOnSpotAndFutrsInf` e `FutrCtrctsInf`: descarta o bloco `EqtyInf`, onde estão as ações, e não grava o `FinInstrmId` do próprio instrumento. Por isso `underlying_id` aponta para um id que não existe na base; na fixture, BBSEW441 e BBSEX404 apontam para 200003011956. O COTAHIST traz o ISIN do objeto na linha da opção (`CODISI` = BRBBSEACNOR5 na BBSEX404), mas o leitor não guarda esse campo, e `asset` = 'BBSE' não distingue a classe da ação. Sem a ligação, o preço do objeto não sai da base, e toda coluna que usa S (preço, gregas, vol implícita, moneyness e distância ao preço) fica sem entrada. A correção aditiva é gravar no IN o `FinInstrmId` e o bloco `EqtyInf`, o que cobre todas as séries, ou guardar o `CODISI` do COTAHIST, o que cobre só as séries negociadas no dia. No Ibovespa nem isso basta, porque o nível do índice não está no COTAHIST (§7).
- "Falta ligação opção → objeto", na linha do índice, marca as telas em que o dado existe, mas S não sai da base.
- "Bloqueada por decisão pendente da fonte" quer dizer que a tela precisa da base acumulada ou de dois pregões seguidos, e a gravação diária (A2 e A3) está parada desde que se viu que a B3 veda coleta automatizada. A fonte (UP2DATA da B3, ProfitDLL, download à mão ou assumir o risco) depende do cartão de 05/11, que segue aberto.
- "Dado parcial na main" quer dizer que a main já grava parte do dado (ver FL-02).
- "Motor parcial" quer dizer que a função de preço ou de grega existe, mas falta a agregação que a tela usa.
- "Duas datas" quer dizer que a tela compara D com D−1 e precisa de dois pregões importados seguidos. Enquanto a coleta diária estiver parada, dois pregões seguidos só existem por download à mão.

## Regras que valem para todas as telas

**Invariantes do repositório**

- Só o DataHub escreve a História. As telas só leem, pela Concessão ou pelas consultas do DataHub. Nenhuma tela grava na base diária.
- Nenhuma tela chega ao caminho de ordens. Buscadores, payoff e estruturas salvas são cálculo e registro, sem botão nem chamada que leve ao envio de Ordem. Os testes `NoOrderCallerTests` e `LiveOrderPathGuardTests` continuam valendo.
- A Fita congelada (ADR-0040) não muda. As telas de fluxo leem a Fita gravada; nenhuma mexe na ingestão.
- A ProfitDLL só é carregada pelo Host. Preço ao vivo e book chegam pelo Gateway (`MarketData.Subscribe`, até 256 assinaturas por identidade), nunca pela DLL direto.
- Preços ficam em decimal na base e na exibição. A conversão para `double` acontece só na entrada do motor, que calcula em `double` (SPEC-0524), e o arredondamento só na exibição.
- Ausência de prêmio é ausência. A tela mostra "sem prêmio", não calcula vol implícita e nunca preenche zero.

**Convenções comuns (padrão proposto; as que estão em aberto voltam no fim)**

- **Objeto:** escolhido num seletor comum a todas as telas (ação ou ETF, Ibovespa, dólar). O modelo, o multiplicador, o forward e a grade do perfil gamma saem da regra do objeto (§7). As diferenças entre objetos ficam na regra, e não em telas separadas.
- **Strike:** o vigente no cadastro do dia, já ajustado por proventos.
- **Posição em aberto (OI):** a do último arquivo publicado (D−1), fixa durante o pregão, porque a B3 publica uma vez por dia.
- **Qual campo é o OI da série:** `open_interest` (`OpnIntrst`) quando vem preenchido; senão `total` (`TtlPos`). Na amostra real de 03/11/2026, a put BBSEW441 veio com `OpnIntrst` nulo e com 0 + 230.600 + 63.700 = 294.300 = `TtlPos` (coberto + travado + descoberto). A call de dólar DOLN27C005300 veio com `OpnIntrst` = 280 e a quebra nula. Falta conferir com mais linhas.
- **Prazo:** `T = DU/252`, com DU pelo calendário de pregões da B3 até o vencimento da opção [MA §1.1]. A curva DI conta dias úteis pelo calendário ANBIMA [MC]. São dois calendários (ver JE-02). O IN traz os dois DU oficiais (`WrkgDays` e `WdrwlDays`) dos futuros e das opções sobre disponível e sobre futuro, mas o branch não os importa.
- **Taxa:** `r = −ln(DF)/T`, com `DF` da curva pré no vértice do vencimento; para uma taxa só, `r = ln(1 + DI)` [MA §1.1].
- **Modelo:** opção de ação ou ETF protegida usa Black-Scholes sem dividendo (q = 0), como a B3 [MA §1.1]. Ibovespa e dólar seguem a regra do objeto (§7). As fórmulas são europeias; uma call americana recebe a marca "americana, fórmula europeia".
- **Escalas das gregas:** o motor devolve theta por ano e vega e rho por variação de 1,00. A tela divide theta por 252 (por DU) e vega e rho por 100 (por ponto percentual).
- **Multiplicador:** sempre do cadastro. O DOL traz `CtrctMltplr` = 50, com prêmio por US$ 1.000. As opções de ações e de IBOV vêm sem `CtrctMltplr`; nelas o valor por opção é o prêmio dividido pelo `PricFctr` do IN, que é igual ao `FATCOT` do COTAHIST: 1 nas opções de ações (m = 1) e 100 no IBOV (m = R$ 0,01 por ponto, confirmado; ver §7). O branch não importa `PricFctr` nem `FATCOT`, então nenhum desses dois valores está na base.
- **Sinal das exposições:** convenção A (formador comprado em calls e vendido em puts: +1 nas calls, −1 nas puts), hipótese nossa e declarada, porque a B3 não publica a posição dos formadores. Os programas de formador de opções da B3 [FM] limitam as séries em que a hipótese faz sentido: nas opções de ações, a atuação obrigatória vale para 2 vencimentos (no 4º dia útil antes do 1º, ela passa para os 2 seguintes); nas opções de índice, para os 6 primeiros; e o formador atua pelo menos 10 minutos dentro dos 30 minutos finais do pregão, com spread e quantidade mínima da planilha de parâmetros. [BB], [BDLM21] e [NPPW21] estudam o efeito do hedge dos formadores no preço. Qualquer calibração de sinal é feita só contra dado próprio, nunca contra tela de terceiros.
- **Unidade das exposições:** R$ de delta por movimento de 1 % no objeto (`S² · 0,01`; `F²` nas opções sobre futuro). Num movimento `dS = 0,01·S`, o delta muda `Γ · 0,01·S` unidades do objeto, que valem `Γ · 0,01·S²` em R$. A derivação é nossa, a partir da definição de gamma [HULL cap. 19].
- **Vol da B3:** o arquivo PE traz a vol em pontos percentuais (29,24 quer dizer 29,24 %). A tela divide por 100 antes de comparar.

## Dados: arquivo público, tabela do branch e telas

| Arquivo público | O que o branch importa | Tabela em `b3_daily_v1` | Telas |
|---|---|---|---|
| IN (BVBG.028, cadastro de instrumentos) [CAD] | Strike vigente, vencimento, tipo, estilo, protegida, multiplicador (`CtrctMltplr`, `AsstQtnQty`), datas de negociação e o SecurityID do objeto (`UndrlygInstrmId`), das opções (`OptnOnEqtsInf`, `OptnOnSpotAndFutrsInf`) e dos futuros IND, DOL e DI1 (`FutrCtrctsInf`). Não importa o bloco `EqtyInf` (ações), o `FinInstrmId` de cada instrumento, `PrmUpfrntInd` (prêmio à vista), `SrsTp`, `TrgtInstrmId`, `AllcnRndLot`, `PricFctr`, `WrkgDays` nem `WdrwlDays` | `instruments` | todas as de opções |
| BDI `OpenPositionsEquities` (posições em aberto) [DOP] | Coberto, travado, descoberto, total, nº de tomadores e de doadores (clientes), OI e `DstrbtnId`. A tabela é única por (ticker, `distribution_id`), e não por ticker | `positions` | OP-02 a OP-10, GX, FL-01 |
| PE (prêmio de referência de opções de ações e índice) [PR; WS16] | Prêmio e vol implícita da B3 de todas as séries, inclusive sem negócio. A vol fica só em `premiums.volatility` | `premiums` (`source = PE`) | OP-01, OP-09, VL, GX (vol da foto) |
| RE (`Premio.txt`, prêmio de referência do segmento BM&F) [PR] | Prêmio das opções de derivativos (DOL e outras), com escala própria | `premiums` (`source = RE`) | regra do dólar (§7) |
| COTAHIST diário [COT] | Abertura, máxima, mínima, médio, último, negócios, quantidade e financeiro. Não importa `PREOFC`, `PREOFV`, `PREEXE`, `DATVEN`, `FATCOT` nem `CODISI` (ISIN do objeto na linha da opção) | `trades` (`source = COTAHIST`) | OP-01, OP-05, OP-10, VL-03, VL-08 |
| BDI `ConsolidatedTradesDerivatives` | Negócios agregados de derivativos, ajuste e taxa de ajuste (DI1) | `trades` (`source = BDI`) | JE-01, §7 |
| TS (`TaxaSwap`, taxas de mercado para swaps) [PR] | Curva PRE e outras, sete casas, dias corridos e saques | `swap_rates` | JE-01, todas que descontam |
| Junção cadastro com prêmio | Cadastro com o valor (`premium`) e a fonte (`premium_source`) do prêmio PE ou RE do dia. A visão não traz a vol do PE | visão `series` | OP-01, VL |
| IR (BVBG.087, Index Report) [PR] | Nível do Ibovespa; o conteúdo só foi visto em código de terceiros [T] | não importado | regra do Ibovespa (§7) |
| `Deltas` (Pesquisa por pregão) [PR] | Deltas de opções padronizadas usados nos limites de posição; só o nome foi confirmado | não importado | VL-04 (a confirmar) |
| DI over (Boletim Diário do Mercado) [CDI] | CDI diário, com o dado de D−1 | não importado | JE-01, ES-05 |
| Planilhas dos programas de formador de opções [FM] | Ativos e parâmetros de cada programa; as planilhas não foram lidas | não importado | OP-01, GX-01 |

**O que a base do branch ainda não traz:** BVBG.086 (PR); a coluna `VartnOpnIntrst`; os campos `PREOFC`, `PREOFV`, `PREEXE`, `DATVEN`, `FATCOT` e `CODISI` do COTAHIST; o COTAHIST anual (o leitor exige a data do pregão em cada linha); no IN, o bloco `EqtyInf` e os campos `FinInstrmId`, `PrmUpfrntInd`, `SrsTp`, `TrgtInstrmId`, `AllcnRndLot`, `PricFctr`, `WrkgDays` e `WdrwlDays`; a vol do PE na visão `series`; o nível do Ibovespa (BVBG.087); o CDI diário; o arquivo `Deltas`; empréstimos registrados e saldo do BTB; participação de investidores (BDI_02, PDF); proventos.

**O que vem de fora da B3:** preço ao vivo, book e negócios com corretora chegam da ProfitDLL, pelo Host e pelo Gateway, e a Fita gravada fica no DataHub, com as colunas `buy_agent`, `sell_agent` e `aggressor`. A coluna `aggressor` não é corretora nem lado binário: é o `TTradeType` da ProfitDLL copiado sem conversão (1 cruzado, 2 comprador agressor, 3 vendedor agressor, 4 leilão, 5 vigilância, 13 RLP, 32 desconhecido) [IPC]. Com 2, a corretora agressora é `buy_agent`; com 3, é `sell_agent` (regra completa na FL-02). A ProfitDLL não tem gregas nem strike.

---

## 1. Cadeia e posição em aberto

### OP-01 Grade de séries

- **O que mostra e para que serve.** Mostra a cadeia de um objeto por vencimento, com calls e puts lado a lado em cada strike. Para cada série: ticker, tipo, strike vigente, vencimento, DU, estilo, protegida, multiplicador, OI, quebra coberto/travado/descoberto, prêmio de referência da B3, vol da B3, último negócio, nossa vol implícita, as gregas, a probabilidade de exercício (VL-05) e a marca "série com formador". É a tela de entrada do tema e a base de conferência das demais. Ao abrir uma série, a tela leva ao histórico dela (OP-09).
- **Definição e fórmula.** Preço e gregas pelo Black-Scholes generalizado com custo de carregamento b: `d1 = [ln(S/K) + (b + σ²/2)·T] / (σ·√T)`, `d2 = d1 − σ·√T`, `c = S·e^{(b−r)T}·N(d1) − K·e^{−rT}·N(d2)`, `p = K·e^{−rT}·N(−d2) − S·e^{(b−r)T}·N(−d1)`; para ação protegida, b = r. Vol implícita: o σ que iguala o preço do modelo ao prêmio escolhido. Moneyness: `K/S`. "Série com formador": série de um ativo que está num programa de formador de opções da B3, dentro dos vencimentos de atuação obrigatória (2 nas ações, 6 no índice) [FM]; a lista de ativos vem das planilhas do programa, que ainda não foram lidas. **Referência:** [MA §1.1]; [HULL cap. 15 e 19]; [HAUG cap. 1 e 2]; [BS73]; [M73]; [FM].
- **Entradas e fonte.** Cadastro (IN), posições (BDI), prêmio (PE), negócios (COTAHIST), curva (TS). Preço do objeto: o fechamento do objeto no COTAHIST, que só sai da base depois da ligação opção → objeto (ver "Como ler o status"); durante o pregão, o último pela ProfitDLL via Gateway. No Ibovespa, o nível do índice não está no COTAHIST (§7).
- **Função do motor.** Já existe no branch: `BlackScholesMerton.Evaluate`, `ImpliedVolatility.ForBlackScholesMerton`, `B3Calendar.BusinessDaysBetween`, `FlatForwardDiCurve.DiscountFactor`. A junção vem da visão `series` com `positions` pela data, pelo ticker e pelo `distribution_id`: como `positions` é única por (ticker, `distribution_id`), a junção soma as distribuições da série ou fixa uma. A vol da B3 não está na visão `series`, que só junta `premium` e `premium_source`; ela vem de `premiums.volatility`.
- **Convenções e escolhas em aberto.** Qual prêmio inverter na foto diária (PE ou fechamento); campo do OI (ver regras comuns); theta exibido por DU ou por dia corrido. Tickers são reaproveitados entre anos, então a chave é ticker com vencimento.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor pronto; falta tela.

### OP-09 Histórico de uma série

- **O que mostra e para que serve.** Para uma série escolhida na grade, a evolução desde o lançamento: prêmio de referência da B3, último negócio, vol da B3, nossa vol implícita, OI com a quebra coberto/travado/descoberto e negócios por pregão (número, quantidade e financeiro), com as datas de ajuste de strike marcadas. É a visão padrão ao abrir uma série da grade.
- **Definição e fórmula.** Uma linha por (data, ticker, vencimento). A chave é ticker com vencimento, porque os tickers são reaproveitados entre anos (OP-01). Cada coluna usa a fórmula da tela de origem (OP-01, OP-02 e VL-04), calculada com o pregão da linha. O lançamento é o `TradgStartDt` do cadastro. **Referência:** as das telas de origem; [CAD] (`TradgStartDt`).
- **Entradas e fonte.** `instruments`, `positions`, `premiums` e `trades` de cada pregão gravado. Antes da gravação própria não há OI histórico gratuito por série, porque o BDI guarda cerca de 21 pregões; o COTAHIST anual daria só os negócios.
- **Função do motor.** Falta a leitura da base acumulada e a composição. Nome proposto: `SeriesHistory.Build`. Não há vetor.
- **Convenções e escolhas em aberto.** Pregões sem gravação aparecem como "sem dado", nunca como zero. Um ajuste de strike no meio da série marca a data e o tipo do ajuste (JE-04).
- **Status.** Bloqueada por decisão pendente da fonte (base acumulada: backlog A2 e A3); falta motor; falta tela.

### OP-10 Atividade do dia

- **O que mostra e para que serve.** Um ranking das séries e dos objetos do pregão por número de negócios, quantidade, financeiro e variação do prêmio, com a razão volume/OI. Mostra onde o mercado de opções negociou no dia e onde pode ter entrado posição nova. É a tela de entrada mais comum nos boletins de bolsa.
- **Definição e fórmula.** Por série: negócios (`TOTNEG`), quantidade (`QUATOT`) e financeiro (`VOLTOT`) do dia. Variação do prêmio: `Δ% = último(D)/ref(D−1) − 1`, com `ref` o último negócio de D−1 ou, se não houve negócio, o prêmio de referência PE de D−1. Razão volume/OI: `Q_i(D) / OI_i(D−1)`. Heurística nossa, declarada: uma razão acima de 1 quer dizer que o volume do dia não cabe na posição anterior e sugere abertura de posição nova, o que a FL-01 confirma no pregão seguinte pelo ΔOI. Por objeto: soma das séries do objeto. A ordenação segue a coluna escolhida. **Referência:** [COT] (campos de negócios); [DOP] (OI); [PP06] (o volume de abertura de posição em opções traz informação sobre o preço futuro do objeto).
- **Entradas e fonte.** `trades` do COTAHIST (`TOTNEG`, `QUATOT`, `VOLTOT`, último) ou do BDI, `positions` (OI de D−1) e `premiums` (PE de D−1).
- **Função do motor.** Falta. Nome proposto: `DailyActivityRanking.Build`. Não há vetor.
- **Convenções e escolhas em aberto.** Campo do OI (ver regras comuns). Número mínimo de negócios para entrar no ranking. O ranking por objeto depende da ligação opção → objeto, porque `asset` não distingue a classe da ação.
- **Status.** Dado pronto no branch para o ranking de séries de um pregão; a variação e a razão volume/OI pedem duas datas; o ranking por objeto depende da ligação opção → objeto; falta motor; falta tela.

### OP-02 Posição por strike

- **O que mostra e para que serve.** Barras por strike de calls e de puts, com o OI dividido em coberto, travado e descoberto, e as contagens de clientes em cada ponta. Mostra onde está a posição vendida a descoberto, que é a parte que pode exigir margem e recompra. Um filtro descritivo, "descoberto alto perto do preço", mostra só as séries com strike numa faixa em torno do preço, ordenadas pelo descoberto.
- **Definição e fórmula.** `OI(K, tipo) = Σ OI_i` sobre as séries do tipo com `K_i = K` nos vencimentos escolhidos. Partes: `coberto% = CvrdQty/total`, `travado% = TtlBlckdPos/total`, `descoberto% = UcvrdQty/total`. Identidade conferida: `CvrdQty + TtlBlckdPos + UcvrdQty = TtlPos`; se não fechar, marca `SOMA_DIVERGE`; se a quebra vier nula (opções de derivativos), marca `SEM_QUEBRA`. Filtro, critério nosso e só descritivo: `{ i : |K_i/S − 1| ≤ h }`, ordenado por `UcvrdQty_i` do maior para o menor, com a distância `K/S − 1`; padrão h = 10 %. O filtro não atribui intenção aos lançadores. **Referência:** [DOP] (definição de cada campo).
- **Entradas e fonte.** `positions` (BDI `OpenPositionsEquities`) juntada a `instruments` (IN) pelo ticker do mesmo pregão, somando as distribuições (`distribution_id`) da série ou fixando uma. S de fechamento ou ao vivo, só para o filtro.
- **Função do motor.** Falta. Nomes propostos: `OpenInterestBreakdown.ByStrike` e `OpenInterestBreakdown.NearPriceUncovered`. Vetor: caso `quebra_oi` de `agregados.json`; não há vetor do filtro.
- **Convenções e escolhas em aberto.** O glossário chama `TtlBlckdPos` de "total de posições bloqueadas"; a leitura como posição vendida compensada por opção comprada é hipótese a confirmar. O glossário diz que `DstrbtnId` não se aplica a derivativos, mas a BBSEW441 veio com `DstrbtnId` = 129; falta saber se uma série pode ter mais de uma distribuição. Vencimentos somados ou separados (padrão: um vencimento por vez, com opção "todos"). Faixa h do filtro.
- **Status.** Dado pronto no branch (o filtro perto do preço depende da ligação opção → objeto); falta motor; falta tela.

### OP-03 Resumo por vencimento

- **O que mostra e para que serve.** Uma linha por vencimento do objeto (mensal, semanais W1, W2, W4, W5 e, no IBOV, diários), com DU, OI de calls e de puts, razão put/call, dor máxima, índice titulares/lançadores, vol ATM, intervalo implícito, exposição gamma total e financeiro do dia. Serve para escolher o vencimento que as outras telas vão detalhar.
- **Definição e fórmula.** Cada coluna é a fórmula da tela de origem (OP-05, OP-06, OP-08, GX-01, VL-01 e VL-05), calculada só com as séries daquele vencimento. A lista de vencimentos vem do `XprtnDt` do cadastro, sem deduzir datas pelo ticker. **Referência:** [VENC] para as regras de vencimento; as demais nas telas de origem.
- **Entradas e fonte.** IN, BDI posições, PE, COTAHIST, TS.
- **Função do motor.** Falta a composição. Nome proposto: `ExpirySummary.Build`, que chama as funções das telas de origem.
- **Convenções e escolhas em aberto.** Se o resumo mostra também a linha "todos os vencimentos" e como ela agrega cada coluna (somas para OI e GEX; recálculo para razões e dor máxima).
- **Status.** Dado pronto no branch (vol ATM, GEX e intervalo implícito dependem da ligação opção → objeto); falta motor; falta tela.

### OP-05 Razão put/call

- **O que mostra e para que serve.** A razão entre puts e calls de um objeto, por OI, por quantidade negociada e por financeiro, por vencimento e no total, com a série diária e médias de 5 e 20 pregões. Mede a procura relativa por proteção.
- **Definição e fórmula.** `PCR_OI = Σ OI_puts / Σ OI_calls`; `PCR_vol = Σ Q_puts / Σ Q_calls`; `PCR_fin = Σ financeiro_puts / Σ financeiro_calls`. Variantes: só descoberto (`Σ UcvrdQty_p / Σ UcvrdQty_c`), ponderada por delta (`Σ |Δ_p|·OI_p / Σ Δ_c·OI_c`) e por faixa de moneyness. Denominador zero devolve ausência com a marca `SEM_CALLS`. **Referência:** [CBOE] (publica a razão por volume); [PP06].
- **Entradas e fonte.** OI de `positions`; quantidade e financeiro de `trades` (COTAHIST ou BDI). Volume intradiário: negócios pela ProfitDLL, se a série estiver assinada. As variantes por delta e por moneyness usam S e dependem da ligação opção → objeto.
- **Função do motor.** Falta. Nome proposto: `PutCallRatio.Compute`. Vetor: caso `pcr` de `agregados.json` (OI, volume, financeiro, descoberto, delta e `SEM_CALLS`).
- **Convenções e escolhas em aberto.** Base padrão (proposta: OI e volume juntos); se a razão "do mercado" soma quantidades de todos os objetos ou faz média das razões. O histórico de volume anterior à gravação própria pode vir do COTAHIST anual, que precisa de leitor próprio.
- **Status.** Dado pronto no branch; falta motor; falta tela.

### OP-06 Dor máxima do vencimento

- **O que mostra e para que serve.** O strike em que os titulares, somados, receberiam o menor valor intrínseco no vencimento, com a curva de "dor" por strike e a distância até o preço. É uma referência de onde o vencimento fica mais barato para os lançadores.
- **Definição e fórmula.** Critério nosso, formalizado aqui. Método A (padrão): `Dor(X) = m·[ Σ_c OI_c·max(X − K_c, 0) + Σ_p OI_p·max(K_p − X, 0) ]`, e a dor máxima é o `X` dos strikes listados que minimiza `Dor(X)`. Como `Dor` é convexa e linear por partes, o mínimo cai num strike. Método B (mostrado junto): minimiza a quantidade de contratos dentro do dinheiro, `ITM(X) = Σ_c OI_c·1[X > K_c] + Σ_p OI_p·1[X < K_p]`. Empate: o strike mais perto de S. Exemplo verificado: calls {28: 1.000, 30: 5.000, 32: 8.000, 34: 3.000} e puts {26: 2.000, 28: 6.000, 30: 4.000, 32: 1.000} dão 30 nos dois métodos. **Referência:** [NPP05], [AL03] e [GJ12] (concentração do preço perto de strikes no vencimento, que motiva a leitura). A definição em si não tem fonte acadêmica e é nossa.
- **Entradas e fonte.** OI de `positions` e strike de `instruments`, do mesmo pregão; um cálculo por objeto e vencimento. A distância até o preço e o desempate usam S.
- **Função do motor.** Falta. Nome proposto: `MaxPain.Compute` (varredura em O(n log n) pela condição de primeira ordem). Vetor: caso `max_pain` de `agregados.json`, com o caso de empate do método B.
- **Convenções e escolhas em aberto.** Método exibido como principal; se existe a versão com todos os vencimentos; como tratar séries com OI zero (padrão: ignorar).
- **Status.** Dado pronto no branch; falta motor; falta tela.

### OP-07 Dor máxima no tempo

- **O que mostra e para que serve.** A dor máxima de cada vencimento dia a dia, sobre o preço de fechamento, até o vencimento, e o preço de liquidação no fim. Mostra se o nível se move e se o preço converge para ele.
- **Definição e fórmula.** Uma linha por (data, objeto, vencimento) com `dor_max_A`, `dor_max_B`, S de fechamento e, no vencimento, o preço de liquidação. A fórmula é a da OP-06. **Referência:** [NPP05]; [AL03]; [GJ12].
- **Entradas e fonte.** A mesma da OP-06, mas com uma foto por pregão. O BDI guarda cerca de 21 pregões; antes da gravação própria não há OI histórico gratuito por série.
- **Função do motor.** Falta `MaxPain.Compute` (OP-06) e a leitura da base acumulada.
- **Convenções e escolhas em aberto.** Quando um strike é ajustado por provento, o histórico fica descontínuo: a tela marca a data do ajuste (JE-04).
- **Status.** Bloqueada por decisão pendente da fonte (base acumulada: backlog A2 e A3, parados até o cartão de 05/11); falta motor; falta tela.

### OP-08 Índice titulares/lançadores

- **O que mostra e para que serve.** Por série e agregado por tipo, a razão entre o número de titulares e o de lançadores, com linhas no tempo junto do preço. Na nossa leitura, muitos titulares pequenos contra poucos lançadores grandes sugerem posição concentrada do lado vendido.
- **Definição e fórmula.** Critério nosso, declarado, sobre os campos de contagem de clientes de [DOP]; o índice não tem fonte acadêmica. `ITL_i = H_i / W_i`, com H = número de clientes titulares e W = número de clientes lançadores. Agregado padrão por tipo: `ITL_calls = Σ H / Σ W` sobre as calls (idem puts). Alternativas: ponderado por OI e ponderado por descoberto. Série com W = 0 sai do agregado com a marca `SEM_LANCADOR`. H e W são pessoas, não contratos. **Referência:** [DOP] (campos de contagem de clientes).
- **Entradas e fonte.** `positions.borrowers` (`BrrwrQty`, "quantidade de tomadores") e `positions.lenders` (`LndrQty`, "quantidade de doadores"). A importação os guarda como contagens de clientes, sem convertê-los em contratos.
- **Função do motor.** Falta. Nomes propostos: `HolderWriterIndex.ForSeries` e `HolderWriterIndex.Aggregate`. Vetor: caso `iq` de `agregados.json` (as três agregações e `SEM_LANCADOR`), que precisa ser regenerado sem o bloco `barreiras` (pendência 5).
- **Convenções e escolhas em aberto.** A amostra real de 03/11/2026 (BBSEW441) trouxe 7 e 124 para 294.300 opções, o que confirma que são contagens de clientes. Falta confirmar qual campo é titular e qual é lançador; a hipótese é tomador = titular e doador = lançador. Agregação padrão: razão de somas. Um cliente com posição em várias séries é contado várias vezes.
- **Status.** Dado pronto no branch, com a leitura dos campos a confirmar; falta motor; falta tela.

## 2. Gamma e exposição

### GX-01 Exposição gamma por strike

- **O que mostra e para que serve.** Barras por strike com a exposição gamma atribuída aos formadores de mercado, o total do objeto e a curva acumulada. Duas camadas opcionais completam a tela: a concentração de gamma por strike, que marca em cada tipo o strike de maior concentração, e o movimento de empate do hedge, em coluna, por série e agregado. Exposição positiva indica hedge contra o movimento (amortece a volatilidade); negativa indica hedge a favor do movimento (acelera) [BB; NPPW21].
- **Definição e fórmula.**
  - Por série: `GEX_i = s_i · Γ_i · OI_i · m_i · S² · 0,01`, em R$ de delta por movimento de 1 % (unidade U3). Por strike: `GEX(K) = Σ_{K_i = K} GEX_i`; total: `Σ_i GEX_i`; acumulado: `Σ_{K ≤ K_j} GEX(K)`. Sinal padrão A: `s = +1` nas calls e `−1` nas puts. Exemplo verificado: Γ = 0,115873, OI = 100.000, m = 1 e S = 30 dão R$ 104.286 por 1 %.
  - Concentração de gamma por strike (camada). Regra b (padrão): o strike de maior OI de calls e o de maior OI de puts, `K_call = argmax_K Σ_{calls, K_i = K} OI_i` (idem `K_put`), sobre o OI definido em [DOP]. Regra a (critério nosso): o mesmo argmax com o peso `Γ_i · OI_i · m_i · S² · 0,01`, sem sinal. Regra c (critério nosso): maior `GEX(K)` positivo e mais negativo, com sinal. Empate: strike mais perto de S. Lado: livre (padrão) ou só `K ≥ S` nas calls e `K ≤ S` nas puts.
  - Movimento de empate do hedge (coluna). Para uma posição com hedge de delta, `δΠ ≈ Θ·δt + ½·Γ·(δS)²`. O movimento de empate é `δS* = √(2·|Θ·δt| / |Γ|)`, só quando Γ e Θ têm sinais opostos. Pela equação de Black-Scholes, `Θ + r·S·Δ + ½·σ²·S²·Γ = r·V`; com o financiamento do hedge, `Θ_fin = Θ + r·(S·Δ − V) = −½·σ²·S²·Γ` e `δS* = σ·S·√δt`. Por série, é o movimento de empate de quem compra a opção e faz o hedge do delta. Agregado: `Γ_tot = Σ s_i·Γ_i·OI_i·m_i`, `Θ_tot = Σ s_i·(Θ_i/252)·OI_i·m_i` e faixa `S ± √(2·|Θ_tot| / |Γ_tot|)`; marca `SINAIS_IGUAIS` se `Γ_tot·Θ_tot ≥ 0`. Exemplo verificado (S = K = 100, T = 30/252, σ = 30 %): 1,889822 com r = 0 e também com r = ln(1,1065) e financiamento; 2,160880 com r = ln(1,1065) sem financiamento.
  - **Referência:** [HULL cap. 19] (definição de gamma, relação entre delta, theta e gamma, e a base da unidade das regras comuns); [BS73]; [BB], [BDLM21] e [NPPW21] (efeito do hedge dos formadores no preço); [DOP] (OI da regra b); [FM] (séries em que a hipótese de sinal faz sentido).
- **Entradas e fonte.** OI de D−1 (`positions`), strike e multiplicador (`instruments`), vol por série (PE na foto diária ou a curva SVI), r da curva (TS), S de fechamento (depende da ligação opção → objeto) ou ao vivo pelo Gateway. Θ e Γ por série para a coluna de empate.
- **Função do motor.** Γ e Θ já existem no branch (`BlackScholesMerton.Evaluate` e `Black76.Evaluate`, campos `Gamma` e `Theta` de `OptionValuation`). Falta a agregação. Nomes propostos: `GammaExposure.ByStrike`, `GammaConcentration.ByType` e `HedgeBreakevenMove.Compute`. Vetores de `agregados.json`: caso `gex_dex` (unidades U1, U2 e U3; sinais A, B e D; por série, por strike, acumulado e total); caso `walls` para a concentração (regras a, b e c; lado livre e restrito); caso `equilibrio_gamma_theta` para o empate, sem vetor de `SINAIS_IGUAIS`. Os casos `walls` e `equilibrio_gamma_theta` citam fontes fora das aceitas e devem ser regenerados com outro nome e com as fontes desta tela (pendência 5).
- **Convenções e escolhas em aberto.** Convenção de sinal (A padrão; B "formador vendido em tudo"; D pela quebra coberto/descoberto, hipótese nossa sem fonte; E pelo saldo de corretoras na Fita, que exige a Fita de opções). Unidade. Vencimentos somados (padrão: todos) ou filtrados. Fonte da vol. Vencimento do dia: tirar a série depois do horário-limite, que deve vir da grade de horários vigente da B3. Regra (b, padrão) e lado da concentração. Empate do hedge com ou sem o financiamento quando r > 0 (decisão do Marcelo); horizonte (1 DU, padrão, ou até o vencimento); theta por DU (Θ/252) ou decaimento exato de 1 DU, que difere de 2 % a 3 % nas ATM.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela.

### GX-02 Preço de gamma zero

- **O que mostra e para que serve.** A curva da exposição gamma total em função de um preço hipotético do objeto (perfil gamma), o preço em que ela troca de sinal (preço de gamma zero) e o regime atual (positivo, negativo ou perto do zero).
- **Definição e fórmula.** `G(X) = Σ_i s_i · Γ_i(X; K_i, T_i, σ_i) · OI_i · m_i · X² · 0,01`, com Γ recalculado em cada X. Método 1 (padrão): varrer X em `[0,7·S; 1,3·S]` com passo de 0,25 % de S, achar as trocas de sinal e refinar cada raiz por Brent; a raiz mais perto de S é a principal. Método 2: o strike em que o acumulado `Σ_{K ≤ K_j} GEX(K)` troca de sinal, com interpolação linear. Regime: positivo se `G(S) > 0`, negativo se `< 0`, perto do zero se `|S − X_0|/S ≤ 0,5 %`, e "sem troca de sinal" se não houver troca na grade. **Referência:** [HULL cap. 19] (gamma recalculado em cada preço); [BR73] (Brent). O método, a grade e os limiares são critério nosso.
- **Entradas e fonte.** As da GX-01.
- **Função do motor.** Γ por preço já existe no branch. O Brent do branch (`VolatilityBrentSolver`) é interno da vol implícita; o perfil precisa de um localizador de raiz genérico. Faltam `GammaProfile.Build` e `ZeroGammaPrice.Find` (nomes propostos). Vetor: caso `gamma_flip` de `agregados.json` (métodos 1 e 2 e o caso sem troca de sinal); não há vetor do regime "perto do zero". O caso e as marcas dele levam o termo comercial em inglês e devem ser renomeados ao regenerar (pendência 5).
- **Convenções e escolhas em aberto.** Método (1 ou 2; no vetor V1 dão 29,76 e 32,99). Vol com strike fixo (padrão) ou com moneyness fixa. A grade do Ibovespa e do dólar está na §7.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela.

### GX-05 Exposição delta por strike

- **O que mostra e para que serve.** Barras por strike com o delta atribuído aos formadores, em R$ e em unidades do objeto, e o total. O hedge implícito é o contrário do total: mostra quanto do objeto os formadores teriam de vender ou comprar.
- **Definição e fórmula.** `DEX_i = s_i · Δ_i · OI_i · m_i · S` (R$); `DEX(K) = Σ_{K_i = K} DEX_i`; `DEX_tot = Σ_i DEX_i`; `hedge = −DEX_tot`. Na convenção A, a put tem Δ < 0 e s = −1, então também soma positivo. **Referência:** [HULL cap. 19] (hedge de delta). O sinal segue a convenção A das regras comuns.
- **Entradas e fonte.** As da GX-01.
- **Função do motor.** Δ já existe no branch. Falta `DeltaExposure.ByStrike` (nome proposto). Vetor: caso `gex_dex` de `agregados.json` (DEX e hedge).
- **Convenções e escolhas em aberto.** Sinal e vencimentos como na GX-01. Nas opções sobre futuro, o delta é em relação a F; para comparar com o à vista, `Δ_S = Δ_F · e^{b·T_F}`.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela.

### GX-06 Exposição perto do dinheiro no tempo

- **O que mostra e para que serve.** A série diária da exposição delta e gamma só das séries perto do dinheiro, junto do preço de fechamento, e o recálculo durante o pregão com o preço ao vivo e o OI fixo. Mostra como a posição perto do preço mudou ao longo dos pregões.
- **Definição e fórmula.** `DEX_perto(h) = Σ_{|K_i/S − 1| ≤ h} DEX_i` e `GEX_perto(h) = Σ_{|K_i/S − 1| ≤ h} GEX_i`, com h = 2 % e 5 %. Uma linha por (data, objeto). **Referência:** as da GX-01 e da GX-05 ([HULL cap. 19]); a faixa h é critério nosso.
- **Entradas e fonte.** As da GX-01, com uma foto por pregão. Durante o pregão, S ao vivo pelo Gateway.
- **Função do motor.** Falta `NearMoneyExposure.Compute` (nome proposto) e a leitura da base acumulada. Vetor: caso `gex_dex` de `agregados.json` (faixas de ±2 % e ±5 %).
- **Convenções e escolhas em aberto.** Faixa h. Se a faixa usa S do dia ou S fixo da data-base.
- **Status.** Bloqueada por decisão pendente da fonte (base acumulada: backlog A2, A3 e C4); falta motor; falta tela.

### GX-07 Exposição de vanna e charm

- **O que mostra e para que serve.** Tela opcional. Mostra quanto o delta dos formadores muda com 1 ponto percentual de vol (vanna) e com a passagem de 1 DU (charm). Ajuda a ler o efeito de queda de vol e da passagem do tempo perto do vencimento.
- **Definição e fórmula.** `VEX = Σ s_i · vanna_i · OI_i · m_i · S · 0,01` (R$ de delta por 1 p.p. de vol); `CEX = Σ s_i · (charm_i/252) · OI_i · m_i · S` (R$ de delta por DU). `vanna = ∂Δ/∂σ`; `charm = ∂Δ/∂t`. **Referência:** [HAUG cap. 2] (gregas de segunda ordem). O sinal segue a convenção A das regras comuns.
- **Entradas e fonte.** As da GX-01.
- **Função do motor.** Falta. `OptionValuation` do branch tem preço, delta, gamma, vega, theta e rho, mas não vanna, charm nem vomma. Nomes propostos: `SecondOrderGreeks.Evaluate` e `SecondOrderExposure.Compute`. Não há vetor no repositório.
- **Convenções e escolhas em aberto.** Se a tela entra na primeira versão.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; falta motor (gregas de 2ª ordem); falta tela.

## 3. Volatilidade

### VL-01 Sorriso por vencimento

- **O que mostra e para que serve.** A vol implícita por strike de um vencimento, com os pontos de mercado, a curva SVI ajustada e a vol publicada pela B3. Serve para ver a inclinação (skew) e a curvatura do sorriso e dar a vol de cada série às telas de exposição. A densidade neutra ao risco (VL-06) é uma aba desta tela.
- **Definição e fórmula.** Ponto: `k = ln(K/F)` e variância total `w = σ_impl² · T`. Curva SVI "raw": `w(k) = a + b·[ρ·(k − m) + √((k − m)² + σ²)]`, ajustada por mínimos quadrados em variância total, só com pontos fora do dinheiro, com no mínimo 5 strikes. Restrições: `b ≥ 0`, `|ρ| < 1`, `σ > 0`, variância mínima positiva, asas `b·(1 ± ρ) < 2` e o critério suficiente de ausência de arbitragem borboleta da SPEC-0524. Forward: `F = K + e^{rT}·(c − p)` pela paridade (mediana de 3 strikes perto do dinheiro) ou `F = S·e^{rT}` para ação protegida. **Referência:** [NT13]; [GJ14 §2 e §3]; [LEE04] (inclinação das asas); [J15] e [BR73] (inversão da vol); [HULL cap. 20].
- **Entradas e fonte.** Foto diária: prêmio PE de todas as séries, inclusive sem negócio, com S de fechamento e a curva TS. O forward `S·e^{rT}` depende da ligação opção → objeto; o forward pela paridade não usa S. Durante o pregão: meio do book (se houver as duas pontas e spread de até 20 % do meio), senão último negócio dos últimos 15 minutos, pela ProfitDLL via Gateway.
- **Função do motor.** Já existem no branch: `ImpliedVolatility.ForBlackScholesMerton` e `ForBlack76`, `RawSviFitter.Fit`, `RawSviParameters.ImpliedVolatility` e `RawSviParameters.DensityFactor`. Faltam a escolha do preço e o forward pela paridade. Nomes propostos: `PriceSelection.Choose` e `ForwardFromParity.Estimate`. Os vetores de SVI ficam em `tests/Web/Farol.Portal.Tests/Options/Data/SviVectors.json` (sintéticos).
- **Convenções e escolhas em aberto.** Preço da foto (PE ou fechamento). Pesos do ajuste (padrão: sem pesos, como a NT-2013-01). RMSE máximo aceito. Para ações, a B3 usa outros modelos de superfície, então a curva SVI é escolha nossa e não reproduz a vol do PE.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela.

### VL-06 Densidade neutra ao risco por vencimento

- **O que mostra e para que serve.** Aba da VL-01. Mostra a densidade neutra ao risco do preço no vencimento, tirada do sorriso ajustado, e a probabilidade implícita de o preço terminar em cada faixa (por exemplo, abaixo de 0,9·F, entre 0,9·F e 1,1·F e acima de 1,1·F).
- **Definição e fórmula.** Pela relação de Breeden e Litzenberger, a densidade do preço terminal é `q(K) = e^{rT}·∂²C/∂K²` [BL78]. Com a SVI em variância total, a densidade de `k = ln(S_T/F)` tem forma fechada: `p(k) = g(k)/√(2π·w(k)) · exp(−d₂(k)²/2)`, com `d₂(k) = −k/√w(k) − √w(k)/2` e `g(k)` a função de Durrleman [GJ14 §2]. Probabilidade da faixa [K1, K2]: `∫ p(k) dk` entre `ln(K1/F)` e `ln(K2/F)`, por integração numérica. Se `g(k) < 0` em algum k, há arbitragem borboleta: a tela marca `DENSIDADE_NEGATIVA` e não mostra a probabilidade. Conferência própria com uma SVI de teste (a = 0,002; b = 0,04; ρ = −0,4; m = 0; σ = 0,1): `∫ p(k) dk` = 1 e `∫ e^k·p(k) dk` = 1 com erro abaixo de 1e-12, e `p(k)` bate com `K·∂²C/∂K²` por diferenças finitas com erro relativo abaixo de 1e-6. **Referência:** [BL78]; [GJ14 §2]; [LEE04].
- **Entradas e fonte.** O ajuste SVI da VL-01, F e T.
- **Função do motor.** Já existem no branch `RawSviParameters.TotalVariance` e `RawSviParameters.DensityFactor`, que dá o g(k). Faltam a densidade e a integração. Nome proposto: `RiskNeutralDensity.FromSvi`. Não há vetor.
- **Convenções e escolhas em aberto.** Faixas exibidas. Além dos strikes listados, a SVI extrapola pelas asas lineares, e a probabilidade nas pontas é sensível a elas [LEE04]. A densidade é neutra ao risco, não a probabilidade real.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela.

### VL-02 Superfície e estrutura a termo

- **O que mostra e para que serve.** Os sorrisos de todos os vencimentos de um objeto numa grade (moneyness por prazo), a vol ATM por vencimento (estrutura a termo) e a vol ATM de prazo constante (21 e 63 DU). Mostra se a vol curta está acima ou abaixo da longa.
- **Definição e fórmula.** Para um T entre dois vencimentos, interpola-se a variância total linearmente em T com k fixo: `w(k, T) = w1(k) + (w2(k) − w1(k))·(T − T1)/(T2 − T1)`, e `σ(k, T) = √(w(k, T)/T)`. Condição de calendário: `w(k, T2) ≥ w(k, T1)` para todo k da grade, senão marca a violação. **Referência:** [GJ14, Lema 2.1]; [NT13] (interpolação em variância total); [MA §6.2 e §6.3].
- **Entradas e fonte.** As da VL-01, para todos os vencimentos.
- **Função do motor.** O ajuste por vencimento já existe no branch (`RawSviFitter.Fit`). Faltam a interpolação e a checagem de calendário. Nomes propostos: `VolatilitySurface.Interpolate` e `VolatilitySurface.CheckCalendar`. A SPEC-0524 declara que não há garantia de arbitragem de calendário.
- **Convenções e escolhas em aberto.** Prazos constantes exibidos. Se a superfície inteira deve ser ajustada de uma vez (SSVI) em vez de vencimento a vencimento.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela.

### VL-05 Intervalo implícito até o vencimento

- **O que mostra e para que serve.** Por vencimento, a faixa de ±1 e ±2 desvios em torno do preço pela vol ATM, comparada com o preço do straddle ATM, e a probabilidade de exercício `N(d2)` de cada série. Também aparece como coluna da OP-03 e como camada da OP-01.
- **Definição e fórmula.** Pela propriedade lognormal do modelo [HULL cap. 15], `faixa_k = [S·e^{−k·σ_ATM·√T}; S·e^{+k·σ_ATM·√T}]`, com k = 1 e 2, que cobre cerca de 68,3 % e 95,4 % da distribuição de `ln S_T` quando se ignora o termo de drift; a versão com o drift neutro ao risco usa `F·e^{−σ²T/2 ± k·σ·√T}`. Straddle ATM: `c(K_ATM) + p(K_ATM)`, mostrado também como fração de S; perto do dinheiro, `straddle ≈ √(2/π)·S·σ·√T ≈ 0,8·S·σ·√T` [BS88]. Probabilidade neutra ao risco de exercício: `N(d2)` na call e `N(−d2)` na put [HULL cap. 15]. Exemplo verificado (S = 30, σ = 35 %, DU = 21, DI = 10,65 %): ±1 desvio vai de 27,12 a 33,19 e ±2 desvios de 24,51 a 36,72; o straddle de strike 30 custa 2,4157 (8,05 % de S), contra 0,8·S·σ·√T = 2,4185; a call de strike 32 tem `N(d2)` = 0,2723. **Referência:** [HULL cap. 15]; [BS88].
- **Entradas e fonte.** Vol ATM (VL-01 ou VL-02), S, T, r (TS) e os prêmios PE das séries ATM.
- **Função do motor.** Preço e vol implícita já existem no branch (`BlackScholesMerton`, `Black76`, `ImpliedVolatility`). Falta expor d2, porque `OptionValuation` não traz d1 nem d2. Nomes propostos: `ExpectedRange.Compute` e `ExerciseProbability.Compute`. Não há vetor.
- **Convenções e escolhas em aberto.** Com ou sem o termo de drift (padrão: sem). Vol ATM pelo strike mais perto de F ou interpolada em k = 0. `N(d2)` é probabilidade neutra ao risco, não a probabilidade real.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor parcial; falta tela.

### VL-03 Vol implícita no tempo

- **O que mostra e para que serve.** A série diária da vol ATM de prazo constante, a inclinação do sorriso, a vol realizada do objeto e a diferença entre as duas, com o percentil da vol implícita nos últimos 252 pregões. Mostra se as opções estão caras ou baratas contra o próprio histórico do objeto.
- **Definição e fórmula.** Vol ATM de 21 DU pela VL-02. Inclinação: `σ(K/F = 0,9) − σ(K/F = 1,1)` no mesmo prazo. Vol realizada: `σ_real = √(252/(n − 1) · Σ (u_t − ū)²)`, com `u_t = ln(S_t/S_{t−1})` em 21 e 63 pregões. Percentil: posição da vol de hoje entre as últimas 252. **Referência:** [HULL cap. 15] (vol a partir de dados históricos); [WS16] (a B3 publica a vol implícita de ações desde 14/12/2016).
- **Entradas e fonte.** Vol do PE de cada pregão (retenção na Pesquisa por pregão ainda não medida) ou nossa vol sobre o PE; fechamento do objeto pelo COTAHIST.
- **Função do motor.** Faltam `RealizedVolatility.CloseToClose` e `ImpliedVolatilityHistory.Build` (nomes propostos), além da VL-02. O COTAHIST anual (desde 1986) daria o passado da vol realizada, mas o leitor do branch só aceita o arquivo diário.
- **Convenções e escolhas em aberto.** Comparar por moneyness `K/F` (ou delta), e não por strike, porque o ajuste por provento muda o strike no meio da série. Prazo constante (21 DU, padrão). Os preços do COTAHIST não são ajustados por proventos, então o retorno da data-ex precisa do ajuste pelo provento (JE-03).
- **Status.** Bloqueada por decisão pendente da fonte (histórico acumulado: backlog A2 e A3); falta leitor do COTAHIST anual; falta motor; falta tela.

### VL-07 Vol implícita entre objetos

- **O que mostra e para que serve.** Um ranking de todos os objetos com opções pela vol implícita ATM de 21 DU, pelo percentil dessa vol em 252 pregões e pela diferença contra a vol realizada de 21 pregões. Serve para achar opções caras ou baratas no mercado inteiro; a VL-03 olha um objeto só.
- **Definição e fórmula.** Por objeto: `σ_ATM,21` (VL-02); `pct` = posição de `σ_ATM,21` de hoje entre as últimas 252; `σ_real,21` (VL-03); e `prêmio de vol = σ_ATM,21 − σ_real,21`. A ordenação segue a coluna escolhida. **Referência:** [HULL cap. 15]. O ranking é critério nosso.
- **Entradas e fonte.** As da VL-03 para cada objeto; a lista de objetos com opções vem do cadastro.
- **Função do motor.** Falta. Nome proposto: `VolatilityRanking.Build`, sobre as funções da VL-02 e da VL-03. Não há vetor.
- **Convenções e escolhas em aberto.** Liquidez mínima para entrar no ranking (número de séries com prêmio perto do dinheiro). Prazo (21 DU, padrão).
- **Status.** Bloqueada por decisão pendente da fonte (histórico); falta ligação opção → objeto; falta motor; falta tela.

### VL-08 Cone de volatilidade

- **O que mostra e para que serve.** Para um objeto, a vol realizada em janelas de 10, 21, 42, 63, 126 e 252 pregões, com o mínimo, os quartis e o máximo históricos de cada janela, e a vol implícita ATM do prazo equivalente por cima. Mostra se a vol implícita está alta ou baixa para o prazo, contra o que o objeto já realizou.
- **Definição e fórmula.** Para cada janela n, a série de `σ_real(n)` pela fórmula da VL-03 em todo o histórico; o cone é o conjunto de mínimo, primeiro quartil, mediana, terceiro quartil e máximo de cada n. A vol implícita de prazo n vem da VL-02 (prazo constante em DU). **Referência:** [BL90]; [HULL cap. 15].
- **Entradas e fonte.** Fechamentos do objeto no COTAHIST (anual, desde 1986, e diário); vol ATM pela VL-02.
- **Função do motor.** Faltam `RealizedVolatility.CloseToClose` (VL-03) e `VolatilityCone.Build` (nomes propostos). Não há vetor.
- **Convenções e escolhas em aberto.** Janelas sobrepostas (padrão) ou não sobrepostas; com sobreposição, as janelas longas têm poucas observações independentes. Os preços do COTAHIST não são ajustados por proventos, e o retorno da data-ex precisa de ajuste (JE-03), senão o cone sobe nas datas de evento. Histórico mínimo para mostrar a janela de 252.
- **Status.** Falta dado (leitor do COTAHIST anual; a vol implícita por cima depende da ligação opção → objeto); falta motor; falta tela.

### VL-04 Conferência com o prêmio de referência da B3

- **O que mostra e para que serve.** Por série, a nossa vol implícita ao lado da vol publicada pela B3 e a diferença entre elas. Também inverte o próprio prêmio da B3 com o nosso modelo. Serve para validar as convenções do motor com um dado oficial todo dia.
- **Definição e fórmula.** `dif_conv = σ_motor(prêmio PE) − σ_PE/100` mede só a diferença de convenção (DU, taxa, preço do objeto), porque inverte o mesmo prêmio. `dif_preço = σ_motor(fechamento) − σ_PE/100` mede a diferença de preço. A B3 calcula com Black-Scholes sem dividendos, DI1 interpolado, objeto das 18h às 18h20 e superfície por SABR, Corrado-Su, VLFit ou VLGARCH (GARCH nas ilíquidas). Conferência possível do delta: o arquivo `Deltas` da Pesquisa por pregão traz os deltas de opções padronizadas usados nos limites de posição [PR]; só o nome foi confirmado, e falta ver se ele cobre as séries e a convenção do nosso delta. **Referência:** [MA §1.1 e §1.2]; [WS16]; [PR].
- **Entradas e fonte.** `premiums` (PE: prêmio e vol), `instruments`, `trades` (COTAHIST) e `swap_rates` (TS). O S de fechamento depende da ligação opção → objeto. Amostra real de 03/11/2026: BBSEW441 com prêmio 1,73 e vol 29,24; IBOVX161 com prêmio 2.311 e vol 21,94.
- **Função do motor.** Já existe no branch: `ImpliedVolatility.ForBlackScholesMerton`, `B3Calendar`, `FlatForwardDiCurve`. A comparação é uma subtração.
- **Convenções e escolhas em aberto.** Limite de diferença aceitável por liquidez. O RE (segmento BM&F) não traz vol, então a conferência do dólar usa só o prêmio. Se o arquivo `Deltas` entra como segunda conferência.
- **Status.** Dado pronto no branch, mas falta ligação opção → objeto; motor pronto; falta tela.

## 4. Fluxo

### FL-01 Variação da posição em aberto

- **O que mostra e para que serve.** As séries com maior aumento e maior queda de OI de um pregão para o outro, com a variação do descoberto e do coberto e a quantidade negociada. Mostra onde entrou posição nova e onde houve encerramento.
- **Definição e fórmula.** `ΔOI_i = OI_i(D) − OI_i(D−1)`; idem para `UcvrdQty`, `CvrdQty` e `TtlBlckdPos`. Heurística própria, declarada: `ΔOI > 0` com negócios no dia é abertura líquida; `ΔOI < 0` é encerramento líquido; `|ΔOI|/Q` mede quanto do volume mudou a posição. **Referência:** [DOP] (o arquivo da B3 tem `VartnOpnIntrst`, a variação contra D−1).
- **Entradas e fonte.** `positions` de dois pregões seguidos; quantidade de `trades`.
- **Função do motor.** Falta `OpenInterestChange.Compute` (nome proposto). O branch não grava `VartnOpnIntrst`: ou a tela calcula a diferença entre duas importações, ou a coluna entra na base como mudança aditiva.
- **Convenções e escolhas em aberto.** Se a tela confere a diferença calculada com o `VartnOpnIntrst` da B3. Como marcar as séries com ajuste de quantidade por evento (JE-04).
- **Status.** Bloqueada por decisão pendente da fonte (duas datas seguidas: backlog A2 e A3); falta motor; falta tela.

### FL-02 Fluxo por grupo de corretoras

- **O que mostra e para que serve.** O saldo comprado menos vendido, em quantidade e em R$, dos grupos de corretoras (estrangeiras, institucionais locais, varejo e ambíguas), por janela (1, 5, 15 e 60 minutos e o dia), no objeto, nos futuros e, nas séries que a Fita de opções cobre, nas opções. Mostra quem está agredindo.
- **Definição e fórmula.** Para o grupo g: `saldo_g = Σ_{buy_agent ∈ g} q − Σ_{sell_agent ∈ g} q` e o mesmo em R$ (`q · preço`). Agressão: a coluna `aggressor` da Fita é o `TTradeType` da ProfitDLL copiado sem conversão (1 cruzado, 2 comprador agressor, 3 vendedor agressor, 4 leilão, 5 vigilância, 13 RLP, 32 desconhecido) [IPC]. Com 2, a corretora agressora é `buy_agent`; com 3, é `sell_agent`. Assim, `agr_compra_g = Σ q` dos negócios com `aggressor = 2` e `buy_agent ∈ g`, e `agr_venda_g = Σ q` dos negócios com `aggressor = 3` e `sell_agent ∈ g`. Os tipos 1, 4, 5 e 32 ficam fora da agressão (padrão) ou recebem o lado pela regra de Lee-Ready [LR91], de forma declarada. O RLP (13) precisa de regra explícita, porque o tipo não diz o lado e a main o inclui na seleção de `TapeQuery` (`aggressor IN (2, 3, 13)`); padrão proposto: fora da agressão e contado à parte. Heurística própria, declarada: o grupo é o da **corretora**, não o do investidor final; corretora estrangeira não quer dizer investidor não residente; o dado oficial por tipo de investidor é a FL-05. **Referência:** [IPC] (definição de `aggressor`); [LR91] (direção do negócio quando falta o agressor); [PRS] (só nas etiquetas que o citam).
- **Entradas e fonte.** Fita gravada no DataHub (`buy_agent`, `sell_agent`, `aggressor`). Etiqueta de cada corretora em `docs/base-de-conhecimento/fluxo-winfut/corretoras-prior.json`: são 36 corretoras, com 7 'estrangeira', 3 'institucional local', 8 'varejo', 17 'ambígua' e 1 'não identificada'. Quatorze citam fontes fora da B3 (gist.github.com, tradehunter.com.br, clubedospoupadores.com e imprensa), quatro só têm fontes fora da B3, e uma não tem fonte. A B3 não publica negócio por corretora. Opções: a main já tem um caminho fora de linha que grava a Fita diária de opções na História sem mexer na ingestão viva (SPEC-0078, integrada em 02/10/2026; `docs/surfaces/data.md`, seção de 2026-10-02) [SPEC0078]. Depois do pregão, a Rotina enfileira um par (opção, Pregão) por série viva com `enqueue-history`, e a Fita vem com `buy_agent`, `sell_agent` e `aggressor`. Hoje esse caminho cobre só as séries dos Sinais, e a DLL guarda cerca de 30 dias.
- **Função do motor.** O saldo por corretora já existe na main (`/api/fluxo/vivo/corretoras`, `FluxoVivoStore`, saldo de 1, 5, 15 e 60 minutos). Falta o agrupamento por etiqueta, que hoje só existe num script de pesquisa. Nome proposto: `BrokerGroupFlow.Aggregate`.
- **Convenções e escolhas em aberto.** 'Ambígua' é um grupo próprio na tela, e corretora sem etiqueta vai para "outras"; quase metade das corretoras fica fora dos três grupos nomeados. Regra dos tipos 1, 4, 5, 13 e 32. Universo das opções: ampliar a lista de séries da SPEC-0078 para as séries perto do dinheiro, pelo mesmo caminho fora de linha; o acompanhamento em tempo real dessas séries é o desenho do backlog D1 (até 256 assinaturas pelo Gateway, sem tocar no caminho congelado).
- **Status.** Dado pronto na main para objeto e futuros; dado parcial de opções na main (SPEC-0078, só séries dos Sinais), falta ampliar o universo; falta motor; falta tela.

### FL-03 Negócios grandes

- **O que mostra e para que serve.** A lista dos negócios grandes do dia, com hora, preço, quantidade, financeiro, lado agressor, corretoras e grupos. Nas opções, mostra também o delta equivalente para comparar strikes. Serve para achar a entrada de participantes grandes.
- **Definição e fórmula.** Heurística própria, declarada. Um negócio, ou um bloco de negócios com o mesmo par comprador e vendedor em até 1 segundo, é grande se `q ≥ max(Q_abs, P99)`, com P99 o percentil 99 do tamanho dos negócios do mesmo ticker nos últimos 20 pregões da Fita, ou se o financeiro passar de `F_min`. Lado agressor pela regra da FL-02 (2 compra, 3 venda; os demais tipos fora ou por Lee-Ready). Nas opções: `delta_equiv = Δ · m · q · S` em R$. **Referência:** [IPC]; [LR91] (classificação do lado); a regra de tamanho é nossa.
- **Entradas e fonte.** Fita gravada no DataHub; Δ pelo motor; S ao vivo ou de fechamento.
- **Função do motor.** Falta `LargeTradeDetector.Detect` (nome proposto).
- **Convenções e escolhas em aberto.** Valores de `Q_abs` e `F_min` por classe de ativo; janela do bloco. O mesmo universo de opções da FL-02 (SPEC-0078).
- **Status.** Dado pronto na main para objeto e futuros; dado parcial de opções na main (SPEC-0078, só séries dos Sinais), falta ampliar o universo; falta motor; falta tela.

### FL-05 Participação por tipo de investidor

- **O que mostra e para que serve.** Compras, vendas e saldo por tipo de investidor (estrangeiro, institucional, instituição financeira, pessoa física e outros) no segmento de ações, acumulado no mês e por dia, e a tabela mensal por mercado, que inclui opções e exercício de opções. É o dado oficial que a FL-02 só aproxima.
- **Definição e fórmula.** O BDI publica o acumulado do mês até D−2. Saldo de um dia, por inferência declarada: `saldo(D−2) = acum(D−2) − acum(D−3)`, zerando na virada do mês. **Referência:** [BDI02].
- **Entradas e fonte.** BDI, capítulo 02 (PDF), `BDI_02_{AAAAMMDD}.pdf`. Futuros (IND, DOL, DI1) não têm série diária gratuita de volume por tipo de investidor; a posição em aberto por tipo de participante existe, mas a página atual da B3 não foi localizada.
- **Função do motor.** Falta. Nome proposto: `InvestorParticipation.DailyFromCumulative`. Ler PDF é dependência nova e precisa de aprovação.
- **Convenções e escolhas em aberto.** Se vale ler o PDF ou esperar uma tabela do BDI em CSV.
- **Status.** Falta dado; falta motor; falta tela.

## 5. Juros e eventos

### JE-01 Curva pré DI

- **O que mostra e para que serve.** A curva pré por DU, com a taxa de cada vértice, o forward entre vértices, o fator de desconto e o PU do DI1, comparada com o pregão anterior. Dá a taxa r de todas as telas que descontam.
- **Definição e fórmula.** Flat forward 252: `A(du) = du/252 · ln(1 + i(du))` linear em du entre vértices, `DF = e^{−A}`; equivalente a `(1 + i)^{du/252} = (1 + i1)^{du1/252} · [(1 + i2)^{du2/252} / (1 + i1)^{du1/252}]^{(du − du1)/(du2 − du1)}`. Forward entre vértices: `(DF1/DF2)^{252/(du2 − du1)} − 1`. PU do DI1: `100.000 / (1 + i)^{n/252}`. Taxa contínua para o modelo: `r = −ln(DF)/T`. A B3 monta a curva com o CDI no vértice de 1 DU e os ajustes do DI1 nos vencimentos, com DU pelo calendário ANBIMA e extrapolação pelo último forward. O CDI diário vem do arquivo "DI over" do Boletim Diário do Mercado [CDI]. **Referência:** [MC]; [DI]; [CDI]; [OC055]; [ANB] (só para conferir).
- **Entradas e fonte.** TS (`swap_rates`, curva PRE, sete casas, saques como DU); ajuste e taxa de ajuste do DI1 (`trades`, BDI); CDI de D−1 pelo DI over [CDI], ainda não importado. Durante o pregão: DI1 pela ProfitDLL via Gateway.
- **Função do motor.** Já existe no branch: `FlatForwardDiCurve` com `DiscountFactor(du)` e `AnnualEffectiveRate(du)`, extrapolação pelo último forward. O forward entre vértices e o PU são uma linha cada. Vetor: caso `curva_di` de `agregados.json` (flat forward, extrapolação e PU) e `FlatForwardDiCurveTests`.
- **Convenções e escolhas em aberto.** Curva com vértices contra DI plano (o vetor de agregados usa DI plano de 10,65 %; com a curva no vértice, a GEX total muda 1,4e-3). Horário do ajuste do DI1 (16h10 a 16h20 na página do produto contra "17h" no Manual de Apreçamento).
- **Status.** Dado pronto no branch (duas datas para a comparação com o pregão anterior); motor pronto; falta tela.

### JE-02 Calendário de pregões e vencimentos

- **O que mostra e para que serve.** Os vencimentos de cada produto (ações mensais e semanais, IBOV mensal e diário, DOL, mini opções de dólar, DI1) com a data, o DU de pregões e o DU ANBIMA até cada um, e os dias sem pregão. Torna visível quando os dois calendários divergem.
- **Definição e fórmula.** `DU_B3` conta pregões; `DU_ANBIMA` conta dias úteis ANBIMA, em que 24/12 e 31/12 contam sem haver pregão. Exemplo verificado: de 01/12/2026 a 15/01/2027 há 29 pregões e 31 DU ANBIMA. Regras [VENC]: opção mensal de ação na 3ª sexta-feira (pregão anterior se não houver pregão); semanais nas demais sextas; IBOV mensal na quarta-feira mais próxima do dia 15 (pregão seguinte se não houver pregão); IBOV diário em todo pregão, menos no dia do vencimento mensal, desde 17/11/2025; DOL no 1º dia útil do mês, com o último dia de negociação no pregão anterior ao vencimento; mini opções de dólar com fixing em qualquer dia útil com pregão e vencimento no pregão seguinte ao fixing, desde 04/05/2026 (OC 017/2026-VPC), com o último dia de negociação na data do fixing; DI1 no 1º pregão do mês. Na mini opção, o resultado fica definido no fixing (PTAX de venda) e a liquidação ocorre no vencimento, o que muda o T da regra do dólar (§7). Novembro de 2026: a opção mensal de ações vence na quinta, 19/11, porque 20/11 é feriado.
  - **DU oficiais do IN.** O IN traz, por instrumento, `WrkgDays`, que conta pregões da B3, e `WdrwlDays`, que conta saques, que são os DU do DI (calendário ANBIMA), nos futuros e nas opções sobre disponível e sobre futuro (`OptnOnSpotAndFutrsInf`). As opções de ações (`OptnOnEqtsInf`) não trazem esses campos. Conferência própria com a lista de feriados do branch, contando (03/11/2026, vencimento]: INDZ26 dá 30 nos dois, igual a `WrkgDays` = `WdrwlDays` = 30; DI1F27 dá 39 pregões e 41 DU ANBIMA, iguais a `WrkgDays` = 39 e `WdrwlDays` = 41, porque 24/12 e 31/12 contam só na ANBIMA; DOLN27C005300 dá 162 e 164, também iguais ao IN. É uma fonte diária e gratuita da B3 para testar o `B3Calendar` nos dois calendários, e ela mostra a divergência real de 24/12 e 31/12.
  - **Referência:** [VENC]; [FER]; [OC055]; [CAD] (`WrkgDays`, `WdrwlDays`).
- **Entradas e fonte.** Datas de vencimento: `XprtnDt` do cadastro (IN), sem deduzir pelo ticker. Feriados: `tests/fixtures/opcoes/feriados-b3-2026-2028.json` (2026 oficial; 2027 e 2028 derivados). DU oficiais: `WrkgDays` e `WdrwlDays` do IN, que o branch ainda não importa.
- **Função do motor.** Já existe no branch: `B3Calendar` com `IsBusinessDay`, `BusinessDaysBetween` e `YearFraction`; para dois calendários, duas instâncias com listas diferentes. Por desenho, o motor não deduz vencimentos. Proposta: importar `WrkgDays` e `WdrwlDays` como mudança aditiva e usá-los como teste da JE-02 (backlog F2); os três instrumentos da fixture já servem de casos.
- **Convenções e escolhas em aberto.** `B3Calendar` conta `[início, fim)`; os vetores e o IN contam `(data-base, vencimento]`. Os dois coincidem quando as duas pontas são dias úteis (de 04/11 a 19/11/2026, 11 nos dois), mas diferem com a data-base num fim de semana (de sábado, 07/11, a sexta, 13/11: 4 contra 5). Fração intradiária e horário-limite do dia do vencimento: sem fonte vigente lida; ler a grade de horários da B3 antes de usar. Os feriados precisam virar configuração com fonte, não ficar só em fixture.
- **Status.** Motor pronto no branch; falta dado (calendário como configuração; `WrkgDays` e `WdrwlDays` não importados); falta tela.

### JE-03 Proventos e eventos corporativos

- **O que mostra e para que serve.** Os proventos em dinheiro (dividendo, juros sobre capital, rendimento) e os eventos em ações (desdobramento, grupamento, bonificação) de cada objeto, com data-com, data-ex, valor bruto, valor que ajusta o strike e as séries afetadas. Avisa quais strikes vão mudar e quando.
- **Definição e fórmula.**
  - Data-ex: o pregão seguinte à data-com (`lastDatePrior`).
  - Valor de ajuste dos proventos em dinheiro: o valor líquido de impostos, que o MPO 7.9.1 usa desde 09/03/2026 para todo provento em dinheiro, sem tabela fixa de alíquota [OC006VPE]. Juros sobre capital: bruto × 0,825 desde 01/01/2026 [OC026]. Até 2025 o dividendo não tinha imposto, então o valor líquido era o bruto. Em aberto está só a alíquota que a B3 aplica a dividendos sob a Lei 15.270/2025 [S], e não a regra.
  - Ajuste usual por subtração: `K_aj = K − D_aj`, em 2 casas, ao fim da data-com. Exceção quando `D ≥ K`: `F = P_ex / P_com` (8 casas), `K_aj = K · F` (2 casas), `qtd_aj = ⌊qtd / F⌋` [OC093; OC141].
  - Eventos em ações, regra usual [S] até a leitura do MPO 7.9.1: a B3 publica o evento com outro fator, que não é `P_ex/P_com` (`factor` em `StockDividends` [T], com sentido a confirmar, ou o fator f do desdobramento). Pelo Manual de Precificação de Eventos Corporativos v5, `P_com = P_ex·(1 + B)` na bonificação B e `P_com = f·P_ex` no desdobramento ou grupamento de fator f [MPEC]. Daí: na bonificação (10 % = 0,10), `K_aj = K/(1 + B)` e `qtd_aj = qtd·(1 + B)`; no desdobramento ou grupamento, `K_aj = K/f` e `qtd_aj = qtd·f`. Escrita com `F = P_ex/P_com`, que fica abaixo de 1 num desdobramento, a mesma regra multiplica o strike por F e divide a quantidade por F.
  - **Referência:** [MPO 7.9.1]; [OC006VPE]; [OC026]; [OC093]; [OC141]; [MPEC]; [EVT].
- **Entradas e fonte.** B3, "Dividendos e outros eventos corporativos" (`sistemaswebb3-listados`, que veda coleta automatizada). Reserva: ProfitDLL `SubscribeAdjustHistory`, que o Host já recebe mas não grava. Conferência: CVM, dados abertos IPE.
- **Função do motor.** Falta. Nomes propostos: `CorporateActionAdjustment.CashAmount` e `CorporateActionAdjustment.Factor`. Não há vetor.
- **Convenções e escolhas em aberto.** A alíquota do dividendo no ajuste, a confirmar no texto do MPO 7.9.1, que ainda não foi lido. O sentido do campo `factor` (fração ou percentual). Não existe calendário público de proventos esperados.
- **Status.** Falta dado; falta motor; falta tela.

### JE-04 Ajustes de strike por série

- **O que mostra e para que serve.** O histórico de mudanças de strike e de quantidade de cada série, com a data, o strike antigo e o novo, o tipo de ajuste e o evento que o explica. Explica descontinuidades nas telas de histórico.
- **Definição e fórmula.** Para cada série com a mesma chave (ticker e vencimento) em D−1 e D: se `K(D) ≠ K(D−1)`, registra o evento. Classificação: subtração se `K(D−1) − K(D)` igualar o valor de ajuste de um provento com data-com em D−1; fator se `K(D)/K(D−1)` igualar um fator e a quantidade mudar; desdobramento ou grupamento pelo fator do evento (JE-03); senão "desconhecido". **Referência:** [MPO 7.9.1]; [OC093]; [OC141]; [MPEC]; [CAD] (`PrtcnFlg`, opção protegida; `TrgtInstrmId`; `SrsTp`).
- **Entradas e fonte.** `instruments` de dois pregões seguidos (strike vigente e protegida, já importados no branch). O IN traz também `TrgtInstrmId`, o instrumento novo depois de fusão ou cisão (a RAIZR20 da fixture tem um), e `SrsTp`; o branch não importa nenhum dos dois, e os dois ajudam a classificar o evento. Reserva: a consulta "ajuste de proventos" do Hub de dados da B3, ainda não aberta.
- **Função do motor.** Falta. Nomes propostos: `StrikeAdjustmentDetector.Detect` e `StrikeAdjustmentDetector.Classify`. Não há vetor.
- **Convenções e escolhas em aberto.** Tolerância para casar o ΔK com o valor do provento (arredondamento em 2 casas).
- **Status.** Bloqueada por decisão pendente da fonte (duas datas seguidas: backlog A2 e A3); falta motor; falta tela.

### JE-05 Aluguel de ações

- **O que mostra e para que serve.** Por ação, o saldo alugado, as taxas doadora e tomadora (mínima, média e máxima) e a série no tempo, com a fração do capital alugada e os dias de negociação para zerar o saldo. O aluguel caro e crescente indica posição vendida grande no objeto e pesa no preço das puts. A tela fica neste tema porque a taxa de aluguel é custo de carregamento do objeto, e não fluxo de negócios.
- **Definição e fórmula.** Taxa média ponderada da B3: média ponderada de todos os negócios e renovações do dia, sem filtro de valores extremos [CE068]. `fração_alugada = saldo / total de ações`. `dias_para_zerar = saldo / volume médio diário de 20 pregões`. **Referência:** [ER]; [CE068]; [NBTB]; [DAV02].
- **Entradas e fonte.** BDI, seção Clearing, "Empréstimos registrados" (taxas, D−1 na abertura); BDI `BTBLendingOpenPosition` (saldo, D−1 na abertura); NEGOCIOSBTB (taxa por negócio, sem renovações); volume do COTAHIST. Total de ações: cadastro da empresa na B3 (`GetListedSupplementCompany`) ou dado da CVM.
- **Função do motor.** Falta. Nome proposto: `SecuritiesLendingMetrics.Compute`. O branch não tem leitor de nenhum desses arquivos, e a rota do BDI de empréstimos registrados não foi confirmada.
- **Convenções e escolhas em aberto.** Fonte do total de ações (a página de empresas da B3 veda coleta automatizada). Se a taxa tomadora entra como custo de carregamento no modelo das puts.
- **Status.** Falta dado; falta motor; falta tela.

## 6. Estruturas

### ES-01 Calculadora de opção

- **O que mostra e para que serve.** Preço e gregas de uma opção a partir de entradas digitadas ou trazidas da grade, e a vol implícita a partir de um preço. Serve para conferir qualquer número das outras telas.
- **Definição e fórmula.** Modelos: Black-Scholes sem dividendo (b = r), BSM-Merton com q (b = r − q), Black-76 sobre o futuro (b = 0, S → F) e Garman-Kohlhagen (b = r_d − r_f). Gregas: Δ, Γ, vega, Θ e ρ; exibição com Θ/252, vega/100 e ρ/100. Vol implícita por Newton com intervalo e Brent de reserva; preço fora de `[intrínseco descontado, teto descontado]` não tem solução. Exemplo verificado: S = 30, K = 32, DU = 21, DI = 10,65 %, σ = 35 % dão call 0,564695 e Γ 0,115873. **Referência:** [BS73]; [M73]; [B76]; [GK83]; [HULL cap. 15, 17, 18 e 19]; [HAUG cap. 1 e 2]; [MA §1.1 e §2.1]; [J15].
- **Entradas e fonte.** S ou F, K, datas (DU pelo `B3Calendar`) ou T, σ ou preço, taxa da curva (TS) ou digitada, q.
- **Função do motor.** Já existe no branch: `BlackScholesMerton.Evaluate`, `Black76.Evaluate`, `ImpliedVolatility.ForBlackScholesMerton`, `ImpliedVolatility.ForBlack76`, `B3Calendar`, `FlatForwardDiCurve`. O Garman-Kohlhagen é o `BlackScholesMerton.Evaluate` com `dividendYield` = cupom contínuo, mas faltam o rho estrangeiro, porque `OptionValuation` só traz o rho da taxa doméstica, e a conversão do cupom (`FxCarry.ContinuousCoupon`, §7).
- **Convenções e escolhas em aberto.** Theta por DU ou por dia corrido. Os 82 casos de `tests/fixtures/opcoes/precificacao.json` ainda não rodam contra o motor C#: os testes do Portal usam os próprios vetores em `Options/Data/`, e só o teste Python confere os geradores. Ligar os dois é trabalho de verificação (backlog F).
- **Status.** Dado digitado; motor pronto no branch para BSM e Black-76, parcial para Garman-Kohlhagen (faltam o rho estrangeiro e a conversão do cupom); falta tela.

### ES-02 Payoff de uma posição

- **O que mostra e para que serve.** O resultado de uma posição livre (uma ou mais pernas de opção, com ou sem o objeto) em função do preço no vencimento e numa data intermediária, com pontos de empate, ganho e perda máximos.
- **Definição e fórmula.** No vencimento: `P&L(S_T) = Σ lado_j · qtd_j · m_j · (valor_j(S_T) − preço_j)`, com `valor = max(S_T − K, 0)` na call, `max(K − S_T, 0)` na put e `S_T` no objeto. Antes do vencimento: `valor_j` pelo modelo com a vol de cada série e strike fixo. Empates: as raízes de `P&L(S_T) = 0`. Marca `GANHO_ILIMITADO` ou `PERDA_ILIMITADA` só pela inclinação acima do último strike, quando ela é positiva ou negativa. Na ponta de baixo, como `S_T ≥ 0`, uma inclinação não nula entre 0 e o primeiro strike dá resultado finito; o ganho e a perda máximos são avaliados nos strikes e em `P&L(0)`. No vetor `payoff`, a `venda_coberta_lote_100` tem inclinação 100 abaixo do primeiro strike, perda máxima de −2.920 em `S_T = 0` e nenhuma marca, e o `straddle_vendido` recebe `PERDA_ILIMITADA` só pela inclinação −1 acima do último strike. **Referência:** [HULL cap. 12].
- **Entradas e fonte.** Pernas digitadas ou escolhidas na grade; preços da grade (PE ou fechamento) ou ao vivo pelo Gateway.
- **Função do motor.** O valor antes do vencimento já existe no branch (`BlackScholesMerton.Evaluate`, `Black76.Evaluate`). Falta o payoff e a análise. Nome proposto: `StructurePayoff.AtExpiry` e `StructurePayoff.Before`. Vetor: caso `payoff` de `agregados.json` (oito estruturas no vencimento); não há vetor antes do vencimento nem de ganho ilimitado.
- **Convenções e escolhas em aberto.** Custos de corretagem e emolumentos (padrão: desligados). Preço usado (executável ou meio).
- **Status.** Dado digitado ou da grade (OP-01); motor parcial; falta tela.

### ES-03 Payoff de estruturas

- **O que mostra e para que serve.** Os modelos prontos (trava de alta e de baixa, borboleta, condor, straddle, strangle, razão 1×2, venda coberta, collar e box) montados automaticamente com as séries da grade, lado a lado, com custo, empate e resultado máximo e mínimo.
- **Definição e fórmula.** Cada modelo é uma lista de pernas com regra de strike (por exemplo, trava de alta: compra call K1 e vende call K2 > K1). O resultado e as marcas de ganho ou perda ilimitados são os da ES-02. **Referência:** [HULL cap. 12].
- **Entradas e fonte.** As da ES-02, com a grade da OP-01.
- **Função do motor.** Igual à ES-02, mais `StructureTemplates.Build` (nome proposto). Vetor: caso `payoff` de `agregados.json`.
- **Convenções e escolhas em aberto.** Quais modelos entram na primeira versão; regra de escolha dos strikes (distância fixa ou por delta).
- **Status.** Dado da grade (OP-01); motor parcial; falta tela.

### ES-04 Gregas da estrutura (delta estrutural)

- **O que mostra e para que serve.** As gregas somadas de uma estrutura, o delta em R$ e em ações equivalentes, o movimento de empate do hedge e uma grade de cenários de preço e de vol. Mostra quanto do objeto neutraliza a estrutura e quanto o preço precisa andar para o gamma pagar o theta.
- **Definição e fórmula.** `Δ_est = Σ lado_j · qtd_j · m_j · Δ_j`, com Δ = 1 por ação do objeto; o mesmo para Γ, vega e Θ. `delta_R$ = Δ_est · S`; hedge = `−Δ_est` ações. Movimento de empate do hedge: `δS* = √(2·|Θ_est·δt| / |Γ_est|)`, só quando `Γ_est` e `Θ_est` têm sinais opostos (fórmula e escolhas na GX-01). Cenários: valor da estrutura com S ± x % e σ ± y p.p. **Referência:** [HULL cap. 19].
- **Entradas e fonte.** As da ES-02.
- **Função do motor.** As gregas por perna já existem no branch (`OptionValuation`). Falta a soma, o movimento de empate e os cenários. Nomes propostos: `StructureGreeks.Aggregate` e `HedgeBreakevenMove.Compute` (o mesmo da GX-01).
- **Convenções e escolhas em aberto.** Delta das opções sobre futuro em relação a F ou ao à vista (GX-05). Empate com ou sem financiamento do hedge (GX-01).
- **Status.** Dado digitado ou da grade (OP-01); motor parcial; falta tela.

### ES-05 Buscador de estruturas de renda

- **O que mostra e para que serve.** Uma tela só, com o tipo de estrutura como filtro: venda coberta, venda de put com garantia em caixa, box de 3 pontas, box de 4 pontas e collar. Para o tipo escolhido, lista as combinações de um objeto (ou de vários) com o capital, a taxa se o preço ficar parado, as taxas mínima e máxima quando existem, a anualização e a comparação com o CDI do prazo.
- **Definição e fórmula.**
  - Comum a todos os tipos: anual `r_aa = (1 + r_per)^{252/DU} − 1`; CDI do período `CDI_per = (1 + DI)^{DU/252} − 1`, com DI da curva no vértice (JE-01) ou o CDI do dia [CDI]; `%CDI(1) = r_per / CDI_per`; `%CDI(2) = [(1 + r_per)^{1/DU} − 1] / [(1 + DI)^{1/252} − 1]` [DI].
  - Venda coberta: capital `I = S_ask − C_bid`; valor extrínseco `VE = C_bid − max(S − K, 0)`; taxa parada `r_per = VE / I`; taxa se exercida `r_max = K/I − 1`; proteção `C_bid/S` [HULL cap. 12].
  - Venda de put com garantia em caixa: capital padrão `I = K − P_bid` (alternativa: `I = K`); taxa do prêmio `r_per = P_bid / I`. Taxa total com a garantia aplicada no CDI, na forma exata: com o capital próprio `K − P_bid` e a garantia K no CDI, `K·(1 + CDI_per)/(K − P_bid) − 1 = (1 + r_per)·(1 + CDI_per) − 1`; a soma `r_per + CDI_per` subestimaria o retorno em `r_per·CDI_per`, e a forma exata é coerente com a anualização acima. Preço efetivo se exercida: `K − P_bid`. Puts dentro do dinheiro: `VE = P_bid − max(K − S, 0)` e taxa parada `VE / I` [HULL cap. 12].
  - Box de 3 pontas (compra do objeto, compra de put e venda de call do mesmo strike e vencimento; renda fixa sintética): `I = S_ask + P_ask(K) − C_bid(K)`; resultado fixo `K` no vencimento; `r_per = K/I − 1`. Exemplo verificado: S = 30, K = 30, P_ask = 1,20, C_bid = 1,65, DU = 21 e DI = 10,65 % dão I = 29,55, r_per = 1,5228 %, r_aa = 19,89 %, 179,8 % do CDI (1) e 179,2 % (2). A B3 tem programa de incentivo tarifário próprio para o box de 3 pontas [OC032] [HULL cap. 11 e 12].
  - Box de 4 pontas (trava de alta com calls e trava de baixa com puts nos mesmos strikes K1 < K2): aplicação `I = C_ask(K1) − C_bid(K2) + P_ask(K2) − P_bid(K1)`, resultado `K2 − K1`, `r_per = (K2 − K1)/I − 1`; captação `I' = C_bid(K1) − C_ask(K2) + P_bid(K2) − P_ask(K1)` e custo `(K2 − K1)/I' − 1`; taxa contínua implícita `ln((K2 − K1)/I) / T`, porque sem atrito o box vale `(K2 − K1)·e^{−rT}` [HULL cap. 12].
  - Collar (objeto comprado, put comprada em K1 e call vendida em K2 ≥ K1): `I = S_ask + P_ask(K1) − C_bid(K2)`; resultado `min(max(S_T, K1), K2)`; `r_min = K1/I − 1`; `r_max = K2/I − 1`; parada `min(max(S, K1), K2)/I − 1`; perda máxima `I − K1`; ganho máximo `K2 − I`; custo zero quando o prêmio da put iguala o da call. O box de 3 pontas é o collar com K1 = K2 [HULL cap. 12].
  - **Referência:** [HULL cap. 11 e 12]; [DI]; [CDI]; [OC032].
- **Entradas e fonte.** Bid e ask executáveis do objeto e das opções: ao vivo pelo Gateway (book) ou, no fechamento, `PREOFC` e `PREOFV` do COTAHIST, que o leitor do branch ainda não lê. DU pelo `B3Calendar`; DI pela curva (JE-01) ou CDI do dia [CDI].
- **Função do motor.** Falta. Nomes propostos: `IncomeStructureScan.Find`, com o tipo de estrutura como parâmetro, e `CdiComparison.Compute`. Vetor: caso `taxas_cdi` de `agregados.json`. O caso aponta para uma nota de metodologia marcada [Q] e deve ser regenerado com as fontes desta tela; o box de 4 pontas do vetor foi montado à mão, com o ask abaixo do meio em 3 das 4 pernas, e precisa ser refeito antes de virar teste (pendência 5).
- **Convenções e escolhas em aberto.** "% do CDI" pela razão (1) ou no estilo CDB (2) (padrão: as duas). CDI de referência (curva no vértice, padrão, ou CDI do dia). Saída "parado" pelo ask ou pelo bid. Capital da venda de put com garantia (K − P ou K) e se a taxa soma o CDI da garantia. Lado padrão do box de 4 pontas (aplicação). Faixa de K1 e K2 em torno de S e custo máximo do collar. Marcas `AMERICANA_VENDIDA` (exercício antecipado de call americana vendida, que entrega a ação, antecipa K e muda a taxa) e `PROVENTO_NO_PRAZO`. Eventos por fator mudam strikes e quantidades, mas o nocional do box fica igual. Custos e tributação (padrão: desligados).
- **Status.** Falta dado (bid/ask); falta motor; falta tela.

### ES-10 Estruturas salvas

- **O que mostra e para que serve.** As estruturas que o usuário guardou (pernas, preços usados, data e nota), reavaliadas a cada pregão com o fechamento ou ao vivo, com o resultado desde a montagem. Serve para acompanhar ideias sem anotar à parte.
- **Definição e fórmula.** Resultado na data t: `Σ lado_j · qtd_j · m_j · (valor_j(t) − preço_j)`, com `valor_j(t)` de mercado ou pelo modelo (ES-02).
- **Entradas e fonte.** Registro do próprio usuário; preços da grade ou do Gateway.
- **Função do motor.** Falta o armazenamento. Nome proposto: `SavedStructureStore`. Local a decidir: um store próprio do Portal, nunca a História, que só o DataHub escreve.
- **Convenções e escolhas em aberto.** Salvar uma estrutura não cria Ordem e não leva a nenhuma tela de envio. O tratamento quando uma perna vence ou tem o strike ajustado (JE-04).
- **Status.** Dado do próprio usuário; falta motor (armazenamento); falta tela.

## 7. Objeto e modelo: Ibovespa e dólar

O objeto é um seletor comum a todas as telas. Esta seção não descreve telas: ela dá a regra que as telas aplicam quando o seletor escolhe o Ibovespa ou o dólar. A grade do índice e a do dólar são a OP-01; as exposições e o preço de gamma zero são a GX; o sorriso e a superfície são a VL. As antigas ID-01 a ID-04 viraram as duas regras abaixo, e o modelo de cada vencimento sai delas (`UnderlyingModelSelector`). O backlog C5 continua como item de trabalho.

### Regra do Ibovespa (antigas ID-01 e ID-02)

- **Modelo.** Padrão: Black-76 com o futuro do mesmo vencimento, `c = e^{−rT}·[F·N(d1) − K·N(d2)]`, `d1 = [ln(F/K) + σ²T/2] / (σ√T)`; o Manual da B3 usa o ajuste do futuro de índice do mesmo vencimento [MA §6.1]. Sem futuro casado: `F = K + e^{rT}·(c − p)` na mediana de 3 strikes perto do dinheiro, ou interpolação do carregamento `F(T) = S·e^{b(T)·T}` entre os futuros vizinhos. Alternativa: BSM-Merton com q sobre o índice à vista, que hoje é "falta dado", porque o nível do Ibovespa não está no COTAHIST nem em outro arquivo do branch. A fonte da B3 é o BVBG.087 (Index Report, código IR da Pesquisa por pregão) [PR], cujo conteúdo só foi visto em código de terceiros [T] e que o branch não importa. Na amostra de 03/11/2026, IBOVX161 e INDZ26 vencem no mesmo dia (16/12/2026). Exemplo verificado: F = 130.000, K = 132.000, DU = 15, σ = 20 % e DI = 10,65 % dão call 1.663,57 e put 3.651,56, em pontos.
- **Multiplicador.** m = R$ 0,01 por ponto, confirmado por três fontes concordantes: no IN, a IBOVX161 traz `PricFctr` = 100, e as opções de ações trazem 1; no COTAHIST, a mesma série traz `FATCOT` = 100, e VOLTOT/QUATOT = 256.492,20/10.495 = 24,4395 = PREMED/100 (2.443,94/100); e a página do produto diz que, desde fev/2025, o ponto vale R$ 0,01 [VENC]. Falta importar `PricFctr` (ou `FATCOT`): hoje o multiplicador do IBOV não está na base, nem o 1 das opções de ações.
- **Exposições.** As da GX, com F no lugar de S: `GEX_i = s_i · Γ_i · OI_i · m_i · F² · 0,01`, com Γ em relação a F. Exemplo verificado: no caso acima, a GEX por contrato é de cerca de R$ 10.134 por 1 % com m = 1; com o multiplicador real, m = R$ 0,01 por ponto, o valor por opção é de cerca de R$ 101,34 por 1 %. Grade do perfil (GX-02): `[0,9·F; 1,1·F]` com passo de 0,1 %. Mistura de séries sobre S e sobre F: só depois de converter para R$ por 1 %.
- **Entradas e fonte.** IN (opções de IBOV e futuros IND), PE (prêmio e vol de IBOV), posições, ajuste do IND (BDI), TS; nível do índice pelo BVBG.087, ainda não importado. Durante o pregão: IND, WIN e o índice pelo Gateway.
- **Função do motor.** Já existem no branch: `Black76.Evaluate`, `BlackScholesMerton.Evaluate`, `ImpliedVolatility.ForBlack76`. Faltam `ForwardFromParity.Estimate` e a regra de escolha do modelo por objeto e vencimento (`UnderlyingModelSelector`, nome proposto). Não há vetor de forward pela paridade.
- **Convenções e escolhas em aberto.** O cadastro distingue IBOV de IND, e a amostra não prova que existam opções sobre o futuro de índice listadas. Os vencimentos diários deixam T muito curto, então o horário-limite e a fração intradiária pesam. Se os vencimentos diários entram na soma das exposições (padrão: entram, e o do dia sai depois do horário-limite). **Referência:** [B76]; [HULL cap. 17 e 18]; [MA §6.1]; [VENC]; [PR].
- **Status da regra.** Dado pronto no branch para o Black-76 (opções de IBOV e futuro IND), sem o multiplicador importado; a alternativa BSM sobre o índice à vista é "falta dado" (BVBG.087); motor parcial (faltam o forward pela paridade e o seletor).

### Regra do dólar (antigas ID-03 e ID-04)

- **Modelo.** Opções sobre dólar (DOL, US$ 50.000, europeias, vencimento no 1º dia útil do mês) e mini opções. Padrão proposto: Black-76 sobre o DOL do mesmo vencimento, que dispensa a curva de cupom. Alternativa: Garman-Kohlhagen na forma da B3, `c = S·e^{−q·T}·N(d1) − K·e^{−r·T}·N(d2)`, com `r = ln(1 + DI)`, `q = (252/DU) · ln(1 + cupom · DC/360)` e S o dólar "cupom limpo". Pela paridade coberta, `F = S·e^{(r − q)·T}`, e o GK coincide com o Black-76 sobre F. Exemplo verificado: S = 5,40, K = 5,50, DU = 20, DC = 28, cupom 5 % linear/360 e σ = 14 % dão q = 0,048905, F = 5,42246, call 0,052240 e put 0,129160 (por US$; 52,240 por US$ 1.000). **Referência:** [GK83]; [B76]; [MA §2.1 a §2.3 e §6.1]; [HULL cap. 17].
- **Prazo.** A opção de DOL vence no 1º dia útil do mês e para de negociar no pregão anterior ao vencimento. Na mini opção, o resultado fica definido no fixing (PTAX de venda) e a liquidação ocorre no pregão seguinte (OC 017/2026-VPC) [VENC]; padrão proposto: T da vol até o fixing e desconto até o vencimento (JE-02).
- **Sorriso.** A B3 ajusta SVI em variância implícita para o dólar, `var(x) = a + b·[ρ·(x − m) + √((x − m)² + σ²)]`, com `x = ln(K/F)`; em variância total, `w = T · var`, ou seja, `a_w = T·a` e `b_w = T·b` [MA §2.2; NT13; GJ14]. O prêmio RE não traz vol: a vol vem da inversão do prêmio.
- **Exposições.** As da GX, com F e m = 50 (strike, prêmio e F por US$ 1.000). Grade do perfil (GX-02): `[0,9·F; 1,1·F]`. Mistura de séries sobre S e sobre F: só depois de converter para R$ por 1 %.
- **Entradas e fonte.** IN (DOLN27C005300: strike 5.300 por US$ 1.000, m = 50, `ExrcStyle` europeia, vence em 01/07/2027, `WrkgDays` = 162 e `WdrwlDays` = 164); posições (OI preenchido, quebra nula); RE (prêmio); ajuste do DOL (BDI); TS (curva PRE; as curvas de cupom vêm no mesmo arquivo, com fonte a confirmar). Durante o pregão: DOL e WDO pelo Gateway.
- **Função do motor.** Já existem no branch: `Black76.Evaluate` e `BlackScholesMerton.Evaluate`, que com `dividendYield = q` é o GK, `ImpliedVolatility.ForBlack76` e `RawSviFitter.Fit`. Faltam o cupom contínuo (`FxCarry.ContinuousCoupon`, nome proposto), o rho estrangeiro, que o `OptionValuation` não traz, o forward e as agregações da GX.
- **Convenções e escolhas em aberto.** Strike, prêmio e F na mesma unidade do cadastro (R$ por US$ 1.000). Se há opções sobre o futuro de dólar listadas, e o código das mini opções diárias (manual de negociação, item 3.2.5.1, não lido). Se as mini opções diárias entram na soma das exposições.
- **Status da regra.** Dado pronto no branch para o Black-76, com o cupom cambial a confirmar para o GK; motor parcial.

---

## Funções que faltam no motor (nomes propostos)

Os nomes seguem o estilo do branch (inglês, namespace `Farol.Portal.Options`, funções puras sem I/O nem relógio). A referência em Python de quase todas está em `scripts/research/opcoes/gerar_agregados.py`, que gera `agregados.json`.

| Função proposta | Telas | Vetor existente |
|---|---|---|
| `SeriesHistory.Build` | OP-09 | nenhum |
| `DailyActivityRanking.Build` | OP-10 | nenhum |
| `OpenInterestBreakdown.ByStrike`, `.NearPriceUncovered` | OP-02, OP-03 | `quebra_oi` (nenhum para o filtro) |
| `ExpirySummary.Build` | OP-03 | nenhum |
| `PutCallRatio.Compute` | OP-03, OP-05 | `pcr` |
| `MaxPain.Compute` | OP-03, OP-06, OP-07 | `max_pain` |
| `HolderWriterIndex.ForSeries`, `.Aggregate` | OP-03, OP-08 | `iq` (regenerar sem o bloco `barreiras`) |
| `GammaExposure.ByStrike` | GX-01, §7 | `gex_dex` |
| `GammaConcentration.ByType` | GX-01, §7 | `walls` (regenerar com outro nome e fontes aceitas) |
| `HedgeBreakevenMove.Compute` | GX-01, ES-04 | `equilibrio_gamma_theta` (regenerar com outro nome e fontes aceitas) |
| `GammaProfile.Build`, `ZeroGammaPrice.Find` | GX-02, §7 | `gamma_flip` (regenerar com outro nome e fontes aceitas) |
| `DeltaExposure.ByStrike` | GX-05, §7 | `gex_dex` |
| `NearMoneyExposure.Compute` | GX-06 | `gex_dex` (faixas) |
| `SecondOrderGreeks.Evaluate`, `SecondOrderExposure.Compute` | GX-07 | nenhum no repositório |
| `PriceSelection.Choose`, `ForwardFromParity.Estimate` | VL-01, VL-02, §7 | nenhum |
| `RiskNeutralDensity.FromSvi` | VL-06 | nenhum |
| `VolatilitySurface.Interpolate`, `.CheckCalendar` | VL-02, VL-03 | nenhum |
| `ExpectedRange.Compute`, `ExerciseProbability.Compute` | VL-05, OP-01, OP-03 | nenhum |
| `RealizedVolatility.CloseToClose`, `ImpliedVolatilityHistory.Build` | VL-03, VL-07, VL-08 | nenhum |
| `VolatilityRanking.Build` | VL-07 | nenhum |
| `VolatilityCone.Build` | VL-08 | nenhum |
| `OpenInterestChange.Compute` | FL-01 | nenhum |
| `BrokerGroupFlow.Aggregate` | FL-02 | nenhum |
| `LargeTradeDetector.Detect` | FL-03 | nenhum |
| `InvestorParticipation.DailyFromCumulative` | FL-05 | nenhum |
| `CorporateActionAdjustment.CashAmount`, `.Factor` | JE-03 | nenhum |
| `StrikeAdjustmentDetector.Detect`, `.Classify` | JE-04, OP-07, OP-09, FL-01 | nenhum |
| `SecuritiesLendingMetrics.Compute` | JE-05 | nenhum |
| `StructurePayoff.AtExpiry`, `.Before`, `StructureTemplates.Build` | ES-02, ES-03, ES-10 | `payoff` |
| `StructureGreeks.Aggregate` | ES-04 | nenhum |
| `IncomeStructureScan.Find`, `CdiComparison.Compute` | ES-05 | `taxas_cdi` (regenerar com as fontes da ES-05) |
| `FxCarry.ContinuousCoupon` | §7 (dólar), ES-01 | caso `TX-CUPOM-CONT-20DU` de `precificacao.json` |
| `UnderlyingModelSelector` | §7, todas | nenhum |
| `SavedStructureStore` (armazenamento, fora do motor puro) | ES-10 | nenhum |

## Pendências que atravessam telas (em ordem de impacto)

1. **Leitura da base pelo Portal** (backlog A5), por data e objeto, pela Concessão. Sem ela nenhuma tela de dado diário abre.
2. **Ligação opção → objeto**, como mudança aditiva da SPEC-0523: gravar no IN o `FinInstrmId` de cada instrumento e o bloco `EqtyInf` (cobre todas as séries), ou guardar o `CODISI` do COTAHIST (cobre só as negociadas no dia). Na mesma mudança cabem os campos que o leitor descarta e que as telas usam: `PricFctr` (ou `FATCOT`), `WrkgDays`, `WdrwlDays`, `TrgtInstrmId`, `SrsTp` e `PrmUpfrntInd`. Sem a ligação, OP-01, OP-03, VL-01, VL-02, VL-04 a VL-07 e a GX ficam sem o preço do objeto.
3. **Gravação diária** (backlog A2 e A3, e E2 junto). Está parada porque a B3 veda coleta automatizada, e a escolha da fonte (UP2DATA da B3, ProfitDLL, download à mão ou assumir o risco) depende do cartão de 05/11, que segue aberto. O BDI guarda cerca de 21 pregões, e as telas OP-07, OP-09, GX-06, VL-03, VL-07, FL-01 e JE-04, além das partes em duas datas da OP-10 e da JE-01, estão bloqueadas por essa decisão.
4. **Motor de agregados e exposições** (backlog B2): as funções da tabela acima.
5. **Vetores ligados ao motor C#.** Os 82 casos de `precificacao.json` e os 12 de `agregados.json` só são conferidos pelo teste Python dos geradores. Antes de virar teste: o caso `iq` precisa ser regenerado sem o bloco `barreiras`, que ainda traz o limiar herdado de material de terceiros (descoberto de 5.000 e índice 1,2); os casos `walls`, `gamma_flip`, `equilibrio_gamma_theta` e `taxas_cdi` precisam de nome próprio (sem os termos comerciais) e de `nota_metodologica` e `fontes` que apontem para as fontes aceitas das telas GX-01, GX-02 e ES-05; e os campos `fontes` de `gex_dex`, `max_pain` e `pcr` também citam páginas fora das aceitas.
6. **Preço executável.** Bid e ask no fechamento (`PREOFC`, `PREOFV` do COTAHIST, ainda não lidos) e o book ao vivo pelo Gateway (backlog D1). Sem isso o buscador da ES-05 não tem entrada.
7. **Fita de opções** para as telas de fluxo (backlog C3). O ponto de partida é o caminho fora de linha que a main já tem (SPEC-0078, 02/10/2026): depois do pregão, a Rotina enfileira um par (opção, Pregão) por série viva com `enqueue-history`, sem mexer na ingestão viva nem na Fita congelada, e a Fita vem com `buy_agent`, `sell_agent` e `aggressor`. Falta ampliar o universo das séries dos Sinais para as séries perto do dinheiro, dentro dos cerca de 30 dias que a DLL guarda. O tempo real dessas séries é o desenho do backlog D1.
8. **Campos a confirmar com mais linhas reais:** qual de `BrrwrQty` e `LndrQty` é titular; `OpnIntrst` contra `TtlPos` nas opções de ações; `DstrbtnId` nas séries de opções; existência de opções sobre futuro de índice e de dólar; fonte do cupom cambial; conteúdo do BVBG.087 e do arquivo `Deltas`; planilhas dos programas de formador; texto do MPO 7.9.1 (alíquota do dividendo no ajuste e eventos em ações).
9. **Termos de uso da B3.** O Hub de dados e a página de proventos vedam coleta automatizada. O backlog atual marca A2, A3 e E2 como PARADOS até a decisão da fonte no cartão de 05/11; a decisão, quando sair, precisa ficar registrada num lugar só e alinhar os índices de conhecimento.

## Convenções em aberto (decisão do Marcelo)

| Convenção | Opções | Padrão proposto | Telas |
|---|---|---|---|
| Sinal das exposições | A, B, D (sem fonte), E (pela Fita) | A | GX, §7 |
| Unidade das exposições | objeto por R$ 1, R$ por R$ 1, R$ por 1 % | R$ por 1 % | GX |
| Vencimentos somados | todos, próximo, até N dias | todos | GX, OP-05 |
| Preço de gamma zero | método 1 (varredura) ou 2 (acumulado) | 1 | GX-02 |
| Concentração de gamma por strike | regra a, b ou c; lado livre ou restrito | b, livre | GX-01 |
| Movimento de empate do hedge com r > 0 | com ou sem financiamento do hedge | em aberto | GX-01, ES-04 |
| Dor máxima | método A ou B | A, com B ao lado | OP-06, OP-07 |
| Razão put/call | OI, volume, financeiro | OI e volume | OP-05 |
| Índice titulares/lançadores | razão de somas ou ponderado | razão de somas | OP-08 |
| Filtro de descoberto perto do preço | faixa h | 10 % | OP-02 |
| Agressão na Fita | tipos 1, 4, 5, 13 e 32 fora da agressão ou com lado por Lee-Ready | fora, com o RLP (13) contado à parte | FL-02, FL-03 |
| Intervalo implícito | com ou sem o termo de drift | sem | VL-05 |
| Theta exibido | Θ/252, Θ/365 ou decaimento exato de 1 DU | Θ/252 | todas |
| Curva | vértices ou DI plano | vértices | todas |
| Dias úteis | B3 para T e ANBIMA para a curva; regra de 24/12 e 31/12 | B3 para T, ANBIMA para a curva | JE-02 e todas |
| "% do CDI" | razão (1) ou estilo CDB (2); CDI da curva ou do dia | as duas; curva | ES-05 |
| Capital da venda de put com garantia em caixa | K − P ou K | K − P | ES-05 |
| Taxa "parada" | pelo ask ou pelo bid | em aberto | ES-05 |
| Modelo do índice e do dólar | Black-76 sobre o futuro ou GK/BSM | Black-76 | §7 |
| Prazo da mini opção de dólar | T da vol até o fixing ou até o vencimento | vol até o fixing, desconto até o vencimento | §7, JE-02 |
| Alíquota do dividendo no ajuste (2026) | a regra já é o valor líquido [OC006VPE]; falta só a alíquota sob a Lei 15.270/2025 | confirmar no MPO 7.9.1 (fato a confirmar, não decisão) | JE-03, JE-04 |

## Referências

**B3 e ANBIMA**

- [MA] B3, *Manual de Apreçamento: Opções*, 20/12/2023. <https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf>
- [MC] B3, *Manual de Curvas*, V21, 12/12/2025. <https://www.b3.com.br/data/files/F3/42/AE/8C/1942B9105B12E5A9AC094EA8/Manual%20de%20Curvas_V21.pdf>
- [NT13] BM&FBovespa, *NT-2013-01: Ajuste de dados de volatilidade implícita por meio da parametrização SVI*. <https://www.b3.com.br/data/files/95/16/EC/5C/42580510FE0C840592D828A8/NT-2013-01-Ajuste-de-dados-de-Volatilidade-Implicita-por-meio-da-parametrizacao-SVI.pdf>
- [DOP] B3, *DerivativesOpenPositionFile*, v1.1, 05/10/2023. <https://b3.com.br/data/files/1E/D1/BA/58/C841B810E9C1AAA8AC094EA8/DerivativesOpenPositionFile%202023.pdf>
- [CAD] B3, *Catálogo de Mensagens: Cadastro de Instrumento* v2.9 (BVBG.028). <https://b3.com.br/data/files/D4/52/03/F5/A86B0A105BF9020AAC094EA8/Catalogo-de-Mensagens-Cadastro-de-Instrumento.pdf>
- [COT] B3, *Layout do COTAHIST* (HistoricalQuotations_B3). <https://www.b3.com.br/data/files/65/50/AD/26/29C8B51095EE46B5790D8AA8/HistoricalQuotations_B3.pdf>
- [PR] B3, *Pesquisa por pregão: descrição dos arquivos* (PE, RE, TS, IR e `Deltas`). <https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/descricao-dos-arquivos/>
- [WS16] B3, *Prêmio de Referência para Opções de Ações*, evento de 14/12/2016. <https://www.b3.com.br/data/files/10/42/D4/6B/F8EF851052122C85790D8AA8/20161214-Premio%20de%20Referencia%20para%20Opcoes%20de%20Acoes%20-%20Evento.pdf>
- [DI] B3, *Programa de treinamento DI: taxas de juros*. <https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/juros/programa-de-treinamento-di/02-taxas-de-juros.htm>
- [CDI] B3, *Boletim Diário do Mercado*, Renda fixa › Indicadores e Informativos › "Taxas – DI PRÉ – Over" (CSV, dado de D−1, histórico desde 06/03/1986), com o *Glossário Taxas DI Over*. Substitui o site da Cetip, desativado em 15/12/2025 (CE 008/2025-VTEC). <https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/boletim-diario-do-mercado/>; <https://www.b3.com.br/data/files/6A/F7/3F/35/2654D9101BEEB2D9AC094EA8/Glossario_Taxas_DI_Over_balcao%204.pdf>; <https://www.b3.com.br/data/files/FA/A2/31/7C/9389A9105B12E5A9AC094EA8/CE%20008-2025-VTEC_MELHORIA%20NO%20ACESSO%20AOS%20DADOS%20HISTORICOS%20DE%20RENDA%20FIXA%20NO%20SITE%20B3_PT.pdf>
- [OC055] B3, OC 055/2024-PRE (contratos futuros de juros, PU e DU ANBIMA). <https://www.b3.com.br/data/files/FF/C5/51/86/158EE810C54843E8DC0D8AA8/OC%20055-2024%20PRE%20Contratos%20FE%20-%20Juros%20%28PT%29.pdf>
- [FM] B3, *Programas de formador de mercado de opções*: página dos programas, OC 031/2026-PRE (regras de atuação) e planilha consolidada de formadores (planilhas não lidas). <https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/formador-de-mercado/programas-listados/opcoes.htm>; <https://www.b3.com.br/data/files/9B/D2/A7/68/CA3BF91094DCD8F9AC094EA8/OC%20031-2026%20PRE%20PRORROGACAO%20PROGRAMA%20DE%20FM%20OPCOES%20SOBRE%20ACOES%20BDRS%20UNITS%20ETFS%20E%20OPCOES%20SOBRE%20%C3%8DNDICES%20COM%20VENCIMENTOS%20MENSAIS_PT.pdf>; <https://www.b3.com.br/data/files/6D/D6/D0/C2/08281A10F2BF771AAC094EA8/Programa%20de%20FM%20Opcoes%20-%20Options%20MM%20Program%20-%20Out%2028%20-%202026.xlsx>
- [ER] B3, *Glossário: Empréstimos Registrados*. <https://b3.com.br/data/files/32/02/C0/25/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Emprestimos_Registrados.pdf>
- [CE068] B3, CE 068/2024-VNC (metodologia da taxa do BTB). <https://b3.com.br/data/files/83/F5/96/95/522239106EEC8429AC094EA8/CE%20068-2024-VNC%20Metodologia_taxaBTB_PT.pdf>
- [NBTB] B3, *Negócio a Negócio: Empréstimos de Ativos (BTB)*, 2023. <https://b3.com.br/data/files/A6/C3/43/9D/3941B810E9C1AAA8AC094EA8/Negocio%20a%20Negocio%20-%20Emprestimos%20de%20Ativos%20-%20btb%202023.pdf>
- [BDI02] B3, *Boletim Diário, capítulo 02: Participação dos Investidores* (exemplo de 21/03/2024). <https://arquivos.b3.com.br/bdi/download/bdi/2024-03-21/BDI_02_20240321.pdf>
- [EVT] B3, *Dividendos e outros eventos corporativos*. <https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/acoes/consultas/dividendos-e-outros-eventos-corporativos/>
- [MPO] B3, *Manual de Procedimentos Operacionais da Câmara B3*, item 7.9.1. <https://www.b3.com.br/data/files/57/86/30/A8/4C8D0A105BF9020AAC094EA8/MPO%20da%20Camara%20B3.pdf>
- [MPEC] B3, *Manual de Precificação de Eventos Corporativos*, v5, 09/01/2023 (`P_com = Q·P_ex` no desdobramento; `P_com = P_ex·(1 + B)` na bonificação). <https://www.b3.com.br/data/files/2C/B0/39/4D/AFA538101E311E28AC094EA8/Manual%20de%20Eventos%20Corporativos.pdf>
- [OC093] B3, OC 093/2022-PRE. <https://www.b3.com.br/data/files/84/E4/55/05/A70628103A654428AC094EA8/OC%20093-2022%20PRE%20Tratamento%20das%20Posi%C3%A7%C3%B5es%20de%20Op%C3%A7%C3%B5es%20sobre%20PETR3%20e%20PETR4%20com%20Pre%C3%A7o%20de%20Exerc%C3%ADcio%20Inferior...%20%28PT%29.pdf>
- [OC141] B3, OC 141/2023-PRE. <https://www.b3.com.br/data/files/44/41/F8/1E/E90E98101D7C7D98DC0D8AA8/OC%20141-2023%20PRE%20Tratamento%20para%20Dividendos%20Superiores%20ao%20Strike_Petrobras%20%28PT%29.pdf>
- [OC026] B3, OC 026/2025-VPE (JCP a 17,5 % desde 2026). <https://www.b3.com.br/data/files/0F/23/BA/E4/1117B9105B12E5A9AC094EA8/OC%20026-2025-VPE%20ATUALIZACAO%20NA%20TRIBUTACAO%20DE%20JCP%20DE%20CONTRATOS%20FUTUROS%20E%20OPCOES%20A%20PARTIR%20DE%202026_PT.pdf>
- [OC006VPE] B3, OC 006/2026-VPE, de 05/03/2026 (eventos em recursos financeiros líquidos de impostos: desde 09/03/2026 o MPO 7.9.1 usa o valor líquido para todo provento em dinheiro, sem tabela fixa de alíquota; lido, [C] na nota `b3-outros/06`). <https://b3.com.br/data/files/3D/25/CE/4A/E9EBC910F37907C9AC094EA8/OC%20006-2026-VPE%20TRATAMENTO%20DE%20EVENTOS%20CORPORATIVOS%20EM%20RECURSOS%20FINANCEIROS%20LIQUIDOS%20DE%20IMPOSTOS_PT.pdf>
- [OC032] B3, OC 032/2026-PRE (prorrogação do programa de incentivo tarifário para operações de box de 3 pontas em opções de ações e ETFs; não lido [S]). <https://www.b3.com.br/data/files/1E/F5/53/51/9C3BF91094DCD8F9AC094EA8/OC%20032-2026%20PRE%20PRORROGACAO%20DO%20PROGRAMA%20DE%20INCENTIVO%20TARIFARIO%20PARA%20OPERACOES%20DE%20BOX%203%20PONTAS%20EM%20OPCOES%20DE%20ACOES%20E%20ETFS%20%28PT%29.pdf>
- [VENC] B3, OC 007/2026-VPC, OC 006/2026-VPC, OC 045/2025-VPC, OC 017/2026-VPC e as páginas de opções sobre Ibovespa e sobre dólar. <https://www.b3.com.br/data/files/05/A1/CA/C2/EFE2C91076A8EEB9AC094EA8/OC%20007-2026-VPC%20ALTERACOES%20CONTRATOSTERMO%20OPCOES%20ACOES%20UNITS%20ETFS%20BDRS%20FUTURO%20ACOES%20UNITS%20REPUBLICACAO%20CONTRATOS%20DERIVATIVOS%20EQUITIES.pdf>; <https://www.b3.com.br/data/files/AC/C5/E4/D2/A4DE9910F5D34899AC094EA8/OC%20045-2025-VPC%20B3%20Novos%20Vencimentos%20das%20Op%C3%A7%C3%B5es%20Semanais%20sobre%20%C3%8Dndice%20Bovespa_PT.pdf>; <https://www.b3.com.br/data/files/6C/B4/07/0B/F996D910973186D9AC094EA8/OC%20017-2026-VPC%20NOVOS%20VENCIMENTOS%20DOS%20MINI%20CONTRATOS%20DE%20OPCOES%20SEMANAIS%20DE%20DOLAR_PT.pdf>; <https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/opcoes-sobre-ibovespa.htm>; <https://b3.com.br/pt_br/produtos-e-servicos/negociacao/moedas/opcoes-sobre-taxa-de-cambio-de-reais-por-dolar-comercial.htm>
- [FER] B3, calendário de negociação de 2026 e OC 054/2025-VNC; ANBIMA, feriados nacionais de 2027 e 2028. <https://www.b3.com.br/pt_br/noticias/calendario-de-negociacao-da-b3-confira-o-funcionamento-da-bolsa-em-2026.htm>; <https://www.anbima.com.br/feriados/fer_nacionais/2027.asp>
- [PRS] B3, *Relação de PRs* e relatórios diários de RLP, fontes B3 de parte das etiquetas de `corretoras-prior.json` (vale só nas etiquetas que os citam). <https://www.b3.com.br/data/files/23/51/B8/A4/7F96D610503056D6AC094EA8/Relacao_PRs.xlsx>
- [ANB] ANBIMA, *Estrutura a termo das taxas de juros (ETTJ)*. <https://www.anbima.com.br/informacoes/est-termo/CZ.asp>

**Outras bolsas**

- [CBOE] Cboe, *Daily Market Statistics* (razões put/call por volume). <https://www.cboe.com/us/options/market_statistics/daily/>

**Repositório Farol (main)**

- [IPC] `src/Contracts/Farol.Protocol/Contracts/IpcMessages.cs`, linhas 577 a 581: `Aggressor` é o `TTradeType` da ProfitDLL, sem conversão. Na main, `src/Research/Farol.Macro.Medicao/TapeQuery.cs` seleciona `aggressor IN (2, 3, 13)`.
- [SPEC0078] `docs/specs/0078-sinais-forward/SPEC.md` e `docs/surfaces/data.md`, seção "2026-10-02 — Fita diária das opções vivas pelo caminho fora de linha (SPEC-0078)".

**Livros**

- [HULL] J. C. Hull, *Options, Futures, and Other Derivatives*, 9ª ed.: cap. 11 (propriedades e paridade), 12 (estratégias e box), 15 (Black-Scholes-Merton, propriedade lognormal, vol histórica e implícita), 17 (índices e moedas), 18 (opções sobre futuro), 19 (gregas), 20 (sorriso). A numeração dos capítulos foi conferida de memória e deve ser checada no livro impresso.
- [HAUG] E. G. Haug, *The Complete Guide to Option Pricing Formulas*, 2ª ed., cap. 1 (Black-Scholes generalizado, Black-76, Garman-Kohlhagen) e cap. 2 (gregas, inclusive as de segunda ordem).

**Artigos**

- [AL03] M. Avellaneda e M. D. Lipkin, "A market-induced mechanism for stock pinning", *Quantitative Finance* 3(6), 2003.
- [BS73] F. Black e M. Scholes, "The pricing of options and corporate liabilities", *Journal of Political Economy* 81(3), 1973.
- [M73] R. C. Merton, "Theory of rational option pricing", *Bell Journal of Economics and Management Science* 4(1), 1973.
- [B76] F. Black, "The pricing of commodity contracts", *Journal of Financial Economics* 3(1–2), 1976.
- [BL78] D. T. Breeden e R. H. Litzenberger, "Prices of state-contingent claims implicit in option prices", *Journal of Business* 51(4), 1978.
- [GK83] M. B. Garman e S. W. Kohlhagen, "Foreign currency option values", *Journal of International Money and Finance* 2(3), 1983.
- [BS88] M. Brenner e M. G. Subrahmanyam, "A simple formula to compute the implied standard deviation", *Financial Analysts Journal* 44(5), 1988.
- [BL90] G. Burghardt e M. Lane, "How to tell if options are cheap", *Journal of Portfolio Management* 16(2), 1990.
- [LR91] C. M. C. Lee e M. J. Ready, "Inferring trade direction from intraday data", *Journal of Finance* 46(2), 1991.
- [DAV02] G. D'Avolio, "The market for borrowing stock", *Journal of Financial Economics* 66(2–3), 2002.
- [LEE04] R. W. Lee, "The moment formula for implied volatility at extreme strikes", *Mathematical Finance* 14(3), 2004.
- [NPP05] S. X. Ni, N. D. Pearson e A. M. Poteshman, "Stock price clustering on option expiration dates", *Journal of Financial Economics* 78(1), 2005.
- [PP06] J. Pan e A. M. Poteshman, "The information in option volume for future stock prices", *Review of Financial Studies* 19(3), 2006.
- [GJ12] B. Golez e J. C. Jackwerth, "Pinning in the S&P 500 futures", *Journal of Financial Economics* 106(3), 2012.
- [GJ14] J. Gatheral e A. Jacquier, "Arbitrage-free SVI volatility surfaces", *Quantitative Finance* 14(1), 2014. <https://arxiv.org/abs/1204.0646>
- [J15] P. Jäckel, "Let's be rational", *Wilmott*, 2015.
- [BR73] R. P. Brent, *Algorithms for Minimization without Derivatives*, Prentice-Hall, 1973.
- [BB] A. Barbon e A. Buraschi, "Gamma fragility", working paper, 2020.
- [BDLM21] G. Baltussen, Z. Da, S. Lammers e M. Martens, "Hedging demand and market intraday momentum", *Journal of Financial Economics* 142(1), 2021.
- [NPPW21] S. X. Ni, N. D. Pearson, A. M. Poteshman e J. White, "Does option trading have a pervasive impact on underlying stock prices?", *Review of Financial Studies* 34(4), 2021.

## Proveniência

- **Lido:** `conhecimento/README.md`, `b3-opcoes/`, `b3-outros/` e `metodologia/` (sem os trechos [Q]); `pesquisa/fontes-dados.md`, `farol-dados.md`, `farol-opcoes-portal.md` e `meusagentes.md`; `backlog.md`; no branch, as SPEC-0523 e SPEC-0524, `tests/fixtures/opcoes/README.md`, o código de `Modules/Options/` e de `Farol.DataHub/B3Daily/` e as fixtures públicas de 03/11/2026 em `tests/Services/Farol.DataHub.Tests/Fixtures/B3Daily/`.
- **Lido na revisão de 05/11/2026:** no branch, `B3InstrumentFile.cs`, `B3TextFiles.cs`, `B3BdiTable.cs`, `B3DailyReader.cs`, `B3DailySnapshot.cs`, `Catalog/B3DailySchema.cs`, `EuropeanOptionPricing.cs`, `OptionValuation.cs` e `RawSviParameters.cs`; as fixtures `in.xml`, `cotahist.txt`, `positions.json` e `positions-dol.json`; os casos `payoff`, `iq`, `walls`, `gamma_flip`, `equilibrio_gamma_theta`, `taxas_cdi`, `gex_dex`, `max_pain` e `pcr` de `agregados.json`; `docs/base-de-conhecimento/fluxo-winfut/corretoras-prior.json`; `AGENTS.md` e `CONTEXT.md`. Na main, `docs/surfaces/data.md` (seção de 2026-10-02), `docs/specs/0078-sinais-forward/SPEC.md`, `IpcMessages.cs` e `TapeQuery.cs`. No conhecimento, `b3-outros/02`, `05`, `06`, `08` e `vencimentos-regras.md`, e `b3-opcoes/01`, `02` e `08`.
- **Não lido:** as pastas e arquivos em quarentena e os sites de terceiros que a regra exclui.
- **Números conferidos** com script próprio em Python (`python3 -I`, só biblioteca padrão): preço e gamma da call de referência, GEX do exemplo, movimento de empate do hedge com e sem juros, box de 3 pontas, dor máxima do vetor, Black-76 do IND e GEX por contrato com m = 1 e com m = 0,01, Garman-Kohlhagen do DOL, identidade da quebra da BBSEW441 e as contagens de dias úteis da JE-02. Na revisão: DU de INDZ26, DI1F27 e DOLN27C005300 contra `WrkgDays` e `WdrwlDays`; `FATCOT`, `CODISI` e VOLTOT/QUATOT do COTAHIST; forma exata da taxa total da venda de put com garantia; densidade da SVI contra Breeden-Litzenberger; faixas, straddle e `N(d2)` do exemplo da VL-05; inclinações e marcas do vetor `payoff`; contagens de `corretoras-prior.json`. Todos bateram com os valores citados.

## Notas da revisão

A revisão de 05/11/2026 tratou os 30 itens da lista de problemas. Nenhum item foi recusado inteiro. Os pontos abaixo registram onde a correção se afastou da proposta, ou foi além dela, e por quê.

1. **Nome da GX-02.** A proposta era "Nível de gamma zero" e `ZeroGammaLevel`. O `CONTEXT.md` reserva **Nível** para o preço de referência do dia calculado com negócios até o minuto da Leitura, e a regra do glossário é uma palavra para cada trabalho. Por isso a tela se chama "Preço de gamma zero", e a função, `ZeroGammaPrice.Find`. Os outros nomes propostos (`GammaConcentration`, `HedgeBreakevenMove`, "Concentração de gamma por strike" e "Movimento de empate do hedge") foram adotados como estavam.
2. **Filtro do buscador único.** A proposta dizia "a estratégia como filtro". O `CONTEXT.md` reserva **Estratégia** para regras de operação com parâmetros e versão, então a ES-05 usa "tipo de estrutura" como filtro.
3. **Códigos.** Para não quebrar referências, nenhum código foi renumerado. Os códigos que saíram (OP-04, GX-03, GX-04, FL-04, ES-06 a ES-09 e ID-01 a ID-04) ficam sem uso, e as telas novas recebem o próximo número livre do tema. A ordem do índice segue a dependência entre as telas.
4. **Tema da cadeia.** O tema passou a se chamar "Cadeia e posição em aberto", como proposto, mas o backlog C1 ainda diz "Opções" e precisa ser alinhado por quem cuida do backlog; este arquivo não o altera. A observação de que a OP-04 deveria vir antes da OP-08 deixou de valer, porque a OP-04 virou filtro da OP-02, e o filtro não usa o índice titulares/lançadores.
5. **Destino da FL-04.** O item só dizia que aluguel não é fluxo de negócios. A tela foi para "Juros e eventos" como JE-05, porque a taxa de aluguel entra como custo de carregamento do objeto. Se o Marcelo preferir outro tema, basta mover a linha.
6. **Filtro da OP-02.** O filtro "descoberto alto perto do preço" ficou só com a faixa h e a ordenação pelo descoberto. Ele não usa percentil nem o índice titulares/lançadores, para não carregar o limiar da tela antiga com outros números.
7. **Ligação opção → objeto.** Além das telas listadas no item, a marca entrou também na OP-03, na OP-10, no filtro da OP-02, na GX-07 e nas telas novas VL-05 a VL-07, porque todas usam S. A OP-05 e a OP-06 continuam como "dado pronto", com a observação de que as variantes por delta e a distância ao preço usam S.
8. **Multiplicador.** A regra geral escrita é "valor por opção = prêmio dividido pelo `PricFctr`", que dá 1 nas ações e R$ 0,01 por ponto no IBOV e bate com o `FATCOT` do COTAHIST. Essa generalização vem das duas linhas da fixture e deve ser conferida com mais séries.
9. **Fontes de nível do índice e de deltas.** O BVBG.087 (IR) só foi visto em código de terceiros, e o arquivo `Deltas` só tem o nome confirmado. Os dois entraram como fonte a confirmar, e não como fato.
10. **Agressor.** Além dos tipos citados no item, a regra inclui o 5 (vigilância), que também aparece no comentário de `IpcMessages.cs`. O padrão proposto para os tipos sem lado, inclusive o RLP, é ficar fora da agressão, com o RLP contado à parte; a alternativa por Lee-Ready continua como escolha.
11. **Fontes acrescentadas além das propostas.** A VL-05 cita também Brenner e Subrahmanyam [BS88] para a relação entre o straddle ATM e σ·√T. A VL-03 e a VL-08 ganharam o aviso de que os preços do COTAHIST não são ajustados por proventos.
12. **Vetores.** O item 3 pedia para regenerar o caso `iq` sem o bloco `barreiras`. Esse caso fica em `tests/fixtures/opcoes/agregados.json`, no branch, e a cópia do repositório usada nesta revisão é só de leitura. Por isso o catálogo não regenera vetores; a regeneração fica para quem mexer no branch. A pendência 5 lista o que cada caso precisa antes de virar teste, inclusive o bloco `barreiras` do caso `iq` e os nomes e fontes dos casos `walls`, `gamma_flip`, `equilibrio_gamma_theta` e `taxas_cdi`.
13. **Termo "exposição".** O `CONTEXT.md` define **Exposição** como a posição agregada por Instrumento e por carteira, valorizada a mercado. O tema "Gamma e exposição" e as siglas GEX e DEX usam a palavra em outro sentido. Como o tema vem do backlog C1, o nome ficou, mas o conflito merece decisão do dono.
