## Pesquisa pública: Jumba Trader (IND/DOL), Trader Flow e Find Your Trade

**Como fiz a pesquisa e o que ficou de fora.** Li só páginas públicas, sem login: jumba.com.br/jumba-trader, /jumba-trader-flow, /jumba-fyt, /jumba-pro, /tradingview e /produtos, além das listagens na Hotmart, de vídeos do YouTube e do canal t.me/s/mapadeopcoes. Nenhuma dessas fontes explica fórmulas ou metodologia, só nomes e descrições de marketing. Não consegui ler pages.jumba.com.br/trader-flow, pages.jumba.com.br/market-gamma-jumba-pro e jumbafyt.com.br/dzflw1 (o curso "Do Zero ao Flow"); as três deram erro. Não achei nenhum script público do Jumba no TradingView.

Para conferir o que o Farol já tem, fiz uma busca rápida (grep) no repositório:
- O Farol já grava negócios com `BuyAgent`, `SellAgent`, `Aggressor` e `TradeType` em `/home/claude/Farol/src/Contracts/Farol.Protocol/Types/MarketDataTypes.cs`. Grava em Parquet via `/home/claude/Farol/src/Services/Farol.DataHub/Storage/ParquetTradeStore.cs` e já tem uma projeção de fluxo em `/home/claude/Farol/src/Services/Farol.DataHub/Services/TradeFlowWire.cs`.
- Não encontrei código de BSM, vol implícita ou gamma de opções no Farol. Isso ainda precisa ser construído.

Legenda: **[C]** = confirmado em fonte pública · **[I]** = inferência ou suposição minha.

---

## Jumba Trader – IND e DOL

### Mapa de Opções (IND/DOL)
- **O que mostra:** a página só diz "Acesso ao Mapa de Opções do Dólar e Índice Futuro" [C]. No Jumba Pro, o Mapa é "um panorama completo de todas as posições cobertas, descobertas e travadas" [C], e os termos coberta/descoberta/travada são os da B3 nos arquivos de posições em aberto.
- **Lógica provável:** por vencimento e strike, mostra posição em aberto de calls e puts, volume e preço de exercício contra o preço do futuro [I].
- **Granularidade:** diária (posições de D-1) [I].
- **Dados de entrada:**
  - Lista de séries de opções sobre o futuro de Ibovespa e o dólar futuro (opções sobre IBOV à vista também, possivelmente) [I].
  - Posições em aberto diárias publicadas pela B3 [I].
  - Último preço e volume via ProfitDLL [I].

### Jumba Walls (IND/DOL)
- **O que mostra:** linhas horizontais azuis de suporte e resistência, "baseados na exposição dos Market Makers" [C]. Elas "indicam no início do pregão as prováveis regiões de suporte e resistência daquele dia" [C]. Existe uma "Ferramenta de Exportação para o Profit" [C].
- **Lógica provável:** strikes com maior gamma ou posição em aberto. Os maiores nas calls viram resistência e os maiores nas puts viram suporte, ou os picos de |GEX| por strike. São calculados antes da abertura, com a posição de D-1, e ficam fixos durante o dia [I].
- **Granularidade:** um conjunto de níveis por pregão [C, porque são definidos "no início do pregão"].
- **Dados de entrada:**
  - Posições em aberto por strike [I].
  - Preço de ajuste ou fechamento do futuro [I].
  - Vol implícita, prazo e taxa (DI1) [I].
- **Exportação:** provavelmente um arquivo de texto ou estratégia NTSL com linhas horizontais para o ProfitChart [I].

### Market Gamma (IND/DOL)
- **O que mostra:** "identificar as prováveis zonas de alta e baixa volatilidade" com base no posicionamento dos formadores de mercado [C].
- **Fórmula provável (Gamma Exposure):** GEX(K) = Σ OI × Γ(Black-76) × multiplicador × F² × 1%, com sinal + para calls e − para puts (a convenção de que o dealer é vendido em puts é suposição) [I].
  - Multiplicador: R$1 por ponto no IND e contrato de US$50 mil no DOL [I].
  - O nível de virada (gamma flip) separa a zona "amortecida" (gamma positivo, baixa vol) da zona "acelerada" (gamma negativo, alta vol) [I].
- **Granularidade:** diária, possivelmente recalculada no intraday com o preço do futuro [I].
- **Dados de entrada:** os mesmos das Walls, mais a vol implícita por série tirada do bid/ask das opções (ProfitDLL) [I].

---

## Jumba Trader Flow

### Jumba Trader Flow
- **O que mostra:** "Dados BMF em tempo real" [C], com três grupos de players [C]:
  - **Market Makers:** "dão liquidez para grandes operações" e fazem delta hedge.
  - **Smart Money:** linha verde, "institucionais e estrangeiros".
  - **Varejo:** linha rosa, descrito como "na contramão do mercado".

  O pacote inclui ainda Mapa de Opções, Market Gamma, Jumba Walls e exportação para o Profit [C]. Ativos: "Dólar e Índice Futuro", e o marketing cita o mini dólar [C].
- **Lógica provável:**
  - Saldo acumulado intraday, em contratos, por grupo de corretoras. Para cada negócio, soma +qtd para o grupo do agente comprador e −qtd para o grupo do agente vendedor [I].
  - A classificação seria feita por corretora (código de agente): bancos e corretoras estrangeiras e institucionais em "smart money", corretoras de varejo em "varejo" [I].
  - A alternativa é o saldo de agressão (aggressor buy menos aggressor sell) por grupo [I].
  - As Walls servem de alvo ou stop. Há um short do Jumba chamado "Configuração Alvos" (não consegui ler o conteúdo) [I].
- **Granularidade:** tick a tick, exibido em barras de 1 minuto ou de tempo configurável [I].
- **Dados de entrada:**
  - Times & trades do WIN/WDO e do IND/DOL com agente comprador, agente vendedor e agressor. A ProfitDLL fornece isso, e o Farol já armazena (`MarketDataTypes.cs`, `TradeFlowWire.cs`) [C no repositório].
  - Uma tabela de classificação das corretoras, que nós teríamos de montar [I].
  - Para calibrar, a B3 publica a participação por tipo de investidor (estrangeiro, institucional, pessoa física) [I, não verifiquei a URL].
- **Pasta útil no repositório:** `/home/claude/Farol/scripts/research/fluxo/` (pesquisa de fluxo já existente).

### Trader Flow — TradingView
- **O que mostra:** o Jumba diz usar a biblioteca **TradingView Advanced Charts** dentro da plataforma, com "estudos, desenhos e personalizações" que podem ser salvos [C, jumba.com.br/tradingview]. A página pública traz só um gráfico gratuito de fim de dia das ações da B3 [C].
- **Interpretação:** é o Trader Flow desenhado sobre um gráfico TradingView embutido, com candles do futuro, as linhas verde e rosa em painel separado e as Walls como linhas horizontais. Não é um script publicado no TradingView.com [I, e não achei script público].
- **Dados de entrada:** candles OHLCV intraday, que o Farol já tem (`BarStore.cs`, `TapeCandleReader.cs`), mais a série do Trader Flow [I].
- **Para a nossa réplica:** TradingView Lightweight Charts (licença Apache 2.0), sem precisar da licença da Advanced Charts [I].

### Trader Flow Beta
- **O que mostra:** não há nenhuma informação pública.
- **Suposição:** é uma versão nova em teste, talvez com outra classificação de players, mais ativos ou outro tempo gráfico [I].
- **Próximo passo:** confirmar navegando com a sua conta.

---

## Find Your Trade (FYT)

**O que vale para todas as telas [C, jumba.com.br/jumba-fyt]:**
- "Acompanhe em TEMPO REAL o preço para montagem de diversas estratégias."
- "+ de 40 estruturas" (a página lista 24, entre elas travas, borboleta, THL, BWB, Seagull, Fence, Collar, Box de 3 Pontas, Venda Coberta e Short Straddle Coberto).
- Ativos: ABEV3, B3SA3, BBAS3, BBDC4, BOVA11, ITUB4, PETR4, PRIO3 e VALE3.
- Também tem: "Buscador de Venda Coberta, Box de 3 e 4 Pontas", "Curva de Volatilidade Implícita Ajustada", alertas por bot do Telegram e monitoramento de rolagens do vencimento atual e do próximo.

**Entradas comuns às telas [I]:**
- Cadeia de opções da B3: ticker, strike, vencimento, tipo e estilo. As calls costumam ser americanas e as puts europeias.
- Melhor bid e ask, mais o último preço, das opções e do ativo-objeto via ProfitDLL (book e cotações).
- Taxa livre de risco tirada da curva DI1 (CDI ou Selic), com prazo em dias úteis sobre 252.
- Dividendos e proventos para o ajuste de strikes.

### Todas as Estruturas
Scanner que monta cada estrutura em todas as combinações de strike e vencimento [I]. Para cada uma, calcula com preço executável (comprar no ask, vender no bid) [I]:
- custo ou crédito de montagem;
- ganho e perda máximos;
- breakevens;
- retorno percentual e anualizado, comparado ao CDI.

Permite filtrar e ranquear [C nos "filtros"; métricas I]. Granularidade: tempo real, por evento de book [C].

### Estruturas Salvas
Estruturas favoritas com alerta de preço, e o bot do Telegram avisa "quando o preço desejado é atingido". Há um painel de alertas criados e disparados [C]. Na nossa réplica, isso vira um agente no MeusAgentes que vigia o preço da estrutura [I].

### Volatilidade
"Curva de Volatilidade Implícita Ajustada" [C].
- **Cálculo provável:** vol implícita por strike e vencimento, obtida invertendo o BSM sobre o preço médio entre bid e ask (ou o último). "Ajustada" deve querer dizer suavização do smile ou correção de strikes ajustados por proventos [I].
- **Dados:** prêmios, spot, taxa DI e prazo.

### Payoff
Gráfico de resultado de uma posição no vencimento e antes dele (curva BSM em D+n), com prêmio e quantidade [I, não está na página pública].

### Calculadora BSM
Entradas: S, K, T (dias úteis/252), r (DI), σ e dividend yield. Saídas: preço teórico, as gregas (Δ, Γ, ν, Θ, ρ) e a vol implícita a partir de um prêmio informado [I]. Fórmula: Black-Scholes-Merton padrão. Para as calls americanas sem dividendo relevante, o valor é igual ao europeu [I].

### Payoff de Estruturas
Payoff de várias pernas somadas, mais o P&L teórico antes do vencimento, com breakevens, ganho e perda máximos [I].

### Delta Estrutural
- **Cálculo provável:** delta líquido da estrutura, Σ (qtd × Δ_perna), em que a ação conta Δ = 1. Talvez mostre como o delta varia com o preço do ativo, para orientar ajustes ("manejos") [I].
- **Atenção:** "Slide Estrutural" aparece na lista como nome de estratégia, não de métrica [C].
- **Dados:** gregas da Calculadora BSM e a vol implícita da curva.

### Venda Coberta
Buscador confirmado [C]. Estrutura: compra da ação e venda da call. Métricas prováveis [I]:
- taxa = prêmio ÷ (S − prêmio);
- proteção percentual = prêmio ÷ S;
- retorno se exercido = (K − S + prêmio) ÷ (S − prêmio);
- todas anualizadas e comparadas ao CDI.

### Cash Put
Não aparece na página pública [I]. Estrutura: venda de put com o caixa aplicado no CDI como garantia. Métricas:
- retorno = prêmio ÷ (K − prêmio);
- preço efetivo de compra = K − prêmio;
- retorno total = retorno da put mais o CDI sobre o caixa.

### Box 3 Pontas
Buscador confirmado [C]. A B3 tem um programa de incentivo tarifário para "Box 3 Pontas em opções de ações e ETFs" (ofício OC 032-2026, achado na busca, mas o PDF não abriu).
- **Estrutura:** compra da ação, compra de put K e venda de call K, no mesmo strike e vencimento. O valor no vencimento fica travado em K.
- **Taxa:** K ÷ (S + P_ask − C_bid) − 1, anualizada e comparada ao CDI. Funciona como renda fixa sintética [I na fórmula].

### Box 4 Pontas
Buscador confirmado [C].
- **Estrutura:** trava de alta com calls (compra K1, vende K2) mais trava de baixa com puts (compra K2, vende K1). O payoff fica fixo em K2 − K1.
- **Taxa:** (K2 − K1) ÷ custo líquido − 1. Pode ser montada como aplicação ou como captação [I na fórmula].

### Long Collar
A página pública lista "Collar" [C]; "Long Collar" deve ser a mesma coisa [I].
- **Estrutura:** compra da ação, compra de put K1 e venda de call K2, com K1 < K2.
- **Métricas:** custo líquido (às vezes zero), perda máxima = S + P − C − K1 e ganho máximo = K2 − S − P + C [I].

---

## Fontes
- https://jumba.com.br/produtos
- https://jumba.com.br/jumba-trader
- https://jumba.com.br/jumba-trader-flow
- https://jumba.com.br/jumba-fyt
- https://jumba.com.br/jumba-pro
- https://jumba.com.br/tradingview
- https://hotmart.com/pt-br/marketplace/produtos/jumba-pro-jumba-trader-combo/Q90970656B
- https://hotmart.com/pt-br/marketplace/produtos/jumba-pro-jumba-trader-flow-combo/R103220460G
- https://hotmart.com/pt-br/marketplace/produtos/jumba-trader-flow-jumba-pro-find-your-trade-combo/T96724476E
- https://www.youtube.com/watch?v=mUYc0MQsqP4
- https://www.youtube.com/watch?v=QfoE6IJ9o-U
- https://www.youtube.com/shorts/WqM6Sl5QPcU
- https://t.me/s/mapadeopcoes
- https://www.b3.com.br/data/files/1E/F5/53/51/9C3BF91094DCD8F9AC094EA8/OC%20032-2026%20PRE%20PRORROGACAO%20DO%20PROGRAMA%20DE%20INCENTIVO%20TARIFARIO%20PARA%20OPERACOES%20DE%20BOX%203%20PONTAS%20EM%20OPCOES%20DE%20ACOES%20E%20ETFS%20(PT).pdf
- https://pypi.org/project/profitdll-wrapper/