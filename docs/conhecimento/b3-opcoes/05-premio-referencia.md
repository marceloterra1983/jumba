# 05. Prêmio de Referência para Opções

Acesso: 2026-11-04. Legenda: **[C]** documento da B3; **[T]** código de terceiros; **[S]** suposição a testar.

## O que é [C]

- **Prêmio teórico de todas as opções autorizadas**, conforme a [descrição dos arquivos](https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/descricao-dos-arquivos/), item "Mercado de Derivativos - Prêmio de Referência para Opções", código **`Premio`**. Inclui **séries sem negócio**: é o que permite calcular a vol implícita de toda a grade.
- Para opções de **ações, ETFs e índice**, a publicação começou em **14/12/2016**, sincronizada com o encerramento. As **volatilidades implícitas** também são publicadas. Na Pesquisa por pregão, o item é "Mercado de Ações - Prêmio de Referência para Opções sobre Ações" ([workshop de 14/12/2016](https://www.b3.com.br/data/files/10/42/D4/6B/F8EF851052122C85790D8AA8/20161214-Premio%20de%20Referencia%20para%20Opcoes%20de%20Acoes%20-%20Evento.pdf)).
- Método ([Manual de Apreçamento – Opções, 20/12/2023](https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf)):
  - Black-Scholes **sem dividendos e sem exercício antecipado**;
  - juros da curva DI1 (ajustes às 17h);
  - objeto pelo fechamento (18h a 18h20);
  - superfície de volatilidade às 18h, por SVI com Corrado & Su ou SABR, e GARCH para ativos ilíquidos.
- Um ativo é "líquido" quando tem pelo menos 7 séries líquidas. Uma série é líquida quando teve negócio ou oferta nos 10 minutos finais em 100% dos pregões do mês anterior.

## URL

- Base: `https://www.b3.com.br/pesquisapregao/download?filelist={CÓDIGO}{aammdd}.ex_` (padrão comum da Pesquisa por pregão, nota 08).
- **O código exato não foi confirmado** [S]. A descrição dos arquivos dá o identificador `Premio` (derivativos); o arquivo de ações tem item próprio. Confira no seletor da Pesquisa por pregão, na máquina com acesso.
- Os `.ex_` da B3 são autoextraíveis com ZIP dentro. O rb3 os abre "detectando o zip pelo conteúdo" [T]. **Não execute o `.ex_`**: abra como ZIP.

## Layout conhecido: `Premio.txt` (opções sobre derivativos BM&F) [T]

Fonte: [rbmfbovespa `tpl-premio.R`](https://rdrr.io/github/wilsonfreitas/rbmfbovespa/src/legacy/tpl-premio.R). Arquivo de largura fixa.

| Campo | Largura | Significado |
|---|---|---|
| id_transacao | 6 | Identificação da transação |
| compl_transacao | 3 | Complemento |
| tipo_registro | 2 | Tipo de registro |
| data_geracao_arquivo | 8 (AAAAMMDD) | Data de geração |
| **cod_mercadoria** | 3 | Mercadoria (ex.: DOL, IND, DI1) |
| tipo_mercado | 1 | 1 disponível, 2 futuro, **3 opção sobre disponível, 4 opção sobre futuro**, 5 termo |
| **serie** | 4 | Série (código BM&F) |
| **tipo_opcao** | 1 | **C = compra, V = venda** |
| **tipo_exercicio** | 1 | **A = americana, E = europeia** |
| **data_vencimento** | 8 (AAAAMMDD) | **Vencimento** |
| **preco_exercicio** | 15 | **Strike**, com `num_casas_decimais` casas implícitas |
| **premio_referencia** | 15 | **Prêmio**, com as mesmas casas |
| num_casas_decimais | 1 | Nº de casas decimais |

O arquivo de **opções de ações** segue "o formato usado para os instrumentos da Fase 1" [C]. Não se sabe se a chave é o ticker ou mercadoria + série, nem se traz a vol implícita numa coluna [S]. Isso só se resolve abrindo um arquivo real.

## Como ligar

- **BM&F:** `cod_mercadoria` + `tipo_mercado` + `serie` (+ vencimento) → cadastro por `Asst` + `XprtnCd` + `OptnTp` + `ExrcPric` [S]. Não há ticker.
- **Ações:** provavelmente pelo ticker ou ISIN [S].

## Traz?

| Strike | Vencimento | Tipo | Estilo | Coberto/travado/descoberto | Titulares/lançadores |
|---|---|---|---|---|---|
| sim | sim | sim | sim (BM&F) | não | não |

Mais **prêmio teórico**, e para ações também a **vol implícita B3** [C].

**Uso no sistema:** conferência da vol implícita calculada por nós, e a vol diária de séries sem negócio. Não é dado intradiário.
