# 01. Convenções de base: notação, tempo, taxa, unidades e multiplicadores

- **Data de acesso das fontes:** 2026-11-04.
- **Legenda:** **[C]** confirmado na fonte citada; **[I]** inferência minha; **[S]** suposição a testar com dado real; **[P]** proposta de convenção para o motor (decisão do Marcelo).
- **Fontes:**
  - B3, *Manual de Apreçamento – Opções* (20/12/2023): <https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf>
  - B3, *Programa de treinamento DI – 02 Taxas de juros*: <https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/juros/programa-de-treinamento-di/02-taxas-de-juros.htm>
  - B3, *Options on U.S. Dollar Spot*: <https://b3.com.br/en_us/products-and-services/trading/exchange-rates/options-on-u-s-dollar-spot.htm>
  - B3, *Options on Ibovespa*: <https://b3.com.br/en_us/products-and-services/trading/equities/options-on-ibovespa.htm>
  - Glossário InstrumentsConsolidatedFile, resumido em `../b3-opcoes/01-cadastro-instrumentos.md`: <https://b3.com.br/data/files/52/74/1E/14/4BA6D8103152D4C8AC094EA8/Glossario%20InstrumentsConsolidatedFile%202024.pdf>

## 1. Notação usada em todas as notas

| Símbolo | Significado | Unidade |
|---|---|---|
| $S$ | preço do ativo-objeto à vista (ação, ETF, índice, dólar) | R$ (ou pontos) |
| $F$ | preço do futuro ou forward com o mesmo vencimento da opção | R$ ou pontos |
| $K$ | preço de exercício (strike) **vigente no cadastro do dia** | mesma unidade de $S$ |
| $T$ | prazo até o vencimento da opção | anos (ver §2) |
| $r$ | taxa pré contínua equivalente à taxa DI do prazo | ao ano, contínua |
| $q$ | rendimento contínuo do ativo (dividend yield ou cupom cambial) | ao ano, contínua |
| $b$ | custo de carregamento ("cost of carry"): $b=r-q$ | ao ano, contínua |
| $\sigma$ | volatilidade implícita | ao ano (fração; 0,35 = 35 %) |
| $N(\cdot)$, $\varphi(\cdot)$ | distribuição acumulada e densidade da normal padrão | — |
| $OI_i$ | posições em aberto da série $i$ (`OpnIntrst`) | contratos/opções |
| $m_i$ | multiplicador: unidades do objeto por contrato | ver §4 |
| $s_i$ | sinal atribuído à posição dos formadores de mercado na série $i$ | $\{-1,0,+1\}$ ou peso |

O motor usa uma única família de fórmulas, o **Black-Scholes generalizado** com custo de carregamento $b$. A nota 05 deriva as gregas dela:

$$
d_1=\frac{\ln(S/K)+\left(b+\tfrac12\sigma^2\right)T}{\sigma\sqrt T},\qquad d_2=d_1-\sigma\sqrt T
$$

$$
c=S\,e^{(b-r)T}N(d_1)-K\,e^{-rT}N(d_2),\qquad p=K\,e^{-rT}N(-d_2)-S\,e^{(b-r)T}N(-d_1)
$$

| Modelo | $b$ | Uso no motor | Nota |
|---|---|---|---|
| Black-Scholes sem dividendos (convenção B3 para ações) | $b=r$ | opções de ações e ETFs protegidas contra proventos | 02 |
| BSM-Merton com rendimento contínuo $q$ | $b=r-q$ | índice à vista, opções não protegidas | 02 |
| Black-76 | $b=0$, com $S\to F$ | opções sobre futuro (IND, DOL futuro) | 03 |
| Garman-Kohlhagen | $b=r_d-r_f$ | opção sobre dólar à vista | 04 |

## 2. Tempo

- **Convenção da B3 [C]:** $T_n = DU_n/252$ (dias úteis), tanto para ações quanto para dólar (Manual de Apreçamento, seções 1.1 e 2.1). O cupom cambial usa dias corridos com base 360 (§3).
- **Contagem de DU [S]:** o cadastro traz `WrkgDays`, descrito como "dias úteis até o vencimento (inclusive)", e `ClnrDays` (dias corridos). Antes de adotar o campo, é preciso testar se a B3 conta o pregão de hoje. Sem o campo, conta-se com o calendário B3 de feriados (no Farol, `B3Holidays`/`OptionExpiry.cs`).
- **Fração intradiária [P]:** o manual da B3 calcula no fechamento. Para recalcular durante o dia, a proposta é
  $$T(t)=\frac{DU_{\text{restantes após hoje}}+f(t)}{252},\qquad f(t)=\frac{\text{tempo restante do pregão de hoje}}{\text{duração do pregão}}$$
  No dia do vencimento, $f(t)$ vai até o horário-limite de negociação da série. O glossário da Jumba cita 15h45, ou 16h45 nas séries de dezembro (`../jumba-publico/glossario-jumba.md`).
- **Piso [P]:** $T_{\min}=1/(252\cdot 390)$, cerca de um minuto de pregão, para evitar divisão por zero no último minuto.

## 3. Taxa de juros e cupom cambial

- **Taxa pré [C]:** $r_n=\ln(1+\text{TPreDI1}_n)$, em que $\text{TPreDI1}_n$ é a taxa DI ao ano (base 252), obtida por **interpolação exponencial** dos ajustes do DI1 até o vértice $DU_n$ (Manual de Apreçamento, §1.1). Assim:
  $$e^{-r_nT_n}=(1+\text{TPreDI1}_n)^{-DU_n/252}$$
- **Interpolação exponencial [I]:** entre dois vértices $(DU_1,i_1)$ e $(DU_2,i_2)$, ela equivale ao *flat forward* 252:
  $$(1+i)^{DU/252}=(1+i_1)^{DU_1/252}\left[\frac{(1+i_2)^{DU_2/252}}{(1+i_1)^{DU_1/252}}\right]^{\frac{DU-DU_1}{DU_2-DU_1}}$$
- **Fator do período e taxa diária [C, convenção 252]:**
  $$FP=(1+i)^{du/252},\qquad i_d=(1+i)^{1/252}-1$$
- **Cupom cambial [C]:** $q_n=\frac{252}{DU_n}\ln\!\left(1+\text{TPreDDI}_n\cdot\frac{DC_n}{360}\right)$ (Manual de Apreçamento, §2.1).
- **Fonte da curva:** arquivo TS da B3 ou BVBG.086 no fechamento; DI1 pela ProfitDLL durante o dia. Ver `../../pesquisa/fontes-dados.md`.

## 4. Multiplicadores e unidades (sempre ler do cadastro)

**Regra [P]:** o motor não fixa multiplicador no código. Ele usa `CtrctMltplr` e `AsstQtnQty` do cadastro (BVBG.028 ou InstrumentsConsolidated) e só cai nos valores da tabela abaixo se o campo vier vazio, registrando aviso.

| Produto | Cotação do prêmio | Multiplicador $m$ (R$ por ponto de prêmio) | Status |
|---|---|---|---|
| Opção de ação ou ETF | R$ por ação | 1 (OI e volume em quantidade de opções; 1 opção = 1 ação) | [I] convenção de mercado; confirmar com `CtrctMltplr` |
| Opção sobre Ibovespa à vista (IBOV) | pontos de índice | a página B3 em inglês diz "BRL 0.01 per index point" | [C] literal da página; **conferir**, porque diverge do R$ 1/ponto do IND |
| Opção sobre futuro de Ibovespa (IND) | pontos | R$ 1 por ponto | [S] |
| Opção sobre dólar à vista (DOL) | R$ por US$ 1.000 | contrato de US$ 50.000 → $m=50$ | [C] tamanho e cotação; [I] $m$ |
| Opção sobre futuro de dólar | R$ por US$ 1.000 | 50 (cheio) ou 10 (mini) | [S] não confirmei se está listada hoje |

**Consequência para exposições:** a GEX e a DEX de produtos diferentes só se somam depois de convertidas para R$ (nota 08).

## 5. Preço de entrada de cada cálculo [P]

| Uso | Preço da opção | Preço do objeto |
|---|---|---|
| Vol implícita intradiária | meio do book $(bid+ask)/2$ se o spread relativo for ≤ 20 % do meio e houver as duas pontas; senão, o último negócio dos últimos 15 min; senão, nada | último ou meio do objeto **no mesmo instante** |
| Vol implícita diária (foto) | Prêmio de Referência B3 (todas as séries) ou fechamento do BVBG.086 | fechamento do objeto |
| Taxas de estruturas (FYT) | executável: compra no **ask**, venda no **bid** | ask para compra do objeto |
| Gregas e exposições | vol da curva SVI ajustada (nota 07) | último do objeto |

## 6. Precisão numérica [P]

- Use `double` em tudo. $N(x)$ deve ter precisão de máquina (por exemplo, `erfc`), e não a aproximação polinomial de 7 casas.
- Arredondar só na exibição. A B3 arredonda strike ajustado em 2 casas e o fator de ajuste em 8 casas (nota 02).
