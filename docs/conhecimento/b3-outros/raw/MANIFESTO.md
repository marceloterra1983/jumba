# Manifesto de raw/ (b3-outros)

Data de acesso de tudo: **2026-11-04**. O conteúdo é de terceiros e não é confiável. **Nada daqui foi executado.**

## Bloqueio de rede

O proxy desta sessão na nuvem recusa (`CONNECT 403`) estes hosts:

- `www.b3.com.br`, `sistemaswebb3-listados.b3.com.br`, `www2.bmf.com.br`;
- `www.anbima.com.br`, `dados.cvm.gov.br`, `www.tesourotransparente.gov.br`;
- `www.bcb.gov.br`, `api.bcb.gov.br`.

Foi uma tentativa por host, sem repetir. Consequências:

- **nenhum PDF, XLSX ou CSV da B3, ANBIMA ou CVM foi salvo como binário**;
- os documentos foram **lidos pelo WebFetch**, que devolve um texto já processado por um modelo, não o original. Os resumos estão em `webfetch/`, um por documento, com URL e data no cabeçalho. **Confira nomes de campos e fórmulas no original antes de codificar;**
- o WebFetch não lê `.xlsx` e só converte cerca de 99 mil caracteres de cada PDF. O MPO da Câmara ficou truncado antes da seção 7.9.1;
- para baixar os originais numa máquina com acesso, use `../scripts/baixar-documentos.sh <raw/> [AAAA-MM-DD]`. O script não foi executado e não executa nada do que baixa.

**robots.txt:** `https://www.b3.com.br/robots.txt` deu erro de cliente no WebFetch e não pôde ser lido. A sessão irmã também não conseguiu ler os da B3. Ritmo usado: uma requisição por vez por host, com mais de 2 s entre elas.

**Termos da B3:** o Hub de Dados Públicos e a página de dividendos dizem que os dados são "de propriedade exclusiva da B3" e que "é expressamente vedada a coleta automatizada, inclusive por meio de ferramentas de inteligência artificial". Nesta coleta só se leu documentação pública, sem baixar dados de pregão. O Marcelo já decidiu seguir com o scraper da B3 (Etapa 2).

## Baixado de verdade (host liberado)

| Pasta | Origem | Licença | Para quê |
|---|---|---|---|
| `exchange-calendars-4.13.2/` | sdist do PyPI: https://files.pythonhosted.org/packages/47/73/460b0ece4e7444e3098b7738974c822787e134578d069d3a88b4be17d50a/exchange_calendars-4.13.2.tar.gz (sha256 `a9459425dd64142cd54fbc639847403c7e0c33d60fbc326c94fc1d6bd127f002`). Extraídos só `LICENSE` e `exchange_calendar_bvmf.py` | Apache-2.0 | Conferência independente das regras de feriado da B3 |

Também usado, sem copiar, o código do rb3, filings-b3 e b3-open-data já baixado pela sessão irmã em `../../b3-opcoes/raw/`.

## Lidos pelo WebFetch (resumos em `webfetch/`)

- `webfetch/anbima-ettj-cz.txt`
- `webfetch/anbima-feriados-nacionais-2026-2028.txt`
- `webfetch/ativa-contratos-em-aberto-20230214.txt`
- `webfetch/b3-faq-opcoes-semanais.txt`
- `webfetch/b3-fm-programas-listados-opcoes.txt`
- `webfetch/b3-hub-dados-publicos.txt`
- `webfetch/b3-manual-aprecamento-pagina.txt`
- `webfetch/b3-noticia-calendario-2026.txt`
- `webfetch/b3-pagina-dividendos-eventos.txt`
- `webfetch/b3-produto-di1.txt`
- `webfetch/b3-produto-opcoes-dolar.txt`
- `webfetch/b3-produto-opcoes-ibovespa.txt`
- `webfetch/b3-produto-opcoes-semanais-ibovespa.txt`
- `webfetch/bdi-02-20240321-participacao-investidores.txt`
- `webfetch/ce-008-2025-vtec-historico-renda-fixa.txt`
- `webfetch/ce-068-2024-vnc-taxa-media-emprestimo.txt`
- `webfetch/glossario-emprestimos-registrados.txt`
- `webfetch/glossario-negocio-a-negocio-btb.txt`
- `webfetch/glossario-taxas-di-over-balcao.txt`
- `webfetch/manual-de-curvas-v21.txt`
- `webfetch/manual-precificacao-eventos-corporativos-v5.txt`
- `webfetch/mpo-camara-b3-2026-06-22-indice.txt`
- `webfetch/oc-006-2026-vpc-opcoes-semanais.txt`
- `webfetch/oc-006-2026-vpe-eventos-liquidos-impostos.txt`
- `webfetch/oc-007-2026-vpc-contratos-opcoes-acoes.txt`
- `webfetch/oc-009-2025-vpc-fm-opcoes-credenciamento.txt`
- `webfetch/oc-017-2026-vpc-mini-opcoes-semanais-dolar.txt`
- `webfetch/oc-026-2025-vpe-jcp-2026.txt`
- `webfetch/oc-031-2026-pre-fm-opcoes-mensais.txt`
- `webfetch/oc-045-2025-vpc-semanais-ibovespa.txt`
- `webfetch/oc-054-2025-vnc-feriados-2026.txt`
- `webfetch/oc-055-2024-pre-contrato-di1.txt`
- `webfetch/oc-141-2023-pre-dividendos-maiores-que-strike.txt`
- `webfetch/oc-151-2022-pre-feriados-2023.txt`
- `webfetch/oc-166-2023-pre-feriados-2024.txt`

## Tentados sem sucesso (erro de cliente no site)

- `https://www.b3.com.br/robots.txt`
- OC 041/2026-VNC (errata do calendário de 2026), com espaços e com `%20`
- `https://borainvestir.b3.com.br/...vencimento-semanal-na-segunda-feira` e `.../opcoes-semanais-de-ibovespa-passam-a-ter-vencimentos-diarios/`
- `https://www.b3.com.br/pt_br/noticias/opcoes-semanais-de-ibovespa-passam-a-ter-vencimentos-em-todos-os-dias-do-mes.htm`
- Página "Taxas Referenciais BM&FBOVESPA" (destino do redirect de www2.bmf.com.br)
- `.../consultas/mercado-a-vista/opcoes/ajuste-de-proventos/` (URL suposta)
- CE 068/2024-VNC e OC 006/2026-VPE com host `www` (abriram com `b3.com.br`)
- `https://okai.com.br/documento/2026-06-30/041-2026-vnc-...`
- `https://arquivos.b3.com.br/bdi/download/bdi/2024-03-21/BDI_03_20240321.pdf` (URL suposta)
- Planilha consolidada de FM de opções (.xlsx): o WebFetch devolve "[binary data]"
- `https://teses.usp.br/teses/disponiveis/12/12139/tde-03042024-160952` (só redirecionamento)
