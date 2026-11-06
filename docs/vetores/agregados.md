# Vetores de teste: agregados, exposições, níveis e estruturas

- **Data:** 2026-11-04 (data de acesso de todas as fontes citadas; nenhuma página nova foi aberta para gerar estes vetores).
- **Pasta:** `/mnt/project-files/jumba/vetores/`. Arquivos: `agregados.json` (todos os números, precisão total), este `agregados.md` (resumo legível) e `geradores/gerar_agregados.py`.
- **Como regenerar:** `python3 -I geradores/gerar_agregados.py` (só biblioteca padrão). O gerador lê, só para conferência, o JSON de feriados de `../conhecimento/b3-outros/`.
- **Dados:** todos **sintéticos**. Objeto inventado SINT3, S = 30,00, data-base 04/11/2026. Nenhum número vem de tela de terceiros.
- **Legenda:** [C] confirmado em fonte; [I] inferência; [S] suposição a testar; [P] proposta de convenção (decisão do Marcelo).
- **Tolerância sugerida nos testes:** igualdade (ou 1e-12) para Max Pain, PCR, IQ, quebra do OI, payoff e contagem de dias úteis; relativa 1e-9 para tudo que passa por N(x) (gregas, GEX, DEX, flip, preços BS). Isso exige N(x) com precisão de máquina (por exemplo, via `erfc`), não a aproximação polinomial de 7 casas.
- **Metodologia:** as fórmulas vêm das notas `../conhecimento/metodologia/` (01, 05, 08 a 14 e `especificacao-motor.md`) e `../conhecimento/b3-outros/` (curva, feriados e vencimentos). Cada caso do JSON aponta a nota e as URLs de origem.

## Estrutura do JSON

`casos.<nome>` tem sempre `descricao`, `nota_metodologica`, `fontes` (URLs), `convencoes`, `saidas` e, quando houve conferência independente, `verificacao`. O bloco `casos.cadeia` traz a cadeia sintética usada pelos casos 1 a 8.

## Resumo dos casos

| # | Caso | O que testa | Resultado-chave | Conferência independente |
|---|---|---|---|---|
| 1 | `max_pain` | Max Pain A (intrínseco) e B (contagem ITM), 10 strikes; empate | A = 30, B = 31 (divergem de propósito) | condição de 1ª ordem e grade fina |
| 2 | `pcr` | PCR por OI, volume, financeiro, descoberto e delta; V1, V2 e TODOS; sem calls | V1 OI 0,8433, vol 0,6902 | TODOS = razão de somas |
| 3 | `iq` | IQ por série e agregado (3 formas), global, barreiras | V1 calls 2,2135, puts 1,0470 | — |
| 4 | `quebra_oi` | Total = Coberto + Travado + Descoberto; bordas | identidade fecha em todas as séries do V1 | — |
| 5 | `gex_dex` | GEX (3 unidades) e DEX por série, strike, acumulado e total; sinais A, B e D | GEX V1 (A) = R$ 9.877,40 por 1 % | Γ, Δ e Θ por diferenças finitas; vetor da nota 05 |
| 6 | `gamma_flip` | Flip por varredura (M1) e por acumulado (M2) | V1: M1 29,7644; M2 32,9919 | Brent × bissecção |
| 7 | `walls` | Call e put wall por 3 regras e 2 lados | regra a: call 31, put 29 | — |
| 8 | `equilibrio_gamma_theta` | √(2|Θ|/Γ) isolado e agregado (hipótese do BGT) | r = 0: 1,889822 = Sσ/√252 | vetor da nota 13 |
| 9 | `payoff` | 8 estruturas: breakevens, máximos, ilimitado, zero em intervalo | ver tabela | resíduo nos breakevens e trocas de sinal |
| 10 | `taxas_cdi` | Venda coberta, cash put, box 3, box 4, long collar contra o CDI | box 3: 75,54 % do CDI | vetor da nota 14 |
| 11 | `dias_uteis` | DU B3 e ANBIMA, duas regras de borda, vencimentos | 2026: 247 pregões, 249 DU ANBIMA | JSON de feriados do projeto e tabela de vencimentos |
| 12 | `curva_di` | Flat forward 252, extrapolação, PU do DI1 | DU 11: 10,696619 % a.a. | interpolação de ln(fator) e forward constante |

Todas as 11 conferências independentes passaram (`conferencias` no topo do JSON; detalhes em `verificacao` de cada caso).

## Convenções que precisei escolher [P]

- **Prazo das opções:** T = DU/252, com DU pelo calendário de **pregões da B3**, excluindo a data-base e incluindo o vencimento. A curva DI usa o calendário **ANBIMA** (24/12 e 31/12 contam como úteis). Para buscar a taxa da curva no vencimento de uma opção, conte o DU ANBIMA até a data do vencimento; para o T da opção, conte o DU B3. Em novembro os dois coincidem.
- **Taxa:** DI sintético de 10,65 % a.a. (base 252) em todos os casos, igual às notas 05 e 14, para os vetores se conferirem entre si. r = ln(1 + DI).
- **Modelo:** BS sem dividendos (b = r), convenção B3 para ações protegidas.
- **Sinal da GEX/DEX:** padrão **A** (formador comprado em calls, +1; vendido em puts, −1). Também gerei B (−1 em tudo) e D (heurística coberto/descoberto, θc = 1, θb = 0, θu = 1, sem fonte). Leitura: GEX > 0 amortece; GEX < 0 acelera.
- **Unidade da GEX:** U3 = s·Γ·OI·m·S²·0,01 (R$ de delta por movimento de 1 %). U1 e U2 também vão no JSON. DEX em R$ = s·Δ·OI·m·S; hedge do formador = −DEX.
- **Flip:** principal = raiz de G(X) mais próxima de S (M1, sticky strike, grade 0,70·S a 1,30·S com passo de 0,25 %). M2 interpola o acumulado por strike, somado do menor strike para o maior. Os dois **não** são equivalentes e o vetor mostra isso.
- **Walls:** padrão regra a (maior gamma nocional por tipo), lado livre; desempate pelo strike mais próximo de S.
- **Max Pain:** só nos strikes listados; ATM não conta como ITM; empate → strike mais próximo de S, depois o menor.
- **PCR TODOS e IQ agregado:** razão de somas (não média de razões). Denominador zero → `null` com flag.
- **IQ:** séries sem lançador ficam fora do agregado (flag `SEM_LANCADOR`). Barreiras com limiar escalado para a cadeia sintética (5.000, não 5 milhões).
- **Quebra do OI:** nas puts sintéticas o coberto é 0. Se a soma não fechar, não corrigir: marcar `SOMA_DIVERGE`. Falta testar no arquivo real se o total certo é `OpnIntrst` ou `TtlPos`.
- **Movimento gamma-theta:** Θ por DU (Θ/252), horizonte de 1 DU; nome próprio (a sigla BGT é hipótese). Com sinal A o Γ total encolhe perto do flip e o movimento explode; o agregado "tudo comprado" é o mais estável.
- **Payoff:** por unidade (salvo a venda coberta em lote de 100), sem custos; intervalo de payoff zero vai em `intervalos_zero`, não em breakevens; ganho ou perda ilimitados viram `null` com flag.
- **Taxas contra o CDI:** preço executável (compra no ask, venda no bid). Livro sintético = preço BS ± R$ 0,01, arredondado para fora; o box 4 usa preços à mão, porque com esse livro a soma dos spreads passa do valor do box (há um caso de borda mostrando a taxa negativa). CDI do período padrão = (1 + DI)^(DU/252) − 1; também calculo LIN360_DC, LIN365_DC e EXP365_DC. Cash put com capital K − P (padrão) e K (alternativa); o "total" aplica o CDI sobre todo o caixa. Liquidação D+1/D+2 ignorada.
- **Curva DI:** antes do 1º vértice vale a taxa do 1º vértice (CDI); depois do último, flat forward com o penúltimo e o último (Manual de Curvas da B3). Vencimento do DI1 = 1ª sessão do mês; DU do DI1 = data-base inclusive até o vencimento exclusive.

## 0. Cadeia sintética (entrada dos casos 1 a 8)

S = 30,00; DI = 10,65 % a.a.; r = 0,101202; V1 vence em 2026-11-19 (11 DU, 15 DC; a 3ª sexta, 20/11, é feriado); V2 vence em 2026-12-18 (31 DU, 44 DC).

**V1**

| Tipo | K | σ | OI | Coberto | Travado | Descoberto | Titulares | Lançadores | Qtd dia | Preço médio |
|---|---|---|---|---|---|---|---|---|---|---|
| C | 26 | 42,0 % | 500 | 300 | 50 | 150 | 40 | 30 | 100 | 4,16 |
| C | 27 | 40,0 % | 800 | 500 | 100 | 200 | 60 | 40 | 200 | 3,22 |
| C | 28 | 38,0 % | 2.000 | 1.200 | 300 | 500 | 150 | 90 | 600 | 2,34 |
| C | 29 | 36,5 % | 4.000 | 2.400 | 600 | 1.000 | 300 | 160 | 1.500 | 1,57 |
| C | 30 | 35,0 % | 4.000 | 2.200 | 700 | 1.100 | 420 | 230 | 3.000 | 0,94 |
| C | 31 | 34,5 % | 16.000 | 7.000 | 2.000 | 7.000 | 900 | 420 | 5.000 | 0,51 |
| C | 32 | 34,5 % | 18.000 | 9.000 | 2.000 | 7.000 | 1.300 | 650 | 6.000 | 0,25 |
| C | 33 | 35,0 % | 20.000 | 13.000 | 3.000 | 4.000 | 1.700 | 800 | 4.000 | 0,12 |
| C | 34 | 36,0 % | 8.000 | 5.000 | 1.000 | 2.000 | 600 | 300 | 1.000 | 0,05 |
| C | 35 | 37,0 % | 25.000 | 18.000 | 2.000 | 5.000 | 2.100 | 700 | 2.000 | 0,03 |
| P | 26 | 42,0 % | 22.000 | 0 | 6.000 | 16.000 | 900 | 1.100 | 3.000 | 0,05 |
| P | 27 | 40,0 % | 9.000 | 0 | 3.000 | 6.000 | 500 | 450 | 1.500 | 0,10 |
| P | 28 | 38,0 % | 18.000 | 0 | 5.000 | 13.000 | 800 | 750 | 4.000 | 0,22 |
| P | 29 | 36,5 % | 14.000 | 0 | 4.000 | 10.000 | 700 | 520 | 3.500 | 0,44 |
| P | 30 | 35,0 % | 10.000 | 0 | 3.000 | 7.000 | 520 | 400 | 2.500 | 0,81 |
| P | 31 | 34,5 % | 6.000 | 0 | 2.000 | 4.000 | 260 | 300 | 1.200 | 1,37 |
| P | 32 | 34,5 % | 2.000 | 0 | 500 | 1.500 | 120 | 110 | 300 | 2,11 |
| P | 33 | 35,0 % | 1.000 | 0 | 300 | 700 | 60 | 50 | 100 | 2,97 |
| P | 34 | 36,0 % | 600 | 0 | 100 | 500 | 40 | 45 | 50 | 3,91 |
| P | 35 | 37,0 % | 300 | 0 | 100 | 200 | 20 | 0 | 0 | 4,87 |

**V2**

| Tipo | K | σ | OI | Coberto | Travado | Descoberto | Titulares | Lançadores | Qtd dia | Preço médio |
|---|---|---|---|---|---|---|---|---|---|---|
| C | 28 | 37,0 % | 3.000 | 2.000 | 500 | 500 | 200 | 150 | 500 | 2,95 |
| C | 29 | 36,0 % | 5.000 | 3.000 | 500 | 1.500 | 330 | 200 | 800 | 2,25 |
| C | 30 | 35,0 % | 7.000 | 4.000 | 1.000 | 2.000 | 500 | 260 | 1.200 | 1,65 |
| C | 31 | 34,5 % | 9.000 | 6.000 | 1.000 | 2.000 | 640 | 300 | 900 | 1,17 |
| C | 32 | 34,5 % | 6.000 | 4.000 | 500 | 1.500 | 420 | 200 | 400 | 0,82 |
| P | 28 | 37,0 % | 8.000 | 0 | 2.000 | 6.000 | 420 | 460 | 900 | 0,60 |
| P | 29 | 36,0 % | 7.000 | 0 | 2.000 | 5.000 | 380 | 360 | 700 | 0,89 |
| P | 30 | 35,0 % | 5.000 | 0 | 1.500 | 3.500 | 300 | 240 | 600 | 1,28 |
| P | 31 | 34,5 % | 2.000 | 0 | 500 | 1.500 | 130 | 100 | 200 | 1,79 |
| P | 32 | 34,5 % | 1.000 | 0 | 200 | 800 | 70 | 60 | 100 | 2,42 |

## 1. Max Pain (V1)

Fonte: /mnt/project-files/jumba/conhecimento/metodologia/10-max-pain.md; https://optionalpha.com/learn/max-pain-options (acesso 2026-11-04).

| X | Dor (R$) | ITM (contratos) | Dor'₋ | Dor'₊ |
|---|---|---|---|---|
| 26 | 183.500 | 60.900 | -82.900 | -60.400 |
| 27 | 123.100 | 52.400 | -60.400 | -50.600 |
| 28 | 72.500 | 35.200 | -50.600 | -30.600 |
| 29 | 41.900 | 23.200 | -30.600 | -12.600 |
| 30 | 29.300 | 17.200 | -12.600 | 1.400 |
| 31 | 30.700 | 15.200 | 1.400 | 23.400 |
| 32 | 54.100 | 29.200 | 23.400 | 43.400 |
| 33 | 97.500 | 46.200 | 43.400 | 64.400 |
| 34 | 161.900 | 65.600 | 64.400 | 73.000 |
| 35 | 234.900 | 73.300 | 73.000 | 98.300 |

- **Método A = 30**, **método B = 31**. Divergem porque o OI de calls em 30 (4.000) é menor que o de puts em 31 (6.000): B anda para 31, mas o acumulado de calls até 30 (11.300) já passa o de puts acima de 30 (9.900), e A fica em 30.
- **Empate no B:** com S = 31,8, os strikes 28, 30, 32 empatam com 2.000 contratos ITM; o mais próximo de S é **32**. O A dá 30.

## 2. Put/Call Ratio

Fonte: /mnt/project-files/jumba/conhecimento/metodologia/11-pcr.md; https://www.cboe.com/us/options/market_statistics/daily/ (acesso 2026-11-04).

| Recorte | OI | Volume | Financeiro | Descoberto | Delta |
|---|---|---|---|---|---|
| V1 | 0,843337 | 0,690171 | 0,611980 | 2,107335 | 0,986537 |
| V2 | 0,766667 | 0,657895 | 0,381404 | 2,240000 | 0,518703 |
| TODOS | 0,825409 | 0,685662 | 0,531086 | 2,135402 | 0,785147 |

- TODOS é Σ puts ÷ Σ calls; a média simples das razões de V1 e V2 daria outro número. Caso sem volume de calls: PCR por volume = `null` com `SEM_CALLS`; por OI = 0,50.

## 3. Índice de Qualidade (IQ)

Fonte: /mnt/project-files/jumba/conhecimento/metodologia/12-indice-qualidade.md; https://www.clubedopairico.com.br/o-indice-de-qualidade-na-venda-de-opcoes/22810 (acesso 2026-11-04). Dependência de dado: [S] titulares e lançadores viriam de BrrwrQty/LndrQty do arquivo de posições em aberto da B3; não confirmado. Os números aqui são sintéticos.

| Recorte | Tipo | Razão de somas (padrão) | Ponderado por OI | Ponderado por descoberto | Fora (sem lançador) |
|---|---|---|---|---|---|
| V1 | calls | 2,213450 | 2,276603 | 2,208123 | — |
| V1 | puts | 1,046980 | 1,067328 | 1,065984 | SINTV1P35 |
| V2 | calls | 1,882883 | 1,917051 | 1,920598 | — |
| V2 | puts | 1,065574 | 1,074344 | 1,072284 | — |
| GLOBAL | calls | 2,132450 | 2,192530 | 2,147292 | — |
| GLOBAL | puts | 1,051567 | 1,068856 | 1,067386 | SINTV1P35 |

Barreiras (descoberto ≥ 5.000, IQ ≥ 1,2, |K/S − 1| ≤ 10 %): SINTV1C31 (IQ 2,1429, 3,33 %); SINTV1C32 (IQ 2,0000, 6,67 %); SINTV1P29 (IQ 1,3462, -3,33 %); SINTV1P30 (IQ 1,3000, 0,00 %).

## 4. Total = Coberto + Travado + Descoberto

| Tipo (V1) | OI | Coberto | Travado | Descoberto | % descoberto | Fecha? |
|---|---|---|---|---|---|---|
| C | 98.300 | 58.600 | 11.750 | 27.950 | 28,43 % | sim |
| P | 82.900 | 0 | 24.000 | 58.900 | 71,05 % | sim |

- `DIVERGE1`: não corrigir; manter os campos como vieram, marcar a série e usar oi_informado como total (flags: SOMA_DIVERGE).
- `SEM_QUEBRA1`: opções sobre futuro costumam vir sem a quebra; % descoberto = null; o total vale (flags: SEM_QUEBRA).
- `VARIACAO1`: VartnOpnIntrst deve ser igual a OpnIntrst(D) − OpnIntrst(D−1); se não for, flag VARIACAO_DIVERGE (flags: nenhuma).

## 5. GEX e DEX

Fonte: /mnt/project-files/jumba/conhecimento/metodologia/08-gex-dex.md; https://squeezemetrics.com/monitor/download/pdf/white_paper.pdf, https://spotgamma.com/gamma-exposure-gex/, https://threadreaderapp.com/thread/1489373524066279430.html (acesso 2026-11-04).

**Convenção de sinal explícita:** A (padrão): calls +1, puts −1. B: −1 em tudo. D: s = (coberto − descoberto)/OI. GEX em R$ por 1 % (U3).

| K | GEX A | Acumulado A | GEX B | GEX D | DEX A (R$) |
|---|---|---|---|---|---|
| 26 | -6.623,29 | -6.623,29 | -6.931,35 | -4.882,75 | 42.259,94 |
| 27 | -4.686,85 | -11.310,14 | -5.601,36 | -3.257,93 | 45.561,69 |
| 28 | -15.150,68 | -26.460,81 | -18.938,35 | -11.647,08 | 140.369,20 |
| 29 | -13.560,55 | -40.021,36 | -24.408,99 | -11.662,07 | 208.315,64 |
| 30 | -9.774,09 | -49.795,45 | -22.806,22 | -9.611,19 | 203.047,27 |
| 31 | 15.575,81 | -34.219,64 | -34.266,79 | -6.230,32 | 288.098,46 |
| 32 | 19.321,46 | -14.898,18 | -24.151,83 | 603,80 | 161.962,50 |
| 33 | 15.020,16 | 121,98 | -16.601,23 | 6.561,44 | 94.881,96 |
| 34 | 3.445,47 | 3.567,45 | -4.004,19 | 1.164,01 | 30.980,18 |
| 35 | 6.309,95 | 9.877,40 | -6.463,23 | 3.269,94 | 30.361,47 |

| Filtro | Sinal | GEX total (R$/1 %) | GEX total (ações/R$1) | DEX total (R$) | Hedge (R$) | DEX ATM ±2 % | DEX ATM ±5 % | Regime |
|---|---|---|---|---|---|---|---|---|
| PROXIMO_V1 | A | 9.877,40 | 1.097,4894 | 1.245.838,31 | -1.245.838,31 | 203.047,27 | 699.461,37 | POSITIVO |
| PROXIMO_V1 | B | -164.173,52 | -18.241,5017 | -8.443,49 | 8.443,49 | 73.776,97 | 54.928,52 | NEGATIVO |
| PROXIMO_V1 | D | -35.692,17 | -3.965,7966 | 574.727,93 | -574.727,93 | 114.663,15 | 309.375,22 | NEGATIVO |
| TODOS | A | 17.947,10 | 1.994,1226 | 1.965.735,80 | -1.965.735,80 | 386.926,85 | 1.209.355,18 | POSITIVO |
| TODOS | B | -211.352,70 | -23.483,6331 | -236.588,32 | 236.588,32 | 20.499,55 | -119.145,52 | NEGATIVO |
| TODOS | D | -39.396,41 | -4.377,3788 | 933.748,69 | -933.748,69 | 194.253,47 | 548.271,60 | NEGATIVO |

Conferência: erro relativo máximo do Γ contra diferenças finitas = 3,4e-07; Γ da nota 05 (S=30, K=32, DU=21) = 0,115873 (esperado 0,115873).

## 6. Gamma flip (sinal A)

| Filtro | Flip M1 | Raízes | Regime | G(S) R$/1 % | Flip M2 | X do mínimo de G | X do máximo de G |
|---|---|---|---|---|---|---|---|
| PROXIMO_V1 | 29,764366 | 1 | POSITIVO | 9.877,40 | 32,991879 | 27,000 | 33,600 |
| TODOS | 29,584187 | 1 | POSITIVO | 17.947,10 | 32,454621 | 26,850 | 33,525 |

- Sem flip: só as calls do V1 dão G(X) > 0 na grade toda → `SEM_FLIP`. Diferença máxima Brent × bissecção: 2,2e-13.
- M1 e M2 dão níveis muito diferentes (cerca de 29,8 contra 33): o M2 depende de onde a soma começa e não recalcula Γ. Esse contraste é parte do vetor.

## 7. Call wall e put wall (V1)

| Regra | Call wall (livre) | Put wall (livre) | Call wall (K ≥ S) | Put wall (K ≤ S) |
|---|---|---|---|---|
| a: gamma nocional (padrão) | 31 | 29 | 31 | 29 |
| b: maior OI | 35 | 26 | 35 | 26 |
| c: GEX com sinal (A) | 32 | 28 | 32 | 28 |

- Mini-cadeia em que o lado importa: livre → call 29, put 31; restrito → call 31, put 29.

## 8. Movimento de equilíbrio gamma-theta, √(2|Θ|/Γ)

| Caso | Γ | Θ por DU | Movimento (1 DU) | S·σ/√252 | Movimento (5 DU) |
|---|---|---|---|---|---|
| call_atm_r0 | 0,038490 | -0,068732 | 1,889822 | 1,889822 | 4,225771 |
| call_atm_r_ln1_1065 | 0,038000 | -0,088720 | 2,160880 | 1,889822 | 4,831874 |
| put_otm_V1_K28 | 0,105213 | -0,025024 | 0,689701 | 0,718132 | 1,542218 |

| Agregado V1 | Γ total | Θ total por DU | Movimento | Bandas | Flags |
|---|---|---|---|---|---|
| V1_convencao_A | 1.097,4894 | -540,4068 | 0,992374 | 29,0076 a 30,9924 | PESOS_COM_SINAIS_MISTOS |
| V1_tudo_comprado | 18.241,5017 | -4.197,4807 | 0,678389 | 29,3216 a 30,6784 | — |

## 9. Payoff de várias pernas (no vencimento)

| Estrutura | Pernas | Breakevens | Ganho máx. | Perda máx. | Fluxo na montagem | Flags |
|---|---|---|---|---|---|---|
| trava_alta_calls | +C28@2,40 −C32@0,45 | 29,95 | 2,05 | -1,95 | -1,95 | — |
| borboleta_calls | +C28@2,40 −2C30@1,05 +C32@0,45 | 28,75, 31,25 | 1,25 | -0,75 | -0,75 | — |
| condor_de_ferro_vendido | +P26@0,10 −P28@0,40 −C32@0,45 +C34@0,12 | 27,37, 32,63 | 0,63 | -1,37 | 0,63 | — |
| straddle_vendido | −C30@1,05 −P30@0,80 | 28,15, 31,85 | 1,85 | — | 1,85 | PERDA_ILIMITADA |
| ratio_calls_1x2 | +C30@1,05 −2C32@0,45 | 30,15, 33,85 | 1,85 | — | -0,15 | PERDA_ILIMITADA |
| venda_coberta_lote_100 | +100ação@30,00 −100C31@0,80 | 29,20 | 180,00 | -2.920,00 | -2.920,00 | — |
| long_collar | +ação@30,00 +P28@0,40 −C33@0,30 | 30,10 | 2,90 | -2,10 | -30,10 | — |
| trava_sem_lucro_zero_em_intervalo | +C30@2,00 −C32@0,00 | — | 0,00 | -2,00 | -2,00 | ZERO_EM_INTERVALO [32,00, ∞) |

`—` em ganho ou perda máximos = ilimitado. O JSON traz também o payoff de S_T = 20 a 40 e o valor em cada ponto de quebra.

## 10. Taxa contra o CDI

Data-base 04/11/2026, vencimento 19/11/2026: 11 DU e 15 DC; DI = 10,65 % a.a.; S bid/ask = 29,99/30,01.

CDI do período por convenção: EXP252_DU = 0,442731 %; LIN360_DC = 0,443750 %; LIN365_DC = 0,437671 %; EXP365_DC = 0,416764 %.

| Estrutura | Capital | r período | r a.a. | % CDI (razão) | % CDI (CDB) | Spread a.a. (p.p.) |
|---|---|---|---|---|---|---|
| venda_coberta_otm_K31 (parado) | 29,5100 | 1,6943 % | 46,95 % | 382,70 % | 380,55 % | 36,30 |
| venda_coberta_otm_K31 (exercida) | 29,5100 | 5,0491 % | 209,09 % | 1.140,45 % | 1.117,33 % | 198,44 |
| venda_coberta_itm_K29 (parado) | 28,4600 | 1,8974 % | 53,82 % | 428,57 % | 425,77 % | 43,17 |
| venda_coberta_itm_K29 (exercida) | 28,4600 | 1,8974 % | 53,82 % | 428,57 % | 425,77 % | 43,17 |
| cash_put_otm_K29 prêmio, capital K−P | 28,5700 | 1,5051 % | 40,81 % | 339,95 % | 338,33 % | 30,16 |
| cash_put_otm_K29 total c/ CDI, capital K−P | 28,5700 | 1,9545 % | 55,80 % | 441,46 % | 438,46 % | 45,15 |
| cash_put_otm_K29 prêmio, capital K | 29,0000 | 1,4828 % | 40,10 % | 334,91 % | 333,34 % | 29,45 |
| cash_put_itm_K31 prêmio, capital K−P | 29,6400 | 4,5884 % | 179,48 % | 1.036,38 % | 1.017,42 % | 168,83 |
| cash_put_itm_K31 total c/ CDI, capital K−P | 29,6400 | 5,0514 % | 209,24 % | 1.140,97 % | 1.117,83 % | 198,59 |
| cash_put_itm_K31 prêmio, capital K | 31,0000 | 4,3871 % | 167,41 % | 990,92 % | 973,64 % | 156,76 |
| box3_K30 | 29,9000 | 0,3344 % | 7,95 % | 75,54 % | 75,58 % | -2,70 |
| box4_K28_K32 aplicação | 3,9900 | 0,2506 % | 5,90 % | 56,61 % | 56,66 % | -4,75 |
| box4_K28_K32 captação (custo) | 3,9500 | 1,2658 % | 33,40 % | 285,91 % | 284,85 % | 22,75 |
| box4 com livro sintético (borda) | 4,0400 | -0,9901 % | -20,38 % | -223,63 % | -225,10 % | -31,03 |
| long_collar_K28_K33 piso | 30,1500 | -7,1310 % | -81,64 % | -1.610,69 % | -1.668,74 % | -92,29 |
| long_collar_K28_K33 teto | 30,1500 | 9,4527 % | 691,86 % | 2.135,10 % | 2.052,64 % | 681,21 |
| long_collar_K28_K33 parado | 30,1500 | -0,4643 % | -10,11 % | -104,88 % | -105,32 % | -20,76 |

Conferência com a nota 14 (box 3, DU = 21): r = 1,5228 %, a.a. 19,89 %, % CDI 179,8 % e 179,2 % (esperado 1,5228 %, 19,89 %, 179,8 % e 179,2 %).

O JSON traz, para cada taxa, o % do CDI nas quatro convenções de CDI do período (`pct_cdi_1_por_convencao_cdi`).

## 11. Dias úteis com feriados B3

| Caso | d0 | d1 | DC | DU B3 (d0,d1] | DU B3 [d0,d1) | DU ANBIMA (d0,d1] | DU ANBIMA [d0,d1) |
|---|---|---|---|---|---|---|---|
| hoje_ate_semanal_13nov | 2026-11-04 | 2026-11-13 | 9 | 7 | 7 | 7 | 7 |
| hoje_ate_mensal_nov_19nov | 2026-11-04 | 2026-11-19 | 15 | 11 | 11 | 11 | 11 |
| hoje_ate_mensal_dez_18dez | 2026-11-04 | 2026-12-18 | 44 | 31 | 31 | 31 | 31 |
| natal_ano_novo | 2026-12-18 | 2027-01-15 | 28 | 16 | 16 | 18 | 18 |
| carnaval_2027_com_cinzas | 2027-02-05 | 2027-02-19 | 14 | 8 | 8 | 8 | 8 |
| ano_2026_inteiro | 2025-12-31 | 2026-12-31 | 365 | 247 | 247 | 249 | 249 |
| ano_2027_inteiro | 2026-12-31 | 2027-12-31 | 365 | 249 | 249 | 251 | 251 |
| ano_2028_inteiro | 2027-12-31 | 2028-12-31 | 366 | 247 | 247 | 248 | 249 |
| inicio_em_sabado | 2026-11-07 | 2026-11-13 | 6 | 5 | 4 | 5 | 4 |
| fim_em_feriado_20nov | 2026-11-13 | 2026-11-20 | 7 | 4 | 5 | 4 | 5 |
| mesmo_dia | 2026-11-04 | 2026-11-04 | 0 | 0 | 0 | 0 | 0 |
| fim_de_2028_31dez_domingo | 2028-12-22 | 2029-01-05 | 14 | 7 | 7 | 8 | 8 |

Vencimentos ajustados: acoes_mensal_2026_11 = 2026-11-19; acoes_mensal_2026_12 = 2026-12-18; acoes_mensal_2028_04 = 2028-04-20; acoes_semanal_sexta_2026_12_25 = 2026-12-23; acoes_semanal_sexta_2027_01_01 = 2026-12-30; di1_2027_01_primeira_sessao = 2027-01-04.

Conferência: os dias sem pregão e os feriados ANBIMA de 2026 a 2028 batem com `/mnt/project-files/jumba/conhecimento/b3-outros/feriados-b3-2026-2028.json` (sim); os vencimentos batem com `vencimentos-regras.md` (sim). 2027 e 2028 são calendários derivados; a errata OC 041/2026-VNC não foi lida.

## 12. Curva DI: flat forward 252

Vértices sintéticos (data-base 04/11/2026, DU ANBIMA da data-base inclusive ao vencimento exclusive):

| Vértice | Vencimento | DU | Taxa a.a. | PU |
|---|---|---|---|---|
| CDI | — | 1 | 10,650 % | — |
| DI1F27 | 2027-01-04 | 40 | 10,700 % | 98.399,40 |
| DI1G27 | 2027-02-01 | 60 | 10,750 % | 97.598,24 |
| DI1J27 | 2027-04-01 | 100 | 10,900 % | 95.977,63 |
| DI1N27 | 2027-07-01 | 163 | 11,100 % | 93.418,09 |
| DI1F28 | 2028-01-03 | 291 | 11,500 % | 88.187,86 |

| DU | Taxa a.a. | Fator | PU | Extrapolado |
|---|---|---|---|---|
| 1 | 10,650000 % | 1,0004016754 | 99.959,8486 | não |
| 5 | 10,691024 % | 1,0020173608 | 99.798,6701 | não |
| 11 | 10,696619 % | 1,0044457829 | 99.557,3895 | não |
| 21 | 10,698840 % | 1,0085062386 | 99.156,5507 | não |
| 31 | 10,699628 % | 1,0125831086 | 98.757,3258 | não |
| 40 | 10,700000 % | 1,0162663808 | 98.399,3979 | não |
| 60 | 10,750000 % | 1,0246086834 | 97.598,2359 | não |
| 63 | 10,767846 % | 1,0258962164 | 97.475,7470 | não |
| 100 | 10,900000 % | 1,0419094538 | 95.977,6300 | não |
| 126 | 11,006733 % | 1,0535973267 | 94.912,9212 | não |
| 163 | 11,100000 % | 1,0704564771 | 93.418,0905 | não |
| 252 | 11,421054 % | 1,1142105437 | 89.749,6443 | não |
| 291 | 11,500000 % | 1,1339429778 | 88.187,8560 | não |
| 300 | 11,515310 % | 1,1385460199 | 87.831,3202 | sim |
| 400 | 11,639141 % | 1,1909655095 | 83.965,4878 | sim |

Forwards entre vértices: 1–40 DU: 10,7013 %; 40–60 DU: 10,8501 %; 60–100 DU: 11,1254 %; 100–163 DU: 11,4182 %; 163–291 DU: 12,0115 %.

Conferência: diferença máxima contra a interpolação linear de ln(fator) = 2,1e-15; forward constante dentro de cada intervalo: sim.

## Números observados em tela de terceiros (retido)

A análise dos dois valores de "CDI no período" lidos em tela de terceiros (0,3413 % e 0,5656 %) está em `retido/cdi-observado.md`, separada destes vetores. Ela não entra em nenhum teste até o Marcelo decidir sobre o uso dessas telas.

Resultado em uma linha: a venda coberta fecha com DI × DC/360 (convenção pública LIN360_DC, que já está calculada nos vetores acima); o cash put **não fechou** com nenhuma das 162 combinações de taxa, forma e prazo em dias inteiros. Só fecha com um parâmetro livre (prazo fracionário, outra taxa ou outra base de capital), e isso não dá para confirmar sem o strike, o prêmio e o horário da leitura.

## Pendências

- Confirmar no arquivo real da B3 se coberto + travado + descoberto fecha com `OpnIntrst` ou com `TtlPos`, e se `BrrwrQty`/`LndrQty` são titulares e lançadores.
- Decidir as convenções [P] acima (sinal da GEX, método do flip, regra das walls, método do Max Pain, base do % do CDI, capital do cash put).
- Refazer os vetores de 2027 e 2028 quando a B3 publicar os calendários; ler a errata OC 041/2026-VNC.
- Trocar a curva sintética por um arquivo TS real da B3 quando houver um baixado, e conferir a interpolação contra a curva PRE publicada.
