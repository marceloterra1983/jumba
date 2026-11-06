# Find Your Trade (FYT): página de produto

- **URL:** https://jumba.com.br/jumba-fyt
- **Acesso:** 2026-11-04, via WebFetch, sem login
- **Bruto:** `raw/jumba-fyt.txt`

## Resumo
Scanner de estruturas de opções que acompanha preços "em TEMPO REAL", com filtros, alertas pelo Telegram, painel de alertas, monitor de rolagens e curva de volatilidade implícita. Cobre 9 ativos.

## Telas e funcionalidades citadas
- **Filtros e alertas:** "Filtre os parâmetros, cadastre alertas de suas estruturas favoritas". Quando o preço desejado é atingido, um bot do Telegram avisa.
- **Painel:** "Monitore os seus alertas criados e disparados por meio de um painel".
- **Rolagens:** "Monitore as rolagens de opções do vencimento atual e do próximo".
- **Buscadores:** Venda Coberta e Box de 3 e 4 Pontas.
- **Curva de Volatilidade Implícita Ajustada.**
- **Estruturas listadas (23):**
  - Trava de Alta, Trava de Baixa e Borboleta
  - THL e THL/p (perene)
  - Short Straddle HA, Short Straddle e Short Straddle Coberto
  - Slide Estrutural e Short Strangle Coberto
  - Linha de Mannerheim
  - Ratio/Booster Vertical, Horizontal, Diagonal e Modular
  - BWB e BWB Short Put
  - Módulo de Atlas
  - Fence, Seagull e Collar
  - Box de 3 Pontas e Venda Coberta de Call
- **Payoff:** esta página não cita. No Telegram (mensagem 1812) aparece um "Payoff de Estruturas" em beta dentro do FYT, que mostra:
  - snapshot do book;
  - mínimo, máximo e Flip do Market Gamma;
  - BGT;
  - Max Pain;
  - vol e skew por vencimento;
  - "Preço Jumba", o preço teórico pela curva de vol;
  - impacto do spread de entrada e saída.

## Fórmulas e definições
A página não traz fórmulas e não diz se usa bid, ask ou último. Pelo Telegram (1721 e 1722), a rolagem mostra **valor negativo para crédito**, e a melhor rolagem fica nos strikes ATM.

## Dados e fontes mencionados
- Ativos: ABEV3, B3SA3, BBAS3, BBDC4, BOVA11, ITUB4, PETR4, PRIO3 e VALE3.
- Fonte dos preços: não informada.

## Horários de atualização
"TEMPO REAL", sem informar a latência.

## Preços (2026-11-04)
| Plano | Preço | Combo com o Pro |
|---|---|---|
| Mensal | R$ 197 | + R$ 200/mês |
| Semestral | R$ 997 | + R$ 166,67/mês |
| Anual | R$ 1.777 | + R$ 139,17/mês |
