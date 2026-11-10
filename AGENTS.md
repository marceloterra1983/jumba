# AGENTS.md — Jumba (sistema próprio)

Política canônica para agentes de IA neste repositório.

## Papel e fronteiras

Sistema próprio de análise de opções da B3, inspirado nas telas do Jumba e construído **exclusivamente com fontes públicas**.

- **Pesquisa, catálogo e vetores:** este repositório (`~/Projects/Jumba`, case-sensitive) concentra o catálogo de telas (`docs/catalogo-telas.md`), o backlog (`docs/backlog.md`), a base de conhecimento da B3 (`docs/conhecimento/`), o desenho de tempo real (`docs/desenho/`), as fontes e transcrições (`docs/fontes/`, lives em `docs/fontes/lives/`) e os vetores de teste reproduzíveis (`docs/vetores/`).
- **Código de produção no Farol:** o motor de opções (BSM, Black-76, Garman-Kohlhagen, SVI, GEX/DEX), o DataHub e as telas do Portal moram em `~/Projects/Farol` e integram exclusivamente pelo portão local do Farol (`integrar.sh`). Não editar Farol a partir de uma sessão só deste repo, salvo pedido explícito.
- **Agentes de apoio no MeusAgentes:** definições e execuções de agentes moram em `~/Projects/MeusAgentes`.
- **Restrição B3:** nenhuma coleta automatizada vedada pela B3 deve ser disparada. Qualquer decisão sobre a fonte da base diária ou sobre o acervo histórico aguarda deliberação explícita do dono.

## Memória e escopo

- ai-memory: `workspace = "default"`, `project = "jumba"` (ver `.ai-memory.toml`). Worktrees (se houver) colapsam no mesmo projeto canônico.
- Worktree extra **não é esperada** neste repo; o trabalho fica na `main` local. Não criar `.worktrees/` sem pedido.

## Git e segredos

- GitHub é **backup**: push normal para `origin`; **sem force-push** em `main`/`master`.
- Nunca commitar `.env`, tokens, chaves, credenciais ou dumps. Áudio das lives (`docs/fontes/lives/audio/`) fica fora do git (ver `.gitignore`).

## Teste oficial deste repositório

Não há suíte C#/npm aqui (isso vive no Farol). O teste reproduzível local é regenerar os vetores e o calendário:

```bash
python3 -I docs/vetores/geradores/gera_precificacao.py --saida docs/vetores/ --espera 0
python3 -I docs/vetores/geradores/gerar_agregados.py --saida docs/vetores/
python3 -I docs/conhecimento/b3-outros/scripts/gerar_calendario.py
```

Saída esperada: scripts terminam com código 0; `precificacao.json` / `agregados.json` / `feriados-b3-2026-2028.json` reescritos de forma determinística.
