## Revisão cética

### (a) Telas sem linha ou com entrada errada
- **As ondas não fecham.** O Jumba Pro não tem uma tela "Market Gamma" separada, só "Market Gamma e Jumba Walls". Trader Flow Beta aparece nas ondas 3 e 4. A Onda 1 promete cerca de 15 telas e lista 11; a Onda 2 promete cerca de 11 e lista 9.
- **Falta o strike das opções de ações.** Isso afeta Mapa, Resumo, Scanner, Max Pain, GEX/DEX e Histórico de Ajustes. O cabeçalho do CSV de cadastro em `/home/claude/Farol/tests/Services/Farol.DataHub.Tests/ScrapperCsvDailyUniverseProviderTests.cs:486` não tem "Preço de exercício". Cerca de 9.300 instrumentos é pouco para cobrir todas as séries de ações. Sem uma fonte nova de cadastro, a Onda 1 não roda.
- **Delta Estrutural está na Onda 1, mas precisa de vol implícita** (item 4 do motor, que só entra na Onda 2).
- **IND/DOL: a síntese não diz qual opção usar.** No índice, pode ser a opção sobre IBOV à vista (segmento de ações) ou sobre o IND futuro. No dólar, a opção sobre o disponível (liquidada pela PTAX) ou sobre o futuro. Isso muda o modelo (Black‑76 ou Garman‑Kohlhagen) e a fonte do OI.
- **Volatilidade e GEX diária:** o arquivo de negócios consolidados (NEG) só traz séries que negociaram, e séries com OI sem negócio ficam sem vol implícita.
- **Aluguel:** as taxas doadora e tomadora não estão no NEGOCIOSBTB, que traz uma taxa por negócio, nem na posição em aberto, que não traz taxa.
- **Eventos Corporativos:** `SubscribeAdjustHistory` traz o histórico de ajustes, não o calendário futuro de data‑com. E nenhuma camada de dados fornece dividendos esperados para o BSM.
- **Trader Flow, grupo Market Makers:** `corretoras-prior.json` tem 18 corretoras, classificadas só como varejo (8), estrangeira (7) e institucional local (3). Não existe classe de market maker.
- **Estruturas Salvas "em tempo real" pelo MeusAgentes não funciona assim.** O intervalo mínimo é PT1M (`/home/claude/MeusAgentes/packages/contracts/src/schedule.ts:10`), não há streaming e o agente precisaria de identidade mTLS, que é configuração protegida.

### (b) Afirmações que os achados não sustentam
1. **"CAD tem ExrcPric/OptnTp".** O glossário citado é o do `InstrumentsConsolidatedFile`, não o da rota `InstrumentsDerivatives` que o Farol baixa.
2. **"OI = OpenPositionsEquities com CvrdQty…".** O glossário citado é o [DerivativesOpenPosition](https://b3.com.br/data/files/1E/D1/BA/58/C841B810E9C1AAA8AC094EA8/DerivativesOpenPositionFile%202023.pdf). Nada mostra que seja a mesma rota usada em `b3_scraper_linux.py:80` (`OpenPositionsEquities@false`, cerca de 400 B segundo `docs/operations/scrapper-derivativos-only.md:56`). Esse glossário também tem `BrrwrQty` e `LndrQty`, que a síntese omitiu. Por isso, concluir que o IQ não tem fonte é prematuro.
3. **A divergência 1 já se resolve no repositório.** Os 881 tickers são 880 de OPCOES‑FUTUROS mais 1 de OPCOES‑JUROS (`docs/specs/0009-universo-sem-opcoes/SPEC.md:21,66`). Não há evidência de opções de ações gravadas.
4. **Os horários 18h30, 19h e 19h30 aparecem como fato.** O achado diz que são os padrões do código e que o `.env` pode mudá-los.
5. **"vigia‑jumba como systemd‑observed" é inválido.** O contrato só aceita esse adaptador numa `rotina` sem entry (`packages/contracts/src/execution.ts:30-33`). Além disso, nenhum agente roda hoje na vps1 (todos estão em `dev` ou `vps2`), e o scraper roda na vps1.
6. **A síntese ignora `/home/claude/MeusAgentes/.design/adocao-farol.md:53`.** A regra P5 diz que, no início, o MeusAgentes só observa as rotinas do Farol. A síntese também ignora o catálogo de agentes do próprio Farol (`/home/claude/Farol/catalog/agents/mercado-freshness` e `datahub-pregao-vigia`, executados pelo `Farol.Adm.Server`). Há risco de dois vigias para a mesma coisa. Cabe ao Marcelo decidir.
7. **"Um ingestor único grava na zona Vivo" conflita com "o DataHub é o único escritor da História".** Ou esse ingestor é o próprio DataHub, ou os dados ficam fora da História.
8. **BSM‑Merton com dividendos.** A B3 ajusta o strike pelos proventos em dinheiro; o OC 141/2023, citado nos achados, trata justamente de dividendo maior que o strike. Somar também o dividend yield contaria o provento duas vezes **[S]**.
9. **"A Onda 1 não precisa de tempo real nem de mudança no Host" não se sustenta.** O preço do ativo (D4) vem da DLL em tempo real, e o DI1 intradiário exige incluir o ticker no TICKADM.
10. **Negócios diretos a favor da síntese:** a coluna `aggressor` da Fita guarda o `TradeType` bruto, em que 1 = Cross (`IpcMessages.cs:579-601`, `MarketDataTypes.cs:64`). O Shark Map pode usar isso.

### (c) Fontes melhores que foram ignoradas
- **Arquivo "Prêmio de Referência" da B3:** cobre todas as séries, inclusive sem negócio. Serve para a vol implícita diária e substitui o NEG.
- **Cadastro de opções de ações:** o BVBG.028 (InstrumentsFile, na Pesquisa por Pregão) ou o COTAHIST diário, que traz PREEXE e DATVEN **[S, conferir no rb3]**.
- **`BrrwrQty`/`LndrQty`:** testar se, para opções, esses campos trazem o número de titulares e de lançadores.
- **Strike no próprio ticker das opções BM&F**, para IND e DOL.
- **Lista de formadores de mercado credenciados da B3:** serve para o grupo Market Makers e para a convenção de sinal da GEX **[S]**.
- **`nContratosOpen` da DLL:** testar antes de investir no OI raspado.

### (d) O que observar no Jumba logado
- **Mapa:** unidade do eixo; se titulares e lançadores são pessoas ou quantidade; a data do dado.
- **Market Gamma e Walls, Gamma Bands, IND/DOL:** unidade e sinal da GEX; se soma vencimentos; quando atualiza durante o dia; quantas walls; formato da exportação para o Profit; qual opção é usada.
- **BGT Bands, Gamma Score, Resumo do Gamma:** legendas, escala, faixa de valores e ativos.
- **Market Exposure e Histórico ATM:** se é delta ou gamma, e qual faixa ATM em %.
- **IQ:** se é por série ou por ativo, e como o "IQ Global" é ponderado.
- **Shark Map e Shark Positions:** limiar de negócio "grande"; se mostra corretora; se marca negócio direto; se mostra estruturas reconstruídas.
- **Trader Flow e Beta:** unidade; corretoras de cada grupo; se zera a cada dia; tempo gráfico; o que muda no Beta.
- **Volatilidade:** eixo x (strike, delta ou moneyness); preço usado (meio do book ou último); se mostra os pontos crus junto da curva.
- **Fluxo de Investimentos, Aluguel, Eventos, Histórico de Ajustes, Max Pain, Curva de Juros:** colunas, categorias, defasagem e vértices.
- **Find Your Trade:** lista das mais de 40 estruturas; filtros; se usa bid/ask; taxa de referência; se considera custos; se o Long Collar é o mesmo que o Collar.