# Conteúdo público do Jumba: índice

- **Acesso:** 2026-11-04, sem login, só páginas públicas.
- **Como baixei:** pelo WebFetch. O curl direto foi bloqueado pelo proxy de saída (CONNECT 403) para jumba.com.br, t.me, youtube.com e hotmart.com.
- **Ritmo e robots.txt:** uma requisição por site por vez, cada uma levando vários segundos. Conferi o robots.txt de jumba.com.br, hotmart.com, youtube.com e legacy.jumbafyt.com.br (`raw/robots-*`). O do t.me não abriu.
- **Limite da ferramenta:** o WebFetch não devolve o HTML. Devolve texto já resumido, com citações curtas de até cerca de 125 caracteres. Por isso, `raw/` guarda o **texto que a ferramenta devolveu**, não a página original.
- **Rotas logadas:** nenhuma foi aberta (`/pro/*`, `/login`, `/register`, `/gamma-mapa/`, `/especializacao-hedges-manejos/entrar`).
- **Pesquisa anterior:** já lida e não repetida (`docs/pesquisa/`).

## Notas: site jumba.com.br
| Nota | URL | Destaque |
|---|---|---|
| `site-home.md` | https://jumba.com.br | 5 planos (Free, Pro, Trader, Insights, FYT); FAQ; a tabela de planos chega com textos de exemplo |
| `site-produtos.md` | https://jumba.com.br/produtos | Lista oficial das funcionalidades de cada produto |
| `site-jumba-pro.md` | https://jumba.com.br/jumba-pro | Combo O.M.G.; 80+ ativos; preços R$ 247 / 1.257 / 2.227 |
| `site-jumba-trader.md` | https://jumba.com.br/jumba-trader | Walls antes do pregão; exportação para o Profit; R$ 197 |
| `site-jumba-trader-flow.md` | https://jumba.com.br/jumba-trader-flow | Smart Money em verde, Varejo em rosa, Walls em azul; "Dados BMF em tempo real"; R$ 327 |
| `site-jumba-fyt.md` | https://jumba.com.br/jumba-fyt | 23 estruturas listadas; rolagens; alertas; 9 ativos |
| `site-tradingview.md` | https://jumba.com.br/tradingview | Advanced Charts; gráfico público de fim de dia |
| `site-quem-somos.md` | https://jumba.com.br/quem-somos | Definições curtas de Walls, Mapa, IQ e Market Gamma |
| `site-educacional.md` | https://jumba.com.br/c/educacional | Exige login: Educacional, News e FAQ ficaram de fora |
| `site-o-codigo-das-opcoes.md` | https://jumba.com.br/o-codigo-das-opcoes | Módulo 10 = mapa oficial das telas do Pro |
| `site-especializacao-hedges-manejos.md` | https://jumba.com.br/especializacao-hedges-manejos | 15 módulos; robô PnT, FlexScan e Profit |
| `site-quick-trade.md` | https://jumba.com.br/quick-trade | Redireciona (302) para a Empiricus (não seguido) |
| `site-insights.md` | https://jumba.com.br/insights | Produto em reformulação |
| `site-codigo-de-conduta.md` | https://jumba.com.br/codigo-de-conduta | Conduta de analistas (CVM 20) |
| `site-legacy.md` | https://legacy.jumbafyt.com.br/legacy | Só a meta descrição (página montada por JavaScript) |
| `site-pages.jumba.com.br.md` | https://pages.jumba.com.br/market-gamma-jumba-pro | SERVER_ERROR |
| **`termos-de-uso.md`** | https://jumba.com.br/termos-de-uso | Automação, cópia, engenharia reversa e multas, com citações |
| `glossario-jumba.md` | (derivado) | 30 termos com definição pública e fonte |

## Notas: Hotmart
| Nota | URL |
|---|---|
| `hotmart-combo-pro-trader.md` | https://hotmart.com/pt-br/marketplace/produtos/jumba-pro-jumba-trader-combo/Q90970656B |
| `hotmart-combo-pro-flow.md` | https://hotmart.com/pt-br/marketplace/produtos/jumba-pro-jumba-trader-flow-combo/R103220460G |
| `hotmart-combo-flow-pro-fyt.md` | https://hotmart.com/pt-br/marketplace/produtos/jumba-trader-flow-jumba-pro-find-your-trade-combo/T96724476E |
| `hotmart-combo-pro-fyt.md` | https://hotmart.com/pt-br/marketplace/produtos/jumba-pro-find-your-trade-combo/T86010315Q |

## Notas: YouTube
- **Canal:** `youtube-canal.md`, com a tabela dos 10 vídeos.
- **Vídeos:** `youtube-TrsidrGxnMw.md`, `youtube-eIZ7xcFAoL4.md`, `youtube-mUYc0MQsqP4.md`, `youtube-sd8YYjLHb0o.md`, `youtube-heCjEQknIak.md`, `youtube-QfoE6IJ9o-U.md`, `youtube-wcXSxacgojA.md` e `youtube-6gsJ3AS5wfU.md`.
- **Sem conteúdo:** k4mC3y7EhhE e WqM6Sl5QPcU vieram como página genérica; ficou só o registro em `raw/`.
- **Conclusão:** as descrições não trazem metodologia, que só aparece na fala dos vídeos.

## Notas: Telegram t.me/s/mapadeopcoes (715 inscritos, cerca de 1.887 mensagens)
**Amostragem:** li 15 páginas, cerca de 300 mensagens. As mais recentes de 1679 a 1887 estão completas, e o resto são amostras: 1478–1499, 1180–1199, 880–899, 576–599 e 279–298. Também fiz 10 buscas no próprio canal, que pegam o histórico todo pelos termos-chave.

| Nota | URL / faixa |
|---|---|
| `telegram-p1-1868-1887.md` | t.me/s/mapadeopcoes |
| `telegram-p2-1848-1867.md` | ?before=1868 |
| `telegram-p3-1828-1847.md` | ?before=1848 (MidWalls pontilhadas, Wall branca) |
| `telegram-p4-1808-1827.md` | ?before=1828 (Payoff beta: min/máx/Flip, BGT, Max Pain, Preço Jumba) |
| `telegram-p5-1787-1806.md` | ?before=1808 |
| `telegram-p6-1764-1786.md` | ?before=1787 (polaridade do gamma, IQ, Flip do IBOV) |
| `telegram-p7-1741-1763.md` | ?before=1764 (Max Pain, Flip no BOVA11 a 177) |
| `telegram-p8-1721-1740.md` | ?before=1741 (rolagem, vencimento +1h, Walls no WIN) |
| `telegram-p9-1700-1720.md` | ?before=1721 (lista de produtos, Jumba Alpha) |
| `telegram-p10-1679-1699.md` | ?before=1700 |
| `telegram-p11-1478-1499.md` | ?before=1500 (mínimo do gamma em CYRE3) |
| `telegram-p12-1180-1199.md` | ?before=1200 |
| `telegram-p13-880-899.md` | ?before=900 |
| `telegram-p14-576-599.md` | ?before=600 (Fence, rolagens ATM) |
| `telegram-p15-279-298.md` | ?before=300 (Mapa grátis; pré-lançamento das Walls) |
| `telegram-busca-flip.md` | ?q=Flip (**definições de 2022: Flip, gamma ±, Put e Call Gamma Wall**) |
| `telegram-busca-bands.md` | ?q=Bands (**Bands = histórico do máximo e do mínimo do gamma**) |
| `telegram-busca-iq.md` | ?q=IQ (**critério de barreira: descoberto > 5 mi e IQ > 1,2**) |
| `telegram-busca-walls.md` | ?q=Walls |
| `telegram-busca-shark.md` | ?q=Shark |
| `telegram-busca-pcr.md` | ?q=PCR |
| `telegram-busca-aluguel.md` | ?q=aluguel (**lista oficial e comentada do Pro, 2023**) |
| `telegram-busca-maxpain-bgt.md` | ?q=Max+Pain, ?q=BGT |
| `telegram-busca-atualiza.md` | ?q=atualiza |

## O que ficou de fora e por quê
- **Exigem login:** menus Educacional, News, Suporte/FAQ e glossário da área logada.
- **Não existem em forma pública:** blog e política de privacidade. Não achei nem link nem página.
- **Erro de servidor:** pages.jumba.com.br.
- **Não seguido:** o redirecionamento do Quick Trade para a Empiricus.
- **Bloqueado pelo robots.txt:** o RSS do YouTube.
- **Telegram:** cerca de 1.500 mensagens antigas não foram lidas página por página. As buscas por termo cobrem a parte técnica delas.

## Os 10 achados mais úteis para replicar as telas
1. **O Market Gamma é uma tela de níveis em preço, não só um gráfico de barras.** Para cada ativo mostra:
   - Put Gamma Wall, Flip e Call Gamma Wall;
   - mínimo e máximo do gamma;
   - ao lado do fechamento anterior, da abertura e do preço atual.

   Exemplo do IBOV: 104,8k / 116,9k / 123,3k, com o atual às 10h04 (Telegram 124, 1812, 1490). O Flip é dado em pontos do IBOV ou em preço do BOVA11 ("acima de 177", Telegram 1762).
2. **O regime de gamma (positivo ou negativo) é relido durante o pregão.** O OI é diário (o "Mapa atualiza diariamente"), mas a leitura muda com o preço: "abriu em gamma negativo... voltou a operar em Market Gamma positivo" (Telegram 125, 1771). Na réplica: OI de D-1 da B3 e Γ recalculado com o spot ao vivo.
3. **Market Gamma Bands = duas séries temporais por ativo e por vencimento ("dentro de um exercício").** São o nível de preço do máximo do gamma (linha verde) e o do mínimo (linha vermelha), sobrepostos ao preço. "O preço do ativo raramente rompe essas linhas". Existe também uma lista de "ativos no mínimo do gamma" (Telegram 765, 1103, 790, 929). Para isso, basta guardar uma foto diária do máximo e do mínimo.
4. **O IQ tem duas séries, uma de calls e outra de puts, desenhadas ao longo do tempo contra o preço (linha branca).** A leitura é o cruzamento ou a "boca de jacaré". A base é titulares ÷ lançadores (Telegram 560–564, 1779; Código das Opções M10). Os campos vêm direto do arquivo de posições em aberto da B3.
5. **O Scanner de Barreiras tem um critério público de exemplo:** strikes com "volume descoberto acima de 5 milhões e IQ acima de 1,2" (Telegram 1597). O Mapa tem também "Maiores variações" (Telegram 1047), provavelmente a variação de OI contra D-1.
6. **Walls e MidWalls:**
   - A Wall é a linha cheia (branca no gráfico do canal, azul na página do Flow) e as MidWalls são pontilhadas.
   - Saem antes da abertura e ficam fixas durante o dia.
   - Ficam nos pontos de maior probabilidade de delta hedge dos MMs.
   - Existem para IND, DOL e ações e são exportadas "diretamente para o Profit".
   - Níveis reais para validar a réplica: WIN 163.385 (Wall) e 163.900 (MidWall); WIN 169.552; WDO 5.208 (MidWall); DOL 6.018.

   Fontes: Telegram 1843, 1734, 1841, 1493, 1712, 1856; /jumba-trader-flow.
7. **O Trader Flow é um painel abaixo do candle, em tempo real.** Mostra Smart Money (verde), Varejo (rosa) e Market Makers, medindo "de que lado grandes players estão agredindo". É saldo de agressão por grupo de corretoras, com "Dados BMF em tempo real" (/jumba-trader-flow; Telegram 1857, 1843). A ProfitDLL fornece isso; o Farol já grava agressor e agentes.
8. **Shark Map e Shark Positions:**
   - **Shark Map:** as "maiores operações executadas na B3, em tempo real", com janela de "últimos 30 dias" de operações relevantes por ativo.
   - **Shark Positions:** reconstrói estruturas (pontas compradas e vendidas, custo de montagem, payoff). Exemplo: "Trava de Baixa de PUTs com 4,2 milhões de opções".

   Fontes: Telegram 1045, 1047, 514, 280. O limiar de "grande" não é publicado.
9. **O Payoff do FYT mostra:**
   - snapshot do book;
   - mínimo, máximo e Flip do gamma, BGT e Max Pain sobrepostos;
   - vol e skew ajustáveis por vencimento;
   - "Preço Jumba", o preço teórico pela curva de vol;
   - impacto do spread de entrada e saída.

   As rolagens do FYT aparecem numa tabela ATM por ativo, com valor negativo = crédito, para o vencimento atual e o próximo (Telegram 1812, 1721, 1722, 596; /jumba-fyt). A curva de vol "estima o preço teórico/justo de uma opção sem book" (Telegram 1047).
10. **Lista oficial e completa das telas do Pro, para a checklist.** São 12 itens:
    - Market Gamma
    - Bands
    - Mapa (com Maiores variações e Scanner de barreiras)
    - Histórico do Mapa
    - Shark Map
    - Shark Positions
    - Walls
    - PCR ("busca por proteção via puts")
    - IQ do ativo e IQ Global
    - Fluxo de investimentos (estrangeiro, institucional, PF e instituição financeira)
    - Curva de vol implícita ajustada
    - Mercado de aluguel e Eventos Corporativos (datas de resultados trimestrais)

    Fontes: /produtos; Telegram 1047, 990; Código das Opções M10. BGT e Max Pain só aparecem dentro do Payoff (Telegram 1812). Gamma Score, Resumo do Gamma e Curva de Juros **não aparecem em nenhuma fonte pública**. Pelos Termos (cláusula 6), a Jumba recebe os dados em tempo real da **Cedro Technologies**, não da ProfitDLL.

**Ressalva:** as fórmulas exatas (sinal da GEX, quantas walls, limiares, BGT) seguem sem fonte pública. Os achados acima mostram a *forma* das telas e dão números reais para validar a réplica.
