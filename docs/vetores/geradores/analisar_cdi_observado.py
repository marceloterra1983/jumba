#!/usr/bin/env python3
"""Testa hipóteses de convenção para dois valores de "CDI no período" lidos numa tela de terceiro.

RETIDO: os dois números (0,3413 % e 0,5656 %) foram lidos na tela de um produto de terceiros.
Este resultado NÃO deve virar vetor de teste do motor até decisão do Marcelo. O motor usa
apenas as convenções públicas (ver agregados.json, caso taxas_cdi, campo cdi_do_periodo_por_convencao).

Uso: python3 -I analisar_cdi_observado.py [--saida DIR]   (DIR padrão: ../retido/)
Só biblioteca padrão; aritmética em Decimal com 40 dígitos.
"""
import argparse
import datetime as dt
import json
import os
from decimal import Decimal as Dd, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN

getcontext().prec = 40
D = dt.date
UM = dt.timedelta(days=1)

# --- calendário mínimo (mesmas regras do gerar_agregados.py) ---------------------
def pascoa(a):
    g = a % 19; b, c = divmod(a, 100); d, e = divmod(b, 4); f = (b + 8) // 25; h0 = (b - f + 1) // 3
    h = (19 * g + b - d - h0 + 15) % 30; i, k = divmod(c, 4); l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (g + 11 * h + 22 * l) // 451; mes, dia = divmod(h + l - 7 * m + 114, 31)
    return D(a, mes, dia + 1)


def sem_pregao(a):
    p = pascoa(a)
    s = {D(a, m, d) for m, d in [(1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (11, 20), (12, 24), (12, 25), (12, 31)]}
    s |= {p - 48 * UM, p - 47 * UM, p - 2 * UM, p + 60 * UM}
    return s


def util(d):
    return d.weekday() < 5 and d not in sem_pregao(d.year)


def du(d0, d1):
    n, d = 0, d0 + UM
    while d <= d1:
        n += util(d)
        d += UM
    return n


def proxima_sessao(d, k=1):
    while k:
        d += UM
        if util(d):
            k -= 1
    return d


# --- dados observados (retidos) --------------------------------------------------
OBS = {
    "venda_coberta": {"valor_pct": Dd("0.3413"), "vencimento": D(2026, 11, 13), "nota": "9 dias corridos (dado do Marcelo)"},
    "cash_put": {"valor_pct": Dd("0.5656"), "vencimento": D(2026, 11, 19), "nota": "15 dias corridos e 11 úteis (dado do Marcelo)"},
}
HOJE = D(2026, 11, 4)  # [S] data da leitura; bate com 9 e 15 dias corridos até os vencimentos de 13/11 e 19/11
TAXAS = {"CDI_13_65": Dd("0.1365"), "SELIC_META_13_75": Dd("0.1375")}


def exp(x):
    return x.exp()


def ln(x):
    return x.ln()


def formas(taxa, dc, du_):
    t = taxa
    return {
        "LIN360_DC": t * dc / 360,
        "LIN365_DC": t * dc / 365,
        "LIN252_DU": t * du_ / 252,
        "EXP252_DU": exp(ln(1 + t) * du_ / 252) - 1,
        "EXP360_DC": exp(ln(1 + t) * dc / 360) - 1,
        "EXP365_DC": exp(ln(1 + t) * dc / 365) - 1,
        "COMP_DIARIA_360_DC": exp(ln(1 + t / 360) * dc) - 1,
        "COMP_DIARIA_365_DC": exp(ln(1 + t / 365) * dc) - 1,
        "DESCONTO_LIN360_DC": 1 - 1 / (1 + t * dc / 360),
    }


def arred(x_pct, modo):
    return x_pct.quantize(Dd("0.0001"), rounding=modo)


def janelas(venc):
    """Variações do prazo: data inicial e final (liquidação)."""
    ini = {"D0_leitura": HOJE, "D1_liq_premio": proxima_sessao(HOJE, 1), "D2_liq_acao": proxima_sessao(HOJE, 2)}
    fim = {"vencimento": venc, "venc_D1": proxima_sessao(venc, 1), "venc_D2": proxima_sessao(venc, 2)}
    out = []
    for ki, a in ini.items():
        for kf, b in fim.items():
            out.append({"inicio": ki, "fim": kf, "d0": a, "d1": b, "dc": (b - a).days, "du": du(a, b)})
    return out


def analisa():
    res = {}
    for nome, o in OBS.items():
        alvo = o["valor_pct"]
        linhas, fecham, perto = [], [], []
        for jn in janelas(o["vencimento"]):
            for tn, t in TAXAS.items():
                for fn, v in formas(t, jn["dc"], jn["du"]).items():
                    pct = v * 100
                    up, ev = arred(pct, ROUND_HALF_UP), arred(pct, ROUND_HALF_EVEN)
                    l = {"janela": f'{jn["inicio"]}->{jn["fim"]}', "dc": jn["dc"], "du": jn["du"], "taxa": tn, "forma": fn,
                         "valor_pct": float(pct), "arred_half_up": float(up), "arred_half_even": float(ev),
                         "dif_pp": float(pct - alvo)}
                    linhas.append(l)
                    if up == alvo or ev == alvo:
                        fecham.append(l)
        perto = sorted(linhas, key=lambda l: abs(l["dif_pp"]))[:8]
        # taxa implícita para cada forma no prazo D0 -> vencimento
        jn = janelas(o["vencimento"])[0]
        dc, du_ = jn["dc"], jn["du"]
        x = alvo / 100
        impl = {
            "LIN360_DC": x * 360 / dc,
            "LIN365_DC": x * 365 / dc,
            "LIN252_DU": x * 252 / du_,
            "EXP252_DU": exp(ln(1 + x) * 252 / du_) - 1,
            "EXP360_DC": exp(ln(1 + x) * 360 / dc) - 1,
            "EXP365_DC": exp(ln(1 + x) * 365 / dc) - 1,
        }
        # parâmetro livre: prazo fracionário com a taxa de 13,65 %
        t = TAXAS["CDI_13_65"]
        prazo_frac = {
            "LIN360_dias_corridos": x * 360 / t,
            "EXP252_dias_uteis": ln(1 + x) / ln(1 + t) * 252,
        }
        res[nome] = {"alvo_pct": float(alvo), "vencimento": o["vencimento"].isoformat(), "nota": o["nota"],
                     "prazo_D0_venc": {"dc": dc, "du": du_},
                     "hipoteses_que_fecham": fecham, "mais_proximas": perto,
                     "taxa_implicita_aa_por_forma": {k: float(v) for k, v in impl.items()},
                     "prazo_fracionario_com_13_65": {k: float(v) for k, v in prazo_frac.items()},
                     "n_hipoteses_testadas": len(linhas)}
    # parâmetro livre: relação prêmio/strike que fecharia o cash put
    cp = OBS["cash_put"]["valor_pct"] / 100
    t = TAXAS["CDI_13_65"]
    bases = {"LIN360_DC": t * 15 / 360, "LIN365_DC": t * 15 / 365, "EXP252_DU": exp(ln(1 + t) * 11 / 252) - 1}
    razao = {}
    for k, b in bases.items():
        # exibido = base·(K−P)/K  →  P/K = 1 − exibido/base ;  exibido = base·K/(K−P) → P/K = 1 − base/exibido
        razao[k] = {"base_pct": float(b * 100),
                    "P_sobre_K_se_exibido_igual_base_vezes_(K-P)/K": float(1 - cp / b),
                    "P_sobre_K_se_exibido_igual_base_vezes_K/(K-P)": float(1 - b / cp)}
    res["cash_put_parametro_P_sobre_K"] = razao
    # conferência: alguma combinação fecha os DOIS números com os mesmos parâmetros?
    chave = lambda l: (l["janela"].split("->")[0], l["janela"].split("->")[1], l["taxa"], l["forma"])
    a = {chave(l) for l in res["venda_coberta"]["hipoteses_que_fecham"]}
    b = {chave(l) for l in res["cash_put"]["hipoteses_que_fecham"]}
    res["fecham_os_dois"] = sorted(list(a & b))
    return res


def br(x, n=4, sinal=False):
    t = f"{x:+,.{n}f}" if sinal else f"{x:,.{n}f}"
    return t.replace(",", "§").replace(".", ",").replace("§", ".")


def render_md(r):
    def f4(x):
        return br(x, 4)
    vc, cp = r["venda_coberta"], r["cash_put"]
    L = []
    L.append("# CDI do período: hipóteses para dois números observados (RETIDO)")
    L.append("")
    L.append("- **Data:** 2026-11-04. Gerado por `../geradores/analisar_cdi_observado.py` (`python3 -I`).")
    L.append("- **Status: retido.** Os dois números foram lidos numa tela de produto de terceiros. Em 04/11, às 23h14, o coordenador suspendeu o uso de números lidos nessas telas em testes do motor, por causa dos termos de uso do site. **Não copie estes números para testes nem para o código** até o Marcelo decidir. O motor usa só convenções públicas (`../agregados.json`, caso `taxas_cdi`).")
    L.append("- **Fonte:** leitura do Marcelo (sem URL; tela logada). Nenhum acesso novo foi feito para esta análise.")
    L.append("- **Suposição [S]:** a leitura foi em 04/11/2026; os prazos batem com os vencimentos de 13/11/2026 (semanal, 9 dias corridos, 7 úteis) e 19/11/2026 (mensal de novembro, antecipado porque 20/11 é feriado; 15 corridos, 11 úteis).")
    L.append("")
    L.append("## Resultado")
    L.append("")
    fv = [h for h in vc["hipoteses_que_fecham"]]
    L.append(f"- **Venda coberta, {f4(vc['alvo_pct'])} %:** {len(fv)} combinação(ões) fecham de {vc['n_hipoteses_testadas']} testadas.")
    for h in fv:
        L.append(f"  - {h['forma']}, {h['taxa']}, prazo {h['janela']} ({h['dc']} DC, {h['du']} DU): {br(h['valor_pct'], 6)} % → half-up {f4(h['arred_half_up'])}, half-even {f4(h['arred_half_even'])}.")
    L.append("  - O valor exato é 0,34125 %. Só vira 0,3413 com arredondamento *half-up* (com *half-even* daria 0,3412).")
    fc = cp["hipoteses_que_fecham"]
    if fc:
        L.append(f"- **Cash put, {f4(cp['alvo_pct'])} %:** fecharam {len(fc)} combinação(ões):")
        for h in fc:
            L.append(f"  - {h['forma']}, {h['taxa']}, {h['janela']} ({h['dc']} DC, {h['du']} DU): {br(h['valor_pct'], 6)} %")
    else:
        L.append(f"- **Cash put, {f4(cp['alvo_pct'])} %: nenhuma hipótese fechou** ({cp['n_hipoteses_testadas']} combinações de taxa, forma e prazo, com dias inteiros).")
    L.append(f"- **Os dois com os mesmos parâmetros:** {'nenhuma combinação' if not r['fecham_os_dois'] else r['fecham_os_dois']}.")
    L.append("")
    L.append("## O que foi testado")
    L.append("")
    L.append("- **Taxas:** CDI 13,65 % a.a. (a que fechou a venda coberta) e Selic meta 13,75 % a.a.")
    L.append("- **Formas:** linear 360 e 365 sobre dias corridos; linear 252 sobre dias úteis; exponencial 252 (DU), 360 e 365 (DC); capitalização diária 360 e 365; desconto linear 360.")
    L.append("- **Prazos (\"dias até a liquidação\"):** início na leitura (D0), na liquidação do prêmio (D+1) ou da ação (D+2); fim no vencimento, em venc+1 ou venc+2 sessões. Calendário B3 (20/11 sem pregão).")
    L.append("- **Arredondamento:** 4 casas em %, *half-up* e *half-even*.")
    L.append("")
    L.append("## As mais próximas do cash put")
    L.append("")
    L.append("| Forma | Taxa | Prazo | DC | DU | Valor (%) | Diferença (p.p.) |")
    L.append("|---|---|---|---|---|---|---|")
    for h in cp["mais_proximas"]:
        L.append(f"| {h['forma']} | {h['taxa']} | {h['janela']} | {h['dc']} | {h['du']} | {br(h['valor_pct'], 6)} | {br(h['dif_pp'], 6, True)} |")
    L.append("")
    L.append("## Hipóteses com parâmetro livre (fecham, mas não dá para confirmar)")
    L.append("")
    ti = cp["taxa_implicita_aa_por_forma"]
    L.append("**Outra taxa.** Taxa anual que daria exatamente 0,5656 % em 15 DC / 11 DU:")
    L.append("")
    for k, v in ti.items():
        L.append(f"- {k}: {br(v*100, 4)} % a.a.")
    L.append("")
    L.append("Nenhuma é uma taxa \"redonda\" nem igual à que fechou a venda coberta. A de EXP252_DU (cerca de 13,79 %) só valeria se a curva DI no vértice de 11 DU estivesse acima do CDI; dá para conferir no arquivo TS da B3 de 04/11/2026.")
    L.append("")
    pf = cp["prazo_fracionario_com_13_65"]
    horas = (15 - pf['LIN360_dias_corridos']) * 24
    L.append(f"**Prazo fracionário.** Com 13,65 %, fecharia com {br(pf['LIN360_dias_corridos'], 4)} dias corridos na forma linear 360 (15 dias menos cerca de {br(horas, 1)} horas; a janela de arredondamento tem uns 4 minutos) ou com {br(pf['EXP252_dias_uteis'], 4)} DU na exponencial 252. Isso exigiria contar horas até o horário de corte do vencimento; na venda coberta, porém, o prazo inteiro de 9 dias fechou.")
    L.append("")
    L.append("**Capital da garantia.** Se a tela aplicasse o CDI do período sobre outra base de capital, a relação prêmio/strike (P/K) teria de ser:")
    L.append("")
    L.append("| Base do CDI | CDI do período (%) | P/K se exibido = base·(K−P)/K | P/K se exibido = base·K/(K−P) |")
    L.append("|---|---|---|---|")
    for k, v in r["cash_put_parametro_P_sobre_K"].items():
        a = v["P_sobre_K_se_exibido_igual_base_vezes_(K-P)/K"]
        b = v["P_sobre_K_se_exibido_igual_base_vezes_K/(K-P)"]
        L.append(f"| {k} | {br(v['base_pct'], 6)} | {'impossível (negativo)' if a < 0 else br(a*100, 4) + ' %'} | {'impossível (negativo)' if b < 0 else br(b*100, 4) + ' %'} |")
    L.append("")
    L.append("Coerente com a venda coberta (forma LIN360_DC), só a variante base·(K−P)/K fecha, e pede P/K = 0,5538 %. Com o strike e o prêmio da put da leitura, isso se testa na hora.")
    L.append("")
    L.append("## Dados que decidiriam")
    L.append("")
    L.append("1. Strike e prêmio da put no momento da leitura (testa as hipóteses de P/K).")
    L.append("2. Horário da leitura (testa o prazo fracionário).")
    L.append("3. Uma segunda leitura do cash put em outro dia ou outro vencimento (separa taxa de prazo).")
    L.append("4. O arquivo TS (curva PRE) da B3 de 04/11/2026 (testa a taxa da curva no vértice).")
    L.append("")
    L.append("Todos os números estão em `cdi-observado.json`.")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    aqui = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--saida", default=os.path.join(os.path.dirname(aqui), "retido"))
    a = ap.parse_args()
    r = analisa()
    doc = {"titulo": "CDI do período: hipóteses para dois números observados (RETIDO)",
           "status": "retido: números lidos em tela de terceiros; não usar em testes do motor até decisão do Marcelo",
           "data": "2026-11-04", "gerado_por": "geradores/analisar_cdi_observado.py", "resultado": r}
    os.makedirs(a.saida, exist_ok=True)
    pj = os.path.join(a.saida, "cdi-observado.json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, default=str)
        f.write("\n")
    pm = os.path.join(a.saida, "cdi-observado.md")
    with open(pm, "w", encoding="utf-8") as f:
        f.write(render_md(r))
    print(pj)
    print(pm)


if __name__ == "__main__":
    main()
