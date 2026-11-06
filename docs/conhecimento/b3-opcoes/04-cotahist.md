# 04. COTAHIST (Cotações Históricas, layout HistoricalQuotations)

Acesso: 2026-11-04. Legenda: **[C]** documento da B3; **[T]** código de terceiros; **[S]** suposição.

- Layout: [HistoricalQuotations_B3.pdf](https://www.b3.com.br/data/files/65/50/AD/26/29C8B51095EE46B5790D8AA8/HistoricalQuotations_B3.pdf) [C]. Há outra versão, não lida: [SeriesHistoricas_Layout.pdf](https://www.b3.com.br:443/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf).
- URLs [T: `raw/rb3-github/b3-cotahist-*.yaml`]:
  - anual: `https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{AAAA}.ZIP` (o rb3 usa `verifyssl: false` nesse host);
  - diário: `https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D{DDMMAAAA}.ZIP` (ex.: `COTAHIST_D04112026.ZIP`);
  - mensal: `COTAHIST_M{MMAAAA}.ZIP` [S, citado no manual do rb3, URL não conferida].
- Formato: ZIP com TXT posicional de **245 bytes** por linha, codificação latin1. Registro 00 é o header (`COTAHIST.AAAA`, `BOVESPA`, data de geração); 01 são as cotações; 99 é o trailer (total de registros) [C].
- Histórico: anual **desde 1986**; o rb3 recomenda não usar dados anteriores a 1995 [T]. Horário de publicação do diário não informado.
- Preços **sem ajuste** por proventos [T].

## Registro 01

| Campo | Pos. | Tipo | Significado |
|---|---|---|---|
| TIPREG | 1–2 | N(2) | "01" |
| DATA | 3–10 | N(8) AAAAMMDD | Data do pregão |
| CODBDI | 11–12 | X(2) | Classificação. **78 = opção de compra, 82 = opção de venda, 74/75 = opção de compra/venda sobre índice**, 38/42 = exercício de opção de compra/venda, 32/33 = exercício sobre índice, 02 = lote padrão |
| **CODNEG** | 13–24 | X(12) | **Ticker** (chave) |
| **TPMERC** | 25–27 | N(3) | Mercado. **070 = opção de compra, 080 = opção de venda**, 010 = vista, 012/013 = exercício de compra/venda, 020 = fracionário, 030 = termo |
| NOMRES | 28–39 | X(12) | Emissor |
| ESPECI | 40–49 | X(10) | Especificação (ON, PN, UNT…) |
| PRAZOT | 50–52 | X(3) | Prazo do termo |
| MODREF | 53–56 | X(4) | Moeda |
| PREABE | 57–69 | (11)V99 | Abertura |
| PREMAX | 70–82 | (11)V99 | Máximo |
| PREMIN | 83–95 | (11)V99 | Mínimo |
| PREMED | 96–108 | (11)V99 | Médio |
| PREULT | 109–121 | (11)V99 | Último |
| PREOFC | 122–134 | (11)V99 | Melhor oferta de compra |
| PREOFV | 135–147 | (11)V99 | Melhor oferta de venda |
| TOTNEG | 148–152 | N(5) | Nº de negócios |
| QUATOT | 153–170 | N(18) | Quantidade negociada |
| VOLTOT | 171–188 | (16)V99 | Volume |
| **PREEXE** | 189–201 | (11)V99 | **Strike** (opções) |
| INDOPC | 202 | N(1) | Correção do strike: 1 = US$, 2 = TJLP, 8 = IGP-M, 9 = URV |
| **DATVEN** | 203–210 | N(8) | **Vencimento** |
| FATCOT | 211–217 | N(7) | Fator de cotação: 1 ou 1000 |
| PTOEXE | 218–230 | (7)V06 | Strike em pontos (opções em dólar) |
| CODISI | 231–242 | X(12) | ISIN |
| DISMES | 243–245 | 9(3) | Distribuição |

`V99` indica duas casas decimais implícitas: divida por 100. Para o preço por ação, divida também por FATCOT.

## Como ligar

Use `CODNEG` + `DATA`. Para histórico entre anos, use `CODNEG` + `DATVEN`, ou `CODISI`.

## Traz?

| Strike | Vencimento | Tipo | Estilo | Coberto/travado/descoberto | Titulares/lançadores |
|---|---|---|---|---|---|
| sim (PREEXE) | sim (DATVEN) | sim (TPMERC 070/080) | **não** | não | não |

**Não tem OI.** Serve para o histórico longo de prêmios (fechamento, sem casamento de horário com o objeto) e de volume, e como **cadastro histórico** de séries que negociaram. Séries sem negócio não aparecem [S].
