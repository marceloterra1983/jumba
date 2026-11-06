# Vetores de teste do motor de precificação

- **Arquivo de dados:** `precificacao.json` (nesta pasta). **Gerador:** `geradores/gera_precificacao.py`.
- **Gerado em / data de acesso das fontes:** 2026-11-04.
- **Como rodar de novo:** `python3 -I geradores/gera_precificacao.py --saida /mnt/project-files/jumba/vetores/`
  (só biblioteca padrão; não baixa nada).
- **Total:** 82 casos: 44 de preço e gregas, 29 de vol implícita (20 com solução e 9 que devem falhar), 9 de taxa na convenção B3. 29 valores publicados (Hull e Haug) conferidos.
- **Legenda:** [C] confirmado na fonte; [I] inferência minha; [P] convenção que escolhi para os vetores (o motor pode ter outra, mas aí o vetor precisa ser convertido).

## 1. Como usar

Cada caso tem `id`, `grupo`, `modelo`, `modelo_motor`, `convencao`, `entradas`, `entradas_gbs`, `saidas_esperadas`, `tolerancia`, `origem` e `nota`.

- `entradas` são os dados como o usuário os conhece (por exemplo, `DU` e `DI_aa` na convenção B3, `r_d` e `r_f` no GK).
- `entradas_gbs` já traz tudo convertido para o Black-Scholes generalizado `preco_gbs(tipo, S, K, T, r, b, σ)` da especificação do motor (`../conhecimento/metodologia/especificacao-motor.md` §2.2). No Black-76, o `S` do GBS é o `F`.
- Um teste do motor passa se, para cada campo de `saidas_esperadas`:

  `|obtido − esperado| ≤ max(abs, rel · |esperado|)`

  com `tolerancia.padrao = {abs: 1e-10, rel: 1e-10}`, salvo quando `tolerancia.por_campo` disser outra coisa (só o `sigma` de alguns casos de vol implícita).
- `origem.tipo = "publicado+calculado"` quer dizer que o caso também tem o valor do livro em `origem.publicado`. Esse valor é arredondado: ele confere com `saidas_esperadas` dentro de `origem.tolerancia_publicado` (meia unidade da última casa publicada). **O teste do motor deve usar `saidas_esperadas`, não o valor publicado.**
- Campos ausentes não se aplicam ao caso (por exemplo, não há `rho_q` no Black-76).

## 2. Convenções

### 2.1 Modelo único: Black-Scholes generalizado (custo de carregamento b)

$$d_1=\frac{\ln(S/K)+(b+\tfrac12\sigma^2)T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T$$

$$c=S e^{(b-r)T}N(d_1)-K e^{-rT}N(d_2),\qquad p=K e^{-rT}N(-d_2)-S e^{(b-r)T}N(-d_1)$$

| `modelo` | `modelo_motor` | b | Observação |
|---|---|---|---|
| BSM_MERTON com q = 0 | BS_B3 | b = r | Black-Scholes sem dividendo. É o que a B3 usa para ações, ETFs e índices [C, Manual B3 §1.1, via nota 01] |
| BSM_MERTON com q > 0 | BSM_Q | b = r − q | dividendo contínuo (índice à vista, opção não protegida) |
| BLACK76 | BLACK76 | b = 0 e S → F | prêmio pago à vista, descontado por e^{−rT} |
| GARMAN_KOHLHAGEN | GK | b = r_d − r_f | dólar à vista; na B3, r_f = cupom cambial |

Isso segue `../conhecimento/metodologia/01-convencoes-base.md` §1.

### 2.2 Tempo, taxa e cupom

- **Hull e Haug:** `T` em anos, como no livro; `r`, `q`, `r_d` e `r_f` são taxas contínuas ao ano.
- **Convenção B3 [C, Manual B3 §1.1 e §2.1, via nota 01]:** `T = DU/252`; `r = ln(1 + DI_aa)`, em que `DI_aa` é a taxa DI ao ano, base 252, capitalização exponencial. Por isso `e^{−rT} = (1 + DI)^{−DU/252}`.
- **Cupom cambial (GK na B3) [C, Manual B3 §2.1, via nota 01]:** `q = (252/DU) · ln(1 + cupom_lin_aa · DC/360)`.
- **Interpolação da curva (casos `TX-DI-INTERP-*`) [I, nota 01 §3]:** exponencial, ou seja, flat forward 252: `(1+i)^{DU/252} = (1+i₁)^{DU₁/252} · [(1+i₂)^{DU₂/252} / (1+i₁)^{DU₁/252}]^{(DU−DU₁)/(DU₂−DU₁)}`.

### 2.3 Gregas e unidades

| Campo | Definição | Unidade |
|---|---|---|
| `delta` | ∂V/∂S (∂V/∂F no Black-76) | objeto por opção |
| `gamma` | ∂²V/∂S² (∂²V/∂F² no Black-76) | 1/(unidade de S) |
| `vega` | ∂V/∂σ | por 1,00 de vol (100 p.p.) |
| `vega_pp` | vega/100 | por 1 p.p. de vol |
| `theta_ano` | Θ = ∂V/∂t = −∂V/∂T | por ano (na B3, ano de 252 DU) |
| `theta_du` | Θ/252 | por dia útil |
| `theta_dc` | Θ/365 | por dia corrido (escala do `escala()` da especificação; na convenção B3 é só Θ/365, não um theta de calendário) |
| `theta_1du_exato` (só B3) | V(T − 1/252) − V(T), com S, σ e taxas contínuas fixas | R$ em 1 DU; com DU = 1 dá intrínseco − preço |
| `rho` | ∂V/∂r. BSM: q fixo, então b = r − q anda junto com r. Black-76: F fixo, ρ = −T·V. GK: ∂V/∂r_d | por 1,00 de taxa contínua |
| `rho_pp` | rho/100 | por 1 p.p. de taxa contínua |
| `rho_q` | BSM: ∂V/∂q; GK: ∂V/∂r_f | por 1,00 |
| `rho_di_pp` (só B3) | ∂V/∂DI por 1 p.p. = rho/[100·(1+DI)], porque dr/dDI = 1/(1+DI) | por 1 p.p. da taxa DI ao ano |
| `F_paridade` (GK) | S·e^{(r−q)T} | R$/US$ |

`rho_q` só aparece nos casos BSM de Hull/Haug quando q > 0, mas aparece em todos os BSM da convenção B3 (lá ele serve para testar a função do motor mesmo com q = 0).

### 2.4 Vol implícita

- **Limites (`limite_inferior` e `limite_superior`) [C, nota 06 §2]:** call: max(0, S·e^{(b−r)T} − K·e^{−rT}) < c < S·e^{(b−r)T}; put: max(0, K·e^{−rT} − S·e^{(b−r)T}) < p < K·e^{−rT}. Os dois limites são estritos.
- **Falha [P, nota 06 §2]:** fora dos limites, `sigma = null`, `falha = true` e `flags = ["FORA_DOS_LIMITES"]`. O motor pode devolver `NaN`; o teste deve aceitar `NaN` ou `null`.
- **O limite é descontado, não o intrínseco simples.** Dois casos pegam o erro: `IV-FALHA-C-ENTRE-INTRINSECO-E-LIMITE` (acima de S − K e mesmo assim falha) e `IV-P-ABAIXO-INTRINSECO-VALIDO` (abaixo de K − S e mesmo assim tem vol europeia).
- **Preço de entrada:** `entradas.preco` é o double exato que o motor vai ler. O `sigma` esperado foi invertido em 100 dígitos sobre esse mesmo double, não sobre o preço "bonito" que o gerou (`sigma_origem`, só informativo).
- **Tolerância de `sigma`:** abs = max(1e-10, 10^⌈log₁₀(16·ε·M/vega)⌉), com ε = 2,2·10⁻¹⁶ e M = o maior dos dois termos da fórmula do preço (na call, S·e^{(b−r)T}·N(d₁) e K·e^{−rT}·N(d₂); na put, os termos com N(−d)) ou o próprio preço. Ela só sai de 1e-10 quando a vega é minúscula perto de termos grandes (casos muito dentro do dinheiro), porque aí um ulp do preço já move σ. Nos casos muito fora do dinheiro os dois termos são pequenos e a tolerância continua 1e-10: o motor precisa calcular o preço direto pela fórmula da própria opção, e não pela paridade a partir da opção dentro do dinheiro. Nesses casos vale também `tolerancia.preco_reprecificado`: o preço do motor no σ obtido tem de bater com `entradas.preco` em 1e-10.
- **Faixa de busca:** todos os σ esperados ficam entre 0,02 e 2,5, dentro do intervalo [0,001; 5] da nota 06.
- A flag `PRECO_MINIMO` (preço ≤ 2 ticks) depende do tick e da configuração; os vetores não a exigem.

## 3. Avisos

- **Proventos em opções de ações da B3:** a B3 ajusta o strike pelos proventos em dinheiro. Usar ao mesmo tempo o strike ajustado e um dividend yield q > 0 conta o provento duas vezes (`../pesquisa/critic.md`, item 8; `../conhecimento/metodologia/02-bsm-merton-proventos.md`). Por isso os casos de ação na convenção B3 usam q = 0. O caso `B3-INDICE-BSMQ-42DU` existe só para testar o BSM com q na base DU/252; o q dele é ilustrativo.
- **Americanas:** todos os vetores são europeus. Puts americanas de ações precisam de árvore ou BAW (nota 06 §7); não há vetor para isso aqui.
- **Valores publicados:** os números do Hull e do Haug foram transcritos dos livros impressos (não há URL; não baixei nada). Cada um foi conferido por recálculo: todos batem dentro de meia unidade da última casa publicada. A numeração dos exemplos é a da 9ª edição do Hull e pode mudar em outras edições [I]. Os capítulos do Haug citados são da 2ª edição [I].
- **Hull arredonda passos intermediários** (N(d₁) e N(d₂) com 4 casas). Por isso alguns valores intermediários que ele imprime (por exemplo, d₁ = 0,5444 no Example 17.1) não entram como "publicado".

## 4. Como os valores foram calculados e conferidos

1. Referência em `decimal.Decimal` com 100 dígitos: π por Machin, erf pela série de termos positivos e cauda da normal pela série assintótica de Mills para |x| > 14. O mpmath não está instalado e não instalei nada.
2. Toda grega analítica foi conferida por diferença finita central em 100 dígitos (h = 10⁻³⁰; 10⁻²² no gamma), com erro relativo < 10⁻³⁰.
3. Todo caso de preço passou na EDP Θ + ½σ²S²Γ + bSΔ − rV = 0 e na paridade c − p = S·e^{(b−r)T} − K·e^{−rT}, ambas com resíduo < 10⁻⁸⁰.
4. Black-76 sobre F = S·e^{(r−q)T} reproduz o GK (`B3-DOL-B76-EQUIV-*`, diferença < 10⁻¹⁵).
5. Uma implementação independente em double (`math.erfc`, Newton protegido por bissecção) passou em todos os casos com as tolerâncias gravadas. Maior erro relativo nas gregas: 6.2e-13. Maior erro de σ: 7.7e-10.
6. Os vetores de 6 casas das notas 03, 04 e 05 da metodologia batem com estes (21 valores conferidos).

## 5. Fontes

- J. C. Hull, Options, Futures, and Other Derivatives, 9a ed., Pearson, 2014 (livro impresso, sem URL).
- E. G. Haug, The Complete Guide to Option Pricing Formulas, 2a ed., McGraw-Hill, 2007 (livro impresso, sem URL).
- B3, Manual de Apreçamento - Opções (20/12/2023), §1.1 e §2.1: https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf (citado em /mnt/project-files/jumba/conhecimento/metodologia/01-convencoes-base.md, acesso 2026-11-04).
- Notas de metodologia usadas para as convenções (lidas em 2026-11-04): `/mnt/project-files/jumba/conhecimento/metodologia/01-convencoes-base.md`, `02-bsm-merton-proventos.md`, `03-black76-futuros.md`, `04-garman-kohlhagen-dolar.md`, `05-gregas-escalas.md`, `06-vol-implicita.md` e `especificacao-motor.md`.
- Revisão cética: `/mnt/project-files/jumba/pesquisa/critic.md` (item 8, proventos).

## 6. Casos


### 6.1 Preço e gregas

| id | modelo | entradas | preço | delta | gamma | vega | theta/ano | rho | origem |
|---|---|---|---|---|---|---|---|---|---|
| HULL-BSM-EX15.6-C | BS_B3 | S=42, K=40, T=0.5, r=0.1, q=0, sigma=0.2 | 4.7594223929 | 0.7791312909 | 0.0499626704 | 8.8134150596 | -4.5590921946 | 13.9820459134 | publicado: preco=4.76, d1=0.7693, d2=0.6278 |
| HULL-BSM-EX15.6-P | BS_B3 | S=42, K=40, T=0.5, r=0.1, q=0, sigma=0.2 | 0.8085993729 | -0.2208687091 | 0.0499626704 | 8.8134150596 | -0.7541744966 | -5.0425425767 | publicado: preco=0.81 |
| HULL-GREGAS-CAP19-C | BS_B3 | S=49, K=50, T_expr=20/52, r=0.05, q=0, sigma=0.2 | 2.4005273233 | 0.5216046611 | 0.0655440393 | 12.1054798826 | -4.3053298229 | 8.9069619496 | publicado: preco=2.4, d1=0.0542, delta=0.522, gamma=0.066, vega=12.1, theta_ano=-4.31, theta_dc=-0.0118, theta_du=-0.0171, rho=8.91 |
| HULL-GREGAS-CAP19-P | BS_B3 | S=49, K=50, T_expr=20/52, r=0.05, q=0, sigma=0.2 | 2.4481754413 | -0.4783953389 | 0.0655440393 | 12.1054798826 | -1.852947417 | -9.9575180958 | calculado |
| HULL-INDICE-EX17.1-C | BSM_Q | S=930, K=900, T_expr=2/12, r=0.08, q=0.03, sigma=0.2 | 51.8329567965 | 0.7034180086 | 0.0045074039 | 129.9484533326 | -106.5313728558 | 100.3909652004 | publicado: preco=51.83 |
| HULL-INDICE-EX17.1-P | BSM_Q | S=930, K=900, T_expr=2/12, r=0.08, q=0.03, sigma=0.2 | 14.5509967738 | -0.2915944706 | 0.0045074039 | 129.9484533326 | -63.2458493752 | -47.6223090706 | calculado |
| HULL-FUTURO-CAP18-C | BLACK76 | F=20, K=20, T_expr=4/12, r=0.09, sigma=0.25 | 1.1166414566 | 0.5131388032 | 0.1337645027 | 4.4588167554 | -1.5715585522 | -0.3722138189 | calculado |
| HULL-FUTURO-CAP18-P | BLACK76 | F=20, K=20, T_expr=4/12, r=0.09, sigma=0.25 | 1.1166414566 | -0.4573067304 | 0.1337645027 | 4.4588167554 | -1.5715585522 | -0.3722138189 | publicado: preco=1.12 |
| HAUG-BS-C | BS_B3 | S=60, K=65, T=0.25, r=0.08, q=0, sigma=0.3 | 2.1333684449 | 0.372482798 | 0.0420427558 | 11.3515440535 | -8.4281743867 | 5.0538998582 | publicado: preco=2.1334 |
| HAUG-BS-P | BS_B3 | S=60, K=65, T=0.25, r=0.08, q=0, sigma=0.3 | 5.8462822099 | -0.627517202 | 0.0420427558 | 11.3515440535 | -3.3311412855 | -10.874328583 | calculado |
| HAUG-MERTON-C | BSM_Q | S=100, K=95, T=0.5, r=0.1, q=0.05, sigma=0.2 | 9.628983522 | 0.7111283124 | 0.0228395743 | 22.8395742963 | -7.160658069 | 30.7419238586 | calculado |
| HAUG-MERTON-P | BSM_Q | S=100, K=95, T=0.5, r=0.1, q=0.05, sigma=0.2 | 2.4647876468 | -0.2641815996 | 0.0228395743 | 22.8395742963 | -3.0005280964 | -14.4414738052 | publicado: preco=2.4648 |
| HAUG-BLACK76-C | BLACK76 | F=19, K=19, T=0.75, r=0.1, sigma=0.28 | 1.7010507252 | 0.5086362359 | 0.0797450347 | 6.045471079 | -0.9583828622 | -1.2757880439 | publicado: preco=1.7011 |
| HAUG-BLACK76-P | BLACK76 | F=19, K=19, T=0.75, r=0.1, sigma=0.28 | 1.7010507252 | -0.4191072504 | 0.0797450347 | 6.045471079 | -0.9583828622 | -1.2757880439 | publicado: preco=1.7011 |
| HAUG-GK-C | GK | S=1.56, K=1.6, T=0.5, r_d=0.06, r_f=0.08, sigma=0.12 | 0.0290992531 | 0.3403859092 | 2.7002660835 | 0.3942820525 | -0.0349478507 | 0.2509513826 | publicado: preco=0.0291 |
| HAUG-GK-P | GK | S=1.56, K=1.6, T=0.5, r_d=0.06, r_f=0.08, sigma=0.12 | 0.0829805817 | -0.6204035299 | 2.7002660835 | 0.3942820525 | -0.0616916015 | -0.5254050442 | calculado |
| HAUG-DELTA-B76-C | BLACK76 | F=105, K=100, T=0.5, r=0.1, sigma=0.36 | 12.4328445082 | 0.5946286597 | 0.0134936371 | 26.7781228458 | -8.3968397737 | -6.2164222541 | publicado: delta=0.5946 |
| HAUG-DELTA-B76-P | BLACK76 | F=105, K=100, T=0.5, r=0.1, sigma=0.36 | 7.6766973857 | -0.3566007648 | 0.0134936371 | 26.7781228458 | -8.8724544859 | -3.8383486928 | publicado: delta=-0.3566 |
| HAUG-GAMMA-VEGA-C | BS_B3 | S=55, K=60, T=0.75, r=0.1, q=0, sigma=0.3 | 5.3927788241 | 0.5333413897 | 0.0278211605 | 18.9357773496 | -6.1812552308 | 17.9557482064 | publicado: gamma=0.0278, vega=18.9358 |
| HAUG-GAMMA-VEGA-P | BS_B3 | S=55, K=60, T=0.75, r=0.1, q=0, sigma=0.3 | 6.0573880038 | -0.4666586103 | 0.0278211605 | 18.9357773496 | -0.6147943128 | -23.7927086784 | publicado: gamma=0.0278, vega=18.9358 |
| HAUG-THETA-C | BSM_Q | S=430, K=405, T=0.0833, r=0.07, q=0.05, sigma=0.2 | 27.323477914 | 0.859740401 | 0.0087846881 | 27.060651833 | -37.966900505 | 28.5189957143 | calculado |
| HAUG-THETA-P | BSM_Q | S=430, K=405, T=0.0833, r=0.07, q=0.05, sigma=0.2 | 1.7560201839 | -0.1361032606 | 0.0087846881 | 27.060651833 | -31.1923670565 | -5.0213591711 | publicado: theta_ano=-31.1924 |
| HAUG-RHO-C | BS_B3 | S=72, K=75, T=1, r=0.09, q=0, sigma=0.19 | 7.2227519482 | 0.6382674579 | 0.0273928883 | 26.9808993042 | -6.0491108855 | 38.7325050173 | publicado: rho=38.7325 |
| HAUG-RHO-P | BS_B3 | S=72, K=75, T=1, r=0.09, q=0, sigma=0.19 | 3.7675908436 | -0.3617325421 | 0.0273928883 | 26.9808993042 | 0.1199246151 | -29.812333878 | calculado |
| B3-ACAO-REF-21DU-C | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, sigma=0.35 | 0.5646945184 | 0.3068575083 | 0.1158729783 | 3.0416656804 | -7.2619864884 | 0.7200858943 | calculado |
| B3-ACAO-REF-21DU-P | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, sigma=0.35 | 2.2959576248 | -0.6931424917 | 0.1158729783 | 3.0416656804 | -4.0507229911 | -1.9241860313 | calculado |
| B3-ACAO-ATM-10DU-C | BS_B3 | S=38.42, K=38, DU=10, DI_aa=0.149, q=0, sigma=0.31 | 1.2863641828 | 0.6171965842 | 0.1608390131 | 2.9205676728 | -14.5225749338 | 0.8899336738 | calculado |
| B3-ACAO-ATM-10DU-P | BS_B3 | S=38.42, K=38, DU=10, DI_aa=0.149, q=0, sigma=0.31 | 0.6574999825 | -0.3828034158 | 0.1608390131 | 2.9205676728 | -9.2736885432 | -0.6097145722 | calculado |
| B3-ACAO-1DU-ATM-C | BS_B3 | S=30, K=30, DU=1, DI_aa=0.149, q=0, sigma=0.4 | 0.3098181753 | 0.5137497146 | 0.5274375511 | 0.7534822158 | -40.0731441549 | 0.0599312431 | calculado |
| B3-ACAO-1DU-ATM-P | BS_B3 | S=30, K=30, DU=1, DI_aa=0.149, q=0, sigma=0.4 | 0.2932879694 | -0.4862502854 | 0.5274375511 | 0.7534822158 | -35.9086801022 | -0.0590507799 | calculado |
| B3-ACAO-1DU-K31-C | BS_B3 | S=30, K=31, DU=1, DI_aa=0.149, q=0, sigma=0.55 | 0.100275715 | 0.180575818 | 0.2529592917 | 0.496884323 | -35.1725721812 | 0.0210992017 | calculado |
| B3-ACAO-1DU-K31-P | BS_B3 | S=30, K=31, DU=1, DI_aa=0.149, q=0, sigma=0.55 | 1.0831945022 | -0.819424182 | 0.2529592917 | 0.496884323 | -30.8692926601 | -0.1018488887 | calculado |
| B3-ACAO-126DU-K26-C | BS_B3 | S=20, K=26, DU=126, DI_aa=0.1435, q=0, sigma=0.45 | 1.1492578439 | 0.3246537859 | 0.0565304058 | 5.0877365188 | -3.0060539285 | 2.6719089368 | calculado |
| B3-ACAO-126DU-K26-P | BS_B3 | S=20, K=26, DU=126, DI_aa=0.1435, q=0, sigma=0.45 | 5.4631935248 | -0.6753462141 | 0.0565304058 | 5.0877365188 | 0.2542925069 | -9.4850589037 | calculado |
| B3-INDICE-BSMQ-42DU-C | BSM_Q | S=145000, K=147000, DU=42, DI_aa=0.1475, q=0.045, sigma=0.21 | 5042.0286056252 | 0.5212206437 | 3.1789040544e-05 | 23392.7602102763 | -21041.0741156307 | 11755.8274541847 | calculado |
| B3-INDICE-BSMQ-42DU-P | BSM_Q | S=145000, K=147000, DU=42, DI_aa=0.1475, q=0.045, sigma=0.21 | 4792.9665573401 | -0.4713074112 | 3.1789040544e-05 | 23392.7602102763 | -7750.7306292654 | -12188.7568625636 | calculado |
| B3-IND-B76-15DU-C | BLACK76 | F=130000, K=132000, DU=15, DI_aa=0.1065, sigma=0.2 | 1663.5718122475 | 0.3841637029 | 5.9965641013e-05 | 12064.5158704933 | -20100.0300666676 | -99.0221316814 | calculado |
| B3-IND-B76-15DU-P | BLACK76 | F=130000, K=132000, DU=15, DI_aa=0.1065, sigma=0.2 | 3651.5601842045 | -0.6098304831 | 5.9965641013e-05 | 12064.5158704933 | -19898.8419049956 | -217.3547728693 | calculado |
| B3-IND-B76-1DU-C | BLACK76 | F=150000, K=150000, DU=1, DI_aa=0.149, sigma=0.18 | 678.1595279119 | 0.5019850283 | 2.3442300413e-04 | 3767.5125663783 | -85352.9940730773 | -2.6911092377 | calculado |
| B3-IND-B76-1DU-P | BLACK76 | F=150000, K=150000, DU=1, DI_aa=0.149, sigma=0.18 | 678.1595279119 | -0.4974639648 | 2.3442300413e-04 | 3767.5125663783 | -85352.9940730773 | -2.6911092377 | calculado |
| B3-DOL-GK-20DU-C | GK | S=5.4, K=5.5, DU=20, DC=28, DI_aa=0.1065, cupom_lin_aa=0.05, sigma=0.14 | 0.052240309 | 0.3654019443 | 1.7609391824 | 0.5705442951 | -0.6011239747 | 0.152454777 | calculado |
| B3-DOL-GK-20DU-P | GK | S=5.4, K=5.5, DU=20, DC=28, DI_aa=0.1065, cupom_lin_aa=0.05, sigma=0.14 | 0.1291604669 | -0.6307242316 | 1.7609391824 | 0.5705442951 | -0.3120301661 | -0.2805612157 | calculado |
| B3-DOL-B76-EQUIV-20DU-C | BLACK76 | F=5.42246, K=5.5, DU=20, DI_aa=0.1065, sigma=0.14 | 0.052240309 | 0.3638884689 | 1.7463819592 | 0.5705442951 | -0.4979332508 | -0.0041460563 | calculado |
| B3-DOL-B76-EQUIV-20DU-P | BLACK76 | F=5.42246, K=5.5, DU=20, DI_aa=0.1065, sigma=0.14 | 0.1291604669 | -0.6281118053 | 1.7463819592 | 0.5705442951 | -0.4901487861 | -0.0102508307 | calculado |

### 6.2 Vol implícita

| id | modelo | entradas | σ esperado | tol. σ | falha | limites | origem |
|---|---|---|---|---|---|---|---|
| IV-HULL-15.11 | BS_B3 | S=21, K=20, T=0.25, r=0.1, q=0, preco=1.875 | 0.234512913998 | 1e-10 | não | (1.493802; 21) | publicado: sigma=0.235 |
| IV-HAUG-B76-PUBLICADO | BLACK76 | F=19, K=19, T=0.75, r=0.1, preco=1.7011 | 0.280008150692 | 1e-10 | não | (0; 17.627126) | calculado |
| IV-B3-REF-C | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, preco=0.564695 | 0.35 | 1e-10 | não | (0; 30) | calculado |
| IV-B3-REF-P | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, preco=2.295958 | 0.35 | 1e-10 | não | (1.731263; 31.731263) | calculado |
| IV-B3-TICK-C | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, preco=0.56 | 0.348455549942 | 1e-10 | não | (0; 30) | calculado |
| IV-ITM-C-MODERADO | BS_B3 | S=100, K=70, T=0.25, r=0.1, q=0, preco=31.749877 | 0.3 | 1e-10 | não | (31.728306; 100) | calculado |
| IV-ITM-C-EXTREMO | BS_B3 | S=100, K=50, T=0.25, r=0.1, q=0, preco=51.234504 | 0.249999996281 | 1e-06 | não | (51.234504; 100) | calculado |
| IV-ITM-P-B3-EXTREMO | BS_B3 | S=20, K=34, DU=21, DI_aa=0.149, q=0, preco=13.608741 | 0.350000000058 | 1e-07 | não | (13.608741; 33.608741) | calculado |
| IV-P-ABAIXO-INTRINSECO-VALIDO | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, preco=1.95 | 0.226563688269 | 1e-10 | não | (1.731263; 31.731263) | calculado |
| IV-OTM-C-PROFUNDO | BS_B3 | S=100, K=150, T=0.25, r=0.05, q=0, preco=0.025032 | 0.3 | 1e-10 | não | (0; 100) | calculado |
| IV-OTM-C-EXTREMO | BS_B3 | S=100, K=200, T=0.25, r=0.05, q=0, preco=1.213233e-05 | 0.3 | 1e-10 | não | (0; 100) | calculado |
| IV-OTM-P-B3 | BS_B3 | S=30, K=22, DU=21, DI_aa=0.149, q=0, preco=0.016549 | 0.5 | 1e-10 | não | (0; 21.746833) | calculado |
| IV-1DU-ATM-C | BS_B3 | S=30, K=30, DU=1, DI_aa=0.149, q=0, preco=0.309818 | 0.4 | 1e-10 | não | (0.01653; 30) | calculado |
| IV-1DU-OTM-C-TICK | BS_B3 | S=30, K=31, DU=1, DI_aa=0.149, q=0, preco=0.05 | 0.437151761551 | 1e-10 | não | (0; 30) | calculado |
| IV-1DU-OTM-P-TICK | BS_B3 | S=30, K=29, DU=1, DI_aa=0.149, q=0, preco=0.01 | 0.316269314192 | 1e-10 | não | (0; 28.984021) | calculado |
| IV-1DU-ITM-C-PERTO-LIMITE | BS_B3 | S=30, K=29, DU=1, DI_aa=0.149, q=0, preco=1.02 | 0.270483220046 | 1e-10 | não | (1.015979; 30) | calculado |
| IV-VOL-ALTA | BS_B3 | S=30, K=30, DU=5, DI_aa=0.149, q=0, preco=4.228559 | 2.5 | 1e-10 | não | (0.08256; 30) | calculado |
| IV-VOL-BAIXA | BS_B3 | S=30, K=31.06, DU=63, DI_aa=0.149, q=0, preco=0.119676 | 0.02 | 1e-10 | não | (0; 30) | calculado |
| IV-B76-IND | BLACK76 | F=130000, K=132000, DU=15, DI_aa=0.1065, preco=1660 | 0.199703919334 | 1e-10 | não | (0; 129219.244177) | calculado |
| IV-GK-DOL | GK | S=5.4, K=5.5, DU=20, DC=28, DI_aa=0.1065, cupom_lin_aa=0.05, preco=0.052 | 0.139578725281 | 1e-10 | não | (0; 5.379081) | calculado |
| IV-FALHA-C-ABAIXO-INTRINSECO | BS_B3 | S=30, K=28, DU=21, DI_aa=0.149, q=0, preco=1.9 | — | — | sim | (2.322213; 30) | calculado |
| IV-FALHA-C-ENTRE-INTRINSECO-E-LIMITE | BS_B3 | S=30, K=28, DU=21, DI_aa=0.149, q=0, preco=2.1 | — | — | sim | (2.322213; 30) | calculado |
| IV-FALHA-P-ABAIXO-LIMITE | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, preco=1.5 | — | — | sim | (1.731263; 31.731263) | calculado |
| IV-FALHA-1DU-ABAIXO-LIMITE | BS_B3 | S=30, K=29, DU=1, DI_aa=0.149, q=0, preco=1.01 | — | — | sim | (1.015979; 30) | calculado |
| IV-FALHA-C-ACIMA-MAXIMO | BS_B3 | S=30, K=28, DU=21, DI_aa=0.149, q=0, preco=30.01 | — | — | sim | (2.322213; 30) | calculado |
| IV-FALHA-P-ACIMA-MAXIMO | BS_B3 | S=30, K=32, DU=21, DI_aa=0.1065, q=0, preco=31.8 | — | — | sim | (1.731263; 31.731263) | calculado |
| IV-FALHA-PRECO-ZERO | BS_B3 | S=30, K=35, DU=21, DI_aa=0.149, q=0, preco=0 | — | — | sim | (0; 30) | calculado |
| IV-FALHA-PRECO-NEGATIVO | BS_B3 | S=30, K=35, DU=21, DI_aa=0.149, q=0, preco=-0.01 | — | — | sim | (0; 30) | calculado |
| IV-FALHA-B76-ABAIXO-LIMITE | BLACK76 | F=130000, K=125000, DU=15, DI_aa=0.1065, preco=4950 | — | — | sim | (4969.97093; 129219.244177) | calculado |

### 6.3 Taxas na convenção B3

| id | função | entradas | saídas |
|---|---|---|---|
| TX-TAXA-CONT-1065 | `taxa_cont` | DI_aa=0.1065 | r=0.101201880509 |
| TX-TAXA-CONT-1490 | `taxa_cont` | DI_aa=0.149 | r=0.138891998867 |
| TX-FATOR-DESCONTO-21DU | `fator_desconto` | DI_aa=0.149, DU=21 | fator_desconto=0.988492391676, fator_periodo=1.01164157501 |
| TX-TAXA-DIARIA | `taxa_diaria` | DI_aa=0.149 | i_d=5.513106415403e-04 |
| TX-DI-INTERP-21DU | `di_interpola` | curva=[[21, 0.149], [63, 0.146]], DU=21 | taxa_aa=0.149, fator_periodo=1.01164157501 |
| TX-DI-INTERP-42DU | `di_interpola` | curva=[[21, 0.149], [63, 0.146]], DU=42 | taxa_aa=0.146749264866, fator_periodo=1.023084280193 |
| TX-DI-INTERP-50DU | `di_interpola` | curva=[[21, 0.149], [63, 0.146]], DU=50 | taxa_aa=0.146389556613, fator_periodo=1.027477371627 |
| TX-DI-INTERP-63DU | `di_interpola` | curva=[[21, 0.149], [63, 0.146]], DU=63 | taxa_aa=0.146, fator_periodo=1.034656414123 |
| TX-CUPOM-CONT-20DU | `cupom_cont` | cupom_lin_aa=0.05, DU=20, DC=28 | q=0.04890496852 |

As notas de cada caso (por que ele existe e o que testa) estão no campo `nota` do JSON.
