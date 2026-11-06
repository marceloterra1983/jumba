#!/usr/bin/env bash
# Baixa os glossários da B3 e UM pregão de amostra, para confirmar os esquemas descritos nas notas 01-08.
# Escrito em 2026-11-04, sem ter sido executado (o proxy da sessão na nuvem bloqueia os hosts da B3).
#
# Uso: bash baixar-amostras.sh /caminho/para/raw/  [AAAA-MM-DD]
# Regras:
# - 1 requisição a cada 2 s por site;
# - cada fonte grava na sua subpasta;
# - nada baixado é executado (.ex_ é aberto como zip);
# - Python só com -I.
# Aviso: o Hub de Dados Públicos da B3 veda coleta automatizada. Rode só com o ok do Marcelo.
set -euo pipefail
RAW="${1:?informe a pasta raw/ de destino}"; RAW="${RAW%/}/"
UA="Mozilla/5.0 (X11; Linux x86_64) uso-proprio"
pausa() { sleep 2; }
baixa() { # $1 = pasta, $2 = nome do arquivo, $3 = URL
  mkdir -p "${RAW}$1/"
  curl -sS -L -m 120 -A "$UA" -o "${RAW}$1/$2" -w "%{http_code} %{size_download} $3\n" "$3" || true
  pausa
}

# 0) robots.txt
baixa robots robots_www.b3.com.br.txt https://www.b3.com.br/robots.txt
baixa robots robots_arquivos.b3.com.br.txt https://arquivos.b3.com.br/robots.txt
baixa robots robots_bvmf.txt https://bvmf.bmfbovespa.com.br/robots.txt

# 1) Glossários e layouts (PDF)
G=glossarios-pdf
baixa $G DerivativesOpenPositionFile_2023.pdf "https://b3.com.br/data/files/1E/D1/BA/58/C841B810E9C1AAA8AC094EA8/DerivativesOpenPositionFile%202023.pdf"
baixa $G DerivativesOpenPositionFile_EN.pdf "https://b3.com.br/data/files/1B/03/10/13/E40B4810A58E3348AC094EA8/DerivativesOpenPositionFile%20EN.pdf"
baixa $G Glossario_InstrumentsConsolidatedFile_2024.pdf "https://b3.com.br/data/files/52/74/1E/14/4BA6D8103152D4C8AC094EA8/Glossario%20InstrumentsConsolidatedFile%202024.pdf"
baixa $G TradeInformationConsolidatedFileV3_PT.pdf "https://www.b3.com.br/data/files/F8/42/7A/61/FEC4A8103234E0A8AC094EA8/TradeInformationConsolidatedFileV3_PT.pdf"
baixa $G HistoricalQuotations_B3.pdf "https://www.b3.com.br/data/files/65/50/AD/26/29C8B51095EE46B5790D8AA8/HistoricalQuotations_B3.pdf"
baixa $G SeriesHistoricas_Layout.pdf "https://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf"
baixa $G Glossario_Posicao_Em_Aberto_BTB.pdf "https://b3.com.br/data/files/BF/F1/58/15/391EA810E9C1AAA8AC094EA8/Glossario%20_%20Posicao_Em_Aberto.pdf"
baixa $G Catalogo-de-Mensagens-Cadastro-de-Instrumento.pdf "https://b3.com.br/data/files/D4/52/03/F5/A86B0A105BF9020AAC094EA8/Catalogo-de-Mensagens-Cadastro-de-Instrumento.pdf"
baixa $G Premio_Referencia_Opcoes_Acoes_2016.pdf "https://www.b3.com.br/data/files/10/42/D4/6B/F8EF851052122C85790D8AA8/20161214-Premio%20de%20Referencia%20para%20Opcoes%20de%20Acoes%20-%20Evento.pdf"
baixa $G Manual_Aprecamento_Opcoes_2023-12-20.pdf "https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf"

# 2) Pregão de referência: o informado ou o último útil, segundo a B3
if [[ -n "${2:-}" ]]; then D="$2"; else
  D=$(curl -sS -m 30 -A "$UA" "https://arquivos.b3.com.br/bdi/table/workday?date=$(date +%F)" | tr -d '"' | cut -c1-10); pausa
fi
AAMMDD=$(date -d "$D" +%y%m%d); DDMMAAAA=$(date -d "$D" +%d%m%Y)
echo "pregão de amostra: $D"

# 3) BDI: só a página 1 (até 1.000 linhas) de cada rota; o bastante para o esquema e o pageCount
for R in OpenPositionsEquities InstrumentsDerivatives ConsolidatedTradesDerivatives; do
  mkdir -p "${RAW}bdi-$D/"
  curl -sS -m 120 -A "$UA" -X POST -H 'Content-Type: application/json' -d '{}' \
    -o "${RAW}bdi-$D/${R}_p1.json" -w "%{http_code} %{size_download} $R\n" \
    "https://arquivos.b3.com.br/bdi/table/$R/$D/$D/1/1000" || true
  pausa
done
# HTML da página de tabelas, para ler a lista de rotas (#selectTabelas). Se for SPA, use o DevTools.
baixa "bdi-$D" tabelas.html "https://arquivos.b3.com.br/bdi/tabelas?lang=pt-BR"

# 4) Pesquisa por pregão: IN (BVBG.028) e PR (BVBG.086) do mesmo pregão
baixa "pregao-$D" "IN$AAMMDD.zip" "https://www.b3.com.br/pesquisapregao/download?filelist=IN$AAMMDD.zip"
baixa "pregao-$D" "PR$AAMMDD.zip" "https://www.b3.com.br/pesquisapregao/download?filelist=PR$AAMMDD.zip"

# 5) COTAHIST diário
baixa "cotahist-$D" "COTAHIST_D$DDMMAAAA.ZIP" "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D$DDMMAAAA.ZIP"

# 6) Resumo do esquema, sem executar nada (python -I, só leitura de JSON)
for f in "${RAW}bdi-$D/"*_p1.json; do
  python3 -I -c '
import json,sys
p=sys.argv[1]
try: t=json.load(open(p,encoding="utf-8")).get("table") or {}
except Exception as e: print(p,"ERRO",e); sys.exit()
cols=[(c.get("order"),c.get("name"),c.get("friendlyNamePt")) for c in t.get("columns") or []]
print("==",p,"pageCount=",t.get("pageCount"),"linhas_p1=",len(t.get("values") or []))
for c in sorted(cols,key=lambda x:int(x[0] or 0)): print("  ",c)
v=t.get("values") or []
print("   exemplo:",v[0] if v else None)' "$f"
done
