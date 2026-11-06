# Gráficos TradingView na Jumba

- **URL:** https://jumba.com.br/tradingview
- **Acesso:** 2026-11-04, via WebFetch, sem login
- **Bruto:** `raw/tradingview.txt`

## Resumo
A página anuncia uma parceria com a TradingView. As ferramentas da Jumba passam a usar a biblioteca **Advanced Charts**, e o usuário pode salvar estudos e desenhos. A página também oferece um gráfico gratuito, sem cadastro, de ações da B3 com "Cotações diárias (fim de dia)".

## Telas e funcionalidades citadas
- Gráfico com indicadores (médias móveis, RSI, MACD), desenhos (suportes, resistências e tendências), vários tipos de gráfico e busca de ativos.
- Estudos e layouts que podem ser salvos (para usuários Jumba).

## Fórmulas e definições
Nenhuma.

## Dados e fontes mencionados
Ações listadas na B3, com cotação de fim de dia. A página não diz quem fornece os dados. No texto devolvido não aparecem a URL do datafeed nem a da biblioteca.

## Horários de atualização
Fim de dia.

## Observações
Os indicadores da Jumba (Walls, Gamma, Flow) não aparecem nesta página. Para a réplica, a TradingView Lightweight Charts (Apache 2.0) cobre o mesmo uso, como já anotado em `pesquisa/jumba-trader-fyt.md`.
