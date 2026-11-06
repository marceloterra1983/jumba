# 04. Participação dos investidores por tipo (à vista e derivativos)

Acesso: 2026-11-04. Legenda: [C] B3 lido; [T] terceiros; [S] suposição.

## A. Segmento listado de ações: seção "Participação dos Investidores" do BDI

| Item | Valor |
|---|---|
| Exemplo lido | [BDI_02_20240321.pdf](https://arquivos.b3.com.br/bdi/download/bdi/2024-03-21/BDI_02_20240321.pdf) [C] |
| Padrão de URL | `https://arquivos.b3.com.br/bdi/download/bdi/{AAAA-MM-DD}/BDI_02_{AAAAMMDD}.pdf` [C] |
| Formato | **PDF** (capítulo 02 do BDI). Não se achou CSV equivalente [S: procurar em `#selectTabelas`] |
| Categorias | Institucionais; Instituições Financeiras; Investidor Estrangeiro; Investidores Individuais; Outros [C] |
| Tabela 1 | "Investidores no Volume Total da B3": **acumulado do mês até D-2** (o BDI de 21/03 trazia até 19/03). Compras e vendas em R$ mil e % [C] |
| Tabela 2 | Mensal do mês anterior por mercado: **Vista, Termo, Opções, Exercícios de Opções, Blocos, Total Geral** (compras + vendas, R$ e %). Atualizada no 2º dia útil do mês [C] |
| Histórico | Um PDF por dia; a retenção do BDI não foi medida [S] |

**Exemplo** (R$ mil, acumulado de março/2024 até 19/03):

| Investidor | Compras | % | Vendas | % |
|---|---|---|---|---|
| Institucionais | 89.126.068 | 13,21 | 87.802.713 | 13,01 |
| Investidor Estrangeiro | 181.705.844 | 26,93 | 185.973.917 | 27,56 |

**Fluxo diário:** a diferença entre dois acumulados seguidos dá o saldo de um dia, com defasagem de 2 pregões. Na virada do mês, o acumulado zera [S: inferência; o PDF não publica o diário].

## B. Derivativos (futuros DOL, WDO, IND, WIN, DI1, DDI)

- **Volume por tipo de investidor:** a seção do BDI **não** cobre futuros; em derivativos, só opções e exercícios de opções de ações [C]. Para IND/WIN, a SPEC-0021 do Farol já concluiu que **não existe série diária gratuita** de volume por tipo de investidor.
- **Posição em aberto por tipo de participante:** a B3 publica esse dado. Relatórios de corretoras o reproduzem como "Contratos em aberto (B3)" ([exemplo da Ativa, 14/02/2023](https://acionista.com.br/wp-content/uploads/2023/02/Contratos-em-aberto-Ativa-Investimentos-14.02.23.pdf)).
  - **Categorias:** Bancos; DTVMs e Corretoras; Outras Jurídicas Financeiras; PJ Não Financeira; Investidor Institucional Nacional; Investidores Não Residentes; Pessoa Física; Banco Central.
  - **Contratos:** DOL, WDO, DDI, SCS, DI1, DAP, futuro de Ibovespa e mini.
  - **Origem:** a página atual da B3 **não foi localizada** nesta coleta. A antiga ficava no site da BM&F (www2.bmf.com.br), que agora redireciona para a B3 [S]. **Pendência alta:** é o dado mais próximo do "Fluxo de Investimentos" para IND/DOL. Procurar no BDI › Derivativos.

## C. Book Pessoa Física (trimestral, contexto)

- PDFs trimestrais da B3, por exemplo o [Book PF 1T26](https://b3.com.br/data/files/EA/80/8F/5D/FDFDD910E7DB5DD9AC094EA8/Book%20PF%201TRI%202026.pdf), com perfil e volume de pessoas físicas. Não foram lidos.
- No Hub de Dados Públicos, "Mercado à vista (opções) › perfil de pessoas físicas" tem recortes por idade, estado e gênero [C].

## Limitações

- O dado diário por tipo de investidor só sai em PDF, acumulado no mês e com D-2. Extrair do PDF exige um leitor de PDF, que é dependência nova e precisa de aprovação.
- **Sem alternativa gratuita** para volume diário por tipo de investidor em futuros.
