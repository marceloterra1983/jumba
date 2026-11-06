# Réplica do Jumba (uso próprio): matriz, dados, motor de cálculo e ondas

O texto se baseia nos seis achados recebidos. **[S]** marca suposição ou inferência, e **[C]** marca o que foi confirmado em fonte pública ou no repositório.

**Legenda das fontes**

- **CAD**: B3 BDI `InstrumentsDerivatives`, com ExrcPric, XprtnDt, OptnTp, OptnStyle e UndrlygTckrSymb1.
- **OI**: B3 BDI `OpenPositionsEquities`, com OpnIntrst, VartnOpnIntrst, CvrdQty, UcvrdQty, TtlBlckdPos e TtlPos. **Não traz o strike.**
- **NEG**: B3 BDI `ConsolidatedTradesDerivatives`.
- **TS**: arquivo da B3 "Taxas de Mercado para Swaps" (`TS<aammdd>.ex_`) e BVBG.086.
- **BTB**: `NEGOCIOSBTB.zip` mais a posição em aberto de aluguel.
- **BDI-PI**: seção "Participação dos Investidores" do PDF do BDI.
- **DLL-T**: `SubscribeTicker`/`SetTradeCallbackV2`, com nBuyAgent, nSellAgent e nTradeType.
- **DLL-B**: `SubscribeOfferBook` e `SubscribePriceBook`.
- **DLL-ADJ**: `SubscribeAdjustHistory`.
- **Calc**: o motor próprio descrito na seção 3.
- **Hist**: foto diária gravada por nós.

Todo acesso à ProfitDLL passa pelo Gateway gRPC (`MarketData.Subscribe` e `History.DownloadTrades`), nunca direto pela DLL.

**Legenda das evidências no Farol**

- **F-SCR**: `Python/b3_scraper_linux.py` já baixa CAD, NEG e OI para `/srv/charlie/finance/scrapper/artifacts/scrapper/B3/Derivativos`. Nenhum código lê o OI (`src/Web/Farol.Portal/Modules/ScrapperEndpoints.cs:146`).
- **F-FITA**: a Fita guarda `buy_agent`, `sell_agent` e `aggressor` (`src/Services/Farol.DataHub/Storage/ParquetTradeStore.cs:106`). Existem também `TradeFlowAgent`, o footprint e a rota `/api/fluxo/vivo/corretoras`.
- **F-CHAIN**: `Host/Services/OptionChainReader.cs` e `OptionChainScan.cs`. Só aparecem em testes.
- **F-CAL**: `Backtest/OptionExpiry.cs` (vencimento e pregões restantes), `TickerClassifier.ParseOption` e o padrão de `OperacaoOpcaoCalculadora.cs`.
- **F-ADJ**: `OnAdjustHistoryV2` (`Host/Services/ProfitService.cs:4137`) recebe os ajustes, mas não os grava.
- **F-DI**: `HistoryDownloadPolicy.IsJurosTicker` e `MacroReadingSources.cs`, que lê DI1F27 e DI1F29 com a nota "convenção não validada".
- **F-CORR**: `docs/base-de-conhecimento/fluxo-winfut/corretoras-prior.json`.
- **"não"**: não existe nada. O grep de `black|scholes|vega|theta|implied` em `src`, `scripts` e `Python` voltou vazio.

**Legenda de frequência:** D = diário (D‑1); D+i = diário, recalculado durante o dia com o preço do ativo; TR = tempo real; 1×P = uma vez por pregão; SD = sob demanda.

---

## 1. Matriz das telas

### Jumba Pro

| Tela | O que mostra | Dados de entrada | Fonte primária | Já existe no Farol? | Freq. | Confiança |
|---|---|---|---|---|---|---|
| Mapa de Opções | OI por strike de calls e puts (coberta, descoberta, travada), titulares e lançadores, IQ, para mais de 80 ativos [C] | séries, OI por série, preço do ativo | CAD + OI; preço via DLL-T | parcial (F-SCR) | D | Alta para a tela; baixa para titulares e lançadores |
| Resumo do Mapa | Consolidado por ativo e vencimento: OI, % descoberto, strikes de maior OI, variação contra D‑1 [S] | o mesmo do Mapa + D‑1 | CAD + OI + Hist | parcial (F-SCR) | D | Média |
| Market Gamma Bands | Faixas no gráfico (flip e picos de GEX), exportáveis para o Profit [C nome, S cálculo] | OI, preço, vol implícita (VI), taxa r, prazo T, dividendos | Calc (GEX) | não | D+i | Média |
| BGT Bands | Sem descrição pública; talvez bandas por gamma e theta [S] | as mesmas + theta | Calc | não | ? | Baixa |
| Market Gamma e Jumba Walls | GEX por strike, GEX acumulada, flip e walls no mesmo gráfico | OI, preço, VI, r, T | Calc (GEX + Walls) | não | D+i | Média‑alta |
| Shark Map | Negócios grandes e diretos por corretora e por série [C conceito] | Fita de ações e opções com agentes e tipo de negócio | DLL-T (DLL-H para até 30 dias) | parcial (F-FITA; a Fita de opções está fora do universo) | TR | Média |
| Shark Positions | Estruturas de várias pernas reconstruídas e posição líquida por player [S] | Fita + VartnOpnIntrst | DLL-T + OI | parcial (F-FITA) | TR + D | Baixa |
| Volatilidade | Smile de VI por vencimento, ajustado (SVI) [C "curva ajustada"] | prêmios, preço, r, T | Calc (VI + SVI) sobre DLL-B ou NEG | não (só a superfície de dólar, que vai para o Google Sheets e está parada em produção) | TR / D | Média |
| Histórico de Volatilidade Implícita | VI ATM ao longo do tempo, IV Rank, comparação com a vol histórica [S] | foto diária da VI, preços do ativo | Hist + Calc; passado aproximado pelo COTAHIST | não | D | Média |
| Resumo do Gamma | Ranking por ativo: GEX total, flip, walls, regime [S] | GEX de todos os ativos | Calc | não | D+i | Baixa‑média |
| Gamma Score | Nota normalizada para comparar ativos; metodologia desconhecida [S] | GEX histórica, volume médio diário (ADV) | Calc + Hist | não | D | Baixa |
| Scanner de Barreiras | Strikes com muito OI, principalmente descoberto, perto do preço [S] | OI, CAD, preço | CAD + OI | parcial (F-SCR) | D | Média |
| Put/Call Ratio (PCR) | Razão puts/calls por OI e por volume, por ativo e vencimento | OI e volume por série | OI + NEG (ou DLL-T) | parcial (F-SCR) | D | Alta |
| Índice de Qualidade (IQ) | Titulares ÷ lançadores por série, agregado por ativo [C fórmula, Clube do Pai Rico] | nº de titulares e de lançadores | **sem fonte confirmada** (os campos não estão no glossário do OI) | não | D | Média na fórmula, baixa no dado |
| Fluxo de Investimentos | Saldo por tipo de investidor (estrangeiro, institucional, pessoa física) | participação por tipo de investidor | BDI-PI (acumulado no mês) | parcial (F-CORR como aproximação; a SPEC-0021 concluiu que não há série diária gratuita) | D, com defasagem | Média |
| Mercados de Aluguel | Taxas doadora e tomadora, saldo alugado, histórico | negócios e posição de aluguel | BTB | não | D | Média |
| Eventos Corporativos | Proventos e desdobramentos e o efeito nas opções | eventos | DLL-ADJ; conferência pelo CVM IPE | parcial (F-ADJ) | por evento | Média |
| Market Exposure | Exposição em delta (DEX) dos market makers, por strike e total [S] | OI, preço, VI | Calc (DEX) | não | D+i | Baixa |
| Jumba Walls | Suporte e resistência definidos no início do pregão, exportáveis para o Profit [C] | perfil de GEX | Calc (Walls) | não | 1×P | Média‑alta |
| Histórico de Ajustes de Strikes | Registro de strike antigo → strike novo, por série e data [S] | CAD de D e de D‑1, eventos | comparação do ExrcPric no CAD + DLL-ADJ | não (o CAD diário já baixado permite começar) | D | Média |
| Histórico do Market Exposure ATM | Série temporal de DEX/GEX na faixa de ±2–5% do preço [S] | fotos diárias de OI e gregas | Hist + Calc | não | D | Baixa |
| Max Pain | Strike que minimiza o valor intrínseco pago | OI, CAD | Calc | parcial (F-SCR) | D | Alta (conceito padrão) |
| Max Pain History | Evolução diária do Max Pain comparada ao preço | OI histórico | Hist | não | D | Média |
| Curva de Juros | Curva pré, comparada com D‑1, uma semana e um mês; fornece o r do BSM | ajustes do DI1, taxas | TS (fechamento) + DI1 via DLL-T (intradiário) | parcial (F-DI; não há curva montada) | D+i | Média |

### Jumba Trader: IND e DOL

| Tela | O que mostra | Dados de entrada | Fonte primária | Já existe no Farol? | Freq. | Confiança |
|---|---|---|---|---|---|---|
| Mapa de Opções | OI por strike das opções sobre IND e DOL, contra o futuro | CAD, OI, preço do futuro | CAD + OI (mesmo segmento [S]) e futuro via DLL-T | parcial (`TickerClassifier`), mas `category:OPCOES-FUTUROS` está na denylist (SPEC-0009) | D | Média |
| Jumba Walls | Linhas azuis no início do pregão, exportáveis para o Profit [C] | perfil de GEX por Black‑76 | Calc | não | 1×P | Média |
| Market Gamma | GEX por Black‑76, com zonas de alta e baixa vol [C conceito] | OI, preço do futuro, VI, r | Calc | não | D+i | Média |

### Jumba Trader Flow

| Tela | O que mostra | Dados de entrada | Fonte primária | Já existe no Farol? | Freq. | Confiança |
|---|---|---|---|---|---|---|
| Jumba Trader Flow | Saldo de Market Makers, Smart Money e Varejo [C grupos] | Fita com agentes e agressor; classificação de corretoras | DLL-T | **sim para os dados** (F-FITA, F-CORR, `scripts/research/fluxo/`); faltam os 3 grupos e a interface | TR | Média‑alta |
| Trader Flow — TradingView | O Flow e as Walls sobre um gráfico de candles [C Advanced Charts] | candles, série do Flow | `bars/v1` e `WatchLiveCandles` | parcial (`lightweight-charts` 5.2.1 no Portal) | TR | Média |
| Trader Flow Beta | Sem informação pública | ? | ? | não | ? | Baixa |

### Research

| Tela | O que mostra | Dados de entrada | Fonte primária | Já existe no Farol? | Freq. | Confiança |
|---|---|---|---|---|---|---|
| Quick Trade | Bloqueada na conta | — | — | — | — | Fora do escopo |

### Find Your Trade

| Tela | O que mostra | Dados de entrada | Fonte primária | Já existe no Farol? | Freq. | Confiança |
|---|---|---|---|---|---|---|
| Todas as Estruturas | Scanner de mais de 40 estruturas a preço executável: custo, ganho e perda máximos, breakevens, retorno contra o CDI | cadeia de opções, bid/ask, r | CAD + DLL-B + Calc | parcial (F-CHAIN monta travas, mas não roda em produção) | TR | Média |
| Estruturas Salvas | Favoritas com alerta de preço [C] | estruturas salvas, preço ao vivo | Calc + agente do MeusAgentes (`whatsapp_out`) | não | TR | Média‑alta |
| Volatilidade | Curva de VI ajustada para os 9 ativos do FYT [C] | prêmios, preço, r, T | Calc (VI + SVI) | não | TR | Média |
| Payoff | Resultado no vencimento e em D+n | pernas, VI, r | Calc | não | SD | Alta |
| Calculadora BSM | Preço teórico, gregas e VI | preço, strike, T, r, σ, dividendos | Calc; T vem da F-CAL | não (o padrão F-CAL serve) | SD | Alta |
| Payoff de Estruturas | Soma das pernas, breakevens, máximos | pernas | Calc | não | SD | Alta |
| Delta Estrutural | Σ qtd × Δ e como varia com o preço | gregas, pernas | Calc | não | TR | Média |
| Venda Coberta | Buscador: taxa, proteção, retorno se exercido, anualizado [C buscador] | preço, bid das calls, r | CAD + DLL-B + Calc | não | TR | Alta |
| Cash Put | Venda de put com o caixa aplicado no CDI | bid das puts, r | o mesmo | não | TR | Alta (não está na página pública) |
| Box 3 Pontas | Ação + compra de put K + venda de call K; taxa contra o CDI [C buscador] | ask da ação, ask da put, bid da call | o mesmo | não (há peças em F-CHAIN) | TR | Alta |
| Box 4 Pontas | Trava de alta com calls + trava de baixa com puts [C buscador] | 4 pernas | o mesmo | não | TR | Alta |
| Long Collar | Ação + compra de put K1 + venda de call K2 | preço, put, call | o mesmo | não | TR | Alta (supõe que seja o "Collar" [S]) |

---

## 2. Camadas de dados

| Dataset | Fonte | Quem coleta | Onde guarda | Freq. |
|---|---|---|---|---|
| **D1 Cadastro de séries** (strike, vencimento, tipo, estilo, objeto, multiplicador) | CAD. DLL-INFO completa validade e multiplicador, mas **não traz strike** | Scraper do Farol já existente (`farol-b3-scraper-linux`, job `derivativos`, às 18h30, 19h e 19h30, na vps1) mais uma rotina nova para interpretar os arquivos | Bruto: a pasta do F-SCR. Normalizado: Parquet em hive na zona Vivo (`/srv/data2/farol`) **[proposta]** | D (de manhã e à noite) |
| **D2 OI diário por série** | OI, ligado ao D1 pelo TckrSymb. A testar: `nContratosOpen` da DLL | O mesmo scraper mais a rotina de interpretação | o mesmo, **gravado todo dia** (a B3 guarda só cerca de 21 pregões) | D‑1 |
| **D3 Prêmios e negócios de opções** | Diário: NEG (COTAHIST para anos passados, sem OI). Intradiário: DLL-B e DLL-T para um subconjunto de séries | B3: scraper. Intradiário: Host → Gateway | DataHub (Fita e bars) e Parquet de NEG | D / TR |
| **D4 Preço do ativo-objeto** | DLL-T e a Fita | Host → DataHub (já existe para cerca de 91 a 96 tickers). Faltam os objetos novos, incluídos pelo TICKADM (`POST /api/datahub/tickers`) | `trades/v1` e `bars/v1` | TR |
| **D5 VI e gregas** (foto diária + cálculo ao vivo) | Calc sobre D1 a D4 e D6 | Rotina nova `snapshot-opcoes-diario` no MeusAgentes **[proposta]**, depois do D2 | Parquet `greeks/v1` **[proposta]** | D + TR (em memória) |
| **D6 Curva DI** | TS e BVBG.086 para o fechamento; DI1 pela DLL para o intradiário; ANBIMA ETTJ para conferir | Rotina `coleta-curva-di` no MeusAgentes. DI1 ao vivo pelo Gateway, depois de incluir no TICKADM | Parquet `curva-di/v1` | D+i |
| **D7 Aluguel** | BTB (taxas no mesmo dia; posição em D‑1) | Rotina `coleta-btb` | Parquet `btb/v1` | D |
| **D8 Eventos e ajustes** | DLL-ADJ, comparação do ExrcPric no D1 entre D e D‑1, CVM IPE | Host (falta gravar o F-ADJ e expor por IPC/gRPC) + rotina de comparação | Parquet `eventos/v1` | por evento / D |
| **D9 Fluxo por tipo de investidor** | BDI-PI | Rotina (ler PDF exige dependência nova, que precisa de aprovação) | Parquet | D |
| **D10 Fluxo por corretora intradiário** | DLL-T (agentes e agressor) e livro | Host → DataHub (**já existe**; o caminho está congelado pelo ADR‑0040) | Fita; o livro só para WINFUT e INDFUT | TR |
| **D11 Estruturas salvas e alertas** | usuário | Portal; alerta por agente do MeusAgentes | Banco do módulo **[proposta]** | TR |

**Agentes no MeusAgentes**

Primeiro o dono precisa decidir se cria um projeto `farol` novo. Hoje existem só `dev`, `charlie` e `teste-runner`.

Rotinas (tipo `rotina`, começando em `shadow`):
- interpretação de CAD, OI e NEG;
- `snapshot-opcoes-diario`;
- `coleta-curva-di`;
- `coleta-btb`;
- `comparar-cadastro`.

Vigia:
- `vigia-jumba`, às 22h em dias úteis. Confere frescor de D1 a D10, avisa pelo WhatsApp (`whatsapp_out`, destinatário `DONO`) e observa o scraper como `systemd-observed`, porque o scraper já tem timer próprio no systemd.

A gravação no DataHub tem duas restrições: o DataHub é o único escritor da História, e cada DuckDB tem um só escritor. Por isso sugiro que as rotinas deixem os arquivos numa pasta de entrada e um único ingestor os grave **[proposta]**.

---

## 3. Motor de cálculo compartilhado

Cálculo puro, sem I/O e testável, no padrão de `OperacaoOpcaoCalculadora.cs`:

1. **Calendário e prazo** (dias úteis/252, `OptionExpiry.cs`, `B3Holidays`) → todas as telas que usam T.
2. **Junção cadastro × OI** (chave TckrSymb) → Mapa (Pro e IND/DOL), Resumo do Mapa, Scanner, PCR, Max Pain, toda a família GEX/DEX.
3. **Preço e gregas**: BSM‑Merton com dividendos para ações, Black‑76 para IND/DOL. Calcula Δ, Γ, ν, Θ, ρ → Calculadora BSM, Payoff (antes do vencimento), Delta Estrutural, GEX e DEX.
4. **Vol implícita** por Newton‑Raphson ou Brent, sobre o meio do book ou o fechamento → Volatilidade (Pro e FYT), Histórico de VI, GEX.
5. **Ajuste do smile** por SVI (nota técnica da B3 NT‑2013‑01) → "Curva Ajustada" e VI para séries sem negócio. Alimenta GEX, Bands e Exposure.
6. **GEX por strike, acumulada e flip**, com a convenção de sinal configurável [S] → Market Gamma (Pro e IND/DOL), Market Gamma e Walls, Gamma Bands, BGT Bands, Resumo do Gamma, Gamma Score.
7. **Walls** (call wall, put wall, maiores \|GEX\|) com exportação para o Profit → Jumba Walls (Pro e IND/DOL), Market Gamma e Walls, Resumo do Gamma, Trader Flow — TradingView.
8. **DEX (Market Exposure)** → Market Exposure e Histórico do Market Exposure ATM.
9. **Max Pain** → Max Pain e Max Pain History.
10. **PCR** por OI e por volume → PCR.
11. **IQ** (titulares/lançadores) → IQ, Mapa, Resumo do Mapa. Depende de dado sem fonte.
12. **Agregações de OI** (coberta, descoberta, travada, variação contra D‑1, top‑N por distância do preço) → Mapa, Resumo do Mapa, Scanner de Barreiras, Shark Positions.
13. **Detector de negócios grandes e diretos, com saldo por agente** → Shark Map e Shark Positions.
14. **Classificação de corretoras** (F-CORR) em Market Makers, Smart Money e Varejo → as três telas do Trader Flow e a aproximação do Fluxo de Investimentos.
15. **Payoff de várias pernas** (no vencimento e em D+n), breakevens, máximos → Payoff, Payoff de Estruturas, Todas as Estruturas, Estruturas Salvas, Venda Coberta, Cash Put, Box 3, Box 4, Long Collar.
16. **Taxa implícita anualizada contra o CDI** → Venda Coberta, Cash Put, Box 3, Box 4, Long Collar, Todas as Estruturas.
17. **Scanner combinatório a preço executável** (compra no ask, vende no bid) → Todas as Estruturas e os buscadores.
18. **Interpolação da curva DI** (flat‑forward 252) → Curva de Juros e o r de todos os cálculos.
19. **Comparação do cadastro** (ExrcPric em D contra D‑1) → Histórico de Ajustes de Strikes e Eventos Corporativos.
20. **Vol histórica e IV Rank** → Histórico de VI.

---

## 4. Ordem sugerida

**Onda 1: base diária da B3 e calculadoras (cerca de 15 telas)**
- **Dados:** D1, D2 e NEG (que o Farol já baixa), D4 e uma versão simples do D6. Do motor: itens 1, 2, 3, 9, 10, 12, 15, 16 e 18.
- **Telas:** Mapa de Opções (Pro e IND/DOL), Resumo do Mapa, Scanner de Barreiras, PCR, Max Pain, Curva de Juros, Calculadora BSM, Payoff, Payoff de Estruturas, Delta Estrutural.
- **Gravação desde o primeiro dia:** fotos diárias de OI e do cadastro.
- **Por que primeiro:** é o maior número de telas com dados que já chegam ao disco, sem tempo real nem mudança no Host. Além disso, toda tela de histórico depende de começar a gravar cedo: a B3 guarda cerca de 21 pregões e a DLL, 30 dias.

**Onda 2: gregas sobre a cadeia (cerca de 11 telas)**
- **Motor:** itens 4 a 8, primeiro com o fechamento do NEG e depois recalculados durante o dia com o preço da DLL. Começa a foto diária D5.
- **Telas:** Market Gamma (Pro e IND/DOL), Market Gamma e Walls, Jumba Walls (Pro e IND/DOL), Gamma Bands, Resumo do Gamma, Market Exposure, Volatilidade (diária).
- **Por quê:** reaproveita D1 e D2. O único dado novo é o preço por série, que o NEG já traz.

**Onda 3: tempo real e fluxo (cerca de 13 telas)**
- **Trader Flow:** as três telas, usando F-FITA e F-CORR, que já existem.
- **Shark Map e Shark Positions:** exigem incluir a Fita de opções no universo.
- **FYT ao vivo:** Todas as Estruturas, Venda Coberta, Cash Put, Box 3, Box 4, Long Collar, Volatilidade do FYT e Estruturas Salvas com alerta. Isso exige ligar o `OptionChainReader` a IPC/gRPC no Host, respeitando o limite de assinaturas. Para isso, os 9 ativos do FYT, só as séries perto do dinheiro.
- **Por quê:** depende de mudanças no Host e na coleta. O Trader Flow pode até ser adiantado, porque os dados já existem.

**Onda 4: periféricas, proprietárias e históricos (cerca de 13 telas)**
- **Periféricas:** Aluguel (D7), Eventos Corporativos e Histórico de Ajustes (D8), Fluxo de Investimentos (D9).
- **De metodologia própria do Jumba:** IQ, Gamma Score, BGT Bands, Trader Flow Beta. Dependem de ver as telas com a conta logada.
- **Históricos:** Histórico de VI, Max Pain History, Histórico do Market Exposure ATM. A essa altura já haverá fotos acumuladas.

---

## 5. Riscos e lacunas

**Termos de uso e licença**
- **A B3 proíbe coleta automatizada**, inclusive para uso próprio ([hub](https://www.b3.com.br/pt_br/dados/hub-de-dados-publicos/)). O Farol já baixa o BDI por robô (`b3_scraper_linux.py:73–84`, `1565–1593`). Cabe ao Marcelo decidir. As alternativas licenciadas são a ProfitDLL e o UP2DATA, que é pago.
- **Jumba:** só observar as telas na conta dele, sem copiar código nem dados. O módulo deve ter nome próprio, sem a marca.

**Dados sem fonte gratuita clara**
- **Titulares e lançadores (IQ e Mapa):** os campos não estão no glossário do arquivo de OI. Talvez apareçam só na consulta em tela de opções da B3 [S].
- **Histórico de OI com mais de cerca de 21 pregões:** só existe pelo UP2DATA, que é pago, ou gravando a partir de agora.
- **Fluxo diário por tipo de investidor em derivativos:** não há série gratuita (SPEC‑0021).
- **Curvas, superfície de vol e eventos pelo UP2DATA:** a gratuidade não foi confirmada.
- **Histórico do arquivo TS e do BVBG.086:** a página da B3 deu erro.
- **ANBIMA:** os termos de uso não foram verificados.

**ProfitDLL**
- Histórico de negócios só dos **últimos 30 dias**. Para WIN/WDO, cada janela precisa ter menos de 10 dias. Séries de opções vencidas não são servidas.
- A ficha do ativo (`RequestTickerInfo`) **não traz strike**.
- **Não há gregas na DLL.** `GetTheoreticalValues` é o preço teórico de leilão.
- Os recursos dependem do plano (`NL_LICENSE_NOT_ALLOWED`). Ainda não se sabe se a licença cobre aluguel e opções sobre futuro.
- Conexão: 3 tentativas a cada 15 minutos, um único dono da DLL e um processo por sessão.
- **Limite de 256 assinaturas por identidade no Gateway** (`GatewayOptions.cs:50`). Não dá para ter tempo real em todas as séries de mais de 80 ativos. A GEX intradiária precisa usar o preço ao vivo com a VI da foto do dia anterior ou do smile.
- A testar na conta: se `nContratosOpen` vem preenchido em opções.

**Telas que dependem de ver o Jumba logado**
- BGT Bands, Gamma Score, a agregação do IQ, Shark Map e Shark Positions, Trader Flow Beta, a convenção de sinal da GEX e o Resumo do Gamma.
- As páginas `pages.jumba.com.br/*` deram erro.

**Arquitetura do Farol**
- A réplica tem de ser **só leitura**. `NoOrderCallerTests` e `LiveOrderPathGuardTests` protegem o caminho de ordens, e o FYT deve ficar como calculadora.
- ADR‑0040 congela o caminho de ingestão da Fita. Vale a regra de um escritor por DuckDB.
- A configuração de mTLS e capabilities é protegida no servidor.
- No Portal, as 24 páginas do Jumba Pro não cabem em abas numa linha só. Proposta: vários tabsets no rail.
- Não há biblioteca de gráfico com eixo por strike. Será preciso Canvas/SVG próprio ou uma dependência nova. A CSP bloqueia CDNs.

**MeusAgentes**
- Não existe projeto `farol`.
- O dono aprova cada ativação, mesmo em `shadow`. O modo `shadow` só bloqueia a Entrega, então o próprio script precisa proteger os seus efeitos.
- Dependências novas precisam de aprovação. Isso pesa para ler PDF e o arquivo `.ex_`.

**Divergências entre os achados**
1. **Fita de opções de ações.** O farol-dados diz que as opções estão fora do universo: OPCOES-ETF só até 14/07/2026 e as opções de IBOV antigas fora da migração. O farol-opcoes-portal diz que o universo diário inclui opções com negócio, que só as opções sobre futuro e sobre juros entraram na denylist, e que 881 tickers continuam gravados (com só 5 pregões na Fita viva, ADR‑0039). É preciso conferir no `ticker-modes.json` e na denylist.
2. **Cadastro das opções de ações.** O farol-dados supõe que `InstrumentsDerivatives` não cobre opções de ações. O fontes-dados mostra campos de opção (ExrcPric, OptnTp) no glossário do arquivo consolidado. A testar.
3. **Arquivo de OI.** O que o Farol baixa tem cerca de **400 B**, ou seja, está quase vazio. A rota, a paginação ou o segmento podem estar errados. Antes da Onda 1 é preciso investigar.
4. **Onde roda o Host.** O MeusAgentes supôs uma VM Windows. O Farol diz Wine na vps1 (ADR‑0027; PC Windows desativado em 24/09/2026). Vale o Farol.
5. **Agentes de corretora na DLL.** O jumba-pro marcou como suposição. O repositório confirma que a Fita os grava.
6. **Horário da coleta.** O scraper roda às 18h30, 19h e 19h30; a minuta de agente propôs 20h30. É preciso alinhar com a publicação dos arquivos pela B3.
7. **Superfície de dólar e indicadores.** Existem no código, mas não rodam em produção (falta o Playwright; drop-in `10-derivativos-only.conf`).