#!/usr/bin/env python3
"""Pasul 5 (paralel) - Verificare Reoon cu pool de threaduri.
Aceeasi logica waterfall ca 06_verify_reoon.py (stop la primul valid/safe sau
catch_all per firma), dar firmele ruleaza concurent (8 workeri).
Checkpoint comun: work/06_verificari.csv - compatibil cu rularile anterioare.

Utilizare:
    python3 scripts/06b_verify_parallel.py --input FISIER [--max-firme N] [--workers N]
"""
import argparse
import csv
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.environ.get("REOON_API_KEY", "")
if not KEY:
    sys.exit("REOON_API_KEY lipseste din .env - adauga cheia si reia.")

VERIF = "work/06_verificari.csv"
API = "https://emailverifier.reoon.com/api/v1/verify"

ap = argparse.ArgumentParser()
ap.add_argument("--max-firme", type=int, default=0)
ap.add_argument("--workers", type=int, default=8)
ap.add_argument("--input", required=True)
args = ap.parse_args()

df = pd.read_csv(args.input, dtype=str).fillna("")

seen = {}          # email -> status (nu re-verifica intre rulari)
firm_done = set()  # id_firma cu rezultat final
if os.path.exists(VERIF):
    v = pd.read_csv(VERIF, dtype=str).fillna("")
    for _, r in v.iterrows():
        seen[r["email"]] = r["status"]
    for fid, g in v.groupby("id_firma"):
        sts = set(g["status"])
        if sts & {"valid", "safe"} or any(s.startswith("catch_all") for s in sts):
            firm_done.add(fid)
    # firme care si-au epuizat toate tiparele fara rezultat
    tried_by_firm = v.groupby("id_firma")["email"].apply(set).to_dict()
    for _, r in df.iterrows():
        fid = r["id_firma"]
        if fid in firm_done:
            continue
        pats = [p for p in r["tipare"].split(";") if p]
        if pats and all(p in tried_by_firm.get(fid, set()) for p in pats):
            firm_done.add(fid)

new_file = not os.path.exists(VERIF)
fout = open(VERIF, "a", newline="")
w = csv.DictWriter(fout, fieldnames=["id_firma", "email", "status", "is_catch_all", "credite"])
if new_file:
    w.writeheader()

todo = df[~df["id_firma"].isin(firm_done)]
if args.max_firme:
    todo = todo.head(args.max_firme)

print(f"De verificat: {len(todo)} firme (din {len(df)}), {args.workers} workeri", flush=True)

lock = threading.Lock()
stats = {"credite": 0, "found": 0, "done": 0, "errors": 0}


def verify_email(email):
    for attempt in range(2):
        try:
            resp = requests.get(API, params={"email": email, "key": KEY, "mode": "power"}, timeout=75)
            d = resp.json() if resp.status_code == 200 else {}
            return d
        except Exception as e:
            with lock:
                stats["errors"] += 1
            print(f"  ! {email}: {type(e).__name__} (incercarea {attempt+1}/2)", flush=True)
            time.sleep(5)
    return None


def process_firm(row):
    fid = row["id_firma"]
    for email in row["tipare"].split(";"):
        if not email:
            continue
        with lock:
            st = seen.get(email)
        if st is None:
            d = verify_email(email)
            if d is None:
                continue
            st = d.get("status", "error")
            # role_account/unknown pot fi totusi livrabile (SMTP a acceptat) -
            # pastram semnalul, altfel cozile de generice (office@) s-ar
            # exclude in bloc la export
            if st not in ("valid", "safe") and d.get("is_deliverable") is True:
                st = st + "_del"
            catch = d.get("is_catch_all_email", d.get("is_catch_all", ""))
            with lock:
                if email in seen:          # alt thread a apucat sa-l verifice
                    st = seen[email]
                else:
                    seen[email] = st
                    stats["credite"] += 1
                    w.writerow({"id_firma": fid, "email": email, "status": st,
                                "is_catch_all": catch, "credite": 1})
                    fout.flush()
            time.sleep(0.2)
        if st in ("valid", "safe"):
            with lock:
                stats["found"] += 1
            break
        if st.startswith("catch_all"):
            break
    with lock:
        stats["done"] += 1
        if stats["done"] % 25 == 0:
            print(f"  {stats['done']}/{len(todo)} firme, {stats['credite']} credite, "
                  f"{stats['found']} valide, {stats['errors']} erori retea", flush=True)


with ThreadPoolExecutor(max_workers=args.workers) as ex:
    list(ex.map(process_firm, (r for _, r in todo.iterrows())))

fout.close()
print(f"GATA {args.input}: {stats['credite']} credite acum, {stats['found']} firme cu adresa valida noua", flush=True)
