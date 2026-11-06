"""Calcula vencimentos 2026-2028 a partir do JSON de feriados gerado por nós. Saída: tabela markdown."""
import json, sys
from datetime import date, timedelta
cal = json.load(open(sys.argv[1], encoding="utf-8"))
sem = set(); duanb_excl = set()
for y,v in cal["anos"].items():
    for x in v["sem_pregao"]:
        d = date.fromisoformat(x["data"]); sem.add(d)
        if not x["dia_util_anbima"]: duanb_excl.add(d)
def sessao(d): return d.weekday()<5 and d not in sem
def dia_util(d): return d.weekday()<5 and d not in duanb_excl
def ant(d):
    while not sessao(d): d -= timedelta(1)
    return d
def prox(d):
    while not sessao(d): d += timedelta(1)
    return d
def nth_weekday(y,m,wd,n):
    d = date(y,m,1)
    while d.weekday()!=wd: d += timedelta(1)
    return d + timedelta(7*(n-1))
DSA = ["seg","ter","qua","qui","sex","sáb","dom"]
def f(d, base=None):
    s = d.strftime("%d/%m/%Y") + " (" + DSA[d.weekday()] + ")"
    if base and base!=d: s += " *"
    return s
rows=[]; ajustes=[]
for y in (2026,2027,2028):
    for m in range(1,13):
        b_acao = nth_weekday(y,m,4,3); v_acao = ant(b_acao)
        b_ibov = next(date(y,m,dd) for dd in range(12,19) if date(y,m,dd).weekday()==2); v_ibov = prox(b_ibov)
        d = date(y,m,1)
        while not dia_util(d): d += timedelta(1)
        v_dol = d
        d = date(y,m,1)
        while not sessao(d): d += timedelta(1)
        v_di1 = d
        # semanais de ações no mês: sextas exceto a 3a
        sem_acao=[]; k=1; dd=nth_weekday(y,m,4,1)
        while dd.month==m:
            if k!=3: sem_acao.append(("W%d"%k, ant(dd), dd))
            k+=1; dd+=timedelta(7)
        rows.append((y,m,b_acao,v_acao,b_ibov,v_ibov,v_dol,v_di1,sem_acao))
        for lab,b,v in (("ações mensal",b_acao,v_acao),("IBOV mensal",b_ibov,v_ibov)):
            if b!=v: ajustes.append(f"{lab} {m:02d}/{y}: regra cai em {f(b)}, sem pregão → {f(v)}")
        for w,v,b in sem_acao:
            if v!=b: ajustes.append(f"semanal ações {w} {m:02d}/{y}: {f(b)} sem pregão → {f(v)}")
        if not sessao(v_dol): ajustes.append(f"DOL {m:02d}/{y}: 1º dia útil {f(v_dol)} não tem pregão (conferir regra)")
print("| Mês | Opções de ações (mensal) | Opções de IBOV (mensal) | Opções de DOL | DI1 / WDO/DOL futuro [S] |")
print("|---|---|---|---|---|")
for y,m,ba,va,bi,vi,vd,vdi,sa in rows:
    print(f"| {m:02d}/{y} | {f(va,ba)} | {f(vi,bi)} | {f(vd)} | {f(vdi)} |")
print()
print("Ajustes por feriado:")
for a in ajustes: print("- "+a)
print()
print("Semanais de ações (sextas, sem a 3ª), contagem por ano:")
for y in (2026,2027,2028):
    n=sum(len(r[8]) for r in rows if r[0]==y); print(y,n)
