# 03. Black-76: opções sobre futuro (IND, DOL futuro) e índice à vista via futuro

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - B3, *Manual de Apreçamento – Opções* (20/12/2023). Na §4.1 (commodities), a fórmula tem a forma de Black sobre o futuro; na §6.1, $A$ é o ajuste do futuro de índice ou de dólar: <https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf>
  - Wikipedia, *Black model*: <https://en.wikipedia.org/wiki/Black_model>
  - Original (não aberto): F. Black, "The pricing of commodity contracts", *Journal of Financial Economics* 3(1–2):167–179, 1976, doi:10.1016/0304-405X(76)90024-6.
  - B3, *Options on Ibovespa*: <https://b3.com.br/en_us/products-and-services/trading/equities/options-on-ibovespa.htm>
  - Glossário do cadastro (campo `PrmUpfrntInd`), resumido em `../b3-opcoes/01-cadastro-instrumentos.md`.

## 1. Fórmula

Para uma opção europeia sobre um futuro de preço $F$, com prêmio pago à vista:

$$
c=e^{-rT}\left[F\,N(d_1)-K\,N(d_2)\right],\qquad
p=e^{-rT}\left[K\,N(-d_2)-F\,N(-d_1)\right]
$$

$$
d_1=\frac{\ln(F/K)+\tfrac12\sigma^2T}{\sigma\sqrt T},\qquad d_2=d_1-\sigma\sqrt T
$$

É o Black-Scholes generalizado com $b=0$ e $S\to F$ (nota 01). Paridade: $c-p=e^{-rT}(F-K)$.

A B3 escreve a mesma forma para commodities (§4.1) [C]:

$$PRC_{CALL}=e^{-rT}\left(F\,N(d_1)-K\,N(d_2)\right)$$

**Prêmio com margem ("futures-style") [S]:** se o prêmio não for pago à vista, não há desconto: $c=F N(d_1)-K N(d_2)$. O cadastro tem o campo `PrmUpfrntInd` ("prêmio pago à vista"). O motor deve descontar só quando ele indicar pagamento à vista [P].

## 2. Gregas de Black-76 (em relação a $F$)

$$
\Delta_c=e^{-rT}N(d_1),\quad \Delta_p=-e^{-rT}N(-d_1),\quad
\Gamma=\frac{e^{-rT}\varphi(d_1)}{F\sigma\sqrt T},\quad
\nu=F e^{-rT}\varphi(d_1)\sqrt T
$$

$$
\Theta_c=-\frac{F e^{-rT}\varphi(d_1)\sigma}{2\sqrt T}+r\,c,\qquad
\Theta_p=-\frac{F e^{-rT}\varphi(d_1)\sigma}{2\sqrt T}+r\,p,\qquad
\rho_{c}=-T\,c,\ \ \rho_p=-T\,p
$$

O $\rho$ acima mede só o efeito do desconto, com $F$ fixo.

**Delta em relação ao à vista [I]:** se o objeto de hedge for o futuro, use o delta em $F$. Para converter para o equivalente à vista: $\Delta_S=\Delta_F\cdot\partial F/\partial S=\Delta_F\,e^{bT_F}$, em que $T_F$ é o prazo do futuro.

## 3. Aplicação aos produtos da B3

| Produto | Modelo | $F$ | $T$ e desconto | Status |
|---|---|---|---|---|
| Opção sobre futuro de Ibovespa (IND) | Black-76 | IND do mesmo vencimento: último ou meio do book (DLL) durante o dia; ajuste no fechamento | $T=DU/252$ até o vencimento da opção; $r$ da curva DI | [S] listagem e estilo a confirmar no cadastro |
| Opção sobre Ibovespa à vista (IBOV, europeia) | Black-76 com $F$ = futuro do mesmo vencimento | o Manual §6.1 usa como $A$ o "preço de ajuste do futuro de índice com o mesmo vencimento" [C] | idem | [C] europeia |
| Opção sobre futuro de dólar | Black-76 | DOL do vencimento | idem | [S] confirmar se está listada |
| Opção sobre dólar à vista | GK, ou Black-76 com o DOL do mesmo vencimento (nota 04) | DOL | idem | [C] europeia |

**Vencimentos sem futuro casado [P]:** opções de IBOV mensais vencem em meses ímpares, quando não há IND. Nesses casos:

1. **Forward implícito pela paridade**, no strike mais perto do dinheiro, com as duas pontas executáveis:
   $$F^{impl}=K+e^{rT}(c-p)$$
   Use a mediana de 3 strikes perto do dinheiro.
2. **Interpolação** do custo de carregamento entre os futuros vizinhos:
   $$F(T)=S\exp\{b(T)\,T\},\quad b(T)\ \text{linear em } T$$
   entre os $b$ implícitos dos dois IND mais próximos.

## 4. GEX com Black-76

Na fórmula de GEX da nota 08, troca-se $S$ por $F$:

$$\text{GEX}_i=s_i\,\Gamma_i\,OI_i\,m_i\,F^2\cdot 0{,}01$$

O resultado é em R$ de delta por movimento de 1 % no futuro.

**Vetor numérico** (F=130.000, K=132.000, DU=15, σ=20 %, DI=10,65 %):

| Série | Preço (pts) | Δ | Γ | GEX por contrato com $m=1$ |
|---|---|---|---|---|
| call | 1.663,57 | 0,3842 | 6,0×10⁻⁵ | R$ 10.134 por 1 % |
| put | 3.651,56 | −0,6098 | 6,0×10⁻⁵ | R$ 10.134 por 1 % |

Leitura: num movimento de 1 % (1.300 pts), o delta de uma call muda 0,078. Isso equivale a 0,078 × 130.000 × R$ 1 = R$ 10.134 de exposição. Para mini (WIN, R$ 0,20/pt), multiplique por 0,2.

## 5. Pendências

- Confirmar no cadastro quais opções a Jumba mostra em "Índice Futuro" e "Dólar": opção sobre futuro ou sobre à vista (ver `../../pesquisa/critic.md`, item IND/DOL).
- Confirmar `PrmUpfrntInd` e `ExrcStyle` nas opções sobre futuro.
- Confirmar o multiplicador do IBOV: a página da B3 diz R$ 0,01 por ponto.
