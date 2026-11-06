# Verificação independente: `agregados.json` e `agregados.md`

- **Data:** 2026-11-04. Verificador cético e independente; nenhuma página web foi aberta.
- **Objeto:** `/mnt/project-files/jumba/vetores/agregados.json` (versão 1.0.0) e `agregados.md`.
- **Veredito: APROVADO COM RESSALVAS.** Nenhuma divergência numérica. As ressalvas são de convenção, de definição e de cobertura (seção 4).
- **Script próprio:** `/tmp/verifica-agregados/verifica.py`, escrito do zero, só com a biblioteca padrão e N(x) via `math.erfc`. Rodar com `python3 -I /tmp/verifica-agregados/verifica.py`. A saída completa vai para `/tmp/verifica-agregados/resultado.json`.
- **Quantificação das ressalvas:** `/tmp/verifica-agregados/convencoes.py`, com saída em `convencoes.json`.
- **O que não usei:**
  - `vetores/geradores/`: nem lido nem importado.
  - `vetores/retido/` e `conhecimento/jumba-publico/`: em quarentena, não usados como fonte.
- **Entradas que usei:** a cadeia sintética e as pernas e preços declarados no próprio JSON, o JSON de feriados `conhecimento/b3-outros/feriados-b3-2026-2028.json` e os vetores publicados nas notas `metodologia/05, 08, 10, 13, 14`.
- **Teste do verificador:** fiz uma cópia do JSON em `/tmp` e injetei 8 erros: Γ × (1 + 1e-7), flip + 1e-6, DU 18 → 17, r_aa do box 3 × 1,0001, PU + 0,01, Max Pain B, um breakeven e um IQ ponderado. O script acusou os 8, além de 3 reflexos no `.md`. A tolerância está apertada o bastante para pegar erro real.

## 1. Casos conferidos

Recalculei **todos os 12 casos**, mais a cadeia, totalizando 2.198 comparações:

- 1.811 contra o JSON;
- 353 contra números e células do `.md`;
- 34 contra âncoras publicadas.

Tolerâncias usadas:

- 1e-12 (ou igualdade) na aritmética exata;
- 1e-9 relativa no que passa por N(x);
- 1e-10 nas taxas e 1e-11 nas raízes do flip.

| # | Caso | Subcasos recalculados | Comparações | Maior dif. relativa | Resultado |
|---|---|---|---|---|---|
| 0 | `cadeia` | 30 séries; DU e DC de V1 e V2 (B3 e ANBIMA); r = ln 1,1065; descoberto = OI − coberto − travado; financeiro; tabela do `.md` × JSON | 100 | 1,4e-16 | confere |
| 1 | `max_pain` | tabela de 10 strikes (Dor, ITM, derivadas laterais); A, B, candidatos; grade fina de 0,01; caso de empate (ITM e Dor de 28 a 32) | 31 | 0 | confere |
| 2 | `pcr` | V1, V2, TODOS × OI, volume, financeiro, descoberto e delta; caso sem calls | 68 | 0 | confere |
| 3 | `iq` | 30 IQ por série e flags; V1, V2, GLOBAL × calls e puts × 3 agregações; barreiras e distâncias | 101 | 0 | confere |
| 4 | `quebra_oi` | 20 séries do V1 (campos, %, flags); somas por tipo; DIVERGE1 e VARIACAO1 | 67 | 0 | confere |
| 5 | `gex_dex` | 30 séries × 14 campos (T, preço, Δ, Γ, Θ, s_A/s_B/s_D, GEX U1/U2/U3 A/B/D, DEX); 2 filtros × 3 sinais × (por strike, acumulado, DEX por strike, totais, hedge, ATM 2 % e 5 %, regime) | 655 | 1,8e-14 | confere |
| 6 | `gamma_flip` | M1 com grade de 241 pontos e bissecção própria (raiz, intervalo, principal, G(S), regime, máximo e mínimo, 61 pontos do perfil) em 2 filtros; M2 (cruzamento e variante); SEM_FLIP | 152 | 1,2e-16 | confere |
| 7 | `walls` | gamma nocional por strike; regras a, b e c × lado livre e restrito; mini-cadeia de lado restrito | 32 | 0 | confere |
| 8 | `equilibrio_gamma_theta` | 3 opções isoladas (Γ, Θ, Θ/DU, movimento em 1 e 5 DU, referência); 2 agregados (Γ_tot, Θ_tot, bandas, σ efetiva, flags) | 37 | 4,2e-16 | confere (ver 4.1) |
| 9 | `payoff` | 8 estruturas: breakevens, intervalos de zero, máximo e mínimo, inclinações, fluxo, pontos de quebra, grade de 20 a 40 | 88 | 2,0e-16 | confere |
| 10 | `taxas_cdi` | 4 convenções de CDI; livro com 20 séries (BS ± 0,01 arredondado para fora); venda coberta OTM e ITM; cash put OTM e ITM nos dois capitais; box 3; box 4 (à mão e livro); collar; vetor da nota 14 | 287 | 2,2e-15 | confere |
| 11 | `dias_uteis` | 12 pares × DC e 4 contagens; 6 vencimentos; listas de dias sem pregão e feriados ANBIMA de 2026 a 2028; sessões por ano no JSON de feriados | 78 | 0 | confere |
| 12 | `curva_di` | 5 vértices DI1 (1ª sessão, DU ANBIMA [d0, venc), PU); 15 pontos (taxa, fator, desconto, r contínua, PU, extrapolado); 10 forwards | 115 | 1,4e-13 | confere |
| — | `.md` | as tabelas das seções 0 e 1 a 12, conferidas célula a célula ou número a número contra o meu recálculo | 353 | — | confere |

**Âncoras publicadas:**

- **Livro (Hull).** O `agregados` não cita nenhum exemplo de livro: a busca por "Hull" no `.md` e no `.json` não acha nada. Por isso usei os exemplos publicados de Hull, *Options, Futures and Other Derivatives*, só para validar o meu BS, nas casas publicadas. Os valores vêm da minha lembrança do livro: não o reabri.
  - Ex. 15.6 (S = 42, K = 40, r = 10 %, σ = 20 %, T = 0,5): c = 4,76, p = 0,81, d1 = 0,7693 e d2 = 0,6278.
  - Cap. 19 (S = 49, K = 50, r = 5 %, σ = 20 %, T = 20/52): c = 2,40, Δ = 0,522, Γ = 0,066, Θ = −4,31 por ano (−0,0118 por dia corrido), vega = 12,1 e ρ = 8,91.
  - Resultado: 11 de 11 conferem.
- **Notas do projeto citadas pelo `agregados`:**
  - nota 05: 13 valores, entre eles Γ = 0,115873 e Θ_call = −7,261986 por ano;
  - nota 08: G3 = 104.286;
  - nota 10: A = B = 30;
  - nota 13: 1,889822 e 2,160880;
  - nota 14, box 3 com DU 21: 29,55, 1,5228 %, 19,89 %, 179,8 % e 179,2 %.
  - Resultado: 23 de 23 conferem.

## 2. Divergências

**Nenhuma.** Nenhum valor do JSON nem do `.md` ficou fora da tolerância. A maior diferença relativa foi 1,4e-13, nos PU da curva, por arredondamento de ponto flutuante.

| id | esperado | recalculado | diferença relativa |
|---|---|---|---|
| — | — | — | — |

Como não achei erro real, **não criei** `correcoes-agregados.json`, e o JSON original não foi alterado.

## 3. Convenções conferidas e que estão certas

- **Unidades das gregas.**
  - Γ está em 1/R$.
  - `theta_aa` é Θ = ∂V/∂t **por ano de 252 DU**, coerente com T = DU/252. Conferi o sinal por diferença finita: −11,517812 contra −11,517812 na C30 do V1.
  - Θ/252 é o theta por DU. Θ/365 estaria errado neste projeto: daria −0,0316 em vez de −0,0457.
  - O equilíbrio usa Θ/252, coerente com isso.
- **Unidades da GEX.**
  - U1 = s·Γ·OI·m, em ações por R$ 1.
  - U3 = U1·S²·0,01, em R$ de delta por movimento de 1 %, o padrão da SpotGamma e do Perfiliev.
  - DEX = s·Δ·OI·m·S, e o hedge do formador é −DEX.
- **Sinal da GEX e da DEX.**
  - A convenção A (+1 em calls, −1 em puts) bate com a SqueezeMetrics.
  - Puts com s = −1 dão GEX < 0 e DEX > 0, como diz a nota 08.
  - O regime segue o sinal de G(S). GEX > 0 amortece, coerente com a leitura da nota 08.
- **Dias úteis.**
  - Bate com o JSON de feriados: 247, 249 e 247 sessões; 249, 251 e 248 DU ANBIMA.
  - Bordas conferidas: (d0, d1] e [d0, d1); 24/12 e 31/12 úteis só para a ANBIMA; 29/12/2028 sem pregão; vencimentos ajustados (19/11/2026, 23/12/2026, 30/12/2026, 20/04/2028).
- **Flat forward 252.**
  - A interpolação está certa e os forwards são constantes dentro de cada intervalo.
  - A extrapolação usa o penúltimo e o último vértice.
  - O PU segue o OC 055/2024, com DU da data-base inclusive ao vencimento exclusive. Os DU 40, 60, 100, 163 e 291 conferem pelo calendário ANBIMA.

## 4. Convenções questionáveis e ressalvas

Em ordem de importância. Nenhuma delas é erro de conta: todas reproduzem a especificação das notas.

1. **Movimento gamma-theta com r > 0 (caso 8, nota 13).**
   - O vetor `call_atm_r_ln1_1065` = 2,160880 usa um Θ que **inclui** o carregamento (−rKe^(−rT)N(d2)), mas **ignora** o financiamento do hedge, r(SΔ − V).
   - A própria derivação da nota 13 diz "desprezando juros". Pela EDP de BS (resíduo de 1e-15), o breakeven de uma posição delta-hedgeada autofinanciada é **Sσ/√252 = 1,889822 também com r > 0**.
   - O valor 2,16 está certo para a fórmula √(2|Θ|/Γ), mas não para a interpretação descrita, "o ganho de gamma paga o theta".
   - Sugestão: o Marcelo decide a definição e, se for o caso, inclui um vetor com Θ + r(SΔ − V).
2. **Taxa plana contra a curva.**
   - Todas as gregas e exposições usam DI plano de 10,65 %. A nota 01 §3 manda usar a taxa da curva no vértice, que daria 10,6966 % no DU 11 e 10,6996 % no DU 31.
   - Com a curva, a GEX TODOS (A) muda 1,4e-3 relativo e o preço da C30 do V1 muda 3,0e-4. As duas diferenças estão muito acima da tolerância de 1e-9.
   - O teste do motor tem de injetar r plano. Falta um vetor que ligue `curva_di` ao T e ao r das opções.
3. **DU B3 contra DU ANBIMA depois de 24/12 e 31/12.**
   - A regra do `.md` é T = DU_B3/252 e a taxa da curva pelo DU ANBIMA. Com r = ln(1 + i), o desconto vira (1 + i)^(−DU_B3/252), e não (1 + i)^(−DU_ANBIMA/252).
   - No par `natal_ano_novo` (16 contra 18 DU), o desconto difere 0,08 %.
   - O CDI do período do caso 10 usa o DU da opção. O CDI rende em 24/12 e 31/12, então nesse par seria 0,7255 % (DU ANBIMA) contra 0,6446 % (DU B3).
   - Nenhum vetor cobre isso: V1, V2 e o caso 10 são de novembro e dezembro antes do Natal, onde os dois DU coincidem.
4. **Θ/252 é derivada instantânea.**
   - Para as ATM do V1, ele difere do decaimento exato de 1 DU, V(T − 1/252) − V(T), em 2,0 % (C30) e 2,7 % (P30).
   - O rótulo da tela deve dizer qual dos dois é exibido. O nome `theta_aa` não diz a base; sugiro documentar como "por ano de 252 DU".
5. **Convenção D da GEX (θc = 1, θb = 0, θu = 1).**
   - Não tem fonte ([S] na nota 08).
   - Com ela, o regime fica NEGATIVO, ao contrário de A. Não serve como referência de teste até ser calibrada.
6. **Taxas "parado" (caso 10).**
   - A venda coberta e o collar supõem saída ao **S_ask** (30,01). Com S_bid (29,99), que é o preço executável de venda:
     - venda coberta OTM: 1,6266 % em vez de 1,6943 %;
     - collar: −0,5307 % em vez de −0,4643 %.
   - A nota 14 diz apenas "S", sem dizer qual.
   - No `.md`, a linha "cash_put_itm_K31 prêmio" (4,5884 %, 1.036 % do CDI) só se realiza se S_T ≥ 31, com S = 29,99 hoje. A taxa parada (1,1808 %, 266,7 % do CDI) está no JSON, mas falta na tabela do `.md`.
   - "% do CDI" de retornos negativos (collar piso −1.610 %) não tem leitura útil.
7. **Box 4 "à mão".** Em 3 das 4 pernas (C28, P28 e P32), o ask fica abaixo do meio BS da cadeia. Isso não afeta a aritmética, mas o livro não envolve o valor teórico.
8. **Calendário fora do JSON.**
   - O par `fim_de_2028_31dez_domingo` usa 2029-01-01 a 2029-01-05, e `ano_2026_inteiro` usa 2025-12-31. Nenhuma das duas datas está no JSON de feriados.
   - Supus 01/01/2029 feriado e 31/12/2025 sem pregão B3 e útil ANBIMA. Com isso, as contagens do vetor conferem.
   - 2027 e 2028 são derivados, e a errata OC 041/2026-VNC não foi lida.
9. **Lacunas de cobertura.** Nenhum vetor exercita:
   - as flags `SINAIS_IGUAIS`, `PERTO_DO_FLIP` e `GANHO_ILIMITADO`;
   - multiplicador m ≠ 1;
   - a borda das barreiras: o vetor usa ≥, e o critério observado é >.

## 5. Arquivos

- `/tmp/verifica-agregados/verifica.py`: recálculo e comparação.
- `/tmp/verifica-agregados/resultado.json`: 2.198 comparações e 0 falhas.
- `/tmp/verifica-agregados/convencoes.py` e `convencoes.json`: números das ressalvas.
- `/tmp/verifica-agregados/mutacao/`: teste com erros injetados.
