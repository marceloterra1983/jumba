#!/usr/bin/env bash
# Baixa os documentos e amostras citados em b3-outros/ para raw/b3/ (máquina com acesso à B3).
# NÃO foi executado na sessão de 2026-11-04 (o proxy da nuvem bloqueia b3.com.br).
# Uso: baixar-documentos.sh <pasta_raw> [AAAA-MM-DD do pregão de amostra]
# Regras: 1 requisição a cada 2 s por host; confere robots.txt antes; nada baixado é executado;
# arquivos .ex_ são ZIP autoextraíveis: abrir só com unzip/python zipfile, nunca rodar.
# Termos da B3: o Hub de Dados Públicos veda coleta automatizada; o Marcelo decidiu seguir (Etapa 2).
set -euo pipefail
RAW="${1:?pasta raw}"; DATA="${2:-}"
mkdir -p "$RAW/b3/docs" "$RAW/b3/amostras" "$RAW/anbima"
UA="Mozilla/5.0 (uso pessoal; contato: dono do Farol)"
get() {  # get <url> <destino>
  [ -s "$2" ] && { echo "já existe: $2"; return; }
  curl -sS -L -A "$UA" --max-time 120 -o "$2" "$1" || echo "FALHOU: $1"
  sha256sum "$2" >> "$RAW/b3/SHA256SUMS" 2>/dev/null || true
  sleep 2
}
get "https://www.b3.com.br/robots.txt" "$RAW/b3/robots-www.b3.com.br.txt"
get "https://arquivos.b3.com.br/robots.txt" "$RAW/b3/robots-arquivos.b3.com.br.txt"
echo "Confira os robots.txt acima antes de seguir (Ctrl-C para parar)"; sleep 5
D="$RAW/b3/docs"
while IFS='|' read -r nome url; do
  [ -z "$nome" ] && continue
  get "$url" "$D/$nome"
done <<'LIST'
mpo-camara-b3-2026-06-22.pdf|https://www.b3.com.br/data/files/57/86/30/A8/4C8D0A105BF9020AAC094EA8/MPO%20da%20Camara%20B3.pdf
manual-de-curvas-v21.pdf|https://www.b3.com.br/data/files/F3/42/AE/8C/1942B9105B12E5A9AC094EA8/Manual%20de%20Curvas_V21.pdf
manual-precificacao-eventos-corporativos-v5.pdf|https://www.b3.com.br/data/files/2C/B0/39/4D/AFA538101E311E28AC094EA8/Manual%20de%20Eventos%20Corporativos.pdf
oc-054-2025-vnc-feriados-2026.pdf|https://www.b3.com.br/data/files/C2/E3/28/AD/4FAEA9105B12E5A9AC094EA8/OC%20054-2025-VNC%20CALENDARIO%20DE%20FERIADOS%20EM%202026%20E%20FUNCIONAMENTO%20DA%20B3%20EM%2018022026%20QUARTAFEIRA%20DE%20CINZAS_PT.pdf
oc-041-2026-vnc-errata-feriados-2026.pdf|https://www.b3.com.br/data/files/20/57/01/AA/06A1F910ADC36BE9AC094EA8/OC%20041-2026-VNC%20ERRATA%20-%20CALENDARIO%20DE%20FERIADOS%20EM%202026_PT.pdf
cl-003-2026-vnc-errata-feriados-2026-en.pdf|https://www.b3.com.br/data/files/93/65/8E/25/9FE9B9109B5E99B9AC094EA8/CL%20003-2026-VNC%20ERRATA_CALENDARIO%20DE%20FERIADOS%20EM%202026%20E%20FUNCIONAMENTO%20DA%20B3%20EM%2018022026%20QUARTAFEIRA%20DE%20CINZAS_EN.pdf
oc-151-2022-pre-feriados-2023.pdf|https://www.b3.com.br/data/files/1C/F2/F3/05/42535810F534EB48AC094EA8/OC%20151-2022%20PRE%20Calendario%20de%20Feriados%20em%202023%20e%20funcionamento%20da%20B3%20em%2022.02.2023%20_Quarta-Feira%20de%20Cinzas_%20_PT_.pdf
oc-007-2026-vpc-contratos-opcoes-acoes.pdf|https://www.b3.com.br/data/files/05/A1/CA/C2/EFE2C91076A8EEB9AC094EA8/OC%20007-2026-VPC%20ALTERACOES%20CONTRATOSTERMO%20OPCOES%20ACOES%20UNITS%20ETFS%20BDRS%20FUTURO%20ACOES%20UNITS%20REPUBLICACAO%20CONTRATOS%20DERIVATIVOS%20EQUITIES.pdf
oc-006-2026-vpc-opcoes-semanais.pdf|https://www.b3.com.br/data/files/D7/A3/54/6B/45E2C91076A8EEB9AC094EA8/OC%20006-2026-VPC%20ALTERACOES%20CONTRATOS%20OPCAO%20DE%20COMPRA%20E%20VENDA%20VENCIMENTOS%20SEMANAIS%20ACAO%20UNIT%20ETF%20BDR_PT.pdf
oc-045-2025-vpc-semanais-ibovespa.pdf|https://www.b3.com.br/data/files/AC/C5/E4/D2/A4DE9910F5D34899AC094EA8/OC%20045-2025-VPC%20B3%20Novos%20Vencimentos%20das%20Op%C3%A7%C3%B5es%20Semanais%20sobre%20%C3%8Dndice%20Bovespa_PT.pdf
oc-017-2026-vpc-mini-opcoes-semanais-dolar.pdf|https://www.b3.com.br/data/files/6C/B4/07/0B/F996D910973186D9AC094EA8/OC%20017-2026-VPC%20NOVOS%20VENCIMENTOS%20DOS%20MINI%20CONTRATOS%20DE%20OPCOES%20SEMANAIS%20DE%20DOLAR_PT.pdf
oc-027-2026-vnc-mpo-negociacao-opcoes-diarias.pdf|https://www.b3.com.br/data/files/A5/06/EB/CC/1A4DD910579CDBD9AC094EA8/OC%20027-2026-VNC%20ALTERACOES%20NO%20MANUAL%20DE%20PROCEDIMENTOS%20OPERACIONAIS%20DE%20NEGOCIACAO%20DA%20B3_PT.pdf
faq-opcoes-semanais.pdf|https://www.b3.com.br/data/files/55/83/20/ED/CE98D8103152D4C8AC094EA8/B3%20Opcoes%20Semanais%20-%20Perguntas%20Frequentes.pdf
oc-055-2024-pre-contrato-di1.pdf|https://www.b3.com.br/data/files/FF/C5/51/86/158EE810C54843E8DC0D8AA8/OC%20055-2024%20PRE%20Contratos%20FE%20-%20Juros%20(PT).pdf
oc-026-2025-vpe-jcp-2026.pdf|https://www.b3.com.br/data/files/0F/23/BA/E4/1117B9105B12E5A9AC094EA8/OC%20026-2025-VPE%20ATUALIZACAO%20NA%20TRIBUTACAO%20DE%20JCP%20DE%20CONTRATOS%20FUTUROS%20E%20OPCOES%20A%20PARTIR%20DE%202026_PT.pdf
oc-006-2026-vpe-eventos-liquidos.pdf|https://b3.com.br/data/files/3D/25/CE/4A/E9EBC910F37907C9AC094EA8/OC%20006-2026-VPE%20TRATAMENTO%20DE%20EVENTOS%20CORPORATIVOS%20EM%20RECURSOS%20FINANCEIROS%20LIQUIDOS%20DE%20IMPOSTOS_PT.pdf
oc-141-2023-pre-dividendos-maiores-strike.pdf|https://www.b3.com.br/data/files/44/41/F8/1E/E90E98101D7C7D98DC0D8AA8/OC%20141-2023%20PRE%20Tratamento%20para%20Dividendos%20Superiores%20ao%20Strike_Petrobras%20(PT).pdf
oc-004-2022-pre-eventos-complexos.pdf|https://www.b3.com.br/data/files/F2/85/C5/72/77E6E7108BD66BD7AC094EA8/OC%20004-2022%20PRE%20Tratamento%20das%20Posi%C3%A7%C3%B5es%20de%20Op%C3%A7%C3%B5es%20em%20Eventos%20Societ%C3%A1rios%20Complexos%20(PT).pdf
oc-014-2025-vpe-mpo-eventos-adicionais.pdf|https://www.b3.com.br/data/files/B9/E7/30/16/4DA789100A29E189AC094EA8/OC%20014-2025-VPE%20ALTERACOES%20NO%20MANUAL%20DE%20PROCEDIMENTOS%20OPERACIONAIS%20DA%20CAMARA%20B3%20EVENTOS%20CORPORATIVOS%20TRATAMENTOS%20ADICIONAIS_PT.pdf
glossario-taxas-di-over.pdf|https://www.b3.com.br/data/files/6A/F7/3F/35/2654D9101BEEB2D9AC094EA8/Glossario_Taxas_DI_Over_balcao%204.pdf
ce-008-2025-vtec-historico-renda-fixa.pdf|https://www.b3.com.br/data/files/FA/A2/31/7C/9389A9105B12E5A9AC094EA8/CE%20008-2025-VTEC_MELHORIA%20NO%20ACESSO%20AOS%20DADOS%20HISTORICOS%20DE%20RENDA%20FIXA%20NO%20SITE%20B3_PT.pdf
glossario-emprestimos-registrados.pdf|https://b3.com.br/data/files/32/02/C0/25/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Emprestimos_Registrados.pdf
glossario-negocio-a-negocio-btb.pdf|https://b3.com.br/data/files/A6/C3/43/9D/3941B810E9C1AAA8AC094EA8/Negocio%20a%20Negocio%20-%20Emprestimos%20de%20Ativos%20-%20btb%202023.pdf
glossario-posicao-em-aberto-btb.pdf|https://b3.com.br/data/files/BF/F1/58/15/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Posicao_Em_Aberto.pdf
ce-068-2024-vnc-taxa-media-emprestimo.pdf|https://b3.com.br/data/files/83/F5/96/95/522239106EEC8429AC094EA8/CE%20068-2024-VNC%20Metodologia_taxaBTB_PT.pdf
oc-031-2026-pre-fm-opcoes-mensais.pdf|https://www.b3.com.br/data/files/9B/D2/A7/68/CA3BF91094DCD8F9AC094EA8/OC%20031-2026%20PRE%20PRORROGACAO%20PROGRAMA%20DE%20FM%20OPCOES%20SOBRE%20ACOES%20BDRS%20UNITS%20ETFS%20E%20OPCOES%20SOBRE%20%C3%8DNDICES%20COM%20VENCIMENTOS%20MENSAIS_PT.pdf
fm-opcoes-consolidado-2026-10-28.xlsx|https://www.b3.com.br/data/files/6D/D6/D0/C2/08281A10F2BF771AAC094EA8/Programa%20de%20FM%20Opcoes%20-%20Options%20MM%20Program%20-%20Out%2028%20-%202026.xlsx
fm-opcoes-mensais-parametros-2026-09-30.xlsx|https://www.b3.com.br/data/files/C3/02/30/95/252F0A105BF9020AAC094EA8/Mensal%20Parametros%20-%20Monthly%20MM%20Parameter%202026-09-30.xlsx
fm-opcoes-semanais-parametros-2026-09-04.xlsx|https://www.b3.com.br/data/files/65/E3/1E/FC/08180A105BF9020AAC094EA8/Opcao%20Semanal%20MM%20Parametros%20-%20Weekly%20Option%20Parameters%202026-09-04.xlsx
LIST
# Páginas HTML (para descobrir rotas e consultas não lidas)
get "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/opcoes/ajuste-de-proventos/" "$D/pagina-ajuste-de-proventos.html"
get "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/formador-de-mercado/series-obrigatorias-de-atuacao/" "$D/pagina-fm-series-obrigatorias.html"
get "https://arquivos.b3.com.br/bdi/tabelas?lang=pt-BR" "$D/bdi-tabelas.html"   # ler as <option> de #selectTabelas
# Amostras de 1 pregão
if [ -n "$DATA" ]; then
  A="$RAW/b3/amostras/$DATA"; mkdir -p "$A"; YMD=$(date -d "$DATA" +%y%m%d)
  get "https://www.b3.com.br/pesquisapregao/download?filelist=TS${YMD}.ex_" "$A/TS${YMD}.ex_"
  get "https://www.b3.com.br/pesquisapregao/download?filelist=PR${YMD}.zip" "$A/PR${YMD}.zip"
  curl -sS -A "$UA" -X POST -H 'Content-Type: application/json' --max-time 120 \
    -d "{\"Name\":\"ConsolidatedTradesDerivatives\",\"Date\":\"$DATA\",\"FinalDate\":\"$DATA\"}" \
    -o "$A/ConsolidatedTradesDerivatives.csv" "https://arquivos.b3.com.br/bdi/table/export/csv?lang=en-us" || true; sleep 2
  get "https://arquivos.b3.com.br/bdi/download/bdi/${DATA}/BDI_02_$(date -d "$DATA" +%Y%m%d).pdf" "$A/BDI_02.pdf"
  # Retenção: repetir TS/PR para 60, 250 e 1000 dias atrás e anotar o que volta vazio.
fi
# ANBIMA (feriados até 2078; conferência)
get "https://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls" "$RAW/anbima/feriados_nacionais.xls"
echo "Fim. Para abrir o TS: python3 -I -c 'import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])' <arquivo.ex_> <pasta_nova>"
