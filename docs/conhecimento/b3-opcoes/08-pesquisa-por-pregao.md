# 08. Pesquisa por pregão (arquivos por sessão)

Acesso: 2026-11-04. Legenda: **[C]** documento da B3; **[T]** código de terceiros; **[S]** suposição a testar.

## Páginas

- Página: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/pesquisa-por-pregao/. **Não foi lida**: o site deu erro de cliente. O fontes-dados.md anterior também tinha falhado.
- Descrição dos arquivos (lida): https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/descricao-dos-arquivos/ [C].
- Layout dos arquivos: https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/layout-dos-arquivos/. Não foi lida (erro). É onde ficam o catálogo e o XSD do BVBG.028 ([CE 052/2026](https://www.b3.com.br/data/files/E1/93/18/98/A76A0A105BF9020AAC094EA8/CE%20052-2026-VNC%20INCLUSAO%20DE%20NOVOS%20CAMPOS%20OPCIONAIS%20NO%20ARQUIVO%20BVBG028_PT.pdf)).

## Download

- Padrão: **GET `https://www.b3.com.br/pesquisapregao/download?filelist={CÓDIGO}{aammdd}.{ext}`** [T: rb3, filings-b3, b3archives].
- O caminho não leva nome de arquivo; ele vai na query.
- O filings-b3 conta **42 conjuntos** de dados nesse endpoint [T].
- Os `.ex_` são executáveis autoextraíveis com ZIP dentro. **Abra como ZIP e nunca execute.**

| Código | Arquivo | Ext. | Confirmação |
|---|---|---|---|
| **IN** | **BVBG.028.02 Cadastro de instrumentos** (nota 01). ZIP dentro de ZIP, uma foto XML por momento do dia; use a de maior `CreDtAndTm` | .zip | [T] filings-b3 |
| **PR** | **BVBG.086.01 Pricing Report** (nota 03). Tem OI total por instrumento; pode haver vários arquivos: use o mais novo | .zip | [T] rb3, b3archives |
| IR | BVBG.087.01 Index Report | .zip | [T] filings-b3 (citado) |
| **TS** | Taxas de Mercado para Swaps (`TaxaSwap.txt`, cerca de 120 curvas, entre elas PRE e DIC) | .ex_ | [T] rb3 |
| `Premio` | **Prêmio de Referência para Opções** (nota 05). Código do filelist **não confirmado** | ? | [C] nome; [S] código |
| `Deltas` | Deltas de opções padronizadas (limites de posição) | ? | [C] nome |
| `PosTrav` | Posições travadas (agro) | ? | [C] nome |
| `BD_Final` / `BDAtual` | Negócios em pregão, final / após processamento noturno | ? | [C] nome |
| `SupVol` | Superfície de vol por delta (opções flexíveis de balcão) | ? | [C] nome |
| `CONTRCAD` | Contratos cadastrados (derivativos) | ? | [C] nome |

A descrição dos arquivos tem 56 itens. Os de interesse estão acima. "Posições Travadas para Equities" aparece como **"Não encontrado"** na própria página [C].

## Histórico

A quantidade de pregões disponível **não foi confirmada** [S]. Há duas indicações:
- o rb3 manda usar o BVBG.086 para dados mais antigos que os 21 pregões do BDI, o que sugere retenção maior;
- o b3archives (2020) baixava PR de datas passadas.

**Teste:** pedir `IN` e `PR` de um pregão de 60, 250 e 1.000 dias atrás.

## Horário

- IN: na abertura, com fotos ao longo do dia [C].
- PR: após o pregão [S].
- Prêmio: sincronizado com o encerramento [C].
- TS: diário [T].
