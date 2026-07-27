#!/usr/bin/env python3
"""Validare secundara catch-all cu BounceBan (endpoint waterfall, sincron).
Input:  work/18_bounceban_top100.csv (prioritate,Companie,Persoana,email_de_verificat,motiv)
Output: work/19_bounceban_rezultate.csv (checkpoint, reluabil)
Se opreste cand crediteles raman 0 sau apar erori repetate de autorizare.
"""
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
KEY = os.environ.get("BOUNCEBAN_API_KEY", "")
if not KEY:
    sys.exit("BOUNCEBAN_API_KEY lipseste din .env")

API = "https://api-waterfall.bounceban.com/v1/verify/single"
OUT = "work/19_bounceban_rezultate.csv"

df = pd.read_csv("work/18_bounceban_top100.csv", dtype=str).fillna("")
done = set()
if os.path.exists(OUT):
    done = set(pd.read_csv(OUT, dtype=str)["email"])
todo = df[~df.email_de_verificat.isin(done)]
print(f"De verificat: {len(todo)} adrese (din {len(df)})", flush=True)

new_file = not os.path.exists(OUT)
fout = open(OUT, "a", newline="")
w = csv.DictWriter(fout, fieldnames=["email", "result", "score", "is_accept_all",
                                     "smtp_provider", "credits_remaining"])
if new_file:
    w.writeheader()

lock = threading.Lock()
state = {"stop": False, "auth_err": 0, "done": 0, "deliverable": 0, "remaining": None}


def verify(row):
    if state["stop"]:
        return
    email = row["email_de_verificat"]
    try:
        r = requests.get(API, params={"email": email, "timeout": 120},
                         headers={"Authorization": KEY}, timeout=150)
        if r.status_code in (401, 403):
            with lock:
                state["auth_err"] += 1
                if state["auth_err"] >= 3:
                    state["stop"] = True
            print(f"  ! autorizare esuata ({r.status_code}) la {email}", flush=True)
            return
        d = r.json()
    except Exception as e:
        print(f"  ! {email}: {type(e).__name__}", flush=True)
        return
    res = d.get("result", "eroare")
    rem = d.get("credits_remaining")
    with lock:
        w.writerow({"email": email, "result": res, "score": d.get("score", ""),
                    "is_accept_all": d.get("is_accept_all", ""),
                    "smtp_provider": d.get("smtp_provider", ""),
                    "credits_remaining": rem})
        fout.flush()
        state["done"] += 1
        if res == "deliverable":
            state["deliverable"] += 1
        if rem is not None:
            state["remaining"] = rem
            if isinstance(rem, (int, float)) and rem <= 0:
                state["stop"] = True
                print("  CREDITE EPUIZATE - opresc", flush=True)
        if state["done"] % 10 == 0:
            print(f"  {state['done']}/{len(todo)}: {state['deliverable']} deliverable, "
                  f"credite ramase: {state['remaining']}", flush=True)
    time.sleep(0.3)


with ThreadPoolExecutor(max_workers=5) as ex:
    list(ex.map(verify, (r for _, r in todo.iterrows())))

fout.close()
print(f"GATA: {state['done']} verificate, {state['deliverable']} deliverable, "
      f"credite ramase: {state['remaining']}", flush=True)
