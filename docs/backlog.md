# Backlog do sistema de opções (trabalho noturno de 04 para 05/11/2026)

Regras em vigor: só fontes públicas (B3 e fórmulas publicadas), nomes e textos próprios, nada de
voltar ao site do Jumba (confirmado em 05/11 08h11). Nenhum acesso automático a b3.com.br. Sem `main`, deploy,
ativação, agendamento, timers, `.env`, matriz ou apagar material guardado sem ok do Marcelo.
Farol: nunca abrir PR; portões só no dev (`scripts/dev/integrar.sh --verificar`).

"Completo" = tudo construído, testado e revisado nos branches, pronto para o ok dele.

## A. Dados (DataHub)

- [x] A1 Importação offline da base diária pública (SPEC-0523), branch `claude/project-thread-ugulea`.
- [!] A2 PARADO (a B3 veda coleta automatizada; 537 MB parciais guardados sem uso no dev). Era: baixar já os arquivos públicos de todos os pregões ainda disponíveis
  (posições em aberto somem em ~21 pregões) para uma pasta no dev, fora da História e do repositório.
- [!] A3 PARADO até decidir a fonte (cartão de 05/11). Coleta diária automática: job do scraper que baixa os arquivos do dia e chama a importação.
  Código e testes; agendamento só com ok.
- [x] A6 Curva DI no Portal (F14, SPEC-0543, e4dbc6b): motor PU/taxa/termo, rota e página; origem real devolve ausência até haver fonte. Revisão adversarial: 12 achados (quase todos lacunas de teste); o do gerador fora do teste de reprodução corrigido na nuvem (2f2aaab), os outros 11 enviados ao dev.
- [ ] A4 Fontes que faltam confirmar: prêmio de referência (séries sem negócio), proventos e eventos
  corporativos, aluguel (BTB), participação de investidores.
- [x] A5 Leitura da base diária pelo Portal (Concessão), por data e objeto (SPEC-0532, 5bd6e9b). Revisão adversarial em curso.

## B. Motor (Portal, `Modules/Options`)

- [x] B1 Calendário, curva DI, BSM, Black-76, vol implícita, SVI (SPEC-0524).
- [x] B2 Agregados e exposições (F4): PCR, Max Pain, IQ, quebra do OI, GEX/DEX, flip, walls,
  equilíbrio gamma-theta, payoff, taxa contra o CDI, buscadores. Ligado aos vetores (388eede). Revisão adversarial em curso.
- [ ] B3 Garman-Kohlhagen para opções de dólar: o motor não cobre (achado 13 do ciclo 1, pedido ao dev).
- [x] B4 Parada do Newton mais fina (dd1d36a: para também pela correção de sigma). Prêmio no piso devolve sigma 0: convenção para o Marcelo.

## C. Portal (menu próprio por tema)

- [x] C1 Módulo com menu: Opções, Gamma e exposição, Volatilidade, Fluxo, Juros e eventos, Estruturas (F5, 111c7eb). Calculadoras (F13, f6c6d17).
- [ ] C2 Telas ligadas aos dados, tema a tema. Cadeia e métricas (SPEC-0541, d24fc8c), exposição e volatilidade (SPEC-0542/0544, 5e73e4c) no ugulea em 2d1b141, portão verde; buscadores (SPEC-0550) em curso no dev. Revisão do ciclo 2 em curso.
- [ ] C3 Fluxo pela Fita (grupos de corretoras, negócios grandes), heurística própria declarada. SPEC-0554 no ugulea (60a6464, portão verde). Defeito conhecido: ainda sem o filtro canônico da Fita (edição em dobro, leilão e quantidade zero no total); correção na SPEC-0555 em curso.
- [ ] C4 Históricos (vol implícita, Max Pain, exposição perto do dinheiro), que dependem da base acumulada.
- [x] C5 IND e DOL (SPEC-0553, 60a6464, portão verde). Falta recusar referenceKind=future sobre ação (SPEC-0555).

## D. Tempo real

- [x] D1 Desenho pronto em desenho/d1-tempo-real.md (faixa própria no Portal, conjunto fixo no dia, ritmo de 1 série a cada 6 s, tudo desligado por padrão), revisado por 3 céticos (38 pontos tratados). Implementação só depois das 15 perguntas da seção 7, em especial o efeito sobre o catch-up congelado (ADR-0040).

## E. MeusAgentes

- [x] E1 PR #2: projeto farol, coleta e vigia em shadow.
- [!] E2 PARADO junto com A3. Ajustar coleta e vigia ao comando de importação da SPEC-0523.

## F. Verificação (em ciclo)

- [ ] F1 Revisão adversarial de cada push (nuvem) e correções pelo dev. As quatro listas (68 achados) fechadas pelo dev em 96279b7 (05/11 06h57 BRT, portão verde, 717 testes de opções). Abertos: «barreiras» voltou no nome das telas da cadeia; busca de estruturas sem teto total por pedido. Ciclo 2 (2d1b141): das 56 correções, 37 resolvidas, 13 incompletas; 20 achados novos no código das telas (altos: vol implícita e exposição nunca calculam para opções de ação reais porque o IN não traz multiplicador; rolagem volta ao topo a cada segundo; 0.250 lido como 250 nas calculadoras). Quinta lista enviada ao dev em 05/11 ~11h30 UTC. Ciclo 1 (5fecc33): 22 achados confirmados, lista enviada ao dev em 05/11 05h UTC; o do vetor de IQ (critério de barreira de terceiro) corrigido na nuvem (65ec900). F4/F5 (b896247): 17 achados confirmados, lista enviada ao dev em 05/11 ~05h30 UTC; fontes dos vetores de agregados trocadas por B3, Cboe, livros e artigos (b0d4a0b). F10/F13 (8cd370b): 17 achados confirmados (o mais grave: gráfico de payoff espaça pontos por índice; e a publicação diária sem fsync), lista enviada ao dev em 05/11 ~05h40 UTC.
- [ ] F2 Vetores extras: DU a partir de datas (B3 e ANBIMA), escala de GEX/DEX. Gerados e testados (5d155a9); falta ligar aos testes C# (pedido ao dev).
- [x] F3 Catálogo próprio das telas (catalogo-telas.md, 37 telas em 6 temas e IND/DOL), revisado em 05/11. Atualizar status depois de F4/F5/F10/F13.

## G. Para o Marcelo decidir na volta

- Integrar na `main` (`integrar.sh`), ativar os agentes, agendar a coleta.
- Apagar ou manter o material do Jumba guardado (notas, perfil do navegador, páginas públicas).
- Matriz de agentes com o Codex primeiro.
- Convenções em aberto: theta por dia corrido, equilíbrio gamma-theta com r > 0, curva DI plana
  contra curva com vértices, DU B3 contra ANBIMA em 24/12 e 31/12.
- ~~Cartão de 05/11: voltar ou não ao site do Jumba.~~ Decidido 05/11 08h11: seguir só com fontes públicas.
- Fonte da base diária: decidido 05/11 09h50 «ProfitDLL + download manual». Eu testo a DLL no Host num pregão, só leitura. Em 05/11 o mapeamento mostrou que o Host em produção não repassa contratos em aberto, ajuste, fechamento anterior nem ficha (só memória); teste não rodou, decidido 05/11 12h03 «Leitura nova no Host»: leitura de diagnóstico sem ordem num branch; desenho em knowledge/estudo/sonda-de-series.md (rlj93h f769439), implementação mandada ao dev 05/11 ~13h BRT; integrar e publicar esperam o ok dele (mapa em fontes/teste-profitdll-05-11.md); ele baixa os arquivos da B3 à mão e pede a cotação do UP2DATA. Levantamento no Claude Doc https://claude.ai/artifact/ELZTiVURCZZjLKxxe42uqb.
- O coletor da B3 que já roda em produção faz o mesmo tipo de download vedado.
- O que fazer com os 537 MB baixados antes do aviso.
- Nome do tema «Gamma e exposição» (choca com «Exposição» do CONTEXT.md). Sugestão: manter e registrar o sentido novo.
- Piso da vol implícita: limite estrito nos dois pisos, vencida a prêmio zero dá Expired. Sugestão: manter.
- TOTAL-REG do COTAHIST: não se sabe se conta cabeçalho e rodapé; hoje só gera aviso. Conferir num arquivo baixado à mão.
- Navegação de Opções (seis temas e segunda fileira de páginas) foge da convenção de grupos do AGENTS.md: aceitar e registrar a exceção, ou voltar ao padrão.
- Tempo real das opções (D1): as 15 perguntas da seção 7 de desenho/d1-tempo-real.md, sobretudo se a faixa nova pode pôr carga no catch-up congelado sem novo ADR.
