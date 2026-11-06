# 14. Taxa contra o CDI: venda coberta, cash put, box de 3 e 4 pontas, collar

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - B3, *Programa de treinamento DI – Taxas de juros* (base 252: "capitalização ocorre apenas em dias úteis"; notação du/252): <https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/juros/programa-de-treinamento-di/02-taxas-de-juros.htm>
  - B3, OC 032-2026 (prorrogação do incentivo tarifário para Box 3 Pontas em opções de ações e ETFs). Achado na pesquisa anterior, **PDF não abriu**: <https://www.b3.com.br/data/files/1E/F5/53/51/9C3BF91094DCD8F9AC094EA8/OC%20032-2026%20PRE%20PRORROGACAO%20DO%20PROGRAMA%20DE%20INCENTIVO%20TARIFARIO%20PARA%20OPERACOES%20DE%20BOX%203%20PONTAS%20EM%20OPCOES%20DE%20ACOES%20E%20ETFS%20(PT).pdf>
  - Jumba FYT: buscadores de Venda Coberta, Box de 3 e 4 Pontas e Collar; "Rolagem" com valor negativo = crédito. Ver `../jumba-publico/site-jumba-fyt.md` e `glossario-jumba.md`.
  - Fórmulas da pesquisa anterior: `../../pesquisa/jumba-trader-fyt.md`.
  - Ajuste de strike por proventos: nota 02 §2.

## 1. Convenções comuns [P]

- **Preço executável:** compra no **ask** e venda no **bid**, do objeto e das opções. Opcional: meio do book, marcado como "teórico".
- **Prazo:** $DU$ = dias úteis de D+0 até o vencimento da opção, contados como na nota 01. O financeiro das opções liquida em D+1 e o da ação em D+2 [I]; o padrão é ignorar essa defasagem, com ajuste opcional.
- **Taxa do período → ao ano (base 252):**
  $$r_{aa}=(1+r_{per})^{252/DU}-1$$
- **CDI de comparação:** a taxa pré da curva DI1 no vértice $DU$ (nota 01 §3), que é o "CDI esperado até o vencimento". Alternativa: a taxa DI do dia (`CDI_hoje`), constante.
  $$\text{CDI}_{per}=(1+\text{DI}_{aa})^{DU/252}-1$$
- **"% do CDI" em duas convenções, em aberto:**
  - Razão de retornos do período:
    $$\%CDI^{(1)}=\frac{r_{per}}{\text{CDI}_{per}}$$
  - Estilo CDB, em que $p$ multiplica o DI diário:
    $$\%CDI^{(2)}=\frac{(1+r_{per})^{1/DU}-1}{(1+\text{DI}_{aa})^{1/252}-1}$$
- **Spread:** $r_{aa}-\text{DI}_{aa}$, em pontos percentuais ao ano.
- **Custos opcionais:** corretagem, emolumentos e taxas B3, aplicados na montagem e no exercício. **IR:** fora do padrão. A tributação do box como renda fixa precisa ser confirmada [I].
- **Proventos durante a vida da estrutura [I]:**
  - Numa opção protegida, o strike cai $D$ e o detentor da ação recebe $D$. Nas estruturas com ação comprada (venda coberta, box 3, collar), o total no vencimento fica igual, com $K_{orig}=K_{aj}+D$, salvo tributação.
  - JCP: o ajuste usa o líquido (0,825 desde 2026), igual ao que o acionista pessoa física recebe.
  - Quando o ajuste é por fator (provento ≥ strike), recalcule a estrutura com quantidades e strikes novos.

## 2. Venda coberta (compra da ação + venda de call $K$)

| Métrica | Fórmula |
|---|---|
| Capital | $I=S_{ask}-C_{bid}$ |
| Valor extrínseco | $VE=C_{bid}-\max(S-K,0)$ |
| **Taxa "se o preço ficar parado"** (padrão de mercado para a "taxa da venda coberta" [I]) | $r_{per}=VE/I$ |
| Taxa máxima (se exercida) | $r^{\max}_{per}=K/I-1$ |
| Proteção | $C_{bid}/S$; breakeven $=I$ |
| Payoff no vencimento | $\min(S_T,K)-I$ |

Quando $K\ge S$ (OTM), as duas taxas fecham em $r_{per}=C/I$ (parado) e $K/I-1$ (exercida). Quando $K<S$ (ITM), $VE/I=K/I-1$, ou seja, a taxa é travada.

**Exercício antecipado [I]:** a call é americana. Se for exercida antes, recebe-se $K$ antes do vencimento e a taxa anualizada aumenta.

## 3. Cash put (venda de put $K$ com garantia em caixa no CDI)

| Métrica | Fórmula |
|---|---|
| Capital | $I=K-P_{bid}$ (padrão [P]) ou $I=K$ (alternativa) |
| Taxa do prêmio (não exercida) | $r_{per}=P_{bid}/(K-P_{bid})$ (ou $P_{bid}/K$) |
| Taxa total com a garantia aplicada | $r^{tot}_{per}=r_{per}+\text{CDI}_{per}$ (aproximado) ou $\dfrac{K(1+\text{CDI}_{per})+P_{bid}(1+\text{CDI}_{per})}{K}-1$ (capital $K$) |
| Preço efetivo de compra se exercida | $K-P_{bid}$ |
| Valor extrínseco (puts ITM) | $VE=P_{bid}-\max(K-S,0)$; "taxa parada" $=VE/I$ |

**Em aberto:** qual capital a Jumba usa e se ela soma o CDI da garantia.

## 4. Box de 3 pontas (ação + compra de put $K$ + venda de call $K$, mesmo vencimento)

$$
I=S_{ask}+P_{ask}(K)-C_{bid}(K),\qquad \text{payoff}=K\ (\text{fixo}),\qquad r_{per}=\frac{K}{I}-1
$$

**Vetor:** S=30,00, K=30, P_ask=1,20, C_bid=1,65, DU=21, DI=10,65 % a.a.

| Saída | Valor |
|---|---|
| $I$ | 29,55 |
| $r_{per}$ | 1,5228 % |
| $r_{aa}$ | 19,89 % |
| $\%CDI^{(1)}$ | 179,8 % |
| $\%CDI^{(2)}$ | 179,2 % |

**Riscos e observações:**
- A call é **americana** [I]. Exercício antecipado entrega a ação e recebe $K$ antes, sobrando a put longa com valor ≥ 0. Não há perda, mas a taxa muda.
- Liquidez: as três pernas precisam ser executadas.
- Há incentivo tarifário B3 específico para Box 3 Pontas (OC 032-2026, não lido) [C pelo título].

## 5. Box de 4 pontas (trava de alta com calls + trava de baixa com puts, $K_1<K_2$)

$$
I=C_{ask}(K_1)-C_{bid}(K_2)+P_{ask}(K_2)-P_{bid}(K_1),\qquad \text{payoff}=K_2-K_1,\qquad r_{per}=\frac{K_2-K_1}{I}-1
$$

- **Captação (vender o box):** recebe $I'=C_{bid}(K_1)-C_{ask}(K_2)+P_{bid}(K_2)-P_{ask}(K_1)$ e paga $K_2-K_1$. O custo é $r_{per}=(K_2-K_1)/I'-1$.
- **Taxa implícita contínua:** $r=\ln\big((K_2-K_1)/I\big)/T$. Pela paridade, um box sem atrito vale $(K_2-K_1)e^{-rT}$.
- **Riscos [I]:**
  - As calls americanas vendidas ($K_2$) podem ser exercidas antes.
  - Proventos ajustam os dois strikes. Por subtração, $K_2-K_1$ não muda. Pelo fator, $(K_2-K_1)F$ muda, mas a quantidade escala por $1/F$, e o nocional fica igual.

## 6. Collar (Long Collar: ação + compra de put $K_1$ + venda de call $K_2$, com $K_1\le K_2$)

$$
I=S_{ask}+P_{ask}(K_1)-C_{bid}(K_2),\qquad \text{payoff}=\min\!\big(\max(S_T,K_1),K_2\big)
$$

| Métrica | Fórmula |
|---|---|
| Taxa mínima (piso) | $r^{\min}_{per}=K_1/I-1$ |
| Taxa máxima (teto) | $r^{\max}_{per}=K_2/I-1$ |
| Taxa "parado" | $\min(\max(S,K_1),K_2)/I-1$ |
| Perda máxima | $I-K_1$ |
| Ganho máximo | $K_2-I$ |
| Custo zero | quando $P_{ask}(K_1)=C_{bid}(K_2)$ |

O box de 3 pontas é o collar com $K_1=K_2$.

## 7. Saídas por estrutura (para o scanner "Todas as Estruturas")

`pernas[]` (ticker, lado, preço usado, quantidade), `capital`, `payoff_min`, `payoff_max`, `breakevens[]`, `r_per`, `r_aa`, `pct_cdi_1`, `pct_cdi_2`, `spread_aa`, `du`, `flags` (`AMERICANA_VENDIDA`, `SEM_BOOK`, `PROVENTO_NO_PRAZO`).
