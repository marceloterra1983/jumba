# 07. API do Boletim Diário do Mercado: `arquivos.b3.com.br/bdi`

Acesso: 2026-11-04. Legenda: **[C]** documento da B3; **[T]** código de terceiros ou do Farol; **[S]** suposição a testar.

**Nada aqui foi chamado ao vivo.** O proxy desta sessão bloqueia `arquivos.b3.com.br`. O conteúdo vem do código do Farol (`/home/claude/Farol/Python/b3_scraper_linux.py:73-86, 1543-1626`), do filings-b3 0.3.5 e do rb3 (pasta `raw/`).

## Contexto

- A página "Dados Públicos" e a API antiga (`arquivos.b3.com.br/api/download/requestname`) foram desativadas ([CE 007/2025](https://www.b3.com.br/data/files/28/C7/3A/11/33F7A9105B12E5A9AC094EA8/CE%20007-2025-VTEC%20MELHORIAS%20NO%20ACESSO%20AOS%20DADOS%20NO%20SITE%20B3_PT.pdf): unificação em 15/12/2025; data final adiada para 31/03/2026 pelo CE 001/2026, segundo `pesquisa/fontes-dados.md`) [C].
- Os derivativos já estavam só no BDI desde 29/03/2024 ([EC 001/2024](https://www.b3.com.br/data/files/74/C7/CA/6D/C926E810D34843E8AC094EA8/EC%20001-2024-VTI_ing_dados%20de%20derivativos_2.pdf)) [C].
- **Histórico: cerca de 21 pregões** [T: rb3 NEWS].
- **Termos:** o [Hub de Dados Públicos](https://www.b3.com.br/pt_br/dados/hub-de-dados-publicos/) veda "coleta automatizada, inclusive por meio de ferramentas de inteligência artificial". Isso já foi registrado em `pesquisa/fontes-dados.md` e está pendente de decisão do Marcelo [C].

## Endpoints

| Uso | Método e URL | Corpo | Resposta |
|---|---|---|---|
| Página (SPA) | GET `https://arquivos.b3.com.br/bdi/tabelas?lang=pt-BR` | — | HTML. Seletor `#selectTabelas` com valores `Rota@bool`, botão `button[title='Exportar CSV']` [T: Farol] |
| Último pregão | GET `https://arquivos.b3.com.br/bdi/table/workday?date=AAAA-MM-DD` | — | String `"AAAA-MM-DDT00:00:00"` [T: Farol] |
| **Tabela paginada** | **POST** `https://arquivos.b3.com.br/bdi/table/{Rota}/{dataIni}/{dataFim}/{pagina}/{tamanho}` | `{}` com `Content-Type: application/json` | JSON (abaixo). **GET devolve 405**. Não exige cookie nem user-agent de navegador [T: filings-b3] |
| **Exportação CSV** | **POST** `https://arquivos.b3.com.br/bdi/table/export/csv?lang=en-us` (para português, provavelmente `lang=pt-br` [S]) | `{"Name":"{Rota}","Date":"AAAA-MM-DD","FinalDate":"AAAA-MM-DD"}` | CSV com preâmbulo, separador `;` e `-` como vazio. O cabeçalho em inglês começa em `Ticker symbol` [T: rb3] |
| PDFs do boletim | GET `https://arquivos.b3.com.br/bdi/download/bdi/{AAAA-MM-DD}/BDI_{NN}_{AAAAMMDD}[_en-Us].pdf` | — | PDF por capítulo. Ex.: BDI_02 traz a participação dos investidores; BDI_05 traz o OI agregado por mercado e as opções flexíveis [C, lido por WebFetch] |

### Parâmetros da tabela paginada

- `{Rota}`: nome interno da tabela (lista abaixo).
- `{dataIni}/{dataFim}`: datas ISO, ambas inclusive. Para um pregão, repita a data. Use o `workday` para saber qual é o último pregão.
- `{pagina}`: começa em 1.
- `{tamanho}`: o Farol usa 100; **o teto da B3 é 1.000** [T: filings-b3].

### Formato da resposta

```json
{"table": {
  "columns": [{"name": "TckrSymb", "friendlyName": "...", "friendlyNamePt": "...",
               "order": 1, "isVisible": true, "hideColumn": false}],
  "values":  [["PETRK300", "..."], ["..."]],
  "pageCount": 37
}}
```

- As linhas são **posicionais**: o valor *i* corresponde a `columns[i]`.
- O Farol ordena as colunas por `order` e filtra as invisíveis (`b3_scraper_linux.py:1607-1609`).
- Algumas tabelas mandam linhas **mais largas que o cabeçalho**, com a última posição sempre `null` (ex.: `DailyAverageStocks`) [T].
- Os números devem ser lidos como Decimal, não float [T].

### Paginação: armadilhas [T: filings-b3]

- De 38 tabelas do BDI, **32 têm uma página só**, **5 são paginadas de verdade** e **3 devolvem as mesmas linhas em qualquer página** (eco).
- Regra segura:
  1. leia `pageCount` na página 1;
  2. pare na primeira página vazia, **ou** na primeira com o mesmo hash da anterior, **ou** em `pageCount`;
  3. use um teto fixo de páginas (o filings-b3 usa 500).
- O Farol pagina até `pageCount` **sem** a checagem de eco. Se alguma das três rotas dele ecoar, as linhas saem duplicadas [S, a conferir].

## Rotas conhecidas

| Rota | Conteúdo | Fonte |
|---|---|---|
| `InstrumentsDerivatives` (`@true`) | Cadastro de instrumentos, derivativos (nota 01) | Farol |
| `ConsolidatedTradesDerivatives` (`@true`) | Negócios consolidados, derivativos (nota 03). Usada também na exportação CSV do rb3 | Farol, rb3 |
| `OpenPositionsEquities` (`@false`) | Posições em aberto, ações (nota 02) | Farol |
| `BTBLendingOpenPosition` | Posição em aberto de aluguel | filings-b3 |
| `DailyAverageStocks` | Resumo do mercado à vista | filings-b3 |
| `HistoricalExchange` | Câmbio oficial do BCB (cerca de 5 anos) | filings-b3 |
| `EconomicIndicators` | Indicadores econômicos | filings-b3 |

O significado do sufixo `@true`/`@false` do seletor é **desconhecido** [S]. Pode indicar se a tabela aceita intervalo de datas, ou se tem paginação.

**Rotas prováveis, não confirmadas [S]:** `InstrumentsEquities`, `ConsolidatedTradesEquities` e `OpenPositionsDerivatives`. Para obter a lista completa (39 tabelas, segundo o filings-b3), abra `bdi/tabelas` e leia as `<option>` de `#selectTabelas` (comando na nota 00).

## API antiga (desativada, só para referência) [T: `raw/b3-open-data-1.0.4/`]

- Pedido: GET `https://arquivos.b3.com.br/api/download/requestname?fileName={Tabela}&date=AAAA-MM-DD&recaptchaToken=` → JSON com `redirectUrl` (`~/...`) → GET do CSV.
- O CSV vinha com a primeira linha `Status do Arquivo: …`, separador `;` e decimal `,`.
- Tabelas: `TradeInformationConsolidated`, `TradeInformationConsolidatedAfterHours`, `OTCTradeInformationConsolidated`, **`DerivativesOpenPosition`**, **`InstrumentsConsolidated`**, `OTCInstrumentsConsolidated`, `EconomicIndicatorPrice`, `MarginScenarioLiquidAssets`, `LendingOpenPosition` e `LoanBalance`.
- Limites de posição (ainda no ar?): GET `https://bvmf.bmfbovespa.com.br/LimitesPosicoes/Posicoes/DownloadArquivoDiretorio?data=AAAA-MM-DD` devolve um CSV em base64 [T] [S: não conferido em 2026].
