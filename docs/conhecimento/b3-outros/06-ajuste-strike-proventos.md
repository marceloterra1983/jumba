# 06. Ajuste do preço de exercício (strike) das opções por proventos

Acesso: 2026-11-04. Legenda: [C] B3 lido; [T] terceiros; [S] suposição.

## Onde está a regra

- **Contrato:** cláusula 5 dos contratos de opções sobre ações, units, ETFs e BDRs ([OC 007/2026-VPC](https://www.b3.com.br/data/files/05/A1/CA/C2/EFE2C91076A8EEB9AC094EA8/OC%20007-2026-VPC%20ALTERACOES%20CONTRATOSTERMO%20OPCOES%20ACOES%20UNITS%20ETFS%20BDRS%20FUTURO%20ACOES%20UNITS%20REPUBLICACAO%20CONTRATOS%20DERIVATIVOS%20EQUITIES.pdf), de 05/02/2026). A B3 "poderá ajustar o preço de exercício e a quantidade em valor equivalente ou proporcional ao evento corporativo". Os detalhes ficam no MPO da Câmara [C].
- **Regra detalhada:** **Manual de Procedimentos Operacionais (MPO) da Câmara B3, Capítulo 7, seção 7.9.1** ("Tratamento de eventos corporativos para opções sobre ativos do mercado à vista"), **páginas 211 a 223**. Versão lida: capa de 22/06/2026; Capítulo 7 na versão 38, de 09/03/2026 ([PDF](https://www.b3.com.br/data/files/57/86/30/A8/4C8D0A105BF9020AAC094EA8/MPO%20da%20Camara%20B3.pdf)) [C: índice].
  - **O texto da 7.9.1 não foi lido.** O WebFetch só converte os primeiros 99.356 caracteres do PDF, até a seção 5.1.2.2.
  - **Pendência número 1** desta pasta: baixar o PDF (`scripts/baixar-documentos.sh`) e extrair as páginas 211 a 223.
- **Insumo de preço ex:** [Manual de Precificação de Eventos Corporativos, v5 de 09/01/2023](https://www.b3.com.br/data/files/2C/B0/39/4D/AFA538101E311E28AC094EA8/Manual%20de%20Eventos%20Corporativos.pdf), que serve, entre outras coisas, para o "ajuste dos preços de exercício das opções listadas" [C]:
  - dinheiro: `Pcom = Pex + X`;
  - bonificação: `Pcom = Pex·(1+B)`;
  - desdobramento e grupamento: `Pcom = Q·Pex`;
  - subscrição: `Pex = (Pcom + w·K)/(1+w)`, se `Pcom > K`, com `w = M/N`.

## O que está confirmado

| Ponto | Regra | Fonte |
|---|---|---|
| Proventos em dinheiro usam **valor líquido de impostos** | O MPO (7.9.1, item 1) descreve a variável das fórmulas como valor líquido de impostos. Desde 09/03/2026, sem tabela fixa de alíquotas | [C] [OC 006/2026-VPE](https://b3.com.br/data/files/3D/25/CE/4A/E9EBC910F37907C9AC094EA8/OC%20006-2026-VPE%20TRATAMENTO%20DE%20EVENTOS%20CORPORATIVOS%20EM%20RECURSOS%20FINANCEIROS%20LIQUIDOS%20DE%20IMPOSTOS_PT.pdf), de 05/03/2026 |
| JCP a partir de 01/01/2026 | Alíquota de IR de **17,5%** (fator 0,825), pela Lei Complementar 224/2025. Vale para futuros e opções sobre renda variável e para o ajuste de preço do à vista | [C] [OC 026/2025-VPE](https://www.b3.com.br/data/files/0F/23/BA/E4/1117B9105B12E5A9AC094EA8/OC%20026-2025-VPE%20ATUALIZACAO%20NA%20TRIBUTACAO%20DE%20JCP%20DE%20CONTRATOS%20FUTUROS%20E%20OPCOES%20A%20PARTIR%20DE%202026_PT.pdf), de 30/12/2025 |
| Provento ≥ strike | O tratamento padrão do MPO não se aplica. Ajuste **multiplicativo**: `PEAj = PE × F` (2 casas, arredondado), `QTDAj = QTD / F` (truncado, 0 casas), `F` com 8 casas, calculado pela razão entre o preço ex (abertura depois do evento) e o preço com (fechamento antes). Há regra de equalização entre posições compradas e vendidas | [C] [OC 141/2023-PRE](https://www.b3.com.br/data/files/44/41/F8/1E/E90E98101D7C7D98DC0D8AA8/OC%20141-2023%20PRE%20Tratamento%20para%20Dividendos%20Superiores%20ao%20Strike_Petrobras%20(PT).pdf), Petrobras, com até 21/08/2023 e ex em 22/08/2023. Casos parecidos: OC 058/2023, 065/2023, 081/2023, 093/2022, 112/2021 (VALE3) |
| Séries com strike > provento | "Tratamento inalterado, nos termos do MPO" | [C] OC 141/2023 |
| Empréstimo (BTB) | Eventos em dinheiro não alteram preço nem quantidade. O reembolso segue a tributação do doador | [C] OC 026/2025-VPE |

## Regra usual, ainda a confirmar no MPO 7.9.1 [S]

```
dinheiro (dividendo, JCP, rendimento):  K_aj = K − P_liq     # P_liq = valor líquido de impostos (JCP: bruto × 0,825 em 2026)
                                        quantidade não muda
bonificação B (ex.: 10% = 0,10):         K_aj = K / (1 + B);   Q_aj = Q × (1 + B)
desdobramento/grupamento fator Q:        K_aj = K / Q;         Q_aj = Q × Q
subscrição:                             fator pelo preço ex teórico do Manual de Precificação [S]
data de aplicação:                      abertura da data ex (primeiro pregão sem direito)
arredondamento:                         2 casas no strike [S; no OC 141 é arredondamento na 2ª casa]
```

- A dedução direta (`K − P`) para proventos em dinheiro é a prática conhecida do mercado. **Não foi lida nesta coleta.** O OC 141/2023 só diz que, quando o provento é maior ou igual ao strike, "o tratamento padrão" não se aplica, o que é coerente com a dedução direta (o strike ficaria ≤ 0).
- **Dividendos tributados a partir de 2026** (Lei 15.270/2025: retenção na fonte sobre dividendos acima de certo valor mensal por pessoa física) [S]. O OC 006/2026-VPE generalizou o texto para "líquido de impostos". **Não se sabe que alíquota a B3 aplica a dividendos no ajuste.** Confirmar no MPO.

## Consequência para o motor (BSM)

- Como o strike já desconta o provento em dinheiro, **não** some também o dividend yield no BSM para proventos já anunciados até o vencimento. Isso contaria o provento duas vezes (critic.md, item 8).
- Para proventos **não anunciados**, o strike não muda. O modelo precisa de uma premissa própria de dividendo, que não vem de nenhuma fonte pública.
- **Histórico de ajustes:** comparar o `ExrcPric` do BVBG.028 entre D-1 e D (nota 05-C) e conferir com a consulta "ajuste de proventos" (nota 05-B).

## Pendências

1. Ler o MPO da Câmara, seção 7.9.1, páginas 211 a 223. Ele traz as fórmulas, o tratamento de dividendos com IR, de subscrição e de cisão, e o arredondamento.
2. Abrir a consulta "ajuste de proventos" da B3 (nota 05-B).
3. Ler o [OC 004/2022-PRE](https://www.b3.com.br/data/files/F2/85/C5/72/77E6E7108BD66BD7AC094EA8/OC%20004-2022%20PRE%20Tratamento%20das%20Posi%C3%A7%C3%B5es%20de%20Op%C3%A7%C3%B5es%20em%20Eventos%20Societ%C3%A1rios%20Complexos%20(PT).pdf) (eventos societários complexos) e o [OC 014/2025-VPE](https://www.b3.com.br/data/files/B9/E7/30/16/4DA789100A29E189AC094EA8/OC%20014-2025-VPE%20ALTERACOES%20NO%20MANUAL%20DE%20PROCEDIMENTOS%20OPERACIONAIS%20DA%20CAMARA%20B3%20EVENTOS%20CORPORATIVOS%20TRATAMENTOS%20ADICIONAIS_PT.pdf) (tratamentos adicionais). Os dois foram encontrados, mas não lidos.
