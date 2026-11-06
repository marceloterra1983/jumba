# 09. Gamma flip, call wall, put wall e demais níveis do perfil de gamma

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - SpotGamma, *Gamma Exposure (GEX)*: "Zero Gamma is the modeled spot price where aggregate GEX crosses zero", recalculado "over a range of hypothetical spot prices". <https://spotgamma.com/gamma-exposure-gex/>
  - SpotGamma Support, *Gamma Flip*: <https://support.spotgamma.com/hc/en-us/articles/15413261162387-Gamma-Flip>
  - SpotGamma, *Call Wall / Put Wall explained*: "The call wall is the strike with the largest concentration of call gamma; the put wall is its counterpart on the put side". <https://spotgamma.com/call-wall-put-wall-explained/>
  - S. Perfiliev, thread sobre zero gamma (recalcular o Γ de cada opção em cada nível de spot e achar onde a curva cruza zero): <https://threadreaderapp.com/thread/1489373524066279430.html>
  - Jumba, frases públicas: Flip, Put/Call Gamma Wall, Mínimo e Máximo do Market Gamma, Bands, Walls e MidWalls. Ver `../jumba-publico/glossario-jumba.md`, `telegram-busca-flip.md`, `telegram-busca-bands.md` e `telegram-busca-walls.md`.

## 1. Perfil de gamma em função de um preço hipotético $X$

$$
\mathcal G(X)=\sum_{i\in\mathcal V}s_i\,\Gamma_i\!\left(X;K_i,T_i,\sigma_i\right)\,OI_i\,m_i\,X^2\cdot0{,}01
$$

Os Γ **têm de ser recalculados** em cada $X$, porque mudam com o spot (Perfiliev [C]).

Convenções do perfil [P]:
- **Vol:** $\sigma_i$ fixo por série, com strike fixo ("sticky strike", padrão). Alternativa: $\sigma_i=\sigma^{SVI}(\ln(K_i/F(X)))$, com moneyness fixa.
- **Taxa e prazo:** $r$ e $T_i$ fixos no instante do cálculo.
- **Grade:** $X\in[0{,}7S;\,1{,}3S]$ com passo de 0,25 % de $S$; para IND e DOL, $[0{,}9F;\,1{,}1F]$ com passo de 0,1 %.

## 2. Gamma flip (zero gamma)

**Método 1: varredura de preço [C SpotGamma e Perfiliev]**
1. Calcular $\mathcal G(X)$ na grade.
2. Achar os intervalos $[X_j,X_{j+1}]$ com troca de sinal.
3. Refinar cada raiz com Brent (nota 06 §4).
4. Se houver várias raízes, reportar **a mais próxima de $S$** como flip principal e listar as demais [P].
5. Se não houver troca de sinal na grade, reportar `SEM_FLIP` e o sinal do regime.

$$X_{flip}:\ \mathcal G(X_{flip})=0$$

**Método 2: acumulado por strike [I, alternativa comum em sites de varejo]**

Com os strikes em ordem crescente e $\text{GEX}(K)$ calculado **no spot atual** (nota 08 §2):

$$C(K_j)=\sum_{K\le K_j}\text{GEX}(K)$$

O flip é o $K$ em que $C$ troca de sinal, com interpolação linear entre os dois strikes vizinhos.

- **Não é equivalente ao método 1:** aqui os Γ não são recalculados, e o resultado depende de onde começa a soma.
- Variante: o strike mais próximo de $S$ em que o próprio $\text{GEX}(K)$ troca de sinal.

**O que a Jumba diz [C]:**
- O flip é o "ponto de transição entre o gamma positivo e negativo", onde a curva cruza zero.
- É expresso em preço do ativo ou pontos do IBOV.
- Perto do vencimento, "os formadores acabam levando o papel para esse ponto".

**Qual método ela usa é desconhecido. Em aberto.**

**Regime [P]:** `POSITIVO` se $\mathcal G(S)>0$; `NEGATIVO` se $<0$; `PERTO_DO_FLIP` se $|S-X_{flip}|/S\le0{,}5\,\%$.

## 3. Call wall e put wall

**Definição SpotGamma [C]:** o strike com maior concentração de gamma de calls, e o equivalente nas puts. Com o gamma nocional sem sinal:

$$
K_{CW}=\arg\max_K\sum_{i\in\text{calls}:K_i=K}\Gamma_iOI_im_iS^2\cdot0{,}01,\qquad
K_{PW}=\arg\max_K\sum_{i\in\text{puts}:K_i=K}\Gamma_iOI_im_iS^2\cdot0{,}01
$$

**Alternativas [C: "the strikes with the largest open interest or largest gamma", citadas e criticadas pela SpotGamma]:**
- (b) maior $OI$ de calls e maior $OI$ de puts;
- (c) maior $\text{GEX}(K)$ positivo e mais negativo, com sinal.

**Restrição de lado [P, em aberto]:** procurar a call wall só em $K\ge S$ e a put wall só em $K\le S$, ou sem restrição, como a SpotGamma.

**Jumba [C]:** cita "Put Gamma Wall" e "Call Gamma Wall" ao lado do Flip (IBOV 104,8k / 116,9k / 123,3k), o que é coerente com a definição da SpotGamma [I].

## 4. Jumba Walls e MidWalls (várias linhas por pregão)

**O que a Jumba diz [C]:**
- Walls são "regiões onde os Market Makers travam o risco", "nos pontos de maior probabilidade de delta hedge".
- Saem "antes mesmo da abertura do pregão".
- Existem para IND, DOL e ações.
- As MidWalls são as "linhas pontilhadas" entre as Walls.

**Proposta [P]:**
1. Usar o perfil $|\text{GEX}(K)|$ por strike, no fechamento de D−1, com OI de D−1.
2. Walls = os **máximos locais** de $|\text{GEX}(K)|$, ordenados por tamanho. Ficam os $N$ maiores dentro de $\pm x\%$ de $S$, com padrão $N=3$ de cada lado e $x=5\,\%$ (ações) ou $2\,\%$ (IND e DOL).
3. MidWall entre duas Walls vizinhas: $(W_j+W_{j+1})/2$ [I].
4. Ficam fixas durante o pregão [C].

## 5. Mínimo e máximo do Market Gamma e Gamma Bands

**O que a Jumba diz [C]:**
- "Mínimo, máximo e Flip do Market Gamma" são níveis de preço; por exemplo, CYRE3 "atingiu o mínimo do Market Gamma (R$ 18,22)".
- As Bands mostram o "histórico do máximo do gamma (linha verde) e o mínimo do gamma (linha vermelha)".
- "O preço do ativo raramente rompe essas linhas."

**Fórmula provável [I]:**

$$
X_{\max}=\arg\max_X\mathcal G(X),\qquad X_{\min}=\arg\min_X\mathcal G(X)
$$

na grade de §1, ou o mesmo sobre $\text{GEX}(K)$ por strike. **Em aberto:** se é o perfil $\mathcal G(X)$ ou o perfil por strike, e se é por vencimento ("dentro de um exercício" [C]) ou agregado.

**Gamma Bands [I]:** a série diária de $(X_{\min},X_{\max})$ por ativo e por vencimento, gravada na foto diária e desenhada sobre o preço.

## 6. Saídas

Por ativo, por instante e por filtro de vencimentos: `flip_m1`, `flip_m2`, `raizes[]`, `regime`, `call_wall`, `put_wall` (e suas variantes b e c), `walls[]`, `midwalls[]`, `x_max`, `x_min`, `gex_spot`, `perfil[X]`.
