# D1: cotações ao vivo das séries de opção perto do dinheiro, numa faixa própria do Portal

## Origem deste desenho

Este desenho parte da proposta da **faixa isolada e autolimitada**, e não da proposta que passa pelo hub do Mercado. Dois fatos do código decidem a escolha:

- Um único ticker recusado derruba o duplex inteiro de quem o pediu (F4). O duplex do Mercado serve ao mesmo tempo as abas, os alertas e a leitura macro (F5).
- O custo de uma série no Host depende da hora da sua primeira assinatura (F7). Com o hub, essa hora seria a hora em que alguém abre a página.

Da proposta do hub vieram cinco peças:
- a seleção pura ancorada no fechamento do dia D, que não segue o preço ao vivo;
- o filtro de forma idêntico ao do Host, mais o filtro de sinal de vida;
- o último negócio escolhido pelo maior par (timestamp, número);
- as cercas de orçamento e de forma;
- a página "Grade por strike" e o aceite por `git diff`.

A conferência no código mudou três pontos das duas propostas, e a revisão mudou mais cinco:

1. **Cancelar no Gateway não alivia o Host.** A assinatura nativa continua até o Host encerrar o processo (F6). Os degraus de redução protegem só o Gateway e o Portal. O Host só se protege antes de assinar, por hora, ritmo, portões e teto de séries distintas.
2. **O recentro contínuo foi trocado.** Ele acumula séries nativas distintas, e cada uma custa mais quanto mais tarde entra (F7). O conjunto passa a ser fixo no dia, com no máximo uma reancoragem por objeto depois da abertura.
3. **A reserva de transição não está provada.** Nenhum teste prova a reserva de 16 pertenças da proposta original (F3). O teto seguro passa a ser 2C ≤ 256 − 16 até que um teste em processo meça essa reserva.
4. **A faixa é um consumidor novo do catch-up congelado.** Não muda código do caminho do ADR-0040, mas cada série nova põe trabalho nele, e as suas fatias podem passar à frente do reparo de arranque do DataHub (F7, F8). O dono aceita esse efeito por escrito nesta SPEC antes de F1 (seção 3.7).
5. **Uma adição nova a cada 6 s.** O duplex não confirma comandos (F15), e só esse ritmo permite saber que série derrubou o stream. O aquecimento passa a ter orçamento próprio, B_a.
6. **Depois de uma queda do pipe, a faixa libera as séries enquanto o pipe está em baixo.** Sem isso, o Gateway repõe-nas no Host novo antes de a graça acabar (F2, F10).
7. **O estado de proteção sobrevive a um reinício do Portal**, num arquivo de estado do dia, e falha fechado quando ele falta (seção 3.5).
8. **Toda lacuna é global**, porque nenhum `GapEvent` diz o ticker (F16).

Os caminhos curtos usados nas citações estão no anexo.

## 1. Valor e comportamento

### 1.1 Problema

O módulo de opções só conhece a base diária:
- As rotas `/api/opcoes/dates`, `/{date}/underlyings` e `/{date}/chain/{underlying}` leem pela Concessão o cadastro de um dia D (OptionDailyEndpoints.cs:9-14; OptionDailyReader.cs:9-57).
- A página "Grade por strike" é um placeholder (optionsModules.ts:10; App.tsx:89-93).

O Portal não tem preço ao vivo de série de opção em lugar nenhum:
- O único caminho ao vivo é o hub do Mercado (RealtimeEndpoints.cs:18-27; MarketHub.cs:16-34).
- A única porta de servidor é `IMarketTradeSource`, fixa em WINFUT e WDOFUT (MarketTradeObservation.cs:14-38, 59-60).

O Gateway já aceita assinar qualquer ticker sob demanda (MarketDataService.cs:165-192), com cota de 256 pertenças por sujeito de certificado (GatewayOptions.cs:50). O custo que de fato limita, porém, está no Host. Cada série nova:
- aciona o catch-up da Fita, que faz parte do caminho congelado;
- pede um fechamento anterior por histórico;
- fica assinada na DLL até o Host encerrar o processo, que é o único caminho que limpa `MarketState.Subscriptions` (F6, F7).

### 1.2 Comportamento pretendido

- **Horário.** Em dia de pregão, das 09:02 às 18:00, o Portal mantém ao vivo um conjunto fixo de séries perto do dinheiro de até L objetos escolhidos pelo dono, cada um numa de duas camadas de prioridade. De cada série mantém o topo do livro (melhor compra, melhor venda e tamanhos) e o último negócio. Mantém também o último negócio de cada objeto.
- **Escolha do conjunto.** O conjunto do dia é escolhido às 08:45, a partir do cadastro diário mais recente publicado como `available` e do fechamento do objeto nessa data. Pode ser reancorado uma vez por objeto, às 10:20.
- **Leitura.** A página "Grade por strike" mostra o quadro de um objeto, só para leitura, com a idade de cada valor.
- **Autolimitação.** A faixa freia-se sozinha pelas métricas do Host lidas sem cache, pela sua própria conta de fatias e pelos orçamentos B_a e B_f. Não se aproxima das cotas do Gateway.
- **Isolamento.** No Portal, uma falha da faixa não chega às abas do Mercado, aos alertas nem à leitura macro. No Gateway, a faixa tem cota e stream próprios, mas compartilha com todos os clientes o semáforo único do registro de assinaturas (F3). O ritmo limita esse acoplamento, e o teste 6b mede-o.
- **Estado inicial.** Tudo nasce desligado: `Portal:OptionLive:Enabled=false` e lista de objetos vazia.

## 2. Limites

### 2.1 Em escopo

- Seletor puro, planejador, leitor de métricas sem cache, estado do dia, faixa de cotações no Farol.Mercado com uma porta pública estreita, duas rotas de leitura, a página `#opcoes` e configuração.
- Um perfil mTLS opcional próprio da faixa, com o seu adaptador de autoridade, e a lista dos passos de produção do dono (seção 3.8).
- Opções de ação e de ETF cuja raiz tem 4 caracteres e cujo código segue a forma de opção de ação do Host (TickerClassifier.cs:44-47). Só séries mensais.
- Testes do Portal; casos novos nos testes do Gateway e do Host, sem tocar no código deles; cercas; o ajuste de `e2e/opcoes-navigation.spec.ts`; uma nova SPEC que abre exceção à SPEC-0526 só para `#opcoes` (docs/specs/0526-portal-opcoes/SPEC.md:57, 66-68, 75-76).

### 2.2 Fora de escopo

- **Recentro contínuo.** Fica de fora o recentro dentro do dia que vai além da reancoragem única.
- **Formas de código excluídas.** Ficam de fora:
  - semanais W1–W5;
  - opções de índice, de futuro e de juros;
  - a forma C/P de ETF, para a qual o Host e o DataHub deduzem Segmentos diferentes (TickerClassifier.cs:49-62, 184-209; LiveIngestReconciliationIdentity.cs:34-38).
- **Cálculo.** Ficam de fora gregas, volatilidade implícita e GEX ao vivo, e o consumo do quadro pelas calculadoras. A SPEC-0540 diz que os formulários não consultam mercado (docs/specs/0540-opcoes-calculadoras/SPEC.md:48-49).
- **História.** Não se grava cotação de opção na História nem se cadastra série no TICKADM (`tickers.admin`, PortalContracts.cs:508). A faixa grava só o seu estado do dia, fora da História (seção 4).
- **Outros componentes.** Não muda código do Host, do Gateway, do DataHub, dos contratos nem do transporte.
- **Itens separados.** Ficam para depois:
  - D1c, a recusa por ticker no Gateway;
  - D1d, impedir que o Gateway reponha intenções órfãs ou fantasmas;
  - D1e, um campo de ticker no `GapEvent`, que exige mudar o contrato (farol_remote.proto:387-393);
  - D1f, uma métrica do Host com o número de assinaturas nativas, porque `subscribed_tickers` não tem produtor (MetricsService.cs:868-876);
  - o Unsubscribe nativo pelo pipe.

## 3. Desenho

### 3.1 Fatos do código que decidem o desenho

- **F1. Cota por sujeito.**
  - O Gateway cobra um lease por par (sessão, ticker) quando entra um dono novo (SubscriptionRegistry.cs:118, 140).
  - A cota é contada pelo sujeito do certificado, sem distinguir maiúsculas (AuthenticatedSubject.cs:9-18; GatewaySubjectQuotaRegistry.cs:35-58; AdapterSubscriptionTests.cs:29-46).
  - Passar do teto lança `ResourceExhausted` antes de qualquer efeito no Host (GatewaySubjectQuotaRegistry.cs:50-55; AdapterSubscriptionTests.cs:29-46). `ProcessCommandsAsync` não captura a exceção (MarketDataService.cs:165-192), e por isso a chamada inteira termina (MarketDataService.cs:41-47, 63-87).
  - Os contadores são privados e não têm leitura (GatewaySubjectQuotaRegistry.cs:69-110). Um teste só vê o teto pela exceção.
  - Cada sujeito tem também 4 sessões vivas e 4 snapshots simultâneos (GatewayOptions.cs:49, 51). Uma sessão conta desde que nasce até sair (GatewaySessionManager.cs:53-82). Numa rotação, a sessão nova nasce antes de a velha sair (MarketDataService.cs:38, 74, 82).
  - Os valores por omissão podem ser mudados pela configuração de produção (RemoteGateway/appsettings.json:18-22), que o repositório não traz.
- **F2. Graça e herança.**
  - Quando um stream termina e a sessão era a última dona de um ticker, a assinatura fica 30 s como fantasma, e o lease continua a contar (SubscriptionRegistry.cs:221-246; GatewayOptions.cs:54-65). Uma sessão que não é a última dona sai na hora, sem fantasma (SubscriptionRegistry.cs:248-262).
  - Um stream novo do mesmo sujeito herda o fantasma sem pagar e, com as mesmas flags, sem chamar o Host (SubscriptionRegistry.cs:70-77, 347-367).
  - O dono de um fantasma é `LingerOwnerId` (SubscriptionRegistry.cs:16, 236-237). Um cancelamento de quem não é dono não faz nada (SubscriptionRegistry.cs:182-183). Para liberar um fantasma, um stream novo tem de o herdar primeiro, reenviando o ticker, e só depois cancelá-lo.
  - O cancelamento explícito do último dono devolve a cota e chama `UnsubscribeAsync` da fonte na hora (SubscriptionRegistry.cs:176-216, 445-450). A expiração da graça faz o mesmo (SubscriptionRegistry.cs:382-421). Esse `UnsubscribeAsync` apaga a intenção guardada mesmo com o pipe em baixo (PipeGatewayMarketSource.cs:217-229).
- **F3. Semáforo único e liberação depois dos comandos (leitura minha, sem teste).**
  - No fim de um stream, o Gateway espera a tarefa de comandos terminar e só depois libera o dono (MarketDataService.cs:63-74).
  - Todas as operações de todos os sujeitos passam por um único semáforo (SubscriptionRegistry.cs:20, 67, 179, 223, 386), que fica preso durante a chamada ao Host (SubscriptionRegistry.cs:102, 125, 144). A confirmação espera até 5 s (PipeGatewayMarketSource.cs:174-215; PipeClient.cs:219, 527-535), e o Gateway não muda esse prazo (RemoteGateway/Program.cs:28-35).
  - Os comandos de uma sessão nova podem, portanto, entrar antes da liberação da velha e pagar a cota em dobro. Uma adição lenta da faixa atrasa também as heranças e os snapshots do DataHub e do Mercado.
- **F4. A recusa derruba a sessão e deixa uma intenção órfã; um código desconhecido fica mudo.**
  - O Host descarta sem resposta um ticker fora de `^[A-Z0-9]{1,15}$` e qualquer pedido de um cliente que já tem 1000 tickers (NamedPipeServer.cs:143-144, 1256-1275).
  - Uma recusa que o Host responde como erro falha a confirmação na hora (PipeClient.cs:1438-1440). Só a falta de resposta espera os 5 s. Nos dois casos sai `UnconfirmedSubscriptionException` (PipeGatewayMarketSource.cs:205-210), que termina o stream (MarketDataService.cs:41-47, 85). A exceção não é `RpcException`, e o status que chega ao cliente não diz o ticker.
  - A intenção fica guardada em `_desiredSubscriptions` (PipeGatewayMarketSource.cs:183-186). Só sai de lá por um Unsubscribe da fonte (PipeGatewayMarketSource.cs:224), e o registro não o envia para um ticker sem dono (SubscriptionRegistry.cs:182-183).
  - Uma recusa nativa não põe trabalho no catch-up, porque todos os efeitos de F7 ficam dentro do ramo de sucesso (ProfitService.cs:1005-1006).
  - Um código que a DLL recusa de forma assíncrona não derruba nada. O Host só regista um aviso (ProfitService.cs:1783-1806), e a série fica muda.
- **F5. O Mercado tem um único duplex.**
  - A união de todas as conexões tem teto de 100 tickers (MarketStreamCoordinator.cs:44, 148-152).
  - O conjunto inteiro é reenviado a cada tentativa (MarketStreamCoordinator.cs:523-537).
  - Um erro que não seja rotação envia um terminal aos navegadores e reconecta 2 s depois (MarketStreamCoordinator.cs:473-481).
  - Uma rotação é um `DeadlineExceeded` depois de qualquer evento (MarketStreamCoordinator.cs:493-494). Todo stream começa com um evento vazio de anúncio (MarketDataService.cs:39; GatewaySessionManager.cs:83), que o Mercado conta como evento (MarketStreamCoordinator.cs:319-327). Uma rotação sem negócio nenhum continua, assim, a ser reconhecida.
  - Toda assinatura pede fita e livro (RemoteModels.cs:11-16; MarketStreamCoordinator.cs:536, 565).
  - Cada negócio vai para o `SessionCandleStore` (MarketStreamCoordinator.cs:349), que guarda 30 pregões em disco (SessionCandleStore.cs:84).
  - A conexão virtual `/macro-reading` está nessa mesma união (MarketTradeObservation.cs:40-67).
- **F6. O Host não desfaz a assinatura nativa vinda do pipe, e a sessão nativa dura o processo.**
  - O Unsubscribe do pipe só tira o filtro do cliente (NamedPipeServer.cs:1298-1317; ClientConnection.cs:341-348).
  - O cancelamento nativo existe só em `ProfitServiceBookScope.UnsubscribeOnOwner` (ProfitServiceBookScope.cs:55-104), e quem o chama é `ProfitService.Unsubscribe` (ProfitService.cs:1178-1194). O servidor de pipe só expõe `TickerSubscriptionRequested` (INamedPipeServer.cs:47). Não encontrei caminho do pipe até esse método.
  - Só `Disconnect` limpa `MarketState.Subscriptions` (ProfitService.cs:894, 939-954; MarketState.cs:105), e, pelo código lido, só o `Dispose` do serviço chama `Disconnect` (ProfitService.cs:878, 4480). A sessão nativa dura, por isso, o processo do Host, e `host_process_start_utc` (MetricsService.cs:927) marca o seu fim.
  - Depois de cancelada no Gateway, a série continua na DLL e no anel da Fita (ProfitService.cs:1658-1686). Continua também no canal geral de 50 000 e no histórico de 200 000 do pipe (NamedPipeServer.cs:270-273), onde cada mensagem sem assinante entra e só depois é descartada e contada (NamedPipeServer.cs:985-1019).
- **F7. Efeitos da primeira assinatura numa sessão nativa (ProfitService.cs:1004).**
  - *Entre 09:00 e 18:45, só pelo relógio, sem feriado* (TapeCatchUp.cs:10-11, 104-108). A assinatura enfileira o catch-up (ProfitService.cs:1018-1021). Sem marca de último negócio, que fica só em memória (HostTapeIngest.cs:50, 400-411), a janela começa às 09:00 (TapeCatchUp.cs:84-96) e é cortada em fatias de 5 min (Host/appsettings.json:16; TapeCatchUpScheduler.cs:266-280).
  - *Fora dessa janela* corre o `ForceLoadSessionData` (ProfitService.cs:1024). Antes da abertura ele carrega o pregão anterior inteiro; depois das 18:45, o pregão do dia inteiro (DailyBackfillPump.cs:127-145).
  - *Sempre:* um `GetHistoryTrades` do fechamento anterior, das 17:00 às 18:00 (ProfitService.cs:1029, 1126-1152); PriceDepth nativo com `BookScope=All` (ProfitService.cs:1034-1050), que é o valor por omissão (Host/appsettings.json:17); AdjustHistory (ProfitService.cs:1065).
  - *Na mesma sessão nativa*, assinar de novo não repete o catch-up, o DailyBackfill nem o fechamento anterior (ProfitService.cs:1004, 1016-1017, 1028-1029). Repete as chamadas nativas `SubscribeTicker`, PriceDepth e AdjustHistory (ProfitService.cs:1005, 1034-1050, 1065).
  - *Colisão com o fechamento anterior (leitura minha, sem teste).* O catch-up é enfileirado antes de o fechamento anterior reservar o histórico do mesmo ticker (ProfitService.cs:1021, 1029, 1132-1140), e o registro de histórico admite um só dono por ticker (HistoryRequestRegistry.cs:785-795). A primeira fatia de uma série nova pode, por isso, ser recusada e esperar 1 s ou 2 s dentro do dreno único (TapeCatchUpScheduler.cs:282-299).
- **F8. Fila do catch-up, fatias e recuperação da DLL.**
  - A fila tem teto de 64 pedidos. Acima dele, um pedido geral é recusado com `tape_catchup_owner_budget_exhausted` (TapeCatchUpScheduler.cs:61, 76-90). O dreno leva a fila inteira de cada vez (TapeCatchUpScheduler.cs:139-147), por isso o teto só morde quando chegam muitos pedidos enquanto ele espera, como numa rajada.
  - As fatias de arranque só correm com a fila de vãos recentes vazia (TapeCatchUpScheduler.cs:159-166). Escolhem a fatia com menos recusas e, entre essas, a de janela mais recente (StartupSliceQueue.cs:42-55). Só WINFUT, WDOFUT, DOLFUT e INDFUT têm prioridade (StartupSliceQueue.cs:32-49; PriorityCatchUpTickers.cs:9-15). Uma série nova tem a janela mais recente e passa à frente do reparo de arranque já em curso de um ticker do DataHub.
  - Há um só dreno (TapeCatchUpScheduler.cs:118-125) e uma só obra de catch-up de cada vez no owner (Host/appsettings.json:13; HostTapeIngest.cs:588-596).
  - Cada arranque declarado conta como `tape_live_gap startup_recovery` (TapeCatchUpScheduler.cs:278; HostTapeIngest.cs:569-578). Essa contagem serve de prova operacional de perda (docs/specs/0422-catchup-winfut-prioritario/SPEC.md:23-25).
  - Quando a DLL se recupera sozinha, o Host enfileira, numa rajada, catch-up para todo `MarketState.Subscriptions` (ProfitService.cs:1483-1492), incluindo as séries que a faixa já cancelou (F6).
- **F9. Pipe, livro e Fita.**
  - O Host publica o livro inteiro de cada instrumento alterado a cada 100 ms (docs/adr/host/0031-book-is-state-tape-is-stream.md:30-35).
  - Com `TapePipeOverflow=DropOldest` (Host/appsettings.json:11), livro e Fita dividem o canal geral, e a expulsão não chega ao cliente como lacuna (docs/adr/host/0034-tape-pipe-lane.md:18-21).
  - A entrega do catch-up para enquanto o canal geral tiver 1/8 da capacidade (TapeCatchUpLane.cs:108-109, 178), e o livro das séries entra nesse canal.
  - O PriceDepth de cada série entra na faixa de livro do owner, de teto 8 000, que descarta acima dele (ProfitDllOptions.cs:175; docs/adr/host/0030-market-callback-work-has-a-ceiling.md:43-51). Na abertura de 22/09 essa faixa já estava no teto (docs/adr/host/0030-market-callback-work-has-a-ceiling.md:52-56). É a mesma faixa do livro de WINFUT e INDFUT que o BookRecorder pode gravar (DataHubOptions.cs:318-322).
  - Os negócios das séries entram na mesma pista viva da Fita (ProfitService.cs:1674-1677; Host/appsettings.json:8). No owner, a Fita viva nunca é descartada (docs/adr/host/0030-market-callback-work-has-a-ceiling.md:52-56), e o transbordo da pista viva é lacuna explícita (BusinessTradeLane.cs:76-103).
  - A fila de despacho do Gateway espera quando enche, e por isso um handler lento trava a leitura do pipe (PipeClient.cs:77, 361-364).
- **F10. O Gateway repõe as intenções sozinho, antes de a graça acabar.**
  - `_desiredSubscriptions` sobrevive à queda do pipe (PipeGatewayMarketSource.cs:895-917). Com o pipe em baixo, uma assinatura fica guardada sem confirmação e sem erro (PipeGatewayMarketSource.cs:178-181, 191-205). Ao religar, o Gateway reenvia as intenções uma a uma (PipeGatewayMarketSource.cs:166-172, 232-263, 923).
  - A queda do pipe termina todos os streams com `Disconnected` (GatewaySessionManager.cs:261-283).
  - Um deploy do Host foi medido em 11,3 s, abaixo dos 30 s de graça (GatewayOptions.cs:59-62). A reposição corre logo na religação, por isso chega ao Host novo antes de os fantasmas expirarem. Esperar a graça não a evita.
  - Publicar e reiniciar o Host é autónomo a qualquer hora, inclusive no pregão (AGENTS.md:42-45; docs/adr/0050-publicacao-liberada-no-pregao.md:33). Um reinício do Host no pregão é, portanto, um evento normal.
- **F11. Métricas que o Portal já lê, e as que não lê.**
  - O Host publica `tape_catchup_queue` com `pending` e `startup_slices` (HostTapeIngest.cs:270-277), `tape_catchup_totals` com `timeouts` (HostTapeIngest.cs:278-280), `dll_connected`, `dropped_callback_work` e `unsubscribed_discards` (MetricsService.cs:851-857), `queue_capacity` e `queue_depth` do canal geral (MetricsService.cs:904-907), `pending_callback_work` (MetricsService.cs:911), `host_start_ordinal` e `host_process_start_utc` (MetricsService.cs:914-928), `client_outbound_live_trade_dropped_total` e `broadcast_live_trade_dropped_total` (NamedPipeServer.RuntimeMetrics.cs:146, 152).
  - `callback_age_<tipo>_ms` também é publicada (MetricsService.cs:961-964), mas pode ser cortada quando o mapa passa de 64 chaves (NamedPipeServer.RuntimeMetrics.cs:215-219).
  - O Portal recebe-as por `IHostStatusSource` (HostStatusSource.cs:101-104, 256-279), através de um cache de 25 s compartilhado com `/api/health` (HostStatusSource.cs:170, 323-332; GatewayHealthReplyCache.cs:18). O Gateway acrescenta um cache de 1 s (PipeGatewayMarketSource.cs:22).
  - Uma chave ausente conta como desconhecida (HostStatusSource.cs:42-44).
  - Nenhuma métrica expõe o tamanho de `MarketState.Subscriptions` (MetricsService.cs:868-876).
  - `tape_live_gap`, `tape_live_payload_unsaved`, `tape_live_admission_shed` e `tape_catchup_owner_budget_exhausted` só existem no diário do Host e em medidores (HostTapeIngest.cs:316-322, 360-393; TapeCatchUpScheduler.cs:83-88). Os medidores estão desligados por omissão (Host/appsettings.json:39).
- **F12. Entrega isolada, catch-up sem marca e objeto compartilhado com o DataHub.**
  - O Gateway filtra a entrega por sessão, ticker e família (GatewaySessionManager.cs:140-145, 151-154).
  - O DataHub assina um conjunto fixo (LiveIngestService.cs:19-32) e não recebe o que a faixa pede.
  - O negócio de catch-up sai como `Trade` comum, atrás da Fita viva (NamedPipeServer.cs:425-438), e o `TradeEvent` não tem campo que o distinga (farol_remote.proto:303-315).
  - O objeto U pode estar no conjunto vivo do DataHub, cujo cadastro de coleta o Portal lê por `ITickerAdminSource` (DataHubEndpoints.cs:19). Se a faixa e o DataHub forem donos de U e o stream do DataHub rodar, o DataHub sai sem fantasma (SubscriptionRegistry.cs:248-262). Um cancelamento explícito da faixa nesse intervalo tira U do filtro do pipe (SubscriptionRegistry.cs:445-450; NamedPipeServer.cs:1298-1317). Quando o DataHub volta a pedir U, o Host acha-o assinado e não faz catch-up (ProfitService.cs:1004, 1016-1017).
- **F13. Cadastro diário e forma do código.**
  - `ChainAsync` devolve a cadeia de D com `UnderlyingClose` (OptionDailyReader.cs:35-57). `UnderlyingClose` é o último preço do objeto na mesma data (B3DailyChainProjection.cs:39, 48-49).
  - A série traz `Expiry`, `Strike` anulável, `ReportedOpenInterest`, `TotalInterest`, `BestBid`, `BestAsk` e `TradeCount` (OptionDailySeries.cs:11-12, 19-20, 31-33). `BestBid` e `BestAsk` só existem quando a série tem linha de negócios em D, porque a cotação é juntada por essa linha (B3DailyChainProjection.cs:46-48).
  - Uma data pode estar publicada como `partial` (OptionDailyFiles.cs:25; B3DailyPublication.cs:72).
  - Cada `ChainAsync` pede uma Concessão nova ao DataHub e abre o DuckDB (OptionDailyConcessions.cs:14-27; OptionDailyReader.cs:35-52).
  - Essa leitura só existe com a funcionalidade DataHub ligada (DataHubEndpoints.cs:13-18, 28-32).
  - O Host deduz o Segmento F para bases com prefixo de futuro (TickerClassifier.cs:72-75, 184-209; NamedPipeServer.cs:1631-1635).
  - O Portal não referencia o Protocol. O precedente é espelhar o limite num literal e prendê-lo por uma cerca (BatchTickerStore.cs:240-246; TwinAuthorityTests.cs:154-163).
- **F14. Cercas e superfície do Portal.**
  - A navegação de opções reprova qualquer requisição que não seja `/api/features` ou `/api/health` (App.opcoes.test.tsx:43-51, 76-96). A prova Playwright faz o mesmo, exige o texto de placeholder em `#opcoes` e uma lista vazia de pedidos inesperados (e2e/opcoes-navigation.spec.ts:29-39, 67, 79).
  - A catraca Portal→Mercado é de 10 tipos (type-surface-ratchet.json:244). Cada registro de DI precisa de linha na `composition-allowlist` (composition-allowlist.json:2-20).
  - Os internos do Mercado só são visíveis a `Farol.Portal.Tests` (MercadoBoundaryTests.cs:18-20).
  - O censo T02 é lexical. Conta qualquer `.WriteAsync(`, `.AppendAsync(` ou `.CopyToAsync(` em `src/`, `scripts/` e `infra/` (PlmGcPhysicalWriterInventoryTests.cs:14; PhysicalWriterCensus.json:2), reprova arquivo novo sem classificação (PlmGcPhysicalWriterInventoryTests.cs:52-56) e corre no portão de integração (integrar.sh:572-574). Os streams gRPC do Mercado e o estado local do Portal já têm linhas `excluded` (WriterInventory/src.json:114-115, 118, 120).
  - Uma rota GET não mapeada cai no fallback do SPA e responde 200 com `index.html` (PortalComposition.cs:291). `/api/features` só expõe DataHub, Dev e Adm (PortalComposition.cs:261-266; PortalContracts.cs:485).
  - O glossário fixa um sentido por palavra (AGENTS.md:152). "Nível" é preço de referência do dia (CONTEXT.md:171-172), e "bolsa" deve ser evitada a favor de "Segmento" (CONTEXT.md:191-193).
- **F15. O duplex não confirma comandos.**
  - O `MarketEvent` não tem evento de confirmação de assinatura (farol_remote.proto:285-300).
  - O Gateway lê os comandos um a um e espera cada `AcquireAsync` antes do seguinte (MarketDataService.cs:165-192). O cliente escreve sem esperar resposta (PortalGatewayMarketClient.cs:129-151).
  - Quando uma confirmação esgota os 5 s (F3), a faixa já escreveu os comandos desses 5 s, e quem os processa é o mesmo laço em série.
- **F16. Nenhum `GapEvent` diz o ticker.**
  - O `GapEvent` só tem sequências, `resync_required`, contagem e motivo (farol_remote.proto:387-393), e `EnqueueGap` monta-o só com esses campos (GatewaySessionManager.cs:329-343).
  - O Gateway emite `state-version-gap` sem ticker (GatewaySessionManager.cs:164, 233), `slow-consumer-drop` sem ticker (GatewaySessionManager.cs:295), e `source-disconnected` ou `state-epoch-changed` para todas as sessões (GatewaySessionManager.cs:248-258).
- **F17. Identidade mTLS.**
  - Cada sujeito permitido exige, no Gateway, uma URI SPIFFE, um ou dois pinos SHA-256 e um estado de sobreposição (ClientCertificateIdentityPolicy.cs:24-63), além de um perfil de capacidades (GatewayIdentityCapabilities.cs:17-41). O certificado tem de ser folha, só com EKU clientAuth e com a URI SPIFFE exata (ClientCertificateValidator.cs:34-43).
  - O Gateway valida isto no arranque e lança se falhar (GatewayOptions.cs:137-147). ClientCertificateIdentityPolicy.cs:11-20 regista um crash-loop deste tipo em 29/08/2026.
  - No Portal, um perfil sem `ClientCertificatePath` e `ClientKeyPath` usa `.authority-client.crt` e `.authority-client.key`, o par do próprio Portal (AuthorityClientFactory.cs:22-24, 78-79).
  - O único adaptador do Mercado está fixo no perfil `Gateway` (MercadoModule.cs:29-31), e é esse adaptador que o construtor público de `PortalGatewayMarketClient` usa (PortalGatewayMarketClient.cs:33-40, 166).
  - A prova PKI de produção exige a mesma folha nos perfis Gateway, DataHub e Adm do Portal e não conhece outro perfil (pki_authority_runtime.py:170-175).
  - O repositório não traz os sujeitos de produção (RemoteGateway/appsettings.json:8-13).

Destes fatos saem as regras do desenho:
- A faixa fica fora do duplex do Mercado (F4, F5).
- A faixa assina cedo e só entre 09:02 e 18:00 (F7).
- O conjunto do dia muda o mínimo, porque cada série distinta fica na DLL até o Host encerrar (F6).
- Uma adição nova só sai a cada 6 s, depois de um portão de métricas frescas e de uma conta própria de fatias (F3, F8, F11, F15).
- Fora do aquecimento, a faixa não adiciona enquanto houver reparo de arranque pendente (F8).
- Depois de uma queda do pipe, a faixa libera as séries antes de o Host voltar (F2, F10).
- A faixa nunca cancela o objeto U explicitamente (F12).
- Toda lacuna é global (F16).

### 3.2 Componentes

| # | Componente | Onde | O que faz |
|---|---|---|---|
| 1 | Seletor puro | `src/Web/Farol.Portal/Modules/OptionLive/OptionLiveSelection.cs` (novo, `internal static`) | Aplica a regra da seção 3.3. Não usa relógio, I/O nem estado. Recebe a cadeia, o objeto, a camada, a data T, a âncora e as cotações para o centro por paridade, e devolve o plano ordenado com as flags de cada ticker. |
| 2 | Planejador | `.../OptionLive/OptionLivePlanner.cs` (novo, `BackgroundService`) | Lê a configuração e o calendário (TradingCalendar.cs:11-22). Lê a cadeia por `OptionDailyReader.ChainAsync` só às 08:45 e nas novas tentativas, e guarda-a em memória para o dia, porque cada leitura pede uma Concessão e abre o DuckDB (F13). Calcula o plano, aplica os portões e os orçamentos da seção 3.4 e entrega o conjunto desejado à faixa. Agenda as etapas 08:45, 09:02, 10:20 e 18:00. |
| 3 | Leitor de métricas | `.../OptionLive/OptionLiveHostMetrics.cs` (novo) | Chama `GatewayHealth.Check` pelo perfil `Gateway` do Portal, que já tem `health.read.v1` (PortalContracts.cs:491-498), sem o cache de 25 s (F11), e converte a resposta com `HostStatusSource.MetricsFrom` (HostStatusSource.cs:256-279). Lê a cada 5 s com adições pendentes e a cada 15 s no resto. Uma leitura é fresca quando o seu `ObservedAt` é mais novo que o da anterior e tem no máximo 15 s. |
| 4 | Estado do dia | `.../OptionLive/OptionLiveStateStore.cs` (novo) | Grava `option-live/AAAA-MM-DD.json` na pasta de `DataProtectionKeyPath`, por temporário e troca, como o diário da leitura macro (WriterInventory/src.json:120). Guarda o `host_process_start_utc`, o conjunto A das séries enviadas neste processo do Host, as reancoragens, as quarentenas, o disjuntor, as janelas de B_a e B_f, os últimos contadores de perda e a versão da configuração. Não grava Fita nem História. |
| 5 | Faixa de cotações | `src/Web/Farol.Mercado/Realtime/OptionQuoteLane.cs` (novo, `internal`, `BackgroundService`) | Abre um duplex próprio com uma instância própria de `PortalGatewayMarketClient`, construída com o adaptador do componente 9 (PortalGatewayMarketClient.cs:33-40). O cliente roda a cada 570 s (PortalGatewayMarketClient.cs:24-25). A faixa envia comandos com flags explícitas, que o cliente repassa (PortalGatewayMarketClient.cs:138-151), e Segmento vazio (farol_remote.proto:276-278). Põe os comandos num canal sem limite com `TryWrite`, porque nunca passam de 2C, e assim não acrescenta `.WriteAsync(` ao censo T02 (F14). Cancela antes de adicionar. Adições novas saem a uma por 6 s, depois do portão; reenvios do conjunto já mantido saem de uma vez. Guarda em memória só o topo do livro e o último negócio de cada ticker. Não usa `SessionCandleStore` nem SignalR. |
| 6 | Porta pública | Junto à faixa, no padrão de `IMarketTradeSource` (MarketTradeObservation.cs:14-38) | Expõe `IOptionQuoteLane` com `ApplyAsync(desejado, portão, ct)`, `Read(tickers)` e `Status`, os registros `OptionQuoteRequest(Ticker, IncludeBook, Priority)`, `OptionQuote` e `OptionQuoteLaneStatus`, e a extensão `AddOptionQuoteLane(autoridade)`, como `MarketTradeSourceComposition` (MarketTradeObservation.cs:30-37). A catraca Portal→Mercado sobe de 10 para o valor medido no build, por volta de 15 (type-surface-ratchet.json:244). |
| 7 | Rotas de leitura | `.../OptionLive/OptionLiveEndpoints.cs` (novo) | `GET /api/opcoes/ao-vivo/estado` devolve fase, estado, tipo de sujeito, orçamentos, plano, A, D_vivo, quarentenas e órfãs. `GET /api/opcoes/ao-vivo/{objeto}` devolve o quadro conflacionado. São mapeadas a partir de `DataHubEndpoints.Map` (DataHubEndpoints.cs:28-32) sempre que o DataHub está ligado, mesmo com a faixa desligada, para não caírem no fallback do SPA (F14). Com a faixa desligada, `/estado` responde `{"fase":"desligada"}` e `/{objeto}` responde 409 `options_live_off`. Exigem `PortalPolicies.Read` e seguem o `RunAsync` de OptionDailyEndpoints.cs:35-48. |
| 8 | Composição | `OptionLiveEndpoints.Add` e a extensão do Mercado | As rotas registam-se com o DataHub. O planejador, o leitor, o estado e a faixa só se registam com `Enabled=true`, com o DataHub ligado (DataHubEndpoints.cs:13-14) e fora de CanaryMode, como em RealtimeEndpoints.cs:23-27. Leva linhas novas na `composition-allowlist.json`. |
| 9 | Identidade e adaptador | `AuthorityTarget.GatewayOpcoes` e seção `Portal:Authorities:GatewayOpcoes` (AuthorityClientFactory.cs:8-13, 42-60); `PortalOutboundCapabilities.GatewayOpcoes`; um segundo adaptador `IMercadoAuthorityClients` ao lado de `PortalMercadoAuthorityClients` (MercadoModule.cs:29-31) | O perfil tem só `market.subscribe.v1` e `market.read.v1`, as capacidades de `Subscribe` e `GetSnapshot` (RemoteProtocol.cs:93-94; CapabilityInterceptor.cs:21-22). O adaptador devolve esse perfil em `GetGateway()` e é passado a `AddOptionQuoteLane`. A faixa só trata o sujeito como próprio quando o perfil tem `ClientCertificatePath` e `ClientKeyPath` explícitos e diferentes dos do perfil `Gateway`. Senão o sujeito é compartilhado, C fica ≤ 20 e F2 e F3 ficam recusadas (F17). Os passos de produção estão na seção 3.8. |
| 10 | Página | `ClientApp/src/modules/opcoes/OptionsLiveGridPage.tsx`, `optionsLiveGrid.ts` (modelo puro) e `useOptionsLiveGrid.ts` (leitura periódica) | Mostra, por vencimento, uma tabela com a call à esquerda, o strike ao centro e a put à direita. Cada lado tem compra, venda, tamanhos, último e idade, mais os dados de D (fechamento, contratos em aberto). Lê `/estado` primeiro e para quando a faixa está desligada. Depois lê a cada 1 s com a aba visível, recua para 5 s em erro e aborta ao desmontar, como `useMeusAgentesReading.ts:12-41`. Não importa nada de `mercado` nem de `ordens`. |
| 11 | Rota da grade | `App.tsx:89-93` | Só `optionsPages["opcoes"]` deixa de ser placeholder. |

Configuração, toda sob `Portal:OptionLive`:

| Chave | Omissão | Efeito |
|---|---|---|
| `Enabled` | `false` | Desligada: só as rotas se registam, e respondem `desligada`. |
| `Underlyings` | `[]` | Lista de pares {Ticker, Tier}. Uma lista vazia equivale a desligada. |
| `Phase` | `Sombra` | `Sombra`, `F1`, `F2` ou `F3`. A fase fixa o teto C (seção 3.7). |
| `Tiers` | T1: E1 w=3, E2 w=2; T2: E1 w=2 | Meia-largura w por vencimento e camada. |
| `WarmupAt` | 09:02 | Início do aquecimento. |
| `AdditionIntervalSeconds` | 6 | Intervalo mínimo entre adições novas. |
| `WarmupSliceBudget` | 240 | B_a, o orçamento de fatias do aquecimento. |
| `SliceBudgetPerHour` | 240 | B_f, o orçamento de fatias das adições fora do aquecimento, por 60 min. |
| `Reanchor` | ligado, 10:20, janela de 5 min, desvio mínimo de 2 posições, admissão até 11:20 | Reancoragem única (seção 3.3, item 10). |
| `StopAt` | 18:00 | Hora do encerramento, sempre antes das 18:45. |
| `MaxDailyAgeSessions` | 3 | Idade máxima de D em pregões. |
| `NativeSessionPregoes` | 5 | N_r, os pregões que uma sessão nativa dura, usado em D_max até à resposta à pergunta 5. |
| `Thresholds` | vazio | Limiares medidos na Sombra: p99 por hora de `pending_callback_work`, de Δ`dropped_callback_work` por minuto e de `callback_age_book_ms`. Vazio fecha o portão em F1 e acima. |
| `BreakerAcknowledgedFor` | vazio | O `host_process_start_utc` para o qual o dono rearmou o disjuntor. |

### 3.3 Regra de escolha das séries

As entradas são a cadeia de D, o objeto U com a sua camada, a data B3 de hoje T e a âncora. T vem de `TimeProvider` convertido por `B3Clock.Zone` (B3Clock.cs:13-14).

1. **Data D.** D é a data mais recente publicada como `available` (OptionDailyReader.cs:9-15; OptionDailyFiles.cs:25). Se a mais recente estiver `partial`, que é um estado aceite (B3DailyPublication.cs:72), usa-se a `available` anterior. Se nenhuma `available` estiver entre os `MaxDailyAgeSessions` pregões anteriores de `ITradingCalendar`, o estado passa a `base_parcial` ou `base_defasada`, e nada é assinado.
2. **Âncora.** A âncora é S_ref = `UnderlyingClose` de D (OptionDailyReader.cs:55-56). Se for nula ou não for positiva, o estado passa a `ancora_indisponivel` e nada é assinado para U.
3. **Objeto.** A raiz de U são os seus 4 primeiros caracteres. A configuração recusa no arranque uma raiz que comece por um prefixo de futuro (TickerClassifier.cs:72-75), porque o Host deduziria o Segmento F (TickerClassifier.cs:184-209).
4. **Elegibilidade.** Uma série só entra se cumprir todas as condições abaixo.
   - (a) O `series_id` casa `^([A-Z][A-Z0-9]{3})([A-X])(\d{1,3})(W[1-5])?$`, o mesmo padrão do Host (TickerClassifier.cs:44-47), e não tem o sufixo W. O código tem então no máximo 8 caracteres, abaixo do teto de 15 do Host (TickerShape.cs:30; NamedPipeServer.cs:144). Os códigos de 17 caracteres ficam fora.
   - (b) Os 4 primeiros caracteres são a raiz de U.
   - (c) O `Strike` não é nulo e é maior que zero (OptionDailySeries.cs:12).
   - (d) `Expiry ≥ T`, sempre pelo vencimento do cadastro, nunca por uma regra de calendário (OptionDailySeries.cs:11).
   - (e) A série deu sinal de vida em D: tem linha de negócios (`TradeCount`, `BestBid` ou `BestAsk` não nulo) ou `ReportedOpenInterest > 0` (OptionDailySeries.cs:19, 31-33). As cotações só chegam por essa linha (F13). O filtro reduz a chance de um código que a DLL não conheça. Um código assim não derruba o stream, fica mudo (F4), e o item 13 tira-o do plano.
5. **Vencimentos.** Entram E1 e E2, os dois menores `Expiry` distintos entre as séries elegíveis.
6. **Strikes.** Em cada vencimento contam só os strikes que têm call e put elegíveis. Entram os 2w+1 de menor distância absoluta entre K e S_ref, e o empate vai para o strike menor.
7. **Duplicatas.** Pode haver mais de uma série elegível para o mesmo (vencimento, strike, tipo). Nesse caso fica a de maior `TotalInterest` (OptionDailySeries.cs:20) e, em empate, a de menor `series_id`.
8. **Saída.** U vem primeiro, só com fita (`IncludeBook=false`). Depois vêm as séries, com fita e livro, ordenadas por camada, vencimento, strike e tipo (call antes da put). A prioridade de envio segue essa ordem, com os strikes mais próximos de S_ref primeiro. O **núcleo** de um objeto da camada 1 são as 6 séries de E1 com w=1.
9. **Larguras por omissão.**
   - Camada 1: 1 + 2·(2·3+1) + 2·(2·2+1) = 1 + 14 + 10 = **25** pertenças.
   - Camada 2: 1 + 2·(2·2+1) = **11** pertenças.
   - Camada 1 reduzida, só para F1 com sujeito compartilhado (E1 w=2, E2 w=1): 1 + 2·5 + 2·3 = **17** pertenças.
10. **Reancoragem única.**
    - *Sinais.* Às 10:20 calcula-se S_ab, a mediana dos negócios de U entre 10:15 e 10:20. A janela fica depois das 10:00, abertura das ações pelo contrato da B3 (sessionHours.ts:28, 59-67). Calcula-se também o centro por paridade: entre os strikes de E1 já assinados que têm compra e venda na call e na put, o código em que o meio da call menos o meio da put troca de sinal. Se o sinal for o mesmo em todos, a troca está fora da banda, do lado que o sinal indica.
    - *Gatilho.* Os itens 6 a 8 são refeitos com S_ab só se o centro por paridade estiver a 2 ou mais posições do centro de S_ref e S_ab apontar no mesmo sentido. Na data-ex, os strikes de D ainda não estão ajustados e os de hoje já estão. S_ab desloca-se pelo provento, mas o centro por paridade, contado em códigos, não, e a regra não dispara.
    - *Bloqueio.* Não há reancoragem se não houver negócio na janela, se a paridade só puder ser calculada em menos de 3 strikes, se os dois sinais discordarem, ou se |S_ab/S_ref − 1| > 15%. Este último caso sugere data-ex ou grupamento, e U fica marcado `suspeito_de_evento`.
    - *Limite.* Há uma reancoragem por objeto por pregão, guardada no estado do dia (componente 4). Um processo do Portal que arranque depois das 10:20 sem estado válido trata-a como gasta.
    - *Ordem e teto.* Primeiro saem as séries que deixam o plano. Depois entram as novas, do código mais próximo do centro novo para fora, camada 1 antes da camada 2, dentro de B_f, D_dia e D_max (seção 3.4.3) e só até às 11:20. O que não couber não entra no dia. Com F(10:20) = 16 e B_f = 240, cabem 15 séries na primeira hora. Um deslocamento de 2 strikes nos seis objetos da fase F2 pediria 36 (8 por objeto da camada 1 e 4 por objeto da camada 2).
11. **Estabilidade.** Fora da reancoragem, nada segue o preço ao vivo. A página avisa ("faixa ancorada em dd/mm" ou "às 10:20") quando a mediana dos últimos 30 s de U sai da faixa de E1.
12. **Determinismo.** Para a mesma (cadeia, T, âncora, configuração), o resultado é sempre o mesmo. Num reinício do Portal, o estado do dia diz que séries já foram enviadas neste processo do Host. Essas custam zero no Host, que não repete o catch-up, o DailyBackfill nem o fechamento anterior (ProfitService.cs:1004, 1016-1017, 1028-1029).
13. **Séries mudas.** Uma série sem nenhum evento (negócio ou livro) entre as 10:00 e as 10:30, ou nos 30 min seguintes à sua entrada se entrou depois, é cancelada e mostrada como `muda` até ao fim do dia. O custo nativo já foi pago; só se libera a pertença.

### 3.4 Orçamento de assinaturas, com a conta

#### 3.4.1 Cotas do Gateway

Notação:
- Q = 256 (GatewayOptions.cs:50);
- M = 100, a união do Mercado (MarketStreamCoordinator.cs:44);
- C = pertenças da faixa, contando séries e objetos;
- margem de 16 pertenças em todos os tetos.

| Situação | Pico | Fonte |
|---|---|---|
| Regime | C para a faixa e ≤ M para o Mercado | F1 |
| Rotação, caso normal | C. O dono velho libera, ficam fantasmas, e o stream novo herda sem lease. | SubscriptionRegistry.cs:231-246, 347-367 |
| Rotação, pior caso lido | 2C, se os comandos novos entrarem antes da liberação | F3 |
| Sessões vivas | 1 em regime; 2 se a sessão nova nascer antes de a velha sair | F1 |

A faixa reabre 6 s depois do fim de uma rotação. Os fantasmas duram 30 s (GatewayOptions.cs:65), por isso a herança continua garantida, e a sessão velha quase sempre já saiu. O reenvio tem de acabar em 10 s, ou seja, até 16 s depois do fim do stream velho.

Daqui saem os tetos seguros:
- **Sujeito próprio:** 2C ≤ 256 − 16, logo C ≤ **120**. Usa até 2 sessões e 2 snapshots, de 4 cada.
- **Sujeito compartilhado com o Mercado:** 2(M + C) ≤ 256 − 16, logo C ≤ **20**. Sessões: o Mercado usa até 2 numa rotação e a faixa 1, total 3 de 4. Snapshots: o Mercado usa 2 (MarketSnapshotQueue.cs:14) e a faixa 1, total 3 de 4. Só F1 aceita sujeito compartilhado.
- **Acima de 120:** só na fase F3, depois de o teste 6a medir R = pico − C. O teto passa a C ≤ 240 − R.

Os snapshots não contam como pertença (SubscriptionRegistry.cs:292).

| Fase | Composição | Pertenças |
|---|---|---|
| F1, sujeito compartilhado | 1 objeto da camada 1 reduzida | 17 ≤ 20 |
| F1, sujeito próprio | 1 objeto da camada 1 | 25 ≤ 120 |
| F2 | 3 objetos da camada 1 (3 × 25 = 75) + 3 da camada 2 (3 × 11 = 33) | 108 ≤ 120 |
| F3, exemplo | 3 da camada 1 com E1 w=5 e E2 w=3 (3 × 37 = 111) + 3 da camada 2 com E1 w=3 e E2 w=1 (3 × 21 = 63) | 174 ≤ 240 − R |

A reancoragem cancela antes de adicionar, por isso nunca aumenta o pico.

#### 3.4.2 Pipe do Host (1000 por cliente)

O Gateway é um único cliente do pipe, com teto de 1000 (NamedPipeServer.cs:143). A conta é:

- DataHub: cerca de 92 a 96 (GatewayOptions.cs:59);
- Mercado: até 100;
- faixa: até 120;
- snapshots: até 8.

O total é de no máximo **324**. Na fase F3 é de no máximo 444. Os dois valores ficam abaixo de 1000.

#### 3.4.3 Custo nativo e catch-up: o orçamento que de fato aperta

Uma série nova que ainda não tem marca de último negócio custa, à hora t do pregão:

- F(t) = ⌈(t − 09:00) / 5 min⌉ fatias de arranque, cada uma declarada como `tape_live_gap startup_recovery` (F7, F8);
- 1 `GetHistoryTrades` de uma hora do pregão anterior, que reserva o histórico do ticker e pode fazer a primeira fatia ser recusada, com 1 s a 2 s de espera no dreno único (F7);
- 1 PriceDepth nativo com `BookScope=All`, na faixa de livro de teto 8 000 do owner (F9);
- 1 AdjustHistory.

Exemplos de F(t): F(09:01) = 1, F(10:20) = 16, F(14:00) = 60, F(17:00) = 96.

Antes das 09:00 ou depois das 18:45, a mesma série custaria o pregão inteiro pelo DailyBackfill (F7). Por isso a faixa nunca assina fora de 09:02–18:00.

**A faixa é um consumidor novo do catch-up.** Só os vãos recentes têm precedência sobre ela (TapeCatchUpScheduler.cs:159-166). As fatias de uma série nova têm a janela mais recente e passam à frente do reparo de arranque de um ticker do DataHub (F8). As regras abaixo existem para que isso só aconteça no aquecimento, quando não há reparo pendente.

**Ritmo.** Uma adição nova sai a cada 6 s, no aquecimento e depois. Há três razões:
- A confirmação do Host espera até 5 s, e o duplex não confirma comandos (F3, F15). Com 6 s, a causa de uma queda é a última ou a penúltima adição enviada.
- Cada adição prende o semáforo único do registro durante a ida ao Host (F3). Com 6 s e uma ida de até 1 s, a faixa ocupa no máximo 17% desse semáforo.
- Cada primeira fatia recusada pode parar o dreno 1 s a 2 s (F7). Com 6 s, o dreno fica livre pelo menos dois terços do tempo.

Os reenvios do conjunto já mantido (rotação, reconexão sem troca de processo do Host, reinício do Portal com estado válido) saem de uma vez, sem ritmo nem portão. Herdam fantasmas ou reassinam na mesma sessão nativa, sem custo no catch-up (F2, F7). As reentradas de custo zero que não herdam fantasma saem até 2 por segundo.

**Aquecimento (B_a).**
- Começa às 09:02, fora do primeiro minuto dos futuros, com os objetos primeiro e depois as séries por prioridade.
- Só começa com uma leitura fresca em que `pending = 0` e `startup_slices = 0`. Enquanto não houver, espera.
- A soma de F(t) das adições do aquecimento não passa de B_a = 240. Se o aquecimento começar tarde, entram só as primeiras séries por prioridade, com o núcleo primeiro, até B_a. Depois das 10:00 não há aquecimento.
- Conta, com uma adição a cada 6 s a partir das 09:02 (120 + 6i s depois das 09:00):
  - F1 com sujeito compartilhado (17): termina às 09:03:36, tudo com F = 1, 17 fatias.
  - F1 com sujeito próprio (25): termina às 09:04:24, tudo com F = 1, 25 fatias.
  - F2 (108): 31 adições com F = 1, 50 com F = 2 e 27 com F = 3, total de 212 fatias; termina às 09:12:42.
  - C = 120: a soma chegaria a 248. Entram 117 (239 fatias), e as três últimas da camada 2 ficam fora do dia.

**Adições depois do aquecimento (B_f).**
- Só saem com uma leitura fresca em que `pending = 0` e `startup_slices = 0`, e sem adição própria desde o `ObservedAt` dessa leitura. Assim a faixa nunca disputa o reparo de arranque do DataHub.
- A soma de F(t) das adições dos últimos 60 min, mais a da nova, cabe em B_f = 240. Na reancoragem das 10:20 isso dá 15 séries na primeira hora. Uma série que volta na mesma sessão nativa custa zero, e o planejador conta-a como zero (F7).
- Depois de uma troca de processo do Host às 14:00 (F = 60), B_f admite 4 séries nessa hora, 3 na das 15:00, 2 na das 16:00 e 2 na das 17:00, cerca de 11 até às 18:00. Na prática, um reinício do Host a partir das 10:30 deixa a faixa quase desligada no resto do dia.

**Conta própria de fatias (pré-portão).** A leitura das métricas tem idade, e por isso a faixa soma F(t) de cada adição desde o `ObservedAt` da última leitura fresca. No aquecimento, uma adição só sai se `startup_slices` lido + soma própria + F(t) da nova ≤ 50. Fora do aquecimento, a regra de B_f acima já exige soma própria zero. A versão anterior dizia que as fatias da própria faixa a freavam no aquecimento; com o cache de 25 s (F11), isso não se sustentava.

**Portão.** Lido pelo componente 3. Uma adição nova não sai com qualquer destas condições:
- leitura ausente, falhada ou com mais de 15 s;
- `dll_connected` diferente de `true` (MetricsService.cs:851);
- `pending ≥ 8` ou `startup_slices > 50` no aquecimento, ou `pending > 0` ou `startup_slices > 0` fora dele (HostTapeIngest.cs:273-277);
- `queue_depth ≥ queue_capacity/16`, metade da marca em que a entrega do catch-up para (TapeCatchUpLane.cs:108-109, 178; MetricsService.cs:904-907);
- `pending_callback_work` acima do limiar da Sombra para a mesma hora, em duas leituras seguidas (MetricsService.cs:911);
- `callback_age_book_ms`, quando presente, acima do limiar da Sombra (MetricsService.cs:961-964);
- Δ`timeouts` de `tape_catchup_totals` maior que zero desde a leitura anterior (HostTapeIngest.cs:278-280).

O portão reabre com as condições limpas e, no aquecimento, com `startup_slices ≤ 25`. Sem limiares da Sombra, fica fechado em F1 e acima.

**Séries distintas na DLL.**
- A é o conjunto das séries que a faixa enviou desde o `host_process_start_utc` atual, guardado no estado do dia. A sessão nativa dura o processo do Host (F6), por isso esse marcador basta. Uma série recusada pela DLL não custa nada no catch-up (F4), e contá-la em A só sobrestima.
- D_vivo são as séries de A ainda não vencidas. São as que mandam livro e negócios para o canal geral mesmo canceladas (F6). As vencidas só ocupam assinatura na DLL e aparecem à parte em `/estado`.
- **D_dia = 1,5·C** é o teto de séries distintas no pregão.
- **D_max = C + T_troca + d·N_r** é o teto de D_vivo. T_troca são as séries novas que a próxima troca de vencimento exige. d é a deriva diária, medida na Sombra e no teste 12. N_r é `NativeSessionPregoes`. As séries da troca de vencimento têm reserva: só as da reancoragem param no teto. Ao chegar a qualquer dos tetos, o estado fica `teto_nativo`.
- Conta com as larguras por omissão e d estimado com um strike por dia:
  - F1 com sujeito próprio: T_troca = 14 (o antigo E2 vira E1 com w=3, +4; entra um E2 novo, +10), d = 4, D_max = 25 + 14 + 20 = 59.
  - F1 com sujeito compartilhado: T_troca = 10, d = 4, D_max = 17 + 10 + 20 = 47.
  - F2: T_troca = 3·14 + 3·10 = 72, d = 3·4 + 3·2 = 18, D_max = 108 + 72 + 90 = 270. Com o teto antigo de 2C = 216 e sem reserva, a troca levaria F2 ao teto em 2 pregões (108 + 72 + 18n ≥ 216 dá n ≥ 2) e bloquearia o E2 novo.
- A carga real das séries fora do plano mede-se por Δ`unsubscribed_discards` por hora contra a Sombra e por `queue_depth` (MetricsService.cs:856-857, 904-907), porque cada mensagem delas entra no canal e no histórico antes de ser descartada (F6).
- O limite real da DLL é desconhecido (knowledge/api/functions/subscriptions.md:233). O total de assinaturas nativas, somando os outros clientes, não é observável (F11) até à D1f.

#### 3.4.4 Snapshots e lacunas

- **Sem snapshot no aquecimento.** Antes das 10:00 há poucos negócios de ações, e o livro das séries pode estar vazio ou só com ofertas de leilão; a coleta do Segmento B começa às 09:30 para apanhar o leilão de abertura (B3MarketSession.cs:4-7, 36-38). O Host não responde sem retrato (NamedPipeServer.cs:1335-1349), e cada `GetSnapshot` pode esperar 4 tentativas de 5 s (SubscriptionRegistry.cs:10, 296-305; PipeGatewayMarketSource.cs:318). O livro chega por substituição inteira quando muda (F9).
- **Nenhum snapshot depois de uma rotação.** A sessão nova herda os fantasmas, e o livro chega por substituição (F2, F9). A página mostra a idade.
- **Toda lacuna é global.** Como nenhum `GapEvent` diz o ticker (F16), qualquer lacuna põe todos os livros em `nao_reconfirmado`. Com `slow-consumer-drop`, o último negócio de todas as séries fica `incerto`. A faixa espera a substituição natural.
- **Snapshots só no núcleo.** Só as séries da camada 1, E1, que continuem `nao_reconfirmado` 60 s depois de uma lacuna recebem pedido de snapshot. A concorrência é 1 com sujeito compartilhado e 2 com sujeito próprio, e saem no máximo 6 pedidos por minuto. Uma série cujo snapshot voltou sem retrato não é pedida de novo até à lacuna seguinte.
- **Conflação na receção.** A faixa reduz cada `BookReplacementEvent` ao topo do livro logo ao recebê-lo. A fila da sessão tem 4 096 mensagens e 16 MiB (GatewayOptions.cs:45-46), e o descarte nela vira `slow-consumer-drop` (GatewaySessionManager.cs:295, 329-343).

#### 3.4.5 Último negócio

- O último negócio de cada ticker é o de maior par (`timestamp_unix_microseconds`, `trade_number`), nunca o último a chegar, porque o catch-up chega atrasado e sem marca (F12).
- Um negócio com `is_edit` atualiza o registro do mesmo `trade_number` e não cria um último novo.

### 3.5 Ciclo de vida

1. **Desligada.** É o estado fora dos dias de pregão de `ITradingCalendar`. O Host não consulta feriados (TapeCatchUp.cs:104-108), e por isso a faixa tem de o fazer. A faixa também fica desligada em CanaryMode, com o DataHub desligado ou com `Enabled=false`. Com o DataHub ligado, as rotas respondem `desligada`.
2. **Planejando (08:45).** O planejador lê o estado do dia, lê a cadeia de cada objeto pela Concessão (OptionDailyConcessions.cs:14-27) uma vez, guarda-a para o dia, calcula o plano e publica-o em `/estado`. Não envia nada. Se a base não estiver disponível, tenta de novo a cada minuto. O aquecimento só começa se couber em B_a, e depois das 10:00 o dia fica desligado.
3. **Aquecendo (a partir das 09:02).**
   - Começa às 09:02 também na Quarta de Cinzas, porque a janela do Host é só de relógio (TapeCatchUp.cs:104-108). A janela de coleta da B3 abre às 12:30 nesse dia (B3MarketSession.cs:33-38), mas o custo F(t) continua a contar desde as 09:00.
   - Espera uma leitura fresca com o catch-up vazio. Depois abre o duplex e assina os objetos e as séries por prioridade, uma a cada 6 s, com o portão, a conta própria e B_a.
   - Não pede snapshots.
4. **Ativa.**
   - A cada 570 s o duplex roda. A faixa reabre 6 s depois e reenvia de uma vez o mesmo conjunto com as mesmas flags, herdando os fantasmas (F2).
   - O planejador não muda o plano nos 35 s antes e depois de uma rotação, que é a graça de 30 s mais margem.
   - O livro de cada série fica `nao_reconfirmado` até chegar uma substituição ou um snapshot.
5. **Reancorando (10:20).** Aplica a seção 3.3, item 10.
6. **Congelada.** Nesta fase só há cancelamentos, nenhuma adição. Entra-se nela por portão fechado, B_f esgotado, `teto_nativo`, mais de 4 quarentenas no dia ou disjuntor (seção 3.6).
7. **Encerrando (`StopAt`, 18:00 por omissão).**
   - A faixa cancela explicitamente todas as séries, da camada 2 para a camada 1, e nenhum objeto U (F12). Depois fecha o duplex. Cada U passa a fantasma e sai 30 s depois pela graça, que apaga a sua intenção (F2).
   - O cancelamento explícito tira as séries de `_desiredSubscriptions` (PipeGatewayMarketSource.cs:224), mas só as que têm dono no registro (SubscriptionRegistry.cs:182-183). Uma série órfã não tem dono (F4).
   - Por isso a faixa abre, até às 18:10, um stream de limpeza só para as séries em quarentena: envia o Subscribe e, 6 s depois, o Unsubscribe. Se o Host confirmar, a série ganha dono, e o Unsubscribe apaga a intenção. Se não confirmar, o stream de limpeza cai, e a série fica publicada em `/estado` como órfã residual. Uma órfã residual volta a ser assinada numa religação noturna do pipe, com o DailyBackfill do pregão inteiro (F7, F10), até à D1d.
   - A assinatura nativa fica (F6). No dia seguinte, no mesmo processo do Host, as séries repetidas custam zero.
8. **Reconectando.** Ver a seção 3.6.
9. **Reinício do Portal.** Ver a seção 3.6. O estado do dia é gravado a cada mudança de A, das reancoragens, das quarentenas, do disjuntor e das janelas de orçamento, no máximo uma vez por adição.

### 3.6 Falhas

| Evento | Sinal | Reação |
|---|---|---|
| Rotação do prazo | `DeadlineExceeded` depois de qualquer evento, inclusive o anúncio vazio que abre todo stream (F5). Vale também antes das 10:00, sem negócios. | A faixa reabre 6 s depois com o mesmo conjunto e as mesmas flags, reenviado de uma vez em até 10 s, e não muda o plano durante 35 s. Não pede snapshots. |
| Cota esgotada | `ResourceExhausted` (F1) | A faixa cancela as séries da camada 2 e espera 5 s, 10 s, 20 s, e assim por diante, até 5 min, com jitter. Fica no estado reduzido pelo menos 30 min. Nunca entra num laço de 2 s, ao contrário de MarketStreamCoordinator.cs:473-481. |
| Stream cai com status desconhecido | `UnconfirmedSubscriptionException` no Gateway (F4) | Primeiro, a faixa lê uma métrica fresca com `ObservedAt` posterior à queda. Se `dll_connected` não for `true` ou se `pending_callback_work` estiver acima do limiar, a culpa é do Host: nenhuma série fica suspeita, o intervalo das adições dobra até 24 s, e o conjunto é reenviado. Senão, ficam suspeitas as adições novas enviadas nos 12 s antes da queda, no máximo duas com o ritmo de 6 s. Voltam por último, uma a cada 6 s. Uma suspeita que derrube de novo fica em quarentena até ao fim do dia. Com mais de 4 quarentenas no dia, a faixa congela. Uma queda durante reentradas de custo zero não cria suspeitas. Cada queda prende o semáforo do Gateway até 5 s (F3), e esta regra limita as quedas a cerca de três por série ruim. |
| Pipe caiu | `StreamTerminal Disconnected` (F10) | 1) A faixa reabre 1 s depois, para o Gateway acabar de liberar a sessão velha (F3). 2) Reenvia os objetos U e, para cada série do conjunto anterior, um Subscribe seguido logo de um Unsubscribe, sem ritmo nem portão. Isso herda o fantasma e apaga a intenção enquanto o pipe está em baixo (F2), e o Gateway deixa de a repor no Host novo. 3) Espera uma métrica fresca com `ObservedAt` posterior à queda e `dll_connected=true`. 4) Se `host_process_start_utc` não mudou, reenvia o plano de uma vez, sem custo no catch-up (F7). Se mudou ou é desconhecido, A esvazia, e as séries voltam como adições novas sob o portão e B_a ou B_f, com o núcleo primeiro. Custo que sobra: F(t) por objeto U que o DataHub não coleta, mais as séries que a corrida deixar passar se o Host voltar antes do passo 2; as duas contagens aparecem em `/estado`. |
| Gateway parou ou a ligação HTTP caiu | Fim do stream sem `Disconnected`, por exemplo `Unavailable` | A faixa reabre com recuo de 2 s, 4 s, 8 s, até 60 s. Não faz o passo 2 da linha anterior, porque com o pipe de pé um Subscribe de série chegaria ao Host. Lê a métrica fresca e segue o passo 4. |
| Gateway fora por muito tempo | Falhas seguidas durante mais de 5 min | O quadro fica `indisponivel`, com a idade explícita. |
| Lacuna | Qualquer `GapEvent` (`state-version-gap`, `slow-consumer-drop`, `source-disconnected`, `state-epoch-changed`), que nunca diz o ticker (F16) | Todos os livros passam a `nao_reconfirmado`. Com `slow-consumer-drop`, o último negócio de todas as séries passa a `incerto`. A faixa espera a substituição natural e só pede snapshots pela regra da seção 3.4.4. Com mais de 3 `slow-consumer-drop` por minuto, cancela as séries da camada 2. |
| A Fita perde (disjuntor) | Com a faixa ativa: Δ`client_outbound_live_trade_dropped_total` > 0, Δ`broadcast_live_trade_dropped_total` > 0, Δ`dropped_callback_work` por minuto acima do limiar da Sombra, ou `queue_depth` ≥ `queue_capacity`/8 em duas leituras seguidas (F9, F11) | A faixa congela até à próxima mudança de `host_process_start_utc` ou até o dono a rearmar por `BreakerAcknowledgedFor`. Cancela as séries da camada 2 e regista a hora, para comparar com as lacunas do DataHub. Cancelar não descarrega o Host (F6), e o Portal não pode reiniciá-lo (docs/adr/0040-ingestao-fita-isolada.md:57-58). As perdas dentro do Host, na pista viva e na faixa de livro, não chegam ao Portal (F11); são lidas do diário do Host no CA10, depois do fato. |
| Owner do Host saturado | `pending_callback_work` acima do limiar da Sombra durante 2 min | A faixa congela. |
| Métricas ausentes ou velhas | Leitura falhada, chave ausente (HostStatusSource.cs:42-44) ou leitura com mais de 15 s | O portão fecha, e o que já está assinado continua. |
| Base diária indisponível | 503 `options_unavailable` (OptionDailyEndpoints.cs:43-47) | Novas tentativas a cada minuto. O aquecimento só começa se couber em B_a, e depois das 10:00 o dia fica desligado. |
| Reinício do Portal | Processo novo | O planejador recalcula o mesmo plano e lê o estado do dia. Com estado válido para o pregão e para o `host_process_start_utc` atual, as séries de A reentram de uma vez, sem custo no catch-up, e a reancoragem, as quarentenas, o disjuntor e as janelas de orçamento continuam. Sem estado válido, a faixa falha fechada: A fica vazio, a reancoragem conta como gasta se já passou das 10:20, e o disjuntor fica armado se os contadores de perda do pipe forem maiores que zero. |
| Recuperação da DLL sem queda do pipe | Nenhum sinal a tempo. O Host enfileira catch-up para todo `MarketState.Subscriptions` (F8). | Não há reação possível no Portal. É risco aceite pelo dono antes de F1 (pergunta 6), medido pelo teste 13. |
| CanaryMode ou dev loop sem Gateway | RealtimeEndpoints.cs:23-27; o dev loop lança o Portal só com a autoridade do DataHub (farol-dev.sh:347-357) | Com `Enabled=false`, só as rotas se registam, e respondem `desligada`. Com `Enabled=true` e sem Gateway, o quadro fica `indisponivel` sem erro. |

### 3.7 Fases de entrada

| Fase | Sujeito | C | Condição para entrar |
|---|---|---|---|
| Sombra | — | 0 | `Enabled=true`. O plano é calculado, publicado e registrado em log, e nada é assinado. Dura 5 pregões e mede a base fixa do CA10 e os limiares do portão (`Thresholds`). |
| F1 | compartilhado (C ≤ 20) ou próprio (C ≤ 25) | ≤ 25 | A Sombra correu sem erro de plano e fixou os limiares. O dono respondeu às perguntas 5 a 7, e as respostas ficaram na nova SPEC como aceitação explícita do efeito sobre o catch-up do ADR-0040, com a decisão sobre um ADR que o reabra. O teste 13 foi medido. O dono acompanha o primeiro pregão. |
| F2 | próprio, com perfil explícito | ≤ 120 | 5 pregões de F1 com o CA10. Os passos da seção 3.8 estão feitos. O teste 6b passou. As recusas da primeira fatia por série foram contadas em F1 pelo log `tape_catchup_slice` (TapeCatchUpScheduler.cs:323). O dono decidiu sobre a D1d. |
| F3 | próprio | ≤ 240 − R | O teste 6a mediu R. Houve 10 pregões de F2 com o CA10. A D1f existe, e o dono respondeu à pergunta 5 sobre o teto da DLL. |

### 3.8 Passos de produção do sujeito próprio (do dono)

1. Emitir o certificado de cliente `CN=farol-portal-opcoes` como folha, com a URI SPIFFE num dos domínios aceites e EKU só clientAuth (ClientCertificateIdentityPolicy.cs:21-22; ClientCertificateValidator.cs:34-43).
2. No Gateway, acrescentar o sujeito em cinco chaves, todas obrigatórias, ou o Gateway não arranca (F17): `AllowedClientSubjects`, `ClientSpiffeUris`, `ClientCertificateSha256Pins` (um ou dois pinos), `ClientCertificateOverlapExpiresAtUtc` e `IdentityCapabilities` com `market.subscribe.v1` e `market.read.v1`.
3. Ensaiar a configuração candidata antes de a instalar, por exemplo carregando-a num teste local em `GatewayOptions` e chamando a validação de GatewayOptions.cs:130-147. Um erro nela derruba o Gateway e, com ele, a Fita do DataHub, as abas e os alertas.
4. Reiniciar o Gateway com rollback pronto: repor o arquivo anterior e reiniciar.
5. No Portal, configurar `Portal:Authorities:GatewayOpcoes` com `ClientCertificatePath` e `ClientKeyPath` explícitos. Sem eles, o perfil cairia no par do Portal (F17), e a faixa trata o sujeito como compartilhado.
6. Atualizar a prova PKI para conhecer o quarto perfil e a sua folha própria (pki_authority_runtime.py:170-175).

## 4. O que não muda

- **Caminho congelado (ADR-0040).**
  - O ADR congela, no Host, `OnTradeV2Managed`, o diário e o catch-up de vão, e, no DataHub, `LiveIngestService`, `LiveSessionWriter` e `CommitAsync` (docs/adr/0040-ingestao-fita-isolada.md:41-44). Nenhum desses códigos muda. Também não mudam `LiveIngestChannel` (LiveIngestChannel.cs:9) e `TapeMinuteGapMeter`, que não estão na lista do ADR mas ficam no mesmo caminho.
  - A faixa é, porém, um consumidor novo do catch-up. Cada primeira assinatura no pregão enfileira trabalho (ProfitService.cs:1018-1021). Cada série acumulada entra na reposição de uma recuperação da DLL (ProfitService.cs:1483-1492). Os negócios das séries entram na pista viva (ProfitService.cs:1674-1677). O Mercado já entra por este caminho quando um navegador pede um ticker novo (MarketStreamCoordinator.cs:561-565), porque o Host trata igual qualquer pedido do pipe (NamedPipeServer.cs:1256-1290). Se isto é "feature nova neste caminho" no sentido do ADR é decisão do dono, tomada antes de F1 (pergunta 6).
  - Só os vãos recentes passam à frente da faixa; o reparo de arranque não passa (F8). Por isso, fora do aquecimento, a faixa só adiciona sem reparo de arranque pendente (seção 3.4.3).
  - Ruído aceite: com a faixa ativa, `tape_live_gap startup_recovery` e o medidor `TapeLiveGaps` crescem cerca de C por pregão (HostTapeIngest.cs:569-578), e isso não é perda. Quem usa essa contagem como prova (docs/specs/0422-catchup-winfut-prioritario/SPEC.md:23-25) tem de excluir as linhas `startup_recovery` dos tickers da faixa.
  - O Portal continua sem reiniciar o Host e sem escrever Fita (docs/adr/0040-ingestao-fita-isolada.md:57-58).
- **Host.**
  - Não muda nenhum arquivo de `Host/`, nem a configuração. `Host.Tests` ganha só os casos do teste 13.
  - `BookScope`, `TapePipeOverflow`, a fila de 64 e o teto de 1000 por cliente ficam como estão.
- **Gateway, transporte e contratos.**
  - Não há código novo em `src/Gateway/`, `src/Transport/` nem `src/Contracts/`, nem descritor gRPC novo. `RemoteSurfacePolicy` não entra em jogo (RemoteSurfacePolicy.cs:10-18). Os testes do Gateway ganham só casos (teste 6).
  - O único ajuste é de configuração de produção, para o sujeito novo, e só se o dono o escolher (seção 3.8).
- **DataHub como único escritor da História** (docs/adr/0013-data-ownership-and-storage.md:42-44).
  - As séries não entram no TICKADM nem no conjunto do `LiveIngestService` (LiveIngestService.cs:19-24).
  - A faixa grava só o seu estado do dia, na pasta de estado do Portal, fora da raiz da História e da Concessão. O censo T02 ganha uma linha `excluded` para esse arquivo, como as do estado local do Portal (WriterInventory/src.json:118, 120), e nenhum dono novo.
  - Os negócios das séries só chegam à sessão da faixa (F12).
- **Caminho de ordens** (AGENTS.md:7-36, 112).
  - A faixa só usa `Subscribe` e `GetSnapshot`, que exigem `market.subscribe.v1` e `market.read.v1` (CapabilityInterceptor.cs:21-22). O leitor de métricas só usa `GatewayHealth.Check`.
  - Nenhum arquivo novo usa os tokens que `NoOrderCallerTests` fixa, nem importa de `ordens`, nem cria capacidade `order.*`.
- **Mercado.**
  - `MarketStreamCoordinator`, `MarketHub`, `SessionCandleStore`, o teto de 100 e a rotação ficam como estão. `PortalGatewayMarketClient` é reutilizado sem mudança.
  - A cerca de módulos do navegador não muda (moduleBoundaries.test.ts:49-60).
- **Biblioteca `Modules/Options`.** Continua sem relógio nem fonte de dados.

## 5. Testes, todos sem mercado aberto

1. **Seletor:** `tests/Web/Farol.Portal.Tests/OptionLive/OptionLiveSelectionTests.cs`, sobre `OptionDailyFixture` (OptionDailyFixture.cs:12). Cobre:
   - o conjunto e a ordem exatos, por camada;
   - o empate de strike;
   - a exclusão de séries vencidas, de 17 caracteres, na forma C/P, semanais, de raiz diferente, com strike nulo ou sem linha de negócios nem contratos em aberto;
   - as duplicatas;
   - a âncora nula, a base defasada e a data `partial` (usa a `available` anterior);
   - menos de dois vencimentos;
   - uma propriedade: para cadeias aleatórias, o resultado é determinístico e tem no máximo o teto da camada.
2. **Reancoragem e orçamentos.** Cobre:
   - o limiar de 2 posições e o critério duplo (paridade e S_ab no mesmo sentido);
   - uma fixture de data-ex, com strikes de D sem ajuste e cotações já ajustadas, que não reancora;
   - uma reancoragem por pregão e o caso `suspeito_de_evento`;
   - cancelar antes de adicionar, e a admissão só até às 11:20;
   - B_a com início tardio, B_f, D_dia e D_max com a reserva da troca de vencimento, sobre uma trajetória sintética de S.
3. **Planejador**, com `FakeTimeProvider`, calendário falso e leitor de métricas falso. Cobre:
   - nenhum comando antes das 09:02, depois de `StopAt` ou em feriado;
   - nenhuma adição com o portão fechado, com a métrica ausente ou velha, com `startup_slices > 0` fora do aquecimento ou com `queue_depth ≥ queue_capacity/16`;
   - a conta própria: às 10:20, nenhuma segunda adição antes de uma leitura fresca;
   - um roteiro das 09:02 às 10:00 só com anúncios de sessão e nenhum evento de mercado: rotações reconhecidas, nenhuma suspeita e nenhum `indisponivel`;
   - às 18:00, um cancelamento explícito de todas as séries e de nenhum objeto, e o stream de limpeza só para as quarentenas.
4. **Faixa com Gateway falso.** `IPortalGatewayMarketClient` (IPortalGatewayMarketClient.cs:6-14) é visível aos testes do Portal (MercadoBoundaryTests.cs:18-20). O falso lê os comandos em série, com escrita em buffer e confirmação de até 5 s. Os roteiros cobrem:
   - a rotação, que reenvia o mesmo conjunto com as mesmas flags em até 10 s;
   - `ResourceExhausted`, sem nova tentativa antes de 5 s;
   - uma série ruim entre 120, em quarentena em até 3 reinícios; e uma queda com a métrica a mostrar o Host lento, sem quarentena nenhuma;
   - `Disconnected`: Subscribe e Unsubscribe de cada série antes de qualquer leitura de métrica, nenhum Unsubscribe de U, e depois os dois ramos, com e sem troca de `host_process_start_utc`;
   - qualquer `GapEvent` tratado como global, e os snapshots só no núcleo, com teto por minuto;
   - o último negócio quando chega um catch-up atrasado, e o caso `is_edit`;
   - a série muda depois das 10:30.
5. **Isolamento no Portal.** No mesmo processo, uma falha forçada da faixa não termina o stream do `MarketStreamCoordinator`, no padrão de ProgressiveSubscriptionTests.cs:14.
6. **Gateway real, em processo**, em `tests/Gateway/Farol.RemoteGateway.Tests`, só com casos novos e sem tocar no código do Gateway:
   - **6a, cota.** Usa o `MarketDataService` real, como MarketDataSubscribeIdleRateLimitTests.cs:30-37, e `Harness/FakeGatewaySource.cs` a segurar uma assinatura 5 s. Abre duas chamadas `Subscribe` seguidas do mesmo sujeito com C tickers, a segunda enquanto a primeira libera. Como os contadores não têm leitura (F1), R é achado por bisseção: R é o menor r em que `MaxSubscriptionMembershipsPerSubject = C + r` não lança `ResourceExhausted` e `C + r − 1` lança. Casos: sujeito próprio com C = 120; sujeito compartilhado com C = 20 e M = 100.
   - **6b, acoplamento.** Um sujeito tipo DataHub, com 92 tickers, roda enquanto a faixa adiciona a uma por 6 s com confirmações de 5 s. Todos os fantasmas do DataHub têm de ser herdados dentro dos 30 s, e mede-se a espera do `AcquireAsync` de um sujeito tipo Mercado.
   - **6c, queda do pipe.** `SubscriptionRegistry` com graça e `PipeGatewayMarketSource` real sobre `FakeMarketDataClient`, no molde de SubscriptionRestoreOnReconnectTests.cs. O pipe cai, a sessão velha da faixa acaba, a nova faz Subscribe e Unsubscribe de cada série, e o pipe volta. A reposição não pode conter nenhuma série da faixa e tem de conter U.
7. **Cerca de orçamento** em `tests/architecture/platform/`, no padrão de TwinAuthorityTests.cs:154-163. Verifica:
   - 2·C_F2 ≤ `MaxSubscriptionMembershipsPerSubject` − 16;
   - 2·(`MaxDesiredTickers` + C_F1 compartilhado) ≤ `MaxSubscriptionMembershipsPerSubject` − 16;
   - 2 sessões do Mercado + 1 da faixa ≤ `MaxLiveSessionsPerSubject` − 1;
   - a concorrência de snapshots do Mercado + 1 ≤ `MaxConcurrentSnapshotsPerSubject`.

   A cerca só vê os valores por omissão do código (GatewayOptions.cs:49-51). Os de produção podem ser outros (RemoteGateway/appsettings.json:18-22), e o dono confirma-os (pergunta 8). Mudar qualquer um destes números obriga a rever a conta.
8. **Cerca de forma.**
   - O padrão do seletor é igual ao `StockOptionRegex`, e a lista de prefixos é igual a `FuturePrefixes` (TickerClassifier.cs:44-47, 72-75).
   - Cada série escolhida a partir da fixture é classificada como opção, não é BMF e tem no máximo `TickerShape.MaxLength` caracteres.
9. **Rotas.** Cobre:
   - com o DataHub ligado e a faixa desligada, `/estado` responde JSON `desligada`, e não `index.html`;
   - um objeto fora da lista, que dá 404;
   - a política `Read`;
   - a faixa indisponível, que dá 503;
   - um perfil `GatewayOpcoes` sem caminhos explícitos, que aparece em `/estado` como sujeito compartilhado e limita a fase a F1.
10. **Vitest do modelo e da página.** Cobre:
    - a grade montada a partir de uma fixture;
    - os estados `desligada`, `sem oferta`, `nao_reconfirmado`, `incerto`, `muda`, `quarentena`, `indisponivel` e "fora da faixa";
    - a leitura que para com a aba oculta e com a faixa desligada;
    - nenhuma requisição além das duas rotas.
11. **Navegação.** `App.opcoes.test.tsx` (App.opcoes.test.tsx:43-51, 76-96) e `e2e/opcoes-navigation.spec.ts` (e2e/opcoes-navigation.spec.ts:29-39, 67, 79) passam a deixar só `#opcoes` chamar `/api/opcoes/ao-vivo/*`, com a rota de estado servida como `desligada` no Playwright. A expectativa do texto de placeholder em `opcoes` passa a ser a do estado da página nova. As outras 15 páginas continuam sem nenhuma requisição.
12. **Replay offline**, um harness e não um teste de CI. Lê uma cópia local dos arquivos diários de opções (`b3-daily/v1`, OptionDailyFiles.cs:19) e das velas de 1 min dos objetos, sem chamar o Portal nem serviços de produção, como o harness offline da SPEC-0475 (type-surface-ratchet.json:5). Para cada um de até 30 pregões, monta a cadeia do dia e o plano e mede quantas reancoragens disparam, quantas séries distintas entram, quantas fatias por hora isso custa e quanto A acumula de pregão em pregão, com as trocas de vencimento. Com menos de 30 arquivos, usa os que houver e diz N. O resultado fixa d.
13. **Rajada da recuperação da DLL**, em `Host.Tests`, no molde de `Host.Tests/Services/TapeCatchUpSchedulerTests.cs`, só com casos novos. Preenche um dicionário concorrente com o mesmo comparador de `MarketState.Subscriptions` (MarketState.cs:49) com 92 nomes tipo DataHub, 100 tipo Mercado e D_vivo tipo faixa. Enfileira na ordem de enumeração das chaves, com o dreno preso por um requisitante falso, e conta quantos tickers do DataHub entram nas 64 vagas, com e sem as séries. A conta proporcional prevê cerca de 31 sem a faixa e 14 com 240 séries.
14. **Estado do dia.** Cobre a escrita e a leitura; o reinício no meio do pregão com estado válido, em que A reentra sem custo; o estado ausente ou corrompido, em que a faixa falha fechada; a troca de `host_process_start_utc`, que esvazia A; e a presença da linha `excluded` no censo T02.

## 6. Critérios de aceite

- **CA1.** `git diff --name-only $(git merge-base HEAD main) HEAD` não lista nada em:
  - `Host/`, `Host.Shared/`, `src/Gateway/`, `src/Transport/`, `src/Contracts/`, `src/Services/` ou `scripts/wine-gate/`;
  - `ClientApp/src/modules/mercado/` ou `ClientApp/src/modules/ordens/`;
  - `MarketStreamCoordinator.cs`, `MarketHub.cs`, `SessionCandleStore.cs` ou `PortalGatewayMarketClient.cs`.

  Em `Host.Tests/` e `tests/Gateway/` só aparecem arquivos de teste novos ou casos novos.
- **CA2.** Passam sem editar os seus arquivos nem as suas listas:
  - `NoOrderCallerTests`, `ForbiddenSurfaceTests`, `LiveOrderPathGuardTests` e `NoTradingCapabilityBeforeP11Tests`;
  - `ProjectReferenceBoundaryTests` e `MercadoBoundaryTests`.

  `T02_physical_writer_inventory…` passa com uma única linha nova em `WriterInventory/src.json`, `excluded` e com razão, para o estado do dia, e sem dono novo no censo. A `type-surface-ratchet` e a `composition-allowlist` só ganham as linhas desta SPEC, com a sua nota.
- **CA3.** Para qualquer cadeia, o seletor devolve no máximo o teto da camada. Todas as séries casam a forma do Host e têm no máximo 15 caracteres, e repetir a chamada dá o mesmo resultado (testes 1 e 8).
- **CA4.** Nenhum comando sai fora de 09:02–`StopAt`, em feriado ou com o portão fechado, exceto o stream de limpeza das 18:00 às 18:10, que só toca séries em quarentena. Às 18:00 sai um cancelamento explícito de todas as séries e de nenhum objeto U. As órfãs que restarem aparecem em `/estado` como risco até à D1d (testes 3 e 4).
- **CA5.** Numa rotação, a faixa reenvia o mesmo conjunto com as mesmas flags em até 10 s. Depois de `ResourceExhausted` não há nova tentativa antes de 5 s. Com confirmação de 5 s e escrita em buffer, uma série ruim entre 120 vai para quarentena em até 3 reinícios, e uma queda por Host lento não põe nenhuma em quarentena. Depois de `Disconnected`, todas as séries são liberadas antes de qualquer leitura de métrica (testes 4 e 6c).
- **CA6.** Uma falha da faixa não termina o stream do Mercado (teste 5). No Gateway, os fantasmas do DataHub são herdados dentro da graça com a faixa a adicionar (teste 6b).
- **CA7.** No teste 6a, com a corrida forçada, o pico fica ≤ 256 − 16 nos dois casos:
  - com sujeito próprio e C = 120;
  - com sujeito compartilhado, C = 20 e M = 100.

  O R medido fica registrado na SPEC.
- **CA8.** As cercas de orçamento e de forma passam (testes 7 e 8).
- **CA9.** A página e a navegação passam, incluindo o Playwright (testes 10 e 11). Com `Enabled=false`, `/estado` responde JSON `desligada`, `/{objeto}` responde 409, e nenhuma das duas responde `index.html`.
- **CA10, operacional, por pregão, em cada fase.** Cada número compara-se com a base fixa da Sombra, nos mesmos horários, e declara a sua fonte. Com a faixa ativa:
  - pelas métricas do pipe (`IHostStatusSource`): Δ`client_outbound_live_trade_dropped_total` = 0 e Δ`broadcast_live_trade_dropped_total` = 0;
  - pelo diário do Host: `tape_live_gap` fora das linhas `startup_recovery` dos tickers da faixa, `tape_live_payload_unsaved`, `tape_live_admission_shed` e `tape_catchup_owner_budget_exhausted` (HostTapeIngest.cs:316-322, 360-393; TapeCatchUpScheduler.cs:83-88) não passam da base;
  - pelos medidores do DataHub: as lacunas do `TapeMinuteGapMeter` não passam da base;
  - pelas métricas do Host: Δ`dropped_callback_work` e Δ`unsubscribed_discards` por hora não passam do p99 da base, somado, no segundo, o aumento previsto pelas séries fora do plano;
  - não há `ResourceExhausted` para o sujeito da faixa, nem terminal do Mercado ao mesmo tempo que uma falha da faixa;
  - as fatias do aquecimento ficam ≤ B_a, as fatias por hora ficam ≤ B_f, as séries distintas no dia ficam ≤ D_dia e D_vivo fica ≤ D_max;
  - em amostras de controle (um snapshot de uma série da camada 1, E1, a cada 5 min, só se a série teve substituição nos últimos 60 s), o topo da faixa coincide com o do snapshot em pelo menos 95% das amostras.
- **CA11.** Depois de um reinício do Portal com estado válido, nenhuma série de A conta no orçamento; sem estado válido, a faixa falha fechada (teste 14).

## 7. Perguntas para o dono

1. **Sujeito.** F1 pode usar o sujeito do Portal, com C ≤ 20, ou um sujeito próprio, com C ≤ 25. F2 e F3 exigem `CN=farol-portal-opcoes`, só com `market.subscribe.v1` e `market.read.v1`, e os passos da seção 3.8, que incluem reiniciar o Gateway. Aceita? O repositório não diz quais sujeitos a produção usa (RemoteGateway/appsettings.json:8-13).
2. **Objetos e camadas.** Quais objetos entram, e em que camada? Aceita as larguras por omissão, ou seja, 25 pertenças na camada 1 e 11 na camada 2, e a camada 1 reduzida de 17 em F1 com sujeito compartilhado?
3. **Reancoragem.** A reancoragem única às 10:20 fica ligada? Aceita o critério duplo (paridade em códigos e S_ab no mesmo sentido), o limiar de 2 posições, o bloqueio de 15%, a admissão só até às 11:20 e que o que não couber em B_f não entre no dia?
4. **Vencimentos.** As semanais ficam fora? No dia do vencimento, a regra é `Expiry ≥ T` ou `Expiry > T`, e até que hora? E2 entra sempre?
5. **Acúmulo nativo** (antes de F1; o teto da DLL, antes de F3). O Unsubscribe do pipe não desfaz a assinatura nativa, e a sessão nativa dura o processo do Host (F6). Isso é intencional? Qual é o teto de assinaturas da ProfitDLL? Quantos pregões dura, em média, um processo do Host (N_r)? Aceita D_max = C + T_troca + d·N_r, com reserva para a troca de vencimento, e D_dia = 1,5·C?
6. **Catch-up congelado** (antes de F1). A faixa não muda código do caminho do ADR-0040, mas é um consumidor novo do catch-up, como o Mercado já é. Cada série nova custa F(t) fatias e declara um `tape_live_gap startup_recovery`. Na recuperação da DLL, todo `MarketState.Subscriptions`, com as séries acumuladas, disputa a fila de 64 (F8). Pela conta proporcional, que o teste 13 vai medir, entram hoje cerca de 64·92/192 ≈ 31 tickers do DataHub nas 64 vagas; com mais 240 séries, cerca de 64·92/432 ≈ 14. Aceita esse efeito? Considera que ele exige um ADR que reabra o ADR-0040? A resposta fica registrada na nova SPEC.
7. **Reinício do Host no pregão** (antes de F1). Com a liberação da seção 3.6, um reinício do Host deixa de repor as séries da faixa. Sobra F(t) por objeto que o DataHub não coleta; por exemplo, 3 objetos às 14:00 custam 3 × 60 = 180 fatias. Em contrapartida, as séries voltam sob B_f: depois de um reinício às 14:00, entram cerca de 11 até às 18:00. Aceita? Quer a D1d (o Gateway não repõe intenções de streams que já terminaram)? A decisão sobre a D1d é condição de F2.
8. **Valores de produção.** A produção roda com `BookScope=All` ou `Watched`, e com `TapePipeOverflow=DropOldest` ou `Block`? Com `Watched`, o livro das séries canceladas sai 60 s depois (docs/adr/host/0033-watched-book-scope.md:25-34). No Gateway, `MaxSubscriptionMembershipsPerSubject`, `MaxLiveSessionsPerSubject`, `MaxConcurrentSnapshotsPerSubject` e `SubscriptionReleaseGraceSeconds` de produção são os do repositório (RemoteGateway/appsettings.json:18-22)? As cercas só veem estes.
9. **Defasagem da base.** Aceita até 3 pregões de defasagem do cadastro, e que uma data `partial` seja trocada pela `available` anterior? Aceita que as séries criadas no próprio dia e os strikes ajustados na data-ex só entrem no dia seguinte?
10. **Página.** A página `#opcoes` pode ser exceção à SPEC-0526, com leitura a cada 1 s?
11. **Cercas.** Aceita que a catraca Portal→Mercado suba de 10 para cerca de 15 tipos, que a `composition-allowlist` ganhe as linhas da faixa, do planejador, do leitor, do estado e do adaptador, e que `WriterInventory/src.json` ganhe uma linha `excluded` para o estado do dia?
12. **Encerramento.** O encerramento fica às 18:00, com o stream de limpeza até às 18:10?
13. **Exclusões.** Confirma que ficam fora as opções de índice, de futuro, de juros e de ETF na forma C/P?
14. **Itens seguintes.** Quer como itens seguintes a D1c, a D1d, a D1e (ticker no `GapEvent`) e a D1f (métrica de assinaturas nativas, condição de F3)?
15. **Estado em disco.** Aceita o arquivo de estado do dia na pasta de estado do Portal, com falha fechada quando ele falta?

## Anexo: caminhos citados

- **Gateway:** `src/Gateway/Farol.RemoteGateway/GatewayOptions.cs`; `src/Gateway/Farol.RemoteGateway/appsettings.json` (RemoteGateway/appsettings.json); `src/Gateway/Farol.RemoteGateway/Program.cs` (RemoteGateway/Program.cs); `Services/{SubscriptionRegistry, MarketDataService, GatewaySubjectQuotaRegistry, PipeGatewayMarketSource, GatewaySessionManager, AuthenticatedSubject}.cs`; `Security/{CapabilityInterceptor, GatewayIdentityCapabilities, ClientCertificateValidator}.cs`; `tests/Gateway/Farol.RemoteGateway.Tests/{AdapterSubscriptionTests, MarketDataSubscribeIdleRateLimitTests, SubscriptionRestoreOnReconnectTests, FakeMarketDataClient}.cs` e `Harness/FakeGatewaySource.cs`.
- **Host:** `Host/IPC/{NamedPipeServer, NamedPipeServer.RuntimeMetrics, ClientConnection, INamedPipeServer}.cs`; `Host/Services/{ProfitService, ProfitServiceBookScope, HostTapeIngest, TapeCatchUp, TapeCatchUpScheduler, TapeCatchUpLane, StartupSliceQueue, PriorityCatchUpTickers, DailyBackfillPump, MetricsService, BusinessTradeLane, ProfitDllOptions}.cs`; `Host/Services/History/HistoryRequestRegistry.cs`; `Host/Core/MarketState.cs`; `Host/appsettings.json`; `Host.Tests/Services/TapeCatchUpSchedulerTests.cs`.
- **Contratos e transporte:** `src/Contracts/Farol.Protocol/Types/{TickerClassifier, TickerShape, B3MarketSession}.cs`; `src/Contracts/Farol.Remote.Contracts/{Abstractions/RemoteModels.cs, Protos/farol_remote.proto, RemoteSurfacePolicy.cs, RemoteProtocol.cs, Security/ClientCertificateIdentityPolicy.cs}`; `src/Transport/Farol.Ipc/PipeClient.cs`.
- **Mercado:** `src/Web/Farol.Mercado/Realtime/{MarketStreamCoordinator, PortalGatewayMarketClient, IPortalGatewayMarketClient, MarketTradeObservation, MarketSnapshotQueue, SessionCandleStore}.cs`; `Modules/{RealtimeEndpoints, HistoricalEndpoints}.cs`; `Hubs/MarketHub.cs`.
- **Portal:** `src/Web/Farol.Portal/Modules/OptionDaily/{OptionDailyReader, OptionDailySeries, OptionDailyEndpoints, OptionDailyConcessions, OptionDailyFiles}.cs`; `Modules/{DataHubEndpoints, MercadoModule}.cs`; `HostAuthority/HostStatusSource.cs`; `Health/GatewayHealthReplyCache.cs`; `Clients/AuthorityClientFactory.cs`; `PortalContracts.cs`; `PortalComposition.cs`; `Operations/{TradingCalendar, B3Clock, BatchTickerStore}.cs`.
- **ClientApp:** `src/Web/Farol.Portal/ClientApp/src/{App.tsx, App.opcoes.test.tsx, moduleBoundaries.test.ts}`; `modules/opcoes/optionsModules.ts`; `modules/meusagentes/useMeusAgentesReading.ts`; `modules/mercado/chart/sessionHours.ts`; `src/Web/Farol.Portal/ClientApp/e2e/opcoes-navigation.spec.ts`.
- **DataHub:** `src/Services/Farol.DataHub/{DataHubOptions.cs, Operations/LiveIngestService.cs, Operations/LiveIngestChannel.cs, Operations/LiveIngestReconciliationIdentity.cs, Catalog/B3DailyChainProjection.cs, Catalog/B3DailyPublication.cs}`.
- **Testes de arquitetura e censo:** `tests/architecture/platform/{type-surface-ratchet.json, composition-allowlist.json, MercadoBoundaryTests.cs, TwinAuthorityTests.cs}`; `tests/Web/Farol.Portal.Tests/{ProgressiveSubscriptionTests.cs, OptionDaily/OptionDailyFixture.cs}`; `tests/Services/Farol.DataHub.Tests/{PlmGcPhysicalWriterInventoryTests.cs, PhysicalWriterCensus.json, WriterInventory/src.json}`.
- **Operação e documentos:** `scripts/dev/{integrar.sh, farol-dev.sh}`; `infra/deploy/pki_authority_runtime.py`; `AGENTS.md`; `CONTEXT.md`; `docs/adr/{0013-data-ownership-and-storage, 0040-ingestao-fita-isolada, 0050-publicacao-liberada-no-pregao}.md`; `docs/adr/host/{0030-market-callback-work-has-a-ceiling, 0031-book-is-state-tape-is-stream, 0033-watched-book-scope, 0034-tape-pipe-lane}.md`; `docs/specs/{0422-catchup-winfut-prioritario, 0526-portal-opcoes, 0540-opcoes-calculadoras}/SPEC.md`; `knowledge/api/functions/subscriptions.md`.

## Notas da revisão

Os problemas estão numerados de R1 a R38, na ordem da lista dos revisores. Todos foram conferidos no código.

**Aplicados.**
- R1, R14: a seção 4 e a 3.4.3 dizem agora que a faixa é um consumidor novo do catch-up congelado. As respostas 5 a 7, com a decisão sobre um ADR, passaram a condição de F1; a decisão sobre a D1d, a condição de F2. Entraram o teste 13, a regra de não adicionar com reparo de arranque pendente e o aviso sobre `tape_live_gap startup_recovery`. A frase "quem repara a Fita passa sempre à frente" saiu, porque as fatias escolhem a janela mais recente (StartupSliceQueue.cs:42-55).
- R2: confirmado que um stream novo só libera um fantasma depois de o herdar (SubscriptionRegistry.cs:182-183). A sequência herdar-e-cancelar antes de ler métricas entrou na seção 3.6 e nos testes 4 e 6c, mas libera todas as séries, e não só as fora do núcleo, para não deixar 6·L·F(t) fatias por reinício no catch-up congelado.
- R3, R18: entrou o stream de limpeza das 18:00, e foram corrigidos a seção 3.5, item 7, e o CA4. A D1d ficou como decisão antes de F2, e não antes de F1, porque a limpeza cobre o caso comum e as quarentenas têm teto de 4 por dia.
- R4, R33: o portão passou a olhar `queue_depth`, `timeouts` e limiares medidos na Sombra; o disjuntor passou a olhar `dropped_callback_work`; o CA10 lê o diário do Host; a meta de idade p95 foi trocada por amostras de controle.
- R5, R11: entraram a seção 3.8, o adaptador do componente 9, a prova PKI e a recusa de F2 e F3 sem perfil explícito.
- R6: a faixa usa `TryWrite`, e o CA2 admite só uma linha `excluded` no censo.
- R7: a faixa nunca cancela U explicitamente.
- R8: o Playwright entrou no teste 11.
- R9: "nível" passou a "camada" (`Tiers`) e "bolsa" a "Segmento". "Camada" só aparece no glossário dentro da definição de Arquivo (CONTEXT.md:115), não como termo.
- R10, R36: o teste 12 é um harness offline com os arquivos diários; o teste 6a usa bisseção; o CA10 compara com a base fixa da Sombra e declara a fonte de cada número.
- R12: toda lacuna é global; snapshots só no núcleo; a D1e ficou como item separado.
- R15: os reenvios saem sem ritmo nem portão, em até 10 s.
- R16, R30: entraram o leitor de métricas sem cache e a conta própria de fatias, e saiu a frase sobre o freio no aquecimento.
- R17: saiu a promessa de isolamento total no Gateway; entrou o teste 6b.
- R19: as rotas são mapeadas sempre que o DataHub está ligado.
- R20, R35: entraram o estado do dia em disco e a falha fechada.
- R21: o teste 6a usa o `MarketDataService` real em processo.
- R22, R37: as sessões contam 2 por duplex; a faixa reabre 6 s depois da rotação; o sujeito compartilhado ficou com C ≤ 20 e margem de 16.
- R23: a data `partial` e o filtro (e) foram corrigidos.
- R24: a cadeia é lida uma vez por dia.
- R25: as citações foram corrigidas (`useMeusAgentesReading.ts`, farol-dev.sh:347-357, a lista exata do ADR-0040, os valores de produção na pergunta 8, as fontes do CA10). `sessionHours.ts` continua citado na linha 28, que tira a abertura das ações às 10:00 do contrato da B3; saiu a afirmação de que o livro está vazio antes das 10:00.
- R26: entrou o ritmo de uma adição a cada 6 s, a leitura da métrica antes de qualquer quarentena, as séries mudas e o Gateway falso com escrita em buffer.
- R28: entraram D_vivo, a reserva da troca de vencimento em D_max, Δ`unsubscribed_discards` e o acumulado no replay.
- R31: entrou B_a.
- R32: tratado como plausível, sem prova (F7). O aquecimento começa às 09:02, o portão olha `timeouts`, e as recusas são contadas em F1.
- R34: entrou o critério duplo por paridade e a admissão só até às 11:20.
- R38: depois de uma rotação não há snapshot.

**Aplicados em parte ou descartados.**
- R13, R27: o diagnóstico está certo, mas "não reabrir até a graça expirar" não evita a reposição, porque o Gateway repõe as intenções logo na religação, cerca de 11 s depois de um deploy, antes dos 30 s da graça (F10). Ficaram a leitura fresca com `ObservedAt` posterior à queda, a readmissão sob B_f e os números na pergunta 7, sobre a sequência de R2.
- R28: a D1f ficou como condição de F3, e não de F2. Com o estado do dia, o conjunto A da própria faixa passa a ser exato; a métrica só acrescenta o total dos outros clientes e o teto da DLL, que pesam acima de F2.
- R29: descartado na premissa. Todo stream começa com um evento vazio de anúncio (MarketDataService.cs:39; GatewaySessionManager.cs:83), e a regra do Mercado conta-o (MarketStreamCoordinator.cs:319-327), por isso uma rotação antes das 10:00 é reconhecida. Ficaram só a redação da linha de rotação e o roteiro do teste 3.

**Correções próprias.**
- F7 dizia que reassinar não repete nada; repete as chamadas nativas `SubscribeTicker`, PriceDepth e AdjustHistory (ProfitService.cs:1005, 1034-1050, 1065).
- F6 passou a dizer que só o `Dispose` chama `Disconnect` (ProfitService.cs:878, 4480), o que faz de `host_process_start_utc` o marcador da sessão nativa.
- F8 dizia que as fatias alternam entre tickers; escolhem a janela mais recente.
- F4 passou a distinguir a recusa respondida, que falha na hora, da recusa assíncrona, que deixa a série muda.