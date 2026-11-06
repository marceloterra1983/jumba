# 02. Posições em aberto (OI, coberto, travado, descoberto)

Acesso: 2026-11-04. Legenda: **[C]** documento da B3; **[T]** código de terceiros; **[S]** suposição a testar.

## Três arquivos com nomes parecidos

| Nome | O que é | Para opções? |
|---|---|---|
| **DerivativesOpenPosition** (antigo "Posições em Aberto em Derivativos (Listado)") | OI por instrumento listado. Migrou para o BDI como "Posições em aberto" em "Derivativos de bolsa" ([CE 007/2025](https://www.b3.com.br/data/files/28/C7/3A/11/33F7A9105B12E5A9AC094EA8/CE%20007-2025-VTEC%20MELHORIAS%20NO%20ACESSO%20AOS%20DADOS%20NO%20SITE%20B3_PT.pdf)) [C] | **Sim** |
| BDI, rota **`OpenPositionsEquities`** | A rota que o Farol baixa (`b3_scraper_linux.py:80,84`) | Provável: é a tabela do BDI para ações e opções de ações [S] |
| "Glossário _ Posição_Em_Aberto" | **Aluguel de ações (BTB)**, não opções [C] | Não |

## DerivativesOpenPosition (glossário)

- Fonte: [DerivativesOpenPositionFile 2023.pdf](https://b3.com.br/data/files/1E/D1/BA/58/C841B810E9C1AAA8AC094EA8/DerivativesOpenPositionFile%202023.pdf), de 05/10/2023 (v1.1) [C]. Há uma versão em inglês: [DerivativesOpenPositionFile EN.pdf](https://b3.com.br/data/files/1B/03/10/13/E40B4810A58E3348AC094EA8/DerivativesOpenPositionFile%20EN.pdf).
- Formato: CSV [C]. Na antiga API, a primeira linha era `Status do Arquivo: …`, com separador `;` e decimal `,` [T: `raw/b3-open-data-1.0.4/scrapper.py`].
- Publicação: diária, **depois do pregão**, sem hora no glossário [C]. Em 04/11, o Farol recebeu um arquivo de cerca de 400 B (só cabeçalho), possivelmente por ter pedido antes da publicação. A hipótese de publicação por volta das 21h **não está confirmada** [S].
- Histórico: no BDI, cerca de **21 pregões** [T: rb3 NEWS]. A antiga API Dados Públicos saiu do ar em 31/03/2026.

| # | Tag | Tipo [T] | Significado [C] |
|---|---|---|---|
| 1 | RptDt | data | Data de referência |
| 2 | **TckrSymb** | texto | Código de negociação (**chave**) |
| 3 | ISIN | texto | ISIN |
| 4 | Asst | texto | Ativo/mercadoria |
| 5 | XprtnCd | texto | Código de vencimento (MYY ou MYOA) |
| 6 | SgmtNm | texto | Segmento |
| 7 | **OpnIntrst** | número | **Contratos em aberto** |
| 8 | **VartnOpnIntrst** | número | **Variação do OI contra D-1** |
| 9 | DstrbtnId | número | Distribuição (não se aplica a derivativos) |
| 10 | **CvrdQty** | número | **Quantidade coberta** |
| 11 | **TtlBlckdPos** | número | **Total de posições bloqueadas (travadas)** |
| 12 | **UcvrdQty** | número | **Quantidade descoberta** |
| 13 | TtlPos | número | Total de posições |
| 14 | **BrrwrQty** | número | "Quantidade de tomadores": nº de **clientes** tomadores |
| 15 | **LndrQty** | número | "Quantidade de doadores": nº de **clientes** doadores |
| 16 | CurQty | número | Ações vinculadas aos contratos em aberto (termo) |
| 17 | FwdPric | número | Preço médio das posições (termo) |

### Titulares e lançadores

O glossário **não usa** as palavras "titulares" e "lançadores" [C]. Os únicos campos com **contagem de clientes** são `BrrwrQty` e `LndrQty`.

**Hipótese [S]:** nas linhas de opções, `BrrwrQty` seria o nº de **titulares** e `LndrQty` o nº de **lançadores**, que é o insumo do IQ. Para confirmar, numa linha de opção de PETR4:
- se os dois vêm preenchidos, e
- se `BrrwrQty` e `LndrQty` são bem menores que `OpnIntrst`,

então são contagens de pessoas. Se vierem vazios, as contagens não estão nesse arquivo.

### Coberto, travado e descoberto

Para opções de ações [C], há três quantidades: `CvrdQty`, `TtlBlckdPos` e `UcvrdQty`. Uma conferência a fazer [S] é se `CvrdQty + TtlBlckdPos + UcvrdQty = TtlPos`.

Em **opções sobre futuro**, a quebra costuma vir vazia (nula), segundo a [brapi](https://brapi.dev/blog/api-open-interest-opcoes-b3-posicoes-em-aberto) [terceiro].

## BDI `OpenPositionsEquities`

- Chamada: `POST https://arquivos.b3.com.br/bdi/table/OpenPositionsEquities/{AAAA-MM-DD}/{AAAA-MM-DD}/{pág}/{tam}`, com corpo `{}` (nota 07). No seletor da página BDI, o valor é `OpenPositionsEquities@false`.
- Colunas: vêm em `table.columns[].name` (tag em inglês) e em `friendlyNamePt`. **Não confirmadas** nesta sessão, porque o proxy bloqueou o host. Espera-se o mesmo conjunto do DerivativesOpenPosition [S].
- Sem strike, sem tipo e sem vencimento por data: só `XprtnCd`. Isso vem do cadastro.
- O limiar do Farol é `MIN_CSV_SIZE_POSICOES_ABERTO = 500_000` bytes. Um arquivo menor é rejeitado.

## Como ligar ao cadastro

`TckrSymb` + `RptDt` → `InstrumentsConsolidated.TckrSymb` (ou `OptnOnEqtsInf/TckrSymb` no BVBG.028). Use o cadastro **do mesmo pregão**: o OI de D foi publicado na noite de D.

Esse é o mesmo join do projeto [flowtradelab/flow PR #4](https://github.com/flowtradelab/flow/pull/4): DerivativesOpenPosition × InstrumentsConsolidated, por `TckrSymb`, para "strike, vencimento, tipo, estilo e ativo objeto" [T].

## Traz?

| Strike | Vencimento | Tipo | Estilo | Coberto/travado/descoberto | Titulares/lançadores |
|---|---|---|---|---|---|
| não | só o código (XprtnCd) | não | não | **sim** | **talvez** (BrrwrQty/LndrQty) [S] |

## Alternativa para histórico longo de OI (sem quebra)

O BVBG.086 (PR{aammdd}.zip) tem `OpnIntrst` por instrumento (nota 03), mas sem coberto/travado/descoberto. Se a Pesquisa por pregão guardar mais pregões que o BDI, ele dá **OI total histórico**. Isso não está confirmado [S].

## Aluguel (BTB), para não confundir

- Glossário: [Glossario _ Posicao_Em_Aberto.pdf](https://b3.com.br/data/files/BF/F1/58/15/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Posicao_Em_Aberto.pdf), v1 de 05/09/2023 [C].
- Arquivo: "Empréstimos de Ativos – Posição em Aberto-DD-MM-AAAA", CSV, publicado **na abertura com D-1**.
- Campos: Data, Ticker, ISIN, Empresa ou Fundo, Tipo, Mercado, Saldo em quantidade do ativo, Preço Médio e Saldo em R$.
- No BDI, a rota é `BTBLendingOpenPosition` [T: filings-b3].

**Achado extra para "Mercados de Aluguel":** a antiga tabela `LoanBalance` tinha `DnrMinRate`, `DnrAvrgRate`, `DnrMaxRate`, `TakrMinRate`, `TakrAvrgRate` e `TakrMaxRate`, ou seja, as **taxas doadora e tomadora** [T: `raw/b3-open-data-1.0.4/meta.py`]. Falta procurar a tabela equivalente no BDI. Isso responde a uma lacuna apontada no `critic.md`.
