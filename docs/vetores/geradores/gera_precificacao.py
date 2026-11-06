#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gera_precificacao.py - vetores de teste do motor de precificacao de opcoes.

Gera `precificacao.json` e `precificacao.md` na pasta de saida.

    python3 -I gera_precificacao.py --saida /mnt/project-files/jumba/vetores/

So biblioteca padrao (decimal, math, json, hashlib). Nada e baixado.

Como os valores esperados sao obtidos
-------------------------------------
1. Referencia em `decimal.Decimal` com 100 digitos significativos: pi por Machin,
   erf pela serie de termos positivos, cauda da normal pela serie assintotica de
   Mills quando |x| > 14. Formulas fechadas do Black-Scholes generalizado (custo de
   carregamento b), das quais saem BSM-Merton (b = r - q), Black-76 (b = 0, S -> F)
   e Garman-Kohlhagen (b = r_d - r_f).
2. Cada grega analitica e conferida por diferencas finitas centrais em 100 digitos.
3. Cada caso e conferido pela EDP de Black-Scholes e pela paridade put-call.
4. A vol implicita de referencia sai de bissecao + Newton em 100 digitos, sobre o
   preco exatamente como ele fica gravado no JSON (double).
5. Uma implementacao independente em double (math.erfc) tem de passar em todos os
   casos com as tolerancias gravadas; senao o script para com erro.
6. Os valores publicados (Hull, Haug) e os vetores de 6 casas das notas de
   metodologia sao conferidos dentro do arredondamento publicado.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time
from decimal import Decimal, getcontext

getcontext().prec = 100
D = Decimal
ZERO, ONE, TWO = D(0), D(1), D(2)
HALF = D("0.5")
DATA_ACESSO = "2026-11-04"
EPS_DOUBLE = 2.220446049250313e-16
TOL_PADRAO = {"abs": 1e-10, "rel": 1e-10}
FLAG_FORA = "FORA_DOS_LIMITES"

# ---------------------------------------------------------------------------
# Fontes (citadas em cada caso pelo campo origem.referencia)
# ---------------------------------------------------------------------------
REF_HULL = ("J. C. Hull, Options, Futures, and Other Derivatives, 9a ed., Pearson, 2014 "
            "(livro impresso, sem URL)")
REF_HAUG = ("E. G. Haug, The Complete Guide to Option Pricing Formulas, 2a ed., McGraw-Hill, "
            "2007 (livro impresso, sem URL)")
REF_MANUAL_B3 = ("B3, Manual de Apreçamento - Opções (20/12/2023), §1.1 e §2.1: "
                 "https://www.b3.com.br/data/files/48/A5/38/D0/CF38C8103152D4C8AC094EA8/"
                 "Manual%20de%20Apre%C3%A7amento%20-%20Op%C3%A7%C3%B5es%202023-12-20.pdf "
                 "(citado em /mnt/project-files/jumba/conhecimento/metodologia/01-convencoes-base.md, "
                 "acesso 2026-11-04)")
REF_METOD = "/mnt/project-files/jumba/conhecimento/metodologia/"
REF_GERADOR = "geradores/gera_precificacao.py (Decimal, 100 digitos)"
REF_SINT = "caso sintético, sem fonte externa (parâmetros escolhidos para o teste)"


# ---------------------------------------------------------------------------
# Aritmetica de alta precisao
# ---------------------------------------------------------------------------
def num(x):
    """'0.1065', '20/52', int, float ou Decimal -> Decimal exato."""
    if isinstance(x, D):
        return x
    if isinstance(x, bool):
        raise TypeError(x)
    if isinstance(x, int):
        return D(x)
    if isinstance(x, float):
        return D(x)  # valor binario exato do double
    if isinstance(x, str):
        if "/" in x:
            a, b = x.split("/")
            return D(a) / D(b)
        return D(x)
    raise TypeError(x)


def _eps():
    return D(10) ** -(getcontext().prec + 5)


def _atan_inv(n):
    n = D(n)
    n2 = n * n
    termo = ONE / n
    soma = termo
    k, sinal = 1, -1
    while True:
        termo /= n2
        t = termo / (2 * k + 1)
        if t < _eps():
            break
        soma += sinal * t
        sinal, k = -sinal, k + 1
    return soma


PI = 16 * _atan_inv(5) - 4 * _atan_inv(239)
SQRT2 = TWO.sqrt()
SQRT2PI = (2 * PI).sqrt()
SQRTPI = PI.sqrt()


def _erf_pos(z):
    """erf(z), z >= 0: 2/sqrt(pi) e^{-z^2} sum 2^n z^{2n+1} / (1*3*...*(2n+1))."""
    if z == 0:
        return ZERO
    z2 = z * z
    termo = z
    soma = z
    n = 0
    while True:
        n += 1
        termo = termo * 2 * z2 / (2 * n + 1)
        soma += termo
        if termo < _eps() * soma:
            break
    return 2 / SQRTPI * (-z2).exp() * soma


def npdf(x):
    return (-(x * x) / 2).exp() / SQRT2PI


def _cauda_mills(x):
    """Q(x) = 1 - N(x) para x > 14, pela serie assintotica (erro relativo < 1e-40)."""
    x2 = x * x
    termo = ONE
    soma = ONE
    k = 1
    while True:
        novo = -termo * (2 * k - 1) / x2
        if abs(novo) >= abs(termo) or abs(novo) < _eps():
            break
        soma += novo
        termo = novo
        k += 1
    return npdf(x) / x * soma


def ncdf(x):
    if x == 0:
        return HALF
    if x > 14:
        return ONE - _cauda_mills(x)
    if x < -14:
        return _cauda_mills(-x)
    e = _erf_pos(abs(x) / SQRT2)
    return (ONE + e) / 2 if x > 0 else (ONE - e) / 2


# ---------------------------------------------------------------------------
# Black-Scholes generalizado em Decimal
# ---------------------------------------------------------------------------
def preco_dec(tipo, S, K, T, r, b, s):
    if T == 0:
        return max(S - K, ZERO) if tipo == "C" else max(K - S, ZERO)
    sq = T.sqrt()
    vs = s * sq
    d1 = ((S / K).ln() + (b + s * s / 2) * T) / vs
    d2 = d1 - vs
    eb = ((b - r) * T).exp()
    er = (-r * T).exp()
    if tipo == "C":
        return S * eb * ncdf(d1) - K * er * ncdf(d2)
    return K * er * ncdf(-d2) - S * eb * ncdf(-d1)


def gbs_dec(tipo, S, K, T, r, b, s):
    sq = T.sqrt()
    vs = s * sq
    d1 = ((S / K).ln() + (b + s * s / 2) * T) / vs
    d2 = d1 - vs
    eb = ((b - r) * T).exp()
    er = (-r * T).exp()
    n1 = npdf(d1)
    if tipo == "C":
        N1, N2 = ncdf(d1), ncdf(d2)
        preco = S * eb * N1 - K * er * N2
        delta = eb * N1
        theta = -S * eb * n1 * s / (2 * sq) - (b - r) * S * eb * N1 - r * K * er * N2
        dVdb = T * S * eb * N1
    else:
        N1, N2 = ncdf(-d1), ncdf(-d2)
        preco = K * er * N2 - S * eb * N1
        delta = -eb * N1
        theta = -S * eb * n1 * s / (2 * sq) + (b - r) * S * eb * N1 + r * K * er * N2
        dVdb = -T * S * eb * N1
    return {
        "preco": preco, "d1": d1, "d2": d2, "delta": delta,
        "gamma": eb * n1 / (S * vs), "vega": S * eb * n1 * sq, "theta": theta,
        "dVdr_b_fixo": -T * preco, "dVdb": dVdb,
    }


def limites_dec(tipo, S, K, T, r, b):
    fs = S * ((b - r) * T).exp()
    fk = K * (-r * T).exp()
    if tipo == "C":
        return max(ZERO, fs - fk), fs
    return max(ZERO, fk - fs), fk


def iv_dec(tipo, P, S, K, T, r, b):
    lo, hi = limites_dec(tipo, S, K, T, r, b)
    if not (lo < P < hi):
        return None
    a, c = D("1e-8"), D(50)
    fa = preco_dec(tipo, S, K, T, r, b, a) - P
    fc = preco_dec(tipo, S, K, T, r, b, c) - P
    if not (fa < 0 < fc):
        raise RuntimeError("raiz fora de [1e-8, 50]")
    for _ in range(90):
        m = (a + c) / 2
        if preco_dec(tipo, S, K, T, r, b, m) - P > 0:
            c = m
        else:
            a = m
    s = (a + c) / 2
    for _ in range(60):
        g = gbs_dec(tipo, S, K, T, r, b, s)
        passo = (g["preco"] - P) / g["vega"]
        s_novo = s - passo
        if not (a <= s_novo <= c):
            raise RuntimeError("Newton saiu do intervalo")
        if abs(s_novo - s) < D("1e-80"):
            s = s_novo
            break
        s = s_novo
    return s


# ---------------------------------------------------------------------------
# Implementacao independente em double (simula o motor)
# ---------------------------------------------------------------------------
def _N(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def _n(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def gbs_f(tipo, S, K, T, r, b, s):
    sq = math.sqrt(T)
    vs = s * sq
    d1 = (math.log(S / K) + (b + 0.5 * s * s) * T) / vs
    d2 = d1 - vs
    eb = math.exp((b - r) * T)
    er = math.exp(-r * T)
    n1 = _n(d1)
    if tipo == "C":
        N1, N2 = _N(d1), _N(d2)
        p = S * eb * N1 - K * er * N2
        de = eb * N1
        th = -S * eb * n1 * s / (2 * sq) - (b - r) * S * eb * N1 - r * K * er * N2
        dvdb = T * S * eb * N1
    else:
        N1, N2 = _N(-d1), _N(-d2)
        p = K * er * N2 - S * eb * N1
        de = -eb * N1
        th = -S * eb * n1 * s / (2 * sq) + (b - r) * S * eb * N1 + r * K * er * N2
        dvdb = -T * S * eb * N1
    return {"preco": p, "d1": d1, "d2": d2, "delta": de, "gamma": eb * n1 / (S * vs),
            "vega": S * eb * n1 * sq, "theta": th, "dVdr_b_fixo": -T * p, "dVdb": dvdb}


def preco_f(tipo, S, K, T, r, b, s):
    if T == 0:
        return max(S - K, 0.0) if tipo == "C" else max(K - S, 0.0)
    return gbs_f(tipo, S, K, T, r, b, s)["preco"]


def iv_f(tipo, P, S, K, T, r, b):
    """Newton protegido por intervalo (bissecao quando o passo sai do intervalo)."""
    fs, fk = S * math.exp((b - r) * T), K * math.exp(-r * T)
    lo, hi = (max(0.0, fs - fk), fs) if tipo == "C" else (max(0.0, fk - fs), fk)
    if not (lo < P < hi):
        return None
    a, c = 1e-6, 10.0
    s = math.sqrt(2.0 / T * abs(math.log(S / K) + b * T)) or 0.3
    s = min(max(s, 0.05), 3.0)
    for _ in range(300):
        g = gbs_f(tipo, S, K, T, r, b, s)
        f = g["preco"] - P
        if f > 0:
            c = s
        else:
            a = s
        s_novo = s - f / g["vega"] if g["vega"] > 0 else -1.0
        if not (a < s_novo < c):
            s_novo = 0.5 * (a + c)
        if abs(s_novo - s) <= 1e-15 * max(1.0, s) or (c - a) <= 1e-15 * max(1.0, s):
            return s_novo
        s = s_novo
    return s


# ---------------------------------------------------------------------------
# Modelos: entradas proprias -> entradas do GBS
# ---------------------------------------------------------------------------
def modelo_para_gbs(m):
    """m: dict de Decimais do conjunto de parametros. Devolve (S, K, T, r, b, sigma)."""
    if m["modelo"] == "BSM_MERTON":
        return m["S"], m["K"], m["T"], m["r"], m["r"] - m["q"], m.get("sigma")
    if m["modelo"] == "BLACK76":
        return m["F"], m["K"], m["T"], m["r"], ZERO, m.get("sigma")
    if m["modelo"] == "GARMAN_KOHLHAGEN":
        return m["S"], m["K"], m["T"], m["r"], m["r"] - m["q"], m.get("sigma")
    raise ValueError(m["modelo"])


NUM_KEYS = {"S", "F", "K", "T", "r", "q", "r_d", "r_f", "DU", "DC", "DI_aa", "cupom_lin_aa", "sigma"}


def completa_b3(p):
    """Converte DU/DI (e DC/cupom) na convencao B3 em T, r e q contínuos."""
    m = {k: (num(v) if k in NUM_KEYS else v) for k, v in p.items()}
    if p.get("convencao") == "B3":
        m["T"] = num(p["DU"]) / 252
        m["r"] = (ONE + num(p["DI_aa"])).ln()
        if p["modelo"] == "GARMAN_KOHLHAGEN":
            m["q"] = D(252) / num(p["DU"]) * (ONE + num(p["cupom_lin_aa"]) * num(p["DC"]) / 360).ln()
    if p["modelo"] in ("BSM_MERTON",) and "q" not in m:
        m["q"] = ZERO
    if p["modelo"] == "GARMAN_KOHLHAGEN" and "r_f" in p:
        m["q"] = num(p["r_f"])
        m["r"] = num(p["r_d"])
    if p["modelo"] == "BSM_MERTON" and "r" not in m:
        raise ValueError("faltou r")
    return m


def modelo_motor(p, q):
    if p["modelo"] == "BLACK76":
        return "BLACK76"
    if p["modelo"] == "GARMAN_KOHLHAGEN":
        return "GK"
    return "BS_B3" if q == 0 else "BSM_Q"


def f(x):
    return float(x)


# ---------------------------------------------------------------------------
# Conjuntos de parametros para preco + gregas
# ---------------------------------------------------------------------------
# 'pub' = valores publicados por tipo (string, para saber o numero de casas).
CONJUNTOS = [
    # ---------------- Hull ----------------
    dict(id="HULL-BSM-EX15.6", modelo="BSM_MERTON", convencao="HULL",
         S="42", K="40", T="0.5", r="0.10", q="0", sigma="0.20",
         ref=REF_HULL + ", cap. 15 (The Black-Scholes-Merton Model), Example 15.6",
         pub={"C": {"preco": "4.76", "d1": "0.7693", "d2": "0.6278"}, "P": {"preco": "0.81"}},
         nota="Acao sem dividendo. Hull arredonda N(d1) e N(d2) em 4 casas."),
    dict(id="HULL-GREGAS-CAP19", modelo="BSM_MERTON", convencao="HULL",
         S="49", K="50", T="20/52", r="0.05", q="0", sigma="0.20",
         ref=REF_HULL + ", cap. 19 (The Greek Letters), exemplo da call vendida (100.000 opções, "
                        "20 semanas) usado nos exemplos de delta, theta, gamma, vega e rho",
         pub={"C": {"preco": "2.40", "d1": "0.0542", "delta": "0.522", "gamma": "0.066",
                    "vega": "12.1", "theta_ano": "-4.31", "theta_dc": "-0.0118",
                    "theta_du": "-0.0171", "rho": "8.91"}},
         nota="T = 20/52 (Hull escreve 0,3846). Hull: theta -4,31/ano = -0,0118 por dia corrido "
              "(/365) = -0,0171 por dia de negociação (/252); vega 12,1 por 1,00 (0,121 por 1 p.p.); "
              "rho 8,91 por 1,00 (0,0891 por 1 p.p.). Preço publicado: 'cerca de US$ 240.000' "
              "para 100.000 opções."),
    dict(id="HULL-INDICE-EX17.1", modelo="BSM_MERTON", convencao="HULL",
         S="930", K="900", T="2/12", r="0.08", q="0.03", sigma="0.20",
         ref=REF_HULL + ", cap. 17 (Options on Stock Indices and Currencies), Example 17.1",
         pub={"C": {"preco": "51.83"}},
         nota="Dividend yield de 0,2 % no 1º mês e 0,3 % no 2º: q = 0,5 %/(2/12) = 3 % a.a. "
              "Hull imprime d1 = 0,5444 (truncado; o exato arredonda para 0,5445), por isso d1 não "
              "entra como publicado."),
    dict(id="HULL-FUTURO-CAP18", modelo="BLACK76", convencao="HULL",
         F="20", K="20", T="4/12", r="0.09", sigma="0.25",
         ref=REF_HULL + ", cap. 18 (Futures Options), exemplo da put europeia sobre futuro de petróleo",
         pub={"P": {"preco": "1.12"}},
         nota="Black-76 com prêmio pago à vista (descontado por e^{-rT})."),
    # ---------------- Haug ----------------
    dict(id="HAUG-BS", modelo="BSM_MERTON", convencao="HAUG",
         S="60", K="65", T="0.25", r="0.08", q="0", sigma="0.30",
         ref=REF_HAUG + ", cap. 1 (Black-Scholes-Merton), exemplo do Black-Scholes 1973",
         pub={"C": {"preco": "2.1334"}}, nota="Call de 3 meses sobre ação sem dividendo."),
    dict(id="HAUG-MERTON", modelo="BSM_MERTON", convencao="HAUG",
         S="100", K="95", T="0.5", r="0.10", q="0.05", sigma="0.20",
         ref=REF_HAUG + ", cap. 1, exemplo do Merton 1973 (índice com dividend yield)",
         pub={"P": {"preco": "2.4648"}}, nota="Put de 6 meses sobre índice com q = 5 % a.a."),
    dict(id="HAUG-BLACK76", modelo="BLACK76", convencao="HAUG",
         F="19", K="19", T="0.75", r="0.10", sigma="0.28",
         ref=REF_HAUG + ", cap. 1, exemplo do Black-76 (opção sobre futuro)",
         pub={"C": {"preco": "1.7011"}, "P": {"preco": "1.7011"}},
         nota="No dinheiro (F = K): call e put têm o mesmo preço."),
    dict(id="HAUG-GK", modelo="GARMAN_KOHLHAGEN", convencao="HAUG",
         S="1.56", K="1.60", T="0.5", r_d="0.06", r_f="0.08", sigma="0.12",
         ref=REF_HAUG + ", cap. 1, exemplo do Garman-Kohlhagen (opção de moeda)",
         pub={"C": {"preco": "0.0291"}}, nota="r_d = taxa doméstica, r_f = taxa estrangeira."),
    dict(id="HAUG-DELTA-B76", modelo="BLACK76", convencao="HAUG",
         F="105", K="100", T="0.5", r="0.10", sigma="0.36",
         ref=REF_HAUG + ", cap. 2 (gregas), exemplo de delta de opção sobre futuro (b = 0)",
         pub={"C": {"delta": "0.5946"}, "P": {"delta": "-0.3566"}},
         nota="Delta em relação a F, já com o desconto e^{-rT}."),
    dict(id="HAUG-GAMMA-VEGA", modelo="BSM_MERTON", convencao="HAUG",
         S="55", K="60", T="0.75", r="0.10", q="0", sigma="0.30",
         ref=REF_HAUG + ", cap. 2, exemplos de gamma e de vega (mesmos parâmetros)",
         pub={"C": {"gamma": "0.0278", "vega": "18.9358"}, "P": {"gamma": "0.0278", "vega": "18.9358"}},
         nota="Gamma e vega iguais para call e put."),
    dict(id="HAUG-THETA", modelo="BSM_MERTON", convencao="HAUG",
         S="430", K="405", T="0.0833", r="0.07", q="0.05", sigma="0.20",
         ref=REF_HAUG + ", cap. 2, exemplo de theta (índice, b = r - q = 0,02)",
         pub={"P": {"theta_ano": "-31.1924"}},
         nota="T = 0,0833 exatamente como publicado (não 1/12). Theta por ano."),
    dict(id="HAUG-RHO", modelo="BSM_MERTON", convencao="HAUG",
         S="72", K="75", T="1", r="0.09", q="0", sigma="0.19",
         ref=REF_HAUG + ", cap. 2, exemplo de rho",
         pub={"C": {"rho": "38.7325"}}, nota="Rho por 1,00 de taxa contínua."),
    # ---------------- Convencao B3 ----------------
    dict(id="B3-ACAO-REF-21DU", modelo="BSM_MERTON", convencao="B3",
         S="30", K="32", DU=21, DI_aa="0.1065", q="0", sigma="0.35",
         ref=REF_MANUAL_B3, consist="metodologia/05 §3 (6 casas)",
         nota="Mesmo vetor da nota 05 da metodologia, agora com 1e-10. Ação protegida contra "
              "proventos: q = 0 (BS_B3)."),
    dict(id="B3-ACAO-ATM-10DU", modelo="BSM_MERTON", convencao="B3",
         S="38.42", K="38.00", DU=10, DI_aa="0.1490", q="0", sigma="0.31",
         ref=REF_MANUAL_B3, nota="Perto do dinheiro, 10 dias úteis."),
    dict(id="B3-ACAO-1DU-ATM", modelo="BSM_MERTON", convencao="B3",
         S="30", K="30", DU=1, DI_aa="0.1490", q="0", sigma="0.40",
         ref=REF_MANUAL_B3, nota="Prazo de 1 dia útil; theta_1du_exato = intrínseco - preço."),
    dict(id="B3-ACAO-1DU-K31", modelo="BSM_MERTON", convencao="B3",
         S="30", K="31", DU=1, DI_aa="0.1490", q="0", sigma="0.55",
         ref=REF_MANUAL_B3, nota="1 dia útil: call fora do dinheiro, put dentro."),
    dict(id="B3-ACAO-126DU-K26", modelo="BSM_MERTON", convencao="B3",
         S="20", K="26", DU=126, DI_aa="0.1435", q="0", sigma="0.45",
         ref=REF_MANUAL_B3,
         nota="Put europeia muito dentro do dinheiro, 126 DU: o preço europeu fica abaixo de K - S."),
    dict(id="B3-INDICE-BSMQ-42DU", modelo="BSM_MERTON", convencao="B3",
         S="145000", K="147000", DU=42, DI_aa="0.1475", q="0.045", sigma="0.21",
         ref=REF_MANUAL_B3,
         nota="BSM-Merton com q contínuo (índice à vista ou opção não protegida); T e r na "
              "convenção B3. q = 4,5 % a.a. é ilustrativo, não é dado da B3."),
    dict(id="B3-IND-B76-15DU", modelo="BLACK76", convencao="B3",
         F="130000", K="132000", DU=15, DI_aa="0.1065", sigma="0.20",
         ref=REF_MANUAL_B3, consist="metodologia/03 §4 (2 casas no preço)",
         nota="Opção sobre futuro de índice (pontos). Mesmo vetor da nota 03."),
    dict(id="B3-IND-B76-1DU", modelo="BLACK76", convencao="B3",
         F="150000", K="150000", DU=1, DI_aa="0.1490", sigma="0.18",
         ref=REF_MANUAL_B3, nota="Black-76 no dinheiro com 1 dia útil."),
    dict(id="B3-DOL-GK-20DU", modelo="GARMAN_KOHLHAGEN", convencao="B3",
         S="5.40", K="5.50", DU=20, DC=28, DI_aa="0.1065", cupom_lin_aa="0.05", sigma="0.14",
         ref=REF_MANUAL_B3, consist="metodologia/04 §3 (6 casas)",
         nota="Dólar à vista em R$/US$ (multiplique o prêmio por 1.000 para cotar em R$ por "
              "US$ 1.000). q = (252/DU)·ln(1 + cupom·DC/360), Manual B3 §2.1."),
]

# Casos de vol implicita. 'sigma_origem' => preco gerado a partir dessa vol;
# 'P' => preco dado (tick de mercado ou publicado). 'falha' => deve falhar.
IV_CASOS = [
    dict(id="IV-HULL-15.11", base=dict(modelo="BSM_MERTON", convencao="HULL", S="21", K="20",
         T="0.25", r="0.10", q="0"), tipo="C", P="1.875",
         ref=REF_HULL + ", cap. 15, seção Implied Volatilities (exemplo iterativo)",
         pub={"sigma": "0.235"},
         nota="Hull: sigma = 0,20 dá 1,76 e sigma = 0,30 dá 2,10; a vol implícita é 23,5 %."),
    dict(id="IV-HAUG-B76-PUBLICADO", base=dict(modelo="BLACK76", convencao="HAUG", F="19", K="19",
         T="0.75", r="0.10"), tipo="C", P="1.7011", ref=REF_HAUG + " (preço publicado do Black-76)",
         nota="Inverte o preço publicado de 4 casas; a vol volta perto de 0,28, mas não exatamente."),
    dict(id="IV-B3-REF-C", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="32", DU=21,
         DI_aa="0.1065", q="0"), tipo="C", sigma_origem="0.35", ref=REF_MANUAL_B3,
         nota="Preço do caso B3-ACAO-REF-21DU com precisão total; deve voltar 0,35."),
    dict(id="IV-B3-REF-P", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="32", DU=21,
         DI_aa="0.1065", q="0"), tipo="P", sigma_origem="0.35", ref=REF_MANUAL_B3, nota="Idem, put."),
    dict(id="IV-B3-TICK-C", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="32", DU=21,
         DI_aa="0.1065", q="0"), tipo="C", P="0.56", ref=REF_MANUAL_B3,
         nota="Prêmio arredondado no tick de R$ 0,01."),
    dict(id="IV-ITM-C-MODERADO", base=dict(modelo="BSM_MERTON", convencao="HULL", S="100", K="70",
         T="0.25", r="0.10", q="0"), tipo="C", sigma_origem="0.30", ref=REF_SINT,
         nota="Call muito dentro do dinheiro (d1 ~ 2,6); vega ainda razoável."),
    dict(id="IV-ITM-C-EXTREMO", base=dict(modelo="BSM_MERTON", convencao="HULL", S="100", K="50",
         T="0.25", r="0.10", q="0"), tipo="C", sigma_origem="0.25", ref=REF_SINT,
         nota="Mal condicionado: d1 ~ 5,8 e vega ~ 1e-6. O valor-tempo é ~1e-8 de um prêmio de ~51; "
              "o próprio arredondamento do double do preço já move sigma. Tolerância de sigma "
              "relaxada; vale também o critério de repreçar."),
    dict(id="IV-ITM-P-B3-EXTREMO", base=dict(modelo="BSM_MERTON", convencao="B3", S="20", K="34",
         DU=21, DI_aa="0.1490", q="0"), tipo="P", sigma_origem="0.35", ref=REF_MANUAL_B3,
         nota="Put muito dentro do dinheiro (d1 ~ -5); preço europeu abaixo de K - S."),
    dict(id="IV-P-ABAIXO-INTRINSECO-VALIDO", base=dict(modelo="BSM_MERTON", convencao="B3", S="30",
         K="32", DU=21, DI_aa="0.1065", q="0"), tipo="P", P="1.95", ref=REF_MANUAL_B3,
         nota="1,95 < K - S = 2,00, mas > K·e^{-rT} - S = 1,7313: existe vol europeia. Testa se o "
              "motor usa o limite descontado e não o intrínseco simples."),
    dict(id="IV-OTM-C-PROFUNDO", base=dict(modelo="BSM_MERTON", convencao="HULL", S="100", K="150",
         T="0.25", r="0.05", q="0"), tipo="C", sigma_origem="0.30", ref=REF_SINT,
         nota="Call muito fora do dinheiro (d1 ~ -2,5)."),
    dict(id="IV-OTM-C-EXTREMO", base=dict(modelo="BSM_MERTON", convencao="HULL", S="100", K="200",
         T="0.25", r="0.05", q="0"), tipo="C", sigma_origem="0.30", ref=REF_SINT,
         nota="Prêmio ~1e-5. Bem condicionado em sigma se o preço for calculado sem cancelamento."),
    dict(id="IV-OTM-P-B3", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="22", DU=21,
         DI_aa="0.1490", q="0"), tipo="P", sigma_origem="0.50", ref=REF_MANUAL_B3,
         nota="Put muito fora do dinheiro, 21 DU."),
    dict(id="IV-1DU-ATM-C", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="30", DU=1,
         DI_aa="0.1490", q="0"), tipo="C", sigma_origem="0.40", ref=REF_MANUAL_B3,
         nota="Prazo de 1 dia útil, no dinheiro."),
    dict(id="IV-1DU-OTM-C-TICK", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="31", DU=1,
         DI_aa="0.1490", q="0"), tipo="C", P="0.05", ref=REF_MANUAL_B3,
         nota="1 DU, fora do dinheiro, cotada a R$ 0,05: vol alta."),
    dict(id="IV-1DU-OTM-P-TICK", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="29", DU=1,
         DI_aa="0.1490", q="0"), tipo="P", P="0.01", ref=REF_MANUAL_B3,
         nota="1 DU, put fora do dinheiro no tick mínimo."),
    dict(id="IV-1DU-ITM-C-PERTO-LIMITE", base=dict(modelo="BSM_MERTON", convencao="B3", S="30",
         K="29", DU=1, DI_aa="0.1490", q="0"), tipo="C", P="1.02", ref=REF_MANUAL_B3,
         nota="1 DU, valor-tempo ~0,005 acima do limite S - K·e^{-rT} = 1,0154."),
    dict(id="IV-VOL-ALTA", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="30", DU=5,
         DI_aa="0.1490", q="0"), tipo="C", sigma_origem="2.5", ref=REF_MANUAL_B3,
         nota="Vol de 250 % (evento), ainda dentro de [0,001; 5]."),
    dict(id="IV-VOL-BAIXA", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="31.06", DU=63,
         DI_aa="0.1490", q="0"), tipo="C", sigma_origem="0.02", ref=REF_MANUAL_B3,
         nota="Vol de 2 % no strike perto do forward (30·1,149^{63/252} = 31,06)."),
    dict(id="IV-B76-IND", base=dict(modelo="BLACK76", convencao="B3", F="130000", K="132000", DU=15,
         DI_aa="0.1065"), tipo="C", P="1660", ref=REF_MANUAL_B3, nota="Black-76, prêmio em pontos."),
    dict(id="IV-GK-DOL", base=dict(modelo="GARMAN_KOHLHAGEN", convencao="B3", S="5.40", K="5.50",
         DU=20, DC=28, DI_aa="0.1065", cupom_lin_aa="0.05"), tipo="C", P="0.052", ref=REF_MANUAL_B3,
         nota="Prêmio de R$ 52,000 por US$ 1.000 (0,052 R$/US$)."),
    # ------------- devem falhar -------------
    dict(id="IV-FALHA-C-ABAIXO-INTRINSECO", base=dict(modelo="BSM_MERTON", convencao="B3", S="30",
         K="28", DU=21, DI_aa="0.1490", q="0"), tipo="C", P="1.90", falha=True, ref=REF_MANUAL_B3,
         nota="1,90 < S - K = 2,00 < limite S - K·e^{-rT} = 2,3224."),
    dict(id="IV-FALHA-C-ENTRE-INTRINSECO-E-LIMITE", base=dict(modelo="BSM_MERTON", convencao="B3",
         S="30", K="28", DU=21, DI_aa="0.1490", q="0"), tipo="C", P="2.10", falha=True,
         ref=REF_MANUAL_B3,
         nota="2,10 > S - K = 2,00, mas < S - K·e^{-rT} = 2,3224: também falha. Pega o motor que "
              "compara com o intrínseco simples."),
    dict(id="IV-FALHA-P-ABAIXO-LIMITE", base=dict(modelo="BSM_MERTON", convencao="B3", S="30",
         K="32", DU=21, DI_aa="0.1065", q="0"), tipo="P", P="1.50", falha=True, ref=REF_MANUAL_B3,
         nota="1,50 < K·e^{-rT} - S = 1,7313."),
    dict(id="IV-FALHA-1DU-ABAIXO-LIMITE", base=dict(modelo="BSM_MERTON", convencao="B3", S="30",
         K="29", DU=1, DI_aa="0.1490", q="0"), tipo="C", P="1.01", falha=True, ref=REF_MANUAL_B3,
         nota="1 DU: 1,01 > S - K = 1,00, mas < limite 1,0154."),
    dict(id="IV-FALHA-C-ACIMA-MAXIMO", base=dict(modelo="BSM_MERTON", convencao="B3", S="30",
         K="28", DU=21, DI_aa="0.1490", q="0"), tipo="C", P="30.01", falha=True, ref=REF_MANUAL_B3,
         nota="Call acima de S·e^{(b-r)T} = 30."),
    dict(id="IV-FALHA-P-ACIMA-MAXIMO", base=dict(modelo="BSM_MERTON", convencao="B3", S="30",
         K="32", DU=21, DI_aa="0.1065", q="0"), tipo="P", P="31.80", falha=True, ref=REF_MANUAL_B3,
         nota="Put acima de K·e^{-rT} = 31,7313."),
    dict(id="IV-FALHA-PRECO-ZERO", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="35",
         DU=21, DI_aa="0.1490", q="0"), tipo="C", P="0", falha=True, ref=REF_MANUAL_B3,
         nota="Prêmio zero: o limite inferior é estrito."),
    dict(id="IV-FALHA-PRECO-NEGATIVO", base=dict(modelo="BSM_MERTON", convencao="B3", S="30", K="35",
         DU=21, DI_aa="0.1490", q="0"), tipo="C", P="-0.01", falha=True, ref=REF_MANUAL_B3,
         nota="Prêmio negativo."),
    dict(id="IV-FALHA-B76-ABAIXO-LIMITE", base=dict(modelo="BLACK76", convencao="B3", F="130000",
         K="125000", DU=15, DI_aa="0.1065"), tipo="C", P="4950", falha=True, ref=REF_MANUAL_B3,
         nota="Black-76: limite e^{-rT}(F - K) = 4.969,9; 4.950 fica abaixo."),
]


# ---------------------------------------------------------------------------
# Construcao dos casos
# ---------------------------------------------------------------------------
def casas(s):
    s = s.lstrip("-")
    return len(s.split(".")[1]) if "." in s else 0


def checa(cond, msg):
    if not cond:
        raise AssertionError(msg)


def perto(a, b, rel):
    return abs(a - b) <= rel * max(ONE, abs(b))


def entradas_json(p, tipo, extra=None):
    e = {"tipo": tipo}
    for k in ("S", "F", "K", "T", "r", "q", "r_d", "r_f", "DU", "DC", "DI_aa", "cupom_lin_aa", "sigma"):
        if k in p:
            v = p[k]
            e[k] = int(v) if k in ("DU", "DC") else f(num(v))
            if k == "T" and isinstance(v, str) and "/" in v:
                e["T_expr"] = v
    if extra:
        e.update(extra)
    return e


def caso_preco(p, tipo, verif):
    m = completa_b3(p)
    S, K, T, r, b, s = modelo_para_gbs(m)
    g = gbs_dec(tipo, S, K, T, r, b, s)
    mod = p["modelo"]
    # rho conforme o modelo
    if mod == "BLACK76":
        rho, rho_q = g["dVdr_b_fixo"], None
    else:
        rho, rho_q = g["dVdr_b_fixo"] + g["dVdb"], -g["dVdb"]
    out = {
        "preco": g["preco"], "d1": g["d1"], "d2": g["d2"], "delta": g["delta"], "gamma": g["gamma"],
        "vega": g["vega"], "vega_pp": g["vega"] / 100,
        "theta_ano": g["theta"], "theta_du": g["theta"] / 252, "theta_dc": g["theta"] / 365,
        "rho": rho, "rho_pp": rho / 100,
    }
    if rho_q is not None and not (mod == "BSM_MERTON" and m["q"] == 0 and p["convencao"] != "B3"):
        out["rho_q"] = rho_q
    if p["convencao"] == "B3":
        di = num(p["DI_aa"])
        out["rho_di_pp"] = rho / (100 * (ONE + di))
        out["theta_1du_exato"] = preco_dec(tipo, S, K, T - ONE / 252, r, b, s) - g["preco"]

    # --- verificacao 1: diferencas finitas em 100 digitos ---
    h1 = D("1e-30")
    P_ = lambda **kw: preco_dec(tipo, kw.get("S", S), K, kw.get("T", T), kw.get("r", r),
                                kw.get("b", b), kw.get("s", s))
    fd = {
        "delta": (P_(S=S + h1) - P_(S=S - h1)) / (2 * h1),
        "vega": (P_(s=s + h1) - P_(s=s - h1)) / (2 * h1),
        "theta_ano": -(P_(T=T + h1) - P_(T=T - h1)) / (2 * h1),
    }
    h2 = D("1e-22")
    fd["gamma"] = (P_(S=S + h2) - 2 * g["preco"] + P_(S=S - h2)) / (h2 * h2)
    if mod == "BLACK76":
        fd["rho"] = (P_(r=r + h1) - P_(r=r - h1)) / (2 * h1)
    else:
        fd["rho"] = (P_(r=r + h1, b=b + h1) - P_(r=r - h1, b=b - h1)) / (2 * h1)
        fd["rho_q"] = -(P_(b=b + h1) - P_(b=b - h1)) / (2 * h1)
    for k, v in fd.items():
        ref = out.get(k, rho_q if k == "rho_q" else None)
        checa(perto(v, ref, D("1e-30")), f"{p['id']} {tipo}: diferenca finita de {k}: {v} x {ref}")
    # --- verificacao 2: EDP  Theta + 1/2 s^2 S^2 Gamma + b S Delta - r V = 0 ---
    edp = g["theta"] + s * s * S * S * g["gamma"] / 2 + b * S * g["delta"] - r * g["preco"]
    checa(abs(edp) < D("1e-80") * max(ONE, S), f"{p['id']}: EDP {edp}")
    # --- verificacao 3: paridade ---
    outro = "P" if tipo == "C" else "C"
    vo = preco_dec(outro, S, K, T, r, b, s)
    c_, p_ = (g["preco"], vo) if tipo == "C" else (vo, g["preco"])
    par = c_ - p_ - (S * ((b - r) * T).exp() - K * (-r * T).exp())
    checa(abs(par) < D("1e-80") * max(ONE, S), f"{p['id']}: paridade {par}")
    verif["edp_paridade_dif"] += 1

    caso = {
        "id": f"{p['id']}-{tipo}",
        "grupo": "preco_gregas",
        "modelo": mod,
        "modelo_motor": modelo_motor(p, m.get("q", ZERO)),
        "convencao": p["convencao"],
        "entradas": entradas_json(p, tipo),
        "entradas_gbs": {"S": f(S), "K": f(K), "T": f(T), "r": f(r), "b": f(b), "sigma": f(s)},
        "saidas_esperadas": {k: f(v) for k, v in out.items()},
        "tolerancia": {"padrao": dict(TOL_PADRAO)},
        "origem": {"tipo": "calculado", "referencia": p["ref"], "calculo": REF_GERADOR,
                   "data_acesso": DATA_ACESSO},
        "nota": p.get("nota", ""),
    }
    if mod == "BLACK76":
        caso["entradas_gbs"]["nota"] = "S do GBS = F"
    if p["modelo"] == "GARMAN_KOHLHAGEN":
        F = S * ((r - m["q"]) * T).exp()
        caso["saidas_esperadas"]["F_paridade"] = f(F)
    pub = p.get("pub", {}).get(tipo)
    if pub:
        tolp = {}
        for k, sv in pub.items():
            val = num(sv)
            tol = D(5) * D(10) ** -(casas(sv) + 1)
            checa(abs(out[k] - val) <= tol + D("1e-12"),
                  f"{caso['id']}: publicado {k}={sv} x calculado {out[k]}")
            tolp[k] = f(tol)
            verif["publicados"] += 1
        caso["origem"]["tipo"] = "publicado+calculado"
        caso["origem"]["publicado"] = {k: f(num(v)) for k, v in pub.items()}
        caso["origem"]["tolerancia_publicado"] = tolp
        caso["origem"]["regra_publicado"] = ("o valor publicado é arredondado: confere com "
                                             "saidas_esperadas dentro de meia unidade da última casa")
    if p.get("consist"):
        caso["origem"]["consistencia"] = p["consist"]
    return caso, out


def caso_b76_equivalente(p_gk, verif):
    """Black-76 sobre F = S e^{(r-q)T} tem de dar o mesmo preço do GK."""
    casos = []
    m = completa_b3(p_gk)
    S, K, T, r, b, s = modelo_para_gbs(m)
    F = S * ((r - m["q"]) * T).exp()
    Fd = D(float(F))  # o F gravado no JSON
    for tipo in ("C", "P"):
        gk = gbs_dec(tipo, S, K, T, r, b, s)
        b76 = gbs_dec(tipo, Fd, K, T, r, ZERO, s)
        checa(abs(gk["preco"] - b76["preco"]) < D("1e-15"), "GK x B76")
        verif["edp_paridade_dif"] += 1
        casos.append({
            "id": f"B3-DOL-B76-EQUIV-20DU-{tipo}",
            "grupo": "preco_gregas",
            "modelo": "BLACK76",
            "modelo_motor": "BLACK76",
            "convencao": "B3",
            "entradas": {"tipo": tipo, "F": f(Fd), "K": f(K), "DU": 20, "DI_aa": f(num("0.1065")),
                         "sigma": f(s)},
            "entradas_gbs": {"S": f(Fd), "K": f(K), "T": f(T), "r": f(r), "b": 0.0, "sigma": f(s),
                             "nota": "S do GBS = F"},
            "saidas_esperadas": {
                "preco": f(b76["preco"]), "preco_gk_mesmo_caso": f(gk["preco"]),
                "delta": f(b76["delta"]), "gamma": f(b76["gamma"]), "vega": f(b76["vega"]),
                "theta_ano": f(b76["theta"]), "theta_du": f(b76["theta"] / 252),
                "rho": f(b76["dVdr_b_fixo"]),
            },
            "tolerancia": {"padrao": dict(TOL_PADRAO)},
            "origem": {"tipo": "calculado", "referencia": REF_MANUAL_B3 + "; " + REF_METOD +
                       "04-garman-kohlhagen-dolar.md §3", "calculo": REF_GERADOR,
                       "data_acesso": DATA_ACESSO},
            "nota": ("F = S·e^{(r-q)T} do caso B3-DOL-GK-20DU (paridade coberta de juros). O preço "
                     "do Black-76 tem de ser igual ao do GK (diferença < 1e-15). As gregas mudam de "
                     "referência: delta e gamma são em F, e o rho mede só o desconto com F fixo."),
        })
    return casos


def caso_iv(c, verif):
    p = dict(c["base"])
    p["id"] = c["id"]
    m = completa_b3(p)
    S, K, T, r, b, _ = modelo_para_gbs(m)
    tipo = c["tipo"]
    if "sigma_origem" in c:
        Pexato = preco_dec(tipo, S, K, T, r, b, num(c["sigma_origem"]))
        Pjson = float(Pexato)
    else:
        Pjson = float(num(c["P"]))
    P = D(Pjson)  # exatamente o double gravado
    lo, hi = limites_dec(tipo, S, K, T, r, b)
    sig = iv_dec(tipo, P, S, K, T, r, b)
    falha = c.get("falha", False)
    checa((sig is None) == falha, f"{c['id']}: falha esperada={falha}, obtida={sig is None}")

    extra = {"preco": Pjson}
    if "sigma_origem" in c:
        extra["sigma_origem"] = f(num(c["sigma_origem"]))
    entradas = entradas_json(p, tipo, extra)
    saidas = {"falha": falha, "flags": [FLAG_FORA] if falha else [],
              "limite_inferior": f(lo), "limite_superior": f(hi)}
    tol = {"padrao": dict(TOL_PADRAO)}
    if falha:
        saidas["sigma"] = None
    else:
        g = gbs_dec(tipo, S, K, T, r, b, sig)
        vega = g["vega"]
        eb, er = ((b - r) * T).exp(), (-r * T).exp()
        if tipo == "C":
            termos = (S * eb * ncdf(g["d1"]), K * er * ncdf(g["d2"]))
        else:
            termos = (K * er * ncdf(-g["d2"]), S * eb * ncdf(-g["d1"]))
        M = max(termos[0], termos[1], abs(P))
        cond = 16 * EPS_DOUBLE * float(M) / float(vega)
        tol_s = max(1e-10, 10.0 ** math.ceil(math.log10(cond))) if cond > 0 else 1e-10
        saidas["sigma"] = f(sig)
        saidas["vega_em_sigma"] = f(vega)
        tol["por_campo"] = {"sigma": {"abs": tol_s, "rel": 0.0}}
        tol["preco_reprecificado"] = {"abs": 1e-10, "rel": 1e-10}
        tol["nota"] = ("sigma: abs = max(1e-10, 10^ceil(log10(16·eps·M/vega))), com M = o maior dos dois "
                       "termos da fórmula do preço (call: S·e^{(b-r)T}·N(d1) e K·e^{-rT}·N(d2)) ou o "
                       "próprio preço. preco_reprecificado: preço do motor no sigma obtido contra o "
                       "preço de entrada.")
        # double independente
        sf = iv_f(tipo, Pjson, f(S), f(K), f(T), f(r), f(b))
        checa(sf is not None, f"{c['id']}: double nao achou vol")
        checa(abs(sf - float(sig)) <= tol_s, f"{c['id']}: double {sf} x {sig} (tol {tol_s})")
        rep = preco_f(tipo, f(S), f(K), f(T), f(r), f(b), sf)
        checa(abs(rep - Pjson) <= max(1e-10, 1e-10 * abs(Pjson)), f"{c['id']}: repreco {rep}")
        verif["iv_double_erro_max"] = max(verif["iv_double_erro_max"], abs(sf - float(sig)))
        verif["iv_ok"] += 1
    if falha:
        sf = iv_f(tipo, Pjson, f(S), f(K), f(T), f(r), f(b))
        checa(sf is None, f"{c['id']}: double devia falhar")
        verif["iv_falha"] += 1

    caso = {
        "id": c["id"],
        "grupo": "vol_implicita",
        "modelo": p["modelo"],
        "modelo_motor": modelo_motor(p, m.get("q", ZERO)),
        "convencao": p["convencao"],
        "entradas": entradas,
        "entradas_gbs": {"S": f(S), "K": f(K), "T": f(T), "r": f(r), "b": f(b), "preco": Pjson},
        "saidas_esperadas": saidas,
        "tolerancia": tol,
        "origem": {"tipo": "calculado", "referencia": c["ref"], "calculo": REF_GERADOR,
                   "data_acesso": DATA_ACESSO},
        "nota": c.get("nota", ""),
    }
    if p["modelo"] == "BLACK76":
        caso["entradas_gbs"]["nota"] = "S do GBS = F"
    if c.get("pub"):
        for k, sv in c["pub"].items():
            tolp = D(5) * D(10) ** -(casas(sv) + 1)
            checa(abs(sig - num(sv)) <= tolp + D("1e-12"), f"{c['id']}: publicado {sv} x {sig}")
            verif["publicados"] += 1
            caso["origem"]["tipo"] = "publicado+calculado"
            caso["origem"]["publicado"] = {k: f(num(sv))}
            caso["origem"]["tolerancia_publicado"] = {k: f(tolp)}
    return caso


def casos_taxa(verif):
    out = []

    def add(id_, funcao, entradas, saidas, nota):
        out.append({"id": id_, "grupo": "taxa_b3", "modelo": "CONVENCAO_B3_252", "funcao_motor": funcao,
                    "convencao": "B3", "entradas": entradas,
                    "saidas_esperadas": {k: f(v) for k, v in saidas.items()},
                    "tolerancia": {"padrao": dict(TOL_PADRAO)},
                    "origem": {"tipo": "calculado", "referencia": REF_MANUAL_B3 + "; " + REF_METOD +
                               "01-convencoes-base.md §3", "calculo": REF_GERADOR,
                               "data_acesso": DATA_ACESSO},
                    "nota": nota})
        verif["taxa"] += 1

    for di in ("0.1065", "0.1490"):
        add(f"TX-TAXA-CONT-{di[2:]}", "taxa_cont", {"DI_aa": f(num(di))},
            {"r": (ONE + num(di)).ln()}, "r = ln(1 + DI): taxa contínua equivalente à DI base 252.")
    di, du = num("0.1490"), 21
    fp = (ONE + di) ** (D(du) / 252)
    r = (ONE + di).ln()
    checa(abs(1 / fp - (-r * D(du) / 252).exp()) < D("1e-90"), "fator x exp")
    add("TX-FATOR-DESCONTO-21DU", "fator_desconto", {"DI_aa": f(di), "DU": du},
        {"fator_desconto": 1 / fp, "fator_periodo": fp},
        "fator_desconto = (1+DI)^(-DU/252) = e^{-rT} com r = ln(1+DI) e T = DU/252.")
    add("TX-TAXA-DIARIA", "taxa_diaria", {"DI_aa": f(di)}, {"i_d": (ONE + di) ** (ONE / 252) - 1},
        "Taxa por dia útil: (1+DI)^(1/252) - 1.")
    v1, i1, v2, i2 = 21, num("0.1490"), 63, num("0.1460")
    for du in (21, 42, 50, 63):
        fpi = ((ONE + i1) ** (D(v1) / 252)) * (((ONE + i2) ** (D(v2) / 252)) /
                                               ((ONE + i1) ** (D(v1) / 252))) ** (D(du - v1) / D(v2 - v1))
        i = fpi ** (D(252) / D(du)) - 1
        add(f"TX-DI-INTERP-{du}DU", "di_interpola",
            {"curva": [[v1, f(i1)], [v2, f(i2)]], "DU": du}, {"taxa_aa": i, "fator_periodo": fpi},
            "Interpolação exponencial (flat forward 252) entre os vértices; no vértice devolve a "
            "própria taxa.")
    c, du, dc = num("0.05"), 20, 28
    add("TX-CUPOM-CONT-20DU", "cupom_cont", {"cupom_lin_aa": f(c), "DU": du, "DC": dc},
        {"q": D(252) / du * (ONE + c * dc / 360).ln()},
        "Cupom cambial linear/360 convertido em taxa contínua base 252 (Manual B3 §2.1).")
    return out


# ---------------------------------------------------------------------------
# Conferencias contra as notas de metodologia (6 casas) e o motor em double
# ---------------------------------------------------------------------------
METOD_6 = {  # nota 05 §3, nota 03 §4, nota 04 §3
    "B3-ACAO-REF-21DU-C": {"preco": 0.564695, "delta": 0.306858, "gamma": 0.115873, "vega": 3.041666,
                           "theta_ano": -7.261986, "rho": 0.720086, "theta_du": -0.028817},
    "B3-ACAO-REF-21DU-P": {"preco": 2.295958, "delta": -0.693142, "theta_ano": -4.050723,
                           "rho": -1.924186, "theta_du": -0.016074},
    "B3-IND-B76-15DU-C": {"preco": 1663.57, "delta": 0.3842},
    "B3-IND-B76-15DU-P": {"preco": 3651.56, "delta": -0.6098},
    "B3-DOL-GK-20DU-C": {"preco": 0.052240, "delta": 0.365402, "gamma": 1.760939, "F_paridade": 5.42246},
    "B3-DOL-GK-20DU-P": {"preco": 0.129160},
}


def confere_metodologia(casos):
    n = 0
    idx = {c["id"]: c for c in casos}
    for cid, vals in METOD_6.items():
        for k, v in vals.items():
            got = idx[cid]["saidas_esperadas"][k]
            dec = len(repr(v).split(".")[1]) if "." in repr(v) else 0
            checa(abs(got - v) <= 0.5 * 10 ** -dec + 1e-12, f"metodologia {cid} {k}: {got} x {v}")
            n += 1
    return n


def confere_double(casos):
    pior = 0.0
    for c in casos:
        if c["grupo"] != "preco_gregas":
            continue
        e = c["entradas_gbs"]
        tipo = c["entradas"]["tipo"]
        g = gbs_f(tipo, e["S"], e["K"], e["T"], e["r"], e["b"], e["sigma"])
        if c["modelo"] == "BLACK76":
            rho, rq = g["dVdr_b_fixo"], None
        else:
            rho, rq = g["dVdr_b_fixo"] + g["dVdb"], -g["dVdb"]
        calc = {"preco": g["preco"], "d1": g["d1"], "d2": g["d2"], "delta": g["delta"],
                "gamma": g["gamma"], "vega": g["vega"], "vega_pp": g["vega"] / 100,
                "theta_ano": g["theta"], "theta_du": g["theta"] / 252, "theta_dc": g["theta"] / 365,
                "rho": rho, "rho_pp": rho / 100, "rho_q": rq}
        if "DI_aa" in c["entradas"]:
            calc["rho_di_pp"] = rho / (100 * (1 + c["entradas"]["DI_aa"]))
            calc["theta_1du_exato"] = (preco_f(tipo, e["S"], e["K"], max(e["T"] - 1 / 252, 0.0), e["r"],
                                               e["b"], e["sigma"]) - g["preco"])
        for k, v in c["saidas_esperadas"].items():
            if k not in calc or calc[k] is None:
                continue
            tol = max(TOL_PADRAO["abs"], TOL_PADRAO["rel"] * abs(v))
            err = abs(calc[k] - v)
            checa(err <= tol, f"double {c['id']} {k}: {calc[k]} x {v}")
            pior = max(pior, err / max(1.0, abs(v)))
    return pior


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
def fmt(v, n=10):
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "sim" if v else "não"
    if isinstance(v, int):
        return str(v)
    if v != 0 and (abs(v) < 1e-3 or abs(v) >= 1e6):
        return f"{v:.{n}e}"
    return f"{v:.{n}f}".rstrip("0").rstrip(".") if "." in f"{v:.{n}f}" else f"{v}"


def resumo_entradas(c):
    e = c["entradas"]
    partes = []
    for k in ("S", "F", "K", "T_expr", "T", "DU", "DC", "DI_aa", "r", "q", "r_d", "r_f", "cupom_lin_aa",
              "sigma", "preco"):
        if k in e:
            if k == "T" and "T_expr" in e:
                continue
            partes.append(f"{k}={fmt(e[k], 6) if not isinstance(e[k], str) else e[k]}")
    return ", ".join(partes)


MD_CABECALHO = """# Vetores de teste do motor de precificação

- **Arquivo de dados:** `precificacao.json` (nesta pasta). **Gerador:** `geradores/gera_precificacao.py`.
- **Gerado em / data de acesso das fontes:** {data}.
- **Como rodar de novo:** `python3 -I geradores/gera_precificacao.py --saida /mnt/project-files/jumba/vetores/`
  (só biblioteca padrão; não baixa nada).
- **Total:** {n_total} casos: {n_pg} de preço e gregas, {n_iv} de vol implícita ({n_iv_ok} com solução e {n_iv_f} que devem falhar), {n_tx} de taxa na convenção B3. {n_pub} valores publicados (Hull e Haug) conferidos.
- **Legenda:** [C] confirmado na fonte; [I] inferência minha; [P] convenção que escolhi para os vetores (o motor pode ter outra, mas aí o vetor precisa ser convertido).

## 1. Como usar

Cada caso tem `id`, `grupo`, `modelo`, `modelo_motor`, `convencao`, `entradas`, `entradas_gbs`, `saidas_esperadas`, `tolerancia`, `origem` e `nota`.

- `entradas` são os dados como o usuário os conhece (por exemplo, `DU` e `DI_aa` na convenção B3, `r_d` e `r_f` no GK).
- `entradas_gbs` já traz tudo convertido para o Black-Scholes generalizado `preco_gbs(tipo, S, K, T, r, b, σ)` da especificação do motor (`../conhecimento/metodologia/especificacao-motor.md` §2.2). No Black-76, o `S` do GBS é o `F`.
- Um teste do motor passa se, para cada campo de `saidas_esperadas`:

  `|obtido − esperado| ≤ max(abs, rel · |esperado|)`

  com `tolerancia.padrao = {{abs: 1e-10, rel: 1e-10}}`, salvo quando `tolerancia.por_campo` disser outra coisa (só o `sigma` de alguns casos de vol implícita).
- `origem.tipo = "publicado+calculado"` quer dizer que o caso também tem o valor do livro em `origem.publicado`. Esse valor é arredondado: ele confere com `saidas_esperadas` dentro de `origem.tolerancia_publicado` (meia unidade da última casa publicada). **O teste do motor deve usar `saidas_esperadas`, não o valor publicado.**
- Campos ausentes não se aplicam ao caso (por exemplo, não há `rho_q` no Black-76).

## 2. Convenções

### 2.1 Modelo único: Black-Scholes generalizado (custo de carregamento b)

$$d_1=\\frac{{\\ln(S/K)+(b+\\tfrac12\\sigma^2)T}}{{\\sigma\\sqrt T}},\\quad d_2=d_1-\\sigma\\sqrt T$$

$$c=S e^{{(b-r)T}}N(d_1)-K e^{{-rT}}N(d_2),\\qquad p=K e^{{-rT}}N(-d_2)-S e^{{(b-r)T}}N(-d_1)$$

| `modelo` | `modelo_motor` | b | Observação |
|---|---|---|---|
| BSM_MERTON com q = 0 | BS_B3 | b = r | Black-Scholes sem dividendo. É o que a B3 usa para ações, ETFs e índices [C, Manual B3 §1.1, via nota 01] |
| BSM_MERTON com q > 0 | BSM_Q | b = r − q | dividendo contínuo (índice à vista, opção não protegida) |
| BLACK76 | BLACK76 | b = 0 e S → F | prêmio pago à vista, descontado por e^{{−rT}} |
| GARMAN_KOHLHAGEN | GK | b = r_d − r_f | dólar à vista; na B3, r_f = cupom cambial |

Isso segue `../conhecimento/metodologia/01-convencoes-base.md` §1.

### 2.2 Tempo, taxa e cupom

- **Hull e Haug:** `T` em anos, como no livro; `r`, `q`, `r_d` e `r_f` são taxas contínuas ao ano.
- **Convenção B3 [C, Manual B3 §1.1 e §2.1, via nota 01]:** `T = DU/252`; `r = ln(1 + DI_aa)`, em que `DI_aa` é a taxa DI ao ano, base 252, capitalização exponencial. Por isso `e^{{−rT}} = (1 + DI)^{{−DU/252}}`.
- **Cupom cambial (GK na B3) [C, Manual B3 §2.1, via nota 01]:** `q = (252/DU) · ln(1 + cupom_lin_aa · DC/360)`.
- **Interpolação da curva (casos `TX-DI-INTERP-*`) [I, nota 01 §3]:** exponencial, ou seja, flat forward 252: `(1+i)^{{DU/252}} = (1+i₁)^{{DU₁/252}} · [(1+i₂)^{{DU₂/252}} / (1+i₁)^{{DU₁/252}}]^{{(DU−DU₁)/(DU₂−DU₁)}}`.

### 2.3 Gregas e unidades

| Campo | Definição | Unidade |
|---|---|---|
| `delta` | ∂V/∂S (∂V/∂F no Black-76) | objeto por opção |
| `gamma` | ∂²V/∂S² (∂²V/∂F² no Black-76) | 1/(unidade de S) |
| `vega` | ∂V/∂σ | por 1,00 de vol (100 p.p.) |
| `vega_pp` | vega/100 | por 1 p.p. de vol |
| `theta_ano` | Θ = ∂V/∂t = −∂V/∂T | por ano (na B3, ano de 252 DU) |
| `theta_du` | Θ/252 | por dia útil |
| `theta_dc` | Θ/365 | por dia corrido (escala do `escala()` da especificação; na convenção B3 é só Θ/365, não um theta de calendário) |
| `theta_1du_exato` (só B3) | V(T − 1/252) − V(T), com S, σ e taxas contínuas fixas | R$ em 1 DU; com DU = 1 dá intrínseco − preço |
| `rho` | ∂V/∂r. BSM: q fixo, então b = r − q anda junto com r. Black-76: F fixo, ρ = −T·V. GK: ∂V/∂r_d | por 1,00 de taxa contínua |
| `rho_pp` | rho/100 | por 1 p.p. de taxa contínua |
| `rho_q` | BSM: ∂V/∂q; GK: ∂V/∂r_f | por 1,00 |
| `rho_di_pp` (só B3) | ∂V/∂DI por 1 p.p. = rho/[100·(1+DI)], porque dr/dDI = 1/(1+DI) | por 1 p.p. da taxa DI ao ano |
| `F_paridade` (GK) | S·e^{{(r−q)T}} | R$/US$ |

`rho_q` só aparece nos casos BSM de Hull/Haug quando q > 0, mas aparece em todos os BSM da convenção B3 (lá ele serve para testar a função do motor mesmo com q = 0).

### 2.4 Vol implícita

- **Limites (`limite_inferior` e `limite_superior`) [C, nota 06 §2]:** call: max(0, S·e^{{(b−r)T}} − K·e^{{−rT}}) < c < S·e^{{(b−r)T}}; put: max(0, K·e^{{−rT}} − S·e^{{(b−r)T}}) < p < K·e^{{−rT}}. Os dois limites são estritos.
- **Falha [P, nota 06 §2]:** fora dos limites, `sigma = null`, `falha = true` e `flags = ["FORA_DOS_LIMITES"]`. O motor pode devolver `NaN`; o teste deve aceitar `NaN` ou `null`.
- **O limite é descontado, não o intrínseco simples.** Dois casos pegam o erro: `IV-FALHA-C-ENTRE-INTRINSECO-E-LIMITE` (acima de S − K e mesmo assim falha) e `IV-P-ABAIXO-INTRINSECO-VALIDO` (abaixo de K − S e mesmo assim tem vol europeia).
- **Preço de entrada:** `entradas.preco` é o double exato que o motor vai ler. O `sigma` esperado foi invertido em 100 dígitos sobre esse mesmo double, não sobre o preço "bonito" que o gerou (`sigma_origem`, só informativo).
- **Tolerância de `sigma`:** abs = max(1e-10, 10^⌈log₁₀(16·ε·M/vega)⌉), com ε = 2,2·10⁻¹⁶ e M = o maior dos dois termos da fórmula do preço (na call, S·e^{{(b−r)T}}·N(d₁) e K·e^{{−rT}}·N(d₂); na put, os termos com N(−d)) ou o próprio preço. Ela só sai de 1e-10 quando a vega é minúscula perto de termos grandes (casos muito dentro do dinheiro), porque aí um ulp do preço já move σ. Nos casos muito fora do dinheiro os dois termos são pequenos e a tolerância continua 1e-10: o motor precisa calcular o preço direto pela fórmula da própria opção, e não pela paridade a partir da opção dentro do dinheiro. Nesses casos vale também `tolerancia.preco_reprecificado`: o preço do motor no σ obtido tem de bater com `entradas.preco` em 1e-10.
- **Faixa de busca:** todos os σ esperados ficam entre 0,02 e 2,5, dentro do intervalo [0,001; 5] da nota 06.
- A flag `PRECO_MINIMO` (preço ≤ 2 ticks) depende do tick e da configuração; os vetores não a exigem.

## 3. Avisos

- **Proventos em opções de ações da B3:** a B3 ajusta o strike pelos proventos em dinheiro. Usar ao mesmo tempo o strike ajustado e um dividend yield q > 0 conta o provento duas vezes (`../pesquisa/critic.md`, item 8; `../conhecimento/metodologia/02-bsm-merton-proventos.md`). Por isso os casos de ação na convenção B3 usam q = 0. O caso `B3-INDICE-BSMQ-42DU` existe só para testar o BSM com q na base DU/252; o q dele é ilustrativo.
- **Americanas:** todos os vetores são europeus. Puts americanas de ações precisam de árvore ou BAW (nota 06 §7); não há vetor para isso aqui.
- **Valores publicados:** os números do Hull e do Haug foram transcritos dos livros impressos (não há URL; não baixei nada). Cada um foi conferido por recálculo: todos batem dentro de meia unidade da última casa publicada. A numeração dos exemplos é a da 9ª edição do Hull e pode mudar em outras edições [I]. Os capítulos do Haug citados são da 2ª edição [I].
- **Hull arredonda passos intermediários** (N(d₁) e N(d₂) com 4 casas). Por isso alguns valores intermediários que ele imprime (por exemplo, d₁ = 0,5444 no Example 17.1) não entram como "publicado".

## 4. Como os valores foram calculados e conferidos

1. Referência em `decimal.Decimal` com 100 dígitos: π por Machin, erf pela série de termos positivos e cauda da normal pela série assintótica de Mills para |x| > 14. O mpmath não está instalado e não instalei nada.
2. Toda grega analítica foi conferida por diferença finita central em 100 dígitos (h = 10⁻³⁰; 10⁻²² no gamma), com erro relativo < 10⁻³⁰.
3. Todo caso de preço passou na EDP Θ + ½σ²S²Γ + bSΔ − rV = 0 e na paridade c − p = S·e^{{(b−r)T}} − K·e^{{−rT}}, ambas com resíduo < 10⁻⁸⁰.
4. Black-76 sobre F = S·e^{{(r−q)T}} reproduz o GK (`B3-DOL-B76-EQUIV-*`, diferença < 10⁻¹⁵).
5. Uma implementação independente em double (`math.erfc`, Newton protegido por bissecção) passou em todos os casos com as tolerâncias gravadas. Maior erro relativo nas gregas: {pior_double:.1e}. Maior erro de σ: {pior_iv:.1e}.
6. Os vetores de 6 casas das notas 03, 04 e 05 da metodologia batem com estes ({n_metod} valores conferidos).

## 5. Fontes

- {ref_hull}.
- {ref_haug}.
- {ref_b3}.
- Notas de metodologia usadas para as convenções (lidas em {data}): `/mnt/project-files/jumba/conhecimento/metodologia/01-convencoes-base.md`, `02-bsm-merton-proventos.md`, `03-black76-futuros.md`, `04-garman-kohlhagen-dolar.md`, `05-gregas-escalas.md`, `06-vol-implicita.md` e `especificacao-motor.md`.
- Revisão cética: `/mnt/project-files/jumba/pesquisa/critic.md` (item 8, proventos).

## 6. Casos
"""


def gera_md(casos, info):
    linhas = [MD_CABECALHO.format(**info)]
    grupos = [("preco_gregas", "### 6.1 Preço e gregas",
               "| id | modelo | entradas | preço | delta | gamma | vega | theta/ano | rho | origem |\n"
               "|---|---|---|---|---|---|---|---|---|---|"),
              ("vol_implicita", "### 6.2 Vol implícita",
               "| id | modelo | entradas | σ esperado | tol. σ | falha | limites | origem |\n"
               "|---|---|---|---|---|---|---|---|"),
              ("taxa_b3", "### 6.3 Taxas na convenção B3",
               "| id | função | entradas | saídas |\n|---|---|---|---|")]
    for g, titulo, cab in grupos:
        linhas += ["", titulo, "", cab]
        for c in casos:
            if c["grupo"] != g:
                continue
            s = c["saidas_esperadas"]
            o = c["origem"]
            orig = "publicado: " + ", ".join(f"{k}={fmt(v, 6)}" for k, v in o["publicado"].items()) \
                if "publicado" in o else "calculado"
            if g == "preco_gregas":
                linhas.append(f"| {c['id']} | {c['modelo_motor']} | {resumo_entradas(c)} | {fmt(s['preco'])} | "
                              f"{fmt(s.get('delta'))} | {fmt(s.get('gamma'))} | {fmt(s.get('vega'))} | "
                              f"{fmt(s.get('theta_ano'))} | {fmt(s.get('rho'))} | {orig} |")
            elif g == "vol_implicita":
                ts = c["tolerancia"].get("por_campo", {}).get("sigma", {}).get("abs")
                linhas.append(f"| {c['id']} | {c['modelo_motor']} | {resumo_entradas(c)} | {fmt(s['sigma'], 12)} | "
                              f"{fmt(ts, 0) if ts else '—'} | {fmt(s['falha'])} | "
                              f"({fmt(s['limite_inferior'], 6)}; {fmt(s['limite_superior'], 6)}) | {orig} |")
            else:
                ent = ", ".join(f"{k}={v}" for k, v in c["entradas"].items())
                sai = ", ".join(f"{k}={fmt(v, 12)}" for k, v in s.items())
                linhas.append(f"| {c['id']} | `{c['funcao_motor']}` | {ent} | {sai} |")
    linhas += ["", "As notas de cada caso (por que ele existe e o que testa) estão no campo `nota` do JSON.", ""]
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
def grava_e_confere(caminho, texto):
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(texto)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", required=True, help="pasta de saída (com barra no fim)")
    ap.add_argument("--espera", type=float, default=10.0,
                    help="segundos antes de reler os arquivos (mount de rede)")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)

    verif = {"publicados": 0, "edp_paridade_dif": 0, "iv_ok": 0, "iv_falha": 0, "taxa": 0,
             "iv_double_erro_max": 0.0}
    casos = []
    gk_set = None
    for p in CONJUNTOS:
        for tipo in ("C", "P"):
            caso, _ = caso_preco(p, tipo, verif)
            casos.append(caso)
        if p["id"] == "B3-DOL-GK-20DU":
            gk_set = p
    casos += caso_b76_equivalente(gk_set, verif)
    casos += [caso_iv(c, verif) for c in IV_CASOS]
    casos += casos_taxa(verif)

    ids = [c["id"] for c in casos]
    checa(len(ids) == len(set(ids)), "ids repetidos")
    n_metod = confere_metodologia(casos)
    pior_double = confere_double(casos)

    doc = {
        "descricao": "Vetores de teste do motor de precificação de opções (BSM-Merton, Black-76, "
                     "Garman-Kohlhagen, gregas e vol implícita). Ver precificacao.md.",
        "versao": 1,
        "gerado_em": DATA_ACESSO,
        "gerador": "geradores/gera_precificacao.py",
        "regra_tolerancia": "|obtido - esperado| <= max(abs, rel*|esperado|); usar tolerancia.por_campo "
                            "quando existir, senão tolerancia.padrao. sigma null = deve falhar.",
        "convencoes": {
            "modelo": "Black-Scholes generalizado com custo de carregamento b (entradas_gbs)",
            "tempo_b3": "T = DU/252",
            "taxa_b3": "r = ln(1 + DI_aa), DI base 252 exponencial",
            "cupom_b3": "q = (252/DU)*ln(1 + cupom_lin_aa*DC/360)",
            "theta": "theta_ano = dV/dt = -dV/dT; theta_du = theta_ano/252; theta_dc = theta_ano/365",
            "vega": "por 1,00 de vol; vega_pp = vega/100",
            "rho": "BSM: dV/dr com q fixo; BLACK76: -T*V com F fixo; GK: dV/dr_d. rho_q: dV/dq ou dV/dr_f",
            "rho_di_pp": "rho/(100*(1+DI_aa))",
            "theta_1du_exato": "V(T-1/252) - V(T), taxas contínuas e sigma fixos",
            "vol_implicita_falha": "sigma null, falha true, flags [FORA_DOS_LIMITES]",
        },
        "casos": casos,
    }
    texto_json = json.dumps(doc, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    info = dict(data=DATA_ACESSO, n_total=len(casos),
                n_pg=sum(c["grupo"] == "preco_gregas" for c in casos),
                n_iv=sum(c["grupo"] == "vol_implicita" for c in casos),
                n_iv_ok=verif["iv_ok"], n_iv_f=verif["iv_falha"], n_tx=verif["taxa"],
                n_pub=verif["publicados"], pior_double=pior_double, pior_iv=verif["iv_double_erro_max"],
                n_metod=n_metod, ref_hull=REF_HULL, ref_haug=REF_HAUG, ref_b3=REF_MANUAL_B3)
    texto_md = gera_md(casos, info)

    arq = {os.path.join(a.saida, "precificacao.json"): texto_json,
           os.path.join(a.saida, "precificacao.md"): texto_md}
    hashes = {c: grava_e_confere(c, t) for c, t in arq.items()}
    time.sleep(a.espera)
    for c, h in hashes.items():
        with open(c, "r", encoding="utf-8") as fh:
            lido = fh.read()
        checa(hashlib.sha256(lido.encode("utf-8")).hexdigest() == h, f"releitura diferente: {c}")
    json.loads(open(os.path.join(a.saida, "precificacao.json"), encoding="utf-8").read())
    print(json.dumps({"casos": len(casos), **info, **verif,
                      "arquivos": list(hashes)}, ensure_ascii=False, default=str, indent=1))


if __name__ == "__main__":
    main()
