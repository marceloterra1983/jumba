# B3 (outras fontes públicas): índice

Acesso: 2026-11-04. Pasta: `docs/conhecimento/b3-outros/`. Antes desta pasta, leia `../../pesquisa/fontes-dados.md` e `critic.md`. Sobre cadastro, OI, BDI e Pesquisa por pregão, veja a pasta irmã `../b3-opcoes/`.

Legenda: **[C]** documento da B3 lido nesta coleta; **[T]** código de terceiros; **[S]** suposição a testar.

## Situação da coleta

- O proxy da nuvem bloqueia B3, ANBIMA, CVM, Tesouro e BCB. **Nenhum binário da B3 foi baixado.** Os documentos foram lidos pelo WebFetch (resumos em `raw/webfetch/`, um por documento). Para baixar os originais numa máquina com acesso, há o script `scripts/baixar-documentos.sh`, que não foi executado.
- Os termos da B3 vedam coleta automatizada, inclusive por IA. Aqui só se leu documentação. O Marcelo já decidiu seguir com o scraper (Etapa 2).

## Notas

| Nota | Assunto |
|---|---|
| [01-curva-de-juros.md](01-curva-de-juros.md) | TS (TaxaSwap), BVBG.086, ajustes do DI1, Manual de Curvas (flat forward 252), PU do DI1, ANBIMA ETTJ |
| [02-cdi-diario.md](02-cdi-diario.md) | "DI over" no Boletim Diário (CSV, 40 anos); fim do site estatísticas da Cetip em 15/12/2025 |
| [03-emprestimo-de-ativos-btb.md](03-emprestimo-de-ativos-btb.md) | **Empréstimos registrados** (taxas doadora e tomadora: mín., média, máx.), NEGOCIOSBTB, posição em aberto |
| [04-participacao-investidores.md](04-participacao-investidores.md) | Seção do BDI_02 (acumulado do mês, por mercado); derivativos sem série gratuita |
| [05-eventos-corporativos-proventos.md](05-eventos-corporativos-proventos.md) | sistemaswebb3-listados (data-com `lastDatePrior`), consulta "ajuste de proventos", ProfitDLL, CVM IPE |
| [06-ajuste-strike-proventos.md](06-ajuste-strike-proventos.md) | MPO da Câmara 7.9.1 (págs. 211 a 223, não lida); valor líquido de impostos; JCP a 17,5%; OC 141/2023 |
| [07-feriados-calendario.md](07-feriados-calendario.md) | Regras e tabela 2026 (oficial), 2027 e 2028 (derivados) |
| [feriados-b3-2026-2028.json](feriados-b3-2026-2028.json) | Dados: `sem_pregao_b3`, `dia_util_anbima`, status, Cinzas, nº de sessões e de DU |
| [vencimentos-regras.md](vencimentos-regras.md) | Vencimentos mensais e semanais de ações, IBOV mensal e diário, DOL, WDT, DI1; tabela 2026 a 2028 |
| [08-formadores-de-mercado.md](08-formadores-de-mercado.md) | Programas de FM de opções, regras de atuação, planilhas .xlsx; lista nominal não encontrada |
| [raw/MANIFESTO.md](raw/MANIFESTO.md) | Cada URL lida, tentada ou baixada |
| `scripts/` | `gerar_calendario.py`, `gerar_vencimentos.py`, `baixar-documentos.sh` |

## Dado → melhor fonte pública

| Dado | 1ª fonte (B3) | Reserva | Freq. / histórico |
|---|---|---|---|
| Curva PRE de fechamento | TS `TS{aammdd}.ex_` (curva PRE) [T] | Ajuste do DI1 (BVBG.086 ou BDI) + CDI, flat forward 252 [C método]; ANBIMA ETTJ para conferir | Diário; retenção do TS por medir |
| Ajuste do DI1 | BVBG.086 `AdjstdQt`/`AdjstdQtTax` [T] | BDI `ConsolidatedTradesDerivatives` (cerca de 21 pregões) [T] | Diário |
| PU e convenção | OC 055/2024: `PO = 100000/(1+i)^(n/252)`, DU pelo calendário ANBIMA [C] | — | — |
| CDI diário | BDI "DI over" (média, fator diário, Selic) [C] | — | D-1, 40 anos |
| Taxas BTB doadora e tomadora | BDI › Clearing › **Empréstimos registrados** [C] | NEGOCIOSBTB (taxa por negócio) [C] | Abertura, D-1 |
| Saldo BTB | BDI `BTBLendingOpenPosition` [T] | — | Abertura, D-1 |
| Participação por investidor (ações) | BDI_02, PDF [C] | — | Acumulado do mês, D-2 |
| Participação por investidor (futuros) | **Nenhuma série de volume.** OI por tipo de participante existe, mas a página atual não foi achada [S] | — | — |
| Proventos e data-com | sistemaswebb3-listados `GetListedSupplementCompany` [T] | ProfitDLL `SubscribeAdjustHistory`; CVM IPE | Por evento |
| Ajuste de strike | Consulta "ajuste de proventos" (Hub) [C nome] + diferença do `ExrcPric` no BVBG.028 | MPO 7.9.1 para recalcular | Diário |
| Feriados | Ofício anual da B3 (2026) [C] | ANBIMA para 2027 e 2028 [C] | Anual |
| Vencimentos | OC 007/2026, 006/2026, 045/2025, 017/2026, página DOL [C] | — | — |
| Formadores de mercado | Planilhas .xlsx dos programas [C link] | Inferir pelo comportamento | Trimestral |

## Fontes SEM alternativa pública gratuita (ou não achada)

1. **Volume diário por tipo de investidor em futuros** (IND/WIN, DOL/WDO, DI1). O BDI só cobre o segmento de ações, acumulado no mês. Fonte paga: UP2DATA.
2. **Posição em aberto por tipo de participante em futuros.** Ela existe (citada por corretoras como "Contratos em aberto (B3)"), mas a página da B3 não foi localizada. **Ainda sem fonte confirmada**, e é preciso procurar no BDI.
3. **Calendário futuro de proventos ("esperados").** A B3 só mostra o que já foi aprovado e comunicado. Nenhuma fonte pública dá dividendos projetados para o BSM.
4. **Histórico longo do BDI** (Empréstimos registrados, ajustes, negócios consolidados): cerca de 21 pregões. Além disso, só gravando todo dia ou pelo UP2DATA, que é pago. O TS e o BVBG.086 podem ter histórico maior, mas isso não foi medido.
5. **Lista nominal de formadores de mercado por ativo, com código do participante.** Não foi achada em texto. Talvez esteja na planilha .xlsx, que não foi lida.
6. **Taxa e ajuste do DI1 durante o pregão.** A B3 só publica depois do fechamento. Em tempo real, só a ProfitDLL.
7. **Regras de ajuste de strike em texto integral** (MPO 7.9.1). É pública, mas não pôde ser lida aqui. Não falta fonte, falta acesso.

## O que muda em relação à pesquisa anterior

- **Taxas doadora e tomadora do BTB existem e são gratuitas** (Empréstimos registrados). Isso fecha a lacuna do critic.md.
- **CDI:** o site da Cetip acabou em 15/12/2025. A fonte agora é o BDI.
- **Opções de IBOV vencem todo dia** desde 17/11/2025. As **mini opções de dólar (WDT) vencem todo dia útil** desde 04/05/2026. As opções semanais de ações vencem em toda sexta-feira menos a 3ª. Isso muda o cálculo de T, a lista de vencimentos e as telas que somam vencimentos.
- **JCP:** o ajuste das opções usa IR de 17,5% desde 01/01/2026. A B3 passou a falar em "líquido de impostos" (OC 006/2026-VPE), o que também afeta dividendos tributados.
- **Dias úteis para DU/252:** a B3 usa o calendário ANBIMA, em que 24/12 e 31/12 são dias úteis sem pregão. O motor precisa de dois calendários: sessões da B3 e dias úteis.
- **Novembro de 2026:** a opção mensal de ações vence na **quinta, 19/11/2026**, porque 20/11 é feriado.
