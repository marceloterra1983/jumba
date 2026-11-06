# Especificação do motor de opções: funções, entradas, saídas e unidades

- **Data:** 2026-11-04. Fontes e fórmulas: notas `01` a `14` desta pasta. Cada função aponta a nota de origem.
- **Legenda:** [C] confirmado em fonte, [I] inferência, [S] a testar, [P] proposta (decisão do Marcelo).

## 0. Princípios [P]

1. **Cálculo puro:** sem I/O, sem relógio e sem rede. Toda entrada vem por parâmetro, incluindo `agora` e o calendário. É o padrão de `OperacaoOpcaoCalculadora.cs` citado em `../../pesquisa/matrix.md` §3.
2. **Unidades explícitas no nome ou no tipo:** `_aa` (ao ano), `_cont` (contínua), `_du`, `_rs`, `_pct`, `_pp`.
3. **Sem exceção por dado ruim:** a função devolve `NaN` e uma lista de `flags`.
4. **Fonte de dados (regra do dono):**
   - **B3 primeiro:** cadastro (BVBG.028 ou InstrumentsConsolidated), OI (DerivativesOpenPosition / BDI), BVBG.086, Prêmio de Referência e curva TS.
   - **ProfitDLL só** para o que a B3 não dá: preço ao vivo, book e DI1 intradiário.
   - A DLL **não tem gregas nem strike** [C manual ProfitDLL; ver `../../pesquisa/fontes-dados.md`].
5. **Convenções em aberto viram parâmetros** do objeto `Config` (§3), nunca constantes no código.

## 1. Tipos de dados

| Tipo | Campos (unidade) | Origem |
|---|---|---|
| `Serie` | `ticker`; `objeto`; `tipo` ∈ {C,P}; `K` (R$ ou pts, **vigente no cadastro do dia**); `vencimento` (data); `estilo` ∈ {AME, EUR} (`OptnStyle`/`ExrcStyle`); `m` (unid. do objeto por contrato; `CtrctMltplr`); `protegida` (bool; `PrtcnFlg`); `premio_a_vista` (bool; `PrmUpfrntInd`); `modelo` ∈ {BS_B3, BSM_Q, BLACK76, GK} | cadastro B3 |
| `PosicaoAberta` | `oi`, `cvrd`, `blck`, `ucvrd` (contratos); `titulares`, `lancadores` (clientes; **[S]** `BrrwrQty`/`LndrQty`); `data_ref` | OI B3 (D−1) |
| `Cotacao` | `bid`, `ask`, `last` (R$/unid); `t_last` (instante); `qtd_dia` (contratos); `fin_dia` (R$) | DLL (ao vivo) ou BVBG.086 (diário) |
| `Objeto` | `S` ou `F` (R$ ou pts); instante | DLL ou fechamento B3 |
| `CurvaDI` | lista de `(du, taxa_aa_252)` | TS/BVBG.086 ou DI1 pela DLL |
| `CurvaCupom` | lista de `(du, dc, cupom_linear_360)` | B3 (DDI/FRC) [S] |
| `Provento` | `tipo` ∈ {DIV, JCP, REND}; `valor_bruto` (R$/ação); `data_com`; `data_ex` | B3 eventos e DLL `SubscribeAdjustHistory` |
| `Superficie` | por vencimento: params SVI `(a,b,ρ,m,σ)` em variância total, `F_T`, `T`, `rmse_vol`, `flags` | saída de `svi_ajusta` |
| `Perna` | `serie` ou `objeto`; `lado` ∈ {+1, −1}; `qtd`; `preco_usado`; `fonte_preco` | usuário ou scanner |

## 2. Funções

### 2.1 Calendário e taxas (nota 01)

| Função | Entradas (unidade) | Saídas (unidade) | Nota |
|---|---|---|---|
| `prazo(agora, vencimento, calendario_b3, hora_limite)` | instantes; feriados B3 | `du` (int), `dc` (int), `T` (anos = (DU restantes + fração do pregão)/252) | 01 §2 |
| `di_interpola(curva, du)` | `CurvaDI`; `du` | `taxa_aa` (fração a.a., base 252), por interpolação exponencial (flat forward 252) | 01 §3 |
| `taxa_cont(taxa_aa)` | fração a.a. | `r` = ln(1+i) (contínua a.a.) | 01 §3 [C B3] |
| `fator_desconto(taxa_aa, du)` | — | $(1+i)^{-du/252}$ | 01 §3 |
| `cupom_cont(cupom_lin, du, dc)` | fração a.a. linear/360 | `q` = (252/du)·ln(1+c·dc/360) | 01 §3, 04 [C B3] |
| `forward_paridade(c, p, K, r, T)` | R$; contínua; anos | `F` = K + e^{rT}(c − p) (mediana de 3 strikes ATM) | 03 §3 |
| `taxa_periodo_para_aa(r_per, du)` | fração; DU | $(1+r_{per})^{252/du}-1$ | 14 §1 |
| `pct_cdi(r_per, du, di_aa, convencao)` | — | `%CDI` pela razão de períodos (1) ou estilo CDB (2) | 14 §1 |

### 2.2 Precificação (notas 02 a 04)

| Função | Entradas | Saídas | Nota |
|---|---|---|---|
| `preco_gbs(tipo, S, K, T, r, b, σ)` | R$; R$; anos; contínua; contínua; fração a.a. | preço (R$/unid. do objeto) | 01 §1 |
| `preco_bs_b3(tipo, S, K, T, r, σ)` | — | `preco_gbs` com b=r (sem dividendo; padrão para ações protegidas) | 02 §1.2 [C B3] |
| `preco_bsm(tipo, S, K, T, r, q, σ)` | `q` contínua a.a. | b=r−q | 02 §1.1 |
| `preco_black76(tipo, F, K, T, r, σ, premio_a_vista)` | F em R$ ou pts | `e^{−rT}[…]` se à vista, senão sem desconto | 03 §1 |
| `preco_gk(tipo, S, K, T, r_d, r_f, σ)` | — | b = r_d − r_f | 04 §2 [C B3] |
| `preco_escrow(tipo, S, K, T, r, σ*, proventos, protegida)` | proventos com `t_ex` e valor ajustado | preço com S* = S − ΣDe^{−rt}; K − D se protegida | 02 §1.3, §3 |
| `valor_ajuste_provento(provento, ano)` | bruto | D_aj: dividendo cheio [S para 2026]; JCP × 0,825 desde 2026 [C OC 026/2025] | 02 §2.1 |
| `ajuste_fator(K, qtd, P_ex, P_com)` | — | `K_aj` (2 casas), `qtd_aj` (truncada), F (8 casas) | 02 §2.2 [C OC 093/2022] |
| `preco_americano(tipo, …, passos=200)` | — | preço por árvore CRR (para puts americanas) | 02 §4 [P] |

### 2.3 Gregas (nota 05)

| Função | Entradas | Saídas (unidade crua) | Nota |
|---|---|---|---|
| `gregas(tipo, S, K, T, r, b, σ, modelo)` | como `preco_gbs` | `delta` (unid./opção), `gamma` (1/R$), `vega` (R$ por 1,00 de vol), `theta` (R$/ano), `rho` (R$ por 1,00 de taxa; fórmula conforme o modelo), `vanna`, `charm` (Δ/ano), `vomma` | 05 §1 |
| `escala(gregas, S, m, qtd, cfg)` | — | `delta_pct` (Δ×100), `delta_rs` (Δ·S·m·qtd), `gamma_1pct` (Γ·S·0,01), `cash_gamma_rs` (Γ·S²·0,01·m·qtd), `pnl_1pct` (½Γ(0,01S)²), `vega_pp` (ν/100), `theta_du` (Θ/252) ou `theta_dc` (Θ/365), `rho_pp` (ρ/100), `rho_di_pp` (ρ/[100(1+DI)]) | 05 §2 |

### 2.4 Vol implícita (nota 06)

| Função | Entradas | Saídas | Nota |
|---|---|---|---|
| `escolhe_preco(cot, regras, agora)` | `Cotacao`; limites de spread e idade | `preco`, `fonte` ∈ {MID, LAST, PREMIO_REF, FECH}, flags | 06 §6 |
| `limites_arbitragem(tipo, S, K, T, r, b)` | — | `(min, max)` em R$ | 06 §2 |
| `vol_implicita(tipo, P, S, K, T, r, b, metodo, σ0)` | preço em R$ | `iv` (fração a.a.), `metodo`, `iteracoes`, flags (`FORA_DOS_LIMITES`, `PRECO_MINIMO`, `NAO_CONVERGIU`, `AMERICANA_APROX`) | 06 §3–5 |

### 2.5 Smile e superfície (nota 07)

| Função | Entradas | Saídas | Nota |
|---|---|---|---|
| `svi_w(k, params)` | k = ln(K/F) | variância total w | 07 §1.1 |
| `svi_ajusta(k[], w[], pesos[], chute, cfg)` | pontos OTM de 1 vencimento; mínimo de 5 | `params`, `rmse_vol`, flags (`SVI_INSUFICIENTE`, `ARBITRAGEM`) | 07 §3 |
| `svi_g(k, params)` | — | g(k) (≥ 0 = sem borboleta) | 07 §2 |
| `checa_calendario(sup, grade_k)` | 2 vencimentos | bool, k violados | 07 §2 |
| `vol_superficie(K, T, sup)` | R$; anos | σ (fração a.a.), por interpolação linear em T da variância total com k fixo | 07 §3 |
| `preco_teorico(serie, sup, objeto, curva)` | — | preço "Preço Jumba" (R$) | 07 §3 |
| `cone(S, σ_atm, T, n=2)` | — | S·e^{±nσ√T} | 07 §4 |

### 2.6 Exposições (nota 08)

| Função | Entradas | Saídas (unidade) | Nota |
|---|---|---|---|
| `sinal(serie, posicao, cfg.convencao_sinal, θ)` | convenção A, B, C, D ou E | `s_i` ∈ [−1, 1] | 08 §3 |
| `gex_serie(Γ, oi, m, S, s, unidade)` | — | U1 (unid./R$1), U2 (R$/R$1) ou **U3 (R$ por 1 %)** | 08 §1 |
| `gex_strike(series, cfg.vencimentos)` | lista de séries com gregas e OI | `{K: GEX_rs_1pct}`, `total`, `acumulado` | 08 §2 |
| `dex_strike(series, cfg)` | — | `{K: DEX_rs}`, `total_rs`, `total_unid`, `hedge_rs = −total` | 08 §4 |
| `dex_atm(series, h)` | h = faixa ±% | DEX_rs na faixa | 08 §4 |
| `vex(series)`, `cex(series)` | — | R$ de Δ por 1 p.p. de vol; R$ de Δ por DU | 08 §4 |

### 2.7 Níveis do perfil (nota 09)

| Função | Entradas | Saídas | Nota |
|---|---|---|---|
| `perfil_gamma(series, grade_X, cfg.vol_modo)` | grade de preços; STICKY_STRIKE ou STICKY_MONEYNESS | `G(X)` em R$ por 1 % | 09 §1 |
| `gamma_flip(perfil ou gex_strike, metodo)` | M1 (varredura + Brent) ou M2 (acumulado por strike) | `x_flip`, `raizes[]`, `regime` ∈ {POSITIVO, NEGATIVO, PERTO_DO_FLIP, SEM_FLIP} | 09 §2 |
| `walls(series, S, cfg.regra_wall, cfg.lado)` | regra a (gamma nocional), b (OI) ou c (GEX com sinal) | `call_wall`, `put_wall` (R$ ou pts) | 09 §3 |
| `jumba_walls(gex_strike, S, N, faixa)` | — | `walls[]`, `midwalls[]` (fixas no pregão) | 09 §4 |
| `extremos_perfil(perfil)` | — | `x_min`, `x_max` (Bands) | 09 §5 |

### 2.8 Métricas de OI (notas 10 a 13)

| Função | Entradas | Saídas | Nota |
|---|---|---|---|
| `max_pain(series_de_1_vencimento, metodo)` | A (intrínseco × OI) ou B (contagem ITM) | `K_max_pain`, `dor[X]` (R$), `itm[X]` (contratos), `dist_pct` | 10 |
| `pcr(series, base, cfg)` | base ∈ {OI, VOL, FIN, DESC, DELTA} | razão (adimensional), flags | 11 |
| `iq_serie(titulares, lancadores)` | contagens de clientes | razão, `SEM_LANCADOR` | 12 §1 |
| `iq_agregado(series, tipo, metodo)` | RAZAO_SOMAS, POND_OI ou POND_DESC | IQ do ativo/tipo e IQ global | 12 §2 |
| `barreiras(series, Q_min, IQ_min, h, S)` | — | lista de strikes com distância % | 12 §3 |
| `bgt_move(series, sinais, horizonte_du)` | — | `bgt` (R$/pts), `bgt_pct`, `banda_inf`, `banda_sup`, `sigma_efetiva`, flag `SINAIS_IGUAIS` | 13 [hipótese] |

### 2.9 Estruturas e taxas (nota 14)

| Função | Entradas | Saídas | Nota |
|---|---|---|---|
| `venda_coberta(S_ask, C_bid, K, du, curva)` | R$ | `capital`, `ve`, `r_parado`, `r_max`, `protecao_pct`, versões a.a. e %CDI | 14 §2 |
| `cash_put(P_bid, K, S, du, curva, cfg.capital)` | — | `r_premio`, `r_total`, `preco_efetivo` | 14 §3 |
| `box3(S_ask, P_ask, C_bid, K, du, curva)` | — | `capital`, `r_per`, `r_aa`, `pct_cdi_1`, `pct_cdi_2`, `spread_aa` | 14 §4 |
| `box4(C1_ask, C2_bid, P2_ask, P1_bid, K1, K2, du, curva, lado)` | lado: aplicação ou captação | idem e `r_cont_implicita` | 14 §5 |
| `collar(S_ask, P1_ask, C2_bid, K1, K2, du, curva)` | — | `r_min`, `r_max`, `r_parado`, `perda_max`, `ganho_max` | 14 §6 |
| `payoff(pernas, grade_ST, t_avaliacao, sup)` | t = vencimento ou D+n | P&L (R$), breakevens, máximos | matrix §3 item 15 |

### 2.10 Ajustes e eventos (nota 02)

| Função | Entradas | Saídas | Nota |
|---|---|---|---|
| `detecta_ajustes(cad_D, cad_Dm1)` | dois cadastros | eventos `(ticker, K_antigo, K_novo, qtd_fator, data)` | 02 §2.3 |
| `classifica_ajuste(evento, proventos)` | — | SUBTRACAO, FATOR, DESDOBRAMENTO ou DESCONHECIDO | 02 §2 |

## 3. `Config`: convenções em aberto e padrão proposto [P]

| Parâmetro | Opções | Padrão |
|---|---|---|
| `modelo_acao` | BS_B3, BSM_Q, ESCROW | BS_B3 (igual à B3; vol comparável com o Prêmio de Referência) |
| `modelo_ind` / `modelo_dol` | BLACK76 sobre o futuro, ou GK | BLACK76 |
| `fracao_intradiaria` | sim ou não; horário-limite | sim; 17h55 (dia normal) e horário-limite da série no vencimento [S] |
| `jcp_fator` | 0,85 (até 2025), 0,825 (2026+) | por data do evento |
| `dividendo_liquido_2026` | bruto ou líquido (OC 006/2026, não lido) | **em aberto** |
| `preco_iv` | MID, LAST, PREMIO_REF | MID com fallback LAST (intradiário); PREMIO_REF (foto) |
| `spread_max_mid` | % | 20 % |
| `svi_pesos` | 1, vega, 1/spread² | 1 (igual à NT-2013-01) |
| `vol_modo_perfil` | STICKY_STRIKE, STICKY_MONEYNESS | STICKY_STRIKE |
| `unidade_gex` | U1, U2, U3 | U3 (R$ por 1 %) |
| `convencao_sinal` | A, B, C, D, E | A (calls +, puts −) |
| `θ_D` (convenção D) | θ_c, θ_b, θ_u | 1, 0, 1 |
| `vencimentos` | TODOS, PROXIMO, ATE_N_DIAS | TODOS |
| `metodo_flip` | M1, M2 | M1 |
| `regra_wall` / `lado_wall` | a, b, c / restrito ou livre | a / livre |
| `n_walls`, `faixa_walls` | — | 3 por lado; 5 % (ações), 2 % (IND e DOL) |
| `faixa_atm` (DEX ATM) | % | 2 % e 5 % |
| `max_pain_metodo` | A, B | A (e B junto) |
| `pcr_base` | OI, VOL, FIN | OI e VOL |
| `iq_agregacao` | RAZAO_SOMAS, POND_OI, POND_DESC | RAZAO_SOMAS |
| `bgt_horizonte_du` | 1, até o vencimento | 1 |
| `pct_cdi` | razão (1), CDB (2) | (1) e (2) exibidos |
| `cdi_ref` | curva DI1 no vértice, ou DI do dia | curva DI1 |
| `capital_cash_put` | K − P, ou K | K − P |
| `custos_ir` | ligado ou desligado | desligado |

## 4. Vetores de teste (tolerância 1e-6)

Gerados por `scripts/vetores.py` e `scripts/check_charm.py` (rodar com `python3 -I`; só biblioteca padrão).

| Caso | Entrada | Saída esperada |
|---|---|---|
| BS_B3 call | S=30, K=32, DU=21, DI=10,65 %, σ=35 % | 0,564695; Δ 0,306858; Γ 0,115873; ν 3,041666; Θ −7,261986/ano; ρ 0,720086 |
| BS_B3 put | idem | 2,295958; Δ −0,693142; Θ −4,050723; ρ −1,924186 |
| IV Newton | preço 0,564695, σ0=0,30 | 0,350000 em 4 iterações |
| Charm, vanna e theta | S=30, K=32, T=21/252, r=0,101203, b=0,07, σ=0,35 | call: charm −1,54008, vanna 0,62374, Θ −6,85576; put: −1,57120, 0,62374, −4,57812 (bate com diferenças finitas) |
| Escrow protegido | D=1,00, data-ex em 10 DU, σ*=σS/S* | 0,564477 (contra 0,564695 do BS_B3) |
| Black-76 IND | F=130.000, K=132.000, DU=15, σ=20 % | call 1.663,57; put 3.651,56; GEX por contrato R$ 10.134 por 1 % |
| GK DOL | S=5,40, K=5,50, DU=20, DC=28, cupom 5 %, σ=14 % | call 0,052240; put 0,129160; F=5,42246; Black-76(F) = GK |
| BGT | S=K=100, T=30/252, σ=30 %, r=0 | 1,889822 = Sσ/√252 |
| Max Pain | ver nota 10 §4 | A = B = 30 |
| Box 3 | S=30, K=30, P=1,20, C=1,65, DU=21 | r_per 1,5228 %; r_aa 19,89 %; %CDI 179,8 % (1) e 179,2 % (2) |

## 5. Telas e funções que alimentam

| Tela (nome genérico) | Funções |
|---|---|
| Mapa e Resumo do Mapa | junção cadastro × OI, `iq_*` |
| Scanner de Barreiras | `barreiras` |
| Market Gamma, Walls, Bands, Resumo do Gamma | `gregas`, `gex_strike`, `perfil_gamma`, `gamma_flip`, `walls`, `jumba_walls`, `extremos_perfil` |
| Market Exposure e Histórico ATM | `dex_strike`, `dex_atm` |
| Volatilidade, Histórico de VI, Preço teórico | `vol_implicita`, `svi_ajusta`, `vol_superficie`, `preco_teorico`, `cone` |
| Max Pain e History | `max_pain` |
| PCR | `pcr` |
| BGT (Payoff) | `bgt_move` [hipótese] |
| FYT: calculadora, payoff, delta estrutural e buscadores | `preco_*`, `gregas`, `payoff`, `venda_coberta`, `cash_put`, `box3`, `box4`, `collar` |
| Histórico de Ajustes | `detecta_ajustes`, `classifica_ajuste` |
