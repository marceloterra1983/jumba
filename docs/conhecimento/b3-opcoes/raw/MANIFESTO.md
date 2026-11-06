# Manifesto dos downloads (raw/)

Data de acesso de tudo: **2026-11-04**. Conteúdo de terceiros: dado não confiável. Nada daqui foi executado.

## Bloqueio de rede

Desta sessão na nuvem, o proxy de saída **recusa** (`CONNECT 403`) os hosts `www.b3.com.br`, `b3.com.br`, `arquivos.b3.com.br`, `bvmf.bmfbovespa.com.br` e `cran.r-project.org`. Por isso:

- **nenhum PDF da B3 foi salvo como arquivo binário** aqui;
- **nenhum pregão de amostra foi baixado** (nem BDI, nem COTAHIST, nem IN/PR);
- os PDFs foram **lidos pela ferramenta WebFetch**, que devolve só um texto já processado por um modelo, não o PDF. As tabelas de campos das notas vêm desse texto. Confira os nomes das tags no PDF original antes de codificar.

`robots.txt`: `https://www.b3.com.br/robots.txt` e `https://arquivos.b3.com.br/robots.txt` deram erro de cliente pelo WebFetch e não puderam ser lidos. `https://raw.githubusercontent.com/robots.txt` responde 404 (sem regras). Ritmo usado: uma requisição por vez por host, com mais de 2 s entre elas.

Para baixar os PDFs e um pregão de amostra numa máquina com acesso, use `../scripts/baixar-amostras.sh`. O script não executa nada do que baixa.

## Lidos pelo WebFetch (texto processado, não salvo como binário)

| # | URL | Resultado |
|---|---|---|
| 1 | https://b3.com.br/data/files/1E/D1/BA/58/C841B810E9C1AAA8AC094EA8/DerivativesOpenPositionFile%202023.pdf | ok: 17 campos (nota 02) |
| 2 | https://b3.com.br/data/files/52/74/1E/14/4BA6D8103152D4C8AC094EA8/Glossario%20InstrumentsConsolidatedFile%202024.pdf | ok: 52 campos, v5 de 02/02/2024 (nota 01) |
| 3 | https://www.b3.com.br/data/files/F8/42/7A/61/FEC4A8103234E0A8AC094EA8/TradeInformationConsolidatedFileV3_PT.pdf | ok: 15 campos, v3 de 15/05/2023 (nota 03) |
| 4 | https://www.b3.com.br/data/files/65/50/AD/26/29C8B51095EE46B5790D8AA8/HistoricalQuotations_B3.pdf | ok: layout de 245 bytes (nota 04) |
| 5 | https://b3.com.br/data/files/BF/F1/58/15/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Posicao_Em_Aberto.pdf | ok: é do **BTB (aluguel)**, não de opções (nota 02) |
| 6 | https://b3.com.br/data/files/D4/52/03/F5/A86B0A105BF9020AAC094EA8/Catalogo-de-Mensagens-Cadastro-de-Instrumento.pdf | ok: BVBG.028.02, v2.9 de 13/03/2026 (nota 01) |
| 7 | https://www.b3.com.br/data/files/E1/93/18/98/A76A0A105BF9020AAC094EA8/CE 052-2026-VNC INCLUSAO DE NOVOS CAMPOS OPCIONAIS NO ARQUIVO BVBG028_PT.pdf | ok (nota 01) |
| 8 | https://www.b3.com.br/data/files/D5/02/29/32/B35FE910ADC36BE9AC094EA8/CE%20035-2026-VNC%20INCLUSAO%20DE%20NOVOS%20CAMPOS%20OPCIONAIS%20NO%20ARQUIVO%20BVBG028%20CADASTRO%20DE%20INSTRUMENTOS_PT.pdf | ok (nota 01) |
| 9 | https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/descricao-dos-arquivos/ | ok: 56 itens (nota 08) |
| 10 | https://www.b3.com.br/data/files/10/42/D4/6B/F8EF851052122C85790D8AA8/20161214-Premio%20de%20Referencia%20para%20Opcoes%20de%20Acoes%20-%20Evento.pdf | ok (nota 05) |
| 11 | https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf | ok (nota 05) |
| 12 | https://www.b3.com.br/data/files/28/C7/3A/11/33F7A9105B12E5A9AC094EA8/CE%20007-2025-VTEC%20MELHORIAS%20NO%20ACESSO%20AOS%20DADOS%20NO%20SITE%20B3_PT.pdf | ok (nota 07) |
| 13 | https://www.b3.com.br/data/files/74/C7/CA/6D/C926E810D34843E8AC094EA8/EC 001-2024-VTI_ing_dados de derivativos_2.pdf | ok (nota 07) |
| 14 | https://arquivos.b3.com.br/bdi/download/bdi/2024-07-02/BDI_05_20240702_en-Us.pdf | ok: só OI agregado por mercado e opções flexíveis |
| 15 | https://rdrr.io/github/wilsonfreitas/rbmfbovespa/src/legacy/tpl-premio.R | ok: layout do Premio.txt (nota 05) |
| 16 | https://packages.ropensci.org/rb3/doc/manual.html | ok: cerca de 21 pregões no BDI |
| 17 | https://brapi.dev/blog/api-open-interest-opcoes-b3-posicoes-em-aberto | ok (nota 02, só contingência) |
| 18 | https://github.com/flowtradelab/flow/pull/4 | ok: usa DerivativesOpenPosition + InstrumentsConsolidated por TckrSymb |
| 19 | https://github.com/guilhermegor/filings-b3 | ok |

Falharam (erro de cliente ou de servidor no site): as páginas HTML de posições em aberto, séries autorizadas, pesquisa por pregão e layout dos arquivos; `arquivos.b3.com.br/bdi/tabelas`; `arquivos.b3.com.br/bdi/table/workday`; `BDI_03-1_20260602_en-Us.pdf`; `bmf.com.br/arquivos1/arquivos_ipn-v2.asp`; a árvore `github.com/ropensci/rb3/tree/main/b3-docs` (bloqueada pelo robots.txt do GitHub).

## Baixados de verdade (curl, por hosts liberados)

| Pasta | Origem | Licença | Para quê |
|---|---|---|---|
| `rb3-github/` | https://raw.githubusercontent.com/ropensci/rb3/main/inst/extdata/templates/*.yaml, `R/downloaders.R`, `R/readers.R`, `NEWS.md` | MIT (rb3) | Padrões de URL de COTAHIST, PR (BVBG.086), TS e exportação CSV do BDI |
| `filings-b3-0.3.5/` | sdist https://files.pythonhosted.org/packages/d6/da/1fbc1b248c3ae69d7b533b42d99c0204003701a97c68b48e3743d24cc74f/filings_b3-0.3.5.tar.gz | ver `LICENSE` | API do BDI (POST, paginação, eco de páginas), IN{aammdd}.zip (BVBG.028) |
| `b3-open-data-1.0.4/` | sdist https://files.pythonhosted.org/packages/23/47/185f0f02d21e4f12524d663121ebb58bae216d56947c270dbe69c64c2edd/b3_open_data-1.0.4.tar.gz | MIT | Antiga API "Dados Públicos" (descontinuada em 31/03/2026) e nomes reais das colunas |
