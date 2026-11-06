# Verificação independente dos vetores de precificação

- **Alvo:** `precificacao.json` e `precificacao.md` (nesta pasta), versão 1, gerados em 2026-11-04.
- **Data da verificação:** 2026-11-04.
- **Veredito:** **APROVADO COM RESSALVAS**. Nenhum valor numérico testável está errado. As ressalvas são de tolerância, de texto e de cobertura (§4 e §5).
- **Como verifiquei:** reimplementei tudo do zero em `/tmp/verifica-precificacao/verifica.py`: Python, só biblioteca padrão, N(x) = erfc(−x/√2)/2 via `math.erfc`, contas em double. Não usei nada de `geradores/`, de `conhecimento/jumba-publico/` nem de `vetores/retido/`.
- **Como rodar de novo:**
  `python3 -I /tmp/verifica-precificacao/verifica.py <precificacao.json> <feriados-b3-2026-2028.json> <saida.json>`
  Checagens extras: `extras.py` (tolerâncias, GK × Black-76), `confere_md.py` (tabelas do .md × JSON) e `gera_correcoes.py`, todos na mesma pasta.
- **Correções propostas:** `correcoes-precificacao.json` (nesta pasta). O JSON original não foi alterado.

## 1. O que foi conferido

| Item | Quantidade | Resultado |
|---|---|---|
| Casos recalculados | **82 de 82**: 44 de preço e gregas, 29 de vol implícita (20 com solução, 9 que devem falhar), 9 de taxa | as contagens batem com o .md |
| Comparações de campo | 1.126: 694 saídas numéricas, 67 campos lógicos (`falha`, `flags`, `sigma = null`) e 365 de `entradas_gbs` (S, K, T, r, b) | **0 fora da tolerância gravada** |
| Valores publicados (Hull 9ª ed., Haug 2ª ed.) | 29 | os 29 batem dentro de meia unidade da última casa (§2) |
| Checagens internas | 412: gregas por diferença finita, EDP Θ + ½σ²S²Γ + bSΔ − rV = 0, paridade c − p, tolerância de σ, repreço no σ, preço no `sigma_origem` | todas passam |
| Tabelas do .md × JSON | 365 valores | todos batem com o JSON |
| Calendário `feriados-b3-2026-2028.json` | dia da semana de cada data, Páscoa e totais por ano | tudo confere (§4.6) |

### 1.1 Como cada parte foi recalculada

- **Conversões B3:** T = DU/252; r = ln(1 + DI) por `log1p`; GK com q = (252/DU)·ln(1 + cupom·DC/360); Black-76 com b = 0 e S → F. Elas reproduzem `entradas_gbs` com erro relativo ≤ 1,7·10⁻¹⁶.
- **Gregas:** derivei as fórmulas do GBS de novo, com o rho que cada modelo pede: BSM com q fixo, Black-76 = −T·V com F fixo, GK = ∂V/∂r_d. Conferi cada uma contra diferença central (gamma com Richardson); o erro relativo ficou abaixo de 10⁻⁵ em todos os casos.
- **Vol implícita:** os limites saem em `Decimal` a partir dos doubles exatos. A inversão é por bissecção até o ulp, sempre pela opção fora do dinheiro, com a paridade em `Decimal`. Assim a cancelação dos casos muito dentro do dinheiro não contamina o σ.
- **Taxas:** fator e taxa diária por `log1p` e `expm1`; interpolação flat forward 252 pela média linear de ln(fator) entre os vértices.

### 1.2 Maior diferença relativa por grupo de campos (todas dentro da tolerância)

| Campo | Maior dif. relativa | Caso |
|---|---|---|
| preço, d1, d2, delta, gamma, vega, theta, rho, rho_q, rho_pp, rho_di_pp, theta_du, theta_dc | ≤ 9,0·10⁻¹⁵ | vários |
| `theta_1du_exato` (diferença de dois preços, logo com cancelação) | 1,25·10⁻¹² | B3-ACAO-126DU-K26-P |
| `sigma` (bem condicionado) | ≤ 2,6·10⁻¹⁵ em valor absoluto | IV-1DU-OTM-P-TICK |
| `sigma` (mal condicionado) | 7,2·10⁻¹¹ abs (tol. 1e-6) | IV-ITM-C-EXTREMO |
| `vega_em_sigma` | 9,4·10⁻⁹ rel (8,9·10⁻¹⁵ abs; tol. 1e-10 abs) | IV-ITM-C-EXTREMO |
| taxas (`r`, `fator_*`, `i_d`, `taxa_aa`, `q`) | ≤ 3,8·10⁻¹⁶ | TX-DI-INTERP-50DU |

**Por que o σ de IV-ITM-C-EXTREMO difere em 7,2·10⁻¹¹:** o gerador usou as entradas como decimais exatos (r = 0,1) e não como o double de 0,1. Refazendo com r = Decimal('0.1'), a diferença cai para 3·10⁻¹⁶. Isso é irrelevante diante da tolerância de 1e-6, mas o .md (§2.4) só diz que o preço é o double exato. Ele poderia dizer também que S, K, T e r foram tratados como decimais.

## 2. Exemplos de livro

Os livros impressos não estão disponíveis aqui. A conferência tem duas partes:

- **(a)** o valor recalculado arredonda para o valor citado;
- **(b)** os parâmetros e o valor citado coincidem com os exemplos clássicos, como eu os conheço [I, não reconferido no impresso].

| Caso | Campo | Publicado | Recalculado | Diferença | Meia casa |
|---|---|---|---|---|---|
| HULL-BSM-EX15.6-C | preço; d1; d2 | 4,76; 0,7693; 0,6278 | 4,759422; 0,769263; 0,627841 | 5,8e-4; 3,7e-5; 4,1e-5 | 5e-3; 5e-5; 5e-5 |
| HULL-BSM-EX15.6-P | preço | 0,81 | 0,808599 | 1,4e-3 | 5e-3 |
| HULL-GREGAS-CAP19-C | preço; d1; Δ; Γ; ν | 2,40; 0,0542; 0,522; 0,066; 12,1 | 2,400527; 0,054181; 0,521605; 0,065544; 12,10548 | ≤ 5,5e-3 | 5e-3 a 5e-2 |
| HULL-GREGAS-CAP19-C | Θ/ano; Θ/365; Θ/252; ρ | −4,31; −0,0118; −0,0171; 8,91 | −4,305330; −0,011795; −0,017085; 8,906962 | 4,7e-3; 4,6e-6; 1,5e-5; 3,0e-3 | 5e-3; 5e-5; 5e-5; 5e-3 |
| HULL-INDICE-EX17.1-C | preço | 51,83 | 51,832957 | 3,0e-3 | 5e-3 |
| HULL-FUTURO-CAP18-P | preço | 1,12 | 1,116641 | 3,4e-3 | 5e-3 |
| IV-HULL-15.11 | σ | 0,235 | 0,2345129 | 4,9e-4 | 5e-4 |
| HAUG-BS-C | preço | 2,1334 | 2,1333684 | 3,2e-5 | 5e-5 |
| HAUG-MERTON-P | preço | 2,4648 | 2,4647876 | 1,2e-5 | 5e-5 |
| HAUG-BLACK76-C e -P | preço | 1,7011 | 1,7010507 | 4,9e-5 | 5e-5 |
| HAUG-GK-C | preço | 0,0291 | 0,0290993 | 7,5e-7 | 5e-5 |
| HAUG-DELTA-B76-C; -P | Δ | 0,5946; −0,3566 | 0,5946287; −0,3566008 | 2,9e-5; 7,7e-7 | 5e-5 |
| HAUG-GAMMA-VEGA-C e -P | Γ; ν | 0,0278; 18,9358 | 0,0278212; 18,9357774 | 2,1e-5; 2,3e-5 | 5e-5 |
| HAUG-THETA-P | Θ/ano | −31,1924 | −31,1923671 | 3,3e-5 | 5e-5 |
| HAUG-RHO-C | ρ | 38,7325 | 38,7325050 | 5,0e-6 | 5e-5 |

Notas da tabela:

- Também conferem as frases citadas em notas: Hull, σ = 0,20 → 1,76 e σ = 0,30 → 2,10 (recalculado: 1,7647 e 2,1010); Θ por dia corrido (/365) e por dia de negociação (/252) do cap. 19.
- **Margens apertadas:** em HAUG-BLACK76 e IV-HULL-15.11 a folga até a meia casa é pequena (1e-6 e 1e-5). Mesmo assim, o valor exato arredonda corretamente para o publicado.

## 3. Divergências

**Numéricas: nenhuma.** Nenhum campo de `saidas_esperadas`, `entradas_gbs`, limite de arbitragem ou tolerância de σ ficou fora da regra `|obtido − esperado| ≤ max(abs, rel·|esperado|)`. Para registro, as seis maiores diferenças:

| id | campo | esperado | recalculado | dif. relativa | limite usado |
|---|---|---|---|---|---|
| IV-ITM-C-EXTREMO | vega_em_sigma | 9,455730716e-07 | 9,455730627e-07 | 9,4e-09 | 1e-10 abs |
| IV-ITM-P-B3-EXTREMO | vega_em_sigma | 5,540965091e-06 | 5,540965089e-06 | 3,9e-10 | 1e-10 abs |
| IV-ITM-C-EXTREMO | sigma | 0,2499999962812 | 0,2499999962096 | 2,9e-10 | 1e-6 abs |
| IV-ITM-P-B3-EXTREMO | sigma | 0,3500000000578 | 0,3500000000526 | 1,5e-11 | 1e-7 abs |
| B3-ACAO-126DU-K26-P | theta_1du_exato | 1,010237016094e-03 | 1,010237016093e-03 | 1,3e-12 | 1e-10 abs |
| B3-DOL-GK-20DU-P | theta_1du_exato | −1,255754635328e-03 | −1,255754635329e-03 | 7,7e-13 | 1e-10 abs |

**De texto, no campo `nota`, que não é testado.** Elas estão em `correcoes-precificacao.json`.

| id | Texto atual | Correto | Base |
|---|---|---|---|
| IV-FALHA-C-ABAIXO-INTRINSECO | S − K·e^{−rT} = 2,3224 | 2,3222 | `limite_inferior` = 2,3222130 |
| IV-FALHA-C-ENTRE-INTRINSECO-E-LIMITE | 2,3224 | 2,3222 | idem |
| IV-1DU-ITM-C-PERTO-LIMITE | valor-tempo ~0,005 acima de 1,0154 | ~0,004 acima de 1,0160 | `limite_inferior` = 1,0159792 |
| IV-FALHA-1DU-ABAIXO-LIMITE | limite 1,0154 | 1,0160 | idem |
| IV-FALHA-B76-ABAIXO-LIMITE | 4.969,9 | 4.969,97 (truncado no texto) | 4.969,9709 |
| HAUG-BS-P | "Call de 3 meses…" | descrever como put calculada | nota do par copiada |
| HAUG-MERTON-C | "Put de 6 meses…" | descrever como call calculada | nota do par copiada |

Fora do escopo, mas achado no caminho: a nota `../conhecimento/metodologia/05-gregas-escalas.md` §3 diz r = ln 1,1065 = 0,101203, mas o valor é 0,1012019 (arredonda para 0,101202). A especificação do motor (linha 176) usa r = 0,101203 como entrada de um vetor de charm e vanna. Os vetores de `precificacao.json` usam o valor certo, 0,10120188050896729.

## 4. Convenções conferidas e questionáveis

### 4.1 Unidades das gregas: corretas e coerentes

- Delta é por unidade do objeto. Gamma é cru (1/R$; no Black-76, por F).
- Vega e rho são por 1,00; `vega_pp` e `rho_pp` são por 1 p.p.
- Bate com Hull (ν = 12,1 e ρ = 8,91 por 1,00), Haug (ν = 18,9358 e ρ = 38,7325), a nota 05 e a especificação §2.3.
- `rho_di_pp` = ρ/[100(1 + DI)] está certo, porque dr/dDI = 1/(1 + DI).

### 4.2 Theta por ano e por dia

- Θ = −∂V/∂T por ano, com o sinal de Hull e Haug. `theta_du` = Θ/252 e `theta_dc` = Θ/365.
- **Questionável:** nos 18 casos B3 que trazem `theta_dc`, ele divide por 365 um Θ cuja base de tempo é o ano de 252 DU. O resultado não é um theta por dia corrido. O próprio .md admite isso (§2.3).
  - Recomendo não exibir `theta_dc` na convenção B3, ou rotulá-lo como "Θ/365 (sem significado de calendário)".
  - O theta útil na B3 é `theta_du` ou `theta_1du_exato`.

### 4.3 `theta_1du_exato`

- Ele mantém fixos r e q contínuos e σ. No GK, o q vem de DC/360 e, na vida real, 1 DU consome 1 a 3 dias corridos, o que muda o forward.
- É uma convenção [P] documentada, não um erro. Basta não comparar esse campo com um "theta de 1 dia" que recalcule o cupom.

### 4.4 Rho por modelo

- As fórmulas conferem por diferença finita.
- No par B3-DOL-B76-EQUIV, o rho (F fixo) não é comparável com o rho do GK. O .md avisa.

### 4.5 Sinal de GEX e DEX

- **Não se aplica a este arquivo:** não há nenhum campo GEX/DEX nem saída de `escala()`.
- O que dá para conferir aqui é que o par GK × Black-76 sustenta a GEX U3 em qualquer base, desde que o motor não misture as bases:
  - S²·Γ_S = F²·Γ_F = 51,348987 (diferença relativa 4·10⁻¹⁶);
  - Δ_S·S = Δ_F·F (1,9731705 na call);
  - Γ_S/Γ_F = e^{2bT}.
- **Cuidado no motor:** usar Γ em F com S² (ou Γ em S com F²) erra a GEX em 0,8 % neste caso. Esse erro é de tamanho, não de sinal.
- O sinal s_i é responsabilidade da nota 08 e de `agregados.json`, fora deste escopo.

### 4.6 Dias úteis e feriados

- Os vetores recebem DU (e DC) prontos. **Nenhum caso testa a contagem a partir de datas**, então o arquivo de feriados não é exercitado.
- Conferi o próprio arquivo:
  - dia da semana de todas as datas;
  - Páscoa de 2026 a 2028 (05/04, 28/03, 16/04), por Meeus;
  - totais: 247, 249 e 247 pregões; 249, 251 e 248 DU ANBIMA. Batem com o arquivo.
- **Questionável:** existem dois calendários. A curva DI usa DU ANBIMA, em que 24/12 e 31/12 são dias úteis. Os pregões excluem esses dias. Por exemplo, de 2026-12-01 a 2027-01-15 há 29 pregões, 31 DU ANBIMA e 45 DC.
- Os vetores usam um único DU para o tempo da vol e para o desconto. O motor precisa decidir qual DU entra em cada lugar, e falta vetor para `prazo()`.
- Os pares DU/DC dos casos (por exemplo, 20/28) são sintéticos e não correspondem a datas.

### 4.7 Flat forward 252: correto

- Os 4 casos TX-DI-INTERP batem com erro ≤ 4·10⁻¹⁶. No vértice, a função devolve a própria taxa.
- O cupom confere: e^{−qT} = 1/(1 + c·DC/360).

### 4.8 Tolerância de `vega_em_sigma`

- Em 9 dos 20 casos de vol com solução, |vomma|·tol_σ passa da tolerância de 1e-10 da vega. Exemplos: IV-OTM-C-PROFUNDO (1,8·10⁻⁹) e IV-ITM-C-MODERADO (1,4·10⁻⁹).
- Um motor com σ dentro da tolerância, mas na borda, reprova na vega se ela for avaliada no σ do próprio motor.
- Proposta: dar uma tolerância própria por caso, ou avaliar a vega no σ esperado.

### 4.9 Critério de parada da nota 06 × tolerância de σ

- A parada |f| < 1e-10·max(1, P) permite um erro de σ de até 1e-10·max(1, P)/ν.
- Isso é maior que a tolerância gravada em 12 dos 20 casos, por exemplo:
  - IV-OTM-C-EXTREMO: 1,1·10⁻⁷ contra 1e-10;
  - IV-ITM-C-EXTREMO: 5,4·10⁻³ contra 1e-6.
- Um motor que siga a nota 06 à risca pode reprovar sem ter bug. É preciso apertar o critério no motor (por exemplo, um passo extra de Newton ou |Δσ| < 1e-13) ou alinhar a nota com os vetores.

## 5. Veredito

**APROVADO COM RESSALVAS.**

- Os 82 casos estão numericamente corretos: preços, gregas, limites, vol implícita, taxas e conversões B3.
- Os 29 valores publicados conferem.
- As convenções de unidade, theta, rho e flat forward 252 estão certas e documentadas.

Ressalvas, nenhuma muda um valor esperado:

1. Ajustar as tolerâncias de `vega_em_sigma` (§4.8) e alinhar o critério de parada da nota 06 com a tolerância de σ (§4.9).
2. Corrigir 7 textos de `nota` (§3).
3. Tratar `theta_dc` na convenção B3 como escala sem significado de calendário (§4.2).
4. Criar vetores de `prazo()` com o calendário de feriados, separando DU de pregão e DU ANBIMA (§4.6).
5. Criar vetores de GEX/DEX e de `escala()`, que este arquivo não cobre (§4.5).
