# 11. Put/Call Ratio (PCR) por OI, por volume e por financeiro

- **Data de acesso das fontes:** 2026-11-04. Legenda: [C] confirmado, [I] inferência, [S] a testar, [P] proposta.
- **Fontes:**
  - Cboe, *Daily Market Statistics*. Publica "TOTAL", "INDEX", "EXCHANGE TRADED PRODUCTS", "EQUITY" e "VIX PUT/CALL RATIO". Os números batem com **volume de puts ÷ volume de calls**, não com OI (total 5.168.990 / 6.034.465 ≈ 0,86; o OI daria 0,75). <https://www.cboe.com/us/options/market_statistics/daily/>
  - Jumba: o PCR "demonstra o sentimento dos investidores, se estão buscando mais ou menos proteção via opções de venda", com leitura contrária na euforia. **Não diz se é OI ou volume.** Ver `../jumba-publico/telegram-busca-pcr.md`.
  - B3: OI por série (`OpnIntrst`) e volume por série (BVBG.086 ou NEG). Ver `../b3-opcoes/00-indice.md`.

## 1. Fórmulas

Para um ativo e um conjunto de vencimentos $\mathcal V$:

$$
\text{PCR}_{OI}=\frac{\sum_{p\in\mathcal V}OI_p}{\sum_{c\in\mathcal V}OI_c},\qquad
\text{PCR}_{vol}=\frac{\sum_{p}Q_p}{\sum_{c}Q_c},\qquad
\text{PCR}_{fin}=\frac{\sum_{p}\sum_{n}P_{p,n}Q_{p,n}}{\sum_{c}\sum_{n}P_{c,n}Q_{c,n}}
$$

- $Q$ = quantidade negociada no dia, em opções (ações) ou contratos.
- $P_{\cdot,n}Q_{\cdot,n}$ = financeiro negócio a negócio. No arquivo diário, use o volume financeiro (`NtlFinVol`) [S, confirmar o campo].

**Variantes opcionais [P]:**
- **Só a parte descoberta:** $\text{PCR}_{desc}=\sum UcvrdQty_p/\sum UcvrdQty_c$. Isola os lançadores com margem.
- **Ponderado por delta:** $\sum|\Delta_p|OI_p\big/\sum\Delta_cOI_c$.
- **Faixa de moneyness:** só séries com $|K/S-1|\le h$.

## 2. Regras [P]

- **Padrão:** PCR por OI (foto diária) e PCR por volume (diário e intradiário).
- **Recortes:** por vencimento e "todos". Cada um vira uma série temporal com média móvel de 5 e 20 pregões.
- **Unidades:** numerador e denominador na mesma unidade (quantidade de opções); o multiplicador se cancela.
- **Denominador zero:** `NaN` com flag `SEM_CALLS`.
- **Intradiário:** $Q$ acumulado desde a abertura, a partir dos negócios da ProfitDLL (assinatura limitada às séries do universo) [S].
- **Histórico de volume antes da gravação própria:** COTAHIST (sem OI) [C fontes-dados].

## 3. Em aberto

- Qual PCR a Jumba mostra: OI, volume ou financeiro, e sobre quais vencimentos.
- Se o PCR "do mercado" agrega todos os ativos, somando quantidades, ou se é uma média dos PCRs.
