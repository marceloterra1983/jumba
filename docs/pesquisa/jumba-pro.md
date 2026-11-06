# Pesquisa pública: as telas do "Jumba Pro" (o que mostram, fórmula provável, dados de entrada)

## 0. O que deu para levantar e o que não deu

**Fontes públicas consultadas, todas sem login:**
- Páginas do site: [jumba.com.br](https://jumba.com.br), [/produtos](https://jumba.com.br/produtos), [/jumba-pro](https://jumba.com.br/jumba-pro), [/quem-somos](https://jumba.com.br/quem-somos), [/jumba-trader](https://jumba.com.br/jumba-trader), [/jumba-trader-flow](https://jumba.com.br/jumba-trader-flow) e [/tradingview](https://jumba.com.br/tradingview).
- Hotmart: combo [Pro+Trader](https://hotmart.com/pt-br/marketplace/produtos/jumba-pro-jumba-trader-combo/Q90970656B) e combo [Pro+FYT](https://hotmart.com/pt-br/marketplace/produtos/jumba-pro-find-your-trade-combo/T86010315Q).
- YouTube: [Market Gamma – O Gráfico dos Formadores de Mercado](https://www.youtube.com/watch?v=k4mC3y7EhhE) (14/04/2023) e [Jumba Walls – Lançamento](https://www.youtube.com/watch?v=sd8YYjLHb0o) (04/10/2022).
- Telegram: [t.me/s/mapadeopcoes](https://t.me/s/mapadeopcoes).
- Clube do Pai Rico: posts sobre o IQ, que não são do Jumba.
- B3: páginas de Consultas e de UP2DATA.

**O que não consegui ler:**
- Todas as páginas de `pages.jumba.com.br/*` deram erro de servidor, incluindo market-gamma-jumba-pro, jumba-pro, trader-flow e jumbaclass-os-segredos-do-market-gamma.
- Também falharam: `lp.somosnomos.com.br/jumba-nomos`, telemetr.io, o feed RSS do YouTube (bloqueado por robots) e a consulta de posições em aberto da B3.
- As páginas de ferramenta, como `/pro/market-gamma` e `/shark-map`, só mostram a tela de login.

**Conclusão geral:** o Jumba não publica metodologia. Só aparecem nomes e descrições de marketing. O site **não cita nenhuma das telas a seguir**: BGT Bands, Gamma Score, Resumo do Gamma, Market Exposure, Max Pain, Histórico de Ajustes e Curva de Juros. Para essas telas, tudo abaixo é **inferência** baseada no conceito de mercado equivalente.

**Fatos confirmados que servem de base:**
- O Jumba Pro é "baseado na movimentação dos grandes investidores que operam na B3" (Hotmart).
- O Mapa de Opções mostra "posições cobertas, descobertas e travadas em opções de mais de 80 ativos" ([/jumba-pro](https://jumba.com.br/jumba-pro)).
- O Mapa também traz o "histórico de titulares e lançadores e IQ" ([/quem-somos](https://jumba.com.br/quem-somos)).
- O canal do YouTube se apresenta como "Pioneira do Market Gamma de opções no Brasil" e diz que o Market Gamma "mostra a exposição dos Market Makers".

**Fontes de dados públicas da B3 que encaixam:**
- Consulta "Posições em aberto" de opções, em Mercado à vista > Opções, listada em [Consultas B3](https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/).
- [UP2DATA – Dados disponíveis](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/up2data/dados-disponiveis/). O canal **Regulatório** é marcado como "públicos e livremente disponibilizados" e inclui:
  - Posições em Aberto de Derivativos;
  - Posições em Aberto de Empréstimo de Ativos e Resumo de Empréstimos;
  - Cadastro de Instrumentos;
  - Negócios Consolidados.
- Os canais Superfície de Volatilidade, Curvas e Eventos Corporativos também existem no UP2DATA, mas a página **não diz que são gratuitos**.

**Conclusão sobre granularidade (inferência forte):** o open interest da B3 sai uma vez por dia, com a posição de D‑1 publicada depois do fechamento. Por isso as métricas baseadas em OI são **diárias**. Elas podem ser **recalculadas durante o dia** com o preço do ativo e a vol vindos da ProfitDLL. Isso combina com a descrição das Jumba Walls, cujos níveis aparecem "no início do pregão" ([/jumba-trader-flow](https://jumba.com.br/jumba-trader-flow)).

**Convenções usadas abaixo:** Γ = gamma de Black‑Scholes‑Merton (BSM); OI = posições em aberto por série; S = preço do ativo-objeto; mult = multiplicador do contrato. Em opções de ações, mult = 1 por opção, e o OI vem em quantidade de opções (convenção de mercado; confiança média).

---

## 1. Mapa de Opções
- **O que mostra:** um gráfico por strike das séries em aberto, separando calls e puts e dividindo cada barra em coberta, descoberta e travada. Tem histórico de titulares e lançadores e o IQ, para mais de 80 ativos. **Fonte pública confirmada**: [/jumba-pro](https://jumba.com.br/jumba-pro) e [/quem-somos](https://jumba.com.br/quem-somos). A página [/produtos](https://jumba.com.br/produtos) cita o Mapa "including its historical data".
- **Métrica:** não há cálculo, é o dado bruto de OI organizado.
- **Granularidade:** ativo × vencimento × strike × tipo, com dado diário (D‑1) e histórico.
- **Dados de entrada:** arquivo de posições em aberto da B3 por série (ticker, strike, vencimento, call/put, coberta, travada, descoberta, total, nº de titulares, nº de lançadores), cadastro de instrumentos e preço do ativo.

## 2. Resumo do Mapa
- **O que mostra (inferência):** uma tabela consolidada por ativo e vencimento com OI total de calls e de puts, percentual descoberto, strikes de maior concentração, variação contra D‑1 e IQ médio.
- **Métrica:** somas e participações percentuais (por exemplo, descoberta ÷ total).
- **Granularidade:** ativo × vencimento, diário.
- **Entrada:** a mesma do Mapa de Opções, mais o D‑1 para calcular variações.

## 3. Market Gamma Bands
- **Confirmado:** o nome aparece no Jumba Pro ([/produtos](https://jumba.com.br/produtos), Hotmart) e as bandas são "exportáveis e compatíveis com o Profit" ([/jumba-pro](https://jumba.com.br/jumba-pro)).
- **Inferência:** faixas de preço desenhadas no gráfico do ativo a partir do perfil de GEX. As bordas seriam o gamma flip (onde a GEX acumulada troca de sinal) e as maiores concentrações de gamma positivo e negativo. Outra possibilidade é uma faixa de movimento esperado, S·σ·√t, ancorada nesses níveis.
- **Granularidade:** ativo, uma por vencimento ou somando todos; nível diário com recálculo intradiário opcional.
- **Entrada:** OI por série, S, vol implícita (VI) por série, taxa, dividendos e tempo até o vencimento.

## 4. BGT Bands
- **Sem informação pública.** O nome não aparece em nenhuma página aberta. Suposição: bandas derivadas de gregas ("B/G/T" pode ser algo como Bandas Gamma‑Theta, mas isso é especulação). Também pode ser uma variação das Gamma Bands com outro ponderador.
- **Ação sugerida:** confirmar dentro da conta ativa, sem copiar dados, e anotar quais eixos e legendas a tela usa.
- **Entrada provável:** a mesma das Gamma Bands, mais theta por série.

## 5. Market Gamma e Jumba Walls
- **Confirmado:**
  - O Market Gamma "mostra a exposição dos Market Makers" ([vídeo](https://www.youtube.com/watch?v=k4mC3y7EhhE)).
  - Mostra o "posicionamento geral, regiões de gamma positivo e negativo" ([/quem-somos](https://jumba.com.br/quem-somos)).
  - Aponta "prováveis zonas de alta e baixa volatilidade" ([/jumba-trader](https://jumba.com.br/jumba-trader)).
- **Fórmula provável (inferência forte):**
  - Por strike: GEX_k = Σ Γ_i · OI_i · mult · S² · 0,01 · sinal_i.
  - Convenção comum: o dealer está comprado nas calls (+) e vendido nas puts (−).
  - O Jumba pode usar outro sinal, inferido a partir de coberta/descoberta e de titulares/lançadores. Isso é suposição.
  - Gráfico típico: barras de GEX por strike, linha de GEX acumulada e marcação do flip.
- **Granularidade:** ativo × strike, com vencimentos agregados ou filtráveis; OI diário e Γ recalculável durante o dia com S.
- **Entrada:** OI por série, S, VI por série (ou o prêmio para inverter BSM), taxa pré/DI, dividendos e dias úteis até o vencimento.

## 6. Shark Map
- **Confirmado:** mostra "movimentos de grandes investidores e market makers, incluindo ordens grandes que não aparecem no book público" ([/jumba-pro](https://jumba.com.br/jumba-pro)).
- **Inferência:** detecta negócios grandes e negócios diretos/cross no times & trades. Eles aparecem como negócios realizados, mas nunca ficaram expostos no book. Agrega por corretora (agente comprador/vendedor), strike e série.
- **Métrica:** filtro por tamanho (quantidade ou financeiro acima de um limiar), mais saldo por agente e por série.
- **Granularidade:** intradiário (tick a tick), por série e por ativo.
- **Entrada:** negócio a negócio com preço, quantidade, horário, agentes comprador/vendedor, agressor e flag de direto. Fonte provável: ProfitDLL em tempo real e histórico. Que a DLL entrega os códigos de agente é **suposição a verificar**.

## 7. Shark Positions
- **Confirmado:** é uma "interpretação algorítmica dos movimentos dos grandes players" ([/jumba-pro](https://jumba.com.br/jumba-pro)). Também "acompanha operações de ativos e opções, operações diretas e grandes estruturas" ([/quem-somos](https://jumba.com.br/quem-somos)).
- **Inferência:**
  - Junta negócios simultâneos do mesmo agente em várias pernas para reconstruir estruturas (travas, borboletas, financiamentos).
  - Mantém a posição líquida estimada de cada "shark" ao longo dos dias.
  - Classifica a estrutura pelo viés (alta, baixa ou neutro).
- **Granularidade:** por player/agente × ativo, intradiário com acumulado diário.
- **Entrada:** a mesma do Shark Map, mais cruzamento com a variação diária de OI da B3 para validar se foi abertura ou fechamento.

## 8. Volatilidade
- **Confirmado:** o plano inclui "Curva de Volatilidade Implícita Ajustada" ([/produtos](https://jumba.com.br/produtos)).
- **Inferência:** um smile por vencimento, VI contra strike ou contra moneyness/delta, ajustado por um modelo paramétrico. A B3 publica a nota técnica de ajuste SVI ([NT‑2013‑01 SVI](https://www.b3.com.br/data/files/95/16/EC/5C/42580510FE0C840592D828A8/NT-2013-01-Ajuste-de-dados-de-Volatilidade-Implicita-por-meio-da-parametrizacao-SVI.pdf)).
- **Fórmula:** a VI vem da inversão de BSM (Newton‑Raphson) sobre o prêmio, e o smile é ajustado por SVI ou spline.
- **Granularidade:** ativo × vencimento × strike, intradiário.
- **Entrada:** prêmios bid/ask ou último negócio, S, taxa, dividendos e tempo. Alternativa: o canal "Superfície de Volatilidade" do UP2DATA, que **não está confirmado como gratuito**.

## 9. Histórico de Volatilidade Implícita
- **Inferência:** série temporal da VI ATM por ativo e vencimento, ou com prazo constante (por exemplo, 30 dias). Mostra IV Rank/Percentil e compara com a vol histórica. A B3 tem uma consulta pública de "volatilidade dos ativos (desvio‑padrão)", que é vol **histórica**, não implícita ([Consultas B3](https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/)).
- **Fórmulas:**
  - IV Rank = (VI_hoje − mín_252) / (máx_252 − mín_252).
  - Vol histórica = desvio‑padrão dos log-retornos × √252.
- **Granularidade:** ativo, diário.
- **Entrada:** um snapshot diário da VI ATM, que precisa ser gravado por rotina própria, mais o histórico de preços do ativo.

## 10. Resumo do Gamma
- **Inferência:** um ranking entre ativos com GEX total, nível do flip, call wall, put wall, distância do preço ao flip e regime (gamma positivo ou negativo).
- **Granularidade:** ativo, diário com refresh intradiário.
- **Entrada:** a saída do cálculo de GEX da tela 5 para todos os ativos.

## 11. Gamma Score
- **Sem informação pública.** Suposição: uma nota normalizada que permite comparar ativos. Candidatos:
  - GEX ÷ volume financeiro médio, ou ÷ valor de mercado;
  - z‑score da GEX contra o histórico do próprio ativo;
  - combinação de regime, distância ao flip e concentração nas walls.
- **Entrada:** GEX histórica por ativo e ADV (volume financeiro médio diário).

## 12. Scanner de Barreiras
- **Confirmado:** o plano lista "Map barrier scanner" ([/produtos](https://jumba.com.br/produtos)).
- **Inferência:** procura, em todos os ativos, os strikes com grande concentração de OI (principalmente descoberto), que funcionam como "barreiras" de suporte/resistência no Mapa, próximos do preço atual. Mostra a distância percentual e o tamanho de cada barreira. Não parece ser sobre opções com barreira (knock‑in/out), mas isso também é inferência.
- **Métrica:** para cada ativo, os strikes no top‑N de OI descoberto dentro de ±X% do preço.
- **Granularidade:** ativo × strike, diário.
- **Entrada:** OI por série (B3) e S.

## 13. Put/Call Ratio (PCR)
- **Confirmado:** a tela existe ([/produtos](https://jumba.com.br/produtos), Hotmart). A fórmula não é publicada.
- **Fórmula padrão:** PCR = OI_puts ÷ OI_calls, ou na versão por volume = Vol_puts ÷ Vol_calls. Pode ser ponderada por financeiro (prêmio × quantidade).
- **Granularidade:** ativo × vencimento, diário com histórico.
- **Entrada:** OI por série (B3) e volume por série (Negócios Consolidados da B3 ou ProfitDLL).

## 14. Índice de Qualidade (IQ)
- **Confirmado em fonte externa:** o conceito vem do autor "Zé da Silva" no Clube do Pai Rico.
  - Fórmula: IQ = nº de titulares ÷ nº de lançadores da série, com dados do "relatório de opções divulgado diariamente pela Bovespa".
  - Exemplo do comentarista: 33 titulares ÷ 261 lançadores = 0,13.
  - Regra de leitura: "Acima de 1 é pó, abaixo, exercício".
  - Fontes: [O índice de qualidade na venda de opções](https://www.clubedopairico.com.br/o-indice-de-qualidade-na-venda-de-opcoes/22810) e [Distorções no IQ](https://www.clubedopairico.com.br/distorcoes-no-indice-de-qualidade-das-opcoes-o-que-isso-significa/39249).
- **No Jumba:** o "IQ do Ativo" e o "IQ Global dos Papéis" são confirmados como nomes ([/produtos](https://jumba.com.br/produtos), Hotmart). A **agregação por ativo é inferência**, por exemplo uma média do IQ ponderada pelo OI das séries.
- **Granularidade:** série e ativo, diário.
- **Entrada:** nº de titulares e nº de lançadores por série, que estão na consulta de posições em aberto da B3. Que esses campos venham na consulta é inferência, apoiada pelo artigo e pela página [/quem-somos](https://jumba.com.br/quem-somos).

## 15. Fluxo de Investimentos
- **Confirmado:** o plano lista "Investment flow" ([/produtos](https://jumba.com.br/produtos)).
- **Inferência:** saldo diário de compra e venda por tipo de investidor (estrangeiro, institucional, pessoa física, instituições financeiras) na B3, com acumulado no mês e no ano.
- **Fonte:** B3, "Participação dos investidores" ([Consultas B3](https://b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/)).
- **Granularidade:** mercado como um todo (não por ativo), diário com defasagem.

## 16. Mercados de Aluguel
- **Confirmado:** o plano lista "Rental market rates" ([/produtos](https://jumba.com.br/produtos)).
- **Inferência:** por ativo, mostra taxa doadora e tomadora, quantidade em aberto alugada, aluguel como % do free float e histórico.
- **Fonte:** UP2DATA Regulatório, "Posições em Aberto de Empréstimo de Ativos" e "Resumo de Empréstimos", ambos públicos.
- **Granularidade:** ativo, diário.

## 17. Eventos Corporativos
- **Inferência:** calendário de dividendos, JCP, bonificações, desdobramentos e grupamentos (data‑com e valor), com impacto nas opções.
- **Fonte:** canal UP2DATA "Eventos Corporativos" (**gratuidade não confirmada**), ou as páginas de proventos de empresas listadas na B3.
- **Granularidade:** ativo × evento.

## 18. Market Exposure
- **Sem descrição pública.** Inferência: é a exposição em **delta** dos formadores de mercado (DEX), em financeiro, por strike e no total.
- **Fórmula:** DEX_k = Σ Δ_i · OI_i · mult · S · sinal_i. Pode incluir também a exposição em vanna/charm.
- **Granularidade:** ativo × strike, diário com recálculo intradiário.
- **Entrada:** a mesma do GEX.

## 19. Jumba Walls
- **Confirmado:**
  - São "regiões onde market makers detêm risco… suporte e resistência", ligadas ao Market Gamma ([/quem-somos](https://jumba.com.br/quem-somos)).
  - São calculadas "nos pontos de maior probabilidade de delta hedge" e aparecem como "linhas horizontais azuis no início do pregão" ([/jumba-trader-flow](https://jumba.com.br/jumba-trader-flow)).
  - Podem ser exportadas para o Profit ([/jumba-trader](https://jumba.com.br/jumba-trader)).
- **Fórmula provável:** os strikes com maior |GEX_k|, ou com maior gamma nominal de calls (call wall) e de puts (put wall). O SpotGamma descreve o mesmo conceito ([Call Wall/Put Wall](https://spotgamma.com/call-wall-put-wall-explained/)).
- **Granularidade:** ativo, alguns níveis por dia.
- **Entrada:** o perfil de GEX da tela 5.

## 20. Histórico de Ajustes de Strikes
- **Inferência:** um log de quando e quanto a B3 ajustou o preço de exercício das séries por proventos e outros eventos (strike antigo, strike novo, ticker, data). Existe também o tratamento especial quando o dividendo supera o strike ([exemplo B3 – OC 141/2023, Petrobras](https://www.b3.com.br/data/files/44/41/F8/1E/E90E98101D7C7D98DC0D8AA8/OC%20141-2023%20PRE%20Tratamento%20para%20Dividendos%20Superiores%20ao%20Strike_Petrobras%20(PT).pdf)).
- **Fonte:** comparar diariamente o Cadastro de Instrumentos (UP2DATA Regulatório) entre D e D‑1, mais os ofícios circulares da B3.
- **Granularidade:** série × data.

## 21. Histórico do Market Exposure ATM
- **Inferência:** série temporal da exposição (delta e/ou gamma) concentrada nos strikes perto do dinheiro (por exemplo, ±2–5% de S), para ver acúmulo ou desmonte.
- **Granularidade:** ativo, diário.
- **Entrada:** snapshots diários de OI e de gregas, gravados por rotina própria.

## 22. Max Pain
- **Sem descrição pública** no Jumba. O conceito é padrão.
- **Fórmula:** Max Pain = argmin_K Σ_i OI_i · payoff_intrínseco_i(K), em que o payoff de call = max(K − strike_i, 0) e o de put = max(strike_i − K, 0).
- **Granularidade:** ativo × vencimento, diário.
- **Entrada:** OI por série (B3).

## 23. Max Pain History
- **Inferência:** a evolução diária do strike de Max Pain para cada vencimento, comparada com o preço do ativo e com o preço de fechamento no vencimento.
- **Entrada:** o histórico diário de OI, que precisa ser armazenado desde o início, porque a B3 não serve séries longas de forma prática.

## 24. Curva de Juros
- **Inferência:** a estrutura a termo pré (DI x pré), desenhada a partir dos ajustes dos futuros DI1 e/ou das taxas referenciais da B3. Pode comparar com D‑1, uma semana e um mês atrás. Também serve de insumo de taxa para BSM.
- **Fonte:** canal UP2DATA "Curvas" (gratuidade não confirmada); ajustes do pregão e taxas referenciais na B3; DI1 em tempo real pela ProfitDLL. Que a DLL tem DI1 é suposição.
- **Granularidade:** vértice × data, com atualização intradiária possível.

---

### Resumo das entradas de dados (para o planejamento Farol/MeusAgentes)

| Dado | Fonte provável | Frequência |
|---|---|---|
| OI por série, com coberta/descoberta/travada e titulares/lançadores | B3 posições em aberto / UP2DATA Regulatório | diária (D‑1) |
| Cadastro de séries (strike, vencimento, tipo, ajustes) | UP2DATA Cadastro de Instrumentos | diária |
| Prêmios, S, volume e times & trades com agentes | ProfitDLL (tempo real e histórico) | tick |
| VI e gregas | cálculo próprio (BSM + SVI) | intradiária |
| Aluguel | UP2DATA Regulatório (empréstimo) | diária |
| Fluxo por investidor | B3 Participação dos investidores | diária |
| Proventos | B3 / UP2DATA Eventos | por evento |
| Curva DI | B3 ajustes / taxas referenciais, DI1 pela DLL | diária / intradiária |

**Ponto crítico:** as telas de histórico (VI, Max Pain, Exposure ATM, ajustes) dependem de **gravar snapshots diários desde o primeiro dia**. Por isso uma rotina agendada é obrigatória.