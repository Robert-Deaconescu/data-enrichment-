#!/usr/bin/env python3
"""Pasul 5 - Verificare tipare cu Reoon Email Verifier.
Verifica tiparele IN ORDINE si se opreste la primul valid/safe per firma.
Checkpoint: work/06_verificari.csv (toate verificarile individuale).
Necesita REOON_API_KEY in .env.

Utilizare:
    python3 scripts/06_verify_reoon.py [--max-firme N] [--input FISIER]
    --max-firme N : proceseaza doar primele N firme fara rezultat (esantion)
    --input       : implicit work/05_tipare.csv
"""
import argparse
import csv
import os
import sys
import time

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.environ.get("REOON_API_KEY", "")
if not KEY:
    sys.exit("REOON_API_KEY lipseste din .env - adauga cheia si reia.")

VERIF = "work/06_verificari.csv"
API = "https://emailverifier.reoon.com/api/v1/verify"
DELAY = 0.6

ap = argparse.ArgumentParser()
ap.add_argument("--max-firme", type=int, default=0)
ap.add_argument("--input", default="work/05_tipare.csv")
args = ap.parse_args()

df = pd.read_csv(args.input, dtype=str).fillna("")

seen = {}          # email -> status (nu re-verifica)
firm_done = set()  # id_firma cu rezultat final (valid sau epuizat)
if os.path.exists(VERIF):
    v = pd.read_csv(VERIF, dtype=str).fillna("")
    for _, r in v.iterrows():
        seen[r["email"]] = r["status"]
    for fid, g in v.groupby("id_firma"):
        sts = set(g["status"])
        if "valid" in sts or "safe" in sts:
            firm_done.add(fid)

new_file = not os.path.exists(VERIF)
fout = open(VERIF, "a", newline="")
w = csv.DictWriter(fout, fieldnames=["id_firma", "email", "status", "is_catch_all", "credite"])
if new_file:
    w.writeheader()

# firmele care si-au epuizat toate tiparele fara valid
if not new_file:
    v = pd.read_csv(VERIF, dtype=str).fillna("")
    for _, r in df.iterrows():
        fid = r["id_firma"]
        if fid in firm_done:
            continue
        pats = r["tipare"].split(";")
        tried = set(v[v["id_firma"] == fid]["email"])
        if all(p in tried for p in pats):
            firm_done.add(fid)

todo = df[~df["id_firma"].isin(firm_done)]
if args.max_firme:
    todo = todo.head(args.max_firme)

print(f"De verificat: {len(todo)} firme (din {len(df)})", flush=True)
credits_used = 0
found = 0

for n, (_, r) in enumerate(todo.iterrows()):
    fid = r["id_firma"]
    got_valid = False
    for email in r["tipare"].split(";"):
        if email in seen:
            st = seen[email]
        else:
            try:
                resp = requests.get(API, params={"email": email, "key": KEY, "mode": "power"}, timeout=45)
                time.sleep(DELAY)
                d = resp.json() if resp.status_code == 200 else {}
            except Exception:
                time.sleep(3)
                continue
            st = d.get("status", "error")
            catch = d.get("is_catch_all_email", d.get("is_catch_all", ""))
            credits_used += 1
            seen[email] = st
            w.writerow({"id_firma": fid, "email": email, "status": st,
                        "is_catch_all": catch, "credite": 1})
            fout.flush()
        if st in ("valid", "safe"):
            got_valid = True
            found += 1
            break
        # catch-all / risky: nu continua tiparele - domeniul accepta orice
        if st == "catch_all":
            break
    if (n + 1) % 25 == 0:
        print(f"  {n+1}/{len(todo)} firme, {credits_used} credite, {found} adrese valide", flush=True)

fout.close()
print(f"GATA: {credits_used} credite consumate acum, {found} firme cu adresa valida noua", flush=True)
