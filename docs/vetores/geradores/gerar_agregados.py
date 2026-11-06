#!/usr/bin/env python3
"""Gerador de vetores de teste: agregados de OI, exposições, níveis e estruturas.

Uso:
    python3 -I gerar_agregados.py [--saida DIR] [--feriados-json ARQ]

- Só biblioteca padrão. Não acessa a rede. Não executa nada baixado.
- Todos os dados de entrada são SINTÉTICOS e estão escritos neste arquivo.
- O único arquivo externo lido (opcional) é o JSON de feriados gerado por outro
  script do projeto (conhecimento/b3-outros/feriados-b3-2026-2028.json), usado só
  para conferência independente do calendário.
- Saídas: DIR/agregados.json e DIR/agregados.md (DIR padrão = pasta-mãe deste arquivo).

Data de referência das notas e fontes: 2026-11-04.
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

DATA_ACESSO = "2026-11-04"
VERSAO = "1.0.0"
NOTAS = "/mnt/project-files/jumba/conhecimento/metodologia/"
NOTAS_B3 = "/mnt/project-files/jumba/conhecimento/b3-outros/"

FONTES = {
    "b3_manual_aprecamento_opcoes": "https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf",
    "b3_manual_curvas": "https://www.b3.com.br/data/files/F3/42/AE/8C/1942B9105B12E5A9AC094EA8/Manual%20de%20Curvas_V21.pdf",
    "b3_di1_oc055_2024": "https://www.b3.com.br/data/files/FF/C5/51/86/158EE810C54843E8DC0D8AA8/OC%20055-2024%20PRE%20Contratos%20FE%20-%20Juros%20(PT).pdf",
    "b3_taxas_juros_252": "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/juros/programa-de-treinamento-di/02-taxas-de-juros.htm",
    "b3_calendario_2026": "https://www.b3.com.br/pt_br/noticias/calendario-de-negociacao-da-b3-confira-o-funcionamento-da-bolsa-em-2026.htm",
    "b3_oc007_2026_vencimentos": "https://www.b3.com.br/data/files/05/A1/CA/C2/EFE2C91076A8EEB9AC094EA8/OC%20007-2026-VPC%20ALTERACOES%20CONTRATOSTERMO%20OPCOES%20ACOES%20UNITS%20ETFS%20BDRS%20FUTURO%20ACOES%20UNITS%20REPUBLICACAO%20CONTRATOS%20DERIVATIVOS%20EQUITIES.pdf",
    "b3_glossario_oi": "https://b3.com.br/data/files/1E/D1/BA/58/C841B810E9C1AAA8AC094EA8/DerivativesOpenPositionFile%202023.pdf",
    "anbima_feriados": "https://www.anbima.com.br/feriados/fer_nacionais/{ano}.asp",
    "squeezemetrics_gex": "https://squeezemetrics.com/monitor/download/pdf/white_paper.pdf",
    "spotgamma_gex": "https://spotgamma.com/gamma-exposure-gex/",
    "spotgamma_walls": "https://spotgamma.com/call-wall-put-wall-explained/",
    "perfiliev_zero_gamma": "https://threadreaderapp.com/thread/1489373524066279430.html",
    "optionalpha_max_pain": "https://optionalpha.com/learn/max-pain-options",
    "cboe_pcr": "https://www.cboe.com/us/options/market_statistics/daily/",
    "clube_pai_rico_iq": "https://www.clubedopairico.com.br/o-indice-de-qualidade-na-venda-de-opcoes/22810",
    "wikipedia_bs_equation": "https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation",
}

# ----------------------------------------------------------------------------
# Numérica básica
# ----------------------------------------------------------------------------
SQ2 = math.sqrt(2.0)
SQ2PI = math.sqrt(2.0 * math.pi)


def N(x):
    return 0.5 * math.erfc(-x / SQ2)


def phi(x):
    return math.exp(-0.5 * x * x) / SQ2PI


def gbs(tipo, S, K, T, r, b, sig):
    """Black-Scholes generalizado (custo de carregamento b). Θ = ∂V/∂t, por ano."""
    sqT = math.sqrt(T)
    d1 = (math.log(S / K) + (b + 0.5 * sig * sig) * T) / (sig * sqT)
    d2 = d1 - sig * sqT
    eb = math.exp((b - r) * T)
    er = math.exp(-r * T)
    if tipo == "C":
        preco = S * eb * N(d1) - K * er * N(d2)
        delta = eb * N(d1)
        theta = -S * eb * phi(d1) * sig / (2 * sqT) - (b - r) * S * eb * N(d1) - r * K * er * N(d2)
    else:
        preco = K * er * N(-d2) - S * eb * N(-d1)
        delta = -eb * N(-d1)
        theta = -S * eb * phi(d1) * sig / (2 * sqT) + (b - r) * S * eb * N(-d1) + r * K * er * N(-d2)
    gamma = eb * phi(d1) / (S * sig * sqT)
    return {"preco": preco, "delta": delta, "gamma": gamma, "theta_aa": theta, "d1": d1, "d2": d2}


def gamma_fd(tipo, S, K, T, r, b, sig):
    h = 1e-4 * S
    f = lambda s: gbs(tipo, s, K, T, r, b, sig)["preco"]
    return (f(S + h) - 2 * f(S) + f(S - h)) / (h * h)


def delta_fd(tipo, S, K, T, r, b, sig):
    h = 1e-4 * S
    f = lambda s: gbs(tipo, s, K, T, r, b, sig)["preco"]
    return (f(S + h) - f(S - h)) / (2 * h)


def theta_fd(tipo, S, K, T, r, b, sig):
    e = 1e-6
    f = lambda t: gbs(tipo, S, K, t, r, b, sig)["preco"]
    return -(f(T + e) - f(T - e)) / (2 * e)


def brent(f, a, b, tol=1e-13, maxit=200):
    """Método de Brent (Brent 1973; forma de Numerical Recipes)."""
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("sem troca de sinal")
    c, fc = b, fb
    d = e = b - a
    for it in range(1, maxit + 1):
        if fb * fc > 0:
            c, fc = a, fa
            d = e = b - a
        if abs(fc) < abs(fb):
            a, b, c = b, c, b
            fa, fb, fc = fb, fc, fb
        tol1 = 2 * 2.220446049250313e-16 * abs(b) + 0.5 * tol
        xm = 0.5 * (c - b)
        if abs(xm) <= tol1 or fb == 0:
            return b, it
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb / fa
            if a == c:
                p = 2 * xm * s
                q = 1 - s
            else:
                q = fa / fc
                rr = fb / fc
                p = s * (2 * xm * q * (q - rr) - (b - a) * (rr - 1))
                q = (q - 1) * (rr - 1) * (s - 1)
            if p > 0:
                q = -q
            p = abs(p)
            if 2 * p < min(3 * xm * q - abs(tol1 * q), abs(e * q)):
                e, d = d, p / q
            else:
                d = xm
                e = d
        else:
            d = xm
            e = d
        a, fa = b, fb
        b = b + d if abs(d) > tol1 else b + math.copysign(tol1, xm)
        fb = f(b)
    return b, maxit


def bissecao(f, a, b, tol=1e-12):
    fa = f(a)
    for _ in range(300):
        m = 0.5 * (a + b)
        fm = f(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
        if b - a < tol:
            break
    return 0.5 * (a + b)


# ----------------------------------------------------------------------------
# Calendário B3 / ANBIMA (implementação própria, conferida contra o JSON do projeto)
# ----------------------------------------------------------------------------
D = dt.date
UM = dt.timedelta(days=1)


def pascoa_meeus(ano):
    """Algoritmo de Meeus/Jones/Butcher (computus gregoriano)."""
    a = ano % 19
    b, c = divmod(ano, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes, dia = divmod(h + l - 7 * m + 114, 31)
    return D(ano, mes, dia + 1)


def feriados_anbima(ano):
    """Dias sem expediente para a contagem de DU da curva (calendário ANBIMA)."""
    p = pascoa_meeus(ano)
    fixos = [(1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (12, 25)]
    s = {D(ano, m, d) for m, d in fixos}
    if ano >= 2024:
        s.add(D(ano, 11, 20))  # Lei 14.759/2023
    s |= {p - 48 * UM, p - 47 * UM, p - 2 * UM, p + 60 * UM}
    return s


def sem_pregao_b3(ano):
    """Dias úteis de semana sem sessão na B3 (ANBIMA + 24/12 + último dia útil do ano)."""
    s = set(feriados_anbima(ano))
    s.add(D(ano, 12, 24))
    u = D(ano, 12, 31)
    while u.weekday() >= 5:
        u -= UM
    s.add(u)
    return {d for d in s if d.weekday() < 5}


_CACHE = {}


def eh_util(d, cal):
    if d.weekday() >= 5:
        return False
    chave = (cal, d.year)
    if chave not in _CACHE:
        _CACHE[chave] = sem_pregao_b3(d.year) if cal == "B3" else feriados_anbima(d.year)
    return d not in _CACHE[chave]


def du_entre(d0, d1, cal="B3", regra="(d0,d1]"):
    """Dias úteis. Regra padrão: exclui d0 e inclui d1. Alternativa '[d0,d1)' (DI1)."""
    if d1 < d0:
        return -du_entre(d1, d0, cal, regra)
    n = 0
    d = d0 + UM if regra == "(d0,d1]" else d0
    fim = d1 if regra == "(d0,d1]" else d1 - UM
    while d <= fim:
        if eh_util(d, cal):
            n += 1
        d += UM
    return n


def sessao_anterior_ou_igual(d):
    while not eh_util(d, "B3"):
        d -= UM
    return d


def sessao_seguinte_ou_igual(d, cal="B3"):
    while not eh_util(d, cal):
        d += UM
    return d


def terceira_sexta(ano, mes):
    d = D(ano, mes, 1)
    while d.weekday() != 4:
        d += UM
    return d + 14 * UM


def venc_acao_mensal(ano, mes):
    return sessao_anterior_ou_igual(terceira_sexta(ano, mes))


def iso(d):
    return d.isoformat()


# ----------------------------------------------------------------------------
# Parâmetros comuns
# ----------------------------------------------------------------------------
HOJE = D(2026, 11, 4)
VENC1 = venc_acao_mensal(2026, 11)   # 2026-11-19 (3ª sexta 20/11 é feriado)
VENC2 = venc_acao_mensal(2026, 12)   # 2026-12-18
DU1 = du_entre(HOJE, VENC1)
DU2 = du_entre(HOJE, VENC2)
DC1 = (VENC1 - HOJE).days
DC2 = (VENC2 - HOJE).days
DI_AA = 0.1065                      # taxa DI sintética, a.a. base 252 (mesma das notas 05 e 14)
R_CONT = math.log(1 + DI_AA)
S0 = 30.0
M = 1                               # multiplicador (opção de ação: 1 opção = 1 ação)

# Cadeia sintética: vencimento 1 (10 strikes) e vencimento 2 (5 strikes). Tudo inventado.
CADEIA = {
    "V1": {
        "vencimento": VENC1, "du": DU1, "dc": DC1,
        "K":     [26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
        "sigma": [0.42, 0.40, 0.38, 0.365, 0.35, 0.345, 0.345, 0.35, 0.36, 0.37],
        "C": {
            "oi":    [500, 800, 2000, 4000, 4000, 16000, 18000, 20000, 8000, 25000],
            "cvrd":  [300, 500, 1200, 2400, 2200, 7000, 9000, 13000, 5000, 18000],
            "blck":  [50, 100, 300, 600, 700, 2000, 2000, 3000, 1000, 2000],
            "tit":   [40, 60, 150, 300, 420, 900, 1300, 1700, 600, 2100],
            "lanc":  [30, 40, 90, 160, 230, 420, 650, 800, 300, 700],
            "qtd":   [100, 200, 600, 1500, 3000, 5000, 6000, 4000, 1000, 2000],
        },
        "P": {
            "oi":    [22000, 9000, 18000, 14000, 10000, 6000, 2000, 1000, 600, 300],
            "cvrd":  [0] * 10,
            "blck":  [6000, 3000, 5000, 4000, 3000, 2000, 500, 300, 100, 100],
            "tit":   [900, 500, 800, 700, 520, 260, 120, 60, 40, 20],
            "lanc":  [1100, 450, 750, 520, 400, 300, 110, 50, 45, 0],
            "qtd":   [3000, 1500, 4000, 3500, 2500, 1200, 300, 100, 50, 0],
        },
    },
    "V2": {
        "vencimento": VENC2, "du": DU2, "dc": DC2,
        "K":     [28, 29, 30, 31, 32],
        "sigma": [0.37, 0.36, 0.35, 0.345, 0.345],
        "C": {
            "oi":    [3000, 5000, 7000, 9000, 6000],
            "cvrd":  [2000, 3000, 4000, 6000, 4000],
            "blck":  [500, 500, 1000, 1000, 500],
            "tit":   [200, 330, 500, 640, 420],
            "lanc":  [150, 200, 260, 300, 200],
            "qtd":   [500, 800, 1200, 900, 400],
        },
        "P": {
            "oi":    [8000, 7000, 5000, 2000, 1000],
            "cvrd":  [0] * 5,
            "blck":  [2000, 2000, 1500, 500, 200],
            "tit":   [420, 380, 300, 130, 70],
            "lanc":  [460, 360, 240, 100, 60],
            "qtd":   [900, 700, 600, 200, 100],
        },
    },
}


def series():
    """Lista plana de séries, com descoberto = OI − coberto − travado e gregas BS_B3."""
    out = []
    for vk, v in CADEIA.items():
        T = v["du"] / 252
        for tipo in ("C", "P"):
            for j, K in enumerate(v["K"]):
                lado = v[tipo]
                oi = lado["oi"][j]
                cv, bl = lado["cvrd"][j], lado["blck"][j]
                sig = v["sigma"][j]
                g = gbs(tipo, S0, K, T, R_CONT, R_CONT, sig)
                preco_medio = max(0.01, round(g["preco"], 2))
                out.append({
                    "id": f"SINT{vk}{tipo}{K}", "venc": vk, "vencimento": iso(v["vencimento"]),
                    "du": v["du"], "T": T, "tipo": tipo, "K": float(K), "sigma": sig,
                    "oi": oi, "cvrd": cv, "blck": bl, "ucvrd": oi - cv - bl,
                    "titulares": lado["tit"][j], "lancadores": lado["lanc"][j],
                    "qtd_dia": lado["qtd"][j], "preco_medio": preco_medio,
                    "fin_dia": round(lado["qtd"][j] * preco_medio, 2), "g": g,
                })
    return out


SERIES = series()


def sel(venc=None, tipo=None):
    return [s for s in SERIES if (venc is None or s["venc"] == venc) and (tipo is None or s["tipo"] == tipo)]


def tabela_entrada(venc):
    v = CADEIA[venc]
    linhas = []
    for s in sel(venc):
        linhas.append({k: s[k] for k in ("id", "tipo", "K", "sigma", "oi", "cvrd", "blck", "ucvrd",
                                         "titulares", "lancadores", "qtd_dia", "preco_medio", "fin_dia")})
    return {"vencimento": iso(v["vencimento"]), "du": v["du"], "dc": v["dc"], "series": linhas}


# ----------------------------------------------------------------------------
# 1. Max Pain
# ----------------------------------------------------------------------------
def caso_max_pain():
    ss = sel("V1")
    Ks = sorted({s["K"] for s in ss})
    calls = [(s["K"], s["oi"]) for s in ss if s["tipo"] == "C" and s["oi"] > 0]
    puts = [(s["K"], s["oi"]) for s in ss if s["tipo"] == "P" and s["oi"] > 0]

    def dor(X):
        return M * (sum(o * max(X - k, 0) for k, o in calls) + sum(o * max(k - X, 0) for k, o in puts))

    def itm(X):
        return sum(o for k, o in calls if X > k) + sum(o for k, o in puts if X < k)

    linhas = []
    for X in Ks:
        dl = M * (sum(o for k, o in calls if k < X) - sum(o for k, o in puts if k >= X))
        dr = M * (sum(o for k, o in calls if k <= X) - sum(o for k, o in puts if k > X))
        linhas.append({"X": X, "dor_rs": dor(X), "itm_contratos": itm(X),
                       "derivada_esq": dl, "derivada_dir": dr})

    def argmin_desempate(f):
        vmin = min(f(X) for X in Ks)
        cand = [X for X in Ks if f(X) == vmin]
        return sorted(cand, key=lambda X: (abs(X - S0), X))[0], cand

    mpA, candA = argmin_desempate(dor)
    mpB, candB = argmin_desempate(itm)
    # conferência independente do método A: condição de 1ª ordem (mediana ponderada)
    foc = [l["X"] for l in linhas if l["derivada_esq"] <= 0 <= l["derivada_dir"]]
    # conferência: mínimo em grade fina (0,01) não fica abaixo do mínimo nos strikes
    fino = min(dor(26 + 0.01 * i) for i in range(0, 901))

    # caso de empate no método B
    calls_e = [(28, 1000), (30, 1000)]
    puts_e = [(30, 1000), (32, 1000)]
    Ke = [28, 29, 30, 31, 32]

    def itm_e(X):
        return sum(o for k, o in calls_e if X > k) + sum(o for k, o in puts_e if X < k)

    def dor_e(X):
        return sum(o * max(X - k, 0) for k, o in calls_e) + sum(o * max(k - X, 0) for k, o in puts_e)

    vmin_e = min(itm_e(X) for X in Ke)
    cand_e = [X for X in Ke if itm_e(X) == vmin_e]
    S_e = 31.8
    esc_e = sorted(cand_e, key=lambda X: (abs(X - S_e), X))[0]

    return {
        "descricao": "Max Pain de um vencimento (V1), cadeia sintética de 10 strikes. Método A = menor valor intrínseco pago aos titulares; método B = menor quantidade de contratos dentro do dinheiro. A cadeia foi montada para os dois métodos darem respostas diferentes.",
        "nota_metodologica": NOTAS + "10-max-pain.md",
        "fontes": [FONTES["optionalpha_max_pain"]],
        "convencoes": {
            "grade": "só os strikes listados (Dor é convexa e linear por partes; o mínimo cai num strike)",
            "atm_conta_como_itm": False,
            "desempate": "strike mais próximo de S; se ainda empatar, o menor strike",
            "multiplicador": M,
            "series_oi_zero": "ignoradas",
        },
        "entradas": {"S": S0, "vencimento": iso(VENC1),
                      "calls_oi": {str(int(k)): o for k, o in calls}, "puts_oi": {str(int(k)): o for k, o in puts}},
        "formulas": {
            "dor": "Dor(X) = m·[Σ_c OI_c·max(X−k_c,0) + Σ_p OI_p·max(k_p−X,0)]",
            "itm": "ITM(X) = Σ_c OI_c·1[X>k_c] + Σ_p OI_p·1[X<k_p]",
            "derivada_esq": "m·[Σ_{k_c<X} OI_c − Σ_{k_p≥X} OI_p]",
            "derivada_dir": "m·[Σ_{k_c≤X} OI_c − Σ_{k_p>X} OI_p]",
        },
        "saidas": {
            "tabela": linhas, "max_pain_a": mpA, "max_pain_b": mpB,
            "candidatos_a": candA, "candidatos_b": candB,
            "dist_pct_a": mpA / S0 - 1, "dist_pct_b": mpB / S0 - 1,
        },
        "verificacao": {
            "metodo_a_por_condicao_1a_ordem": foc,
            "minimo_grade_fina_0_01": fino,
            "confere": foc == [mpA] and abs(fino - dor(mpA)) < 1e-9,
        },
        "caso_empate_b": {
            "descricao": "Empate no método B: dois strikes com a mesma contagem mínima; escolhe o mais próximo de S.",
            "S": S_e, "calls_oi": {str(k): o for k, o in calls_e}, "puts_oi": {str(k): o for k, o in puts_e},
            "itm": {str(X): itm_e(X) for X in Ke}, "dor": {str(X): dor_e(X) for X in Ke},
            "candidatos_b": cand_e, "max_pain_b": esc_e,
            "max_pain_a": min(Ke, key=lambda X: (dor_e(X), abs(X - S_e))),
        },
    }


# ----------------------------------------------------------------------------
# 2. PCR
# ----------------------------------------------------------------------------
def razao(num, den):
    if den == 0:
        return None, ["SEM_CALLS"]
    return num / den, []


def pcr_bloco(ss):
    c = [s for s in ss if s["tipo"] == "C"]
    p = [s for s in ss if s["tipo"] == "P"]
    out = {}
    for nome, campo in (("oi", "oi"), ("vol", "qtd_dia"), ("fin", "fin_dia"), ("desc", "ucvrd")):
        num = sum(s[campo] for s in p)
        den = sum(s[campo] for s in c)
        v, fl = razao(num, den)
        out[nome] = {"puts": num, "calls": den, "pcr": v, "flags": fl}
    # ponderado por delta
    num = sum(abs(s["g"]["delta"]) * s["oi"] for s in p)
    den = sum(s["g"]["delta"] * s["oi"] for s in c)
    out["delta"] = {"puts": num, "calls": den, "pcr": num / den, "flags": []}
    return out


def caso_pcr():
    vazio = [
        {"tipo": "C", "oi": 1000, "qtd_dia": 0, "fin_dia": 0.0, "ucvrd": 400},
        {"tipo": "P", "oi": 500, "qtd_dia": 200, "fin_dia": 90.0, "ucvrd": 300},
    ]
    vz = {}
    for nome, campo in (("oi", "oi"), ("vol", "qtd_dia"), ("fin", "fin_dia"), ("desc", "ucvrd")):
        num = sum(s[campo] for s in vazio if s["tipo"] == "P")
        den = sum(s[campo] for s in vazio if s["tipo"] == "C")
        v, fl = razao(num, den)
        vz[nome] = {"puts": num, "calls": den, "pcr": v, "flags": fl}
    return {
        "descricao": "Put/Call Ratio por OI, por volume (quantidade), por financeiro, só descoberto e ponderado por delta; por vencimento e em TODOS (soma de quantidades, não média de razões).",
        "nota_metodologica": NOTAS + "11-pcr.md",
        "fontes": [FONTES["cboe_pcr"]],
        "convencoes": {
            "agregacao_todos": "razão de somas (Σ puts ÷ Σ calls) sobre todos os vencimentos",
            "unidade": "quantidade de opções; o multiplicador se cancela",
            "denominador_zero": "pcr = null e flag SEM_CALLS",
            "financeiro": "qtd_dia × preco_medio (preço médio sintético, 2 casas)",
            "delta": "Σ|Δ_p|·OI_p ÷ Σ Δ_c·OI_c, com Δ do BS_B3 (S=30, DI 10,65 %, σ da tabela)",
        },
        "entradas": "ver bloco 'cadeia' (V1 e V2)",
        "saidas": {"V1": pcr_bloco(sel("V1")), "V2": pcr_bloco(sel("V2")), "TODOS": pcr_bloco(SERIES)},
        "caso_sem_calls": {"series": vazio, "saidas": vz},
        "verificacao": {
            "todos_oi_igual_soma": abs(pcr_bloco(SERIES)["oi"]["pcr"] -
                                       (sum(s["oi"] for s in SERIES if s["tipo"] == "P") /
                                        sum(s["oi"] for s in SERIES if s["tipo"] == "C"))) < 1e-15,
            "todos_diferente_da_media_das_razoes": abs(pcr_bloco(SERIES)["oi"]["pcr"] -
                                                       0.5 * (pcr_bloco(sel("V1"))["oi"]["pcr"] + pcr_bloco(sel("V2"))["oi"]["pcr"])) > 1e-6,
        },
    }


# ----------------------------------------------------------------------------
# 3. IQ
# ----------------------------------------------------------------------------
def iq_bloco(ss, tipo):
    xs = [s for s in ss if s["tipo"] == tipo]
    validas = [s for s in xs if s["lancadores"] > 0]
    fora = [s["id"] for s in xs if s["lancadores"] == 0]
    H = sum(s["titulares"] for s in validas)
    W = sum(s["lancadores"] for s in validas)
    iq_i = {s["id"]: s["titulares"] / s["lancadores"] for s in validas}
    soi = sum(s["oi"] for s in validas)
    sdesc = sum(s["ucvrd"] for s in validas)
    return {
        "razao_somas": H / W, "soma_titulares": H, "soma_lancadores": W,
        "pond_oi": sum(s["oi"] * iq_i[s["id"]] for s in validas) / soi,
        "pond_desc": sum(s["ucvrd"] * iq_i[s["id"]] for s in validas) / sdesc,
        "excluidas_sem_lancador": fora,
    }


def caso_iq():
    por_serie = []
    for s in SERIES:
        if s["lancadores"] == 0:
            por_serie.append({"id": s["id"], "titulares": s["titulares"], "lancadores": 0, "iq": None, "flags": ["SEM_LANCADOR"]})
        else:
            por_serie.append({"id": s["id"], "titulares": s["titulares"], "lancadores": s["lancadores"],
                              "iq": s["titulares"] / s["lancadores"], "flags": []})
    # barreiras: limiar escalado para a cadeia sintética
    Qmin, IQmin, h = 5000, 1.2, 0.10
    barr = []
    for s in SERIES:
        if s["lancadores"] == 0:
            continue
        iq = s["titulares"] / s["lancadores"]
        dist = s["K"] / S0 - 1
        if s["ucvrd"] >= Qmin and iq >= IQmin and abs(dist) <= h:
            barr.append({"id": s["id"], "K": s["K"], "ucvrd": s["ucvrd"], "iq": iq, "dist_pct": dist})
    return {
        "descricao": "Índice de Qualidade = titulares ÷ lançadores (contagens de clientes), por série e agregado por tipo (calls e puts separados), por vencimento e global; mais o filtro de barreiras (descoberto alto e IQ alto perto do preço).",
        "nota_metodologica": NOTAS + "12-indice-qualidade.md",
        "fontes": [FONTES["clube_pai_rico_iq"], FONTES["b3_glossario_oi"]],
        "dependencia_de_dado": "[S] titulares e lançadores viriam de BrrwrQty/LndrQty do arquivo de posições em aberto da B3; não confirmado. Os números aqui são sintéticos.",
        "convencoes": {
            "padrao": "razão de somas por tipo (Σ titulares ÷ Σ lançadores)",
            "alternativas": ["ponderado por OI", "ponderado por descoberto"],
            "lancadores_zero": "série fora do agregado, iq = null, flag SEM_LANCADOR",
            "global": "razão de somas sobre V1 + V2 (no produto real: sobre todos os ativos do universo)",
            "barreiras": {"Q_min_descoberto": Qmin, "IQ_min": IQmin, "faixa_h": h,
                          "obs": "limiar de 5 milhões da nota 12 escalado para 5.000 por causa do tamanho da cadeia sintética"},
        },
        "saidas": {
            "por_serie": por_serie,
            "V1": {"calls": iq_bloco(sel("V1"), "C"), "puts": iq_bloco(sel("V1"), "P")},
            "V2": {"calls": iq_bloco(sel("V2"), "C"), "puts": iq_bloco(sel("V2"), "P")},
            "GLOBAL": {"calls": iq_bloco(SERIES, "C"), "puts": iq_bloco(SERIES, "P")},
            "barreiras": barr,
        },
    }


# ----------------------------------------------------------------------------
# 4. Total = Coberto + Travado + Descoberto
# ----------------------------------------------------------------------------
def caso_quebra_oi():
    linhas = []
    for s in sel("V1"):
        tot = s["cvrd"] + s["blck"] + s["ucvrd"]
        linhas.append({"id": s["id"], "oi": s["oi"], "cvrd": s["cvrd"], "blck": s["blck"], "ucvrd": s["ucvrd"],
                       "soma": tot, "pct_coberto": s["cvrd"] / s["oi"], "pct_travado": s["blck"] / s["oi"],
                       "pct_descoberto": s["ucvrd"] / s["oi"], "flags": [] if tot == s["oi"] else ["SOMA_DIVERGE"]})
    por_tipo = {}
    for tipo in ("C", "P"):
        xs = sel("V1", tipo)
        o = sum(s["oi"] for s in xs)
        c = sum(s["cvrd"] for s in xs)
        b = sum(s["blck"] for s in xs)
        u = sum(s["ucvrd"] for s in xs)
        por_tipo[tipo] = {"oi": o, "cvrd": c, "blck": b, "ucvrd": u, "pct_descoberto": u / o, "confere": c + b + u == o}
    especiais = [
        {"id": "DIVERGE1", "oi_informado": 10000, "cvrd": 6000, "blck": 1000, "ucvrd": 2900,
         "soma": 9900, "diferenca": -100, "flags": ["SOMA_DIVERGE"],
         "regra": "não corrigir; manter os campos como vieram, marcar a série e usar oi_informado como total"},
        {"id": "SEM_QUEBRA1", "oi_informado": 5000, "cvrd": None, "blck": None, "ucvrd": None,
         "soma": None, "diferenca": None, "flags": ["SEM_QUEBRA"],
         "regra": "opções sobre futuro costumam vir sem a quebra; % descoberto = null; o total vale"},
        {"id": "VARIACAO1", "oi_d": 12000, "oi_dm1": 9500, "variacao_informada": 2500,
         "variacao_calculada": 2500, "flags": [],
         "regra": "VartnOpnIntrst deve ser igual a OpnIntrst(D) − OpnIntrst(D−1); se não for, flag VARIACAO_DIVERGE"},
    ]
    return {
        "descricao": "Identidade Total = Coberto + Travado + Descoberto por série do V1, percentuais e somas por tipo; casos de borda (soma diverge, sem quebra, variação contra D−1).",
        "nota_metodologica": "/mnt/project-files/jumba/conhecimento/b3-opcoes/02-posicoes-em-aberto.md",
        "fontes": [FONTES["b3_glossario_oi"]],
        "convencoes": {
            "campos_b3": {"oi": "OpnIntrst", "cvrd": "CvrdQty", "blck": "TtlBlckdPos", "ucvrd": "UcvrdQty", "total_alternativo": "TtlPos"},
            "identidade": "cvrd + blck + ucvrd = total [S]: falta testar no arquivo real se o total certo é OpnIntrst ou TtlPos",
            "puts_coberto": "nas puts sintéticas o coberto é 0 (escolha do vetor; conferir no arquivo real)",
            "percentuais": "sobre o total da série",
        },
        "saidas": {"por_serie": linhas, "por_tipo": por_tipo, "especiais": especiais},
    }


# ----------------------------------------------------------------------------
# 5. GEX e DEX
# ----------------------------------------------------------------------------
def sinal(s, conv):
    if conv == "A":
        return 1.0 if s["tipo"] == "C" else -1.0
    if conv == "B":
        return -1.0
    if conv == "D":  # θc=1, θb=0, θu=1
        return (1.0 * s["cvrd"] + 0.0 * s["blck"] - 1.0 * s["ucvrd"]) / s["oi"]
    raise ValueError(conv)


def gex_serie(s, conv, S=S0):
    g = s["g"]["gamma"] if S == S0 else gbs(s["tipo"], S, s["K"], s["T"], R_CONT, R_CONT, s["sigma"])["gamma"]
    u1 = sinal(s, conv) * g * s["oi"] * M
    return {"u1": u1, "u2": u1 * S, "u3": u1 * S * S * 0.01}


def dex_serie(s, conv):
    d1 = sinal(s, conv) * s["g"]["delta"] * s["oi"] * M
    return {"unid": d1, "rs": d1 * S0}


def gex_por_strike(ss, conv):
    Ks = sorted({s["K"] for s in ss})
    por = {K: 0.0 for K in Ks}
    for s in ss:
        por[s["K"]] += gex_serie(s, conv)["u3"]
    acum, a = {}, 0.0
    for K in Ks:
        a += por[K]
        acum[K] = a
    return por, acum


def caso_gex_dex():
    ss_all = SERIES
    tab = []
    for s in ss_all:
        gA = gex_serie(s, "A")
        tab.append({"id": s["id"], "tipo": s["tipo"], "K": s["K"], "du": s["du"], "T": s["T"], "sigma": s["sigma"],
                    "oi": s["oi"], "preco_bs": s["g"]["preco"], "delta": s["g"]["delta"], "gamma": s["g"]["gamma"],
                    "theta_aa": s["g"]["theta_aa"],
                    "s_A": sinal(s, "A"), "s_B": sinal(s, "B"), "s_D": sinal(s, "D"),
                    "gex_u1_A": gA["u1"], "gex_u2_A": gA["u2"], "gex_u3_A": gA["u3"],
                    "gex_u3_B": gex_serie(s, "B")["u3"], "gex_u3_D": gex_serie(s, "D")["u3"],
                    "dex_rs_A": dex_serie(s, "A")["rs"]})
    blocos = {}
    for filtro, ss in (("PROXIMO_V1", sel("V1")), ("TODOS", ss_all)):
        b = {}
        for conv in ("A", "B", "D"):
            por, acum = gex_por_strike(ss, conv)
            tot = sum(gex_serie(s, conv)["u3"] for s in ss)
            b[conv] = {
                "gex_strike_u3": {str(k): v for k, v in por.items()},
                "gex_acumulado_u3": {str(k): v for k, v in acum.items()},
                "gex_total_u3": tot,
                "gex_total_u1": sum(gex_serie(s, conv)["u1"] for s in ss),
                "gex_total_u2": sum(gex_serie(s, conv)["u2"] for s in ss),
            }
            Ks = sorted({s["K"] for s in ss})
            dpor = {K: 0.0 for K in Ks}
            for s in ss:
                dpor[s["K"]] += dex_serie(s, conv)["rs"]
            dtot = sum(dpor.values())
            b[conv].update({
                "dex_strike_rs": {str(k): v for k, v in dpor.items()},
                "dex_total_rs": dtot,
                "dex_total_unid": sum(dex_serie(s, conv)["unid"] for s in ss),
                "hedge_formador_rs": -dtot,
                "dex_atm_2pct_rs": sum(dex_serie(s, conv)["rs"] for s in ss if abs(s["K"] / S0 - 1) <= 0.02 + 1e-12),
                "dex_atm_5pct_rs": sum(dex_serie(s, conv)["rs"] for s in ss if abs(s["K"] / S0 - 1) <= 0.05 + 1e-12),
                "regime_no_spot": "POSITIVO" if tot > 0 else ("NEGATIVO" if tot < 0 else "ZERO"),
            })
        blocos[filtro] = b
    # verificação independente: gamma e delta por diferenças finitas; theta por diferença no prazo
    errs_g = max(abs(gamma_fd(s["tipo"], S0, s["K"], s["T"], R_CONT, R_CONT, s["sigma"]) - s["g"]["gamma"]) / s["g"]["gamma"] for s in ss_all)
    errs_d = max(abs(delta_fd(s["tipo"], S0, s["K"], s["T"], R_CONT, R_CONT, s["sigma"]) - s["g"]["delta"]) for s in ss_all)
    errs_t = max(abs(theta_fd(s["tipo"], S0, s["K"], s["T"], R_CONT, R_CONT, s["sigma"]) - s["g"]["theta_aa"]) for s in ss_all)
    # vetor da nota 05 (S=30, K=32, DU=21, DI=10,65 %, σ=35 %)
    g05 = gbs("C", 30.0, 32.0, 21 / 252, R_CONT, R_CONT, 0.35)
    return {
        "descricao": "GEX (gamma exposure) e DEX (delta exposure) por série, por strike, acumulado e total; filtros PROXIMO_V1 e TODOS; três convenções de sinal.",
        "nota_metodologica": NOTAS + "08-gex-dex.md",
        "fontes": [FONTES["squeezemetrics_gex"], FONTES["spotgamma_gex"], FONTES["perfiliev_zero_gamma"]],
        "convencoes": {
            "modelo": "BS sem dividendos, convenção B3 para ações (b = r)",
            "r": "r = ln(1 + DI), DI = 10,65 % a.a. base 252",
            "T": "DU/252, DU pelo calendário B3, de 2026-11-04 (exclusive) ao vencimento (inclusive)",
            "S": S0, "multiplicador": M,
            "sinal": {
                "A": "PADRÃO. Formador comprado em calls (+1) e vendido em puts (−1)",
                "B": "formador vendido em tudo (−1 em calls e puts)",
                "D": "heurística B3: s = (θc·coberto + θb·travado − θu·descoberto)/OI, com θc=1, θb=0, θu=1 [S, sem fonte]",
            },
            "leitura": "GEX > 0: hedge do formador contra o movimento (amortece). GEX < 0: hedge a favor (acelera).",
            "unidades": {
                "u1": "s·Γ·OI·m (ações por R$ 1 de movimento)",
                "u2": "s·Γ·OI·m·S (R$ de delta por R$ 1)",
                "u3": "s·Γ·OI·m·S²·0,01 (R$ de delta por movimento de 1 %) — PADRÃO",
                "dex_rs": "s·Δ·OI·m·S (R$); hedge do formador = −DEX",
            },
            "eixo": "strike vigente; séries de vencimentos diferentes com o mesmo strike somam no mesmo ponto",
            "faixa_atm": "|K/S − 1| ≤ h, com h = 2 % e 5 % (inclusive)",
        },
        "entradas": {"S": S0, "DI_aa": DI_AA, "r_cont": R_CONT,
                      "V1": {"vencimento": iso(VENC1), "du": DU1}, "V2": {"vencimento": iso(VENC2), "du": DU2}},
        "saidas": {"por_serie": tab, "agregados": blocos},
        "verificacao": {
            "erro_rel_max_gamma_vs_diferencas_finitas": errs_g,
            "erro_abs_max_delta_vs_diferencas_finitas": errs_d,
            "erro_abs_max_theta_vs_diferencas_finitas": errs_t,
            "vetor_nota_05_gamma_call_S30_K32_DU21": g05["gamma"],
            "vetor_nota_05_esperado": 0.115873,
            "confere_nota_05": abs(g05["gamma"] - 0.115873) < 5e-7,
        },
    }


# ----------------------------------------------------------------------------
# 6. Gamma flip
# ----------------------------------------------------------------------------
def perfil(ss, conv, X):
    tot = 0.0
    for s in ss:
        g = gbs(s["tipo"], X, s["K"], s["T"], R_CONT, R_CONT, s["sigma"])["gamma"]
        tot += sinal(s, conv) * g * s["oi"] * M * X * X * 0.01
    return tot


def flip_m1(ss, conv):
    passos = [0.70 + 0.0025 * i for i in range(241)]
    grade = [S0 * p for p in passos]
    vals = [perfil(ss, conv, X) for X in grade]
    raizes = []
    for i in range(len(grade) - 1):
        a, b = grade[i], grade[i + 1]
        fa, fb = vals[i], vals[i + 1]
        if fa == 0:
            raizes.append({"x": a, "brent_iter": 0, "bissecao": a})
        elif fa * fb < 0:
            f = lambda x: perfil(ss, conv, x)
            x, it = brent(f, a, b)
            xb = bissecao(f, a, b)
            raizes.append({"x": x, "brent_iter": it, "bissecao": xb, "intervalo": [a, b]})
    principal = min(raizes, key=lambda r: abs(r["x"] - S0))["x"] if raizes else None
    gs = perfil(ss, conv, S0)
    if principal is None:
        regime = "SEM_FLIP"
    elif abs(S0 - principal) / S0 <= 0.005:
        regime = "PERTO_DO_FLIP"
    else:
        regime = "POSITIVO" if gs > 0 else "NEGATIVO"
    amostra = [{"X": grade[i], "G": vals[i]} for i in range(0, 241, 4)]  # a cada 1 % de S
    imax = max(range(241), key=lambda i: vals[i])
    imin = min(range(241), key=lambda i: vals[i])
    return {"raizes": raizes, "flip_principal": principal, "G_no_spot": gs, "regime": regime,
            "perfil_amostra_1pct": amostra, "x_max_grade": grade[imax], "G_max": vals[imax],
            "x_min_grade": grade[imin], "G_min": vals[imin]}


def flip_m2(ss, conv):
    por, acum = gex_por_strike(ss, conv)
    Ks = sorted(acum)
    cruz = []
    for i in range(len(Ks) - 1):
        a, b = acum[Ks[i]], acum[Ks[i + 1]]
        if a == 0:
            cruz.append(Ks[i])
        elif a * b < 0:
            cruz.append(Ks[i] + (Ks[i + 1] - Ks[i]) * (-a) / (b - a))
    troca_local = []
    for i in range(len(Ks) - 1):
        a, b = por[Ks[i]], por[Ks[i + 1]]
        if a * b < 0:
            troca_local.append([Ks[i], Ks[i + 1]])
    return {"acumulado": {str(k): v for k, v in acum.items()}, "cruzamentos": cruz,
            "flip": min(cruz, key=lambda x: abs(x - S0)) if cruz else None,
            "variante_troca_de_sinal_do_gex_por_strike": troca_local}


def caso_flip():
    out = {}
    for filtro, ss in (("PROXIMO_V1", sel("V1")), ("TODOS", SERIES)):
        out[filtro] = {"M1_varredura": flip_m1(ss, "A"), "M2_acumulado": flip_m2(ss, "A")}
    # caso sem flip: só calls (convenção A) → G(X) > 0 em toda a grade
    so_calls = sel("V1", "C")
    sem = flip_m1(so_calls, "A")
    return {
        "descricao": "Gamma flip pelo método 1 (varredura de preço com Γ recalculado em cada X, raiz por Brent) e pelo método 2 (troca de sinal do GEX acumulado por strike, interpolação linear). Convenção de sinal A.",
        "nota_metodologica": NOTAS + "09-gamma-flip-walls.md",
        "fontes": [FONTES["spotgamma_gex"], FONTES["perfiliev_zero_gamma"]],
        "convencoes": {
            "grade_M1": "X de 0,70·S a 1,30·S, passo 0,25 % de S (241 pontos)",
            "vol_no_perfil": "STICKY_STRIKE: σ de cada série fixo; r e T fixos",
            "raiz_principal": "a mais próxima de S; as demais vão em 'raizes'",
            "regime": "PERTO_DO_FLIP se |S − flip|/S ≤ 0,5 %; senão sinal de G(S)",
            "M2": "acumulado do menor para o maior strike, no spot atual, sem recalcular Γ",
            "unidade": "G em R$ por 1 % (u3)",
        },
        "saidas": out,
        "caso_sem_flip_so_calls_V1": {"flip_principal": sem["flip_principal"], "regime": sem["regime"], "G_no_spot": sem["G_no_spot"]},
        "verificacao": {"brent_vs_bissecao_max_dif": max(abs(r["x"] - r["bissecao"]) for f in out.values() for r in f["M1_varredura"]["raizes"]),
                        "G_na_raiz_max_abs": max(abs(perfil(ss, "A", r["x"])) for (fk, ss) in (("PROXIMO_V1", sel("V1")), ("TODOS", SERIES)) for r in out[fk]["M1_varredura"]["raizes"])},
    }


# ----------------------------------------------------------------------------
# 7. Call wall e put wall
# ----------------------------------------------------------------------------
def caso_walls():
    ss = sel("V1")
    Ks = sorted({s["K"] for s in ss})
    nocional = {"C": {K: 0.0 for K in Ks}, "P": {K: 0.0 for K in Ks}}
    oi = {"C": {K: 0 for K in Ks}, "P": {K: 0 for K in Ks}}
    for s in ss:
        nocional[s["tipo"]][s["K"]] += s["g"]["gamma"] * s["oi"] * M * S0 * S0 * 0.01
        oi[s["tipo"]][s["K"]] += s["oi"]
    gexA, _ = gex_por_strike(ss, "A")

    def am(d, cand, sinal_=1):
        return max(cand, key=lambda K: (sinal_ * d[K], -abs(K - S0)))

    acima = [K for K in Ks if K >= S0]
    abaixo = [K for K in Ks if K <= S0]
    regras = {
        "a_gamma_nocional": {"livre": {"call_wall": am(nocional["C"], Ks), "put_wall": am(nocional["P"], Ks)},
                             "restrito": {"call_wall": am(nocional["C"], acima), "put_wall": am(nocional["P"], abaixo)}},
        "b_oi": {"livre": {"call_wall": am(oi["C"], Ks), "put_wall": am(oi["P"], Ks)},
                 "restrito": {"call_wall": am(oi["C"], acima), "put_wall": am(oi["P"], abaixo)}},
        "c_gex_com_sinal_A": {"livre": {"call_wall": am(gexA, Ks, 1), "put_wall": am(gexA, Ks, -1)},
                              "restrito": {"call_wall": am(gexA, acima, 1), "put_wall": am(gexA, abaixo, -1)}},
    }
    return {
        "descricao": "Call wall e put wall do V1 por três regras (a: gamma nocional sem sinal por tipo; b: maior OI por tipo; c: GEX com sinal, maior positivo e mais negativo) e duas opções de lado (livre; restrito a K ≥ S para call e K ≤ S para put).",
        "nota_metodologica": NOTAS + "09-gamma-flip-walls.md",
        "fontes": [FONTES["spotgamma_walls"]],
        "convencoes": {"padrao": "regra a, lado livre", "desempate": "strike mais próximo de S",
                        "nocional": "Γ·OI·m·S²·0,01 por tipo e strike (R$ por 1 %, sem sinal)"},
        "saidas": {
            "gamma_nocional_calls": {str(k): v for k, v in nocional["C"].items()},
            "gamma_nocional_puts": {str(k): v for k, v in nocional["P"].items()},
            "oi_calls": {str(k): v for k, v in oi["C"].items()},
            "oi_puts": {str(k): v for k, v in oi["P"].items()},
            "gex_strike_A": {str(k): v for k, v in gexA.items()},
            "regras": regras,
        },
        "observacao": "A call 35 tem o maior OI de calls (25.000) mas pouco gamma; por isso a regra b dá 35 e a regra a dá outro strike. É de propósito.",
        "caso_lado_restrito": caso_walls_lado(),
    }


def caso_walls_lado():
    """Mini-cadeia em que a restrição de lado muda a resposta (call ITM e put ITM com muito OI)."""
    T = DU1 / 252
    mini = [("C", 29.0, 20000), ("C", 31.0, 8000), ("P", 31.0, 15000), ("P", 29.0, 6000)]
    noc = {"C": {}, "P": {}}
    for tipo, K, oi in mini:
        g = gbs(tipo, S0, K, T, R_CONT, R_CONT, 0.35)["gamma"]
        noc[tipo][K] = g * oi * M * S0 * S0 * 0.01
    def am(d, cand):
        return max(cand, key=lambda K: (d[K], -abs(K - S0)))
    return {
        "descricao": "S = 30, σ = 35 % em todas, DU = 11. Calls em 29 (ITM) e 31; puts em 31 (ITM) e 29.",
        "series": [{"tipo": t, "K": K, "oi": o} for t, K, o in mini],
        "gamma_nocional": {t: {str(k): v for k, v in d.items()} for t, d in noc.items()},
        "livre": {"call_wall": am(noc["C"], list(noc["C"])), "put_wall": am(noc["P"], list(noc["P"]))},
        "restrito": {"call_wall": am(noc["C"], [k for k in noc["C"] if k >= S0]),
                     "put_wall": am(noc["P"], [k for k in noc["P"] if k <= S0])},
    }


# ----------------------------------------------------------------------------
# 8. Movimento de equilíbrio gamma-theta (√(2|Θ|/Γ))
# ----------------------------------------------------------------------------
def caso_equilibrio_gt():
    casos = []
    for nome, tipo, S, K, T, r, sig in (
        ("call_atm_r0", "C", 100.0, 100.0, 30 / 252, 0.0, 0.30),
        ("call_atm_r_ln1_1065", "C", 100.0, 100.0, 30 / 252, R_CONT, 0.30),
        ("put_otm_V1_K28", "P", S0, 28.0, DU1 / 252, R_CONT, 0.38),
    ):
        g = gbs(tipo, S, K, T, r, r, sig)
        th1 = g["theta_aa"] / 252
        casos.append({"nome": nome, "tipo": tipo, "S": S, "K": K, "T": T, "r_cont": r, "sigma": sig, "b": r,
                      "gamma": g["gamma"], "theta_aa": g["theta_aa"], "theta_1du": th1,
                      "movimento": math.sqrt(2 * abs(th1) / g["gamma"]),
                      "referencia_S_sigma_raiz_1_252": S * sig / math.sqrt(252),
                      "movimento_5du": math.sqrt(2 * abs(th1 * 5) / g["gamma"])})
    agreg = {}
    for nome, conv in (("V1_convencao_A", "A"), ("V1_tudo_comprado", "+")):
        ss = sel("V1")
        sg = (lambda s: 1.0) if conv == "+" else (lambda s: sinal(s, "A"))
        G = sum(sg(s) * s["g"]["gamma"] * s["oi"] * M for s in ss)
        Th = sum(sg(s) * s["g"]["theta_aa"] / 252 * s["oi"] * M for s in ss)
        ok = G * Th < 0
        w = [sg(s) * s["g"]["gamma"] * s["oi"] * M * S0 * S0 for s in ss]
        pesos_pos = all(wi > 0 for wi in w)
        sig_ef = math.sqrt(sum(wi * s["sigma"] ** 2 for wi, s in zip(w, ss)) / sum(w)) if pesos_pos else None
        mv = math.sqrt(2 * abs(Th) / abs(G)) if ok else None
        agreg[nome] = {"gamma_tot": G, "theta_tot_1du": Th, "movimento": mv,
                       "banda_inf": S0 - mv if mv else None, "banda_sup": S0 + mv if mv else None,
                       "movimento_pct": mv / S0 if mv else None,
                       "sigma_efetiva_ponderada_por_gamma": sig_ef,
                       "referencia_S_sigma_ef_raiz_1_252": S0 * sig_ef / math.sqrt(252) if sig_ef else None,
                       "flags": ([] if ok else ["SINAIS_IGUAIS"]) + ([] if pesos_pos else ["PESOS_COM_SINAIS_MISTOS"])}
    return {
        "descricao": "Movimento de equilíbrio gamma-theta: deslocamento do objeto em que o ganho de gamma de uma posição delta-hedgeada paga o theta do período. Hipótese para a métrica chamada BGT na pesquisa; aqui com nome próprio.",
        "nota_metodologica": NOTAS + "13-bgt-move.md",
        "fontes": [FONTES["wikipedia_bs_equation"]],
        "formula": "mov = √(2·|Θ_δt| / |Γ|), Θ_δt = Θ_aa·h/252 (h em DU); só vale se Γ e Θ tiverem sinais opostos",
        "convencoes": {"theta": "por DU = Θ_aa/252", "horizonte_padrao_du": 1,
                        "agregado": "Γ_tot = Σ s·Γ·OI·m; Θ_tot = Σ s·(Θ/252)·OI·m; bandas = S ± mov",
                        "flag": "SINAIS_IGUAIS quando Γ_tot·Θ_tot ≥ 0 (movimento = null); PESOS_COM_SINAIS_MISTOS quando a vol efetiva ponderada por gamma não faz sentido (sigma_efetiva = null)",
                        "aviso": "com convenção de sinal A o Γ_tot fica pequeno perto do flip e o movimento explode; use o agregado com cuidado"},
        "saidas": {"opcao_isolada": casos, "agregado": agreg},
        "verificacao": {"r0_igual_S_sigma_raiz": abs(casos[0]["movimento"] - casos[0]["referencia_S_sigma_raiz_1_252"]) < 1e-9,
                        "nota_13_r0": 1.889822, "nota_13_r_ln1_1065": 2.160880,
                        "confere_nota_13": abs(casos[0]["movimento"] - 1.889822) < 5e-7 and abs(casos[1]["movimento"] - 2.160880) < 5e-7},
    }


# ----------------------------------------------------------------------------
# 9. Payoff de várias pernas e breakevens (no vencimento)
# ----------------------------------------------------------------------------
def valor_perna(p, ST):
    if p["tipo"] == "ACAO":
        bruto = ST
    elif p["tipo"] == "C":
        bruto = max(ST - p["K"], 0.0)
    else:
        bruto = max(p["K"] - ST, 0.0)
    return p["lado"] * p["qtd"] * (bruto - p["preco"])


def payoff(pernas, ST):
    return sum(valor_perna(p, ST) for p in pernas)


def analisa_payoff(pernas):
    kinks = sorted({p["K"] for p in pernas if p["tipo"] != "ACAO"})
    pts = sorted(set([0.0] + kinks))
    vals = [payoff(pernas, x) for x in pts]
    escala = max([1.0] + [abs(v) for v in vals])
    eps = 1e-9 * escala
    vals = [0.0 if abs(v) < eps else v for v in vals]
    # inclinação analítica depois do último strike (calls e ação valem +1 por unidade)
    incl_dir = sum(p["lado"] * p["qtd"] for p in pernas if p["tipo"] in ("C", "ACAO"))
    incl_ini = sum(p["lado"] * p["qtd"] * (1 if p["tipo"] == "ACAO" else (-1 if p["tipo"] == "P" else 0)) for p in pernas)
    be, zeros = [], []
    for i in range(len(pts) - 1):
        a, b, fa, fb = pts[i], pts[i + 1], vals[i], vals[i + 1]
        if fa == 0 and fb == 0:
            if zeros and zeros[-1][1] == a:
                zeros[-1][1] = b
            else:
                zeros.append([a, b])
        elif fa == 0:
            be.append(a)
        elif fb != 0 and fa * fb < 0:
            be.append(a + (b - a) * (-fa) / (fb - fa))
    xl, vl = pts[-1], vals[-1]
    if vl == 0:
        if incl_dir == 0:
            if zeros and zeros[-1][1] == xl:
                zeros[-1][1] = None
            else:
                zeros.append([xl, None])
        else:
            be.append(xl)
    elif incl_dir != 0 and vl * incl_dir < 0:
        be.append(xl - vl / incl_dir)
    def em_zero(x):
        return any(z[0] <= x <= (z[1] if z[1] is not None else float("inf")) for z in zeros)
    be = sorted(set(round(x, 12) for x in be if not em_zero(x)))
    gmax = max(vals) if incl_dir <= 0 else None
    pmax = min(vals) if incl_dir >= 0 else None
    custo = sum(p["lado"] * p["qtd"] * p["preco"] for p in pernas)
    grade = {f"{x:.0f}": payoff(pernas, float(x)) for x in range(20, 41)}
    flags = []
    if incl_dir > 0:
        flags.append("GANHO_ILIMITADO")
    if incl_dir < 0:
        flags.append("PERDA_ILIMITADA")
    if zeros:
        flags.append("ZERO_EM_INTERVALO")
    return {"breakevens": be, "intervalos_zero": zeros, "ganho_max": gmax, "perda_max": pmax,
            "valor_em_ST_0": vals[0], "inclinacao_acima_do_ultimo_strike": incl_dir,
            "inclinacao_entre_0_e_1o_strike": incl_ini,
            "fluxo_montagem": -custo, "pontos_de_quebra": {f"{x:g}": v for x, v in zip(pts, vals)},
            "grade_20_a_40": grade, "flags": flags}


def P(tipo, K, lado, qtd, preco):
    return {"tipo": tipo, "K": None if tipo == "ACAO" else float(K), "lado": lado, "qtd": qtd, "preco": preco}


def caso_payoff():
    estruturas = {
        "trava_alta_calls": [P("C", 28, +1, 1, 2.40), P("C", 32, -1, 1, 0.45)],
        "borboleta_calls": [P("C", 28, +1, 1, 2.40), P("C", 30, -1, 2, 1.05), P("C", 32, +1, 1, 0.45)],
        "condor_de_ferro_vendido": [P("P", 26, +1, 1, 0.10), P("P", 28, -1, 1, 0.40), P("C", 32, -1, 1, 0.45), P("C", 34, +1, 1, 0.12)],
        "straddle_vendido": [P("C", 30, -1, 1, 1.05), P("P", 30, -1, 1, 0.80)],
        "ratio_calls_1x2": [P("C", 30, +1, 1, 1.05), P("C", 32, -1, 2, 0.45)],
        "venda_coberta_lote_100": [P("ACAO", None, +1, 100, 30.00), P("C", 31, -1, 100, 0.80)],
        "long_collar": [P("ACAO", None, +1, 1, 30.00), P("P", 28, +1, 1, 0.40), P("C", 33, -1, 1, 0.30)],
        "trava_sem_lucro_zero_em_intervalo": [P("C", 30, +1, 1, 2.00), P("C", 32, -1, 1, 0.00)],
    }
    out = {}
    verif = {}
    for nome, pernas in estruturas.items():
        a = analisa_payoff(pernas)
        out[nome] = {"pernas": pernas, "saidas": a}
        # conferência independente: payoff nos breakevens ≈ 0 e contagem de trocas de sinal numa grade fina
        resid = max([abs(payoff(pernas, x)) for x in a["breakevens"]] or [0.0])
        trocas = 0
        prev = None
        for i in range(0, 100001):
            x = i * 0.001
            v = payoff(pernas, x)
            sgn = 0 if abs(v) < 1e-12 else (1 if v > 0 else -1)
            if sgn != 0:
                if prev is not None and sgn != prev:
                    trocas += 1
                prev = sgn
        verif[nome] = {"residuo_max_nos_breakevens": resid, "trocas_de_sinal_grade_0_a_100": trocas}
    return {
        "descricao": "Payoff no vencimento de estruturas de várias pernas (por unidade do objeto, salvo o lote de 100), breakevens exatos, ganho e perda máximos e indicação de ilimitado.",
        "nota_metodologica": NOTAS + "especificacao-motor.md (função payoff) e 14-taxa-estruturas-cdi.md",
        "convencoes": {
            "lado": "+1 comprado, −1 vendido",
            "preco": "prêmio pago (comprado) ou recebido (vendido) por unidade; ação comprada ao preço indicado",
            "payoff": "Σ lado·qtd·(valor_intrínseco(S_T) − preço); ação: lado·qtd·(S_T − preço)",
            "breakeven": "raízes exatas da função linear por partes; quebras só nos strikes; S_T ≥ 0",
            "ganho_max/perda_max": "max/min nos pontos de quebra e em S_T = 0; null quando ilimitado",
            "intervalo_zero": "quando o payoff é 0 num intervalo inteiro, ele vai em 'intervalos_zero' (None = +∞) e não em breakevens",
            "custos": "sem corretagem, emolumentos ou IR",
        },
        "saidas": out,
        "verificacao": verif,
    }


# ----------------------------------------------------------------------------
# 10. Taxa contra o CDI das estruturas
# ----------------------------------------------------------------------------
def book(tipo, K, venc="V1"):
    """bid/ask sintéticos: BS ± 0,01 arredondado para fora (centavos)."""
    v = CADEIA[venc]
    j = v["K"].index(K)
    mid = gbs(tipo, S0, float(K), v["du"] / 252, R_CONT, R_CONT, v["sigma"][j])["preco"]
    bid = max(0.01, math.floor((mid - 0.01) * 100 + 1e-9) / 100)
    ask = math.ceil((mid + 0.01) * 100 - 1e-9) / 100
    return {"mid_bs": mid, "bid": bid, "ask": ask}


S_BID, S_ASK = 29.99, 30.01


def cdi_periodo(du, dc, conv, di=DI_AA):
    if conv == "EXP252_DU":
        return (1 + di) ** (du / 252) - 1
    if conv == "LIN360_DC":
        return di * dc / 360
    if conv == "LIN365_DC":
        return di * dc / 365
    if conv == "EXP365_DC":
        return (1 + di) ** (dc / 365) - 1
    raise ValueError(conv)


CONVS_CDI = ["EXP252_DU", "LIN360_DC", "LIN365_DC", "EXP365_DC"]


def metricas_taxa(r_per, du, dc, di=DI_AA):
    cdi = cdi_periodo(du, dc, "EXP252_DU", di)
    r_aa = (1 + r_per) ** (252 / du) - 1
    return {
        "r_per": r_per, "r_aa": r_aa,
        "cdi_per": cdi,
        "pct_cdi_1_razao": r_per / cdi,
        "pct_cdi_2_estilo_cdb": ((1 + r_per) ** (1 / du) - 1) / ((1 + di) ** (1 / 252) - 1),
        "spread_aa_pp": (r_aa - di) * 100,
        "pct_cdi_1_por_convencao_cdi": {c: r_per / cdi_periodo(du, dc, c, di) for c in CONVS_CDI},
    }


def caso_taxas():
    du, dc = DU1, DC1
    T = du / 252
    cdi_tab = {c: cdi_periodo(du, dc, c) for c in CONVS_CDI}
    estr = {}

    # Venda coberta OTM (K=31) e ITM (K=29)
    for nome, K in (("venda_coberta_otm_K31", 31), ("venda_coberta_itm_K29", 29)):
        c = book("C", K)
        I = S_ASK - c["bid"]
        ve = c["bid"] - max(S_ASK - K, 0.0)
        r_par = ve / I
        r_max = K / I - 1
        estr[nome] = {
            "entradas": {"S_ask": S_ASK, "K": float(K), "C_bid": c["bid"], "du": du, "dc": dc},
            "capital": I, "valor_extrinseco": ve, "protecao_pct": c["bid"] / S_ASK, "breakeven": I,
            "parado": metricas_taxa(r_par, du, dc), "exercida": metricas_taxa(r_max, du, dc),
            "obs": "valor extrínseco medido contra S_ask (preço que se paga pela ação)",
        }

    # Cash put OTM (K=29) e ITM (K=31)
    for nome, K in (("cash_put_otm_K29", 29), ("cash_put_itm_K31", 31)):
        p = book("P", K)
        Pb = p["bid"]
        cdi = cdi_tab["EXP252_DU"]
        ve = Pb - max(K - S_BID, 0.0)
        estr[nome] = {
            "entradas": {"S_bid": S_BID, "K": float(K), "P_bid": Pb, "du": du, "dc": dc},
            "preco_efetivo_compra": K - Pb,
            "valor_extrinseco": ve,
            "capital_K_menos_P": {
                "capital": K - Pb, "caixa_aplicado_no_cdi": float(K),
                "premio": metricas_taxa(Pb / (K - Pb), du, dc),
                "total_nao_exercida": metricas_taxa(K * (1 + cdi) / (K - Pb) - 1, du, dc),
                "parado_extrinseco": metricas_taxa(ve / (K - Pb), du, dc),
            },
            "capital_K": {
                "capital": float(K), "caixa_aplicado_no_cdi": K + Pb,
                "premio": metricas_taxa(Pb / K, du, dc),
                "total_nao_exercida": metricas_taxa((K + Pb) * (1 + cdi) / K - 1, du, dc),
                "aproximacao_soma": Pb / K + cdi,
            },
            "obs": "valor extrínseco medido contra S_bid. 'total' usa o CDI do período em EXP252_DU sobre o caixa aplicado.",
        }

    # Box 3 pontas (K=30)
    K = 30
    pa = book("P", K)["ask"]
    cb = book("C", K)["bid"]
    I = S_ASK + pa - cb
    estr["box3_K30"] = {"entradas": {"S_ask": S_ASK, "K": float(K), "P_ask": pa, "C_bid": cb, "du": du, "dc": dc},
                        "capital": I, "payoff_fixo": float(K), **metricas_taxa(K / I - 1, du, dc),
                        "r_cont_implicita": math.log(K / I) / T}

    # Box 4 pontas (K1=28, K2=32), aplicação e captação, com preços escolhidos à mão
    K1, K2 = 28, 32
    c1 = {"bid": 2.33, "ask": 2.34}
    c2 = {"bid": 0.25, "ask": 0.26}
    p1 = {"bid": 0.21, "ask": 0.22}
    p2 = {"bid": 2.10, "ask": 2.11}

    def box4(c1, c2, p1, p2):
        I_ap = c1["ask"] - c2["bid"] + p2["ask"] - p1["bid"]
        I_cap = c1["bid"] - c2["ask"] + p2["bid"] - p1["ask"]
        res = {"aplicacao": {"capital": I_ap, "payoff_fixo": float(K2 - K1), **metricas_taxa((K2 - K1) / I_ap - 1, du, dc),
                             "r_cont_implicita": math.log((K2 - K1) / I_ap) / T},
               "captacao": {"recebe": I_cap, "paga_no_vencimento": float(K2 - K1), **metricas_taxa((K2 - K1) / I_cap - 1, du, dc),
                            "r_cont_implicita": math.log((K2 - K1) / I_cap) / T}}
        res["flags"] = ["TAXA_NEGATIVA"] if I_ap > K2 - K1 else []
        return res

    estr["box4_K28_K32"] = {
        "entradas": {"C28": c1, "C32": c2, "P28": p1, "P32": p2, "du": du, "dc": dc,
                     "obs": "preços escolhidos à mão, perto do BS da cadeia (box teórico = 3,9824)"},
        **box4(c1, c2, p1, p2),
        "teorico_sem_atrito": (K2 - K1) * math.exp(-R_CONT * T),
    }
    lb = {"C28": book("C", 28), "C32": book("C", 32), "P28": book("P", 28), "P32": book("P", 32)}
    estr["box4_livro_sintetico_taxa_negativa"] = {
        "entradas": {**lb, "du": du, "dc": dc,
                     "obs": "com o livro sintético (BS ± 1 centavo, arredondado para fora), a soma dos spreads passa do valor do box"},
        **box4(lb["C28"], lb["C32"], lb["P28"], lb["P32"]),
    }

    # Long collar (K1=28 put comprada, K2=33 call vendida)
    K1, K2 = 28, 33
    pa = book("P", K1)["ask"]
    cb = book("C", K2)["bid"]
    I = S_ASK + pa - cb
    estr["long_collar_K28_K33"] = {
        "entradas": {"S_ask": S_ASK, "K1": float(K1), "K2": float(K2), "P_ask": pa, "C_bid": cb, "du": du, "dc": dc},
        "capital": I, "perda_max": I - K1, "ganho_max": K2 - I, "breakeven": I,
        "piso": metricas_taxa(K1 / I - 1, du, dc), "teto": metricas_taxa(K2 / I - 1, du, dc),
        "parado": metricas_taxa(min(max(S_ASK, K1), K2) / I - 1, du, dc),
        "payoff_por_analise": analisa_payoff([P("ACAO", None, +1, 1, S_ASK), P("P", K1, +1, 1, pa), P("C", K2, -1, 1, cb)]),
    }

    # vetor da nota 14 (Box 3, DU=21)
    I14 = 30.0 + 1.20 - 1.65
    m14 = metricas_taxa(30.0 / I14 - 1, 21, 30)
    livro = {}
    for venc in ("V1",):
        for K in CADEIA[venc]["K"]:
            livro[f"C{K}"] = book("C", K)
            livro[f"P{K}"] = book("P", K)
    return {
        "descricao": "Taxa contra o CDI de venda coberta, cash put, box de 3 pontas, box de 4 pontas (aplicação e captação) e long collar, a preço executável (compra no ask, venda no bid).",
        "nota_metodologica": NOTAS + "14-taxa-estruturas-cdi.md",
        "fontes": [FONTES["b3_taxas_juros_252"]],
        "convencoes": {
            "data_base": iso(HOJE), "vencimento": iso(VENC1), "du": du, "dc": dc,
            "DI_aa": DI_AA, "S_bid": S_BID, "S_ask": S_ASK,
            "precos_opcoes": "bid/ask sintéticos = preço BS_B3 da cadeia V1 ± R$ 0,01, arredondados para fora (centavos); tabela em 'livro'",
            "r_aa": "(1 + r_per)^(252/DU) − 1",
            "cdi_per_padrao": "EXP252_DU: (1 + DI)^(DU/252) − 1",
            "cdi_per_alternativas": {"LIN360_DC": "DI·DC/360", "LIN365_DC": "DI·DC/365", "EXP365_DC": "(1 + DI)^(DC/365) − 1"},
            "pct_cdi_1": "r_per ÷ CDI_per (razão de retornos do período)",
            "pct_cdi_2": "[(1 + r_per)^(1/DU) − 1] ÷ [(1 + DI)^(1/252) − 1] (estilo CDB)",
            "spread": "(r_aa − DI) em pontos percentuais",
            "liquidacao": "ignora D+1 do prêmio e D+2 da ação (padrão da nota 14)",
            "custos_ir": "desligados",
        },
        "cdi_do_periodo_por_convencao": cdi_tab,
        "livro": livro,
        "saidas": estr,
        "verificacao": {"vetor_nota_14_box3_DU21": {"capital": I14, "r_per": m14["r_per"], "r_aa": m14["r_aa"],
                                                    "pct_cdi_1": m14["pct_cdi_1_razao"], "pct_cdi_2": m14["pct_cdi_2_estilo_cdb"],
                                                    "esperado_nota_14": {"r_per": 0.015228, "r_aa": 0.1989, "pct_cdi_1": 1.798, "pct_cdi_2": 1.792}}},
    }


# ----------------------------------------------------------------------------
# 11. Dias úteis com feriados B3
# ----------------------------------------------------------------------------
def caso_dias_uteis(feriados_json):
    pares = [
        ("hoje_ate_semanal_13nov", D(2026, 11, 4), D(2026, 11, 13)),
        ("hoje_ate_mensal_nov_19nov", D(2026, 11, 4), VENC1),
        ("hoje_ate_mensal_dez_18dez", D(2026, 11, 4), VENC2),
        ("natal_ano_novo", D(2026, 12, 18), D(2027, 1, 15)),
        ("carnaval_2027_com_cinzas", D(2027, 2, 5), D(2027, 2, 19)),
        ("ano_2026_inteiro", D(2025, 12, 31), D(2026, 12, 31)),
        ("ano_2027_inteiro", D(2026, 12, 31), D(2027, 12, 31)),
        ("ano_2028_inteiro", D(2027, 12, 31), D(2028, 12, 31)),
        ("inicio_em_sabado", D(2026, 11, 7), D(2026, 11, 13)),
        ("fim_em_feriado_20nov", D(2026, 11, 13), D(2026, 11, 20)),
        ("mesmo_dia", D(2026, 11, 4), D(2026, 11, 4)),
        ("fim_de_2028_31dez_domingo", D(2028, 12, 22), D(2029, 1, 5)),
    ]
    linhas = []
    for nome, a, b in pares:
        linhas.append({"nome": nome, "d0": iso(a), "d1": iso(b), "dc": (b - a).days,
                       "du_b3_excl_incl": du_entre(a, b, "B3"),
                       "du_b3_incl_excl": du_entre(a, b, "B3", "[d0,d1)"),
                       "du_anbima_excl_incl": du_entre(a, b, "ANBIMA"),
                       "du_anbima_incl_excl": du_entre(a, b, "ANBIMA", "[d0,d1)")})
    venc = {
        "acoes_mensal_2026_11": iso(venc_acao_mensal(2026, 11)),
        "acoes_mensal_2026_12": iso(venc_acao_mensal(2026, 12)),
        "acoes_mensal_2028_04": iso(venc_acao_mensal(2028, 4)),
        "acoes_semanal_sexta_2026_12_25": iso(sessao_anterior_ou_igual(D(2026, 12, 25))),
        "acoes_semanal_sexta_2027_01_01": iso(sessao_anterior_ou_igual(D(2027, 1, 1))),
        "di1_2027_01_primeira_sessao": iso(sessao_seguinte_ou_igual(D(2027, 1, 1))),
    }
    esperado_vencimentos_nota = {
        "acoes_mensal_2026_11": "2026-11-19", "acoes_mensal_2026_12": "2026-12-18",
        "acoes_mensal_2028_04": "2028-04-20", "acoes_semanal_sexta_2026_12_25": "2026-12-23",
        "acoes_semanal_sexta_2027_01_01": "2026-12-30", "di1_2027_01_primeira_sessao": "2027-01-04",
    }
    sem = {str(y): sorted(iso(d) for d in sem_pregao_b3(y)) for y in (2026, 2027, 2028)}
    anb = {str(y): sorted(iso(d) for d in feriados_anbima(y) if d.weekday() < 5) for y in (2026, 2027, 2028)}
    conf = {"json_lido": None, "confere_sem_pregao": None, "confere_anbima": None, "confere_contagens": None, "diferencas": []}
    if feriados_json:
        conf["json_lido"] = feriados_json["_caminho"]
        ok_s = ok_a = ok_n = True
        for y in ("2026", "2027", "2028"):
            ano = feriados_json["anos"][y]
            js = sorted(x["data"] for x in ano["sem_pregao"] if x.get("sem_pregao_b3"))
            ja = sorted(x["data"] for x in ano["sem_pregao"] if x.get("sem_pregao_b3") and not x.get("dia_util_anbima"))
            if js != sem[y]:
                ok_s = False
                conf["diferencas"].append({"ano": y, "campo": "sem_pregao", "json": js, "gerador": sem[y]})
            if ja != anb[y]:
                ok_a = False
                conf["diferencas"].append({"ano": y, "campo": "anbima", "json": ja, "gerador": anb[y]})
            ns = du_entre(D(int(y) - 1, 12, 31), D(int(y), 12, 31), "B3")
            na = du_entre(D(int(y) - 1, 12, 31), D(int(y), 12, 31), "ANBIMA")
            if ns != ano.get("n_sessoes_b3") or na != ano.get("n_dias_uteis_anbima"):
                ok_n = False
                conf["diferencas"].append({"ano": y, "campo": "contagens", "json": [ano.get("n_sessoes_b3"), ano.get("n_dias_uteis_anbima")], "gerador": [ns, na]})
        conf.update({"confere_sem_pregao": ok_s, "confere_anbima": ok_a, "confere_contagens": ok_n})
    return {
        "descricao": "Contagem de dias úteis entre datas pelo calendário de pregões da B3 e pelo calendário ANBIMA (24/12 e 31/12 contam como úteis), nas duas regras de borda; datas de vencimento ajustadas por feriado.",
        "nota_metodologica": NOTAS_B3 + "07-feriados-calendario.md e vencimentos-regras.md",
        "fontes": [FONTES["b3_calendario_2026"], FONTES["b3_oc007_2026_vencimentos"], FONTES["anbima_feriados"].format(ano="2027"),
                   FONTES["anbima_feriados"].format(ano="2028"), FONTES["b3_manual_curvas"]],
        "convencoes": {
            "padrao_opcoes": "du_b3_excl_incl: exclui d0, inclui d1 (dias de pregão restantes depois de hoje até o vencimento)",
            "di1": "du_anbima_incl_excl: inclui a data da operação e exclui o vencimento (OC 055/2024-PRE); igual à anterior quando d0 e d1 são úteis",
            "curva_di": "calendário ANBIMA (Manual de Curvas da B3)",
            "status_anos": {"2026": "oficial (B3)", "2027": "derivado", "2028": "derivado"},
            "regras": ["feriados nacionais + Carnaval (seg e ter) + Sexta-feira Santa + Corpus Christi; 20/11 desde 2024",
                       "B3 sem pregão também em 24/12 e no último dia útil do ano (31/12 ou a sexta anterior se cair em fim de semana)",
                       "Quarta-feira de Cinzas é dia útil (abertura às 13h)",
                       "25/01 e 09/07 (São Paulo) têm pregão normal"],
            "pendencia": "errata OC 041/2026-VNC não lida (pode alterar o 2º semestre de 2026)",
        },
        "saidas": {"pares": linhas, "vencimentos": venc, "sem_pregao_b3_dias_de_semana": sem, "feriados_anbima_dias_de_semana": anb},
        "verificacao": {"vencimentos_iguais_a_nota": venc == esperado_vencimentos_nota, "esperado_nota": esperado_vencimentos_nota,
                        "conferencia_com_json_do_projeto": conf},
    }


# ----------------------------------------------------------------------------
# 12. Curva DI: interpolação flat-forward 252
# ----------------------------------------------------------------------------
def ff252(curva, du):
    """curva: lista ordenada de (du, taxa a.a.). Antes do 1º vértice: taxa do 1º vértice.
    Depois do último: flat forward com o penúltimo e o último vértices."""
    if du <= 0:
        return None
    if du <= curva[0][0]:
        return curva[0][1]
    for (da, ia), (dp, ip) in zip(curva, curva[1:]):
        if da <= du <= dp:
            break
    else:
        (da, ia), (dp, ip) = curva[-2], curva[-1]
    fa = (1 + ia) ** (da / 252)
    fp = (1 + ip) ** (dp / 252)
    f = fa * (fp / fa) ** ((du - da) / (dp - da))
    return f ** (252 / du) - 1


def ff252_log(curva, du):
    """Implementação independente: interpolação linear de ln(fator) em DU."""
    if du <= curva[0][0]:
        return curva[0][1]
    pts = [(d, (d / 252) * math.log1p(i)) for d, i in curva]
    if du >= pts[-1][0]:
        (a, la), (b, lb) = pts[-2], pts[-1]
    else:
        j = max(k for k in range(len(pts)) if pts[k][0] <= du)
        (a, la), (b, lb) = pts[j], pts[min(j + 1, len(pts) - 1)]
        if a == b:
            return math.expm1(la * 252 / du)
    l = la + (lb - la) * (du - a) / (b - a)
    return math.expm1(l * 252 / du)


def caso_curva_di():
    base = HOJE
    venc_di1 = {"DI1F27": D(2027, 1, 1), "DI1G27": D(2027, 2, 1), "DI1J27": D(2027, 4, 1),
                "DI1N27": D(2027, 7, 1), "DI1F28": D(2028, 1, 1)}
    taxas = {"DI1F27": 0.1070, "DI1G27": 0.1075, "DI1J27": 0.1090, "DI1N27": 0.1110, "DI1F28": 0.1150}
    vert = [{"nome": "CDI", "vencimento": None, "du": 1, "taxa_aa": DI_AA}]
    for k, d in venc_di1.items():
        v = sessao_seguinte_ou_igual(d, "B3")
        du = du_entre(base, v, "ANBIMA", "[d0,d1)")
        vert.append({"nome": k, "vencimento": iso(v), "du": du, "taxa_aa": taxas[k],
                     "pu": 100000 / (1 + taxas[k]) ** (du / 252)})
    curva = [(x["du"], x["taxa_aa"]) for x in vert]
    pontos = sorted(set([1, 5, DU1, 21, DU2, 40, 63, 100, 126, 252, 300, 400] + [x["du"] for x in vert]))
    saida = []
    for du in pontos:
        i1 = ff252(curva, du)
        i2 = ff252_log(curva, du)
        saida.append({"du": du, "taxa_aa": i1, "fator": (1 + i1) ** (du / 252),
                      "fator_desconto": (1 + i1) ** (-du / 252), "r_cont": math.log1p(i1),
                      "pu_100000": 100000 / (1 + i1) ** (du / 252),
                      "extrapolado": du > curva[-1][0], "dif_impl_independente": abs(i1 - i2)})
    # forwards entre vértices e conferência de forward constante dentro do intervalo
    fwd = []
    for (da, ia), (dp, ip) in zip(curva, curva[1:]):
        f = ((1 + ip) ** (dp / 252) / (1 + ia) ** (da / 252)) ** (252 / (dp - da)) - 1
        meio = (da + dp) // 2
        im = ff252(curva, meio)
        f_meio = ((1 + im) ** (meio / 252) / (1 + ia) ** (da / 252)) ** (252 / (meio - da)) - 1 if meio > da else f
        fwd.append({"de_du": da, "ate_du": dp, "forward_aa": f, "du_meio": meio, "forward_ate_o_meio": f_meio,
                    "constante": abs(f - f_meio) < 1e-12})
    return {
        "descricao": "Interpolação exponencial (flat forward 252) da curva pré a partir do CDI (vértice de 1 DU) e de ajustes sintéticos do DI1; extrapolação depois do último vértice com o penúltimo e o último; PU do DI1.",
        "nota_metodologica": NOTAS_B3 + "01-curva-de-juros.md e " + NOTAS + "01-convencoes-base.md §3",
        "fontes": [FONTES["b3_manual_curvas"], FONTES["b3_di1_oc055_2024"], FONTES["b3_manual_aprecamento_opcoes"]],
        "convencoes": {
            "data_base": iso(base),
            "du": "calendário ANBIMA; DI1: data-base inclusive até o vencimento exclusive",
            "vencimento_di1": "1ª sessão B3 do mês",
            "formula": "f(DU) = (1+i_a)^(DU_a/252)·[(1+i_p)^(DU_p/252)/(1+i_a)^(DU_a/252)]^((DU−DU_a)/(DU_p−DU_a)); taxa = f^(252/DU) − 1",
            "antes_do_1o_vertice": "taxa do 1º vértice (CDI)",
            "depois_do_ultimo": "flat forward com penúltimo e último vértices (Manual de Curvas, item 1.4.2)",
            "pu": "PU = 100.000 / (1 + i)^(DU/252)",
            "taxas": "sintéticas",
        },
        "entradas": {"vertices": vert},
        "saidas": {"pontos": saida, "forwards": fwd},
        "verificacao": {"max_dif_implementacao_independente": max(p["dif_impl_independente"] for p in saida),
                        "forwards_constantes": all(f["constante"] for f in fwd),
                        "vertices_reproduzidos": all(abs(ff252(curva, x["du"]) - x["taxa_aa"]) < 1e-14 for x in vert)},
    }


# ----------------------------------------------------------------------------
# Saída
# ----------------------------------------------------------------------------
def limpa(o):
    if isinstance(o, float):
        if math.isnan(o) or math.isinf(o):
            return None
        return o
    if isinstance(o, dict):
        return {str(k): limpa(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpa(v) for v in o]
    if isinstance(o, dt.date):
        return o.isoformat()
    return o


def gera(feriados_json):
    casos = {
        "cadeia": {"descricao": "Cadeia sintética usada pelos casos 1 a 8. Objeto SINT3 (inventado), S = 30,00; descoberto = OI − coberto − travado.",
                   "data_base": iso(HOJE), "S": S0, "DI_aa": DI_AA, "r_cont": R_CONT, "multiplicador": M,
                   "V1": tabela_entrada("V1"), "V2": tabela_entrada("V2")},
        "max_pain": caso_max_pain(),
        "pcr": caso_pcr(),
        "iq": caso_iq(),
        "quebra_oi": caso_quebra_oi(),
        "gex_dex": caso_gex_dex(),
        "gamma_flip": caso_flip(),
        "walls": caso_walls(),
        "equilibrio_gamma_theta": caso_equilibrio_gt(),
        "payoff": caso_payoff(),
        "taxas_cdi": caso_taxas(),
        "dias_uteis": caso_dias_uteis(feriados_json),
        "curva_di": caso_curva_di(),
    }
    conf = conferencias(casos)
    doc = {
        "titulo": "Vetores de teste: agregados, exposições, níveis e estruturas",
        "conferencias": conf,
        "versao": VERSAO,
        "data_acesso_fontes": DATA_ACESSO,
        "gerado_por": "geradores/gerar_agregados.py (python3 -I, só biblioteca padrão)",
        "dados": "todos sintéticos; nenhum número vem de tela de terceiros",
        "tolerancia": {
            "aritmetica_exata": "Max Pain, PCR, IQ, quebra do OI, payoff, contagem de DU: igualdade (ou 1e-12)",
            "depende_de_N_x": "gregas, GEX, DEX, flip, taxas com preço BS: relativa 1e-9 (exige N(x) com precisão de máquina, ex. erfc)",
        },
        "legenda": "[C] confirmado em fonte; [I] inferência; [S] suposição a testar; [P] proposta de convenção",
        "casos": casos,
    }
    return limpa(doc)


def conferencias(c):
    """Junta as conferências independentes num só lugar (True = passou)."""
    v = {}
    v["max_pain_condicao_1a_ordem_e_grade_fina"] = c["max_pain"]["verificacao"]["confere"]
    v["pcr_todos_razao_de_somas"] = all(c["pcr"]["verificacao"].values())
    g = c["gex_dex"]["verificacao"]
    v["gregas_vs_diferencas_finitas"] = (g["erro_rel_max_gamma_vs_diferencas_finitas"] < 1e-5
                                         and g["erro_abs_max_delta_vs_diferencas_finitas"] < 1e-6
                                         and g["erro_abs_max_theta_vs_diferencas_finitas"] < 1e-6)
    v["gamma_nota_05"] = g["confere_nota_05"]
    f = c["gamma_flip"]["verificacao"]
    v["flip_brent_vs_bissecao"] = f["brent_vs_bissecao_max_dif"] < 1e-9 and f["G_na_raiz_max_abs"] < 1e-6
    v["equilibrio_gamma_theta_nota_13"] = c["equilibrio_gamma_theta"]["verificacao"]["confere_nota_13"] and c["equilibrio_gamma_theta"]["verificacao"]["r0_igual_S_sigma_raiz"]
    pv = c["payoff"]["verificacao"]
    v["payoff_breakevens"] = all(pv[k]["residuo_max_nos_breakevens"] < 1e-9 and
                                 pv[k]["trocas_de_sinal_grade_0_a_100"] == len(c["payoff"]["saidas"][k]["saidas"]["breakevens"])
                                 for k in pv)
    t = c["taxas_cdi"]["verificacao"]["vetor_nota_14_box3_DU21"]
    e = t["esperado_nota_14"]
    v["box3_nota_14"] = (abs(t["r_per"] - e["r_per"]) < 5e-7 and abs(t["r_aa"] - e["r_aa"]) < 5e-5
                         and abs(t["pct_cdi_1"] - e["pct_cdi_1"]) < 5e-4 and abs(t["pct_cdi_2"] - e["pct_cdi_2"]) < 5e-4)
    d = c["dias_uteis"]["verificacao"]
    cj = d["conferencia_com_json_do_projeto"]
    v["vencimentos_vs_nota"] = d["vencimentos_iguais_a_nota"]
    v["feriados_vs_json_do_projeto"] = (None if cj["json_lido"] is None else
                                        bool(cj["confere_sem_pregao"] and cj["confere_anbima"] and cj["confere_contagens"]))
    cv = c["curva_di"]["verificacao"]
    v["curva_di_impl_independente"] = cv["max_dif_implementacao_independente"] < 1e-12 and cv["forwards_constantes"] and cv["vertices_reproduzidos"]
    v["todas"] = all(x for x in v.values() if x is not None)
    return v


def carrega_feriados(caminho):
    if not caminho or not os.path.isfile(caminho):
        return None
    with open(caminho, encoding="utf-8") as f:
        d = json.load(f)
    d["_caminho"] = caminho
    return d


def br(x, n=2, sinal=False):
    if x is None:
        return "—"
    if isinstance(x, bool):
        return "sim" if x else "não"
    if isinstance(x, int) and n == 0:
        t = f"{x:+,d}" if sinal else f"{x:,d}"
    else:
        t = f"{x:+,.{n}f}" if sinal else f"{x:,.{n}f}"
    return t.replace(",", "§").replace(".", ",").replace("§", ".")


def sci(x):
    return f"{x:.1e}".replace(".", ",")


def pct(x, n=4):
    return "—" if x is None else br(100 * x, n) + " %"


def tabela(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    for l in linhas:
        out.append("| " + " | ".join(str(c) for c in l) + " |")
    return out


def render_md(doc):
    c = doc["casos"]
    L = []
    a = L.append
    a("# Vetores de teste: agregados, exposições, níveis e estruturas")
    a("")
    a(f"- **Data:** {doc['data_acesso_fontes']} (data de acesso de todas as fontes citadas; nenhuma página nova foi aberta para gerar estes vetores).")
    a("- **Pasta:** `/mnt/project-files/jumba/vetores/`. Arquivos: `agregados.json` (todos os números, precisão total), este `agregados.md` (resumo legível) e `geradores/gerar_agregados.py`.")
    a("- **Como regenerar:** `python3 -I geradores/gerar_agregados.py` (só biblioteca padrão). O gerador lê, só para conferência, o JSON de feriados de `../conhecimento/b3-outros/`.")
    a("- **Dados:** todos **sintéticos**. Objeto inventado SINT3, S = 30,00, data-base 04/11/2026. Nenhum número vem de tela de terceiros.")
    a("- **Legenda:** [C] confirmado em fonte; [I] inferência; [S] suposição a testar; [P] proposta de convenção (decisão do Marcelo).")
    a("- **Tolerância sugerida nos testes:** igualdade (ou 1e-12) para Max Pain, PCR, IQ, quebra do OI, payoff e contagem de dias úteis; relativa 1e-9 para tudo que passa por N(x) (gregas, GEX, DEX, flip, preços BS). Isso exige N(x) com precisão de máquina (por exemplo, via `erfc`), não a aproximação polinomial de 7 casas.")
    a("- **Metodologia:** as fórmulas vêm das notas `../conhecimento/metodologia/` (01, 05, 08 a 14 e `especificacao-motor.md`) e `../conhecimento/b3-outros/` (curva, feriados e vencimentos). Cada caso do JSON aponta a nota e as URLs de origem.")
    a("")
    a("## Estrutura do JSON")
    a("")
    a("`casos.<nome>` tem sempre `descricao`, `nota_metodologica`, `fontes` (URLs), `convencoes`, `saidas` e, quando houve conferência independente, `verificacao`. O bloco `casos.cadeia` traz a cadeia sintética usada pelos casos 1 a 8.")
    a("")
    # resumo
    mp = c["max_pain"]["saidas"]
    pc = c["pcr"]["saidas"]
    gx = c["gex_dex"]["saidas"]["agregados"]
    fl = c["gamma_flip"]["saidas"]
    wl = c["walls"]["saidas"]["regras"]
    eq = c["equilibrio_gamma_theta"]["saidas"]
    tx = c["taxas_cdi"]["saidas"]
    du = c["dias_uteis"]
    cv = c["curva_di"]
    a("## Resumo dos casos")
    a("")
    linhas = [
        ["1", "`max_pain`", "Max Pain A (intrínseco) e B (contagem ITM), 10 strikes; empate", f"A = {br(mp['max_pain_a'],0)}, B = {br(mp['max_pain_b'],0)} (divergem de propósito)", "condição de 1ª ordem e grade fina"],
        ["2", "`pcr`", "PCR por OI, volume, financeiro, descoberto e delta; V1, V2 e TODOS; sem calls", f"V1 OI {br(pc['V1']['oi']['pcr'],4)}, vol {br(pc['V1']['vol']['pcr'],4)}", "TODOS = razão de somas"],
        ["3", "`iq`", "IQ por série e agregado (3 formas), global, barreiras", f"V1 calls {br(c['iq']['saidas']['V1']['calls']['razao_somas'],4)}, puts {br(c['iq']['saidas']['V1']['puts']['razao_somas'],4)}", "—"],
        ["4", "`quebra_oi`", "Total = Coberto + Travado + Descoberto; bordas", "identidade fecha em todas as séries do V1", "—"],
        ["5", "`gex_dex`", "GEX (3 unidades) e DEX por série, strike, acumulado e total; sinais A, B e D", f"GEX V1 (A) = R$ {br(gx['PROXIMO_V1']['A']['gex_total_u3'],2)} por 1 %", "Γ, Δ e Θ por diferenças finitas; vetor da nota 05"],
        ["6", "`gamma_flip`", "Flip por varredura (M1) e por acumulado (M2)", f"V1: M1 {br(fl['PROXIMO_V1']['M1_varredura']['flip_principal'],4)}; M2 {br(fl['PROXIMO_V1']['M2_acumulado']['flip'],4)}", "Brent × bissecção"],
        ["7", "`walls`", "Call e put wall por 3 regras e 2 lados", f"regra a: call {br(wl['a_gamma_nocional']['livre']['call_wall'],0)}, put {br(wl['a_gamma_nocional']['livre']['put_wall'],0)}", "—"],
        ["8", "`equilibrio_gamma_theta`", "√(2|Θ|/Γ) isolado e agregado (hipótese do BGT)", f"r = 0: {br(eq['opcao_isolada'][0]['movimento'],6)} = Sσ/√252", "vetor da nota 13"],
        ["9", "`payoff`", "8 estruturas: breakevens, máximos, ilimitado, zero em intervalo", "ver tabela", "resíduo nos breakevens e trocas de sinal"],
        ["10", "`taxas_cdi`", "Venda coberta, cash put, box 3, box 4, long collar contra o CDI", f"box 3: {pct(tx['box3_K30']['pct_cdi_1_razao'],2)} do CDI", "vetor da nota 14"],
        ["11", "`dias_uteis`", "DU B3 e ANBIMA, duas regras de borda, vencimentos", "2026: 247 pregões, 249 DU ANBIMA", "JSON de feriados do projeto e tabela de vencimentos"],
        ["12", "`curva_di`", "Flat forward 252, extrapolação, PU do DI1", f"DU 11: {pct(cv['saidas']['pontos'][2]['taxa_aa'],6)} a.a.", "interpolação de ln(fator) e forward constante"],
    ]
    L += tabela(["#", "Caso", "O que testa", "Resultado-chave", "Conferência independente"], linhas)
    a("")
    cf_ = doc["conferencias"]
    if cf_["todas"]:
        a(f"Todas as {len(cf_) - 1} conferências independentes passaram (`conferencias` no topo do JSON; detalhes em `verificacao` de cada caso).")
    else:
        a("**Atenção: conferências que falharam:** " + ", ".join(k for k, x in cf_.items() if x is False and k != "todas") + ".")
    a("")
    a("## Convenções que precisei escolher [P]")
    a("")
    for t in [
        "**Prazo das opções:** T = DU/252, com DU pelo calendário de **pregões da B3**, excluindo a data-base e incluindo o vencimento. A curva DI usa o calendário **ANBIMA** (24/12 e 31/12 contam como úteis). Para buscar a taxa da curva no vencimento de uma opção, conte o DU ANBIMA até a data do vencimento; para o T da opção, conte o DU B3. Em novembro os dois coincidem.",
        "**Taxa:** DI sintético de 10,65 % a.a. (base 252) em todos os casos, igual às notas 05 e 14, para os vetores se conferirem entre si. r = ln(1 + DI).",
        "**Modelo:** BS sem dividendos (b = r), convenção B3 para ações protegidas.",
        "**Sinal da GEX/DEX:** padrão **A** (formador comprado em calls, +1; vendido em puts, −1). Também gerei B (−1 em tudo) e D (heurística coberto/descoberto, θc = 1, θb = 0, θu = 1, sem fonte). Leitura: GEX > 0 amortece; GEX < 0 acelera.",
        "**Unidade da GEX:** U3 = s·Γ·OI·m·S²·0,01 (R$ de delta por movimento de 1 %). U1 e U2 também vão no JSON. DEX em R$ = s·Δ·OI·m·S; hedge do formador = −DEX.",
        "**Flip:** principal = raiz de G(X) mais próxima de S (M1, sticky strike, grade 0,70·S a 1,30·S com passo de 0,25 %). M2 interpola o acumulado por strike, somado do menor strike para o maior. Os dois **não** são equivalentes e o vetor mostra isso.",
        "**Walls:** padrão regra a (maior gamma nocional por tipo), lado livre; desempate pelo strike mais próximo de S.",
        "**Max Pain:** só nos strikes listados; ATM não conta como ITM; empate → strike mais próximo de S, depois o menor.",
        "**PCR TODOS e IQ agregado:** razão de somas (não média de razões). Denominador zero → `null` com flag.",
        "**IQ:** séries sem lançador ficam fora do agregado (flag `SEM_LANCADOR`). Barreiras com limiar escalado para a cadeia sintética (5.000, não 5 milhões).",
        "**Quebra do OI:** nas puts sintéticas o coberto é 0. Se a soma não fechar, não corrigir: marcar `SOMA_DIVERGE`. Falta testar no arquivo real se o total certo é `OpnIntrst` ou `TtlPos`.",
        "**Movimento gamma-theta:** Θ por DU (Θ/252), horizonte de 1 DU; nome próprio (a sigla BGT é hipótese). Com sinal A o Γ total encolhe perto do flip e o movimento explode; o agregado \"tudo comprado\" é o mais estável.",
        "**Payoff:** por unidade (salvo a venda coberta em lote de 100), sem custos; intervalo de payoff zero vai em `intervalos_zero`, não em breakevens; ganho ou perda ilimitados viram `null` com flag.",
        "**Taxas contra o CDI:** preço executável (compra no ask, venda no bid). Livro sintético = preço BS ± R$ 0,01, arredondado para fora; o box 4 usa preços à mão, porque com esse livro a soma dos spreads passa do valor do box (há um caso de borda mostrando a taxa negativa). CDI do período padrão = (1 + DI)^(DU/252) − 1; também calculo LIN360_DC, LIN365_DC e EXP365_DC. Cash put com capital K − P (padrão) e K (alternativa); o \"total\" aplica o CDI sobre todo o caixa. Liquidação D+1/D+2 ignorada.",
        "**Curva DI:** antes do 1º vértice vale a taxa do 1º vértice (CDI); depois do último, flat forward com o penúltimo e o último (Manual de Curvas da B3). Vencimento do DI1 = 1ª sessão do mês; DU do DI1 = data-base inclusive até o vencimento exclusive.",
    ]:
        a("- " + t)
    a("")

    # 0. cadeia
    a("## 0. Cadeia sintética (entrada dos casos 1 a 8)")
    a("")
    cad = c["cadeia"]
    a(f"S = {br(cad['S'],2)}; DI = {pct(cad['DI_aa'],2)} a.a.; r = {br(cad['r_cont'],6)}; V1 vence em {cad['V1']['vencimento']} ({cad['V1']['du']} DU, {cad['V1']['dc']} DC; a 3ª sexta, 20/11, é feriado); V2 vence em {cad['V2']['vencimento']} ({cad['V2']['du']} DU, {cad['V2']['dc']} DC).")
    a("")
    for vk in ("V1", "V2"):
        a(f"**{vk}**")
        a("")
        ls = []
        for s in cad[vk]["series"]:
            ls.append([s["tipo"], br(s["K"], 0), pct(s["sigma"], 1), br(s["oi"], 0), br(s["cvrd"], 0), br(s["blck"], 0), br(s["ucvrd"], 0),
                       br(s["titulares"], 0), br(s["lancadores"], 0), br(s["qtd_dia"], 0), br(s["preco_medio"], 2)])
        L.extend(tabela(["Tipo", "K", "σ", "OI", "Coberto", "Travado", "Descoberto", "Titulares", "Lançadores", "Qtd dia", "Preço médio"], ls))
        a("")

    # 1 max pain
    m = c["max_pain"]
    a("## 1. Max Pain (V1)")
    a("")
    a(f"Fonte: {m['nota_metodologica']}; {m['fontes'][0]} (acesso 2026-11-04).")
    a("")
    L.extend(tabela(["X", "Dor (R$)", "ITM (contratos)", "Dor'₋", "Dor'₊"],
                    [[br(l["X"], 0), br(l["dor_rs"], 0, False) if isinstance(l["dor_rs"], int) else br(l["dor_rs"], 0), br(l["itm_contratos"], 0), br(l["derivada_esq"], 0), br(l["derivada_dir"], 0)] for l in m["saidas"]["tabela"]]))
    a("")
    a(f"- **Método A = {br(m['saidas']['max_pain_a'],0)}**, **método B = {br(m['saidas']['max_pain_b'],0)}**. Divergem porque o OI de calls em 30 (4.000) é menor que o de puts em 31 (6.000): B anda para 31, mas o acumulado de calls até 30 (11.300) já passa o de puts acima de 30 (9.900), e A fica em 30.")
    e = m["caso_empate_b"]
    a(f"- **Empate no B:** com S = {br(e['S'],1)}, os strikes {', '.join(br(x,0) for x in e['candidatos_b'])} empatam com {br(min(e['itm'].values()),0)} contratos ITM; o mais próximo de S é **{br(e['max_pain_b'],0)}**. O A dá {br(e['max_pain_a'],0)}.")
    a("")

    # 2 pcr
    a("## 2. Put/Call Ratio")
    a("")
    a(f"Fonte: {c['pcr']['nota_metodologica']}; {c['pcr']['fontes'][0]} (acesso 2026-11-04).")
    a("")
    ls = []
    for k in ("V1", "V2", "TODOS"):
        b = pc[k]
        ls.append([k, br(b["oi"]["pcr"], 6), br(b["vol"]["pcr"], 6), br(b["fin"]["pcr"], 6), br(b["desc"]["pcr"], 6), br(b["delta"]["pcr"], 6)])
    L.extend(tabela(["Recorte", "OI", "Volume", "Financeiro", "Descoberto", "Delta"], ls))
    a("")
    sz = c["pcr"]["caso_sem_calls"]["saidas"]
    a(f"- TODOS é Σ puts ÷ Σ calls; a média simples das razões de V1 e V2 daria outro número. Caso sem volume de calls: PCR por volume = `null` com `SEM_CALLS`; por OI = {br(sz['oi']['pcr'],2)}.")
    a("")

    # 3 iq
    iq = c["iq"]["saidas"]
    a("## 3. Índice de Qualidade (IQ)")
    a("")
    a(f"Fonte: {c['iq']['nota_metodologica']}; {c['iq']['fontes'][0]} (acesso 2026-11-04). Dependência de dado: {c['iq']['dependencia_de_dado']}")
    a("")
    ls = []
    for k in ("V1", "V2", "GLOBAL"):
        for t, nome in (("calls", "calls"), ("puts", "puts")):
            b = iq[k][t]
            ls.append([k, nome, br(b["razao_somas"], 6), br(b["pond_oi"], 6), br(b["pond_desc"], 6), ", ".join(b["excluidas_sem_lancador"]) or "—"])
    L.extend(tabela(["Recorte", "Tipo", "Razão de somas (padrão)", "Ponderado por OI", "Ponderado por descoberto", "Fora (sem lançador)"], ls))
    a("")
    a("Barreiras (descoberto ≥ 5.000, IQ ≥ 1,2, |K/S − 1| ≤ 10 %): " + "; ".join(f"{b['id']} (IQ {br(b['iq'],4)}, {pct(b['dist_pct'],2)})" for b in iq["barreiras"]) + ".")
    a("")

    # 4 quebra
    q = c["quebra_oi"]["saidas"]
    a("## 4. Total = Coberto + Travado + Descoberto")
    a("")
    L.extend(tabela(["Tipo (V1)", "OI", "Coberto", "Travado", "Descoberto", "% descoberto", "Fecha?"],
                    [[t, br(v["oi"], 0), br(v["cvrd"], 0), br(v["blck"], 0), br(v["ucvrd"], 0), pct(v["pct_descoberto"], 2), br(v["confere"])] for t, v in q["por_tipo"].items()]))
    a("")
    for e in q["especiais"]:
        a(f"- `{e['id']}`: {e['regra']} (flags: {', '.join(e['flags']) or 'nenhuma'}).")
    a("")

    # 5 gex
    g = c["gex_dex"]
    a("## 5. GEX e DEX")
    a("")
    a(f"Fonte: {g['nota_metodologica']}; {', '.join(g['fontes'])} (acesso 2026-11-04).")
    a("")
    a("**Convenção de sinal explícita:** A (padrão): calls +1, puts −1. B: −1 em tudo. D: s = (coberto − descoberto)/OI. GEX em R$ por 1 % (U3).")
    a("")
    ks = list(gx["PROXIMO_V1"]["A"]["gex_strike_u3"].keys())
    ls = []
    for k in ks:
        ls.append([br(float(k), 0), br(gx["PROXIMO_V1"]["A"]["gex_strike_u3"][k], 2), br(gx["PROXIMO_V1"]["A"]["gex_acumulado_u3"][k], 2),
                   br(gx["PROXIMO_V1"]["B"]["gex_strike_u3"][k], 2), br(gx["PROXIMO_V1"]["D"]["gex_strike_u3"][k], 2), br(gx["PROXIMO_V1"]["A"]["dex_strike_rs"][k], 2)])
    L.extend(tabela(["K", "GEX A", "Acumulado A", "GEX B", "GEX D", "DEX A (R$)"], ls))
    a("")
    ls = []
    for f in ("PROXIMO_V1", "TODOS"):
        for conv in ("A", "B", "D"):
            b = gx[f][conv]
            ls.append([f, conv, br(b["gex_total_u3"], 2), br(b["gex_total_u1"], 4), br(b["dex_total_rs"], 2), br(b["hedge_formador_rs"], 2), br(b["dex_atm_2pct_rs"], 2), br(b["dex_atm_5pct_rs"], 2), b["regime_no_spot"]])
    L.extend(tabela(["Filtro", "Sinal", "GEX total (R$/1 %)", "GEX total (ações/R$1)", "DEX total (R$)", "Hedge (R$)", "DEX ATM ±2 %", "DEX ATM ±5 %", "Regime"], ls))
    a("")
    v = g["verificacao"]
    a(f"Conferência: erro relativo máximo do Γ contra diferenças finitas = {sci(v['erro_rel_max_gamma_vs_diferencas_finitas'])}; Γ da nota 05 (S=30, K=32, DU=21) = {br(v['vetor_nota_05_gamma_call_S30_K32_DU21'],6)} (esperado 0,115873).")
    a("")

    # 6 flip
    a("## 6. Gamma flip (sinal A)")
    a("")
    ls = []
    for f in ("PROXIMO_V1", "TODOS"):
        m1, m2 = fl[f]["M1_varredura"], fl[f]["M2_acumulado"]
        ls.append([f, br(m1["flip_principal"], 6), str(len(m1["raizes"])), m1["regime"], br(m1["G_no_spot"], 2), br(m2["flip"], 6), br(m1["x_min_grade"], 3), br(m1["x_max_grade"], 3)])
    L.extend(tabela(["Filtro", "Flip M1", "Raízes", "Regime", "G(S) R$/1 %", "Flip M2", "X do mínimo de G", "X do máximo de G"], ls))
    a("")
    a(f"- Sem flip: só as calls do V1 dão G(X) > 0 na grade toda → `SEM_FLIP`. Diferença máxima Brent × bissecção: {sci(c['gamma_flip']['verificacao']['brent_vs_bissecao_max_dif'])}.")
    a("- M1 e M2 dão níveis muito diferentes (cerca de 29,8 contra 33): o M2 depende de onde a soma começa e não recalcula Γ. Esse contraste é parte do vetor.")
    a("")

    # 7 walls
    a("## 7. Call wall e put wall (V1)")
    a("")
    ls = []
    for r_, nome in (("a_gamma_nocional", "a: gamma nocional (padrão)"), ("b_oi", "b: maior OI"), ("c_gex_com_sinal_A", "c: GEX com sinal (A)")):
        ls.append([nome, br(wl[r_]["livre"]["call_wall"], 0), br(wl[r_]["livre"]["put_wall"], 0), br(wl[r_]["restrito"]["call_wall"], 0), br(wl[r_]["restrito"]["put_wall"], 0)])
    L.extend(tabela(["Regra", "Call wall (livre)", "Put wall (livre)", "Call wall (K ≥ S)", "Put wall (K ≤ S)"], ls))
    a("")
    cl = c["walls"]["caso_lado_restrito"]
    a(f"- Mini-cadeia em que o lado importa: livre → call {br(cl['livre']['call_wall'],0)}, put {br(cl['livre']['put_wall'],0)}; restrito → call {br(cl['restrito']['call_wall'],0)}, put {br(cl['restrito']['put_wall'],0)}.")
    a("")

    # 8 equilibrio
    a("## 8. Movimento de equilíbrio gamma-theta, √(2|Θ|/Γ)")
    a("")
    ls = []
    for x in eq["opcao_isolada"]:
        ls.append([x["nome"], br(x["gamma"], 6), br(x["theta_1du"], 6), br(x["movimento"], 6), br(x["referencia_S_sigma_raiz_1_252"], 6), br(x["movimento_5du"], 6)])
    L.extend(tabela(["Caso", "Γ", "Θ por DU", "Movimento (1 DU)", "S·σ/√252", "Movimento (5 DU)"], ls))
    a("")
    ls = []
    for k, x in eq["agregado"].items():
        ls.append([k, br(x["gamma_tot"], 4), br(x["theta_tot_1du"], 4), br(x["movimento"], 6), f"{br(x['banda_inf'],4)} a {br(x['banda_sup'],4)}", ", ".join(x["flags"]) or "—"])
    L.extend(tabela(["Agregado V1", "Γ total", "Θ total por DU", "Movimento", "Bandas", "Flags"], ls))
    a("")

    # 9 payoff
    a("## 9. Payoff de várias pernas (no vencimento)")
    a("")
    ls = []
    for k, x in c["payoff"]["saidas"].items():
        s_ = x["saidas"]
        pernas = " ".join(f"{'+' if p['lado']>0 else '−'}{p['qtd'] if p['qtd']!=1 else ''}{p['tipo'] if p['tipo']!='ACAO' else 'ação'}{br(p['K'],0) if p['K'] is not None else ''}@{br(p['preco'],2)}" for p in x["pernas"])
        zeros = "; ".join(f"[{br(z[0],2)}, {'∞' if z[1] is None else br(z[1],2)})" for z in s_["intervalos_zero"])
        ls.append([k, pernas, ", ".join(br(b, 2) for b in s_["breakevens"]) or "—", br(s_["ganho_max"], 2), br(s_["perda_max"], 2), br(s_["fluxo_montagem"], 2), (", ".join(s_["flags"]) + (" " + zeros if zeros else "")) or "—"])
    L.extend(tabela(["Estrutura", "Pernas", "Breakevens", "Ganho máx.", "Perda máx.", "Fluxo na montagem", "Flags"], ls))
    a("")
    a("`—` em ganho ou perda máximos = ilimitado. O JSON traz também o payoff de S_T = 20 a 40 e o valor em cada ponto de quebra.")
    a("")

    # 10 taxas
    t = c["taxas_cdi"]
    cvn = t["cdi_do_periodo_por_convencao"]
    a("## 10. Taxa contra o CDI")
    a("")
    a(f"Data-base 04/11/2026, vencimento 19/11/2026: {t['convencoes']['du']} DU e {t['convencoes']['dc']} DC; DI = {pct(t['convencoes']['DI_aa'],2)} a.a.; S bid/ask = 29,99/30,01.")
    a("")
    a("CDI do período por convenção: " + "; ".join(f"{k} = {pct(v,6)}" for k, v in cvn.items()) + ".")
    a("")
    ls = []

    def lin(nome, capital, m_):
        ls.append([nome, br(capital, 4), pct(m_["r_per"], 4), pct(m_["r_aa"], 2), pct(m_["pct_cdi_1_razao"], 2), pct(m_["pct_cdi_2_estilo_cdb"], 2), br(m_["spread_aa_pp"], 2)])
    for k in ("venda_coberta_otm_K31", "venda_coberta_itm_K29"):
        x = tx[k]
        lin(k + " (parado)", x["capital"], x["parado"])
        lin(k + " (exercida)", x["capital"], x["exercida"])
    for k in ("cash_put_otm_K29", "cash_put_itm_K31"):
        x = tx[k]
        lin(k + " prêmio, capital K−P", x["capital_K_menos_P"]["capital"], x["capital_K_menos_P"]["premio"])
        lin(k + " total c/ CDI, capital K−P", x["capital_K_menos_P"]["capital"], x["capital_K_menos_P"]["total_nao_exercida"])
        lin(k + " prêmio, capital K", x["capital_K"]["capital"], x["capital_K"]["premio"])
    x = tx["box3_K30"]
    lin("box3_K30", x["capital"], x)
    x = tx["box4_K28_K32"]
    lin("box4_K28_K32 aplicação", x["aplicacao"]["capital"], x["aplicacao"])
    lin("box4_K28_K32 captação (custo)", x["captacao"]["recebe"], x["captacao"])
    x = tx["box4_livro_sintetico_taxa_negativa"]
    lin("box4 com livro sintético (borda)", x["aplicacao"]["capital"], x["aplicacao"])
    x = tx["long_collar_K28_K33"]
    lin("long_collar_K28_K33 piso", x["capital"], x["piso"])
    lin("long_collar_K28_K33 teto", x["capital"], x["teto"])
    lin("long_collar_K28_K33 parado", x["capital"], x["parado"])
    L.extend(tabela(["Estrutura", "Capital", "r período", "r a.a.", "% CDI (razão)", "% CDI (CDB)", "Spread a.a. (p.p.)"], ls))
    a("")
    v = t["verificacao"]["vetor_nota_14_box3_DU21"]
    a(f"Conferência com a nota 14 (box 3, DU = 21): r = {pct(v['r_per'],4)}, a.a. {pct(v['r_aa'],2)}, % CDI {pct(v['pct_cdi_1'],1)} e {pct(v['pct_cdi_2'],1)} (esperado 1,5228 %, 19,89 %, 179,8 % e 179,2 %).")
    a("")
    a("O JSON traz, para cada taxa, o % do CDI nas quatro convenções de CDI do período (`pct_cdi_1_por_convencao_cdi`).")
    a("")

    # 11 dias uteis
    a("## 11. Dias úteis com feriados B3")
    a("")
    ls = []
    for l in du["saidas"]["pares"]:
        ls.append([l["nome"], l["d0"], l["d1"], br(l["dc"], 0), br(l["du_b3_excl_incl"], 0), br(l["du_b3_incl_excl"], 0), br(l["du_anbima_excl_incl"], 0), br(l["du_anbima_incl_excl"], 0)])
    L.extend(tabela(["Caso", "d0", "d1", "DC", "DU B3 (d0,d1]", "DU B3 [d0,d1)", "DU ANBIMA (d0,d1]", "DU ANBIMA [d0,d1)"], ls))
    a("")
    a("Vencimentos ajustados: " + "; ".join(f"{k} = {v}" for k, v in du["saidas"]["vencimentos"].items()) + ".")
    a("")
    cf = du["verificacao"]["conferencia_com_json_do_projeto"]
    a(f"Conferência: os dias sem pregão e os feriados ANBIMA de 2026 a 2028 batem com `{cf['json_lido']}` ({'sim' if cf['confere_sem_pregao'] and cf['confere_anbima'] and cf['confere_contagens'] else 'NÃO'}); os vencimentos batem com `vencimentos-regras.md` ({'sim' if du['verificacao']['vencimentos_iguais_a_nota'] else 'NÃO'}). 2027 e 2028 são calendários derivados; a errata OC 041/2026-VNC não foi lida.")
    a("")

    # 12 curva
    a("## 12. Curva DI: flat forward 252")
    a("")
    a("Vértices sintéticos (data-base 04/11/2026, DU ANBIMA da data-base inclusive ao vencimento exclusive):")
    a("")
    L.extend(tabela(["Vértice", "Vencimento", "DU", "Taxa a.a.", "PU"],
                    [[x["nome"], x["vencimento"] or "—", br(x["du"], 0), pct(x["taxa_aa"], 3), br(x.get("pu"), 2)] for x in cv["entradas"]["vertices"]]))
    a("")
    L.extend(tabela(["DU", "Taxa a.a.", "Fator", "PU", "Extrapolado"],
                    [[br(p["du"], 0), pct(p["taxa_aa"], 6), br(p["fator"], 10), br(p["pu_100000"], 4), br(p["extrapolado"])] for p in cv["saidas"]["pontos"]]))
    a("")
    a("Forwards entre vértices: " + "; ".join(f"{br(f['de_du'],0)}–{br(f['ate_du'],0)} DU: {pct(f['forward_aa'],4)}" for f in cv["saidas"]["forwards"]) + ".")
    a("")
    a(f"Conferência: diferença máxima contra a interpolação linear de ln(fator) = {sci(cv['verificacao']['max_dif_implementacao_independente'])}; forward constante dentro de cada intervalo: {br(cv['verificacao']['forwards_constantes'])}.")
    a("")

    a("## Números observados em tela de terceiros (retido)")
    a("")
    a("A análise dos dois valores de \"CDI no período\" lidos em tela de terceiros (0,3413 % e 0,5656 %) está em `retido/cdi-observado.md`, separada destes vetores. Ela não entra em nenhum teste até o Marcelo decidir sobre o uso dessas telas.")
    a("")
    a("Resultado em uma linha: a venda coberta fecha com DI × DC/360 (convenção pública LIN360_DC, que já está calculada nos vetores acima); o cash put **não fechou** com nenhuma das 162 combinações de taxa, forma e prazo em dias inteiros. Só fecha com um parâmetro livre (prazo fracionário, outra taxa ou outra base de capital), e isso não dá para confirmar sem o strike, o prêmio e o horário da leitura.")
    a("")
    a("## Pendências")
    a("")
    for t_ in [
        "Confirmar no arquivo real da B3 se coberto + travado + descoberto fecha com `OpnIntrst` ou com `TtlPos`, e se `BrrwrQty`/`LndrQty` são titulares e lançadores.",
        "Decidir as convenções [P] acima (sinal da GEX, método do flip, regra das walls, método do Max Pain, base do % do CDI, capital do cash put).",
        "Refazer os vetores de 2027 e 2028 quando a B3 publicar os calendários; ler a errata OC 041/2026-VNC.",
        "Trocar a curva sintética por um arquivo TS real da B3 quando houver um baixado, e conferir a interpolação contra a curva PRE publicada.",
    ]:
        a("- " + t_)
    a("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    aqui = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--saida", default=os.path.dirname(aqui))
    ap.add_argument("--feriados-json", default=NOTAS_B3 + "feriados-b3-2026-2028.json")
    a = ap.parse_args()
    doc = gera(carrega_feriados(a.feriados_json))
    os.makedirs(a.saida, exist_ok=True)
    pj = os.path.join(a.saida, "agregados.json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, allow_nan=False)
        f.write("\n")
    pm = os.path.join(a.saida, "agregados.md")
    with open(pm, "w", encoding="utf-8") as f:
        f.write(render_md(doc))
    print(pj)
    print(pm)


if __name__ == "__main__":
    main()
