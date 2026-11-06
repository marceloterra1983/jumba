# 02. BSM-Merton, com e sem dividendo, e o ajuste de strike por proventos da B3

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - B3, *Manual de Apreçamento – Opções* (20/12/2023), §1.1: <https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf>
  - B3, OC 093/2022-PRE (opções PETR com strike inferior ao provento, 02/08/2022): <https://www.b3.com.br/data/files/84/E4/55/05/A70628103A654428AC094EA8/OC%20093-2022%20PRE%20Tratamento%20das%20Posi%C3%A7%C3%B5es%20de%20Op%C3%A7%C3%B5es%20sobre%20PETR3%20e%20PETR4%20com%20Pre%C3%A7o%20de%20Exerc%C3%ADcio%20Inferior...%20(PT).pdf>
  - B3, OC 141/2023-PRE (dividendos superiores ao strike, Petrobras, 10/08/2023): <https://www.b3.com.br/data/files/44/41/F8/1E/E90E98101D7C7D98DC0D8AA8/OC%20141-2023%20PRE%20Tratamento%20para%20Dividendos%20Superiores%20ao%20Strike_Petrobras%20(PT).pdf>
  - B3, OC 026/2025-VPE (tributação de JCP em futuros e opções a partir de 2026, 30/12/2025): <https://www.b3.com.br/data/files/0F/23/BA/E4/1117B9105B12E5A9AC094EA8/OC%20026-2025-VPE%20ATUALIZACAO%20NA%20TRIBUTACAO%20DE%20JCP%20DE%20CONTRATOS%20FUTUROS%20E%20OPCOES%20A%20PARTIR%20DE%202026_PT.pdf>
  - B3, OC 006/2026-VPE ("Tratamento de eventos corporativos em recursos financeiros líquidos de impostos"). **Não abriu** (erro do site), só o título apareceu na busca: <https://www.b3.com.br/data/files/3D/25/CE/4A/E9EBC910F37907C9AC094EA8/OC%20006-2026-VPE%20TRATAMENTO%20DE%20EVENTOS%20CORPORATIVOS%20EM%20RECURSOS%20FINANCEIROS%20LIQUIDOS%20DE%20IMPOSTOS_PT.pdf>
  - B3, *MPO da Câmara B3* (24/02/2025). Só consegui ler o índice: o item 7.9.1, "Tratamento de eventos corporativos para opções sobre ativos do mercado à vista", fica na p. 186. <https://www.b3.com.br/data/files/CC/F6/D6/2E/8083591029BEEC39AC094EA8/MPO%20da%20Camara%20B3.pdf>
  - B3, CE 017/2025-VPC (equalização do tratamento de proventos em opções flexíveis): <https://www.b3.com.br/data/files/33/E5/9B/96/E87379106B8BCB69AC094EA8/CE%20017-2025-VPC%20PLATAFORMA%20NOME%20EQUALIZACAO%20TRATAMENTO%20PROVENTOS%20OPCOES%20FLEXIVEIS_PT.pdf>
  - Wikipedia, *Greeks (finance)*, fórmulas com dividend yield: <https://en.wikipedia.org/wiki/Greeks_(finance)>
  - Wikipedia, *Black–Scholes equation*: <https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation>
  - Referência original (não aberta): R. C. Merton, "Theory of Rational Option Pricing", *Bell Journal of Economics and Management Science* 4(1), 1973.

## 1. Fórmulas

### 1.1 BSM-Merton com rendimento contínuo $q$

$$
c=S e^{-qT}N(d_1)-K e^{-rT}N(d_2),\qquad
p=K e^{-rT}N(-d_2)-S e^{-qT}N(-d_1)
$$

$$
d_1=\frac{\ln(S/K)+(r-q+\tfrac12\sigma^2)T}{\sigma\sqrt T},\qquad d_2=d_1-\sigma\sqrt T
$$

Paridade: $c-p=Se^{-qT}-Ke^{-rT}$. Forward: $F=Se^{(r-q)T}$.

### 1.2 Black-Scholes sem dividendos (o que a B3 usa para ações, ETFs e índices) [C]

O Manual de Apreçamento (§1.1) escreve, com $r_n=\ln(1+\text{TPreDI1}_n)$ e $T_n=DU_n/252$:

$$
PR_{CALL}=S\,N(d_1)-K e^{-r_nT_n}N(d_2),\qquad
PR_{PUT}=-S\,N(-d_1)+K e^{-r_nT_n}N(-d_2)
$$

$$
d_{1,2}=\frac{\ln(S/K)+(r_n\pm\sigma^2/2)T_n}{\sigma\sqrt{T_n}}
$$

**Não há termo de dividendo.** É o caso $q=0$ da fórmula 1.1. A B3 usa $S$ = fechamento do objeto e $\sigma$ da superfície da B3 (SABR, Corrado-Su, VLFit ou VLGARCH para líquidas; GARCH para ilíquidas).

### 1.3 Dividendo discreto conhecido (modelo "escrowed")

Para um dividendo $D$ com data-ex em $t_{ex}<T$:

$$
S^{*}=S-D\,e^{-r\,t_{ex}},\qquad c=\text{BS}(S^{*},K,r,T,\sigma^{*})
$$

Aqui $\sigma^{*}$ é a vol de $S^{*}$, e não a de $S$. A aproximação usual é $\sigma^{*}\approx\sigma\,S/S^{*}$.

## 2. Como a B3 ajusta o strike por proventos

### 2.1 Regra geral para proventos em dinheiro (dividendos, JCP, rendimentos)

- **Onde está [C]:** a regra fica no MPO da Câmara B3, item 7.9.1, subitem 1, "Eventos corporativos em recursos financeiros". O texto do item não foi lido.
- **Forma do ajuste: dedução do valor do provento do strike [S forte].**
  - Os OC 093/2022 e 141/2023 dizem que, para séries com strike "igual ou inferior ao valor pago", "não [é] possível a aplicação do tratamento previsto no Manual". Por isso adotam o método de fator descrito em 2.2.
  - A única razão para o método do Manual não servir quando $D\ge K$ é que ele **subtrai** $D$ do strike, o que daria strike nulo ou negativo.
  - Daí: $K_{aj}=K-D_{aj}$, aplicado ao final da data-com e vigente na data-ex.
  - **Confirmar** lendo a p. 186 do MPO numa máquina com acesso.
- **Valor do JCP usado [C]:** desde 01/01/2026, a atualização das posições em opções por JCP usa "a alíquota de 17,5 % (0,825)" (OC 026/2025-VPE, que cita a LC 224/2025). Portanto:
  $$D_{aj}^{JCP}=0{,}825\cdot JCP_{bruto}$$
  **Inferência:** antes de 2026 o fator era 0,85, correspondente a 15 %.
- **Dividendos [S]:** até 2025 eram isentos e o ajuste usava o valor cheio. O OC 006/2026-VPE trata de recursos financeiros "líquidos de impostos", o que sugere uma mudança em 2026 para dividendos com retenção. **Não lido; convenção em aberto.**
- **Timing [C para opções flexíveis; I para listadas]:** o CE 017/2025 move o ajuste das flexíveis para "o processamento da última Data Com", para que estejam ajustadas na Data Ex. Os OC 093 e 141 também ajustam "as opções em aberto ao final da data Com".
- **Arredondamento [C nos OC]:** strike ajustado em 2 casas decimais.

### 2.2 Exceção: provento ≥ strike (método de fator) [C]

$$
F=\frac{P_{ex}}{P_{com}},\qquad PE_{aj}=PE\cdot F\ \ (\text{2 casas}),\qquad QTD_{aj}=\left\lfloor\frac{QTD}{F}\right\rfloor
$$

- $P_{ex}$ = preço de abertura do objeto depois do evento; $P_{com}$ = fechamento antes do evento.
- $F$ é arredondado na 8ª casa.
- Há equalização quando as quantidades compradas e vendidas divergem.
- Só se aplica às séries com $K\le D$. As demais seguem o Manual.
- **Consequência para o motor:** nesses eventos, o **multiplicador efetivo muda**, porque a quantidade foi multiplicada por $1/F$. A junção cadastro × OI tem de usar a quantidade ajustada, e o histórico de OI fica descontínuo na data.

### 2.3 Eventos em ativos (desdobramento, grupamento, bonificação) [I]

- Ajuste por fator: strike × fator e quantidade ÷ fator, segundo o mesmo item 7.9.1, que não foi lido.
- O motor não precisa modelar o fator. Ele precisa **usar o strike e a quantidade do cadastro de cada dia** e registrar a mudança (série × data) para o "Histórico de Ajustes de Strikes", comparando `ExrcPric` entre D e D−1 (nota `../b3-opcoes/00-indice.md`).
- **Opção protegida ou não:** o cadastro tem `PrtcnFlg` ("opção protegida contra eventos") e `SrsTpNm` ("tipo de série (correção do strike)"). O motor deve ler esses campos por série.

## 3. Consequência para o modelo: não contar o provento duas vezes

Numa opção **protegida**, o payoff no vencimento é $\max(S_T-(K-D),0)$, e $S_T$ já está ex-dividendo. No modelo escrowed:

$$
c^{prot}=\text{BS}\!\left(S-De^{-rt_{ex}},\;K-D,\;r,\;T,\;\sigma^{*}\right)
$$

O forward líquido fica $F^{*}-K^{*}=Se^{rT}-K-D\left(e^{r(T-t_{ex})}-1\right)$. Ou seja, difere do caso sem dividendo **só pelo carregamento do dividendo entre a data-ex e o vencimento**. Com $\sigma^{*}=\sigma S/S^{*}$, o preço coincide com o Black-Scholes sem dividendos sobre $(S,K)$. Por isso a convenção da B3 (§1.2) é coerente com opções protegidas.

**Vetor numérico** (script `scripts/vetores.py`; S=30, K=32, DU=21, DI=10,65 % a.a., σ=35 %, D=1,00 com data-ex em 10 DU):

| Modelo | Preço da call |
|---|---|
| B3: BS sem dividendo sobre $(S,K)$ | 0,564695 |
| Escrowed protegido $(S^{*},K-D)$ com $\sigma^{*}=\sigma S/S^{*}=36{,}20\,\%$ | 0,564477 (diferença 0,0002 = carregamento) |
| Escrowed protegido com $\sigma^{*}=35\,\%$ | 0,529303 (vol implícita no modelo B3: 33,83 %) |
| **Errado:** dividendo no preço **e** strike sem ajuste $(S^{*},K)$ | 0,313579 |

**Regra do motor [P]:**

1. **Protegida** (`PrtcnFlg` = sim, ou padrão para ações e ETFs listados): BS com $q=0$ sobre o strike vigente no cadastro. É o mesmo modelo da B3. A vol implícita sai comparável com a do Prêmio de Referência.
2. **Não protegida, ou índice à vista:** BSM-Merton com $q$, ou Black-76 com o futuro como forward (nota 03).
3. **Modo "escrow" opcional:** para gregas perto da data-ex em proventos grandes (≥ 3 % de $S$), quando o usuário quiser separar o salto do objeto.

**Atenção na data-ex [S]:** entre o anúncio e o ajuste no cadastro, o strike ainda não mudou. No modelo da regra 1 nada muda, porque o efeito se cancela. Mas no histórico de vol implícita, comparar a série antes e depois do ajuste mistura strikes diferentes. Para comparar, use moneyness $K/F$ ou delta.

## 4. Exercício antecipado [I]

- As calls de ações na B3 são, em geral, **americanas**, e as puts são, em geral, **europeias**. Confirmar por série em `OptnStyle`.
- Com o strike protegido, o titular da call não perde o dividendo ao esperar. Com $r>0$, o exercício antecipado da call raramente é ótimo, então tratar a call americana como europeia é aproximação aceitável.
- **Exceções [S]:**
  - JCP: o ajuste usa o valor líquido (0,825), mas o titular que exerce antes da data-com recebe o JCP líquido do mesmo jeito. Diferença esperada pequena.
  - Fator (§2.2) e eventos com $D\ge K$.
- **Puts americanas**, se houver: o modelo europeu subestima o preço. Use árvore binomial (Cox-Ross-Rubinstein) ou Barone-Adesi-Whaley [P].

## 5. Relação gamma-theta (usada na nota 13)

A equação de Black-Scholes em termos das gregas (Wikipedia), com $q$, é:

$$
\Theta+\tfrac12\sigma^2S^2\Gamma+(r-q)S\Delta-rV=0
$$

Numa carteira delta-hedgeada, "a perda por theta e o ganho do termo gamma se compensam".
