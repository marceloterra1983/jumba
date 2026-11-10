# Metodologia do motor de opções: índice e convenções em aberto

- **Data:** 2026-11-04 (acesso a todas as fontes citadas nas notas).
- **Pasta:** `docs/conhecimento/metodologia/`
- **Base lida antes:**
  - `../../pesquisa/` (fontes-dados, jumba-pro, jumba-trader-fyt, matrix, critic);
  - `../b3-opcoes/` (cadastro, OI, Prêmio de Referência);
  - `../jumba-publico/` (glossário e buscas no Telegram).
- **Regra de fontes do dono:** B3 primeiro; ProfitDLL só para preço ao vivo, book e DI1 intradiário. A DLL não tem gregas nem strike. Nenhum login.
- **Legenda:** [C] confirmado na fonte citada · [I] inferência · [S] suposição a testar · [P] proposta de convenção.
- **Acesso às fontes:** todos os documentos B3 foram lidos via WebFetch, que devolve texto processado. Nada foi baixado como binário nem executado. Em alguns PDFs, os símbolos matemáticos se perderam na extração; a nota avisa quando isso acontece.

## Notas

| # | Arquivo | Assunto |
|---|---|---|
| 01 | [01-convencoes-base.md](01-convencoes-base.md) | Notação, Black-Scholes generalizado com custo de carregamento $b$, tempo DU/252, $r=\ln(1+DI)$, cupom cambial, multiplicadores, preço de entrada, precisão |
| 02 | [02-bsm-merton-proventos.md](02-bsm-merton-proventos.md) | BSM-Merton com e sem dividendo; BS sem dividendos da B3; modelo escrowed; **ajuste de strike por proventos na B3** (dedução, JCP × 0,825 em 2026, fator quando provento ≥ strike); exercício antecipado |
| 03 | [03-black76-futuros.md](03-black76-futuros.md) | Black-76 para opções sobre IND e DOL futuro; IBOV à vista via futuro; forward pela paridade; GEX com $F^2$ |
| 04 | [04-garman-kohlhagen-dolar.md](04-garman-kohlhagen-dolar.md) | Garman-Kohlhagen da B3 para dólar à vista; equivalência com Black-76 sobre o DOL do mesmo vencimento |
| 05 | [05-gregas-escalas.md](05-gregas-escalas.md) | Δ, Γ, ν, Θ, ρ, vanna, charm e vomma no modelo generalizado; rho por modelo; escalas (Γ 1 %, cash gamma, ν/100, Θ/252 ou Θ/365, ρ por p.p. de DI); vetores de teste |
| 06 | [06-vol-implicita.md](06-vol-implicita.md) | Limites de arbitragem, Newton (chutes de Manaster-Koehler e Brenner-Subrahmanyam), Brent, Jäckel; qual preço inverter; americanas |
| 07 | [07-svi-nt-2013-01.md](07-svi-nt-2013-01.md) | SVI raw (Gatheral-Jacquier), forma da B3 em variância, **NT-2013-01** (mínimos quadrados e Levenberg-Marquardt, calendário, interpolação), condições g(k) ≥ 0 e asas, SSVI, procedimento proposto |
| 08 | [08-gex-dex.md](08-gex-dex.md) | GEX em 3 unidades (SqueezeMetrics em ações; SpotGamma e Perfiliev em $S^2\times0{,}01$), por strike e total; **5 convenções de sinal** (A a E, incluindo a heurística coberta/descoberta da B3); DEX, VEX e CEX; intradiário |
| 09 | [09-gamma-flip-walls.md](09-gamma-flip-walls.md) | Perfil $\mathcal G(X)$; flip por varredura e por acumulado; call wall e put wall (3 regras); Jumba Walls e MidWalls; mínimo e máximo do perfil; Bands |
| 10 | [10-max-pain.md](10-max-pain.md) | Max Pain pelo método A (intrínseco × OI) e B (contagem ITM); condição de primeira ordem (mediana ponderada); vetor de teste; History |
| 11 | [11-pcr.md](11-pcr.md) | PCR por OI, volume e financeiro, mais variantes (descoberto, delta); a Cboe publica por volume |
| 12 | [12-indice-qualidade.md](12-indice-qualidade.md) | IQ = titulares ÷ lançadores (Clube do Pai Rico); agregações; barreiras (descoberto > 5 mi e IQ > 1,2); dependência de `BrrwrQty`/`LndrQty` |
| 13 | [13-bgt-move.md](13-bgt-move.md) | **Hipótese** BGT = $\sqrt{2\lvert\Theta\rvert/\Gamma}$; com r = 0, igual a $S\sigma\sqrt{\delta t}$; versão agregada com vol ponderada por gamma |
| 14 | [14-taxa-estruturas-cdi.md](14-taxa-estruturas-cdi.md) | Venda coberta, cash put, box de 3 e 4 pontas, collar; anualização base 252; duas definições de "% do CDI"; proventos e americanas |
| — | [especificacao-motor.md](especificacao-motor.md) | **Lista de funções** com entradas, saídas e unidades; tipos de dados; `Config` com padrões; vetores de teste; mapa tela → função |
| — | `scripts/vetores.py`, `scripts/check_charm.py` | Geram os vetores de teste. Só biblioteca padrão; rodar com `python3 -I` |

## Convenções que ficam em aberto (decisão do Marcelo ou validação na conta Jumba, só olhando)

### Dados e regras da B3

1. **Regra geral de ajuste por provento em dinheiro.** A dedução $K-D$ é inferência forte, porque o método de fator só existe quando $D\ge K$. Falta ler o MPO da Câmara B3, item 7.9.1, p. 186.
2. **Dividendo em 2026.** O ajuste usa o valor bruto ou o líquido de IR? O OC 006/2026-VPE não abriu. O JCP usa 0,825 desde 01/01/2026 [C].
3. **Contagem de DU** (`WrkgDays` inclui hoje?) e horário-limite para a fração intradiária.
4. **Multiplicadores:** IBOV (a página B3 diz R$ 0,01/ponto), IND opção (R$ 1/ponto?), opções sobre futuro de dólar (listadas?). Também `PrmUpfrntInd`, que decide se Black-76 desconta.
5. **Quais opções a Jumba usa em "Índice Futuro" e "Dólar":** sobre o futuro ou sobre o à vista. Isso decide entre Black-76 e GK/IBOV e a fonte do OI.
6. **Titulares e lançadores:** se `BrrwrQty`/`LndrQty` trazem as contagens. Sem isso, o IQ não tem fonte.

### Modelagem

7. **Modelo para ações:** BS sem dividendos (padrão B3, coerente com strike protegido) ou escrow perto da data-ex.
8. **Preço para inverter a vol:** mid, último ou Prêmio de Referência; limite de spread.
9. **SVI:** pesos (1, vega ou 1/spread²); mínimo de pontos; tratamento de arbitragem. Para ações, a B3 usa SABR, Corrado-Su, VLFit e VLGARCH, não SVI.

### Exposições e níveis

10. **Sinal da GEX/DEX:** A (calls +, puts −; padrão de mercado), B (tudo −), D (heurística coberta/descoberta) ou E (corretoras). **A Jumba não publica a dela.**
11. **Unidade da GEX:** ações por R$ 1, R$ por R$ 1, ou R$ por 1 % ($S^2\times0{,}01$); e se a Jumba soma vencimentos.
12. **Gamma flip:** varredura de preço (SpotGamma/Perfiliev) ou acumulado por strike; vol com strike fixo ou moneyness fixa.
13. **Walls:**
    - regra: gamma nocional, OI ou GEX com sinal;
    - se há restrição de lado;
    - quantas walls;
    - se MidWall é o ponto médio.
14. **Mínimo e máximo do Market Gamma e Bands:** perfil $\mathcal G(X)$ ou por strike; por vencimento ou agregado.
15. **Faixa ATM** do Histórico do Market Exposure (2 % ou 5 %), e se "Market Exposure" é DEX ou GEX.

### Métricas de OI

16. **Max Pain:** método A ou B; por vencimento ou agregado.
17. **PCR:** OI, volume ou financeiro; quais vencimentos; como agregar o "mercado".
18. **IQ do ativo e IQ Global:** razão de somas ou média ponderada.
19. **BGT:** confirmar que é gamma-theta e com qual horizonte (1 DU ou até o vencimento). Pode ser outra coisa.

### Estruturas

20. **% do CDI:**
    - razão de retornos ou estilo CDB;
    - CDI de referência: curva DI1 no vértice ou DI do dia;
    - capital do cash put: $K-P$ ou $K$;
    - custos e IR (tributação do box como renda fixa a confirmar).
21. **Theta exibido** por dia útil (Θ/252) ou por dia corrido (Θ/365).
