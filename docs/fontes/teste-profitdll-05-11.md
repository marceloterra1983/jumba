# Teste da ProfitDLL no Host: o que dá para ler sem publicar (05/11/2026)

Mapeado em origin/main 871c7f3 por quatro leitores, um plano, três céticos e uma revisão. Nada rodou na produção.

## Resumo

Hoje, sem publicar nem reiniciar nada, o teste diz se o Host aceita três opções, uma de cada vez e depois as três juntas: uma de ação com negócio, uma de ação sem negócio e uma de índice, esta só se o dono confirmar a licença. Ele separa recusa imediata, recusa assíncrona (InvalidTicker) e confirmação que não chegou em 5 s, e diz se chegam negócios e livro; dos dois DI1 lê só, de forma passiva, a vela diária da História (último negócio). O Ajuste do OnDaily, o PreviousClose e a bolsa inferida só aparecem se o journal tiver linhas Information, e o próprio código diz que o piso implantado é Warning. O máximo de séries simultâneas não se mede: o teste só mostra que mais três couberam. nContratosOpen, GetLastDailyClose e a ficha da opção ficam sem resposta, porque só existem na memória do Host ou em código que a produção não chama. A parte das opções depende de três respostas do dono: a máquina, a fonte dos códigos e o ok do gate G2.

## O que fica sem resposta sem mudar o Host

- nContratosOpen (contratos em aberto) de qualquer série. Em produção, o valor só existe na memória do Host: entra por Host/Services/TinyBookDailyConsumer.cs:88,118 e fica em DailyAggregator (Host/Services/DailyAggregator.cs:64,153,182). Fora da memória, só aparece na mensagem Daily do pipe, que exige IncludeDaily (Host/IPC/ClientConnection.cs:361-374). O Gateway assina com daily:false (src/Gateway/Farol.RemoteGateway/Services/PipeGatewayMarketSource.cs:194-200), o DailyEvent remoto não tem o campo (src/Contracts/Farol.Remote.Contracts/Protos/farol_remote.proto:378-385) e a linha OnDaily do log não o imprime (Host/Services/TinyBookDailyConsumer.cs:130-137). Ler exigiria um cliente de pipe no grupo pdllbridge, que marce não tem (scripts/wine-gate/etc/systemd/system/pdll-gateway.service:24-30), ou código novo no Host. As duas coisas estão fora do escopo.
- GetLastDailyClose. O único chamador é o OptionChainReader (Host/Services/OptionChainReader.cs:96,282-286), e nenhum código de produção o instancia; só Host.Tests/Services/OptionChainReaderTests.cs. Precisa de código novo no Host e de publicação.
- Ficha da opção (descrição, validade, multiplicador, tipo) pelo RequestTickerInfo. Em produção, só a sonda de arranque chama RequestTickerInfo (Host/Authority/ProfitDllStartupProbe.cs:145), e o evento TickerInfoReceived não tem assinante (Host/Services/ProfitService.cs:319,4111). O substituto do plano é: listada no cadastro com vencimento futuro e aceita pelo Host.
- Ajuste (sAjuste) com precisão cheia. O único caminho é a linha Information OnDaily, com N2 e escrita só quando muda (Host/Services/TinyBookDailyConsumer.cs:126-137). O código diz que o piso implantado é Warning (Host/Hosting/MarketSessionHostedService.cs:60-62; Host/Authority/HostAuthorityRuntimeEvidenceWriter.cs:230-235). Então o provável é não haver leitura nenhuma, e Ajuste=0.00 não se distingue de ausente.
- PreviousClose do Host da OPC_SEM, por construção: só existe se houve negócio entre 17h e 18h de D-1 (Host/Services/ProfitService.cs:1123-1127,3650,3661). O mesmo vale para qualquer série sem esse negócio, e para todas se não houver Information.
- Quantas séries a DLL aceita ao mesmo tempo, no máximo. Não há métrica (Host/Services/MetricsService.cs:868-876) nem limite documentado (knowledge/api/functions/subscriptions.md:233), e medir exigiria forçar o limite. O teste só mostra que mais 3 couberam.
- Quantas séries estão assinadas agora na DLL (o N de N+3). O Host não publica esse número. Com Information, sai só um piso por cliente de pipe (Host/IPC/ClientTickerSubscription.cs:58-59; Host/IPC/NamedPipeServer.cs:1314-1315), que não conta o resíduo nativo.
- Quantos ativos o Portal compartilha com o DataHub, isto é, o tamanho da cascata de uma recusa. O Portal não publica a sua união (src/Web/Farol.Mercado/Modules/RealtimeEndpoints.cs:75-99).
- Os dois DI1, se nenhum estiver vivo no DataHub hoje: o teste não os assina.
- Retirar o que o teste deixou: as assinaturas nativas (sem reset nativo não há caminho; Host/IPC/NamedPipeServer.cs:1298-1316) e a intenção retida no Gateway de uma série recusada ou sem confirmação (src/Gateway/Farol.RemoteGateway/Services/PipeGatewayMarketSource.cs:183-186,224). As duas ficam até o próximo reinício do Host ou do Gateway.
- A bolsa que a DLL de fato usa para a opção de índice e para o DI1. Só aparece com a linha Information Subscribed to (Host/Services/ProfitService.cs:1013), ou, numa recusa assíncrona, pelo @Exchange da linha de InvalidTicker (Host/Services/ProfitService.cs:1802-1805).
- Quando a DLL preenche o ajuste e os contratos em aberto. O manual não diz (knowledge/nelogica/Manual/Manual - ProfitDLL pt_br.md:2023).
- A comparação com os arquivos da B3: depende do download manual do dono, e os nomes de coluna desses arquivos não estão no repositório.
- Qual release está de fato instalada. O plano registra host_process_start_utc, mas não o SHA da release em execução.
- Em qual máquina roda o Host de produção: o contexto diz dev, e o repositório diz vps1 (docs/specs/0326-leitura-macro-pregao/DATA-EVIDENCE.md:7; docs/runbooks/prova-nativa-orderout.md:22-23). Só o dono responde, no G0.

## Riscos do teste limitado pelo Portal

- Uma recusa, ou uma confirmação que passe de 5 s mesmo com série válida, derruba a sessão inteira do Portal no Gateway (src/Gateway/Farol.RemoteGateway/Services/MarketDataService.cs:42-47,74,165-191). Todas as abas e alertas recebem terminal, e o Portal reconecta em cerca de 2 s (src/Web/Farol.Mercado/Realtime/MarketStreamCoordinator.cs:472-482). Os ativos compartilhados com o DataHub são reassinados no Host duas vezes: estreitamento imediato sem livro, e de novo com livro (src/Gateway/Farol.RemoteGateway/Services/SubscriptionRegistry.cs:231,250,441-466). O efeito foi inferido do código, não observado com o Portal real.
- Uma série recusada, ou sem confirmação, fica como intenção no Gateway até ele reiniciar. Ela é reenviada ao Host a cada reconexão do pipe (src/Gateway/Farol.RemoteGateway/Services/PipeGatewayMarketSource.cs:183-186,224,237-255,923). No caso de timeout, o Host pode ligar o filtro do pipe sem dono (Host/IPC/ClientTickerSubscription.cs:47; src/Transport/Farol.Ipc/PipeSubscriptions.cs:35-41).
- Vagas nativas ocupadas até o fim do dia, com o limite da DLL desconhecido. Se ele estiver perto, uma assinatura de produção posterior pode ser recusada, e o DataHub entraria em laço de reconexão a cada 5 s (src/Services/Farol.DataHub/Operations/LiveIngestService.cs:56,683-688,719-723). É inferência; a vigilância vai até 18h45 e só avisa o dono.
- Se a limpeza da sonda não chegar antes do novo pedido do Portal (~2 s depois do terminal), a série recusada pode ser pedida de novo e causar uma segunda queda. A sonda lê a cada 0,25 s e envia a lista vazia antes de fechar, mas isso só foi testado contra um servidor de referência.
- Carga extra por série: reposição desde as 09h a 250 msg/s, PreviousClose de D-1 e livro pelo resto do dia. O livro entra no anel de replay antes do filtro (Host/Services/ProfitService.cs:1018-1073; Host/IPC/NamedPipeServer.cs:273,986-988). Carga de livro aumenta o congelamento da DLL, e acima de 60 s o processo do Host é substituído (Host/Services/ProfitDllOptions.cs:141). Por isso OPC_COM tem volume moderado.
- A sonda hub_probe.py é código novo, testada só contra um servidor de referência local, nunca contra o Portal ASP.NET real. Uma falha de protocolo deve só fechar a ligação, e, ao fechar, o Portal retira as séries (src/Web/Farol.Mercado/Hubs/MarketHub.cs:119-124), mas isso não foi provado no real.
- Identidade: a sonda e as leituras do Portal rodam como farol-portal e se apresentam com a capacidade de leitura que o tailscaled injeta, sem identidade humana (infra/systemd/farol-portal.service:41-45; src/Web/Farol.Portal/PortalSecurity.cs:388-413,433-438). O G2 informa isso ao dono. Se sudo -u farol-portal for negado, o plano não troca por root sem perguntar.
- Escrita persistente fora da História: o Portal grava barras de 1 minuto das séries do teste por 30 pregões (src/Web/Farol.Mercado/Realtime/SessionCandleStore.cs:64-84).
- O teto de 100 do Portal é a união de todas as abas e alertas (src/Web/Farol.Mercado/Realtime/MarketStreamCoordinator.cs:142-152). Abrir gráficos ou armar alertas durante a sonda pode dar HubException e encolher o teste. O G2 pede ao dono que não faça isso.
- Outro agente pode publicar ou reiniciar o Host no pregão (Host/AGENTS.md:25-27). O plano detecta isso por host_process_start_utc, mas não impede, e um reinício faz o Gateway reenviar a intenção retida de uma série recusada.
- Rodar na máquina errada dá leituras vazias, que podem ser confundidas com dado ausente. O G0 confirma a máquina; sem resposta, nada roda.
- Origin errado devolve 403 sem efeito nenhum. O risco é ler /etc/farol/farol-portal.env ou tentar outras origens; o plano manda perguntar ao dono.
- Falso incidente: connected_clients e as conexões do Portal mudam quando o dono abre ou fecha abas. Linhas de InvalidTicker de produção podem existir por outros motivos; compará-las com a linha de base do passo 2.2.
- Precisão e unidade: F2 e N2 cortam DI1 de 3 casas e prêmios pequenos de opção. O preço de DI viaja sem unidade no fio (docs/specs/0326-leitura-macro-pregao/DATA-EVIDENCE.md, Orçamento e semântica).
- O arquivo da B3 baixado pelo dono pode vir em outra codificação ou com outros cabeçalhos. O script normaliza como o DataHub e avisa se ler como latin-1, mas a escolha final das séries é sempre conferida à mão.

## Plano do teste limitado (não executado)

# Plano final: teste da ProfitDLL no Host, pregão de 05/11/2026 (só leitura)

Base de leitura: o `origin/main` atual é `ca287bc`. O código foi conferido no checkout `871c7f3`; o `ca287bc` só acrescenta um commit de docs. As citações `caminho:linha` são relativas à raiz do repositório. O branch `origin/claude/project-thread-ugulea` não entra.

## Como as objeções foram tratadas

Conferi as 21 objeções no código. Todas se sustentam e entram no plano. Três entram com ajuste:

- **Produção 6 (snapshot):** o Portal cancela o RPC de snapshot em 5 s (`src/Web/Farol.Mercado/Realtime/MarketStreamCoordinator.cs:636`, `src/Web/Farol.Mercado/Realtime/MarketSnapshotQueue.cs:15`), não em 20 s. O efeito existe, mas é menor.
- **Produção 5 (congelamento):** o console não imprime o nome do EventId (`Host/appsettings.json:106`). Por isso o plano procura o texto das mensagens (`Host/Services/ProfitService.cs:1398-1402,1557-1560,1572-1574,1586-1589`), e não os nomes sugeridos.
- **Conformidade 3 (root):** a sonda e as leituras do Portal passam a rodar como `farol-portal`, dono do socket, e não como root. O G2 explica a identidade. A aba do próprio dono não é a alternativa recomendada: numa recusa, o Portal volta a pedir a série a cada ~2 s enquanto a aba a mantiver (`MarketStreamCoordinator.cs:311-316,472-482`). A sonda limpa a própria lista no primeiro `terminal`.

Mudanças principais:

- A sonda assina no máximo **3 opções**. Os DI1 nunca são assinados pelo teste.
- A recusa assíncrona agora é detectada: `ProfitDLL rejected ticker metadata request for T@X` (`Host/Services/ProfitService.cs:1303-1305,1783-1806`; manual `knowledge/nelogica/Manual/Manual - ProfitDLL pt_br.md:1079`).
- Os snapshots são classificados como bons ou ruins (`MarketStreamCoordinator.cs:647-672`).
- A falta de confirmação em 5 s é tratada como desconhecida, e não como recusa (`src/Transport/Farol.Ipc/PipeSubscriptions.cs:35-41`, `src/Transport/Farol.Ipc/PipeClient.cs:250,527-535`).
- Ao sair, a sonda chama `SetDesiredSubscriptions([])` antes de fechar.
- O G2 descreve a intenção que fica retida no Gateway (`src/Gateway/Farol.RemoteGateway/Services/PipeGatewayMarketSource.cs:183-186,224,237-255,923`) e a cascata sobre os ativos que o Portal compartilha com o DataHub (`src/Gateway/Farol.RemoteGateway/Services/SubscriptionRegistry.cs:231,250,441-466`).
- A fonte das séries passa a ser o dono, e não o coletor.
- A máquina é confirmada com o dono, sem `ssh vps1` por suposição.
- `OPC_COM` passa a ter volume moderado.
- O dia é vigiado até 18h45.
- Os greps e o `jq` foram corrigidos, e o script de listagem foi refeito com as regras do DataHub.

## O que este plano consegue e o que não consegue

- **Consegue:** saber, para até 3 opções, se o Host aceita a série. A classificação é `recusado_sincrono`, `recusado_assincrono`, `aceito_com_dados`, `sem_recusa_sem_dados` ou `desconhecido_confirmacao_nao_chegou`. Também registra recusas parciais de livro e de ajuste, se chegam negócios, livro e snapshot bom, e a vela diária da História dos DI1 que o DataHub já assina.
- **Só com linhas Information no journal:** `Ajuste` do `OnDaily`, `PreviousClose` do Host, bolsa inferida (`Subscribed to ... on exchange`) e piso de assinaturas por cliente de pipe. O código diz que o piso implantado é Warning (`Host/Hosting/MarketSessionHostedService.cs:60-62`, `Host/Authority/HostAuthorityRuntimeEvidenceWriter.cs:230-235`, `Host/appsettings.json:93-100`). O publicador, porém, espera uma linha Information (`scripts/wine-gate/publish-wine-host.sh:66-67`, `Host/Services/ProfitService.cs:2026`). O passo 2.2 mede qual dos dois vale. A expectativa é que não haja linhas Information.
- **Não consegue:** `nContratosOpen`, `GetLastDailyClose`, ficha da opção e máximo de séries da DLL (ver `o_que_fica_sem_resposta`).

Expectativa por série:

- **OPC_COM:** aceitação, negócios e livro. `PreviousClose` só se houve negócio entre 17h e 18h de 04/11 (`Host/Services/ProfitService.cs:1123-1127`) e houver Information.
- **OPC_SEM:** o resultado provável é `sem_recusa_sem_dados`. `PreviousClose` não existe por construção (`Host/Services/ProfitService.cs:3661` só loga Debug).
- **OPC_IDX:** a pergunta é se a licença cobre opção de índice.
- **DI1:** só a História. `Ajuste=0.00` é "zero ou ausente, indistinguível".

## Regras durante todo o teste

- Proibido: caminho de ordem, timers, `.env`, matriz de agentes, configuração protegida, coletores, publicar ou reiniciar Host, Gateway, DataHub ou Portal, segundo processo nativo (`Host/AGENTS.md:50`), b3.com.br e escrever na História.
- Não rodar `scripts/ladder-test/driver/ladder.mjs`, que assina uma lista de até 100 tickers (`:16-26`), nem `testa-candidatos.mjs`, que aponta para `127.0.0.1:7445` (`:4-6`), onde nada escuta desde o #824 (`infra/deploy/portal-preflight.sh:18-22`).
- `journalctl` sempre com `grep` antes de gravar em arquivo. Nunca `curl -v` ou `curl -i`. A sonda imprime só a linha de estado do upgrade, nunca os cabeçalhos (testado: o `Set-Cookie` do servidor de referência não aparece na saída).
- Horário: BRT = UTC-3. Assinatura nova só entre 10h30 e 15h30 BRT (13h30 a 18h30 UTC). Teto do teste: 3 séries novas.
- Se o dono não responder a um gate, o passo que depende dele não roda. Não há substituto automático.

## Passo 0: gates G0 e G1 (uma mensagem ao dono, antes de tudo)

Mandar ao dono, numa mensagem só:

1. **G0, máquina.** "Em qual máquina roda o Host de produção hoje? Mande o `hostname`." O contexto da tarefa diz "dev", com o repositório em `/home/marce/Projects/Farol`. O repositório diz vps1: `docs/specs/0326-leitura-macro-pregao/DATA-EVIDENCE.md:7`, `docs/runbooks/prova-nativa-orderout.md:22-23` e `docs/specs/0456-host-net10/SPEC.md:130-138`, que tratam dev e vps1 como máquinas distintas. Se a resposta não for a máquina desta sessão, parar: o teste não abre `ssh` por conta própria.
2. **G1, códigos das séries.** "Prefere (a) me passar 3 códigos, uma opção de ação com algumas dezenas a centenas de negócios ontem, uma do mesmo ativo sem negócio e uma de índice, (b) baixar à mão os arquivos da B3 de 04/11, cadastro de instrumentos e negócios consolidados de derivativos, para `~/farol-teste-dll/2026-11-05/b3-manual/`, ou (c) autorizar a leitura do CSV local do coletor (`infra/scrapper/b3-scrapper-paths.env:3`)?" Sem resposta, nenhuma série é assinada.
3. **Licença.** "A sua licença Nelogica cobre opção de índice? Sim, não ou não sei."
4. O texto do G2 (passo 5), para o dono já ir lendo.

Gravar as respostas com a hora em `$BASE/gates.json`, depois de criar a pasta no passo 1.

## Passo 1: ambiente (na máquina confirmada pelo G0)

```bash
hostname
systemctl is-active pdll-runtime.service pdll-gateway.service farol-portal.service
```

As três unidades têm de responder `active`, e o `hostname` tem de ser o do G0. Não iniciar nem reiniciar nada. Se não bater, parar e registrar o motivo.

```bash
BASE="$HOME/farol-teste-dll/2026-11-05"
mkdir -p "$BASE"/{bin,brutos,insumos,b3-manual}
chmod 700 "$BASE"
cat > "$BASE/bin/env.sh" <<'EOF'
BASE="$HOME/farol-teste-dll/2026-11-05"
CAP='{"profitbridge.com/cap/portal":[{"action":"read"}]}'
PORTAL_SOCK=/run/farol-portal/portal.sock
# Leitura do Portal pelo socket, como a sonda do deploy (infra/deploy/deploy-portal.sh:204-207),
# mas com o usuario dono do socket (farol-portal) em vez de root.
portal_get() { sudo -u farol-portal curl --unix-socket "$PORTAL_SOCK" --fail --silent --show-error --max-time 15 --header "Tailscale-App-Capabilities: ${CAP}" "http://localhost$1"; }
jhost()   { sudo journalctl -u pdll-runtime.service --since "$1" --no-pager -o short-iso; }
jgw()     { sudo journalctl -u pdll-gateway.service --since "$1" --no-pager -o short-iso; }
jportal() { sudo journalctl -u farol-portal.service --since "$1" --no-pager -o short-iso; }
PAT_RECUSA='Native subscription (rejected|failed) for|Failed to subscribe to [A-Z0-9]+:|ProfitDLL rejected ticker metadata request for|Failed to subscribe to PriceDepth for|Failed to SubscribeAdjustHistory for'
PAT_GW='Host did not confirm the subscription for|UnconfirmedSubscription|Failed to restore subscription for'
PAT_CONGELA='threads FROZEN|report its threads responsive again|did not report its threads responsive|unfroze on its own'
PAT_INFO='Market connected \(state=|Auto-subscribing to [0-9]+ tickers|Subscribed to [A-Z0-9]+ on exchange|OnDaily: |PreviousClose for |subscriptions: [0-9]+'
EOF
. "$BASE/bin/env.sh"
date -u +%FT%TZ > "$BASE/brutos/inicio_utc.txt"
git -C /home/marce/Projects/Farol rev-parse HEAD > "$BASE/brutos/repo_head.txt" 2>/dev/null || echo "repo ausente nesta máquina" > "$BASE/brutos/repo_head.txt"
cd / && portal_get /api/host > /dev/null && echo "socket ok como farol-portal"
```

Em todo shell novo, rodar antes `. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"`.

O socket é `0700` do usuário `farol-portal` (`infra/systemd/farol-portal.service:41-45,57`). O Portal trata como local quem chega pelo socket (`src/Web/Farol.Portal/PortalSecurity.cs:558-559`) e autoriza pelo cabeçalho de capacidade (`src/Web/Farol.Portal/PortalSecurity.cs:388-413`). Esse cabeçalho é o que o tailscaled injeta, e com ele não há identidade humana (`:433-438`). Isso vai escrito no G2.

**Parada:** se `sudo -u farol-portal` for negado, não trocar por root sem o dono: perguntar. Se o `sudo journalctl` pedir uma senha que a sessão não tem, parar.

## Passo 2: pré-checagem, sem assinar nada (depois das 10h05 BRT)

### 2.1 Estado do Host e de recuperação no arranque

Isto **não** é o orçamento de conexão do publicador. A tag guarda o resultado que o supervisor gravou ao concluir a conexão (`Host/Hosting/NativeConnectionSupervisor.cs:237-241,414-422`). O publicador conta tentativas numa janela de 15 min a partir de um arquivo (`scripts/wine-gate/check-native-connection-budget.sh:36-45`). O teste não faz login, então não gasta esse orçamento. A regra do `Host/AGENTS.md:50` vale para publicar ou reiniciar.

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
cd / && portal_get /api/host > "$BASE/brutos/host_antes.json"
jq '{observedAt, gateway: {ready: .gateway.ready, state: .gateway.state}, pipeConnected: .pipe.connected,
     marketOpen: .serverTime.marketOpen, b3SessionDate: .serverTime.b3SessionDate,
     tags: (.metrics.tags // {} | {dll_connected, market_open, connected_clients, recovery_state, recovery_reason,
            recovery_attempts_used, recovery_attempts_remaining, unsubscribed_discards, host_process_start_utc,
            queue_depth, dropped_client, dropped_broadcast, dropped_callback_work})}' "$BASE/brutos/host_antes.json" | tee "$BASE/precheck_host.json"
jq -e '(.metrics != null) and (.gateway.ready == true) and (.pipe.connected == true)
       and (.metrics.tags.dll_connected == "true") and (.metrics.tags.market_open == "true")
       and ((.metrics.tags.recovery_attempts_remaining // "") | test("^[0-9]+$"))
       and ((.metrics.tags.recovery_attempts_remaining | tonumber) >= 2)' "$BASE/brutos/host_antes.json"; echo "precheck_rc=$?"
```

Fontes: `src/Web/Farol.Portal/Modules/HostEndpoints.cs:15-21,25-33,65-120` e as tags em `Host/Services/MetricsService.cs:849-856,885,927,943-948`; as tags são strings, por isso o `tonumber`.

**Parada:** se `precheck_rc` for diferente de 0, abortar. Se a tag de recuperação estiver ausente, parar também e perguntar ao dono.

### 2.2 Journal do Host desde o arranque, linhas Information e linha de base de recusas

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
HOST_START="$(jq -r '.metrics.tags.host_process_start_utc' "$BASE/brutos/host_antes.json")"
SINCE_HOST="$(date -u -d "$HOST_START" '+%Y-%m-%d %H:%M:%S UTC')"; echo "$SINCE_HOST" > "$BASE/brutos/since_host.txt"
jhost "$SINCE_HOST" | grep -E "$PAT_INFO|$PAT_RECUSA|$PAT_CONGELA|B3 session boundary crossed|No subscribers for" > "$BASE/brutos/journal_host_desde_inicio.txt"
for p in 'Market connected (state=' 'Auto-subscribing to' ' on exchange ' 'OnDaily: ' 'PreviousClose for ' 'subscriptions: ' \
         'Native subscription rejected for' 'Native subscription failed for' 'Failed to subscribe to ' \
         'ProfitDLL rejected ticker metadata request for' 'Failed to SubscribeAdjustHistory for' 'No subscribers for' \
         'threads FROZEN' 'did not report its threads responsive'; do
  printf '%s\t%s\n' "$p" "$(grep -cF -- "$p" "$BASE/brutos/journal_host_desde_inicio.txt")"
done | tee "$BASE/brutos/journal_host_contagens.tsv"
INFO="$(awk -F'\t' '$1 ~ /Market connected|Auto-subscribing|on exchange|OnDaily|subscriptions: / && $2 > 0 {n++} END {print (n > 0) ? "true" : "false"}' "$BASE/brutos/journal_host_contagens.tsv")"
jq -n --argjson v "$INFO" '{info_visivel: $v}' | tee "$BASE/precheck_journal.json"
grep -E 'Client [^ ]+ (subscribed to [A-Z0-9]+, total|unsubscribed from [A-Z0-9]+, remaining) subscriptions: [0-9]+' "$BASE/brutos/journal_host_desde_inicio.txt" \
  | sed -E 's/.*Client ([^ ]+) .* subscriptions: ([0-9]+).*/\1 \2/' | awk '{u[$1]=$2} END {for (c in u) print c, u[c]}' > "$BASE/brutos/piso_pipe_por_cliente.txt"
```

Origem das linhas:

- `Host/Services/ProfitService.cs:1013,1082,1114,2026,2114,3650,1783-1806`
- `Host/IPC/ClientTickerSubscription.cs:23,28,58-59`
- `Host/IPC/NamedPipeServer.cs:1013,1314-1315`
- `Host/Services/TinyBookDailyConsumer.cs:128-137`
- `Host/Hosting/MarketSessionHostedService.cs:63-65`

As linhas de recusa e de `No subscribers` são Warning, então aparecem mesmo com o piso Warning.

**Parada:** nenhuma. Com `info_visivel=false`, ficam sem resposta o ajuste, o `PreviousClose`, a bolsa (salvo pela linha de InvalidTicker) e o piso por cliente.

### 2.3 Linha de base do DataHub, do Portal e do Gateway

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
cd / && portal_get /api/market/relay > "$BASE/brutos/relay_antes.json"
cd / && portal_get /api/datahub/tickers | jq -r '.tickers[] | select(.mode=="live") | .ticker' | sort > "$BASE/brutos/live_antes.txt"
test -s "$BASE/brutos/live_antes.txt" || echo "AVISO: conjunto vivo vazio ou ilegível"
grep -E '^DI1[FGHJKMNQUVXZ][0-9]{2}$' "$BASE/brutos/live_antes.txt" | tee "$BASE/brutos/di1_live.txt"
jgw "2026-11-05 03:00:00 UTC" | grep -E "$PAT_GW" > "$BASE/brutos/gw_antes.txt"; wc -l < "$BASE/brutos/gw_antes.txt"
jportal "2026-11-05 03:00:00 UTC" | grep -cF 'Realtime upstream disconnected' > "$BASE/brutos/portal_quedas_antes.txt"
```

Fontes: `src/Web/Farol.Mercado/Modules/RealtimeEndpoints.cs:75-99`, `src/Web/Farol.Portal/Modules/DataHubEndpoints.cs:41-42`, `src/Web/Farol.Portal/Modules/TickerAdminEndpoints.cs:225-232,272-279`, `src/Web/Farol.Portal/Operations/TickerAdminSource.cs:240`. O JSON bruto da lista não é guardado, porque traz `updatedBy`.

### 2.4 Vagas de assinatura, sem forçar

Não existe contador de assinaturas da DLL: `subscribed_tickers` está ausente de propósito (`Host/Services/MetricsService.cs:868-876`), e o manual não traz limite (`knowledge/api/functions/subscriptions.md:233`).

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
AUTO="$(grep -oE 'Auto-subscribing to [0-9]+' "$BASE/brutos/journal_host_desde_inicio.txt" | tail -1 | grep -oE '[0-9]+$')"
jq -n --arg auto "${AUTO:-desconhecido}" --argjson live "$(wc -l < "$BASE/brutos/live_antes.txt")" \
      --argjson conns "$(jq '.connections' "$BASE/brutos/relay_antes.json")" \
      --arg piso "$(cat "$BASE/brutos/piso_pipe_por_cliente.txt")" \
  '{dll_limite_documentado: null, dll_assinaturas_atuais: null,
    motivo: "Host não publica contagem (Host/Services/MetricsService.cs:868-876); manual sem limite (knowledge/api/functions/subscriptions.md:233)",
    piso_conhecido: {tickadm_live_agora: $live, auto_subscribe_no_arranque: $auto, cadastro_live_em_2026_10_20: 104,
                     piso_pipe_por_cliente: (if $piso == "" then null else $piso end)},
    tetos_do_farol: {portal_uniao_de_conexoes: 100, portal_conexoes_agora: $conns, gateway_por_sujeito: 256, host_por_cliente_pipe: 1000},
    vagas_calculaveis: false}' | tee "$BASE/vagas_antes.json"
```

O piso por cliente só existe com Information. Ele não conta o resíduo nativo nem o que o Host auto-assinou sem cliente. Os 104 vivos de 20/10 estão em `docs/specs/0326-leitura-macro-pregao/DATA-EVIDENCE.md:9`. Tetos do Farol:

- Portal: `src/Web/Farol.Mercado/Realtime/MarketStreamCoordinator.cs:42-44,142-152`
- Gateway: `src/Gateway/Farol.RemoteGateway/GatewayOptions.cs:49-50`
- pipe: `Host/IPC/NamedPipeServer.cs:143`

O Portal não publica a sua união de ativos (o relay só tem conexões, `RealtimeEndpoints.cs:75-99`). Por isso não dá para medir quantos ativos o Portal compartilha com o DataHub.

## Passo 3: História, só leitura passiva dos DI1

A História não guarda ajuste, contratos em aberto nem fechamento anterior. O DataHub assina com `IncludeDaily:false` (`src/Services/Farol.DataHub/Operations/LiveIngestService.cs:475`). A vela diária traz o `close` = último negócio (`src/Web/Farol.Mercado/Historical/DataHubHistoricalSource.cs:67-90`).

Escolher `DI1A` e `DI1B`: os dois vencimentos mais próximos, depois de hoje, de `di1_live.txt`. O DI1 vence no primeiro dia útil do mês do código, então o DI1X26 já venceu. Em 19/10, DI1F27, F28, F29, F31 e F33 estavam vivos (`DATA-EVIDENCE.md:15-19`). **O teste nunca assina DI1.** Assinar juntaria a assinatura com livro à do coletor (`src/Gateway/Farol.RemoteGateway/Services/SubscriptionRegistry.cs:116-126,441-466`), e já houve recusa de DI1 em produção (`docs/specs/0456-host-net10/SPEC.md:139`). Se `di1_live.txt` vier vazio, a parte DI1 fica sem resposta hoje.

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
DI1A=DI1F27; DI1B=DI1F28   # trocar pelos que estiverem em di1_live.txt
for T in "$DI1A" "$DI1B"; do
  cd / && portal_get "/api/history/candles?ticker=$T&bucketSeconds=86400&from=2026-11-03&to=2026-11-04" > "$BASE/brutos/historia_${T}_diario.json"
  jq --arg t "$T" '{ticker: $t, readStatus: .coverage.readStatus, truncated,
                    candles: [.candles[] | {dia: (.timeUnixSeconds|todate), open, high, low, close, volume, source}]}' \
     "$BASE/brutos/historia_${T}_diario.json" > "$BASE/historia_${T}.json"
done
cd / && portal_get "/api/history/candles?ticker=$DI1A&bucketSeconds=60&from=2026-11-05&to=2026-11-05" \
  | jq '{n: (.candles|length), ultima_barra_utc: ((.candles[-1].timeUnixSeconds // null) | if . == null then null else todate end)}' > "$BASE/brutos/fluxo_datahub_antes.json"
```

Fontes: `src/Web/Farol.Mercado/Modules/HistoricalEndpoints.cs:37,198-240`. Só essas três chamadas, sem polling (`DATA-EVIDENCE.md`, seção "Orçamento e semântica"). Testado: o `jq` antigo abortava com lista vazia (`strftime/1 requires parsed datetime inputs`, rc=5).

**Parada:** HTTP diferente de 200 ou `readStatus` diferente de `complete` vira "História indisponível", e o teste segue.

## Passo 4: escolha das 3 opções (depende do G1)

- **G1 (a), códigos do dono:** usar os códigos do dono, com `fonte_escolha: "dono"`.
- **G1 (b), arquivos baixados pelo dono** em `$BASE/b3-manual/`: são dado não confiável. Ler só com `python3 -I` e com o script abaixo.
- **G1 (c), coletor autorizado:** copiar sem `sudo`. Se der permissão negada, voltar ao dono.

```bash
D=/srv/charlie/finance/scrapper/artifacts/scrapper/B3/Derivativos
cp "$D/derivativos_cadastro_instrumentos_20261104.csv" "$D/derivativos_negocios_consolidados_20261104.csv" "$BASE/insumos/"
```

Para (b) e (c), gravar o script. Ele segue o DataHub: cabeçalho normalizado (`src/Services/Farol.DataHub/Operations/ScrapperCsvDailyUniverseProvider.cs:505-534`), colunas (`:223-231,268-269`), soma de negócios (`:285`), `""` e `"-"` como vazio (`:572-573`) e a coluna deslocada (`:689-697`). Foi testado com CSVs sintéticos: cabeçalho com outra caixa e sem acento, BOM, linhas repetidas, `1.234`, tipo vazio e código de 16 caracteres. O sha256 testado é `c90bf0aa95974b4f3b2857b9a4a684fe5de77c3acbf1a199e38ee5ff3904fee0`.

```bash
cat > "$HOME/farol-teste-dll/2026-11-05/bin/lista_candidatas.py" <<'PYEOF'
#!/usr/bin/env python3
"""Le o par cadastro_instrumentos / negocios_consolidados da B3 (arquivo local, sem rede)
e lista candidatas a serie de teste. Segue as regras de leitura do DataHub
(ScrapperCsvDailyUniverseProvider.cs:223-231, 268-285, 505-534, 572-573, 689-697):
cabecalho normalizado (caixa, acento, BOM), "" e "-" como vazio, negocios somados por ticker.

Uso:
  lista_candidatas.py CADASTRO NEGOCIOS --hoje 2026-11-05 --resumo
  lista_candidatas.py CADASTRO NEGOCIOS --hoje 2026-11-05 --ativo PETR [--segmento X] [--mercado Y] [--categoria Z]
Saida: JSON por linha. Nao escolhe sozinho: quem escolhe e o executor, com a regra do plano.
"""
import argparse
import csv
import datetime
import json
import re
import sys
import unicodedata

SHAPE = re.compile(r"^[A-Z0-9]{1,15}$")
DATE_FORMATS = ("%d/%m/%Y", "%Y-%m-%d", "%Y%m%d")


def norm(value):
    text = unicodedata.normalize("NFD", value.strip().lstrip("﻿"))
    text = "".join(ch.lower() for ch in text if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", text)


def empty_to_none(value):
    value = value.strip()
    return None if value in ("", "-") else value


def read_table(path):
    try:
        with open(path, encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle, delimiter=";", quotechar='"'))
    except UnicodeDecodeError:
        print(f"aviso: {path} nao e UTF-8; lido como latin-1 (o DataHub so le UTF-8)", file=sys.stderr)
        with open(path, encoding="latin-1", newline="") as handle:
            rows = list(csv.reader(handle, delimiter=";", quotechar='"'))
    for position, row in enumerate(rows[:100]):
        if len(row) >= 2 and any(norm(field) == "instrumento financeiro" for field in row):
            columns = {}
            for index, name in enumerate(row):
                columns.setdefault(norm(name), index)
            return columns, len(row), position + 1, rows[position + 1:]
    raise SystemExit(f"cabecalho 'Instrumento financeiro' ausente nas 100 primeiras linhas de {path}")


def column(columns, name, path):
    key = norm(name)
    if key not in columns:
        raise SystemExit(f"coluna '{name}' ausente em {path}")
    return columns[key]


def field(row, index):
    return row[index].strip() if index < len(row) else ""


def parse_date(text):
    text = (empty_to_none(text) or "")
    for fmt in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cadastro")
    parser.add_argument("negocios")
    parser.add_argument("--hoje", required=True)
    parser.add_argument("--resumo", action="store_true")
    parser.add_argument("--ativo")
    parser.add_argument("--segmento")
    parser.add_argument("--mercado")
    parser.add_argument("--categoria")
    args = parser.parse_args()
    today = datetime.date.fromisoformat(args.hoje)

    n_cols, n_count, _, n_rows = read_table(args.negocios)
    n_ticker = column(n_cols, "Instrumento financeiro", args.negocios)
    n_trades = column(n_cols, "Quantidade de negócios", args.negocios)
    shifted = norm("Segmento") in n_cols and norm("Mercado") not in n_cols
    trades, invalid = {}, 0
    for row in n_rows:
        ticker = field(row, n_ticker).upper()
        if not ticker:
            continue
        index = n_trades
        if shifted and len(row) == n_count + 1 and n_cols[norm("Segmento")] < index:
            index += 1
        raw = (empty_to_none(field(row, index)) or "0").replace(".", "")
        if not raw.isdigit():
            invalid += 1
            continue
        trades[ticker] = trades.get(ticker, 0) + int(raw)
    if invalid:
        print(f"aviso: {invalid} linhas com quantidade de negocios invalida em {args.negocios}", file=sys.stderr)

    c_cols, _, c_start, c_rows = read_table(args.cadastro)
    names = ("Instrumento financeiro", "Ativo", "Segmento", "Mercado", "Categoria",
             "Data de expiração", "Tipo de opção")
    idx = {name: column(c_cols, name, args.cadastro) for name in names}
    combos = {}
    for offset, row in enumerate(c_rows):
        record = {name: field(row, idx[name]) for name in names}
        ticker = record["Instrumento financeiro"].upper()
        if not ticker:
            continue
        option_type = empty_to_none(record["Tipo de opção"])
        key = (record["Segmento"], record["Mercado"], record["Categoria"], option_type is not None)
        combos[key] = combos.get(key, 0) + 1
        if args.resumo:
            continue
        if args.ativo and record["Ativo"].upper() != args.ativo.upper():
            continue
        if args.segmento and record["Segmento"] != args.segmento:
            continue
        if args.mercado and record["Mercado"] != args.mercado:
            continue
        if args.categoria and record["Categoria"] != args.categoria:
            continue
        expiry = parse_date(record["Data de expiração"])
        print(json.dumps({
            "ticker": ticker,
            "ativo": record["Ativo"],
            "segmento": record["Segmento"],
            "mercado": record["Mercado"],
            "categoria": record["Categoria"],
            "tipo_opcao": option_type,
            "expiracao": expiry.isoformat() if expiry else record["Data de expiração"],
            "vence_depois_de_hoje": bool(expiry and expiry > today),
            "negocios_d1": trades.get(ticker, 0),
            "forma_ok": bool(SHAPE.match(ticker)),
            "registro_csv": c_start + offset + 1,
        }, ensure_ascii=False))
    if args.resumo:
        for (segment, market, category, has_type), count in sorted(combos.items()):
            print(json.dumps({"segmento": segment, "mercado": market, "categoria": category,
                              "tem_tipo_de_opcao": has_type, "linhas": count}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
PYEOF
sha256sum "$HOME/farol-teste-dll/2026-11-05/bin/lista_candidatas.py"
cd "$HOME/farol-teste-dll/2026-11-05" && python3 -I bin/lista_candidatas.py <CADASTRO> <NEGOCIOS> --hoje 2026-11-05 --resumo | tee brutos/cadastro_resumo.jsonl
```

`<CADASTRO>` e `<NEGOCIOS>` são os caminhos em `b3-manual/` ou em `insumos/`. Pelo `--resumo`, identificar os valores reais de `Segmento`, `Mercado` e `Categoria` das opções sobre ação e sobre índice. O plano não presume esses valores. Depois:

```bash
cd "$HOME/farol-teste-dll/2026-11-05" && python3 -I bin/lista_candidatas.py <CADASTRO> <NEGOCIOS> --hoje 2026-11-05 --ativo PETR --mercado '<valor do resumo>' > brutos/candidatas_PETR.jsonl
cd "$HOME/farol-teste-dll/2026-11-05" && python3 -I bin/lista_candidatas.py <CADASTRO> <NEGOCIOS> --hoje 2026-11-05 --ativo IBOV > brutos/candidatas_IBOV.jsonl
```

Regras de escolha. Toda série precisa de `forma_ok=true`, isto é, 1 a 15 caracteres ASCII alfanuméricos, que é o limite do Host (`src/Contracts/Farol.Protocol/Types/TickerShape.cs:30,36-38`; os códigos de 17 caracteres ficam de fora, `:16-17`). Precisa também de `vence_depois_de_hoje=true` e de não estar em `live_antes.txt`.

- `OPC_COM`: opção sobre ação do vencimento mais próximo que não vence hoje, com **20 a 300** negócios em D-1 (a mais perto de 100). Só se não houver nenhuma nessa faixa, a menor acima de 300. Não escolher a mais negociada: a reposição começa às 09h (`Host/Services/HostTapeIngest.cs:405-411`, `Host/Services/TapeCatchUp.cs:84-96`), e o livro entra no anel de replay antes do filtro (`Host/IPC/NamedPipeServer.cs:273,986-988`).
- `OPC_SEM`: do mesmo ativo-objeto, listada, com `negocios_d1 = 0`.
- `OPC_IDX`: sobre o Ibovespa (`Ativo` = `IBOV`, se o arquivo usar esse valor), de preferência com 1 a 300 negócios. Só entra se a resposta sobre a licença for "sim", ou se o dono aceitar o risco no G2.

Gravar `$BASE/series.json` com ticker, papel, fonte (`dono`, `b3_manual_20261104` ou `coletor_20261104`) e a linha do CSV. Gravar `$BASE/brutos/series_teste.txt` com um ticker por linha. Se nenhuma série for assinada, gravar a linha `NENHUMA_SERIE`.

## Passo 5: gate G2, antes de qualquer assinatura

Mandar ao dono, com as séries escolhidas:

> Para testar as 3 opções, uma sonda vai assiná-las pelo hub do Portal, uma a cada 3 minutos, por cerca de 9 minutos, entre 10h30 e 15h30. Efeitos:
> 1. **Resíduo nativo.** As séries aceitas ficam assinadas na DLL (ticker, livro e ajuste) até o próximo reset nativo do Host. Elas seguem gerando callbacks que o Host descarta. Fonte: `Host/IPC/NamedPipeServer.cs:1298-1316`; nada chama o `UnsubscribeTicker` nativo, `Host/Services/ProfitService.cs:1178-1194`.
> 2. **Série recusada ou sem confirmação em 5 s.** Fica como intenção no Gateway até o **Gateway** reiniciar, o que está fora deste teste. O Gateway a reenvia ao Host em toda reconexão do pipe, inclusive depois de uma publicação do Host, que pode acontecer no pregão (`Host/AGENTS.md:25-27`). Se for timeout, o Host pode ter ligado o filtro do pipe sem dono. Fontes: `PipeGatewayMarketSource.cs:183-186,224,237-255,923`, `SubscriptionRegistry.cs:139-157,182-183`, `ClientTickerSubscription.cs:47`.
> 3. **Queda do fluxo do Portal.** Uma recusa, ou o Host levar mais de 5 s para confirmar uma série válida, derruba a sessão inteira do Portal no Gateway. Todas as abas e alertas recebem `terminal`, as velas ficam marcadas com descontinuidade, e o Portal reconecta em ~2 s. **Todos os ativos que o Portal compartilha com o DataHub são reassinados no Host duas vezes, durante o pregão**: na hora, sem livro, e de novo, com livro, na reconexão. Não dá para medir quantos são, porque o Portal não publica a sua união. Fontes: `MarketDataService.cs:42-47,74,165-191`, `SubscriptionRegistry.cs:231,250,441-466`, `MarketStreamCoordinator.cs:472-482`. A sonda limpa a própria lista no primeiro `terminal`, para não ser pedida de novo.
> 4. **Vagas nativas.** As séries ocupam vagas até o fim do dia, e o limite da DLL é desconhecido. Se estiver perto, uma assinatura de produção posterior pode ser recusada, e o DataHub entraria em laço de reconexão a cada 5 s (`LiveIngestService.cs:56,683-688,719-723`). Isto é inferência, não foi observado. Vou vigiar até 18h45 e avisar na primeira ocorrência; reiniciar é decisão sua.
> 5. **Carga.** Cada série nova dispara a reposição da fita desde 09h, o `PreviousClose` de D-1 e o livro pelo resto do dia (`Host/Services/ProfitService.cs:1018-1029,1036-1053,1065-1073`; `docs/HOST-POLICY.md:831-836`).
> 6. **Escrita no disco do Portal.** O Portal grava barras de 1 minuto das séries por 30 pregões (`SessionCandleStore.cs:64-84`). Não é a História.
> 7. **Identidade.** A sonda roda como `farol-portal` e se apresenta com a capacidade de leitura que normalmente o tailscaled injeta, sem a sua identidade (`infra/systemd/farol-portal.service:41-45`, `PortalSecurity.cs:388-413,433-438`). A alternativa é você abrir as séries numa aba sua. Nesse caso, numa recusa, o Portal repete o pedido a cada ~2 s enquanto a aba mantiver a série, e você teria de tirá-la na hora.
> 8. **Durante os ~10 minutos da sonda:** não abra gráficos nem arme alertas novos, e, se puder, feche as abas de mercado do Portal. Isso reduz o item 3 e o teto de 100 (`MarketStreamCoordinator.cs:142-152`).
>
> Sobre a licença de opção de índice: se a resposta for "não sei", rodo só `OPC_COM` e `OPC_SEM`, salvo se você aceitar o risco do item 2 para `OPC_IDX`.
>
> Posso seguir? Responda sim, não, ou sim sem OPC_IDX.

Gravar a resposta, com a hora, em `$BASE/gate_g2.json`. **Sem um "sim" explícito, pular para os passos 7 (só DI1 e linha de base), 9 e 10.**

## Passo 6: sonda (10h30 a 15h30 BRT)

### 6.1 Gravar a sonda

É um cliente SignalR mínimo, só com a biblioteca padrão. Ele chama apenas `SetDesiredSubscriptions` (`src/Web/Farol.Mercado/Hubs/MarketHub.cs:16`) e lê `MarketEnvelope` (`MarketStreamCoordinator.cs:16-32,834`). Não é processo nativo e não fala com o pipe.

Foi testado só contra um servidor de referência local (WebSocket + SignalR JSON), em seis cenários:

- terminal: código 3, limpa e fecha;
- erro do hub: código 4, limpa;
- servidor fecha: código 5, sem limpeza;
- normal: código 0, limpa;
- 403: código 2;
- Ctrl-C: código 6, limpa.

**Não** foi testado contra o Portal real. O sha256 testado é `d537ffaf9b767928b3b9c91c9eb68f8dd60b8365286186e71dd41ab994cb6d14`.

```bash
cat > "$HOME/farol-teste-dll/2026-11-05/bin/hub_probe.py" <<'PYEOF'
#!/usr/bin/env python3
"""Sonda minima do hub SignalR /hubs/market do Portal, pelo socket Unix.

So chama SetDesiredSubscriptions: uma lista que cresce um ticker por patamar e, ao sair por
qualquer motivo com a ligacao ainda aberta, a lista vazia. A lista vazia tira as series do
conjunto desejado do Portal antes de ele reabrir o fluxo (MarketStreamCoordinator.cs:472-482),
para uma serie recusada nao voltar a ser pedida. Le os MarketEnvelope. Uma linha JSON por evento.

Codigos de saida: 0 terminou; 2 upgrade/handshake recusado; 3 envelope "terminal";
4 o hub devolveu erro no SetDesiredSubscriptions; 5 o servidor fechou a ligacao;
6 interrompido (Ctrl-C); 7 erro local da sonda.
"""
import argparse
import base64
import json
import os
import socket
import struct
import sys
import time

RS = "\x1e"
CAP = '{"profitbridge.com/cap/portal":[{"action":"read"}]}'
CLEAR_ID = "limpa"


class _Stop(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def emit(**fields):
    fields = {"at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **fields}
    print(json.dumps(fields, ensure_ascii=False), flush=True)


class UnixWebSocket:
    def __init__(self, path, origin, host, hub):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect(path)
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {hub} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\nOrigin: {origin}\r\n"
            f"Tailscale-App-Capabilities: {CAP}\r\n\r\n"
        )
        self.sock.sendall(request.encode())
        buffer = b""
        while b"\r\n\r\n" not in buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("ligacao fechada durante o upgrade")
            buffer += chunk
        head, self.pending = buffer.split(b"\r\n\r\n", 1)
        # So a linha de estado: os cabecalhos da resposta (Set-Cookie) nunca saem daqui.
        self.status = head.split(b"\r\n", 1)[0].decode(errors="replace")
        if self.status.split(" ")[1:2] != ["101"]:
            raise ConnectionError(f"upgrade recusado: {self.status}")
        self.sock.settimeout(0.25)
        self._parts, self._first = [], None

    def send(self, payload, opcode=1):
        data = payload.encode() if isinstance(payload, str) else payload
        mask = os.urandom(4)
        size = len(data)
        header = bytes([0x80 | opcode])
        if size < 126:
            header += bytes([0x80 | size])
        elif size < 65536:
            header += bytes([0x80 | 126]) + struct.pack(">H", size)
        else:
            header += bytes([0x80 | 127]) + struct.pack(">Q", size)
        body = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.sock.sendall(header + mask + body)

    def _frame(self):
        buf = self.pending
        if len(buf) < 2:
            return None
        b1, b2 = buf[0], buf[1]
        size, offset = b2 & 0x7F, 2
        if size == 126:
            if len(buf) < 4:
                return None
            size, offset = struct.unpack(">H", buf[2:4])[0], 4
        elif size == 127:
            if len(buf) < 10:
                return None
            size, offset = struct.unpack(">Q", buf[2:10])[0], 10
        mask = None
        if b2 & 0x80:
            if len(buf) < offset + 4:
                return None
            mask, offset = buf[offset:offset + 4], offset + 4
        if len(buf) < offset + size:
            return None
        data = buf[offset:offset + size]
        if mask:
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.pending = buf[offset + size:]
        return bool(b1 & 0x80), b1 & 0x0F, data

    def read_messages(self):
        """Le o que houver por ate ~0,25 s; devolve lista de (opcode, bytes)."""
        try:
            chunk = self.sock.recv(65536)
            if not chunk:
                return [(8, b"")]
            self.pending += chunk
        except socket.timeout:
            pass
        out = []
        while True:
            frame = self._frame()
            if frame is None:
                break
            fin, opcode, data = frame
            if opcode == 9:
                self.send(data, opcode=10)
                continue
            if opcode in (8, 10):
                if opcode == 8:
                    out.append((8, data))
                continue
            if opcode != 0:
                self._first = opcode
            self._parts.append(data)
            if fin:
                out.append((self._first, b"".join(self._parts)))
                self._parts, self._first = [], None
        return out

    def close(self):
        try:
            self.send(struct.pack(">H", 1000), opcode=8)
        except OSError:
            pass
        self.sock.close()


class Probe:
    def __init__(self, ws, tickers, max_logged):
        self.ws = ws
        self.text = ""
        self.max_logged = max_logged
        self.logged = {}
        self.server_closed = False
        self.subscribed = False
        self.clear_done = None
        self.gaps = 0
        self.last_ping = time.monotonic()
        self.stats = {t: {"trade": 0, "book": 0, "replacement": 0, "snapshot_bom": 0,
                          "snapshot_ruim": 0, "primeiro_snapshot": None,
                          "primeiro_trade": None, "ultimo_trade": None} for t in tickers}

    def poll(self):
        if time.monotonic() - self.last_ping >= 10:
            self.ws.send(json.dumps({"type": 6}) + RS)
            self.last_ping = time.monotonic()
        messages = []
        for opcode, data in self.ws.read_messages():
            if opcode == 8:
                self.server_closed = True
                raise _Stop(5)
            self.text += data.decode(errors="replace")
        while RS in self.text:
            raw, self.text = self.text.split(RS, 1)
            if raw:
                messages.append(json.loads(raw))
        return messages

    def invoke(self, tickers, invocation_id):
        self.ws.send(json.dumps({"type": 1, "invocationId": invocation_id,
                                 "target": "SetDesiredSubscriptions",
                                 "arguments": [tickers]}) + RS)

    def handshake(self):
        self.ws.send(json.dumps({"protocol": "json", "version": 1}) + RS)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            for opcode, data in self.ws.read_messages():
                if opcode == 8:
                    self.server_closed = True
                    emit(evento="fechado_pelo_servidor", fase="handshake")
                    raise _Stop(5)
                self.text += data.decode(errors="replace")
            if RS in self.text:
                first, self.text = self.text.split(RS, 1)
                answer = json.loads(first or "{}")
                if "error" in answer:
                    emit(evento="handshake_falhou", resposta=answer)
                    raise _Stop(2)
                emit(evento="handshake_ok")
                return
        emit(evento="handshake_falhou", resposta=None)
        raise _Stop(2)

    def handle(self, message, step):
        kind = message.get("type")
        if kind == 3:
            if message.get("invocationId") == CLEAR_ID:
                self.clear_done = message.get("error") or "ok"
                return
            if message.get("error"):
                emit(evento="hub_erro", patamar=step, erro=message["error"])
                raise _Stop(4)
            emit(evento="hub_aceitou", patamar=step, resultado=message.get("result"))
        elif kind == 7:
            self.server_closed = True
            emit(evento="hub_close", patamar=step, erro=message.get("error"))
            raise _Stop(5)
        elif kind == 1 and str(message.get("target", "")).lower() == "marketenvelope":
            envelope = (message.get("arguments") or [{}])[0] or {}
            self.envelope(envelope, step)

    def envelope(self, envelope, step):
        env_kind = envelope.get("kind", "desconhecido")
        ticker = (envelope.get("ticker") or "").upper()
        payload = envelope.get("payload")
        if env_kind == "terminal":
            emit(evento="terminal", patamar=step, observedAt=envelope.get("observedAt"))
            if step is not None:
                raise _Stop(3)
            return
        if env_kind == "gap":
            self.gaps += 1
        entry = self.stats.get(ticker)
        if entry is not None:
            if env_kind == "snapshot":
                good = envelope.get("resyncRequired") is False and isinstance(payload, list) and len(payload) > 0
                entry["snapshot_bom" if good else "snapshot_ruim"] += 1
                if entry["primeiro_snapshot"] is None:
                    entry["primeiro_snapshot"] = {
                        "resyncRequired": envelope.get("resyncRequired"),
                        "niveis": len(payload) if isinstance(payload, list) else None,
                        "observedAt": envelope.get("observedAt")}
            elif env_kind == "trade":
                compact = {k: (payload or {}).get(k) for k in
                           ("price", "quantity", "tradeNumber", "timestampUnixMicroseconds", "isEdit")}
                entry["trade"] += 1
                if entry["primeiro_trade"] is None:
                    entry["primeiro_trade"] = compact
                entry["ultimo_trade"] = compact
            elif env_kind in ("book", "replacement"):
                entry[env_kind] += 1
        key = (ticker, env_kind)
        self.logged[key] = self.logged.get(key, 0) + 1
        if self.logged[key] <= self.max_logged:
            shown = payload if env_kind in ("trade", "book") else "omitido"
            emit(evento="envelope", patamar=step, kind=env_kind, ticker=ticker,
                 resyncRequired=envelope.get("resyncRequired"), payload=shown)

    def clear(self):
        """SetDesiredSubscriptions([]) e espera a conclusao por ate 10 s."""
        try:
            self.invoke([], CLEAR_ID)
            deadline = time.monotonic() + 10
            while self.clear_done is None and time.monotonic() < deadline:
                for message in self.poll():
                    if message.get("type") == 1:
                        envelope = (message.get("arguments") or [{}])[0] or {}
                        self.envelope(envelope, None)
                    elif message.get("type") == 3 and message.get("invocationId") == CLEAR_ID:
                        self.clear_done = message.get("error") or "ok"
                    elif message.get("type") == 7:
                        self.server_closed = True
                        break
                if self.server_closed:
                    break
        except (_Stop, OSError, ValueError, KeyboardInterrupt) as error:
            emit(evento="limpeza_interrompida", erro=type(error).__name__)
        emit(evento="limpeza", resultado=self.clear_done or "sem_resposta")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", default="/run/farol-portal/portal.sock")
    parser.add_argument("--origin", required=True)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--hub", default="/hubs/market")
    parser.add_argument("--tickers", required=True, help="lista separada por virgula, na ordem dos patamares")
    parser.add_argument("--step-seconds", type=int, default=180)
    parser.add_argument("--max-envelopes-logged", type=int, default=5)
    args = parser.parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    if not tickers or len(tickers) > 3:
        emit(evento="argumentos_invalidos", detalhe="entre 1 e 3 tickers")
        return 2

    try:
        ws = UnixWebSocket(args.socket, args.origin, args.host, args.hub)
    except (OSError, ConnectionError) as error:
        emit(evento="upgrade_falhou", erro=str(error))
        return 2
    emit(evento="upgrade_ok", status=ws.status)

    probe = Probe(ws, tickers, args.max_envelopes_logged)
    exit_code = 0
    try:
        probe.handshake()
        for step in range(1, len(tickers) + 1):
            desired = tickers[:step]
            emit(evento="patamar_inicio", patamar=step, tickers=desired)
            probe.subscribed = True
            probe.invoke(desired, str(step))
            step_end = time.monotonic() + args.step_seconds
            while time.monotonic() < step_end:
                for message in probe.poll():
                    probe.handle(message, step)
            emit(evento="patamar_fim", patamar=step, resumo={t: probe.stats[t] for t in desired})
    except _Stop as stop:
        exit_code = stop.code
    except KeyboardInterrupt:
        exit_code = 6
    except (OSError, ValueError) as error:
        emit(evento="erro_local", erro=f"{type(error).__name__}: {error}")
        exit_code = 7
    finally:
        if probe.subscribed and not probe.server_closed:
            probe.clear()
        ws.close()
        emit(evento="resumo_final", codigo_saida=exit_code, gaps=probe.gaps, por_ticker=probe.stats)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
PYEOF
sha256sum "$HOME/farol-teste-dll/2026-11-05/bin/hub_probe.py"
python3 -I -c 'import ast,sys; ast.parse(open(sys.argv[1]).read())' "$HOME/farol-teste-dll/2026-11-05/bin/hub_probe.py" && echo sintaxe_ok
```

Se o sha256 divergir do registrado, comparar o arquivo com este plano antes de rodar.

### 6.2 Origem esperada pelo hub

O WebSocket do hub exige `Origin` igual a `Portal:PublicOrigin` (`src/Web/Farol.Portal/PortalSecurity.cs:440-449,561-563`). Usar o valor versionado (`src/Web/Farol.Portal/appsettings.json:11`), sem ler `.env` nem arquivos da release:

```bash
echo 'https://vps1.tail9a3d97.ts.net:8443' > "$HOME/farol-teste-dll/2026-11-05/brutos/origin.txt"
```

O `/etc/farol/farol-portal.env` pode sobrescrever esse valor (`infra/systemd/farol-portal.service:58`). Um script antigo usava outra origem (`scripts/ladder-test/driver/testa-candidatos.mjs:6`). Se a sonda sair com código 2 e `403`, **não ler o `.env` nem tentar outras origens**: perguntar ao dono qual é a origem pública do Portal. O 403 não tem efeito nenhum.

### 6.3 Rodar

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
ORIGIN="$(cat "$BASE/brutos/origin.txt")"
OPC_COM=...; OPC_SEM=...; OPC_IDX=...            # de series.json
LISTA="$OPC_COM,$OPC_SEM,$OPC_IDX"              # sem ,$OPC_IDX se o G2 disser "sem OPC_IDX"
T0="$(date -u '+%Y-%m-%d %H:%M:%S') UTC"; echo "$T0" > "$BASE/brutos/t0.txt"
cd / && sudo -u farol-portal python3 -I - --origin "$ORIGIN" --tickers "$LISTA" --step-seconds 180 \
  < "$BASE/bin/hub_probe.py" | tee "$BASE/brutos/hub_probe.jsonl"
echo "codigo_saida=${PIPESTATUS[0]}" | tee "$BASE/brutos/hub_probe_saida.txt"
date -u '+%Y-%m-%d %H:%M:%S UTC' > "$BASE/brutos/t1.txt"
```

O script vai pela entrada padrão para que `farol-portal` não precise ler a pasta `0700`. A ordem vai da série com menor chance de recusa para a de maior chance.

O evento `hub_aceitou` diz só que o Portal pegou a lista: `SetDesiredSubscriptions` retorna antes de o Gateway confirmar (`MarketStreamCoordinator.cs:145-157,546-568`).

**Parada.** A sonda para sozinha nos códigos 3, 4, 5 e 2. Nos códigos 3 e 4, antes de fechar, ela envia a lista vazia e espera a resposta (evento `limpeza`). Em qualquer código diferente de 0: não repetir a série, não trocar por outra, ir aos passos 7 e 8.

Num segundo shell, rodar `portal_get /api/host | jq -r .metrics.tags.dll_connected` a cada ~1 min. Se a resposta for diferente de `true`, interromper com Ctrl-C: a sonda limpa e fecha (código 6).

## Passo 7: leituras no journal (séries do teste e DI1)

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
OPC_COM=...; OPC_SEM=...; OPC_IDX=...; DI1A=...; DI1B=...
T0="$(cat "$BASE/brutos/t0.txt")"; SINCE_HOST="$(cat "$BASE/brutos/since_host.txt")"
TODAS="$OPC_COM $OPC_SEM $OPC_IDX $DI1A $DI1B"; PAT_S="$(echo $TODAS | tr ' ' '|')"
jhost "$SINCE_HOST" | grep -E "($PAT_S)" | grep -E "$PAT_RECUSA|$PAT_INFO|No subscribers for|Skipping PreviousClose" > "$BASE/brutos/journal_host_series.txt"
jgw "$T0" | grep -E "$PAT_GW" > "$BASE/brutos/journal_gw_desde_t0.txt"
jportal "$T0" | grep -E 'Realtime upstream disconnected|SetDesiredSubscriptions failed|Realtime snapshot unavailable for|O limite inicial' > "$BASE/brutos/journal_portal_desde_t0.txt"
H="$BASE/brutos/journal_host_series.txt"; G="$BASE/brutos/journal_gw_desde_t0.txt"
for T in $TODAS; do
  echo "== $T"
  echo "-- recusa_sincrona";   grep -E "Native subscription rejected for $T:|Native subscription failed for $T( |\$)|Failed to subscribe to $T:" "$H" | tail -3
  echo "-- recusa_assincrona"; grep -F "ProfitDLL rejected ticker metadata request for $T@" "$H" | tail -3
  echo "-- recusa_livro";      grep -F "PriceDepth for $T:" "$H" | tail -1
  echo "-- recusa_ajuste";     grep -F "SubscribeAdjustHistory for $T:" "$H" | tail -1
  echo "-- gw_sem_confirmacao"; grep -F "subscription for $T;" "$G" | tail -1
  echo "-- gw_restore";        grep -F "Failed to restore subscription for $T " "$G" | tail -1
  echo "-- bolsa";             grep -E "Subscribed to $T on exchange " "$H" | tail -1
  echo "-- previous_close";    grep -E "PreviousClose for $T: [0-9]" "$H" | tail -1
  echo "-- previous_close_pulado"; grep -F "Skipping PreviousClose for $T:" "$H" | tail -1
  echo "-- ondaily";           grep -F "OnDaily: $T " "$H" | head -1; grep -F "OnDaily: $T " "$H" | tail -1
  echo "-- no_subscribers";    grep -F "No subscribers for $T;" "$H" | tail -1
done | tee "$BASE/brutos/leituras_journal.txt"
```

Gravar `$BASE/leituras.json` por série. Cada campo leva o valor e a linha do journal com o carimbo de hora; sem a linha, `null` e o motivo. A classificação de `aceito_pelo_host` vale só para linhas depois de `t0`, nesta ordem:

1. `recusado_sincrono`: há linha de recusa síncrona (`ClientTickerSubscription.cs:23,28`; `ProfitService.cs:1082`). Leva o código, por exemplo `NL_LICENSE_NOT_ALLOWED` (`Host/Services/NativeResultText.cs:15-28`).
2. `recusado_assincrono`: há linha `ProfitDLL rejected ticker metadata request for T@X` (`ProfitService.cs:1802-1805`). Vale mesmo que a sonda tenha recebido algo. O `@X` é a bolsa que a DLL recusou.
3. `desconhecido_confirmacao_nao_chegou`: houve `terminal` no patamar da série sem linha de recusa no Host, e/ou há `Host did not confirm the subscription for T;` no Gateway (`UnconfirmedSubscriptionException.cs:4`).
4. `aceito_com_dados`: pelo menos 1 `trade`, `book` ou `replacement`, ou `snapshot_bom ≥ 1`, sem nenhuma linha de recusa.
5. `sem_recusa_sem_dados`: nenhum dado e nenhuma recusa. `snapshot_ruim` sozinho não prova nada: o Portal manda `snapshot` com `resyncRequired=true` quando o RPC falha ou o Gateway não tem livro (`MarketStreamCoordinator.cs:647-672`).

Campos adicionais:

- `recusa_livro` (`ProfitService.cs:1051`) e `recusa_ajuste` (`:1072`), com código e linha. Uma série aceita com livro ou ajuste recusado leva essa ressalva.
- `bolsa_inferida`: da linha `Subscribed to` (Information) ou do `@X` da recusa assíncrona.
- `previous_close_host`: só da linha `PreviousClose for T: <número>` (`:3650`, `F2`). A linha `Skipping PreviousClose` (`:1113-1115`) vai em outro campo e não conta como valor. Não é `GetLastDailyClose`. Para os DI1, se a data da linha for anterior a 05/11, marcar `referente_a_outro_d1: true`.
- `ajuste_ondaily`: o `Ajuste=` da última linha `OnDaily` (`TinyBookDailyConsumer.cs:128-137`, `N2`, só logado quando a linha muda). `0.00` vira "zero ou ausente, indistinguível".
- `n_contratos_open`, `get_last_daily_close` e `ficha`: `null`, com os motivos de `o_que_fica_sem_resposta`.
- `negocios_recebidos`, `primeiro_trade`, `ultimo_trade`, `primeiro_snapshot`, `snapshot_bom` e `snapshot_ruim`: do `resumo_final` de `hub_probe.jsonl`.

Para os DI1 não há sonda: os dados vêm só do journal e do passo 3. Esperado no Portal: zero `Realtime upstream disconnected` entre `t0` e `t1`, ou exatamente um se houve `terminal`. Mais de um quer dizer que a limpeza não segurou o novo pedido. Registrar.

## Passo 8: conferência da produção (≥ 90 s depois de `t1`)

Depois de um `terminal`, as séries aceitas ficam por 30 s como dono fantasma no Gateway antes do Unsubscribe (`SubscriptionRegistry.cs:231-247,385-421`; `GatewayOptions.cs:65`). Por isso a espera é de pelo menos 90 s.

```bash
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
OPC_COM=...; OPC_SEM=...; OPC_IDX=...; DI1A=...
T0="$(cat "$BASE/brutos/t0.txt")"; TESTE="$(paste -sd'|' "$BASE/brutos/series_teste.txt")"
cd / && portal_get /api/host > "$BASE/brutos/host_depois.json"
cd / && portal_get /api/market/relay > "$BASE/brutos/relay_depois.json"
cd / && portal_get /api/datahub/tickers | jq -r '.tickers[] | select(.mode=="live") | .ticker' | sort > "$BASE/brutos/live_depois.txt"
cd / && portal_get "/api/history/candles?ticker=$DI1A&bucketSeconds=60&from=2026-11-05&to=2026-11-05" \
  | jq '{n: (.candles|length), ultima_barra_utc: ((.candles[-1].timeUnixSeconds // null) | if . == null then null else todate end)}' > "$BASE/brutos/fluxo_datahub_depois.json"
jhost "$T0" | grep -E "No subscribers for ($TESTE);" > "$BASE/brutos/no_subscribers_teste.txt"
jhost "$T0" | grep -E "$PAT_RECUSA" > "$BASE/brutos/recusas_desde_t0.txt"
grep -vE "($TESTE)" "$BASE/brutos/recusas_desde_t0.txt" > "$BASE/brutos/recusas_producao_desde_t0.txt"
jhost "$T0" | grep -E "$PAT_CONGELA" > "$BASE/brutos/congelamento_desde_t0.txt"
jgw "2026-11-05 03:00:00 UTC" | grep -E "$PAT_GW" > "$BASE/brutos/gw_depois.txt"
jq -n --slurpfile a "$BASE/brutos/host_antes.json" --slurpfile d "$BASE/brutos/host_depois.json" \
      --slurpfile ra "$BASE/brutos/relay_antes.json" --slurpfile rd "$BASE/brutos/relay_depois.json" \
  '{mesmo_processo_host: ($a[0].metrics.tags.host_process_start_utc == $d[0].metrics.tags.host_process_start_utc),
    dll_connected_depois: $d[0].metrics.tags.dll_connected,
    connected_clients: {antes: $a[0].metrics.tags.connected_clients, depois: $d[0].metrics.tags.connected_clients},
    unsubscribed_discards: {antes: $a[0].metrics.tags.unsubscribed_discards, depois: $d[0].metrics.tags.unsubscribed_discards},
    dropped_client: {antes: $a[0].metrics.tags.dropped_client, depois: $d[0].metrics.tags.dropped_client},
    dropped_broadcast: {antes: $a[0].metrics.tags.dropped_broadcast, depois: $d[0].metrics.tags.dropped_broadcast},
    portal_conexoes: {antes: $ra[0].connections, depois: $rd[0].connections}}' | tee "$BASE/conferencia_producao.json"
diff "$BASE/brutos/live_antes.txt" "$BASE/brutos/live_depois.txt" > "$BASE/brutos/live_diff.txt"; echo "diff_rc=$?"
diff "$BASE/brutos/gw_antes.txt" "$BASE/brutos/gw_depois.txt" | grep '^>' > "$BASE/brutos/gw_novas.txt"
```

Critérios. As quatro primeiras falhas são incidente de produção: não tentar mais nada, não reiniciar, registrar e avisar o dono.

- `mesmo_processo_host = true`. Se for `false`, houve reinício no meio do teste (`Host/AGENTS.md:25-27`) e as leituras ficam inválidas.
- `dll_connected_depois = "true"`.
- `recusas_producao_desde_t0.txt` vazio, e `congelamento_desde_t0.txt` vazio.
- `live_diff.txt` vazio (`diff_rc=0`), e `fluxo_datahub_depois.ultima_barra_utc` a poucos minutos da hora atual, com `n` maior que antes.
- `connected_clients` e `portal_conexoes` **sem queda inexplicada**. Eles mudam quando o dono abre ou fecha abas (`MarketStreamCoordinator.cs:49-56`); anotar com o dono as abas abertas no início e no fim.
- `gw_novas.txt` só com séries do teste.
- Esperado, e não é falha: uma linha `No subscribers for <série>;` por série aceita que tenha recebido dado depois da saída (`Host/IPC/NamedPipeServer.cs:1009-1015`), e `unsubscribed_discards` maior. A ausência da linha **não** deve ser atribuída a outra aba: série ilíquida pode não gerar mensagem, e, no caso de timeout, o filtro do pipe pode ter ficado ativo sem dono.

Gravar `$BASE/residuo_nativo.json`, uma entrada por série do teste, com o tipo:

- `assinatura_nativa_residual` (aceitas e recusa assíncrona): dura até o próximo reset nativo do Host.
- `intencao_retida_no_gateway` (`recusado_sincrono`): dura até o Gateway reiniciar e volta a ser recusada a cada reconexão do pipe. Ver `Failed to restore subscription for` no Gateway.
- `intencao_retida_e_possivel_filtro_sem_dono` (`desconhecido_confirmacao_nao_chegou`).

O teste não faz nada para tirar nenhuma delas.

## Passo 9: vigilância até o fim do dia e releitura passiva

### 9.1 Vigilância (14h, 15h, 16h e 17h BRT, e de novo às 18h45; 17:00, 18:00, 19:00, 20:00 e 21:45 UTC)

```bash
cat > "$HOME/farol-teste-dll/2026-11-05/bin/vigia.sh" <<'EOF'
#!/usr/bin/env bash
# Leitura passiva: recusas e congelamento desde t0, separando series do teste e producao.
set -u
. "$HOME/farol-teste-dll/2026-11-05/bin/env.sh"
T0="$(cat "$BASE/brutos/t0.txt" 2>/dev/null || cat "$BASE/brutos/inicio_utc.txt")"
TESTE="$(paste -sd'|' "$BASE/brutos/series_teste.txt")"
AGORA="$(date -u +%H%M)"
jhost "$T0" | grep -E "$PAT_RECUSA|$PAT_CONGELA" > "$BASE/brutos/vigia_host_$AGORA.txt"
jgw "$T0" | grep -E "$PAT_GW" > "$BASE/brutos/vigia_gw_$AGORA.txt"
(cd / && portal_get /api/host) | jq '{observedAt, dll_connected: .metrics.tags.dll_connected, host_process_start_utc: .metrics.tags.host_process_start_utc, dropped_broadcast: .metrics.tags.dropped_broadcast, dropped_client: .metrics.tags.dropped_client, unsubscribed_discards: .metrics.tags.unsubscribed_discards}' > "$BASE/brutos/vigia_tags_$AGORA.json"
echo "recusas_producao_host: $(grep -E "$PAT_RECUSA" "$BASE/brutos/vigia_host_$AGORA.txt" | grep -cvE "($TESTE)")"
echo "gateway_producao:      $(grep -cvE "($TESTE)" "$BASE/brutos/vigia_gw_$AGORA.txt")"
echo "congelamento:          $(grep -cE "$PAT_CONGELA" "$BASE/brutos/vigia_host_$AGORA.txt")"
cat "$BASE/brutos/vigia_tags_$AGORA.json"
EOF
chmod 700 "$HOME/farol-teste-dll/2026-11-05/bin/vigia.sh"
"$HOME/farol-teste-dll/2026-11-05/bin/vigia.sh"
```

Na primeira contagem de produção maior que 0, ou com `dropped_broadcast` crescendo entre rodadas, avisar o dono com a linha e a hora. Reiniciar não é do teste. Fontes:

- congelamento: `Host/Services/ProfitService.cs:1398-1402,1557-1560,1586-1589` (acima de 60 s o processo é substituído, `Host/Services/ProfitDllOptions.cs:141`);
- laço do DataHub: `src/Services/Farol.DataHub/Operations/LiveIngestService.cs:683-688,719-723`.

### 9.2 Releitura passiva depois do fechamento (18h30 BRT = 21h30 UTC)

Sem assinar nada, repetir só a extração do passo 7 com `jhost "2026-11-05 19:55:00 UTC"`, gravando em `$BASE/brutos/journal_host_pos_fechamento.txt`. Só tem valor com `info_visivel=true`: serve para ver se o `Ajuste` do `OnDaily` muda depois do fechamento. O manual não diz quando o ajuste é preenchido (`knowledge/nelogica/Manual/Manual - ProfitDLL pt_br.md:2023`).

## Passo 10: registro final e comparação com a B3

Gravar `$BASE/registro_final.json`:

```json
{
  "data": "2026-11-05",
  "inicio_utc": "<inicio_utc.txt>", "t0": "<t0.txt>", "t1": "<t1.txt>",
  "gates": "<gates.json + gate_g2.json>",
  "maquina": "<hostname confirmado no G0>",
  "release": {"repo_head": "<repo_head.txt>", "host_process_start_utc": "<host_antes>", "sha_release_em_execucao": null},
  "precheck": "<precheck_host.json + precheck_journal.json>",
  "vagas": "<vagas_antes.json>",
  "series": [
    {"ticker": "", "papel": "opcao_acao_com_negocio|opcao_acao_sem_negocio|opcao_indice|di1",
     "fonte_escolha": "dono|b3_manual_20261104|coletor_20261104|tickadm",
     "assinada_pelo_teste": true,
     "aceito_pelo_host": "recusado_sincrono|recusado_assincrono|desconhecido_confirmacao_nao_chegou|aceito_com_dados|sem_recusa_sem_dados|nao_testado",
     "codigo_recusa": null, "recusa_livro": null, "recusa_ajuste": null,
     "bolsa_inferida": {"valor": null, "linha": null},
     "negocios_recebidos": 0, "ultimo_trade": null, "primeiro_snapshot": null, "snapshot_bom": 0, "snapshot_ruim": 0,
     "previous_close_host": {"valor": null, "linha": null, "precisao": "F2", "nao_e": "GetLastDailyClose"},
     "ajuste_ondaily": {"valor": null, "linha": null, "precisao": "N2", "zero_e_ambiguo": true},
     "historia_close_d1": {"valor": null, "e": "ultimo negocio da Fita"},
     "n_contratos_open": {"valor": null, "motivo": "não exposto em produção"},
     "get_last_daily_close": {"valor": null, "motivo": "não chamado em produção"},
     "ficha": {"valor": null, "motivo": "não exposta em produção"},
     "residuo": "assinatura_nativa_residual|intencao_retida_no_gateway|intencao_retida_e_possivel_filtro_sem_dono|nenhum",
     "b3_manual": "pendente"}
  ],
  "simultaneas": {"novas_aceitas_ao_mesmo_tempo": 0, "primeira_recusa": null,
                  "interpretacao": "mostra só que N+k couberam; não é o máximo da DLL"},
  "producao": "<conferencia_producao.json + live_diff + recusas_producao_desde_t0 + congelamento + gw_novas + journal_portal_desde_t0>",
  "vigilancia": "<vigia_* até 18h45>",
  "faltou": ["nContratosOpen", "GetLastDailyClose", "ficha", "máximo de séries", "..."]
}
```

### 10.1 Comparação com os arquivos da B3 (quando o dono baixar)

Os arquivos ficam em `$BASE/b3-manual/` e são dado não confiável: ler só com `python3 -I` e com scripts de `$BASE/bin`, sem executar nada que venha de lá. Comparar por série:

- último preço e quantidade de negócios contra `ultimo_trade` e `negocios_recebidos`. A sonda só vê negócios enquanto a série está assinada, mais a reposição desde as 09h;
- ajuste contra `ajuste_ondaily`, lembrando as 2 casas decimais;
- fechamento anterior contra `previous_close_host` e `historia_close_d1`;
- contratos em aberto, que só existem do lado da B3.

O preço de DI não tem unidade no fio (`DATA-EVIDENCE.md`, "Orçamento e semântica"): não presumir se é taxa ou PU. Registrar os nomes de coluna como vierem.

## Resultado esperado

Com os três gates aprovados e o pregão normal, o teste diz, para até 3 opções, se o Host as aceita e por qual caminho recusa, inclusive se a licença cobre opção de índice. Diz também se chegam negócios e livro, e se houve recusa parcial de livro ou de ajuste. Para os DI1, traz só o último negócio da História. Ajuste, `PreviousClose` e bolsa só aparecem se `info_visivel=true`, o que é improvável. Não diz `nContratosOpen`, `GetLastDailyClose`, a ficha nem o máximo de séries. Esses itens ficam para uma mudança no Host fora deste teste.

