# MeusAgentes: como se cria e opera um agente com rotinas

Li `/home/claude/MeusAgentes` sem alterar nada. O guia oficial é `docs/criar-agente.md`, conferido em 02/11/2026. Nos documentos o repositório aparece como `/home/marce/Projects/MeusAgentes`.

## 1. Peças

Um agente é um manifesto mais um executável. Ele é importado por commit num release e executado pelo Runner do host, nunca a partir do checkout (`criar-agente.md` §0).

| Peça | Papel |
|---|---|
| `packages/contracts` | Valida as regras. `agent.ts` define `AGENT_TYPES` (rotina, vigia, reativo, analista, engenheiro, operador), `validateAgentManifest` e `checkCatalog`. `schedule.ts` trata cron e interval. `project.ts` fixa `HOSTS = dev, vps1, vps2`. `manifest.ts` tem `scanSecrets` |
| `packages/registro` | PostgreSQL (migrations 001–007). Guarda projeto, release, catálogo, corrida, gatilho, entrega e painel. `registrar.ts` importa e ativa |
| `packages/catalog` | Só um README. A implementação fica em `registro/src/catalogo.ts` |
| `packages/runner` | `main.ts` roda um tick a cada 15 s com trava por host. Também tem `launcher-script.ts`, `launcher-eve-tools.ts`, `entrega.ts` e `gatilhos.ts` |
| `packages/adapters/eve` | Wrappers determinísticos e `modeloBloqueado()`. Codex e Claude Code ainda não têm launcher (`montarLauncher`) |
| `catalog/<tipo>/<id>/item.yaml` | Tools (`effect: none/read/write`), connections (`access: read/write`) e channels, com `versao` atrelada ao hash |
| `apps/web` | Painel em 127.0.0.1:3090 |

## 2. O que vai em `agents/<id>/`

Segundo `criar-agente.md` §2, a pasta tem:
- `manifest.yaml`;
- o entry executável com shebang (`coleta.py`);
- `test_coleta.py`, que usa só fixtures;
- `README.md`;
- a pasta `agent/` com `agent.ts`, `sandbox.ts` (JustBashSandbox), `instructions.md`, `tools/<id>.md`, `connections/<id>.md`, `channels/<id>.md`, `tools/executar_rotina.ts` e `channels/runner.ts`.

Os dois últimos arquivos precisam ter exatamente duas linhas, conferidas byte a byte por `scripts/eve-tools-paridade-estrutural.test.ts`. Para reaproveitar código, use `agents/_comum/` (`relato.py`, `mascara.py`, `sessao.py`).

## 3. `projects/*.yaml`

Cada projeto define sua política: `repositorios_permitidos`, `hosts`, `classe_padrao`, `teto_capacidade`, `teto_destino` e `limite_concorrencia`. O agente só pode estreitar esses limites.

Hoje existem `dev.yaml`, `charlie.yaml` e `teste-runner.yaml`. **Não existe projeto `farol`**, e criar um é uma decisão de política do dono.

## 4. Agendamento

- **Não há systemd timer nem crontab por agente.** A ADR 008 define a plataforma como único agendador.
- O gatilho fica no manifesto: `trigger` com `kind: cron` (5 campos POSIX) ou `interval` (ISO, no mínimo PT1M), `timezone` IANA obrigatório, `window` e `delay_policy` (`skip_missed` ou `coalesce_if_active`).
- O comando `--ativar` grava o gatilho no banco. O Runner do dev o avalia a cada tick (`evaluateTriggers`).
- Em `shadow`, a ativação passa a autoridade para `meusagentes`. Um gatilho novo já em `active` fica com `sistema_anterior` e **não dispara** (§11).
- Para mudar o horário, crie um `trigger_id` novo com `substitui`.
- Não existe comando "rodar agora".
- Alguns timers systemd antigos continuam donos das suas rotinas, como `farol-hd-backup.timer`. Nesses casos o MeusAgentes só observa (`agents/backup-hd`, `adapter: systemd-observed`).

## 5. Como um agente roda na máquina do dono

- O Runner é uma unit systemd de usuário (`ops/systemd/meusagentes-runner.service`, com `NoNewPrivileges=yes`). Ela lê `prod/runner.env` e executa a partir de `prod/current`, conferindo `.commit-fonte` e o hash do manifesto.
- O entry é chamado como `entry $1 $2 $3`:
  - `$1`: diretório de estado persistente;
  - `$2`: `<corrida>.entrega.json`;
  - `$3`: chave de idempotência.
  - Ambiente limpo, mais `MEUSAGENTES_MODO`.
- Os artefatos vão em `<estado>/<corrida>.artefatos/*.json`. O Runner aceita até 2 MiB por arquivo, mas o painel só mostra até 256 KiB.
- `limits.timeout_minutes` encerra a corrida como `failed` por timeout.
- **`shadow` só bloqueia a Entrega.** O próprio script precisa guardar os seus efeitos; `agents/limpeza-armazenamento/limpeza.py` mostra como (§7).

## 6. Falhas e alertas

1. **Corrida que falha** (`failed`, `timeout`, `start_failed`) aparece no painel em Corridas. O Runner registra `gatilho_falhou` com um código (`gatilhos.ts`).
2. **Saúde ruim não falha a corrida.** Por convenção, saída 0 significa relatório gravado mesmo com FAIL, e saída 2 significa que a coleta falhou. A Home do painel só lê fontes que já conhece: em `apps/web/lib/vigias-saude.ts` estão higiene e ai-memory, cada um com seu `staleMs`; Backup e Update têm vistas próprias. **Suposição**: um vigia novo precisa ser ligado ali.
3. **Aviso por WhatsApp (Entrega).** O script grava uma intenção em `$2` com `canal`, `destinatario_ref`, `chave` e `texto`. Quem envia é o Runner, via Evolution, e só se houver `mode: active`, capability `entrega`, o canal em `channels`, o destinatário em `recipients` e o canal no teto do projeto. Só `whatsapp_out` tem transporte (`entrega.ts`, `canaisPadrao`).
4. **Caminho antigo.** `~/.local/bin/dev-alert` (usado por `agents/backup/estado_backup.py`, `avisar`) e o OnFailure do systemd chamando `agents/backup/alerta-falha.sh`.
5. **Vigia do vigia.** `agents/backup/frescor_vigia.py` confere se o próprio vigia rodou.

## 7. Credenciais

- Cada agente tem seu arquivo `prod/agentes/<projeto>/<id>.env`, fora do git, no formato KEY=VALOR, lido sem shell. O agente não herda `DATABASE_URL` nem o ambiente do Runner (`readAgentEnv`, `cleanEnv`).
- O número do destinatário fica no env do Runner como `ENTREGA_DEST_<REF>`. O script usa só a referência, por exemplo `DONO`.
- `scanSecrets` recusa tokens no manifesto.
- Não há receita genérica para criar esse arquivo com segurança; o guia marca isso como "não conferido" (§8).

## 8. Exemplos reais

- **`agents/higiene-armazenamento`**: vigia com cron `0 3 * * 0`. Mede espaço com `statvfs` em 5 volumes (inclui `/mnt/serverdisk`, o disco do Farol) e roda `smartctl` em 5 discos via `systemd-run --user … sudo -n`. Grava `relatorio.json`. Em FAIL de SMART, grava uma intenção `whatsapp_out` para `DONO` com chave por episódio e repete até aparecer o recibo em `entregas-confirmadas.jsonl`.
- **`agents/update`**: vigia com cron `20 8,14,20 * * *`. Lê pendências e timers do dev, e de vps1 e vps2 por SSH, só leitura (`hosts.py`). Alerta por transição usando `MA_PREVIOUS_STATE_PATH`, que só existe porque o id está em `AGENTES_COM_ESTADO_ANTERIOR` (`runner.ts:110`). Avisa só pelo painel e não aplica nada.
- **`agents/backup`**, para comparar: vigia `active` com `effects` liberados por lista (`reexecutar_unit`, `acrescentar_exclude_rebuildavel`).

## 9. Passo a passo para os dois agentes novos

**Antes de escrever, decisões do dono:**
- projeto `farol` novo ou `dev`;
- host;
- destino dos arquivos.

**Suposição sobre o host:** o contrato só aceita dev, vps1 e vps2. Se a ProfitDLL roda em Windows (há uma VM em `/var/lib/libvirt/images/windows-vm`), a captura pela DLL fica no Host do Farol. O MeusAgentes roda no dev e só confere os arquivos resultantes.

### `coleta-b3-diaria` (tipo `rotina`, porque grava arquivos)

1. Em `projects/farol.yaml`, coloque no teto as capacidades `leitura`, `escrita_dados_b3` e `entrega`, e os destinos `painel-local` e `whatsapp_out`.
2. No catálogo, crie:
   - `connections/b3-publico` com `access: read`;
   - `connections/dados-b3-escrita` com `access: write`;
   - `tools/baixar_arquivos_b3` com `effect: write`.
3. Manifesto (o horário é suposição, a ajustar à publicação dos arquivos da B3):

```yaml
id: coleta-b3-diaria
project: farol
type: rotina
runtime: script
execution:
  adapter: eve-tools
model: null
entry: coleta.py
host: dev
mode: shadow
data_policy:
  class: restrito
capabilities: [leitura, escrita_dados_b3]
trigger:
  trigger_id: coleta-b3-pos-pregao
  kind: cron
  expression: "30 20 * * 1-5"
  timezone: America/Sao_Paulo
  window: PT4H
  delay_policy: skip_missed
tools: [baixar_arquivos_b3]
connections: [b3-publico, dados-b3-escrita]
effects:
  - id: gravar_arquivos_b3
    capability: escrita_dados_b3
    connection: dados-b3-escrita
channels: [painel-local]
limits:
  timeout_minutes: 30
  concurrent_runs: 1
failure: stop_without_fallback
```

   O bloco `execution:` tem que ficar nesse formato de duas linhas, porque o cálculo do pino remove esse texto exato (§9).

4. `coleta.py` em Python só com stdlib (`urllib`), já que dependência nova exige aprovação. O script deve:
   - em feriado, sair 0 com `sem_pregao`, porque o cron não conhece o calendário da B3;
   - ser idempotente por data e por `$3`;
   - gravar no destino final **só se `MEUSAGENTES_MODO == "active"`**; em shadow, deixa apenas evidência em `$1`;
   - sair 2 se o download falhar.
5. `test_coleta.py` com HTTP falso, sem acessar a rede.
6. Arquivos de integração (§9):
   - `baseline` em `scripts/eve-tools-paridade-estrutural.test.ts`;
   - `IDS` em `scripts/eve-inventario.ts` e o registro em `docs/migracao-eve-inventario.json`;
   - `scripts/eve-inventario.test.ts`;
   - `scripts/eve-layout.test.ts`;
   - a lista `scripts.test` em `package.json`.
7. Validar com o script do §10, depois `npm test` e `bash scripts/portao.sh`.
8. Com aprovação do dono, nesta ordem:
   1. `registrar.ts projeto farol`;
   2. `scripts/publicar.sh`;
   3. `registrar.ts agente farol coleta-b3-diaria --ativar`, ainda em shadow;
   4. conferir no painel;
   5. passar para `active` num commit novo e publicar de novo.

### `vigia-jumba` (tipo `vigia`)

- `source` aponta para a conexão `dados-b3-local` (`access: read`) e a tool `conferir_dados_dia` (`effect: read`). Os campos obrigatórios ficam `previous_state: ultimo_relatorio_saude` e `comparison: item_passou_a_fail`.
- Cron `0 22 * * 1-5`, depois da janela da coleta.
- Itens conferidos (suposição): arquivos B3 do dia, histórico da ProfitDLL, frescor do tempo real e cálculos do portal. Sai 0 mesmo com FAIL.
- Para avisar no WhatsApp, siga o padrão da higiene:
  - `capabilities: [leitura, entrega]`;
  - `channels: [painel-local, whatsapp_out]`;
  - `alert` com `channel` e `destination` em `whatsapp_out`;
  - `destinations: [whatsapp_out]`;
  - `recipients: [DONO]`;
  - chave por dia e por item.
- O estado anterior fica com o próprio script, em `$1`. O id não está na lista fixa, então o Runner não fornece `MA_PREVIOUS_STATE_*`.
- Um vigia não pode escrever. Se for preciso disparar a coleta de novo, isso é trabalho de outra rotina.
- Para aparecer na Home, ligar o vigia em `apps/web/lib/vigias-saude.ts` (inferência, ver §6).

## 10. Regras do AGENTS.md que valem aqui

- **Always:** rodar `npm test` e reportar a saída; portão vermelho não é entrega.
- **Ask first:** dependência npm nova, migration ou schema, deploy, `prod/current`, ler ou colar segredo.
- **Never:**
  - commitar `.env` ou tokens;
  - mockar regra de negócio;
  - apontar o runtime para o checkout;
  - dar `docker.sock` ao container;
  - fallback automático entre rotas pagas;
  - uma segunda memória além do `ai-memory`.
- A publicação exige o recibo do portão para o SHA do HEAD, e não se publica a partir de worktree.
- A fundação não usa Jev nem modelo de linguagem para julgar evidência.
- Pela AD-008 em `.specs/STATE.md`, o dono aprova a ativação, inclusive em shadow, porque a sombra agendada já executa código.