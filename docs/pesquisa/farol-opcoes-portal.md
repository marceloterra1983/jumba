# Farol: o que já serve para a réplica do Jumba

Fiz só leitura de `/home/claude/Farol` e não alterei nada. O Farol já tem a cadeia de dados (B3, ProfitDLL, DataHub e Portal) e o fluxo por corretora. **Não tem nada de gregas, volatilidade implícita, Black-Scholes, aluguel nem fluxo de estrangeiros.** Confirmei a ausência com grep de `black|scholes|vega|theta|implied|IV` em `src`, `scripts` e `Python`.

## 1. O que existe, por tema

| Tema | Evidência | Para quais telas |
|---|---|---|
| **Séries, strikes e vencimentos** | `src/Contracts/Farol.Protocol/Types/TickerClassifier.cs` (`ParseOption`, `ExtractOptionBase`, `IsBmfTicker`). `src/Services/Farol.Signals.Ordens/Backtest/OptionExpiry.cs` calcula o vencimento pela letra do ticker (3ª sexta) e os pregões restantes com `B3Holidays`. `src/Web/Farol.Portal/Modules/OperacaoOpcaoCalculadora.cs` tem `EhOpcao`. | Mapa de Opções, Max Pain e calculadoras |
| **Cadastro B3 de derivativos** | `Python/b3_scraper_linux.py` baixa de `https://arquivos.b3.com.br/bdi` os arquivos `derivativos_cadastro_instrumentos_*.csv` e `derivativos_negocios_consolidados_*.csv` para `/srv/charlie/finance/scrapper/artifacts/scrapper/B3/Derivativos` (`infra/scrapper/b3-scrapper-paths.env`). `src/Services/Farol.DataHub/Operations/ScrapperCsvDailyUniverseProvider.cs` lê as colunas «Instrumento financeiro», «Ativo», «Data de expiração» e «Tipo de opção». | Base de toda a cadeia de opções |
| **Posições em aberto (open interest)** | O mesmo scraper já baixa `derivativos_posicoes_aberto_YYYYMMDD.csv` (rota `OpenPositionsEquities`). **Nenhum código interpreta esse arquivo.** Ele só aparece como item no `ScrapperCard` (`src/Web/Farol.Portal/Modules/ScrapperEndpoints.cs:146`). | Market Gamma, Jumba Walls, Max Pain, PCR, Market Exposure |
| **Cadeia ao vivo pela DLL** | `Host/Services/OptionChainReader.cs` com `src/Contracts/Farol.Protocol/Types/OptionChainScan.cs`: descobre séries em torno do preço, lê `RequestTickerInfo` (descrição, multiplicador, validade) e bid/ask, e monta trava com crédito e débito. É limitado: comentário «cadeia de PETR4», até 80 candidatos, teto de 100 assinaturas. **Não tem chamador em produção**, só `Host.Tests/Services/OptionChainReaderTests.cs`. | Mapa de Opções em tempo real, Box 3/4 Pontas |
| **Volatilidade** | Só a «Superfície de Volatilidade de Dólar» da B3 (`collect_superficie` em `b3_scraper_linux.py`), que vai para o Google Sheets e não para o DataHub. Atenção: `GetTheoreticalValues` e `OnTheoreticalPrice` (`Host/Core/ProfitDLL.cs:248`, `Host/Services/ProfitService.cs:4209`) dão o **preço teórico de leilão**, não preço de opção (`knowledge/api/functions/market-data.md:152`). | Volatilidade (só DOL) |
| **Futuros IND e DOL** | `TickerClassifier.IsMiniFuture`/`IsFullFuture`. O tape de WINFUT e WDOFUT já é usado pela Leitura (`MacroReadingSources.cs`) e pelo Fluxo. | Jumba Trader IND/DOL |
| **DI e juros** | `HistoryDownloadPolicy.IsJurosTicker` (DI1, DDI, DAP, FRC, OC1, FRP) e a categoria `InterestRateFuture` no universo. `MacroReadingSources.cs` lê DI1F27 e DI1F29 com a nota «convenção não validada». O scraper coleta SELIC, cupom limpo, SOFR e dif. oper. casada (`collect_indicadores`). **Não existe curva montada.** | Curva de Juros, e a taxa r do BSM |
| **Eventos corporativos** | O Host assina `SubscribeAdjustHistory`. `OnAdjustHistoryV2` (`ProfitService.cs:4137`) recebe valor, tipo, observação, data do ajuste, deliberação, pagamento e multiplicador, mas só passa para `DailyAggregator.UpdateAdjustment` e não persiste. *Suposição:* pela assinatura, isso é o histórico de proventos e desdobramentos da DLL. Falta verificar com a DLL real. | Eventos Corporativos, Histórico de Ajustes de Strikes |
| **Book e negócios por corretora** | `farol_datahub.proto`: `TradeRow` traz `buy_agent`, `sell_agent` e `aggressor`. `TradeFlowAgent` traz saldo em 1, 5, 15 e 60 minutos. Há também `TradeFootprintSnapshot` (células por agente e minuto) e `QueryBook` (replay do livro). `Host/Services/AgentService.cs` resolve os nomes e `ClientApp/src/lib/agents.json` tem o mapa. As rotas já existem: `/api/fluxo/vivo/corretoras`, `/api/fluxo/footprint/corretoras`, `/api/fluxo/livro/negocios`. | Shark Map, Shark Positions, Trader Flow |
| **Classificação de corretoras** | `docs/base-de-conhecimento/fluxo-winfut/corretoras-prior.json` separa estrangeira, institucional local e varejo. É usado por `scripts/research/fluxo/players_comp.py`. | Aproxima o «Fluxo de Investimentos». Não é o dado oficial da B3. |
| **Acervo de opções** | Pelo código, o universo diário inclui instrumentos com negócio no dia, opções inclusive. A SPEC-0009 tirou opções sobre futuro e sobre juros (denylist `category:OPCOES-FUTUROS/JUROS`); 881 tickers de opções continuam gravados (`docs/surfaces/data.md:1281`). A Fita viva guarda só 5 pregões (ADR-0039). | Histórico de séries |
| **Pesquisa (`src/Research`)** | QuantLab (backtest de candles, `MetricCalculator`), `Farol.Macro.Medicao`, `MarketStructureEngine` e `MarketVolumeProfileEngine`. **Nenhum indicador de opções.** `OptionSignal.cs` só interpreta sinais de canal do Telegram. | Pouco aproveitável |

**O que falta construir:** cálculo de BSM, IV e gregas; leitura das posições em aberto; curva DI; aluguel BTC (não há nenhuma fonte, só custos de corretagem em `scripts/dev/custos-btg.py`); proventos persistidos; dado oficial de participação de investidores da B3; histórico de IV.

## 2. O Portal (`src/Web/Farol.Portal`)

**Stack** (`ClientApp/package.json`):
- Front: React 19.3, Vite 8.3, TypeScript 7.0, Vitest 5 e Playwright. Tempo real via `@microsoft/signalr` (hub em `src/Web/Farol.Mercado/Hubs/MarketHub.cs`).
- BFF: ASP.NET em .NET 10 com minimal APIs, em `Modules/*Endpoints.cs` e `Farol.Mercado/Modules/*`, ligadas em `PortalComposition.cs` (linhas 268–290) com `RequireAuthorization`. O BFF esconde do navegador os endpoints, os certificados mTLS e a DLL (`Farol.Portal.md`).

**Bibliotecas de gráfico:**
- `lightweight-charts` 5.2.1 e `klinecharts` 10.0.3: gráficos de candle com eixo de tempo.
- `@xyflow/react`: diagramas.
- Canvas próprio, como `modules/fluxo/footprintCanvas.ts`.

Não há biblioteca de gráfico com eixo por strike (GEX por strike, OI, payoff). *Suposição:* isso vai pedir Canvas/SVG próprio ou uma dependência nova.

**Menus:** ficam no array `modules` de `ClientApp/src/App.tsx` (linhas 85–104), cada um com `{id, nav, title, code, tabset?}`. Pela convenção do AGENTS.md, cada grupo de páginas é **um botão no rail**, e as páginas viram **abas numa linha só** no topo. Exemplo: o tabset «Negociação» junta Contas, Posição, Ordem, Sinais, Replicador e Performance. As páginas são `lazy(import(...))` e entram no mapa de renderização perto da linha 371.

**Como adicionar uma página:**
1. Criar `ClientApp/src/modules/<id>/` com `<Id>Page.tsx`. Cada módulo tem um dono por branch.
2. Adicionar a entrada em `modules`, o `lazy` e o render em `App.tsx`.
3. Atualizar a lista de módulos em `ClientApp/AGENTS.md`. A cerca `src/moduleBoundaries.test.ts` barra import entre módulos fora de `ALLOWED_CROSS_MODULE_IMPORTS`.
4. No BFF, criar `XxxEndpoints.Map(app)` e registrar em `PortalComposition.cs`.
5. Passar nos testes do Vitest e nos ratchets de estilo (`styleRatchet.test.ts`) e de tamanho de arquivo (`fileSizeRatchet.test.ts`), e registrar em `docs/surfaces/portal.md`.
6. Publicar com `scripts/dev/farol-deploy submit --module <id>`.

**Sistema de design:** `src/styles/tokens.css` e `src/styles/README.md`, na «Direção B: Painel arejado». Tema escuro grafite, Manrope e IBM Plex Mono, cores semânticas (`--healthy`, `--degraded`, `--error`…) e espaçamento de 4 a 32 px. Os componentes compartilhados estão em `components/PortalComponents.tsx`: `PageHeader`, `MetricCard`, `DataTable`, `StatusPill`, `EmptyState`, `LoadingState`, `ErrorPanel`, `Button`. A CSP bloqueia fontes e CDNs externos (SPEC-0497).

## 3. Área nova no Portal ou app separado?

**Recomendo uma área nova no Portal do Farol.** As regras do AGENTS.md que pesam nisso:

- **«The Portal is the only human UI»** (Architecture) e a **invariante 6**, «Host and Gateway stay headless; UI belongs to the Portal». Um app separado iria contra a política do repositório.
- **Invariante 1:** só o Host carrega a ProfitDLL. Um app separado também teria de consumir dados pelo Gateway e pelo DataHub com mTLS, e acabaria duplicando a autenticação por capability do Tailscale e o BFF que o Portal já tem.
- **O portão de ordens:** `NoOrderCallerTests` e `LiveOrderPathGuardTests`. A réplica tem de ser só leitura, e o «Find Your Trade» deve ser apenas calculadora, sem nenhum caminho até `SendOrderAsync`.
- **O deltax está fora:** «Nunca tocar em `~/Projects/deltax`» (`plans/brief-auditoria-pessoal.md:51`) e «proibido por governança» (SPEC-0480).
- **Posse por módulo** (`docs/knowledge/isolamento-de-trabalho-paralelo.md`): um módulo novo, por exemplo `opcoes`, fica isolado. Mexer em `PortalComponents.tsx`, `tokens.css` ou `mercado/chart/` exige coordenação, porque afeta todos os módulos.

**Um cuidado de layout:** o menu «Jumba Pro» tem 24 páginas. Isso não cabe na regra de abas em uma linha só. *Proposta:* dividir em vários tabsets no rail (por exemplo Opções/Mapa, Gamma e Walls, Volatilidade, Fluxo/Shark, Juros/Eventos, Estruturas) e dar ao módulo um nome próprio, sem a marca do Jumba.

**Onde fica cada parte:**
- Cálculo puro (BSM, gregas, GEX, Max Pain): no padrão de `OperacaoOpcaoCalculadora.cs`, sem I/O e testável.
- Ingestão de posições em aberto, curva DI e BTC: no scraper e no DataHub.
- Rotinas agendadas: no MeusAgentes. O AGENTS.md já delega o backup do Farol a ele, e `catalog/agents/` já tem agentes de frescor de dados.