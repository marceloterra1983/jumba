# Telegram @mapadeopcoes: busca "Flip"

- **URL:** https://t.me/s/mapadeopcoes?q=Flip
- **Acesso:** 2026-11-04, via WebFetch (busca pública t.me/s, sem login). A ferramenta só enxerga o recorte de resultados que a página devolve.
- **Bruto:** `raw/telegram-busca-flip.txt`

## Resumo
A busca mais valiosa. As mensagens da fase inicial (78 a 268, de 2022) **definem** os termos do Market Gamma e trazem os níveis do IBOV.

## Telas e funcionalidades citadas
- **Mensagem 124:** pontos do IBOV, com Put Gamma Wall em 104,8k, Flip em 116,9k e Call Gamma Wall em 123,3k, ao lado do fechamento anterior, da abertura e do preço atual "(10h04)".
- **Mensagem 268:** "Market Gamma mostra o Gamma dos principais ativos da B3". O endereço antigo era jumba.com.br/gamma-mapa/ (não aberto).
- **Mensagem 125:** o Mapa "atualiza diariamente todas as séries em aberto (travadas, cobertas e descobertas)".

## Fórmulas e definições
- **Flip** = "ponto de transição entre o gamma positivo e negativo", ou seja, onde a curva cruza zero (mensagens 78 e 91).
- **Perto do Flip,** os formadores "acabam levando o papel para esse ponto" (efeito pin).
- **Gamma positivo** segura a volatilidade (mensagem 91).
- **Gamma negativo:** "Se entra venda o MM vende junto". O MM faz delta hedge vendendo o papel (mensagem 261).
- **A influência do gamma** é maior em ativos com muito OI e perto do vencimento (mensagem 125).
- **Níveis do Market Gamma:** Put Gamma Wall, Flip, Call Gamma Wall, mínimo e máximo.

## Dados e fontes mencionados
B3: séries em aberto, travadas, cobertas e descobertas.

## Horários de atualização
- O Mapa atualiza todo dia.
- Os níveis do Market Gamma ficam ao lado do preço atual, durante o dia ("10h04").
- O regime é lido durante o dia (mensagem 1771).
