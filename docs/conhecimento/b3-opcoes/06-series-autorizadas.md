# 06. Séries autorizadas

Acesso: 2026-11-04. Legenda: **[C]** documento da B3; **[T]** código de terceiros; **[S]** suposição.

- Página de consulta: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/opcoes/series-autorizadas/
- **Não foi lida.** O WebFetch deu erro de cliente, e o curl foi bloqueado pelo proxy desta sessão. Por isso não há confirmação de colunas, botão de download nem origem dos dados (iframe ou API).
- A busca na web não achou arquivo de download próprio para séries autorizadas.

## O que substitui, com arquivo estruturado

O conjunto de séries autorizadas é o próprio **cadastro de instrumentos** do pregão (nota 01):

1. **BVBG.028 (`IN{aammdd}.zip`), bloco `OptnOnEqtsInf`:** todas as opções de ações, ETFs e índice cadastradas no dia, com TckrSymb, ExrcPric, XprtnDt, OptnTp, OptnStyle, SrsTp, PrtcnFlg, objeto e datas de início e fim de negociação [C]. **É a fonte recomendada.**
2. **InstrumentsConsolidated** (BDI "Cadastro de instrumentos"), filtrando MktNm = OPC/OPV, ou SgmtNm = Ações – Derivativos [C].
3. **Prêmio de Referência**, que cobre "todas as opções autorizadas" [C] (nota 05). Serve para conferir se a lista está completa.

## Teste a fazer (máquina com acesso)

Abra a página num navegador comum, sem login, e anote:
- as colunas;
- se há botão de CSV ou TXT;
- a URL de dados no DevTools.

Depois compare a contagem de séries de PETR4 com o bloco `OptnOnEqtsInf` do IN do mesmo dia.

## Traz? (pelo BVBG.028)

| Strike | Vencimento | Tipo | Estilo | Coberto/travado/descoberto | Titulares/lançadores |
|---|---|---|---|---|---|
| sim | sim | sim | sim | não | não |
