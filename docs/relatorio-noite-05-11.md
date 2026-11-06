# Relatório da noite de 04 para 05/11/2026

Tudo ficou nos branches, sem `main`, deploy, agente ativado, timer ou acesso automático à B3.

## O que está pronto

No Farol, branch `claude/project-thread-ugulea` (último push 60a6464, 07h56 BRT; portão do dev verde, 60 passaram, 717 testes de opções):

- **Base diária da B3:** importação offline dos arquivos públicos (cadastro, posições, prêmio, negócios, taxas), agora com fator de cotação, prazo do termo e publicação durável. Leitura pelo Portal através da Concessão do DataHub.
- **Motor:** calendário, curva DI, BSM, Black-76, Garman-Kohlhagen, vol implícita, SVI, agregados (PCR, Max Pain, titulares/lançadores, quebra do OI), exposição (GEX/DEX, perfil gamma, nível de troca de sinal), payoff e taxas contra o CDI.
- **Portal:** módulo Opções com os seis temas, calculadoras (preço, vol implícita, payoff), telas de cadeia, métricas, exposição, volatilidade, curva DI, IND e DOL, e Fluxo.
- **Vetores de teste:** 82 casos de preço, 12 de agregados, 26 de prazos, escala das exposições e curva DI, todos reproduzidos por gerador e com fontes públicas (B3, Cboe, livros, artigos).

## Revisão

- Quatro revisões adversariais do código, com três céticos por achado: 68 achados confirmados.
- Segunda rodada (sobre 2d1b141): das correções conferidas, 37 fecharam e 13 ficaram incompletas. O código novo das telas teve 20 achados. O mais grave: a vol implícita e a exposição nunca calculam para opções de ação reais, porque o cadastro da B3 não traz o multiplicador. Tudo voltou ao dev.
- Abertos no dev: o Fluxo ainda não aplica o filtro canônico da Fita (não confiar nos totais), a palavra "barreira" voltou no nome de uma tela, e a busca de estruturas precisa de teto total por pedido.

## Desenho do tempo real (sem código)

`desenho/d1-tempo-real.md`: séries perto do dinheiro ao vivo numa faixa própria do Portal, tudo desligado por padrão. A implementação espera as 15 perguntas da seção 7.

## Decisões suas, em ordem

1. **Fonte da base diária:** levantamento de UP2DATA e ProfitDLL em curso; trago a comparação e a recomendação.
2. **Integrar na `main`** (`integrar.sh`), depois que a segunda rodada de revisão fechar.
3. **Coletor da B3 que já roda em produção:** faz o mesmo tipo de download que a B3 veda.
4. **Material guardado:** apagar ou manter os 537 MB baixados antes do aviso e o material antigo do Jumba.
5. **Convenções** (sugestão entre parênteses): piso estrito da vol implícita (manter); nome do tema "Gamma e exposição" (manter e registrar o sentido); TOTAL-REG do COTAHIST (conferir num arquivo baixado à mão); theta por dia corrido; equilíbrio gamma-theta com juros; curva DI plana ou com vértices; DU B3 contra ANBIMA em 24/12 e 31/12.
6. **Tempo real:** as 15 perguntas do desenho.
7. **Agentes** (MeusAgentes#2 em rascunho): ativar depois da fonte e da integração.

O detalhe de cada frente está em `backlog.md`.
