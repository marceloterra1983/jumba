# 02. CDI (Taxa DI) diário

Acesso: 2026-11-04. Legenda: [C] B3 lido; [T] terceiros; [S] suposição.

## Fonte B3 (preferida)

| Item | Valor |
|---|---|
| Nome | Arquivo **"DI over"**, Boletim Diário do Mercado › Renda fixa › **Indicadores e Informativos › Taxas – DI PRÉ – Over** [C] |
| Página | https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/boletim-diario-do-mercado/ |
| Glossário | [Glossario_Taxas_DI_Over_balcao 4.pdf](https://www.b3.com.br/data/files/6A/F7/3F/35/2654D9101BEEB2D9AC094EA8/Glossario_Taxas_DI_Over_balcao%204.pdf): v1 de 15/12/2025; v2 de mar/2026 passou a consulta para ano a ano [C] |
| Formato | CSV [C] |
| Horário | "Diariamente no fechamento do dia", com o dado de D-1 [C]. Hora exata não informada |
| Histórico | Cerca de 40 anos [C]. O [CE 008/2025-VTEC](https://www.b3.com.br/data/files/FA/A2/31/7C/9389A9105B12E5A9AC094EA8/CE%20008-2025-VTEC_MELHORIA%20NO%20ACESSO%20AOS%20DADOS%20HISTORICOS%20DE%20RENDA%20FIXA%20NO%20SITE%20B3_PT.pdf) dá **DI – Taxas – Over de 06/03/1986 a 11/12/2025** e **DI – Índice de 02/01/2008 a 11/12/2025** (consulta histórica) [C] |
| Campos | `Data referência` (DD/MM/AAAA); `Número de operações`; `Volume financeiro`; `Média` (taxa média, % a.a.); `Fator diário`; `Taxa SELIC` [C] |
| Método | Taxa DI exponencial, fator diário, ano de 252 dias úteis [C] |

### Mudança de fonte

O site **estatisticas.cetip.com.br** (Séries Históricas da Cetip) foi **desativado em 15/12/2025**. Os dados foram para o Boletim Diário [C: CE 008/2025-VTEC]. Robôs que usavam o FTP ou o site da Cetip precisam ser revistos.

**Rota do BDI:** não confirmada [S]. As candidatas são `EconomicIndicators`, que existe e foi medida pelo filings-b3 [T], e uma tabela própria de "Taxas DI Over". Para achar o nome, leia as `<option>` de `#selectTabelas` em `https://arquivos.b3.com.br/bdi/tabelas`.

## Uso no sistema

- **Fator diário** → acumula o CDI e alimenta o `FC` do DI1 (nota 01) e a "taxa contra o CDI" das estruturas (Find Your Trade).
- **Média do dia** → vértice de 1 dia útil da curva PRE.
- O valor de D só sai depois do fechamento. **Durante o dia, use o último CDI publicado.**

## Alternativa (só se a B3 falhar)

- Banco Central, SGS série 12 (CDI) e 11 (Selic). Não está entre as fontes autorizadas nesta tarefa e não foi acessado [S].
- ANBIMA: não publica o CDI.

## Limitações

- Nenhum CSV foi baixado: o proxy bloqueia a B3. O glossário não traz nome técnico de coluna nem exemplo de valor.
- O glossário só cita a média. Mínimo, máximo, moda e mediana não aparecem.
