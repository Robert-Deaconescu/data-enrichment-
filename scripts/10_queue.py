#!/usr/bin/env python3
"""Construieste coada de verificare Reoon si calculeaza necesarul de credite.
Scrie: work/10_coada_tipare.csv, work/10_coada_scrape.csv,
       work/10_coada_generice.csv, work/10_necesar_credite.md"""
import os
import re

import pandas as pd
from unidecode import unidecode

df = pd.read_csv("work/04_imbogatit.csv", dtype=str).fillna("")
tip = pd.read_csv("work/05_tipare.csv", dtype=str).fillna("")
ver = pd.read_csv("work/06_verificari.csv", dtype=str).fillna("") if os.path.exists("work/06_verificari.csv") else pd.DataFrame(columns=["id_firma", "email", "status"])
scr = pd.read_csv("work/07_scrape.csv", dtype=str).fillna("") if os.path.exists("work/07_scrape.csv") else pd.DataFrame(columns=["id_firma", "emailuri"])

CALIB_CREDITS_PER_FIRM = 4.4  # din esantionul de calibrare

verified_ok = set(ver[ver["status"].isin(["valid", "safe"])]["id_firma"])
tried = ver.groupby("id_firma")["email"].apply(set).to_dict() if len(ver) else {}

# A. tipare ramase de verificat
rows_t = []
for _, r in tip.iterrows():
    fid = r["id_firma"]
    if fid in verified_ok:
        continue
    pats = [p for p in r["tipare"].split(";") if p not in tried.get(fid, set())]
    if pats:
        rows_t.append({"id_firma": fid, "tipare": ";".join(pats), "nr": len(pats)})
qt = pd.DataFrame(rows_t)
qt.to_csv("work/10_coada_tipare.csv", index=False)

# B. adrese din scraping (max 3/firma, preferam pe cele cu numele persoanei)
pers = df.set_index("id_firma")["persoana_fin"].to_dict()
doms = df.set_index("id_firma")["domeniu"].to_dict()
GENERIC_LOCAL = {"office", "contact", "info", "secretariat", "comenzi", "vanzari",
                 "sales", "hr", "recrutare", "marketing", "press", "gdpr"}
rows_s = []
for _, r in scr.iterrows():
    fid = r["id_firma"]
    ems = [e for e in r["emailuri"].split(";") if e]
    if not ems:
        continue
    p = unidecode(pers.get(fid, "")).lower().replace("-", " ").split()
    def score(e):
        local = e.split("@")[0].lower()
        s = 0
        if any(tok in local for tok in p if len(tok) > 2):
            s += 10  # contine numele decidentului
        if re.match(r"^[a-z]+\.[a-z]+$", local):
            s += 5   # forma prenume.nume
        if local in GENERIC_LOCAL:
            s -= 5
        return -s
    ems = sorted(set(ems), key=score)[:3]
    nominal = [e for e in ems if score(e) < 0]
    rows_s.append({"id_firma": fid, "emailuri": ";".join(ems),
                   "nominale_probabile": ";".join(nominal), "nr": len(ems)})
qs = pd.DataFrame(rows_s)
qs.to_csv("work/10_coada_scrape.csv", index=False)

# C. generice existente care intra in campanie (re-verificare finala)
gen = df[(df["status"] == "Pending") & (df["email1"] != "")][["id_firma", "email1"]]
gen.to_csv("work/10_coada_generice.csv", index=False)

# calcul credite
c_tipare = int(len(qt) * CALIB_CREDITS_PER_FIRM) if len(qt) else 0
c_scrape = int(qs["nr"].astype(int).sum()) if len(qs) else 0
c_gen = len(gen)
total = c_tipare + c_scrape + c_gen
with open("work/10_necesar_credite.md", "w") as f:
    f.write(f"""# Necesar credite Reoon

| Coada | Firme/adrese | Credite estimate |
|---|---|---|
| Tipare nominale ({len(qt)} firme x ~{CALIB_CREDITS_PER_FIRM}) | {len(qt)} firme | {c_tipare} |
| Adrese din scraping (max 3/firma) | {len(qs)} firme | {c_scrape} |
| Re-verificare generice campanie | {c_gen} adrese | {c_gen} |
| **TOTAL estimat** | | **{total}** |

Marja de siguranta recomandata: +20% -> ~{int(total*1.2)} credite.
Pachet recomandat: 10.000 credite instant = $11.90 (nu expira).
""")
print(f"tipare: {len(qt)} firme (~{c_tipare} cr) | scrape: {len(qs)} firme ({c_scrape} cr) | generice: {c_gen} cr | TOTAL ~{total} cr")
