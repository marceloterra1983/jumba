# 01. Curva de juros: Taxas Referenciais, arquivo TS, BVBG.086, ajustes do DI1, convenção 252 e PU

Acesso: 2026-11-04. Legenda: **[C]** documento da B3 lido nesta coleta; **[T]** código de terceiros (rb3, em `../b3-opcoes/raw/rb3-github/`); **[S]** suposição a testar. Os textos lidos estão em `raw/webfetch/`.

## Fontes, em ordem de preferência

| # | Fonte | URL | Formato | Horário | Histórico | Situação |
|---|---|---|---|---|---|---|
| 1 | **Arquivo TS, "Taxas de Mercado para Swaps"** (`TaxaSwap.txt`) | `https://www.b3.com.br/pesquisapregao/download?filelist=TS{aammdd}.ex_` [T: rb3 `b3-reference-rates.yaml`] | `.ex_` autoextraível com ZIP dentro. **Abrir como ZIP, nunca executar.** TXT posicional, latin1 | Diário, depois do fechamento [S: hora não confirmada] | Pesquisa por pregão; retenção não confirmada [S] | Substitui a página Taxas Referenciais [T: rb3 NEWS #125] |
| 2 | **BVBG.086 (Pricing Report)**, ajuste do DI1 | `https://www.b3.com.br/pesquisapregao/download?filelist=PR{aammdd}.zip` [T] | ZIP com XML. Campos `AdjstdQt`, `AdjstdQtTax` (ajuste em taxa), `PrvsAdjstdQt`, `PrvsAdjstdQtTax`, `AdjstdValCtrct` (ver `../b3-opcoes/03-negocios-consolidados.md`) | Depois do pregão [S]. Na Quarta-feira de Cinzas o horário de publicação não muda [C OC 054/2025] | Por confirmar | Monta a curva PRE pelo método da B3 (ver abaixo) |
| 3 | **BDI, negócios consolidados de derivativos** (ajuste do dia) | POST `https://arquivos.b3.com.br/bdi/table/export/csv?lang=en-us` com `{"Name":"ConsolidatedTradesDerivatives","Date":"AAAA-MM-DD","FinalDate":"AAAA-MM-DD"}` [T: rb3 `b3-futures-settlement-prices.yaml`] | CSV `;`. Colunas `Ticker symbol`, `Adjusted quote`, `Previous adjusted quote tax` (rótulo errado: é o ajuste anterior), `Variation`, `Settlement value per contract (R$)` | Diário | **Cerca de 21 pregões** [T] | A página "Ajustes do pregão" foi descontinuada em dez/2025 [T: rb3 NEWS] |
| 4 | Página **Taxas Referenciais BM&FBOVESPA** | `www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-taxas-referenciais-bmf-ptBR.asp` redireciona (302) para `https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-de-derivativos/precos-referenciais/taxas-referenciais-bm-fbovespa/` [C: redirect lido] | Tela | — | — | O destino deu erro de cliente no WebFetch. O Hub de Dados Públicos ainda lista o item, mas o rb3 diz que ele foi descontinuado. **Não usar** |
| 5 | **ANBIMA ETTJ** (só para conferência) | https://www.anbima.com.br/informacoes/est-termo/CZ.asp [C] | XLS, CSV, TXT, XML. ETTJ PRE, ETTJ IPCA, inflação implícita, % a.a./252, vértices de 252 a 8.316 DU; parâmetros Svensson (β1–β4, λ1, λ2); taxas da Circular 3.361; erro por título (LTN, NTN-F, NTN-B) | Diário. Na leitura, a data exibida era 03/11/2026 | Não informado | Modelo paramétrico sobre títulos públicos, não sobre o DI1. Nenhum aviso de termos de uso apareceu no texto lido |
| 6 | Tesouro Transparente (taxas do Tesouro Direto) | ver `../../pesquisa/fontes-dados.md` | CSV (CKAN) | Diário | Anos | Só como reserva. Curva de títulos, não de DI |

## Layout do TS (TaxaSwap.txt) [T: rb3 `readers.R`, `curve_read`]

Largura fixa: 6, 3, 2, 8, 2, 5, 15, 5, 5, 1, 14, 1, 5.

| Campo | Largura | Significado |
|---|---|---|
| seq | 6 | Sequencial |
| seq_compl | 3 | Complemento |
| regtype | 2 | Tipo de registro |
| refdate | 8 | Data de referência, `AAAAMMDD` |
| curve_type | 2 | Tipo de curva |
| curve_name | 5 | Código da curva (PRE, DIC, DOC, DOL…; cerca de 120 curvas no arquivo) |
| description | 15 | Descrição |
| cur_days | 5 | Dias corridos |
| biz_days | 5 | Dias úteis (saques) |
| sign | 1 | Sinal |
| rate | 14 | Taxa com 7 decimais implícitos, em % (rb3: `rate = sinal·valor/1e7`) |
| vertex_type | 1 | Tipo de vértice |
| vertex_code | 5 | Código do vértice |

A taxa vem na base da curva: 252 para PRE e DIC, 360 para DOC [T]. **Os nomes dos campos são do rb3, não da B3.** O layout oficial não foi encontrado. Conferir num arquivo real.

## Como a B3 monta a curva PRE ([Manual de Curvas, 12/12/2025](https://www.b3.com.br/data/files/F3/42/AE/8C/1942B9105B12E5A9AC094EA8/Manual%20de%20Curvas_V21.pdf)) [C]

- **Insumos:** a taxa CDI referencial do dia (`TxJuros`) e a taxa de ajuste de cada vencimento do DI1 (`TxDI1`).
- **Vértice de 1 dia útil:** a taxa CDI do dia.
- **Vértices nos vencimentos do DI1:** a taxa de ajuste do vencimento.
- **Demais vértices:** **flat forward 252** (item 1.4.2). Depois do último vencimento, extrapola-se com flat forward usando o penúltimo e o último vencimentos.
- **Precisão:** % a.a. com 3 casas.
- **Dias úteis:** pelo calendário de feriados da **ANBIMA**. Nele, 24/12 e 31/12 contam como dias úteis, embora não haja pregão (ver `feriados-b3-2026-2028.json`).

**Fórmula do flat forward**, reconstruída do texto, que veio parcialmente ilegível (conferir no PDF):

```
f(DU) = (1+i_a)^(DU_a/252) · [ (1+i_p)^(DU_p/252) / (1+i_a)^(DU_a/252) ]^((DU−DU_a)/(DU_p−DU_a))
taxa(DU) = ( f(DU)^(252/DU) − 1 ) · 100
```

`i_a`/`DU_a` = vértice anterior; `i_p`/`DU_p` = vértice posterior; as taxas em fração.

Códigos de curva do manual: PRE, SLP, TJP, TFP, TP, TR, TIE, SFR, EST, ZMX, ZUS, ZEU, DIC, DPL, DIM, PTX, EUR, JPY, DOL, DOC, DCL, EUC, YCL, SDE, SGP, SMX, SYD, BRP, INP, SML, CYI, MBR, CYM, VIX, CYX.

## Contrato DI1: PU, 252 e ajuste ([OC 055/2024-PRE, Anexo I](https://www.b3.com.br/data/files/FF/C5/51/86/158EE810C54843E8DC0D8AA8/OC%20055-2024%20PRE%20Contratos%20FE%20-%20Juros%20(PT).pdf); [página do produto](https://b3.com.br/pt_br/produtos-e-servicos/negociacao/juros/futuro-de-taxa-media-de-depositos-interfinanceiros-de-um-dia.htm)) [C]

- **Cotação:** taxa efetiva anual, base 252, com 3 casas.
- **Valor:** 100.000 pontos no vencimento, R$ 1 por ponto.
- **Variação mínima:** 0,001 até 3 meses; 0,005 acima.
- **PU:** `PO = 100.000 / (1 + i/100)^(n/252)`, em que `n` = dias úteis da data da operação (inclusive) até o vencimento (exclusive).
- **Ajuste diário:**
  - operação do dia: `AD = (PA_t − PO) · M · N`;
  - posição anterior: `AD = [PA_t − PA_{t−1} · FC_t] · M · N`;
  - `FC_t = Π (1 + DI_{t−j}/100)^(1/252)`, com a Taxa DI em até 6 casas.
- **Vencimento:** 1ª sessão de negociação do mês, quando PA = 100.000. O último dia de negociação é a sessão anterior.
- **Preço de ajuste:** VWAP de 10 minutos, das 16h10 às 16h20 (página do produto) [C]. A nota `../b3-opcoes/05-premio-referencia.md` cita "ajustes às 17h". **Divergência a conferir.**
- **Taxa do ajuste:** `i = ((100.000/PA)^(252/n) − 1)·100` (inversa do PU) [S: álgebra].

## Para o motor (BSM e Black-76)

1. **Fechamento oficial:** curva PRE do TS. Na falta dele, monte a curva com o ajuste do DI1 (BVBG.086 ou BDI) e o CDI do dia (nota 02), por flat forward 252, como a B3.
2. **Taxa contínua para BSM:** `r = ln(1 + taxa/100)`, em base 252 com `T = DU/252` [S: convenção do motor; a B3 não define].
3. **Durante o pregão:** DI1 em tempo real só pela ProfitDLL, porque a B3 não publica ajuste intradiário gratuito.

## Limitações

- O proxy desta sessão bloqueia `b3.com.br` e `arquivos.b3.com.br`. **Nenhum TS, PR ou CSV real foi baixado.** Layouts vêm do rb3 [T] e do WebFetch [C].
- A retenção do TS e do PR na Pesquisa por pregão não foi medida (teste em `scripts/baixar-documentos.sh`).
- Termos da B3: o Hub de Dados Públicos veda coleta automatizada, inclusive por IA. O Marcelo decidiu seguir com o scraper (decisão da Etapa 2).
