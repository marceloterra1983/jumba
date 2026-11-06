# 10. Max Pain (dois métodos) e Max Pain History

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - Option Alpha, *Max Pain Options*:
    - passos: "Calculate the intrinsic value for in-the-money calls and puts" → "Multiply each contract's intrinsic value by its open interest" → "Add the call and put values together for each strike price";
    - o exemplo escolhe o strike de **menor** total ("results in the lowest total intrinsic value");
    - a definição fala em "the maximum number of options would expire worthless".
    - URL: <https://optionalpha.com/learn/max-pain-options>
    - **Atenção:** o passo 4 da página diz "highest value", o que contradiz o exemplo; parece erro de redação.
  - Jumba: "Max Pain do IBOV deslocou" e Max Pain no Payoff, sem definição pública (`../jumba-publico/telegram-busca-maxpain-bgt.md`).

## 1. Notação

Para um ativo e **um** vencimento $T$: calls com strikes $k_c$ e $OI_c$, puts com strikes $k_p$ e $OI_p$, e multiplicador $m$. O preço hipotético de liquidação é $X$, avaliado nos strikes listados $\mathcal K$. Strikes vigentes no cadastro, ou seja, já ajustados.

## 2. Método A: menor valor intrínseco pago aos titulares (padrão)

$$
\text{Dor}(X)=m\left[\sum_cOI_c\,(X-k_c)^+ +\sum_pOI_p\,(k_p-X)^+\right],\qquad
\text{MaxPain}_A=\arg\min_{X\in\mathcal K}\text{Dor}(X)
$$

- **A grade de strikes é exata [I]:** $\text{Dor}(X)$ é convexa e linear por partes, com quebras só nos strikes. O mínimo em $\mathbb R$ cai sempre num strike, então avaliar só em $\mathcal K$ não perde nada.
- **Algoritmo rápido** pela condição de primeira ordem, em O(n log n). As derivadas laterais são
  $$
  \text{Dor}'_-(X)=m\Big[\sum_{k_c<X}OI_c-\sum_{k_p\ge X}OI_p\Big],\qquad
  \text{Dor}'_+(X)=m\Big[\sum_{k_c\le X}OI_c-\sum_{k_p>X}OI_p\Big]
  $$
  O Max Pain é o strike com $\text{Dor}'_-\le0\le\text{Dor}'_+$: o ponto em que **o OI acumulado de calls abaixo** alcança **o OI acumulado de puts acima**. É uma mediana ponderada. Implementação: ordenar os strikes, fazer as somas acumuladas e uma varredura.
- **Incluir o prêmio pago não muda o resultado [I]:** subtrair o prêmio histórico de cada série soma uma constante $-\sum OI\cdot\text{prêmio}$, e o argmin fica igual. Logo, "P&L líquido dos titulares" **não** é um terceiro método.

## 3. Método B: maior número de contratos que viram pó (menor contagem de ITM)

$$
\text{ITM}(X)=\sum_cOI_c\,\mathbb 1[X>k_c]+\sum_pOI_p\,\mathbb 1[X<k_p],\qquad
\text{MaxPain}_B=\arg\min_{X\in\mathcal K}\text{ITM}(X)
$$

- Corresponde à frase "the maximum number of options would expire worthless" [C].
- É uma função em degraus. O mínimo pode ser um intervalo; nesse caso, escolher o strike do intervalo mais próximo de $S$ [P].
- Convenção para $X=k$: ATM não conta como ITM [P].

## 4. Vetor de teste

Script `scripts/vetores.py`. Calls: {28: 1.000, 30: 5.000, 32: 8.000, 34: 3.000}. Puts: {26: 2.000, 28: 6.000, 30: 4.000, 32: 1.000}. $m=1$.

| $X$ | Dor (R$) | ITM (contratos) | $\text{Dor}'_-$ | $\text{Dor}'_+$ |
|---|---|---|---|---|
| 26 | 34.000 | 11.000 | −13.000 | −11.000 |
| 28 | 12.000 | 5.000 | −11.000 | −4.000 |
| **30** | **4.000** | **2.000** | **−4.000** | **5.000** |
| 32 | 14.000 | 6.000 | 5.000 | 14.000 |
| 34 | 42.000 | 14.000 | 14.000 | 17.000 |

Os dois métodos dão Max Pain = 30. A condição de primeira ordem também troca de sinal em 30.

## 5. Regras de dados [P]

- Um cálculo por (ativo, data de vencimento). As séries semanais têm vencimento próprio.
- **Agregado de todos os vencimentos:** opcional; em aberto se a Jumba faz.
- Usar o OI do arquivo B3 mais recente e o strike do cadastro do mesmo pregão.
- Séries com $OI=0$ são ignoradas.
- **Empate:** strike mais próximo de $S$.
- **Saídas:** `max_pain_a`, `max_pain_b`, `dor[X]`, `itm[X]`, `distancia_pct=(MaxPain/S-1)`.

## 6. Max Pain History

Uma linha por (data, ativo, vencimento) com `max_pain_a`, `max_pain_b`, $S$ de fechamento e, no vencimento, o preço de liquidação.

**Só existe se a foto diária de OI for gravada todo dia**: o BDI guarda cerca de 21 pregões (ver `../../pesquisa/fontes-dados.md`).
