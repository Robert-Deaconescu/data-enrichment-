#!/usr/bin/env python3
"""Findere comerciale pe free tiers: Prospeo, Dropcontact, GetProspect.
Input:  work/20_finders_tinta.csv (id_firma,firma,first_name,last_name,domeniu,trust)
Output: work/20_finders_rezultate.csv (checkpoint per id_firma+tool)
Ruleaza: python3 scripts/15_finders.py --tool prospeo|dropcontact|getprospect [--max N]
Se opreste la eroare de credite. Firmele gasite de un tool sunt sarite de urmatoarele.
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
OUT = "work/20_finders_rezultate.csv"

ap = argparse.ArgumentParser()
ap.add_argument("--tool", required=True, choices=["prospeo", "dropcontact", "getprospect"])
ap.add_argument("--max", type=int, default=0)
ap.add_argument("--input", default="work/20_finders_tinta.csv")
args = ap.parse_args()

t = pd.read_csv(args.input, dtype=str).fillna("")
found_ids, tried = set(), set()
if os.path.exists(OUT):
    prev = pd.read_csv(OUT, dtype=str).fillna("")
    found_ids = set(prev[prev.email != ""].id_firma)
    tried = set(prev[prev.tool == args.tool].id_firma)
todo = t[~t.id_firma.isin(found_ids) & ~t.id_firma.isin(tried)]
if args.max:
    todo = todo.head(args.max)
print(f"[{args.tool}] de incercat: {len(todo)} firme", flush=True)

new_file = not os.path.exists(OUT)
fout = open(OUT, "a", newline="")
w = csv.DictWriter(fout, fieldnames=["id_firma", "tool", "email", "calificare"])
if new_file:
    w.writeheader()

stats = {"found": 0, "done": 0}


def write(fid, email, cal):
    w.writerow({"id_firma": fid, "tool": args.tool, "email": email, "calificare": cal})
    fout.flush()
    stats["done"] += 1
    if email:
        stats["found"] += 1
    if stats["done"] % 20 == 0:
        print(f"  {stats['done']}/{len(todo)}: {stats['found']} gasite", flush=True)


if args.tool == "prospeo":
    KEY = os.environ["PROSPEO_API_KEY"]
    for _, r in todo.iterrows():
        d = None
        for attempt in range(4):
            try:
                resp = requests.post("https://api.prospeo.io/enrich-person",
                                     headers={"X-KEY": KEY, "Content-Type": "application/json"},
                                     json={"first_name": r.first_name, "last_name": r.last_name,
                                           "company_website": r.domeniu}, timeout=60)
                d = resp.json()
            except Exception as e:
                print(f"  ! {r.domeniu}: {type(e).__name__}", flush=True)
                break
            if resp.status_code == 429 or "Rate limit" in str(d.get("error_code", "")):
                wait = 30 * (attempt + 1)
                print(f"  rate limit - astept {wait}s", flush=True)
                time.sleep(wait)
                d = None
                continue
            break
        if d is None:
            continue
        if d.get("error") and "INSUFFICIENT_CREDITS" in str(d.get("error_code", "")):
            print("  CREDITE PROSPEO EPUIZATE - stop", flush=True)
            break
        em = ((d.get("response") or {}).get("email") or {})
        if isinstance(em, dict) and em.get("email"):
            write(r.id_firma, em["email"].lower(), f"prospeo:{em.get('status','')}")
        else:
            write(r.id_firma, "", "negasit")
        time.sleep(0.5)

elif args.tool == "getprospect":
    KEY = os.environ["GETPROSPECT_API_KEY"]
    for _, r in todo.iterrows():
        try:
            resp = requests.get("https://api.getprospect.com/public/v1/email/find",
                                params={"name": f"{r.first_name} {r.last_name}", "company": r.domeniu},
                                headers={"apiKey": KEY}, timeout=60)
        except Exception as e:
            print(f"  ! {r.domeniu}: {type(e).__name__}", flush=True)
            continue
        if resp.status_code in (402, 429):
            print(f"  CREDITE/RATA GETPROSPECT ({resp.status_code}) - stop", flush=True)
            break
        if resp.status_code == 404:
            write(r.id_firma, "", "negasit")
        elif resp.status_code == 200:
            d = resp.json()
            em = d.get("email") or (d.get("contact") or {}).get("email") or ""
            if isinstance(em, dict):
                em = em.get("email", "")
            st = str(d.get("status", d.get("emailStatus", "")))
            write(r.id_firma, str(em).lower() if em else "", f"getprospect:{st}" if em else "negasit")
        else:
            print(f"  ? HTTP {resp.status_code} la {r.domeniu}: {resp.text[:120]}", flush=True)
            if resp.status_code == 401:
                break
        time.sleep(0.7)

elif args.tool == "dropcontact":
    KEY = os.environ["DROPCONTACT_API_KEY"]
    H = {"X-Access-Token": KEY, "Content-Type": "application/json"}
    batch = todo.to_dict("records")
    for i in range(0, len(batch), 25):
        chunk = batch[i:i+25]
        data = [{"first_name": c["first_name"], "last_name": c["last_name"],
                 "website": c["domeniu"]} for c in chunk]
        try:
            resp = requests.post("https://api.dropcontact.com/v1/enrich/all",
                                 headers=H, json={"data": data}, timeout=60)
            d = resp.json()
        except Exception as e:
            print(f"  ! batch {i}: {type(e).__name__}", flush=True)
            continue
        rid = d.get("request_id")
        if not rid:
            print(f"  STOP dropcontact: {str(d)[:200]}", flush=True)
            break
        res = None
        for _ in range(30):
            time.sleep(15)
            try:
                rr = requests.get(f"https://api.dropcontact.com/v1/enrich/all/{rid}",
                                  headers=H, timeout=60).json()
            except Exception:
                continue
            if rr.get("success") and rr.get("data"):
                res = rr["data"]
                break
        if res is None:
            print(f"  ! batch {i}: fara rezultat dupa asteptare", flush=True)
            continue
        for c, item in zip(chunk, res):
            emails = item.get("email") or []
            best = ""
            cal = "negasit"
            for e in emails:
                if isinstance(e, dict) and e.get("email"):
                    q = e.get("qualification", "")
                    if "nominative" in q:
                        best, cal = e["email"].lower(), f"dropcontact:{q}"
                        break
                    if not best:
                        best, cal = e["email"].lower(), f"dropcontact:{q}"
            write(c["id_firma"], best, cal)
        print(f"  batch {i//25+1}: total {stats['found']} gasite", flush=True)

fout.close()
print(f"GATA {args.tool}: {stats['found']} emailuri gasite din {stats['done']} incercari", flush=True)
