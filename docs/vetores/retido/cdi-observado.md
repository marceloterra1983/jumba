# CDI do período: hipóteses para dois números observados (RETIDO)

- **Data:** 2026-11-04. Gerado por `../geradores/analisar_cdi_observado.py` (`python3 -I`).
- **Status: retido.** Os dois números foram lidos numa tela de produto de terceiros. Em 04/11, às 23h14, o coordenador suspendeu o uso de números lidos nessas telas em testes do motor, por causa dos termos de uso do site. **Não copie estes números para testes nem para o código** até o Marcelo decidir. O motor usa só convenções públicas (`../agregados.json`, caso `taxas_cdi`).
- **Fonte:** leitura do Marcelo (sem URL; tela logada). Nenhum acesso novo foi feito para esta análise.
- **Suposição [S]:** a leitura foi em 04/11/2026; os prazos batem com os vencimentos de 13/11/2026 (semanal, 9 dias corridos, 7 úteis) e 19/11/2026 (mensal de novembro, antecipado porque 20/11 é feriado; 15 corridos, 11 úteis).

## Resultado

- **Venda coberta, 0,3413 %:** 1 combinação(ões) fecham de 162 testadas.
  - LIN360_DC, CDI_13_65, prazo D0_leitura->vencimento (9 DC, 7 DU): 0,341250 % → half-up 0,3413, half-even 0,3412.
  - O valor exato é 0,34125 %. Só vira 0,3413 com arredondamento *half-up* (com *half-even* daria 0,3412).
- **Cash put, 0,5656 %: nenhuma hipótese fechou** (162 combinações de taxa, forma e prazo, com dias inteiros).
- **Os dois com os mesmos parâmetros:** nenhuma combinação.

## O que foi testado

- **Taxas:** CDI 13,65 % a.a. (a que fechou a venda coberta) e Selic meta 13,75 % a.a.
- **Formas:** linear 360 e 365 sobre dias corridos; linear 252 sobre dias úteis; exponencial 252 (DU), 360 e 365 (DC); capitalização diária 360 e 365; desconto linear 360.
- **Prazos ("dias até a liquidação"):** início na leitura (D0), na liquidação do prêmio (D+1) ou da ação (D+2); fim no vencimento, em venc+1 ou venc+2 sessões. Calendário B3 (20/11 sem pregão).
- **Arredondamento:** 4 casas em %, *half-up* e *half-even*.

## As mais próximas do cash put

| Forma | Taxa | Prazo | DC | DU | Valor (%) | Diferença (p.p.) |
|---|---|---|---|---|---|---|
| DESCONTO_LIN360_DC | CDI_13_65 | D0_leitura->vencimento | 15 | 11 | 0,565534 | -0,000066 |
| LIN365_DC | SELIC_META_13_75 | D0_leitura->vencimento | 15 | 11 | 0,565068 | -0,000532 |
| COMP_DIARIA_365_DC | SELIC_META_13_75 | D0_leitura->vencimento | 15 | 11 | 0,566561 | +0,000961 |
| EXP252_DU | SELIC_META_13_75 | D0_leitura->vencimento | 15 | 11 | 0,563950 | -0,001650 |
| EXP252_DU | SELIC_META_13_75 | D1_liq_premio->venc_D1 | 18 | 11 | 0,563950 | -0,001650 |
| EXP252_DU | SELIC_META_13_75 | D2_liq_acao->venc_D2 | 18 | 11 | 0,563950 | -0,001650 |
| LIN360_DC | CDI_13_65 | D0_leitura->vencimento | 15 | 11 | 0,568750 | +0,003150 |
| COMP_DIARIA_365_DC | CDI_13_65 | D0_leitura->vencimento | 15 | 11 | 0,562430 | -0,003170 |

## Hipóteses com parâmetro livre (fecham, mas não dá para confirmar)

**Outra taxa.** Taxa anual que daria exatamente 0,5656 % em 15 DC / 11 DU:

- LIN360_DC: 13,5744 % a.a.
- LIN365_DC: 13,7629 % a.a.
- LIN252_DU: 12,9574 % a.a.
- EXP252_DU: 13,7928 % a.a.
- EXP360_DC: 14,4951 % a.a.
- EXP365_DC: 14,7105 % a.a.

Nenhuma é uma taxa "redonda" nem igual à que fechou a venda coberta. A de EXP252_DU (cerca de 13,79 %) só valeria se a curva DI no vértice de 11 DU estivesse acima do CDI; dá para conferir no arquivo TS da B3 de 04/11/2026.

**Prazo fracionário.** Com 13,65 %, fecharia com 14,9169 dias corridos na forma linear 360 (15 dias menos cerca de 2,0 horas; a janela de arredondamento tem uns 4 minutos) ou com 11,1079 DU na exponencial 252. Isso exigiria contar horas até o horário de corte do vencimento; na venda coberta, porém, o prazo inteiro de 9 dias fechou.

**Capital da garantia.** Se a tela aplicasse o CDI do período sobre outra base de capital, a relação prêmio/strike (P/K) teria de ser:

| Base do CDI | CDI do período (%) | P/K se exibido = base·(K−P)/K | P/K se exibido = base·K/(K−P) |
|---|---|---|---|
| LIN360_DC | 0,568750 | 0,5538 % | impossível (negativo) |
| LIN365_DC | 0,560959 | impossível (negativo) | 0,8206 % |
| EXP252_DU | 0,560089 | impossível (negativo) | 0,9743 % |

Coerente com a venda coberta (forma LIN360_DC), só a variante base·(K−P)/K fecha, e pede P/K = 0,5538 %. Com o strike e o prêmio da put da leitura, isso se testa na hora.

## Dados que decidiriam

1. Strike e prêmio da put no momento da leitura (testa as hipóteses de P/K).
2. Horário da leitura (testa o prazo fracionário).
3. Uma segunda leitura do cash put em outro dia ou outro vencimento (separa taxa de prazo).
4. O arquivo TS (curva PRE) da B3 de 04/11/2026 (testa a taxa da curva no vértice).

Todos os números estão em `cdi-observado.json`.
