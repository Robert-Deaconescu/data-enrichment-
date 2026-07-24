#!/usr/bin/env python3
"""Pasul 2 - Date oficiale ANAF via demoanaf.ro (gratuit).
Faza A: rezolvare CUI dupa nume (+judet) via /api/search?q=
Faza B: /api/company/{cui} -> administratori, stare, TVA.
Rate limit: 200 req/min (0.3s/cerere). Checkpoint: work/03_cui_map.csv,
work/03_anaf_data.jsonl. Reluabil - sare peste ce e deja rezolvat."""
import csv
import json
import os
import re
import sys
import time

import pandas as pd
import requests
from rapidfuzz import fuzz
from unidecode import unidecode

BASE = "https://demoanaf.ro/api"
DELAY = 0.3          # 200 req/min
CUI_MAP = "work/03_cui_map.csv"
ANAF_DATA = "work/03_anaf_data.jsonl"

sess = requests.Session()
sess.headers["User-Agent"] = "TB-enrichment/1.0 (proiect date B2B; contact: robertdeaconescu2020@gmail.com)"


def get(url, params=None, tries=5):
    """404 = raspuns valid (negasit). Orice alta eroare (429/403/5xx/retea)
    se reincearca cu backoff, ca sa nu marcam gresit firme drept negasite."""
    for a in range(tries):
        try:
            r = sess.get(url, params=params, timeout=25)
            if r.status_code in (200, 404):
                return r
            time.sleep(min(60, 5 * 2 ** a))
        except requests.RequestException:
            time.sleep(min(60, 2 ** a))
    return None


def nkey(s):
    s = unidecode(str(s)).upper()
    # unifica forma juridica cu puncte (S.R.L. -> SRL) inainte de eliminare
    s = re.sub(r"\bS\.?\s*R\.?\s*L\.?(?=\s|$|\.)", "SRL", s)
    s = re.sub(r"\bS\.?\s*A\.?(?=\s|$|\.)", "SA", s)
    s = re.sub(r"\bP\.?\s*F\.?\s*A\.?(?=\s|$|\.)", "PFA", s)
    s = re.sub(r"\b(SRL|SA|PFA|SCS|SNC|SRL-D)\b", "", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def njud(s):
    return unidecode(str(s)).upper().replace("-", " ").strip()


df = pd.read_csv("work/02_dedup.csv", dtype=str).fillna("")

# ---------- Faza A: rezolvare CUI ----------
done = {}
if os.path.exists(CUI_MAP):
    with open(CUI_MAP) as f:
        for row in csv.DictReader(f):
            done[row["id_firma"]] = row

new_file = not os.path.exists(CUI_MAP)
fout = open(CUI_MAP, "a", newline="")
w = csv.DictWriter(fout, fieldnames=["id_firma", "cui", "anaf_name", "scor", "metoda"])
if new_file:
    w.writeheader()

todo = [r for _, r in df.iterrows() if r["id_firma"] not in done]
print(f"Faza A: {len(todo)} firme de rezolvat (din {len(df)})", flush=True)

for n, r in enumerate(todo):
    fid = r["id_firma"]
    firma, jud = r["firma"], njud(r["judet"])
    key = nkey(firma)
    best = {"id_firma": fid, "cui": "", "anaf_name": "", "scor": "", "metoda": ""}

    # 1) bid-ul din sursa ca posibil CUI (verificare directa)
    if r["cui"]:
        resp = get(f"{BASE}/company/{r['cui']}")
        time.sleep(DELAY)
        if resp is not None and resp.status_code == 200:
            d = resp.json().get("data", {})
            sc = fuzz.token_sort_ratio(nkey(d.get("name", "")), key)
            if sc >= 85:
                best.update(cui=str(d["cui"]), anaf_name=d.get("name", ""),
                            scor=sc, metoda="bid")

    # 2) cautare dupa nume
    if not best["cui"]:
        q = key if len(key) >= 3 else firma
        resp = get(f"{BASE}/search", params={"q": q, "limit": 50})
        time.sleep(DELAY)
        cands = []
        if resp is not None and resp.status_code == 200:
            cands = resp.json().get("data", []) or []
        if not cands and len(key.split()) > 2:
            resp = get(f"{BASE}/search", params={"q": " ".join(key.split()[:2]), "limit": 50})
            time.sleep(DELAY)
            if resp is not None and resp.status_code == 200:
                cands = resp.json().get("data", []) or []
        # fereastra de 50 plina de omonime din alte judete? reia cu forma juridica
        lf = re.search(r"\b(SRL|SA|PFA)\b", firma)
        if lf and len(cands) >= 50 and jud and not any(
                njud(c.get("county", "")) == jud for c in cands):
            resp = get(f"{BASE}/search", params={"q": f"{key} {lf.group(1)}", "limit": 50})
            time.sleep(DELAY)
            if resp is not None and resp.status_code == 200:
                cands += resp.json().get("data", []) or []
        scored = []
        for c in cands:
            sc = fuzz.token_sort_ratio(nkey(c.get("name", "")), key)
            cj = njud(c.get("county", ""))
            if jud and cj:
                if cj == jud:
                    sc += 4
                else:
                    sc -= 25
            scored.append((sc, c))
        scored.sort(key=lambda x: -x[0])
        if scored and scored[0][0] >= 88:
            sc, c = scored[0]
            best.update(cui=str(c["cui"]), anaf_name=c.get("name", ""),
                        scor=min(sc, 100), metoda="search")

    w.writerow(best)
    fout.flush()
    if (n + 1) % 100 == 0:
        found = sum(1 for x in open(CUI_MAP) if x.strip()) - 1
        print(f"  A {n+1}/{len(todo)} procesate", flush=True)

fout.close()

cmap = pd.read_csv(CUI_MAP, dtype=str).fillna("")
resolved = cmap[cmap["cui"] != ""]
print(f"Faza A gata: CUI rezolvat pentru {len(resolved)}/{len(cmap)}", flush=True)

# ---------- Faza B: date complete per CUI ----------
have = set()
if os.path.exists(ANAF_DATA):
    with open(ANAF_DATA) as f:
        for line in f:
            try:
                have.add(str(json.loads(line)["cui"]))
            except Exception:
                pass

cuis = [c for c in resolved["cui"].unique() if c not in have]
print(f"Faza B: {len(cuis)} CUI-uri de interogat", flush=True)

with open(ANAF_DATA, "a") as f:
    for n, cui in enumerate(cuis):
        resp = get(f"{BASE}/company/{cui}")
        time.sleep(DELAY)
        if resp is not None and resp.status_code == 200:
            d = resp.json().get("data", {})
            rec = {
                "cui": str(cui),
                "name": d.get("name", ""),
                "inactive": d.get("inactive"),
                "registrationState": d.get("registrationState", ""),
                "vatRegistered": d.get("vatRegistered"),
                "phone": d.get("phone", ""),
                "county": (d.get("headquartersAddress") or {}).get("county", ""),
                "locality": (d.get("headquartersAddress") or {}).get("locality", ""),
                "administrators": [
                    {"name": a.get("name", ""), "role": a.get("role", "")}
                    for a in (d.get("administrators") or [])
                    if not a.get("gdprHidden")
                ],
            }
        else:
            rec = {"cui": str(cui), "error": resp.status_code if resp is not None else "network"}
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        if (n + 1) % 100 == 0:
            print(f"  B {n+1}/{len(cuis)}", flush=True)

print("Faza B gata.", flush=True)
