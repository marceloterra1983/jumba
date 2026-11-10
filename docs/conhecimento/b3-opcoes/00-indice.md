# Arquivos públicos da B3 para opções: índice

Acesso: 2026-11-04. Pasta: `docs/conhecimento/b3-opcoes/`. Base anterior: `../../pesquisa/fontes-dados.md` e `critic.md`.

Legenda: **[C]** confirmado em documento da B3; **[T]** confirmado em código de terceiros ou do Farol; **[S]** suposição a testar.

## Situação desta coleta

- **O proxy desta sessão na nuvem bloqueia** os hosts `b3.com.br`, `www.b3.com.br`, `arquivos.b3.com.br` e `bvmf.bmfbovespa.com.br` (`CONNECT 403`).
- Os glossários e layouts foram **lidos pelo WebFetch**, que devolve só um texto processado. **Nenhum PDF ficou salvo como binário** e **nenhum pregão de amostra foi baixado**. O esquema real ainda não foi conferido.
- Para baixar os PDFs e um pregão numa máquina com acesso: `scripts/baixar-amostras.sh` (não foi executado).
- Em `raw/` estão o `MANIFESTO.md` e o código de terceiros baixado de hosts liberados: rb3, filings-b3 e b3-open-data.
- **Termos da B3:** o Hub de Dados Públicos veda coleta automatizada, inclusive por IA ([hub](https://www.b3.com.br/pt_br/dados/hub-de-dados-publicos/)). A decisão continua com o Marcelo; aqui só se leu documentação.

## Notas

| Nota | Assunto |
|---|---|
| [01-cadastro-instrumentos.md](01-cadastro-instrumentos.md) | InstrumentsConsolidated (52 colunas), BDI `InstrumentsDerivatives`, **BVBG.028 / IN{aammdd}.zip** |
| [02-posicoes-em-aberto.md](02-posicoes-em-aberto.md) | DerivativesOpenPosition (17 colunas), BDI `OpenPositionsEquities`, BTB |
| [03-negocios-consolidados.md](03-negocios-consolidados.md) | TradeInformationConsolidated V3, BDI `ConsolidatedTradesDerivatives`, **BVBG.086 / PR{aammdd}.zip** |
| [04-cotahist.md](04-cotahist.md) | COTAHIST: layout de 245 bytes, URLs anual e diária |
| [05-premio-referencia.md](05-premio-referencia.md) | Prêmio de Referência (`Premio`): layout BM&F, método B3 |
| [06-series-autorizadas.md](06-series-autorizadas.md) | Séries autorizadas: página não lida; o BVBG.028 a substitui |
| [07-api-bdi.md](07-api-bdi.md) | API `arquivos.b3.com.br/bdi`: rotas, POST, paginação, eco, exportação CSV, PDFs |
| [08-pesquisa-por-pregao.md](08-pesquisa-por-pregao.md) | `pesquisapregao/download?filelist=`: códigos IN, PR, TS, Premio… |
| [raw/MANIFESTO.md](raw/MANIFESTO.md) | Cada URL lida ou baixada, com o resultado |
| [scripts/baixar-amostras.sh](scripts/baixar-amostras.sh) | Glossários e 1 pregão (BDI, IN, PR, COTAHIST) |

## Dado → melhor arquivo B3

| Dado | 1º arquivo B3 | Reserva B3 | Chave | Histórico |
|---|---|---|---|---|
| Strike | **BVBG.028** (`IN`), `OptnOnEqtsInf/ExrcPric` | InstrumentsConsolidated `ExrcPric`; COTAHIST `PREEXE` (só séries negociadas) | TckrSymb (+XprtnDt) | IN: retenção por confirmar; COTAHIST: anos |
| Vencimento | BVBG.028 `XprtnDt` | InstrumentsConsolidated `XprtnDt` + `WrkgDays`; COTAHIST `DATVEN` | TckrSymb | idem |
| Tipo (call/put) | BVBG.028 `OptnTp` | InstrumentsConsolidated `OptnTp`; COTAHIST TPMERC 070/080 | TckrSymb | idem |
| Estilo (americana/europeia) | BVBG.028 `OptnStyle` (ações) ou `ExrcStyle` (sobre futuro) | InstrumentsConsolidated `OptnStyle`; Premio `tipo_exercicio` | TckrSymb | **COTAHIST não tem** |
| Ativo-objeto | BVBG.028 `UndrlygInstrmId` (é SecurityID: juntar ao `FinInstrmId` do objeto) | InstrumentsConsolidated `Asst` / `UndrlygTckrSymb1` [S] | SecurityID | — |
| Ajuste de strike | Comparar `ExrcPric` do BVBG.028 entre D-1 e D, por série; `PrtcnFlg`/`SrsTp` | — | TckrSymb + XprtnDt | Só a partir das fotos diárias |
| OI por série | **BDI `OpenPositionsEquities`** (= DerivativesOpenPosition) `OpnIntrst`, `VartnOpnIntrst` | BVBG.086 `OpnIntrst` (total, sem quebra) | TckrSymb + RptDt | BDI cerca de 21 pregões; PR por confirmar |
| Coberto / travado / descoberto | BDI `OpenPositionsEquities`: `CvrdQty` / `TtlBlckdPos` / `UcvrdQty` | — (em opção sobre futuro tende a vir vazio) | TckrSymb | cerca de 21 pregões; **gravar todo dia** |
| Titulares / lançadores (IQ) | **Candidatos:** `BrrwrQty` / `LndrQty` do mesmo arquivo [S] | Nenhum confirmado | TckrSymb | cerca de 21 pregões |
| Prêmio de fechamento, OHLC, volume, nº de negócios | **BVBG.086** (`PR`): FrstPric…LastPric, BestBid/Ask, RglrTxsQty, NtlFinVol | TradeInformationConsolidated (sem abertura); COTAHIST (anos) | TckrSymb | PR por confirmar; COTAHIST desde 1986 |
| Prêmio teórico e vol implícita de **todas** as séries | **Prêmio de Referência** (`Premio`, Pesquisa por pregão) | Calcular sobre o BVBG.086 | ticker ou mercadoria+série [S] | por confirmar |
| Curva DI para BSM | **TS{aammdd}.ex_** (TaxaSwap, curva PRE) | BVBG.086 `AdjstdQt` do DI1 | — | por confirmar |
| Lista de séries autorizadas | BVBG.028 bloco `OptnOnEqtsInf` | Página "séries autorizadas" (não lida) | TckrSymb | — |
| Aluguel: saldo | BDI `BTBLendingOpenPosition` | — | Ticker | D-1, na abertura |
| Aluguel: taxas doadora e tomadora | Antiga `LoanBalance` (DnrAvrgRate, TakrAvrgRate…); **procurar a rota do BDI** [S] | NEGOCIOSBTB (taxa por negócio) | Ticker | — |

**A ProfitDLL só entra** em preço ao vivo, book, negócios intradiários com corretora e ajuste de proventos estruturado, que nenhum arquivo B3 acima cobre.

## O que muda em relação à pesquisa anterior

1. O "Glossário _ Posição_Em_Aberto" é de **aluguel (BTB)**, não de opções [C].
2. O DerivativesOpenPosition tem **`BrrwrQty`/`LndrQty`**, contagens de **clientes**. São a melhor aposta para titulares e lançadores [S]. O teste está abaixo.
3. O **BVBG.086 tem `OpnIntrst`**. Se a Pesquisa por pregão guardar mais que 21 pregões, há **OI total histórico** sem pagar UP2DATA [S].
4. No BVBG.028, o objeto vem como **SecurityID**, não como ticker. Nas opções sobre futuro, o estilo vem em **`ExrcStyle`** [T].
5. O IN é **ZIP dentro de ZIP com várias fotos**: é preciso usar a de maior `CreDtAndTm` [T].
6. A API do BDI exige **POST** (GET devolve 405), aceita até 1.000 linhas por página, e **3 tabelas ecoam as mesmas linhas** em qualquer página [T]. O Farol pagina sem checar eco.
7. Há uma **exportação CSV do BDI** sem paginação: `POST /bdi/table/export/csv` com `{"Name","Date","FinalDate"}` [T].
8. A antiga `LoanBalance` trazia taxas doadora e tomadora (lacuna do critic.md) [T].
9. A B3 publica o Prêmio de Referência com **vol implícita** para ações, ETFs e índice desde 14/12/2016 [C].

## Testes a fazer (máquina com acesso, 1 pregão, ritmo de 2 s)

1. Rodar `scripts/baixar-amostras.sh <raw/> AAAA-MM-DD` com um pregão já publicado.
2. **OpenPositionsEquities, página 1:**
   - listar `columns[].name` e `friendlyNamePt`;
   - numa linha de opção de PETR4, ver se `BrrwrQty`/`LndrQty` vêm preenchidos e se são menores que `OpnIntrst` (então são titulares e lançadores);
   - conferir se `CvrdQty + TtlBlckdPos + UcvrdQty = TtlPos`;
   - comparar o `pageCount` com o tamanho do arquivo do Farol (cerca de 400 B).
3. **InstrumentsDerivatives:**
   - ver se tem `ExrcPric`/`OptnStyle` e linhas de opções de ações;
   - se não tiver, achar a rota de ações em `#selectTabelas`.
4. **IN{aammdd}.zip:**
   - contar os `OptnOnEqtsInf` de PETR4;
   - pegar a foto de maior `CreDtAndTm`;
   - comparar com a página de séries autorizadas.
5. **PR{aammdd}.zip:** ver se `OpnIntrst` vem em opções de ações; pedir um pregão de 60, 250 e 1.000 dias atrás para medir a retenção.
6. **Prêmio de Referência:** achar o código do filelist (ações e derivativos), abrir como ZIP e documentar as colunas.
7. **Paginação:** para cada rota usada, comparar o hash da página 2 com o da página 1 (eco).
