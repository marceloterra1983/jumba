# 01. Cadastro de instrumentos (strike, vencimento, tipo, estilo)

Acesso: 2026-11-04. Legenda: **[C]** confirmado em documento da B3; **[T]** confirmado em código de terceiros; **[S]** suposição a testar.

Há **três formas** do mesmo cadastro. Para opções, a melhor é o **BVBG.028 (IN)**. A tabela do BDI serve de atalho, se trouxer o strike.

| Forma | Onde | Formato | Histórico |
|---|---|---|---|
| A. InstrumentsConsolidated (CSV, 52 colunas) | Antiga página "Dados Públicos", hoje BDI "Cadastro de instrumentos" | CSV `;` | BDI: cerca de 21 pregões [T: rb3 NEWS] |
| B. BDI, rota `InstrumentsDerivatives` (e possivelmente outra rota para o segmento de ações [S]) | `POST https://arquivos.b3.com.br/bdi/table/InstrumentsDerivatives/{AAAA-MM-DD}/{AAAA-MM-DD}/{pág}/{tam}` (nota 07) | JSON (`columns` + `values`) | cerca de 21 pregões |
| C. **BVBG.028.02 InstrumentReport** | `https://www.b3.com.br/pesquisapregao/download?filelist=IN{aammdd}.zip` [T: filings-b3] | ZIP dentro de ZIP, com um XML ISO 20022 por foto intradiária | Pesquisa por pregão (quantidade de pregões não confirmada) |

## A. InstrumentsConsolidatedFile (glossário v5)

- Fonte: [Glossario InstrumentsConsolidatedFile 2024.pdf](https://b3.com.br/data/files/52/74/1E/14/4BA6D8103152D4C8AC094EA8/Glossario%20InstrumentsConsolidatedFile%202024.pdf), v5 de 02/02/2024 [C].
- Publicação: **de manhã, antes da abertura, e à noite, depois do encerramento** [C].
- Os nomes das colunas batem com os do pacote b3-open-data (`raw/b3-open-data-1.0.4/meta.py`) [T]. A ordem é a do arquivo.

| # | Tag | Tipo [T] | Significado |
|---|---|---|---|
| 1 | RptDt | data | Data de referência |
| 2 | **TckrSymb** | texto | Código de negociação (**chave**) |
| 3 | Asst | texto | Mercadoria/ativo (ex.: PETR, DOL) |
| 4 | AsstDesc | texto | Descrição do ativo |
| 5 | SgmtNm | texto | Segmento (Ações – Vista, Ações – Derivativos, Financeiro…) |
| 6 | MktNm | texto | Mercado (OPC, OPV, OPCOES SOBRE DISPONIVEL, OPCOES SOBRE FUTURO…) |
| 7 | SctyCtgyNm | texto | Categoria (3º nível) |
| 8 | **XprtnDt** | data | **Vencimento** |
| 9 | XprtnCd | texto | Código de vencimento (MYY ou MYOA) |
| 10 | TradgStartDt | data | Início da negociação |
| 11 | TradgEndDt | data | Fim da negociação |
| 12 | BaseCd | número | Base de dias (252/360/365) para contratos em taxa |
| 13 | ConvsCritNm | texto | Critério de conversão |
| 14 | MtrtyDtTrgtPt | número | Pontos no vencimento |
| 15 | ReqrdConvsInd | texto | Precisa converter taxa em preço |
| 16 | ISIN | texto | ISIN |
| 17 | CFICd | texto | Código CFI |
| 18 | DlvryNtceStartDt | data | Início do aviso de entrega |
| 19 | DlvryNtceEndDt | data | Fim do aviso de entrega |
| 20 | **OptnTp** | texto | **Tipo**: Compra / Venda |
| 21 | CtrctMltplr | número | Multiplicador do contrato |
| 22 | AsstQtnQty | número | Quantidade do ativo por cotação |
| 23 | AllcnRndLot | número | Lote de alocação |
| 24 | TradgCcy | texto | Moeda |
| 25 | DlvryTpNm | texto | Entrega física ou financeira |
| 26 | WdrwlDays | número | Dias de saque até o vencimento |
| 27 | WrkgDays | número | **Dias úteis até o vencimento (inclusive)** |
| 28 | ClnrDays | número | Dias corridos até o vencimento |
| 29 | RlvrBasePricNm | texto | Preço-base da estratégia |
| 30 | OpngFutrPosDay | número | Dias para abrir a posição futura |
| 31 | SdTpCd1 | texto | Perna 1: BUYI/SELL |
| 32 | UndrlygTckrSymb1 | texto | Ativo-objeto da perna 1 |
| 33 | SdTpCd2 | texto | Perna 2: BUYI/SELL |
| 34 | UndrlygTckrSymb2 | texto | Ativo-objeto da perna 2 |
| 35 | PureGoldWght | número | Peso de ouro puro |
| 36 | **ExrcPric** | número | **Strike** |
| 37 | **OptnStyle** | texto | **Estilo**: Americano / Europeu |
| 38 | ValTpNm | texto | Tipo de valor do indicador |
| 39 | PrmUpfrntInd | texto | Prêmio pago à vista |
| 40 | OpngPosLmtDt | data | Data-limite para posição em aberto |
| 41 | DstrbtnId | número | Distribuição (ações e ouro) |
| 42 | PricFctr | número | Fator de preço (ex.: 1000) |
| 43 | DaysToSttlm | número | Dias para liquidação |
| 44 | SrsTpNm | texto | Tipo de série (correção do strike) |
| 45 | PrtcnFlg | texto | Opção protegida contra eventos |
| 46 | AutomtcExrcInd | texto | Exercício automático |
| 47 | SpcfctnCd | texto | Especificação (ON, PN…) |
| 48 | CrpnNm | texto | Nome da empresa |
| 49 | CorpActnStartDt | data | Início do evento corporativo |
| 50 | CtdyTrtmntTpNm | texto | Tratamento de custódia |
| 51 | MktCptlstn | número | Capital social |
| 52 | CorpGovnLvlNm | texto | Nível de governança |

O campo nº 53 foi removido na v3 (set/2023) [C].

## B. BDI, rota `InstrumentsDerivatives` (a que o Farol baixa)

- O código está em `/home/claude/Farol/Python/b3_scraper_linux.py:82,86` e em `:1565-1593`. Gera cerca de 2,2 MB e cerca de 9.300 instrumentos (`docs/operations/scrapper-derivativos-only.md`).
- O CSV gravado pelo Farol usa os nomes amigáveis em português (`friendlyNamePt`). Exemplo de cabeçalho em `tests/Services/Farol.DataHub.Tests/ScrapperCsvDailyUniverseProviderTests.cs:486`: `Data de referência;Instrumento financeiro;Ativo;Descrição do ativo;Segmento;Mercado;Categoria;Data de expiração;Código de expiração;…;Tipo de opção`. É a mesma ordem das colunas 1 a 20 de A.
- **Em aberto [S]:** o fixture para em "Tipo de opção" (coluna 20). Não se sabe se a rota real traz as colunas 21 a 52 (com **ExrcPric** e **OptnStyle**) nem se cobre **opções de ações** (segmento "Ações – Derivativos") ou só BM&F. Com cerca de 9.300 linhas, é provável que não cubra todas as séries de ações. O teste está na nota 00.

## C. BVBG.028.02 (InstrumentReport) — o melhor para opções

- Layout: [Catálogo de Mensagens – Cadastro de Instrumento](https://b3.com.br/data/files/D4/52/03/F5/A86B0A105BF9020AAC094EA8/Catalogo-de-Mensagens-Cadastro-de-Instrumento.pdf), v2.9 de 13/03/2026, XSD 2.8 [C].
- URL: `https://www.b3.com.br/pesquisapregao/download?filelist=IN{aammdd}.zip` (ex.: `IN261104.zip`) [T: `raw/filings-b3-0.3.5/_base_instruments_file_reader.py:249`].
- Formato: ZIP com outro ZIP dentro e **um XML por foto intradiária**. As fotos são cumulativas: **use a de maior `<CreDtAndTm>`**; qualquer outra perde os cadastros feitos ao longo do dia [T].
- Publicação: enviado **na abertura do dia**. Complementos saem durante o dia pela mensagem `bvmf.100.02` [C]. Horário exato não informado.
- Estrutura: `RptParams` → `FinInstrmId` → `FinInstrmAttrCmon` → `InstrmInf` (um único sub-bloco por instrumento, entre 20 tipos) [C][T].

### Campos comuns (todo registro)

| Caminho | Significado |
|---|---|
| RptParams/RptDtAndTm/Dt | Data de referência |
| FinInstrmId/OthrId/Id | **SecurityID** numérico do instrumento (Trade Structure) |
| FinInstrmId/OthrId/Tp/Prtry | Sempre 8 |
| FinInstrmId/PlcOfListg/MktIdrCd | MIC (BVMF) |
| FinInstrmAttrCmon/Asst, AsstDesc | Ativo e descrição |
| FinInstrmAttrCmon/Mkt | Mercado: 70 = OPC, 80 = OPV, 10 = Vista… |
| FinInstrmAttrCmon/Sgmt | Segmento: 1 = Ações-Vista, 2 = Ações-Derivativos… |
| FinInstrmAttrCmon/Desc | Descrição |

### `OptnOnEqtsInf` (opções sobre ações, ETFs e índice) [C][T]

| Tag | Tipo | Significado |
|---|---|---|
| **TckrSymb** | texto | Código de negociação |
| ISIN | 12 caracteres | ISIN |
| DstrbtnId | int | Distribuição |
| CFICd | texto | CFI |
| **ExrcPric** (atributo `@Ccy`) | decimal, até 10 casas | **Strike** |
| **OptnStyle** | código | **Estilo** americano/europeu |
| **XprtnDt** | data | **Vencimento** |
| **OptnTp** | código | **Call/Put** |
| SrsTp | código | Correção do strike: 0 sem correção, 1 dólar, 2 TJLP, 3 TR, 4 IPCR, 5 SWOPTIONS, 6 pontos de índice, 7 dólar protegida, 8 IGP-M, 9 URV, 234 DI |
| **UndrlygInstrmId/OthrId/Id** | id | **Ativo-objeto, como SecurityID (não é ticker)** |
| TrgtInstrmId/OthrId/Id | id | Novo instrumento após fusão ou cisão |
| PrtcnFlg | sim/não | Protegida contra eventos (strike ajustável) |
| PrmUpfrntInd | sim/não | Prêmio pago à vista |
| TradgStartDt, TradgEndDt | data | Início e fim da negociação |
| PmtTp | código | 0 netting, 1 bruta… |
| AllcnRndLot | int | Lote |
| PricFctr | int | Fator de preço |
| TradgCcy | moeda | Moeda |
| DaysToSttlm | texto | Dias para liquidação |
| DlvryTp | código | 0 física, 1 financeira |
| AutomtcExrcInd | sim/não | Exercício automático |

### `OptnOnSpotAndFutrsInf` (opções sobre disponível e futuro: IND, DOL, DI1…) [T]

As tags são TckrSymb, ISIN, **ExrcPric**, **ExrcStyle** (aqui o nome muda: não é `OptnStyle`), **OptnTp**, **XprtnDt**, XprtnCd, **CtrctMltplr**, AsstQtnQty, AllcnRndLot, UndrlygInstrmId/OthrId/Id, AsstSttlmInd/OthrId/Id, WdrwlDays, **WrkgDays**, ClnrDays, OpngPosLmtDt, PmtTp, PrmUpfrntInd, TradgCcy, TradgStartDt, TradgEndDt e PureGoldWght. Fonte: `raw/filings-b3-0.3.5/instruments_file_optn_on_spot_and_futures.py`.

### Novidades de 2026

O [CE 035/2026](https://www.b3.com.br/data/files/D5/02/29/32/B35FE910ADC36BE9AC094EA8/CE%20035-2026-VNC%20INCLUSAO%20DE%20NOVOS%20CAMPOS%20OPCIONAIS%20NO%20ARQUIVO%20BVBG028%20CADASTRO%20DE%20INSTRUMENTOS_PT.pdf) (23/06/2026) e o [CE 052/2026](https://www.b3.com.br/data/files/E1/93/18/98/A76A0A105BF9020AAC094EA8/CE%20052-2026-VNC%20INCLUSAO%20DE%20NOVOS%20CAMPOS%20OPCIONAIS%20NO%20ARQUIVO%20BVBG028_PT.pdf) (15/09/2026) incluem campos opcionais [C]:

- `CtdyStartDt` e `CtdyEndDt` (custódia);
- `StdLotQty` (lote padrão; substituiu `NegtnLot`);
- **`SctyCtgy` em opções sobre disponível e futuro**;
- `DaysToRed` (ETF; substituiu `RedemptionDaysToSttlm`);
- `Artl3Ind`.

O parser deve **tolerar tags desconhecidas**.

## Como ligar

- **CSV (A e B):** `TckrSymb` + `RptDt`. Como reserva, `ISIN`.
- **BVBG.028:** a chave interna é o `FinInstrmId/OthrId/Id`. Para obter o **ticker do ativo-objeto**, junte `UndrlygInstrmId/OthrId/Id` ao `FinInstrmId/OthrId/Id` do registro do objeto no **mesmo arquivo**, que fica no bloco `EqtyInf` ou `FutrCtrctsInf`.
- **Cuidado [S, prática conhecida]:** os tickers de opções de ações são **reaproveitados** em outros anos. No histórico, use `(TckrSymb, XprtnDt)` ou o ISIN como chave, nunca só o ticker.

## Traz?

| Strike | Vencimento | Tipo | Estilo | Coberto/travado/descoberto | Titulares/lançadores |
|---|---|---|---|---|---|
| sim (ExrcPric) | sim (XprtnDt; e WrkgDays no CSV) | sim (OptnTp) | sim (OptnStyle / ExrcStyle) | não | não |

O **ajuste de strike** por provento aparece como mudança de `ExrcPric` entre D-1 e D na mesma série (`PrtcnFlg`/`SrsTp` dizem se ela é ajustável) [S].
