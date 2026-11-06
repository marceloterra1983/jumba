# 04. Garman-Kohlhagen: opção sobre dólar à vista (DOL disponível)

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - B3, *Manual de Apreçamento – Opções* (20/12/2023), §2.1 a 2.3 e §6.1: <https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf>
  - B3, *Options on U.S. Dollar Spot*: <https://b3.com.br/en_us/products-and-services/trading/exchange-rates/options-on-u-s-dollar-spot.htm>
  - Wikipedia, *Foreign exchange option* (modelo de Garman-Kohlhagen): <https://en.wikipedia.org/wiki/Foreign_exchange_option>
  - Original (não aberto): M. B. Garman e S. W. Kohlhagen, "Foreign currency option values", *Journal of International Money and Finance* 2(3):231–237, 1983.

## 1. Especificação do contrato [C]

- **Objeto:** taxa de câmbio R$/US$ à vista. Ticker DOL. Europeia.
- **Tamanho:** US$ 50.000. Prêmio cotado em R$ por US$ 1.000, com 3 casas. Lote-padrão: 5 contratos.
- **Vencimento:** 1º dia útil do mês do contrato. Último dia de negociação: o pregão anterior.
- **Exercício:** automático no vencimento, se o preço de liquidação for favorável ao titular.
- **Preço de liquidação:** a PTAX800 de venda (Banco Central) entra no prêmio de referência do último dia e do vencimento, por valor intrínseco (Manual, eq. 2.7 e 2.8).

## 2. Fórmula da B3 [C]

$$
PR_{CALL}=S e^{-q_nT_n}N(d_1)-K e^{-r_nT_n}N(d_2),\qquad
PR_{PUT}=-S e^{-q_nT_n}N(-d_1)+K e^{-r_nT_n}N(-d_2)
$$

$$
d_{1,2}=\frac{\ln(S/K)+(r_n-q_n\pm\tfrac12\sigma^2)T_n}{\sigma\sqrt{T_n}},\qquad T_n=\frac{DU_n}{252}
$$

$$
r_n=\ln(1+\text{TPreDI1}_n),\qquad
q_n=\frac{252}{DU_n}\ln\!\left(1+\text{TPreDDI}_n\frac{DC_n}{360}\right)
$$

- $S$ é o **"dólar cupom limpo"**, não a PTAX.
- $q_n$ é o cupom cambial (DDI/FRC), convertido para taxa contínua na base 252.
- É o Black-Scholes generalizado com $b=r_d-r_f$ (nota 01), com $r_d=r_n$ e $r_f=q_n$.

## 3. Forma equivalente por Black-76 (recomendada para o motor) [P]

Pela paridade coberta de juros, $F=S\,e^{(r_n-q_n)T_n}$. Substituindo:

$$c^{GK}=e^{-r_nT_n}\left[F N(d_1)-K N(d_2)\right]=c^{Black76}(F)$$

Vetor numérico (S=5,40; K=5,50; DU=20; DC=28; DI=10,65 %; cupom=5 % linear/360; σ=14 %):

| Saída | Valor |
|---|---|
| $q_n$ | $\tfrac{252}{20}\ln(1+0{,}05\cdot 28/360)=0{,}048905$ |
| $F$ | 5,42246 |
| call GK | 0,052240 R$/US$ (= 52,240 R$ por US$ 1.000) |
| call Black-76 com $F$ | 0,05224031 (idêntico) |
| put GK | 0,129160 |
| Δ call, Γ | 0,365402; 1,760939 |

**Por que preferir Black-76 sobre o DOL do mesmo vencimento [P]:**

1. O DOL e a opção sobre o à vista vencem no mesmo dia, o 1º dia útil do mês.
2. O Manual da B3 usa o próprio ajuste do DOL como $A$ na conversão delta → strike (§6.1).
3. Evita montar o "dólar cupom limpo" e a curva de cupom.
4. O DOL e o WDO chegam em tempo real pela ProfitDLL.

Quando não houver DOL casado, o motor recai em GK com $S$ e o cupom da curva DDI/FRC, ou interpola $F$.

## 4. Unidades

- **Prêmio:** se as contas forem feitas em R$/US$ (S = 5,40), multiplique por 1.000 para cotar em R$ por US$ 1.000, e por 50.000 para chegar ao valor do contrato.
- **Recomendação [P]:** trabalhe com $S$ e $F$ em R$/US$ e $m=50.000$ (US$ por contrato). Assim, $\Gamma$ fica por R$ 1 de variação no câmbio. A GEX por 1 % (nota 08) é $\Gamma\cdot OI\cdot 50.000\cdot S^2\cdot 0{,}01$, em R$.

## 5. Volatilidade do dólar na B3 [C]

A B3 ajusta o smile do dólar comercial por SVI em variância, em função de $x=\ln(K/F_n)$ (Manual §2.2), e corrige a vol (§2.3). Ver nota 07.
