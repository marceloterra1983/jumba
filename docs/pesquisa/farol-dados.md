## Farol: como os dados de mercado entram e onde ficam guardados

Li só o repositório `/home/claude/Farol` e não alterei nada. O que está marcado **[suposição]** não foi confirmado no código.

### 1. Arquitetura dos componentes de dados

**Host (ProfitDLL)**
- É o processo .NET `net10.0-windows` em `Host/`. Roda **sob Wine no servidor Linux**, num prefixo dourado em `/opt/pdll-test/golden`, supervisionado pelo systemd através de `pdll-runtime.service`. Não há Windows nativo: o PC Windows foi desativado em 2026-09-24. Fontes: `README.md`, `Host/README.md`, `docs/adr/0027-host-under-wine-on-linux.md` e `docs/HOST-POLICY.md`.
- Só `Host/Core/ProfitDLL.cs` carrega a DLL (P/Invoke). As funções e callbacks usados para dados são:
  - **Negócios em tempo real:** `SetTradeCallbackV2` mais `SubscribeTicker`.
  - **Histórico de negócios:** `GetHistoryTrades` com `SetHistoryTradeCallbackV2` e `SetSerieProgressCallback`.
  - **Livro:** `SubscribePriceDepth`, `SetPriceDepthCallback`, `SubscribeOfferBook`, `SetOfferBookCallbackV2` e `SubscribePriceBook`.
  - **Diário:** `SetDailyCallback` e `GetLastDailyClose`.
  - **Ajustes de proventos:** `SubscribeAdjustHistory` com `SetAdjustHistoryCallbackV2`, que alimenta o `DailyAggregator` (`Host/Services/ProfitService.cs:4137`).
  - **Ficha do ativo:** `RequestTickerInfo` com `SetAssetListInfoCallbackV2`. Traz tipo, subtipo, validade (`validityDate`), multiplicador, ISIN e descrição.
  - **Preço teórico de leilão:** `SetTheoreticalPriceCallback`.
- `GetTheoreticalValues` e `SetAssetListCallback` estão declaradas mas não são usadas.
- Limites da DLL (`knowledge/api/functions/market-data.md:200`):
  - histórico tick a tick só dos **últimos 30 dias**;
  - para WIN*/WDO*, um pedido de 10 dias ou mais é recusado;
  - séries de opções já vencidas não são servidas (`docs/specs/0078-sinais-forward/SPEC.md`).
- Orçamento de conexão: **3 tentativas nativas a cada 15 minutos**. Nunca se abre um segundo dono da DLL.

**IPC e Gateway**
- O Host serve o Named Pipe `ProfitBridge.MarketData` em MessagePack (`src/Contracts/Farol.Protocol/Contracts/IpcMessages.cs`). O caminho é: relay Wine→Linux (`scripts/wine-gate/relay`, porta 127.0.0.1:8765 dentro do prefixo) e depois **RemoteGateway** nativo, gRPC com mTLS na porta `127.0.0.1:7443`.
- Por uid, só a conta `farol-gateway` alcança o socket do Host. Portal e DataHub ficam bloqueados (`scripts/wine-gate/README.md:296`).
- O contrato está em `src/Contracts/Farol.Remote.Contracts/Protos/farol_remote.proto`, com estes serviços:
  - `MarketData.Subscribe`: stream nos dois sentidos com `include_trades`, `include_book` e `include_daily`;
  - `GetSnapshot` e `GetCandles`;
  - `History.DownloadTrades`;
  - `MarketReference.GetTickers`: devolve só símbolo, bolsa e categoria;
  - `Time.GetTradingCalendar`.

**DataHub** (`src/Services/Farol.DataHub`, unidade systemd `farol-datahub`)
- É o único escritor da **História**: um catálogo DuckDB (`/var/lib/profitbridge/catalog/batch_catalog.duckdb`) mais Parquet em hive.
- **Fita:** `trades/v1/category=…/ticker=…/year=…/month=…/part-<guid>.parquet` (`Storage/ParquetTradeStore.cs:106`). Colunas: `session_date`, `event_timestamp_utc`, `trade_number`, `price`, `quantity`, `volume`, `buy_agent`, `sell_agent`, `aggressor`, `is_edit`.
  - Entrada ao vivo: `OnTradeV2` no Host, depois pipe, Gateway e `LiveIngestService` (caminho congelado pelo ADR-0040, ver `Operations/INGEST.md`).
  - O Catch-up recupera buracos de até 15 minutos.
  - A conferência de coleta corre às 18h45.
  - O backfill entra pelo `BatchCoordinator` e pelo `GatewayBatchExecutor`.
- **Livro:** `book/v1/.../day=DD/` (`Storage/BookStore.cs:133`), gravado pelo `BookRecorderService` com 10 níveis. A consulta aceita só WINFUT e INDFUT (`ParquetBookQuery.cs:86`).
- **Candles:**
  - `bars/v1/.../tf=…` é uma projeção da Fita feita às 19h (`Data.Core/Bars/BarSchemaV1.cs`);
  - `external-candles/v1` guarda candles de outra fonte, usados só onde a Fita não tem negócio;
  - o vivo sai por `WatchLiveCandles`.
- **Cadastro de coleta** (TICKADM): `ticker-modes.json` sob o `CanonicalRoot`, com os modos `live` e `end-of-day`. Só muda pelo gRPC `TickerAdminOperations`, que só a identidade do Portal pode usar. Há ainda uma lista de bloqueio do Batch, a denylist em `/etc/farol/batch-ticker-denylist.txt` (SPEC-0009).
- **Discos:** zona Vivo em `/srv/data2/farol` (no código o padrão ainda é `/srv/data2/profitbridge`), Réplica em `/srv/data1/...` e Arquivo em `/srv/farol/arquivo`. O backup externo usa restic/rclone.
- **Concessão:** `Concession.Acquire(ticker, from, to, duração ≤ 86.400 s)` devolve uma lista de Parquets imutáveis, com caminho relativo, sha256, contagem de linhas, geração e commit (`farol_datahub.proto:53`). O consumidor **lê os ficheiros diretamente do disco** e confere o hash. O arrendamento impede o GC de apagar esses ficheiros. O leitor de referência é `Storage/CanonicalConcessionReader.cs`.

### 2. Classes de ativo e símbolos coletados

- **Taxonomia** (`Data.Core/Trades/AssetCategoryClassifier.cs`): IBOV, ACOES, FII, ETF, INDICES, FUTUROS (WINFUT, WDOFUT, DOLFUT e INDFUT contínuos, mais raízes como DI1, DOL, IND…), OPCOES, OPCOES-ETF, OPCOES-FUTUROS e OPCOES-JUROS.
- **Coleta viva:** cerca de 91 a 96 tickers no Cadastro (`docs/runbooks/SINGLE-ASSET-HISTORY-DOWNLOAD.md:156,214`), principalmente IBOV, ETFs e os futuros contínuos. As âncoras do Portal são BOVA11, DOLFUT, INDFUT, PETR4, WDOFUT e WINFUT.
- **Opções estão fora do universo de propósito:**
  - `category:OPCOES-FUTUROS` (880 tickers) e `OPCOES-JUROS` estão na denylist desde 2026-09-28. O dono disse que vai "desenvolver outra forma" (`docs/specs/0009-universo-sem-opcoes/SPEC.md`).
  - OPCOES-ETF tem dados só até 14/07/2026.
  - As opções de ações do IBOV antigas ficaram fora da migração (`infra/README.md`).
  - A única exceção: a Rotina `sinais-forward` enfileira por fora (offline) as opções dos Sinais vivos (SPEC-0078).
- **Cadeia de séries:**
  - Existe `Host/Services/OptionChainReader.cs`. Ele tenta adivinhar os tickers de PETR4 por strike e mês, até 80 candidatos e 100 assinaturas, e lê o strike da descrição (`Protocol/Types/OptionChainScan.cs`).
  - Não está ligado a nenhum IPC nem gRPC: só aparece em testes.
  - A tabela `tickers` do Host tem `validity_date`, `exercise_price` e `parent_ticker` (`Host/Data/TickerDatabase.cs:297`), mas **nada grava `exercise_price`**.
  - Não há gregas, volatilidade implícita nem posições em aberto.

### 3. `Python/b3_scraper_linux.py` e `data/`

- Raspa três coisas:
  - **Indicadores** (SELIC, DIF Oper Casada, Cupom Limpo, SOFR), via Playwright em `sistemaswebb3-derivativos.b3.com.br`;
  - **Superfície de volatilidade USD** (primeira linha da tabela);
  - **Derivativos** pela API `arquivos.b3.com.br/bdi/table/<rota>/…`, nas rotas `InstrumentsDerivatives`, `ConsolidatedTradesDerivatives` e `OpenPositionsEquities`. Saem como CSVs `derivativos_*_AAAAMMDD.csv`.
- Indicadores e superfície iam para uma planilha Google.
- **Em produção só corre o job `derivativos`.** O drop-in `infra/scrapper/farol-b3-scraper-linux.service.d/10-derivativos-only.conf` força isso porque o servidor não tem os binários do Playwright nem a conta Google (`docs/operations/scrapper-derivativos-only.md`).
  - Saída em `/srv/charlie/finance/scrapper/artifacts/scrapper/B3/Derivativos`.
  - Tamanhos: cadastro com cerca de 9.300 instrumentos, negócios consolidados com cerca de 780 KB, e posições em aberto com cerca de 400 B, ou seja, quase vazio.
- **Frequência:** daemon em dias úteis. Os padrões do código são `DERIVATIVOS_TIMES=18:30,19:00,19:30` e `INDICADORES_TIMES=07:30,12:00` (BRT), com nova tentativa a cada 30 minutos. **[suposição]** O `.env` instalado pode mudar esses horários. Atenção: `docs/integrations/scrapper.spec.md` (07h30, "retirado") está desatualizado.
- **Uso:** o `ScrapperCsvDailyUniverseProvider` lê o cadastro e os negócios para montar o universo diário do `CentralBatchScheduler`. Esse agendador estava em `BatchSchedulerEnabled=false` em 2026-09-21. **[suposição]** Ainda pode estar desligado.
- `data/`: só `.gitkeep`. Não há dados versionados (`data/README.md`).

### 4. Como um consumidor novo obtém dados

**(a) Histórico**
- Pelo gRPC do DataHub com mTLS: `TradeQueries.Query`, `QueryPage`, `QueryCandles`, `QueryBook`, `Coverage` e `ExportCsv`, ou pela `Concession.Acquire` para ler o Parquet direto.
- Precisa da capability `data.query` (`Security/DataHubCapabilityInterceptor.cs`). O certificado tem de constar em `AllowedClientSubjects`, `IdentityCapabilities` e nos pinos, que é configuração protegida do servidor.
- Para trazer um histórico novo da DLL:
  - `BatchOperations.Start` exige `batch.command`, que só vale com `MutationEnabled` e o agendador ligados (`DataHubIdentityCapabilities.cs`);
  - a alternativa é o `enqueue-history` offline, com o DataHub parado (runbook acima).

**(b) Tempo real**
- Pelo gRPC do Gateway, `MarketData.Subscribe`, com as capabilities `market.subscribe.v1` e `market.read.v1`. O limite é de 256 assinaturas por identidade (`GatewayOptions.cs:50`).
- Ou pelo DataHub, `WatchLiveCandles`.
- O browser usa o Portal: SignalR em `/hubs/market` e as rotas `/api/fluxo/vivo/*`.
- Nunca diretamente pelo pipe ou pela DLL.
- Incluir um símbolo na coleta exige o TICKADM pelo Portal (`POST /api/datahub/tickers`).

### 5. Onde roda e restrições operacionais

- **Servidor Linux "vps1":** Host sob Wine, relay, Gateway, DataHub, Portal e scraper, além de timers como `farol-hive-backup`, `farol-tape-gc`, `farol-archive-*` e `farol-resumo-pregao` (`infra/systemd/`). A "vps2" roda o monitor MT5/Performance. Os docs antigos dizem "server": **[suposição]** é a mesma máquina que a vps1.
- **Ordens:** o caminho de ordens é real, mas só os pares do dono o alcançam (`IpcOrderPort` e `IlfIpcOrderPort`). Os testes `NoOrderCallerTests` e `LiveOrderPathGuardTests` o guardam (`AGENTS.md`). Um consumidor de análise **não pode** chamar nada que envie Ordem. Os protos recusam símbolos com "order".
- **Regras de trabalho:**
  - um escritor por DuckDB;
  - ADR-0040: não mexer no caminho de ingestão da Fita;
  - nada em `src/` carrega a ProfitDLL;
  - trabalhar em worktree e integrar com `scripts/dev/integrar.sh`, sem PR;
  - publicar é permitido mesmo durante o Pregão (ADR-0050).

### O que falta no Farol para as telas do Jumba

- Cadastro de séries de opções com strike, vencimento e objeto. Pode vir do `InstrumentsDerivatives` da B3, que hoje traz só derivativos; as opções de ações exigiriam a tabela equivalente de renda variável **[suposição]**.
- Posições em aberto por strike, que hoje não vêm.
- Fita de opções de ações, hoje fora do universo.
- Volatilidade implícita e gregas, a calcular.
- Curva de juros: não há coleta própria. Os futuros de juros (DI1 etc.) estão na taxonomia, mas nenhum documento diz que entram na coleta viva.
- O limite de 30 dias da DLL obriga a gravar enquanto a série está viva.