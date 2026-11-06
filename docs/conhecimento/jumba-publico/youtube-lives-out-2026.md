# Lives do canal (YouTube público): conteúdo de ensino

- **Fonte:** legenda automática baixada com yt-dlp no dev em 2026-11-06 (arquivos em `~/jumba-lives` no dev). A legenda troca a palavra "put" por "[__]".
- **Live 05/11/2026:** sem legenda no YouTube; transcrita pelo áudio com Whisper large-v3-turbo no dev.

## Live 29/10/2026 (6gsJ3AS5wfU), "Mercado cai 15%!", 1:02:08. Tema: collar
1. ~2–3 min: antes da queda, hedge forte: muita put, PCR alto, skew inclinado para puts (proteção cara).
2. ~3 min: crashes vêm em ondas (queda, alívio, nova queda).
3. ~4–5 min: índice em gamma negativo explica quedas aceleradas de 1,5–2%.
4. ~5–6 min: paredões de put por strike (ex.: 170 mil), filtrados no vencimento atual. Se as posições forem realizadas, a barreira some.
5. ~6–7 min: gamma total = soma por strike. "Score" = desvios-padrão em relação à média de 1 ano; estava perto de −2σ.
6. ~8 min: strike de gamma mínimo (161) como alvo de queda (índice em ~166).
7. ~10 min: espiral: compra de put empurra o gamma para baixo e o MM vende o papel junto.
8. ~11–17 min: gestão: não vender descoberto em gamma negativo; se vender, tamanho pequeno, aguentar 20–40% contra. Margem do simulador B3 é foto do momento e pode multiplicar 10–20x no estresse.
9. ~17–21 min: collar = venda coberta + put comprada; ganho e perda máximos definidos.
10. ~21–24 min: montagem: (a) definir risco aceito; (b) risco zero = put no preço pago pelo papel; (c) vender a call cujo prêmio paga a put.
11. ~24–25 min: BOVA no meio da série deu <1% (pouco prazo, vol baixa).
12. ~26–30 min: PETR4 série seguinte: papel 52,23, put 52,41 a 2,07, call 53,91; risco zero ~1,5%. Quanto maior a vol, melhor a taxa.
13. ~32–34 min: put em 51,91: perda máx. R$200 (~0,4%), ganho ~3,4%.
14. ~42–48 min: VALE3 60,69: put 60,70 a 2,17, call 62,70: ~3,35% sem risco; put 60,20: risco 0,7%, ganho ~4,2%.
15. ~40–41 min: entrada técnica: collar de alta em suporte ou após queda forte, não no topo.
16. ~53–55 min: collar de baixa; vencimentos longos se houver liquidez; ajustes: put longa e rolagem da call.

Telas citadas: grade com preço por horário (estudar com o preço das 15h), payoff de estruturas com strikes arrastáveis, curva de vol, BSM; posição dos MMs, gamma e paredões; TradingView com zonas de ganho/perda, ±1σ e break-even.

## Live 22/10/2026 (wcXSxacgojA), "A última oportunidade antes do 2º turno?", 1:12:34. Tema: comprar alta sem sofrer com a queda de vol
1. ~2–3 min: após o 1º turno, procura por proteção (tela de estruturas montadas).
2. ~3–5 min: smile de BBAS3 quase simétrico no 1º turno, inclinado para puts no 2º. Histórico de vol ATM: BBAS 53→72%; BOVA ~40 contra ~16 normal.
3. ~5–7 min: vol implícita precifica a incerteza do evento e cai depois dele.
4. ~10–11 min: a implícita sobe com o mercado lateral enquanto a realizada cai.
5. ~12–21 min: call seca BOVA 207 nov no payoff (branca = hoje, amarela = vencimento, choque de vol): papel +R$2 com vol estável = +R$1.140; vol −5 pts = −R$70; com vol normal, precisa subir ~R$9.
6. ~21–22 min: call seca = comprado em vega; o ativo tem de andar mais que a vol cai.
7. ~23–28 min: trava de alta 207/214: 2.700 contra 7.500 da seca, ~3x a mão, melhora com vol caindo. Ganho máx. R$7/trava.
8. ~29–30 min: condor de ferro ganha com queda de vol, ruim se espera explosão.
9. ~30–41 min: borboleta com asa ~5% do preço; na semanal pós-evento amadurece mais rápido.
10. ~35–36 min: em evento muito grande, dor máxima, gamma e barreiras deixam de valer.
11. ~41–43 min: broken wing: custo zero, mas descoberta para a alta.
12. ~45–48 min: BBAS: subiu 15% e devolveu; máxima do gamma em 27 = teto e topo da trava.
13. ~49–51 min: gráfico com break-even (25,73), ±1σ e zonas até o vencimento (19/11).
14. ~51–55 min: seagull: trava 25/27 paga por put vendida 17,79 em fundo gráfico de papel que aceitaria ter. Custo ~700 → R$36 para ganho ~960; put só entra com −25%. Margem de put vendida.
15. ~55–63 min: call em dezembro vira THL/diagonal; ideal: vol da série vendida cair mais que a da comprada. Preço no payoff: ask para comprar, bid para vender, ou preço teórico pela curva.
16. ~67–71 min: borboleta com lucro: zerar parte e reduzir risco; se corre para a asa, vira prejuízo.

## Lições para o roteiro próprio
1. Regime: gamma total, score em σ de 1 ano, strikes de gamma mín./máx. como alvo e teto, paredões por vencimento e se estão sendo desfeitos.
2. Vol: implícita contra o histórico do ativo, skew, evento antes do vencimento.
3. Vol alta antes de evento: não comprar seco (trava, seagull). Gamma negativo: não vender descoberto.
4. Perda máxima definida antes; ela fixa o strike da put, e o prêmio fixa a call.
5. Vencimento: começo de série, ou semanal pós-evento para borboleta; liquidez nos dois.
6. Avaliar em % do capital contra o CDI; conferir break-even e ±1σ.
7. Estudar com preço intradiário, não com o de fechamento; bid/ask é o pior caso.

## Live 05/11/2026 (WgdeaWbWP9M), "Bolsa Sem Gatilho?", ~50:54. Tema: barreiras e mercado lateral
- ~1–5: tese de lateralidade: estrangeiro saiu ~12 bi após o 2º turno e estabilizou; menos volume segura nível.
- ~5–8: scanner de barreiras ordenado por distância. Critério: calls descobertas ≥5 mi e IQ ≥1,2. Estudo deles: segura em 96% dos casos; quando rompe, 90% não passa de 4% além. Ex.: BBAS3 dez 17,95, IQ 3,3, 8% acima do spot 16,48.
- ~8–10: dor máxima no mesmo strike = confluência. Dor máxima só atrai perto do vencimento; barreira não atrai.
- ~9–11: IQ >10 em opção muito barata é distorção (ex.: BOVA K250 IQ 45). Barreiras mudam de um dia para outro: checar todo dia.
- ~12–14: snapshot do book à tarde para estudar à noite.
- ~16–18: lançamento coberto na barreira ou logo acima.
- ~18–22: calendário: vende a barreira de dez a 0,38 e compra jan (teórico 0,55).
- ~22–27: diagonal custo zero comprando 1,2x de jan mais OTM (18,95): colchão ~6% acima da barreira.
- ~31–33: borboleta ou broken wing custo zero centrada na barreira. Fluxo estrangeiro é o que rompe barreira.
- ~33–35: trava de alta terminando na barreira; se a barreira sumir, gerir.
- ~41–45: barreira coincide com S/R do gráfico, junto com dor máxima e gamma.

## Outras lives de ensino (legenda automática)
**18/09 – Trava calendário (~55 min):** estudar com snapshot do book, nunca último negócio (último dava R$1.380, custo real R$440); breakevens em ±1σ; IV rank 99 favorece calendário; alinhar breakevens com gamma, dor máxima, barreiras e S/R; na prática captura-se ~metade do lucro máximo; trade real BOVA I188 vendida 1,57 / out 192 comprada 4,40, custo R$2.830, +15–16% em 3 pregões.
**25/09 – Borboleta (~68 min):** conversão IBOV→BOVA ÷ ~1017–1020; borboleta 195/205/215 custo R$1.130, máx. ~R$8.870; vol BOVA 29,9 com IV rank 96,7 (normal 15–17): esperar queda; borboleta é vendida em vol; comparação com trava; gestão com outra borboleta/broken wing; condor.
**16/10 – Vendeu call e o mercado subiu (~80 min):** rolagem simples rende 2–2,5% do strike; borboleta de ações custo zero; backtest BBDC 2025: gatilho 1 semana antes do vencimento com call ≥5% ITM; rolagem 2,3% contra borboleta 6,7%; com 10–15% ITM a borboleta não fecha; call descoberta se trava com ação, LEAP ou sintético; vencimentos longos mais líquidos em jun/jul, dez/jan e mar.
**09/10 – Mercado +8% (~60 min):** fluxo estrangeiro sai em D+2; queda de vol pós-evento; comprar BOVA só com vol 12–14%; borboleta 195/205/215 fez ~+300%; preço teórico e skew; venda de straddle com asas de dez compradas; direcional depois da queda de vol.
**30/04 – Entrevista com formador de mercado (~84 min):** conceitual: spread em pontos de vol, gamma do dia contra theta, hedge com futuro por financeiro, margem B3 em vol alta.

## Regras práticas acrescentadas
1. Barreira: calls descobertas ≥5 mi, IQ ≥1,2, descartar IQ >10 em opção muito barata; checar todo dia.
2. Confluência: barreira, dor máxima, gamma e S/R no mesmo strike.
3. IV rank alto: estrutura vendida em vol (borboleta, calendário). IV baixa: compra. Entrar depois do evento.
4. Preço sempre pelo book (bid/ask), nunca último negócio.
5. Breakeven em ±1σ da vol implícita.
6. Call vendida: gatilho 1 semana antes com ≥5% ITM, borboleta em vez de rolagem.
7. Alvo: ~metade do lucro máximo do payoff.
