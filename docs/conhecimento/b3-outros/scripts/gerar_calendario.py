"""Gera feriados-b3-2026-2028.json e tabela de vencimentos. Não lê nenhum arquivo baixado."""
import json, sys, datetime as dt
from datetime import date, timedelta

DS = ["segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado","domingo"]

def pascoa(y):
    a=y%19;b=y//100;c=y%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3;h=(19*a+b-d-g+15)%30
    i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7;m=(a+11*h+22*l)//451
    mes=(h+l-7*m+114)//31;dia=((h+l-7*m+114)%31)+1
    return date(y,mes,dia)

F_B3_2026 = "https://www.b3.com.br/pt_br/noticias/calendario-de-negociacao-da-b3-confira-o-funcionamento-da-bolsa-em-2026.htm"
F_OC054 = "https://www.b3.com.br/data/files/C2/E3/28/AD/4FAEA9105B12E5A9AC094EA8/OC 054-2025-VNC CALENDARIO DE FERIADOS EM 2026 E FUNCIONAMENTO DA B3 EM 18022026 QUARTAFEIRA DE CINZAS_PT.pdf"
F_ANB = "https://www.anbima.com.br/feriados/fer_nacionais/{y}.asp"
F_OC151 = "https://www.b3.com.br/data/files/1C/F2/F3/05/42535810F534EB48AC094EA8/OC%20151-2022%20PRE%20Calendario%20de%20Feriados%20em%202023%20e%20funcionamento%20da%20B3%20em%2022.02.2023%20_Quarta-Feira%20de%20Cinzas_%20_PT_.pdf"

def feriados_ano(y):
    p = pascoa(y)
    nac = [
        (date(y,1,1),"Confraternização Universal","nacional"),
        (p-timedelta(48),"Carnaval (segunda-feira)","ponto facultativo / feriado ANBIMA"),
        (p-timedelta(47),"Carnaval (terça-feira)","ponto facultativo / feriado ANBIMA"),
        (p-timedelta(2),"Sexta-feira Santa (Paixão de Cristo)","nacional"),
        (date(y,4,21),"Tiradentes","nacional"),
        (date(y,5,1),"Dia do Trabalho","nacional"),
        (p+timedelta(60),"Corpus Christi","ponto facultativo / feriado ANBIMA"),
        (date(y,9,7),"Independência do Brasil","nacional"),
        (date(y,10,12),"Nossa Senhora Aparecida","nacional"),
        (date(y,11,2),"Finados","nacional"),
        (date(y,11,15),"Proclamação da República","nacional"),
        (date(y,11,20),"Dia Nacional de Zumbi e da Consciência Negra","nacional (Lei 14.759/2023)"),
        (date(y,12,25),"Natal","nacional"),
    ]
    b3_extra = [(date(y,12,24),"Véspera de Natal (sem sessão; expediente interno bancário)","B3")]
    d31 = date(y,12,31)
    if d31.weekday()==5: d31 = d31-timedelta(1)
    elif d31.weekday()==6: d31 = d31-timedelta(2)
    nome31 = "Último dia útil do ano (sem sessão; expediente interno bancário)" if d31.day!=31 else "Véspera de Ano Novo (sem sessão; expediente interno bancário)"
    b3_extra.append((d31,nome31,"B3"))
    return nac, b3_extra, p

def gerar():
    out = {
      "titulo": "Feriados e dias sem pregão da B3, 2026 a 2028",
      "acesso": "2026-11-04",
      "pasta": "/mnt/project-files/jumba/conhecimento/b3-outros/",
      "legenda_status": {
        "oficial": "confirmado em publicação da B3 para o ano",
        "derivado": "B3 ainda não publicou o calendário do ano; datas calculadas pelas regras abaixo e conferidas com a lista de feriados nacionais da ANBIMA. Conferir quando a B3 publicar o ofício (costuma sair em dezembro do ano anterior)."
      },
      "regras": [
        "Sem pregão nos feriados nacionais, no Carnaval (segunda e terça), na Sexta-feira Santa e em Corpus Christi (OC 054/2025-VNC; notícia B3 de 09/01/2026).",
        "Sem pregão em 24/12 e 31/12 (expediente interno bancário). Se 31/12 cair em fim de semana, a B3 fecha no último dia útil do ano (29/12/2023, OC 151/2022-PRE). Se 24/12 cair em fim de semana, não há compensação (2023).",
        "Feriados municipais/estadual de São Paulo (25/01 e 09/07): a B3 funciona normalmente desde o calendário de 2022 (OC 054/2025-VNC; OC 166/2023-PRE).",
        "Quarta-feira de Cinzas: dia de pregão com abertura às 13h (pré-abertura 12h45 em renda variável; 12h55 em derivativos).",
        "Feriados dos EUA não fecham a B3; afetam câmbio, CSD2 e liquidação de derivativos agro.",
        "Contagem de dias úteis (DU/252) da curva DI e do DI1: calendário de feriados da ANBIMA (Manual de Curvas da B3). 24/12 e 31/12 são dias úteis ANBIMA, mas sem pregão; por isso cada data traz os dois indicadores."
      ],
      "fontes": [F_B3_2026, F_OC054, F_OC151, F_ANB.format(y=2026), F_ANB.format(y=2027), F_ANB.format(y=2028),
                 "https://www.b3.com.br/data/files/92/94/5A/0A/80E3B810DDBC40B8DC0D8AA8/OC%20166-2023%20PRE%20Calend%C3%A1rio%20de%20Feriados%202024%20e%20Funcionamento%20da%20B3%20em%2014.02.2024%20(Quarta-Feira%20de%20Cinzas)%20(PT).pdf"],
      "pendencias": [
        "OC 041/2026-VNC (Errata do calendário de feriados de 2026, de 30/06/2026) não pôde ser lido (erro do site). A notícia da B3 de 09/01/2026 confere com a lista abaixo; a errata pode mudar algo do 2º semestre de 2026.",
        "OC 003/2026-VNC (que revogou o OC 054/2025-VNC) não foi lido; a versão em inglês CL 003-2026 indica errata do mesmo calendário."
      ],
      "anos": {}
    }
    oficial_2026 = {date(2026,1,1),date(2026,2,16),date(2026,2,17),date(2026,4,3),date(2026,4,21),date(2026,5,1),
                    date(2026,6,4),date(2026,9,7),date(2026,10,12),date(2026,11,2),date(2026,11,20),date(2026,12,24),
                    date(2026,12,25),date(2026,12,31)}
    for y in (2026,2027,2028):
        nac, extra, p = feriados_ano(y)
        status = "oficial" if y==2026 else "derivado"
        sem, fds = [], []
        for d,nome,tipo in nac+extra:
            item = {"data": d.isoformat(), "dia_semana": DS[d.weekday()], "nome": nome, "tipo": tipo,
                    "sem_pregao_b3": d.weekday()<5, "dia_util_anbima": tipo=="B3",
                    "status": status}
            if d.weekday()>=5:
                item["sem_pregao_b3"] = False
                item["obs"] = "cai em fim de semana"
                fds.append(item)
            else:
                sem.append(item)
        sem.sort(key=lambda x:x["data"]); fds.sort(key=lambda x:x["data"])
        if y==2026:
            got = {date.fromisoformat(x["data"]) for x in sem}
            assert got==oficial_2026, (got ^ oficial_2026)
        cinzas = p-timedelta(46)
        out["anos"][str(y)] = {
          "status": status,
          "pascoa": p.isoformat(),
          "sem_pregao": sem,
          "feriados_em_fim_de_semana": fds,
          "pregao_normal_em_feriado_de_sp": [ {"data": date(y,1,25).isoformat(), "dia_semana": DS[date(y,1,25).weekday()], "nome": "Aniversário da cidade de São Paulo"},
                                               {"data": date(y,7,9).isoformat(), "dia_semana": DS[date(y,7,9).weekday()], "nome": "Revolução Constitucionalista (SP)"} ],
          "horario_especial": [ {"data": cinzas.isoformat(), "dia_semana": DS[cinzas.weekday()], "nome": "Quarta-feira de Cinzas", "abertura": "13:00", "status": status} ],
          "n_sessoes_b3": None
        }
        # contar sessões
        n=0; d=date(y,1,1); semset={date.fromisoformat(x["data"]) for x in sem}
        while d.year==y:
            if d.weekday()<5 and d not in semset: n+=1
            d+=timedelta(1)
        out["anos"][str(y)]["n_sessoes_b3"]=n
        # DU ANBIMA
        anb={date.fromisoformat(x["data"]) for x in sem if not x["dia_util_anbima"]}
        n2=0; d=date(y,1,1)
        while d.year==y:
            if d.weekday()<5 and d not in anb: n2+=1
            d+=timedelta(1)
        out["anos"][str(y)]["n_dias_uteis_anbima"]=n2
    return out

if __name__=="__main__":
    o = gerar()
    json.dump(o, open(sys.argv[1],"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    for y,v in o["anos"].items():
        print(y, v["status"], "sessões", v["n_sessoes_b3"], "DU anbima", v["n_dias_uteis_anbima"])
        for x in v["sem_pregao"]: print("  ", x["data"], x["dia_semana"], x["nome"], "DUanbima" if x["dia_util_anbima"] else "")
