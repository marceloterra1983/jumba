# 08. GEX e DEX por strike e total: fórmulas, unidades e convenções de sinal

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - SqueezeMetrics (Prior Analytics LLC), *Gamma Exposure (GEX): Quantifying hedge rebalancing in SPX options*, mar/2016, revisado em dez/2017: <https://squeezemetrics.com/monitor/download/pdf/white_paper.pdf>
  - SpotGamma, *Gamma Exposure (GEX)*: <https://spotgamma.com/gamma-exposure-gex/> (também acessível por <https://spotgamma.com/?p=19312>)
  - SpotGamma, *Call Wall / Put Wall explained*: <https://spotgamma.com/call-wall-put-wall-explained/>
  - S. Perfiliev, thread "How to calculate gamma exposure and zero gamma level" (01/02/2022): <https://threadreaderapp.com/thread/1489373524066279430.html>. O blog citado na thread é perfiliev.co.uk/market-commentary/how-to-calculate-gamma-exposure-and-zero-gamma-level (não aberto).
  - Jumba, frases públicas sobre Market Gamma: `../jumba-publico/glossario-jumba.md` e `../jumba-publico/telegram-busca-flip.md`.
  - Glossário das posições em aberto da B3 (CvrdQty, UcvrdQty, TtlBlckdPos): `../b3-opcoes/02-posicoes-em-aberto.md`.

## 1. Definições por opção

Para cada série $i$: $\Gamma_i$ e $\Delta_i$ por unidade do objeto (notas 02 a 05), $OI_i$ em contratos, $m_i$ em unidades do objeto por contrato (nota 01 §4) e $s_i$ o sinal ou peso da posição atribuída aos formadores de mercado (§3).

**GEX em três unidades**, que não são intercambiáveis [C SpotGamma]:

| Unidade | Fórmula | Leitura | Quem usa |
|---|---|---|---|
| U1: objeto por R$ 1 | $G^{(1)}_i=s_i\,\Gamma_i\,OI_i\,m_i$ | unidades do objeto (ações, contratos) que o hedge precisa negociar por R$ 1 de movimento | SqueezeMetrics: "GEX = Γ · OI · 100" (calls) e "Γ · OI · (−100)" (puts), "in shares" [C] |
| U2: R$ por R$ 1 | $G^{(2)}_i=s_i\,\Gamma_i\,OI_i\,m_i\,S$ | R$ de delta por R$ 1 de movimento | SqueezeMetrics "denominate GEX in dollars" (SPX) [C] |
| **U3: R$ por 1 %** | $G^{(3)}_i=s_i\,\Gamma_i\,OI_i\,m_i\,S^2\cdot0{,}01$ | R$ de delta que o hedge negocia num movimento de 1 % | SpotGamma: "Γ × modeled dealer position × contract multiplier × spot² × 0.01" [C]; Perfiliev: "Gamma × Contract Size × Open Interest × Spot² × 0.01" [C] |

**De onde vem o $S^2\cdot0{,}01$:**
- Num movimento $dS=0{,}01S$, o delta muda $\Gamma\cdot0{,}01S$ unidades do objeto.
- Em R$, isso é $\Gamma\cdot0{,}01S\cdot S$.
- **Padrão do motor [P]: U3**, que permite somar ativos diferentes e IND, DOL e ações na mesma escala. Nas opções sobre futuro, troque $S$ por $F$ (nota 03).

## 2. Por strike e total

$$
\text{GEX}(K)=\sum_{i\in\mathcal V:\,K_i=K}G^{(3)}_i,\qquad
\text{GEX}_{tot}=\sum_{i\in\mathcal V}G^{(3)}_i,\qquad
\text{GEX}^{acum}(K_j)=\sum_{K\le K_j}\text{GEX}(K)
$$

- $\mathcal V$ = conjunto de vencimentos escolhido: todos, só o próximo, ou até N dias. Perfiliev e SpotGamma somam todas as expirações [C].
- A Jumba deixa filtrar? **Em aberto.**
- **Strike no eixo:** o strike vigente no cadastro, já ajustado por proventos.
- Séries do mesmo strike com vencimentos diferentes somam no mesmo ponto do eixo.

**Vetor:** ação a S=30. Uma série call K=32, DU=21, σ=35 %, com Γ=0,115873, $OI$=100.000 opções, $m$=1 e $s=+1$:

$$G^{(3)}=0{,}115873\times100.000\times30^2\times0{,}01=\text{R\$ }104.286\ \text{por 1 \%}$$

Conferência: num movimento de R$ 0,30, o delta da posição muda 3.476 ações, que valem cerca de R$ 104 mil.

## 3. Convenções de sinal ($s_i$)

| Código | Convenção | $s_i$ calls | $s_i$ puts | Fonte e status |
|---|---|---|---|---|
| **A** (padrão de mercado) | Formador de mercado **comprado em calls e vendido em puts**: o investidor vende call coberta e compra put de proteção | +1 | −1 | SqueezeMetrics, hipóteses 2 e 3: "Call options are sold by investors; bought by market-makers"; "Put options are bought by investors; sold by market-makers" [C]. Perfiliev: "crude approximation", mais discutível em ações [C]. SpotGamma: "a call-positive/put-negative public-data formula is a simplifying inventory convention" [C] |
| B | Formador **vendido em tudo**: o cliente compra calls e puts | −1 | −1 | variante usada por alguns sites [I, sem fonte lida] |
| C | Posição **modelada** do formador | estimada | estimada | SpotGamma usa o "SGOI", proprietário: "modeled position is positive when estimated dealer inventory is long gamma" [C] |
| D (B3) | Heurística pela quebra **coberta / travada / descoberta** do arquivo de OI | $\dfrac{\theta_c\,Cvrd_i+\theta_b\,Blck_i-\theta_u\,Ucvrd_i}{OI_i}$ | idem, com os próprios $\theta$ | [S] Lógica: o **lançador coberto** é tipicamente pessoa física fazendo venda coberta, então a ponta titular tende a ser formador ou institucional (+). O **lançador descoberto** pode ser o próprio formador (−). Padrão proposto: $\theta_c=1$, $\theta_b=0$, $\theta_u=1$. **Não tem fonte**; calibrar comparando com as telas da Jumba |
| E | Formadores identificados por corretora (código de agente na ProfitDLL) e saldo acumulado de negócios por série | do saldo | do saldo | [S] exige a Fita de opções e a lista de formadores credenciados (ver `../../pesquisa/critic.md`) |

**O que a Jumba diz [C]:**
- "Market Gamma mostra a exposição dos Market Makers".
- Gamma positivo "segurou a volatilidade".
- Gamma negativo: "Se entra venda o MM vende junto".

Isso é coerente com qualquer das convenções. **A convenção da Jumba não é pública.** O padrão do motor é **A**, configurável [P].

**Leitura dos sinais (vale para todas as convenções):**
- $\text{GEX}>0$: o hedge do formador é contrário ao movimento (vende na alta, compra na baixa) e amortece a volatilidade.
- $\text{GEX}<0$: o hedge acompanha o movimento e acelera a volatilidade.

## 4. DEX (exposição em delta, candidata ao "Market Exposure")

$$
D^{(1)}_i=s_i\,\Delta_i\,OI_i\,m_i\ \ [\text{unidades do objeto}],\qquad
D^{(R\$)}_i=s_i\,\Delta_i\,OI_i\,m_i\,S\ \ [\text{R\$}]
$$

$$
\text{DEX}(K)=\sum_{i:K_i=K}D^{(R\$)}_i,\qquad \text{DEX}_{tot}=\sum_iD^{(R\$)}_i
$$

- O **hedge** do formador é $-\text{DEX}_{tot}$: na convenção A, ele vende o objeto para neutralizar calls compradas.
- Na convenção A, $\Delta_{put}<0$ e $s=-1$, então as puts também contribuem com sinal positivo para a DEX.
- **Faixa ATM** (para o "Histórico do Market Exposure ATM"): somar só $|K/S-1|\le h$, com $h$ = 2 % ou 5 %. **Em aberto.**

**Exposições de segunda ordem (opcionais) [P]:**

$$
\text{VEX}=\sum_is_i\,\text{Vanna}_i\,OI_i\,m_i\,S\cdot0{,}01\ \ [\text{R\$ de delta por 1 p.p. de vol}]
$$

$$
\text{CEX}=\sum_is_i\,\frac{\text{Charm}_i}{252}\,OI_i\,m_i\,S\ \ [\text{R\$ de delta por DU}]
$$

## 5. Cálculo diário e intradiário [P]

| Item | Foto diária (D) | Recalculado durante o dia |
|---|---|---|
| $OI_i$ | último arquivo B3 publicado (D−1) | fixo durante o dia [C: a B3 publica uma vez por dia] |
| $S$ / $F$ | fechamento | último da ProfitDLL |
| $\sigma_i$ | SVI do fechamento (nota 07) | SVI de D−1 com strike fixo ("sticky strike", padrão) ou reajuste ao vivo |
| $T_i$ | DU/252 | $T(t)$ com fração intradiária (nota 01 §2) |

- **Vencimento do dia:** excluir as séries depois do horário-limite de negociação. Antes dele, usar $T_{\min}$ (nota 01) e marcar `GAMMA_VENCIMENTO`.
- **Somar produtos diferentes** (ações + IND + DOL): só em U3 e em R$.
