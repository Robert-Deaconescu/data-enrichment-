#!/usr/bin/env python3
"""Runda de recuperare: pentru firmele fara domeniu validat, gaseste candidati
de domeniu (din nume) care au MX activ - chiar daca nu au site sau site-ul nu
a putut fi validat. Acestia merg la verificare Reoon cu regula:
- tipar cu numele administratorului valid (non catch-all) => nominal acceptat
- doar office@ valid => generic marcat 'incert' (decizia clientului)
Scrie work/11_candidati_mx.csv"""
import re
from concurrent.futures import ThreadPoolExecutor

import dns.resolver
import pandas as pd
from unidecode import unidecode

GENERIC = {"COM", "PROD", "SERV", "SERVICE", "SERVICII", "GRUP", "GROUP", "TRANS",
           "ROMANIA", "RO", "IMPEX", "EXIM", "COMPANY", "INTERNATIONAL", "INDUSTRY",
           "INDUSTRIES", "CONSTRUCT", "CONSULTING", "TRADING", "HOLDING", "AGRO"}
TLDS = [".ro", ".com", ".eu", ".net"]


def toks(name):
    s = unidecode(str(name)).upper()
    s = re.sub(r"\b(SRL|SA|PFA|SCS|SNC|SRL-D|II|IF)\b", "", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return [t for t in s.split() if len(t) >= 2]


def candidates(name):
    t = toks(name)
    if not t:
        return []
    joined = "".join(t).lower()
    hyphen = "-".join(t).lower()
    bases = []
    if len(joined) <= 24:
        bases.append(joined)
    if len(t) > 1 and len(hyphen) <= 26:
        bases.append(hyphen)
    if t[0] not in GENERIC and len(t[0]) >= 4:
        bases.append(t[0].lower())
    if len(t) >= 2:
        b2 = "".join(t[:2]).lower()
        if b2 not in bases and len(b2) <= 20:
            bases.append(b2)
    seen, out = set(), []
    for b in bases:
        for tld in TLDS:
            d = b + tld
            if d not in seen:
                seen.add(d)
                out.append(d)
    return out

resolver = dns.resolver.Resolver()
resolver.timeout = 1.5
resolver.lifetime = 2.5


def mx_ok(dom):
    try:
        return len(resolver.resolve(dom, "MX")) > 0
    except Exception:
        return False


df = pd.read_csv("work/04_imbogatit.csv", dtype=str).fillna("")
todo = df[(df["status"] == "Pending") & (df["domeniu"] == "")]
print(f"Firme fara domeniu: {len(todo)}", flush=True)

rows = []
with ThreadPoolExecutor(max_workers=24) as ex:
    for n, (_, r) in enumerate(todo.iterrows()):
        cands = candidates(r["firma"])[:6]
        oks = [d for d, ok in zip(cands, ex.map(mx_ok, cands)) if ok]
        if oks:
            rows.append({"id_firma": r["id_firma"], "firma": r["firma"],
                         "persoana": r["persoana_fin"],
                         "candidati_mx": ";".join(oks[:2])})
        if (n + 1) % 200 == 0:
            print(f"  {n+1}/{len(todo)}, {len(rows)} cu MX", flush=True)

out = pd.DataFrame(rows)
out.to_csv("work/11_candidati_mx.csv", index=False)
n_pats = sum(2 + (3 if r["persoana"] else 0) * len(r["candidati_mx"].split(";")) for _, r in out.iterrows())
print(f"GATA: {len(out)} firme cu candidati MX; estimare verificari: ~{n_pats}", flush=True)
