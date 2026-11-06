# 05. Eventos corporativos e proventos com data-com

Acesso: 2026-11-04. Legenda: [C] B3 lido; [T] terceiros; [S] suposição.

## A. B3: "Dividendos e outros eventos corporativos" (fonte principal)

| Item | Valor |
|---|---|
| Página | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/acoes/consultas/dividendos-e-outros-eventos-corporativos/ [C] |
| Sistema | Aponta para `https://sistemaswebb3-listados.b3.com.br/dividensOtherCorpActPage?language=pt-br` [C]. A tela é montada em JavaScript; o WebFetch não capturou o corpo |
| API usada pela tela | GETs em `sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/{Metodo}/{base64(JSON)}` [S: caminho exato não confirmado]. O rb3 monta assim: os parâmetros em JSON, codificados em base64 e anexados ao caminho (`url_encode` em `../b3-opcoes/raw/rb3-github/downloaders.R`) [T] |
| Métodos [T: rb3 `scraper-company.R`] | `GetListedSupplementCompany` (parâmetro: código da empresa), `GetListedCashDividends` (parâmetro: nome de pregão), `GetDetailsCompany` (código CVM) |
| Formato | JSON |
| Horário | Por evento, quando a empresa comunica e a B3 cadastra [S] |
| Histórico | Vários anos por empresa [S] |

**Campos [T: rb3]:**

- `GetListedSupplementCompany`:
  - `Info`: `code`, `tradingName`, `codeCVM`, `stockCapital`, `totalNumberShares`, `numberCommonShares`, `numberPreferredShares`, `roundLot`, `segment`.
  - `CashDividends` (proventos em dinheiro): `isinCode`, `approvedOn`, **`lastDatePrior` (último dia "com")**, `label` (DIVIDENDO, JRS CAP PROPRIO, RENDIMENTO…), `rate` (valor por ação).
  - `StockDividends` (bonificação, desdobramento, grupamento): os mesmos campos mais `factor`.
  - `Subscriptions`: os mesmos campos mais `percentage`, `tradingPeriod`, `priceUnit`, `subscriptionDate`.
- `GetListedCashDividends`: `typeStock`, `dateApproval`, **`lastDatePriorEx`**, `corporateAction`, `valueCash`.

**Data-com e data-ex:** `lastDatePrior` é o último pregão "com". A data-ex é a sessão seguinte, pelo calendário em `feriados-b3-2026-2028.json` [S: confirmar com 1 evento conhecido, por exemplo Petrobras de 21/08/2023 ("com") e 22/08/2023 ("ex"), como no OC 141/2023].

**Limitações:**

- A página traz o aviso de que os dados são "de propriedade exclusiva da B3" e de que é "expressamente vedada a coleta automatizada, inclusive por meio de ferramentas de inteligência artificial" [C].
- O proxy bloqueia `sistemaswebb3-listados.b3.com.br` nesta sessão. Nenhuma resposta real foi vista.
- A B3 só cadastra o evento depois do aviso da empresa. **Não há calendário de proventos "esperados".**

## B. B3: "Ajuste de proventos" (opções)

- O Hub de Dados Públicos lista, em "Mercado à vista (opções)", uma consulta **"ajuste de proventos"**, ao lado de "posições em aberto" e "séries autorizadas" [C: nome lido no [Hub](https://www.b3.com.br/pt_br/dados/hub-de-dados-publicos/)].
- A URL provável é `.../market-data/consultas/mercado-a-vista/opcoes/ajuste-de-proventos/`, mas deu erro de cliente [S].
- **É a fonte direta para "Histórico de Ajustes de Strikes".** Pendência: abrir numa máquina com acesso e documentar.

## C. Cadastro diário (BVBG.028), por comparação

Comparar `ExrcPric` série a série entre D-1 e D dá o strike ajustado (ver `../b3-opcoes/01-cadastro-instrumentos.md`).

## D. ProfitDLL (só se a B3 falhar)

`SubscribeAdjustHistory` + `TAdjustHistoryCallbackV2` (manual v4.0.0.42, p. 73), com os campos:

| Campo | Conteúdo |
|---|---|
| `dValue` | Valor |
| `strAdjustType` | Tipo |
| `strObserv` | Observação |
| `dtAjuste` | Data do ajuste |
| `dtDeliber` | Data da deliberação |
| `dtPagamento` | Data do pagamento |
| `nFlags` | bit 0 = afeta o preço; bit 1 = ajuste de soma |
| `dMult` | Multiplicador; −9999 = inválido |

Regra do manual:
- com `dMult` válido, preço × `dMult`;
- com o bit de soma ligado, preço − `dValue`;
- nos demais casos, preço ÷ `dValue`.

Traz histórico, não o calendário futuro.

## E. CVM (só como conferência)

CVM Dados Abertos, IPE ([dataset](https://dados.cvm.gov.br/dataset/cia_aberta-doc-ipe)): índice de Avisos aos Acionistas e Fatos Relevantes, desde 2003, ZIP anual, licença ODbL. Os documentos não são estruturados (ver `../../pesquisa/fontes-dados.md`). O proxy desta sessão bloqueia `dados.cvm.gov.br`.
