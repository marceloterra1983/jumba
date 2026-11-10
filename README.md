# Jumba (sistema próprio)

Sistema próprio de análise de opções da B3, inspirado nas telas do Jumba, construído **só com fontes públicas**.

Path canônico: `~/Projects/Jumba` (case-sensitive).

## Estrutura

- `docs/catalogo-telas.md`, `docs/backlog.md` — catálogo e backlog do sistema.
- `docs/conhecimento/` — base B3 e material público Jumba (só fontes públicas).
- `docs/fontes/lives/` — transcrições de lives (`.txt`; VTT de origem quando houver; áudio local ignorado pelo git).
- `docs/vetores/` — vetores de teste reproduzíveis + geradores Python.
- `docs/desenho/`, `docs/pesquisa/` — desenho (ex.: tempo real) e pesquisa.

## Teste local

Ver `AGENTS.md` (regenerar vetores e calendário com `python3 -I`).

## Repositórios relacionados

- [Farol](https://github.com/marceloterra1983/Farol) — motor, DataHub e Portal (produção).
- [MeusAgentes](https://github.com/marceloterra1983/MeusAgentes) — agentes de apoio.

O código de produção continua nesses repositórios; este repo é pesquisa, catálogo e vetores.
