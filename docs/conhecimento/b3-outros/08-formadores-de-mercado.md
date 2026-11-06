# 08. Formadores de mercado (FM) de opções

Acesso: 2026-11-04. Legenda: [C] B3 lido; [T] terceiros; [S] suposição.

## Páginas e arquivos da B3

| Programa | Vigência | Parâmetros (xlsx) | Ofício |
|---|---|---|---|
| Opções mensais sobre ações, units, ETFs, BDRs e índices | 02/06/2025 a **26/02/2027** | [Mensal Parametros 2026-09-30.xlsx](https://www.b3.com.br/data/files/C3/02/30/95/252F0A105BF9020AAC094EA8/Mensal%20Parametros%20-%20Monthly%20MM%20Parameter%202026-09-30.xlsx) | [OC 031/2026-PRE](https://www.b3.com.br/data/files/9B/D2/A7/68/CA3BF91094DCD8F9AC094EA8/OC%20031-2026%20PRE%20PRORROGACAO%20PROGRAMA%20DE%20FM%20OPCOES%20SOBRE%20ACOES%20BDRS%20UNITS%20ETFS%20E%20OPCOES%20SOBRE%20%C3%8DNDICES%20COM%20VENCIMENTOS%20MENSAIS_PT.pdf), de 30/07/2026 |
| Opções semanais sobre ações, units, ETFs e índices | 02/06/2025 a 26/02/2027 | [Opcao Semanal MM Parametros 2026-09-04.xlsx](https://www.b3.com.br/data/files/65/E3/1E/FC/08180A105BF9020AAC094EA8/Opcao%20Semanal%20MM%20Parametros%20-%20Weekly%20Option%20Parameters%202026-09-04.xlsx) | [OC 030/2026-PRE](https://www.b3.com.br/data/files/23/B0/FC/58/248CF91094DCD8F9AC094EA8/OC%20030-2026%20PRE%20PRORROGACAO%20DO%20PROGRAMA%20DE%20FORMADOR%20DE%20MERCADO%20DAS%20OPCOES%20COM%20VENCIMENTOS%20SEMANAIS_2027_PT%20_1_.pdf) |
| Opções sobre S&P/B3 Bovespa VIX | 08/12/2025 a 28/06/2027 | [Derivativos de VIX FM.xlsx](https://www.b3.com.br/data/files/00/14/5D/25/66FDA9105B12E5A9AC094EA8/Derivativos%20de%20VIX%20FM%20-%20MM%20VIX%20Derivatives.xlsx) | [OC 030/2026-VPC](https://www.b3.com.br/data/files/48/C0/3D/E3/548CF91094DCD8F9AC094EA8/OC%20030-2026-VPC%20PRORROGACAO%20PROGRAMA%20DE%20FORMADOR%20DE%20MERCADO%20CONTRATO%20FUTURO%20OPCOES%20SOBRE%20INDICE%20SPB3%20BOVESPA%20VIX_PT.pdf) |
| **Consolidado de opções** | — | [Programa de FM Opcoes - Out 28 - 2026.xlsx](https://www.b3.com.br/data/files/6D/D6/D0/C2/08281A10F2BF771AAC094EA8/Programa%20de%20FM%20Opcoes%20-%20Options%20MM%20Program%20-%20Out%2028%20-%202026.xlsx) | — |

- **Página dos programas de opções:** https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/formador-de-mercado/programas-listados/opcoes.htm [C].
- **Séries obrigatórias:** https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/formador-de-mercado/series-obrigatorias-de-atuacao/ (não lida).

## Regras de atuação (OC 031/2026 e OC 009/2025-VPC) [C]

- **Opções individuais:** atuação em 2 vencimentos obrigatórios. No 4º dia útil antes do 1º vencimento, a atuação passa para os 2 seguintes.
- **Puts de PETR4 e VALE3:** vencimentos trimestrais (janeiro, abril, julho e outubro).
- **Opções de índice:** os 6 primeiros vencimentos.
- **Tempo mínimo:** 10 minutos dentro dos 30 minutos finais do pregão. Spread e quantidade mínima ficam na planilha de parâmetros.
- **Credenciamento:** até 12 FMs no programa mensal. Benefícios:
  - BOVA11, PETR4 e VALE3: 85% de desconto nas opções e 25% no delta hedge isento;
  - demais ativos: 100% nas opções e 50% no delta hedge.

## Lista nominal de FMs por ativo

- **Não foi encontrada em texto.** Nenhuma página ou ofício lido traz o nome das instituições por ativo. Os credenciamentos saem "pelos meios usuais de comunicação" da B3 [C].
- **Candidata:** a planilha consolidada (.xlsx). O WebFetch não lê xlsx e o proxy bloqueia o download, então o conteúdo não foi visto [S].
- **Uso no Trader Flow** (grupo Market Makers):
  - cruzar o código de participante dos FMs com `nBuyAgent`/`nSellAgent` da ProfitDLL e com `LenderParticipantCode`/`BorrowerParticipantCode` do BTB;
  - para isso, a lista precisa ter o **código do participante**, não só o nome [S].
- **Sem a lista**, a alternativa é inferir os FMs pelo comportamento (presença contínua nas séries obrigatórias), com a Fita de opções [S].
