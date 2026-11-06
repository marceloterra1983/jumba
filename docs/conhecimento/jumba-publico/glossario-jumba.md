# Glossário Jumba montado com fontes públicas

- **O que é:** um glossário derivado, que eu montei. A Jumba não publica glossário aberto: o menu Educacional exige login (ver `site-educacional.md`).
- **Acesso às fontes:** 2026-11-04. Cada verbete diz de onde veio. **[C]** é citação ou fato de fonte pública. **[I]** é inferência minha.
- **Uso:** os nomes próprios ("Jumba Walls", "Shark Map", "Market Gamma Bands"...) são marcas da Jumba (Termos, cláusula 13). Na réplica, convém usar nomes genéricos.

| Termo | Definição pública | Fonte |
|---|---|---|
| Mapa de Opções | "Um panorama completo de todas as posições cobertas, descobertas e travadas das opções de mais de 80 ativos" [C]. "atualiza diariamente todas as séries em aberto" [C]. Tem "histórico de titulares e lançadores" [C]. | /jumba-pro; Telegram 125; /quem-somos |
| Barreiras do Mapa / Scanner de barreiras | Exemplo: "quatro strikes de opções com volume descoberto acima de 5 milhões e índice de qualidade (IQ) acima de 1,2" [C]. Na prática: strikes com muita posição descoberta e IQ alto [I]. | Telegram 1597, 1183; /produtos |
| Maiores variações | Recurso do Mapa, citado sem descrição [C]. Deve ser a variação de OI por série em relação a D-1 [I]. | Telegram 1047 |
| IQ (Índice de Qualidade) | "Relação Titulares/Lançadores" [C]. "compila o posicionamento de titulares e lançadores" [C]. Calculado à parte para calls e para puts, em linhas ao longo do tempo, com o preço como linha branca [C]. Fórmula de fonte externa: titulares ÷ lançadores [C, Clube do Pai Rico]. | Código das Opções M10; Telegram 1779, 560–564 |
| Boca de jacaré | No IQ, é o cruzamento ou a abertura das linhas, que "costuma" anteceder um movimento amplo [C]. | Telegram 1779, 1745 |
| IQ Global dos Papéis | O nome aparece no Jumba Pro [C]. A fórmula não é pública. Deve agregar vários ativos [I]. | /produtos |
| PCR (Put/Call Ratio) | "demonstra o sentimento dos investidores, se estão buscando mais ou menos proteção via opções de venda" [C]. Leitura contrária na euforia [C]. A Jumba não diz se usa OI ou volume. | Telegram 1047, 547 |
| Market Gamma | "mostra a exposição dos Market Makers" [C]. Mostra "se a ação está no cenário de Gamma positivo, Gamma negativo ou nas proximidades do Flip" [C]. | Telegram 125, 268; YouTube (pesquisa anterior) |
| Gamma positivo / negativo | Positivo "segurou a volatilidade" [C]. Negativo: "Se entra venda o MM vende junto" (delta hedge) [C]. A mudança de negativo para positivo é sinal de alta [C]. | Telegram 91, 261, 1771 |
| Flip | "ponto de transição entre o gamma positivo e negativo", onde a curva cruza zero [C]. O preço tende a ser levado para lá perto do vencimento [C]. É expresso em pontos do IBOV ou em preço do ativo, como o BOVA11 "acima de 177" [C]. | Telegram 78, 91, 1762, 1786 |
| Put Gamma Wall / Call Gamma Wall | Níveis do IBOV ao lado do Flip: 104,8k / 116,9k / 123,3k [C]. Seriam os strikes de maior gamma de puts e de calls [I]. | Telegram 124 |
| Mínimo / Máximo do Market Gamma | São níveis de preço. Exemplo: CYRE3 "atingiu o mínimo do Market Gamma (R$ 18,22)" [C]. O Payoff mostra "Mínimo, máximo e Flip" [C]. | Telegram 1490, 1812 |
| Market Gamma Bands | "mostra dentro de um exercício, prováveis regiões de suporte e resistência" perto do "mínimo negativo do Market Gamma" e da "linha superior (máximo do gamma)" [C]. Histórico do máximo (linha verde) e do mínimo (linha vermelha) [C]. "O preço do ativo raramente rompe essas linhas" [C]. Exportável para o Profit [C]. | Telegram 765, 1103, 790; /jumba-pro |
| Jumba Walls | "regiões onde os Market Makers travam o risco no mercado de opções" [C]. Ficam nos pontos de maior probabilidade de delta hedge [C]. Saem "antes mesmo da abertura do pregão" [C]. Existem para IND, DOL e ações [C]. Aparecem como linha branca (Telegram) ou azul (página do Trader Flow) [C]. | /quem-somos; /jumba-trader-flow; Telegram 1716, 1712, 1843 |
| MidWalls | "linhas pontilhadas" entre as Walls [C]. Devem ser o ponto médio entre Walls vizinhas [I]. | Telegram 1843, 1734 |
| Shark Map | "maiores operações executadas na B3, em tempo real" [C]. Inclui "ordens grandes que não aparecem no book público" [C]. Tem "Operações Relevantes ... nos últimos 30 dias" [C]. | Telegram 1045, 1047; /jumba-pro |
| Shark Positions | "identifica estruturas com opções, pontas compradas e vendidas, custo de montagem e gráfico de payoff" [C]. | Telegram 1045 |
| Trader Flow | "direção do fluxo do Smart Money" [C]. "de que lado grandes players estão agredindo" [C]. Smart Money em linha verde, Varejo em linha rosa, mais um grupo de Market Makers [C]. Fica num painel abaixo do gráfico [C]. | /jumba-trader-flow; Telegram 1857, 1843 |
| Curva de Volatilidade Implícita (Ajustada) | "estima o preço teórico/justo de uma opção sem book de ofertas" [C]. "Ajustada" deve querer dizer suavizada [I]. | Telegram 1047; /produtos |
| Preço Jumba | "Preço teórico das opções calculado com base na curva de volatilidade" [C]. | Telegram 1812 |
| BGT | É um dado do Jumba Pro exibido no Payoff [C]. A sigla não é explicada em nenhuma fonte pública. | Telegram 1812 |
| Max Pain | "Max Pain do IBOV deslocou" [C]. Sem definição pública. Conceito de mercado: o strike que minimiza o valor intrínseco total pago aos titulares [I]. | Telegram 1745, 1812 |
| Payoff de Estruturas (FYT, beta) | Snapshot com book; níveis do Market Gamma, BGT e Max Pain; vol e skew por vencimento ajustáveis; Preço Jumba; spread de entrada e saída; dashboard com vários painéis [C]. | Telegram 1812 |
| Rolagem | "encerramento da posição atual e remontagem no próximo vencimento" [C]. No FYT, valor negativo = crédito [C]. O melhor "embolso" fica no ATM [C]. Há tabelas ATM por ativo [C]. | Telegram 1721, 1722, 594, 596 |
| Cone ±2σ | Linhas de −2σ, spot e +2σ "a partir da volatilidade implícita" até o vencimento [C]. Fórmula provável: S·exp(±2σ√T) ou S(1±2σ√T) [I]. | Telegram 1819 |
| Fluxo de investimentos | "fluxo de entrada e saída por player: estrangeiro, institucional, pessoa física e instituição financeira" [C]. | Telegram 1047 |
| Mercado de Aluguel | "taxas de aluguel dos ativos" [C]. | Telegram 1047; /produtos |
| Eventos Corporativos | "datas de divulgação de resultados trimestrais das empresas" [C]. | Telegram 1047; Código das Opções M10 |
| Fence | "Trava de Baixa de PUTs financiada pela venda de uma CALL fora do dinheiro" [C]. | Telegram 585 |
| Dia de vencimento | O canal repete os mesmos horários [C]: exercício manual antecipado até 14h45, negociação até 15h45, exercício automático às 18h15 e aftermarket das 18h25 às 18h40. Nas séries L/X (dezembro), tudo +1h: 15h45, 16h45, 19h15 e 19h25–19h40. Depois do horário-limite, recomprar a opção zera a obrigação. | Telegram 1852, 1845, 1809, 1784, 1732 |
