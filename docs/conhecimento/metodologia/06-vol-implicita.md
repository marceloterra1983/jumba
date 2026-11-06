# 06. Volatilidade implícita: Newton-Raphson, Brent e salvaguardas

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - Wikipedia, *Implied volatility*, seção de métodos numéricos (Newton com vega analítica, Brent e Jäckel "Let's be rational"): <https://en.wikipedia.org/wiki/Implied_volatility>
  - Wikipedia, *Brent's method*: <https://en.wikipedia.org/wiki/Brent%27s_method>
  - P. Jäckel, "Let's be rational", *Wilmott Magazine* 2015(75):40–53, doi:10.1002/wilm.10395. Implementação de referência livre, empacotada em Python como `lets_be_rational`/`py_vollib`: <https://libraries.io/pypi/lets_be_rational>
  - B3, *Manual de Apreçamento – Opções*, §1.2.3 (inversão de BS) e §1.2.2.6 (médias e incertezas intradiárias): <https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf>
  - B3, Prêmio de Referência (vol implícita B3 publicada para ações, ETFs e índice desde 14/12/2016), resumido em `../b3-opcoes/05-premio-referencia.md`.
  - Referências clássicas para chute inicial (não abertas): S. Manaster e G. Koehler, *Journal of Finance* 37(1), 1982; M. Brenner e M. Subrahmanyam, *Financial Analysts Journal* 44(5), 1988.

## 1. Problema

Achar $\sigma^{*}$ tal que

$$f(\sigma)=V(\sigma;S\text{ ou }F,K,T,r,b)-P^{mkt}=0$$

$V$ é crescente em $\sigma$ (porque $\nu>0$), então a raiz é única quando existe.

## 2. Limites de não-arbitragem (checar antes de iterar)

$$
\max\!\left(0,\;Se^{(b-r)T}-Ke^{-rT}\right)<c<Se^{(b-r)T},\qquad
\max\!\left(0,\;Ke^{-rT}-Se^{(b-r)T}\right)<p<Ke^{-rT}
$$

Fora desses limites não há vol implícita. O motor devolve `NaN` e a flag `FORA_DOS_LIMITES` [P].

Muito perto do limite inferior (opção muito fora do dinheiro, preço de 0,01), a vol é mal condicionada. Flag `PRECO_MINIMO` quando $P^{mkt}\le$ 2 ticks [P].

## 3. Newton-Raphson

$$\sigma_{n+1}=\sigma_n-\frac{V(\sigma_n)-P^{mkt}}{\nu(\sigma_n)}$$

Converge de forma quadrática perto da raiz. Precisa da vega, que é analítica (nota 05).

**Chutes iniciais:**
- Manaster-Koehler, que garante convergência monotônica para BS europeu:
  $$\sigma_0=\sqrt{\frac{2}{T}\left|\ln\frac{S}{K}+bT\right|}$$
  com fallback para 0,3 se der zero.
- Brenner-Subrahmanyam, perto do dinheiro:
  $$\sigma_0\approx\sqrt{\frac{2\pi}{T}}\,\frac{c}{S}$$

**Salvaguardas [P]:**
- Se $\nu<10^{-8}$, ou se o passo sair de $[\sigma_{\min},\sigma_{\max}]=[0{,}001;\,5{,}0]$, troque para Brent.
- Critério de parada: $|f|<10^{-10}\cdot\max(1,P)$ ou $|\Delta\sigma|<10^{-8}$; no máximo 50 iterações.

**Vetor:** com S=30, K=32, DU=21, DI=10,65 % e preço 0,564695, Newton parte de $\sigma_0=0{,}30$ e chega a σ=0,350000 em 4 iterações. Para a put (2,295958), também em 4.

## 4. Brent (Brent-Dekker)

- Combina bisseção, secante e interpolação quadrática inversa.
- Exige um intervalo com troca de sinal, $f(a)f(b)<0$. Usar $[0{,}001;\,5{,}0]$.
- **Convergência garantida:** no pior caso, o quadrado do número de iterações da bisseção. Para funções bem comportadas, é superlinear.
- **Uso no motor [P]:** fallback do Newton, ou método único quando a robustez importa mais que a velocidade (por exemplo, foto diária de toda a grade).

## 5. Jäckel "Let's be rational" (padrão-ouro)

Usa um chute por expansões assintóticas e dois passos de Householder de 4ª ordem. Chega à precisão de máquina em todo o domínio [C Wikipedia].

**Recomendação [P]:** se a dependência for aceita, use `py_vollib`/`lets_be_rational` como referência de teste. Rode Newton+Brent próprio em produção e compare os dois numa grade de 10⁴ pontos.

## 6. Qual preço inverter [P]

| Situação | Preço | Observação |
|---|---|---|
| Intradiário | meio do book, se as duas pontas existem e o spread ≤ 20 % do meio | objeto no mesmo instante (book da DLL) |
| Sem book válido | último negócio se ocorreu há ≤ 15 min; senão, não calcular | — |
| Foto diária | Prêmio de Referência B3; se faltar, o fechamento do BVBG.086 | o Prêmio cobre séries sem negócio [C] |
| Smile | **só opções fora do dinheiro**: puts com $K<F$ e calls com $K>F$; perto do ATM, média das duas | evita o prêmio de exercício antecipado e o spread largo das ITM [I] |

**A B3 também ajusta a vol por incertezas [C]:** a consolidação intradiária usa médias e incertezas das opções (§1.2.2.6). Na nossa curva SVI, isso vira peso (nota 07).

## 7. Americanas [I]

- Calls de ações protegidas: tratar como europeias (nota 02 §4).
- Puts americanas: inverter um modelo europeu superestima a vol. Use binomial com 200 passos ou BAW, e marque a série com `AMERICANA_APROX`.

## 8. Saídas por série

Saídas: `iv`, `metodo` (newton, brent ou jäckel), `iteracoes`, `preco_usado`, `fonte_preco` (mid, last, premio_ref ou fechamento), `flags`.
