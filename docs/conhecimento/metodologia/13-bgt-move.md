# 13. "BGT Move": hipótese de deslocamento de equilíbrio gamma-theta

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Status:** **hipótese**. A sigla BGT não é explicada em nenhuma fonte pública da Jumba.
- **Fontes:**
  - Jumba, mensagem 1812 do Telegram: no Payoff do FYT (beta), "Mínimo, máximo e Flip do Market Gamma", "BGT" e Max Pain aparecem como "informações do Jumba Pro". Ver `../jumba-publico/telegram-busca-maxpain-bgt.md` e `glossario-jumba.md`.
  - **Leitura [I]:** BGT aparece ao lado de níveis de preço, então é um nível ou um par de níveis.
  - Wikipedia, *Black–Scholes equation*: $\Theta+\tfrac12\sigma^2S^2\Gamma+rS\Delta=rV$; "the loss from theta and the gain from the gamma term must offset each other". <https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation>
  - Wikipedia, *Greeks (finance)*: <https://en.wikipedia.org/wiki/Greeks_(finance)>

## 1. Derivação

Uma posição em opção delta-hedgeada, num intervalo $\delta t$ com movimento $\delta S$, tem P&L de primeira ordem em $t$ e segunda em $S$ (desprezando vega e juros):

$$\delta\Pi\approx\Theta\,\delta t+\tfrac12\Gamma\,(\delta S)^2$$

O **movimento de equilíbrio** (breakeven) é aquele em que o ganho de gamma paga o theta do período:

$$
\boxed{\ \delta S^{*}=\sqrt{\frac{2\,|\Theta_{\delta t}|}{|\Gamma|}}\ },\qquad \Theta_{\delta t}=\Theta\cdot\delta t
$$

Exige que $\Gamma$ e $\Theta_{\delta t}$ tenham sinais opostos, o normal para opções sozinhas. Em carteiras pode não acontecer.

**Caso BS com $r=q=0$ [I, decorre da EDP]:** $\Theta=-\tfrac12\sigma^2S^2\Gamma$, então

$$\delta S^{*}=S\,\sigma\sqrt{\delta t}$$

Para $\delta t=1/252$, o BGT Move é **o movimento de 1 desvio-padrão diário implícito**.

**Vetor numérico** (S=K=100, T=30/252, σ=30 %, Θ por DU = Θ/252):

| Taxa | $\sqrt{2\lvert\Theta_{1DU}\rvert/\Gamma}$ | $S\sigma/\sqrt{252}$ |
|---|---|---|
| $r=0$ | 1,889822 | 1,889822 |
| $r=\ln1{,}1065$ | 2,160880 | 1,889822 |

Com juros, o theta inclui o carregamento, e o BGT fica maior que o 1σ diário.

## 2. Versão agregada (nível de mercado) [P]

Com o sinal $s_i$ dos formadores (nota 08):

$$
\Gamma_{tot}=\sum_is_i\Gamma_iOI_im_i,\qquad
\Theta_{tot}=\sum_is_i\frac{\Theta_i}{252}OI_im_i\ \ (\text{por DU})
$$

$$
\text{BGT}=\sqrt{\frac{2|\Theta_{tot}|}{|\Gamma_{tot}|}}\quad\text{(só se }\Gamma_{tot}\Theta_{tot}<0\text{)},\qquad
\text{Bandas BGT}=S\pm\text{BGT}
$$

Com $r\approx0$, isso equivale a $S\,\bar\sigma/\sqrt{252}$, em que

$$\bar\sigma^2=\frac{\sum_iw_i\sigma_i^2}{\sum_iw_i},\qquad w_i=s_i\Gamma_iOI_im_iS^2$$

é uma **vol média ponderada pelo gamma** [I].

**Horizonte:** para $h$ pregões, use $\delta t=h/252$, supondo $\Gamma$ e $\Theta$ constantes. Em aberto qual horizonte a Jumba usaria: 1 dia ou até o vencimento.

## 3. Outras leituras possíveis da sigla [S]

1. "Breakeven Gamma-Theta" ou "Bandas Gamma-Theta" (a hipótese acima).
2. Bandas por theta e gamma por strike: o strike em que $|\Theta|$ agregado é máximo.
3. Outra métrica proprietária sem relação com gregas.

**Validação:** abrir o Payoff do FYT na conta do Marcelo, só observando e sem copiar dados.
- Comparar o valor de BGT com $S\pm S\sigma_{ATM}/\sqrt{252}$ e com a versão agregada.
- Ver se o valor muda durante o dia e com o vencimento escolhido.

## 4. Saídas

`bgt_move` (R$ ou pontos), `bgt_pct=bgt_move/S`, `banda_inf`, `banda_sup`, `gamma_tot`, `theta_tot_du`, `sigma_efetiva`, flag `SINAIS_IGUAIS` quando $\Gamma_{tot}\Theta_{tot}\ge0$.
