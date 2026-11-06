# Regras de vencimento das opções na B3

Acesso: 2026-11-04. Pasta: `/mnt/project-files/jumba/conhecimento/b3-outros/`. Os textos lidos estão em `raw/webfetch/` (texto processado pelo WebFetch, não o PDF original).

Legenda: **[C]** confirmado em documento da B3 lido nesta coleta; **[T]** código de terceiros; **[S]** suposição ou conhecimento não conferido aqui.

## Resumo

| Produto | Código | Data de vencimento | Se o dia não tiver pregão | Último dia de negociação | Estilo | Fonte |
|---|---|---|---|---|---|---|
| Opções mensais sobre ações, units, ETFs, BDRs | ex.: PETRA300 | **3ª sexta-feira do mês** | **Sessão imediatamente anterior**. Feriado extraordinário: adia para a sessão seguinte | No vencimento | Call: americana ou europeia (a série define). Put: europeia | [C] [OC 007/2026-VPC](https://www.b3.com.br/data/files/05/A1/CA/C2/EFE2C91076A8EEB9AC094EA8/OC%20007-2026-VPC%20ALTERACOES%20CONTRATOSTERMO%20OPCOES%20ACOES%20UNITS%20ETFS%20BDRS%20FUTURO%20ACOES%20UNITS%20REPUBLICACAO%20CONTRATOS%20DERIVATIVOS%20EQUITIES.pdf), de 05/02/2026 |
| Opções semanais sobre ações, units, BDRs, cotas de fundos | sufixo **W1, W2, W4, W5** (não existe W3) | **Toda sexta-feira, menos a 3ª** | Sessão imediatamente anterior. Feriado extraordinário: adia | No vencimento | Call: americana ou europeia. Put: europeia | [C] [OC 006/2026-VPC](https://www.b3.com.br/data/files/D7/A3/54/6B/45E2C91076A8EEB9AC094EA8/OC%20006-2026-VPC%20ALTERACOES%20CONTRATOS%20OPCAO%20DE%20COMPRA%20E%20VENDA%20VENCIMENTOS%20SEMANAIS%20ACAO%20UNIT%20ETF%20BDR_PT.pdf) e [FAQ das semanais](https://www.b3.com.br/data/files/55/83/20/ED/CE98D8103152D4C8AC094EA8/B3%20Opcoes%20Semanais%20-%20Perguntas%20Frequentes.pdf) |
| Opções mensais sobre Ibovespa | IBOV | **Quarta-feira mais próxima do dia 15** (a quarta entre os dias 12 e 18) | **Próxima sessão** | No vencimento | Europeia | [C] [página do produto](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/opcoes-sobre-ibovespa.htm) |
| Opções semanais e diárias sobre Ibovespa | IBOV | **Todos os dias de sessão**, menos o dia do vencimento mensal (desde 17/11/2025) | **Não há vencimento** naquele dia. Feriado extraordinário: adia | No vencimento | Europeia | [C] [OC 045/2025-VPC](https://www.b3.com.br/data/files/AC/C5/E4/D2/A4DE9910F5D34899AC094EA8/OC%20045-2025-VPC%20B3%20Novos%20Vencimentos%20das%20Op%C3%A7%C3%B5es%20Semanais%20sobre%20%C3%8Dndice%20Bovespa_PT.pdf), de 16/10/2025 |
| Opções sobre dólar comercial (padrão) | DOL (USD 50.000) | **1º dia útil do mês** | Não informado na página [S: dia útil já é a regra] | **Sessão anterior** ao vencimento | Europeia | [C] [página do produto](https://b3.com.br/pt_br/produtos-e-servicos/negociacao/moedas/opcoes-sobre-taxa-de-cambio-de-reais-por-dolar-comercial.htm) |
| Mini opções semanais/diárias de dólar | WDT (USD 10.000) | Fixing em **qualquer dia útil** com sessão; vencimento na **sessão seguinte** ao fixing (desde 04/05/2026) | Feriado extraordinário: fixing e vencimento adiados | Data de fixing | Europeia. Liquida pela PTAX de venda do fixing | [C] [OC 017/2026-VPC](https://www.b3.com.br/data/files/6C/B4/07/0B/F996D910973186D9AC094EA8/OC%20017-2026-VPC%20NOVOS%20VENCIMENTOS%20DOS%20MINI%20CONTRATOS%20DE%20OPCOES%20SEMANAIS%20DE%20DOLAR_PT.pdf), de 07/04/2026 |
| Futuro DI1 (referência para a curva) | DI1 | **1ª sessão de negociação do mês** | — | Sessão anterior | — | [C] [OC 055/2024-PRE](https://www.b3.com.br/data/files/FF/C5/51/86/158EE810C54843E8DC0D8AA8/OC%20055-2024%20PRE%20Contratos%20FE%20-%20Juros%20(PT).pdf) |

### Detalhes

- **Semanais de ações:** a B3 cadastra 5 semanas seguidas, com limite de 10 semanas para abrir séries. O primeiro vencimento foi 09/02/2024 (W2). O ticker segue `AAAABCCCWn`; para exercício, acrescenta-se `E` (ex.: `B3SAO275W5E`). Exemplos do FAQ: `B3SAA300W1` (call, 1ª sexta de janeiro) e `B3SAM300W2` (put, 2ª sexta de janeiro) [C].
- **"W1 de janeiro" pode vencer em dezembro.** Ex.: a 1ª sexta de jan/2027 é 01/01/2027 (feriado). A sessão anterior é 30/12/2026, porque 31/12 não tem pregão [cálculo nosso].
- **Opções diárias:** o código das opções com vencimento diário está na seção 3.2.5.1 do Manual de Procedimentos Operacionais de Negociação, em vigor desde 04/05/2026 ([OC 027/2026-VNC](https://www.b3.com.br/data/files/A5/06/EB/CC/1A4DD910579CDBD9AC094EA8/OC%20027-2026-VNC%20ALTERACOES%20NO%20MANUAL%20DE%20PROCEDIMENTOS%20OPERACIONAIS%20DE%20NEGOCIACAO%20DA%20B3_PT.pdf)) [C]. **O texto do manual não foi lido**, então a regra do código continua em aberto. O OC 045/2025 remete ao item 3.2 do mesmo título.
- **Letra do mês nos tickers mensais de ações:** calls de A (jan) a L (dez) e puts de M (jan) a X (dez) [S: conhecimento comum, não conferido no manual nesta coleta].
- **Exercício:** é automático no vencimento para séries dentro do dinheiro, e o titular pode pedir o bloqueio [C OC 007/2026]. Pela grade do OC 001/2024-VNC (revogado pelo OC 013/2024-PRE), o exercício manual vai das 10h às 15h45 no dia do vencimento, o automático de ações ocorre depois das 19h15 e o de índice depois das 18h. **Confirmar a grade vigente antes de usar** [C, documento revogado].
- **Ibovespa:** desde fev/2025 o ponto do índice vale R$ 0,01, com variação mínima de 5 pontos [C página do produto].
- **IND futuro e opções sobre futuro de Ibovespa:** não foram lidos nesta coleta. Pela regra do futuro, o vencimento é na quarta-feira mais próxima do dia 15 dos meses pares [S]. Conferir na página do produto antes de usar.
- **Opções sobre futuro de dólar:** não foram lidas. A regra do DOL acima é a da opção sobre a taxa de câmbio (disponível).

## Como calcular (para o motor)

```
vencimento_acao_mensal(ano, mes)  = sessao_anterior_ou_igual(terceira_sexta(ano, mes))
vencimento_acao_semanal(sexta)    = sessao_anterior_ou_igual(sexta)          # só sextas que não são a 3ª
vencimento_ibov_mensal(ano, mes)  = proxima_sessao_ou_igual(quarta_entre_12_e_18(ano, mes))
vencimentos_ibov_diarios(mes)     = todas as sessões do mês, menos o vencimento mensal
vencimento_dol(ano, mes)          = primeiro_dia_util(ano, mes)
vencimento_di1(ano, mes)          = primeira_sessao(ano, mes)
```

- "Sessão" = dia com pregão na B3 (`feriados-b3-2026-2028.json`, campo `sem_pregao`).
- "Dia útil" para DU/252 = calendário ANBIMA. Nele, 24/12 e 31/12 **contam** como dias úteis (campo `dia_util_anbima`).
- O script `scripts/gerar_vencimentos.py` gera a tabela abaixo a partir do JSON.

## Vencimentos mensais calculados, 2026 a 2028

`*` = dia ajustado por falta de pregão. Os anos de 2027 e 2028 usam o calendário **derivado** (a B3 ainda não publicou). A coluna DI1/futuros traz a 1ª sessão do mês: vale para o DI1 [C]. Para os futuros de dólar, supõe-se a mesma data [S].

| Mês | Opções de ações (mensal) | Opções de IBOV (mensal) | Opções de DOL | DI1 / WDO/DOL futuro [S] |
|---|---|---|---|---|
| 01/2026 | 16/01/2026 (sex) | 14/01/2026 (qua) | 02/01/2026 (sex) | 02/01/2026 (sex) |
| 02/2026 | 20/02/2026 (sex) | 18/02/2026 (qua) | 02/02/2026 (seg) | 02/02/2026 (seg) |
| 03/2026 | 20/03/2026 (sex) | 18/03/2026 (qua) | 02/03/2026 (seg) | 02/03/2026 (seg) |
| 04/2026 | 17/04/2026 (sex) | 15/04/2026 (qua) | 01/04/2026 (qua) | 01/04/2026 (qua) |
| 05/2026 | 15/05/2026 (sex) | 13/05/2026 (qua) | 04/05/2026 (seg) | 04/05/2026 (seg) |
| 06/2026 | 19/06/2026 (sex) | 17/06/2026 (qua) | 01/06/2026 (seg) | 01/06/2026 (seg) |
| 07/2026 | 17/07/2026 (sex) | 15/07/2026 (qua) | 01/07/2026 (qua) | 01/07/2026 (qua) |
| 08/2026 | 21/08/2026 (sex) | 12/08/2026 (qua) | 03/08/2026 (seg) | 03/08/2026 (seg) |
| 09/2026 | 18/09/2026 (sex) | 16/09/2026 (qua) | 01/09/2026 (ter) | 01/09/2026 (ter) |
| 10/2026 | 16/10/2026 (sex) | 14/10/2026 (qua) | 01/10/2026 (qui) | 01/10/2026 (qui) |
| 11/2026 | 19/11/2026 (qui) * | 18/11/2026 (qua) | 03/11/2026 (ter) | 03/11/2026 (ter) |
| 12/2026 | 18/12/2026 (sex) | 16/12/2026 (qua) | 01/12/2026 (ter) | 01/12/2026 (ter) |
| 01/2027 | 15/01/2027 (sex) | 13/01/2027 (qua) | 04/01/2027 (seg) | 04/01/2027 (seg) |
| 02/2027 | 19/02/2027 (sex) | 17/02/2027 (qua) | 01/02/2027 (seg) | 01/02/2027 (seg) |
| 03/2027 | 19/03/2027 (sex) | 17/03/2027 (qua) | 01/03/2027 (seg) | 01/03/2027 (seg) |
| 04/2027 | 16/04/2027 (sex) | 14/04/2027 (qua) | 01/04/2027 (qui) | 01/04/2027 (qui) |
| 05/2027 | 21/05/2027 (sex) | 12/05/2027 (qua) | 03/05/2027 (seg) | 03/05/2027 (seg) |
| 06/2027 | 18/06/2027 (sex) | 16/06/2027 (qua) | 01/06/2027 (ter) | 01/06/2027 (ter) |
| 07/2027 | 16/07/2027 (sex) | 14/07/2027 (qua) | 01/07/2027 (qui) | 01/07/2027 (qui) |
| 08/2027 | 20/08/2027 (sex) | 18/08/2027 (qua) | 02/08/2027 (seg) | 02/08/2027 (seg) |
| 09/2027 | 17/09/2027 (sex) | 15/09/2027 (qua) | 01/09/2027 (qua) | 01/09/2027 (qua) |
| 10/2027 | 15/10/2027 (sex) | 13/10/2027 (qua) | 01/10/2027 (sex) | 01/10/2027 (sex) |
| 11/2027 | 19/11/2027 (sex) | 17/11/2027 (qua) | 01/11/2027 (seg) | 01/11/2027 (seg) |
| 12/2027 | 17/12/2027 (sex) | 15/12/2027 (qua) | 01/12/2027 (qua) | 01/12/2027 (qua) |
| 01/2028 | 21/01/2028 (sex) | 12/01/2028 (qua) | 03/01/2028 (seg) | 03/01/2028 (seg) |
| 02/2028 | 18/02/2028 (sex) | 16/02/2028 (qua) | 01/02/2028 (ter) | 01/02/2028 (ter) |
| 03/2028 | 17/03/2028 (sex) | 15/03/2028 (qua) | 01/03/2028 (qua) | 01/03/2028 (qua) |
| 04/2028 | 20/04/2028 (qui) * | 12/04/2028 (qua) | 03/04/2028 (seg) | 03/04/2028 (seg) |
| 05/2028 | 19/05/2028 (sex) | 17/05/2028 (qua) | 02/05/2028 (ter) | 02/05/2028 (ter) |
| 06/2028 | 16/06/2028 (sex) | 14/06/2028 (qua) | 01/06/2028 (qui) | 01/06/2028 (qui) |
| 07/2028 | 21/07/2028 (sex) | 12/07/2028 (qua) | 03/07/2028 (seg) | 03/07/2028 (seg) |
| 08/2028 | 18/08/2028 (sex) | 16/08/2028 (qua) | 01/08/2028 (ter) | 01/08/2028 (ter) |
| 09/2028 | 15/09/2028 (sex) | 13/09/2028 (qua) | 01/09/2028 (sex) | 01/09/2028 (sex) |
| 10/2028 | 20/10/2028 (sex) | 18/10/2028 (qua) | 02/10/2028 (seg) | 02/10/2028 (seg) |
| 11/2028 | 17/11/2028 (sex) | 16/11/2028 (qui) * | 01/11/2028 (qua) | 01/11/2028 (qua) |
| 12/2028 | 15/12/2028 (sex) | 13/12/2028 (qua) | 01/12/2028 (sex) | 01/12/2028 (sex) |

Ajustes por feriado:
- semanal ações W1 04/2026: 03/04/2026 (sex) sem pregão → 02/04/2026 (qui)
- semanal ações W1 05/2026: 01/05/2026 (sex) sem pregão → 30/04/2026 (qui)
- ações mensal 11/2026: regra cai em 20/11/2026 (sex), sem pregão → 19/11/2026 (qui)
- semanal ações W4 12/2026: 25/12/2026 (sex) sem pregão → 23/12/2026 (qua)
- semanal ações W1 01/2027: 01/01/2027 (sex) sem pregão → 30/12/2026 (qua)
- semanal ações W4 03/2027: 26/03/2027 (sex) sem pregão → 25/03/2027 (qui)
- semanal ações W4 12/2027: 24/12/2027 (sex) sem pregão → 23/12/2027 (qui)
- semanal ações W5 12/2027: 31/12/2027 (sex) sem pregão → 30/12/2027 (qui)
- ações mensal 04/2028: regra cai em 21/04/2028 (sex), sem pregão → 20/04/2028 (qui)
- semanal ações W2 04/2028: 14/04/2028 (sex) sem pregão → 13/04/2028 (qui)
- IBOV mensal 11/2028: regra cai em 15/11/2028 (qua), sem pregão → 16/11/2028 (qui)
- semanal ações W5 12/2028: 29/12/2028 (sex) sem pregão → 28/12/2028 (qui)

Semanais de ações (sextas, sem a 3ª), contagem por ano:
2026 40
2027 41
2028 40

## Limitações

- A errata do calendário de 2026 ([OC 041/2026-VNC](https://www.b3.com.br/data/files/20/57/01/AA/06A1F910ADC36BE9AC094EA8/OC%20041-2026-VNC%20ERRATA%20-%20CALENDARIO%20DE%20FERIADOS%20EM%202026_PT.pdf)) não abriu.
- 2027 e 2028 são calculados. Refazer quando a B3 publicar os ofícios.
- Um feriado extraordinário (não previsto) muda a regra: o vencimento passa para a sessão seguinte em todos os produtos acima.
- Opções sobre IND futuro, opções sobre futuro de dólar e o código das opções diárias não foram confirmados.
