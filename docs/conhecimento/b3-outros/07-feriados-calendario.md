# 07. Calendário de feriados da B3, 2026 a 2028

Acesso: 2026-11-04. Arquivo de dados: [`feriados-b3-2026-2028.json`](feriados-b3-2026-2028.json), gerado por `scripts/gerar_calendario.py` (não lê nada baixado).

## Fontes

| Ano | Status | Fonte |
|---|---|---|
| 2026 | **Oficial** | [Notícia da B3 de 09/01/2026](https://www.b3.com.br/pt_br/noticias/calendario-de-negociacao-da-b3-confira-o-funcionamento-da-bolsa-em-2026.htm) [C]. Também o [OC 054/2025-VNC](https://www.b3.com.br/data/files/C2/E3/28/AD/4FAEA9105B12E5A9AC094EA8/OC%20054-2025-VNC%20CALENDARIO%20DE%20FERIADOS%20EM%202026%20E%20FUNCIONAMENTO%20DA%20B3%20EM%2018022026%20QUARTAFEIRA%20DE%20CINZAS_PT.pdf), de 04/12/2025, revogado pelo OC 003/2026-VNC [C]. A errata [OC 041/2026-VNC](https://www.b3.com.br/data/files/20/57/01/AA/06A1F910ADC36BE9AC094EA8/OC%20041-2026-VNC%20ERRATA%20-%20CALENDARIO%20DE%20FERIADOS%20EM%202026_PT.pdf), de 30/06/2026, **não abriu** |
| 2027 | **Derivado** | A B3 ainda não publicou (costuma sair em dezembro). Regras da B3 + [ANBIMA 2027](https://www.anbima.com.br/feriados/fer_nacionais/2027.asp) [C] |
| 2028 | **Derivado** | Regras da B3 + [ANBIMA 2028](https://www.anbima.com.br/feriados/fer_nacionais/2028.asp) [C] |

Conferência independente: as mesmas regras do `exchange_calendars` 4.13.2 (`raw/exchange-calendars-4.13.2/exchange_calendar_bvmf.py`, Apache-2.0). Lá, `AniversarioSaoPaulo` termina em 2022 e 31/12 em fim de semana passa para a sexta anterior [T].

## Regras usadas

1. Sem pregão em: feriados nacionais, Carnaval (segunda e terça), Sexta-feira Santa, Corpus Christi, 24/12 e 31/12 [C].
2. **31/12 em fim de semana:** a B3 fecha no último dia útil do ano. Exemplo: 29/12/2023, pelo [OC 151/2022-PRE](https://www.b3.com.br/data/files/1C/F2/F3/05/42535810F534EB48AC094EA8/OC%20151-2022%20PRE%20Calendario%20de%20Feriados%20em%202023%20e%20funcionamento%20da%20B3%20em%2022.02.2023%20_Quarta-Feira%20de%20Cinzas_%20_PT_.pdf) [C]. **24/12 em fim de semana:** sem compensação (2023) [C].
3. **25/01 e 09/07** (feriados de São Paulo): pregão normal desde 2022 [C].
4. **20/11** é nacional desde 2024 (Lei 14.759/2023): sem pregão [C].
5. **Quarta-feira de Cinzas:** abertura às 13h [C para 2026; S para 2027 e 2028].
6. **Dias úteis para DU/252:** calendário ANBIMA, em que 24/12 e 31/12 contam como dias úteis. Por isso o JSON traz `sem_pregao_b3` e `dia_util_anbima` em cada data.

## Datas sem pregão

| 2026 (oficial) | 2027 (derivado) | 2028 (derivado) |
|---|---|---|
| 01/01 qui Confraternização | 01/01 sex Confraternização | — (01/01 sáb) |
| 16/02 seg Carnaval | 08/02 seg Carnaval | 28/02 seg Carnaval |
| 17/02 ter Carnaval | 09/02 ter Carnaval | 29/02 ter Carnaval |
| 03/04 sex Sexta-feira Santa | 26/03 sex Sexta-feira Santa | 14/04 sex Sexta-feira Santa |
| 21/04 ter Tiradentes | 21/04 qua Tiradentes | 21/04 sex Tiradentes |
| 01/05 sex Trabalho | — (01/05 sáb) | 01/05 seg Trabalho |
| 04/06 qui Corpus Christi | 27/05 qui Corpus Christi | 15/06 qui Corpus Christi |
| 07/09 seg Independência | 07/09 ter Independência | 07/09 qui Independência |
| 12/10 seg Aparecida | 12/10 ter Aparecida | 12/10 qui Aparecida |
| 02/11 seg Finados | 02/11 ter Finados | 02/11 qui Finados |
| — (15/11 dom) | 15/11 seg Proclamação | 15/11 qua Proclamação |
| 20/11 sex Consciência Negra | — (20/11 sáb) | 20/11 seg Consciência Negra |
| 24/12 qui (dia útil ANBIMA) | 24/12 sex (dia útil ANBIMA) | — (24/12 dom) |
| 25/12 sex Natal | — (25/12 sáb) | 25/12 seg Natal |
| 31/12 qui (dia útil ANBIMA) | 31/12 sex (dia útil ANBIMA) | **29/12 sex** (31/12 dom; dia útil ANBIMA) |
| **247 sessões; 249 DU ANBIMA** | **249 sessões; 251 DU ANBIMA** | **247 sessões; 248 DU ANBIMA** |

**Horário especial (Cinzas):** 18/02/2026, 10/02/2027 e 01/03/2028.

## Limitações

- 2027 e 2028 podem mudar: novo feriado nacional, erratas ou feriado extraordinário. Refazer quando a B3 publicar.
- A errata de 2026 (OC 041/2026) não foi lida. Pelo título, corrige o calendário de 2026. A notícia de 09/01/2026 confere com a lista acima.
- Os feriados dos EUA não fecham a B3 (só câmbio, CSD2 e agro). Não entram no JSON.
