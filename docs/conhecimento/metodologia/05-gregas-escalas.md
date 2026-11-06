# 05. Gregas e as escalas usuais de exibição

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - Wikipedia, *Greeks (finance)*, seção "Formulae for European option Greeks" e notas de escala (vega e rho por 1 ponto percentual; theta dividido pelo número de dias do ano): <https://en.wikipedia.org/wiki/Greeks_(finance)>
  - SpotGamma, *Gamma Exposure (GEX)*: "Per-$1 and per-1% figures are not interchangeable". <https://spotgamma.com/gamma-exposure-gex/>
  - B3, *Manual de Apreçamento – Opções* (base DU/252): <https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf>

## 1. Gregas do Black-Scholes generalizado (custo de carregamento $b$)

Notação da nota 01. $\Theta$ é a derivada no tempo calendário, $\Theta=\partial V/\partial t=-\partial V/\partial T$.

Abreviações:

$$e_b\equiv e^{(b-r)T},\qquad e_r\equiv e^{-rT}$$

| Grega | Call | Put |
|---|---|---|
| $\Delta=\partial V/\partial S$ | $e_b\,N(d_1)$ | $-e_b\,N(-d_1)$ |
| $\Gamma=\partial^2V/\partial S^2$ | $\dfrac{e_b\,\varphi(d_1)}{S\sigma\sqrt T}$ | idem |
| $\nu=\partial V/\partial\sigma$ | $S\,e_b\,\varphi(d_1)\sqrt T$ | idem |
| $\Theta$ | $-\dfrac{S e_b\varphi(d_1)\sigma}{2\sqrt T}-(b-r)S e_b N(d_1)-rK e_r N(d_2)$ | $-\dfrac{S e_b\varphi(d_1)\sigma}{2\sqrt T}+(b-r)S e_b N(-d_1)+rK e_r N(-d_2)$ |
| Vanna $=\partial\Delta/\partial\sigma$ | $-e_b\,\varphi(d_1)\,d_2/\sigma$ | idem |
| Charm $=\partial\Delta/\partial t$ | $-e_b\left[(b-r)N(d_1)+\varphi(d_1)\left(\frac{b}{\sigma\sqrt T}-\frac{d_2}{2T}\right)\right]$ | $-e_b\left[-(b-r)N(-d_1)+\varphi(d_1)\left(\frac{b}{\sigma\sqrt T}-\frac{d_2}{2T}\right)\right]$ |
| Vomma $=\partial\nu/\partial\sigma$ | $\nu\,d_1d_2/\sigma$ | idem |

**Rho depende do modelo**, porque muda o que se move junto com $r$:

| Modelo | $\rho_{call}$ | $\rho_{put}$ |
|---|---|---|
| Ações, $b=r$ (ou $b=r-q$ com $q$ fixo) | $TKe^{-rT}N(d_2)$ | $-TKe^{-rT}N(-d_2)$ |
| Black-76, $b=0$, $F$ fixo | $-T\,c$ | $-T\,p$ |
| GK, taxa doméstica $r_d$ | $TKe^{-r_dT}N(d_2)$ | $-TKe^{-r_dT}N(-d_2)$ |
| GK, taxa estrangeira $r_f$ | $-TSe^{-r_fT}N(d_1)$ | $TSe^{-r_fT}N(-d_1)$ |

Com $b=r-q$, as fórmulas reproduzem as da Wikipedia para BSM-Merton: $\Delta_c=e^{-qT}N(d_1)$ e $\Theta_c=-\frac{Se^{-qT}\varphi(d_1)\sigma}{2\sqrt T}-rKe^{-rT}N(d_2)+qSe^{-qT}N(d_1)$.

## 2. Escalas de exibição

| Grega | Unidade natural | Escalas usuais | Recomendação do motor [P] |
|---|---|---|---|
| Δ | objeto por opção | Δ × 100 ("delta 30"); **delta financeiro** $\Delta\cdot S\cdot m\cdot q$ em R$ | guardar Δ cru; exibir Δ×100 e o financeiro |
| Γ | 1/R$ (variação de Δ por R$ 1) | **Γ 1 %** $=\Gamma S\cdot0{,}01$ (variação de Δ num movimento de 1 %); **cash gamma** $=\Gamma S^2\cdot0{,}01$ (R$ de delta por 1 %, base da GEX); **P&L de 1 %** $=\tfrac12\Gamma(0{,}01S)^2$ | guardar Γ cru; exibir Γ 1 % por opção e cash gamma por posição |
| ν | R$ por 1,00 de vol (100 p.p.) | **ν/100** = R$ por 1 p.p. de vol [C Wikipedia] | exibir ν/100 |
| Θ | R$ por ano | **Θ/252 por dia útil** (coerente com $T=DU/252$); Θ/365 por dia corrido (padrão americano) [C: "dividido pelo número de dias do ano"; a escolha 252 ou 365 varia] | exibir Θ/252; opcionalmente o theta de 1 DU exato $V(T-\tfrac1{252})-V(T)$ |
| ρ | R$ por 1,00 de taxa contínua | **ρ/100** = R$ por 1 p.p. [C] | ρ por 1 p.p. da **taxa DI a.a.**: $\rho_{DI}=\rho/[100\,(1+DI)]$, porque $dr/dDI=1/(1+DI)$ quando $r=\ln(1+DI)$ [I] |
| Vanna | 1/vol | por 1 p.p.: vanna/100 | idem |
| Charm | Δ por ano | por DU: charm/252 | idem |

**Consequência da base DU [I]:** com $T=DU/252$, sábado, domingo e feriado não consomem tempo no modelo. Isso é coerente com a B3, mas difere do theta "por dia corrido" dos sites americanos. Por isso a escala precisa aparecer no rótulo da tela.

## 3. Vetores de teste

Script `scripts/vetores.py`; tolerância 1e-6. BS sem dividendo (convenção B3): S=30, K=32, DU=21 (T=0,083333), DI=10,65 % a.a. ($r=\ln 1{,}1065=0{,}101203$), σ=35 %.

| Saída | Call | Put |
|---|---|---|
| $d_1$; $d_2$ | −0,504778; −0,605814 | idem |
| Preço | 0,564695 | 2,295958 |
| Δ | 0,306858 | −0,693142 |
| Γ | 0,115873 | 0,115873 |
| ν (por 1,00) | 3,041666 | 3,041666 |
| Θ (por ano) | −7,261986 | −4,050723 |
| ρ (por 1,00) | 0,720086 | −1,924186 |
| ν/100 | 0,030417 | 0,030417 |
| Θ/252 | −0,028817 | −0,016074 |
| Θ/365 | −0,019896 | −0,011098 |
| ρ/100 | 0,007201 | −0,019242 |
| Γ 1 % | 0,034762 | 0,034762 |
| cash gamma $\Gamma S^2\cdot0{,}01$ | 1,042857 | 1,042857 |
| P&L de 1 % | 0,005214 | 0,005214 |

Paridade: $c-p=-1{,}73126311=S-Ke^{-rT}$.

Os vetores de Black-76 e GK estão nas notas 03 e 04.
