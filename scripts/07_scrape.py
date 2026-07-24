#!/usr/bin/env python3
"""Pasul 6 - Scraping pagini de contact (gratuit), pentru firmele fara adresa
nominala verificata. 1 cerere/secunda, robots.txt respectat, doar pagini de
contact/echipa. Checkpoint: work/07_scrape.csv"""
import csv
import os
import re
import time
import urllib.robotparser as robotparser
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

PATHS = ["/contact", "/contacte", "/contact-us", "/echipa", "/despre-noi", "/despre", "/"]
OUT = "work/07_scrape.csv"
UA = "Mozilla/5.0 (compatible; TB-enrichment/1.0; contact: robertdeaconescu2020@gmail.com)"
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
SKIP_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js")

df = pd.read_csv("work/04_imbogatit.csv", dtype=str).fillna("")
tip = pd.read_csv("work/05_tipare.csv", dtype=str).fillna("")
verified = set()
if os.path.exists("work/06_verificari.csv"):
    v = pd.read_csv("work/06_verificari.csv", dtype=str).fillna("")
    verified = set(v[v["status"].isin(["valid", "safe"])]["id_firma"])

done = set()
if os.path.exists(OUT):
    done = set(pd.read_csv(OUT, dtype=str)["id_firma"].astype(str))

new_file = not os.path.exists(OUT)
fout = open(OUT, "a", newline="")
w = csv.DictWriter(fout, fieldnames=["id_firma", "domeniu", "emailuri", "pagini_ok", "nota"])
if new_file:
    w.writeheader()

# tinta: Pending, cu domeniu, fara adresa nominala verificata deja
todo = df[(df["status"] == "Pending") & (df["domeniu"] != "")
          & (~df["id_firma"].isin(verified)) & (~df["id_firma"].isin(done))]
print(f"De scanat: {len(todo)} domenii", flush=True)

sess = requests.Session()
sess.headers["User-Agent"] = UA


def fetch(url):
    try:
        r = sess.get(url, timeout=15, allow_redirects=True)
        time.sleep(1.0)
        if r.status_code == 200 and "text/html" in r.headers.get("content-type", ""):
            return r.text
    except requests.RequestException:
        time.sleep(1.0)
    return None


for n, (_, row) in enumerate(todo.iterrows()):
    dom = row["domeniu"]
    base = f"https://{dom}"
    emails, pages_ok, nota = set(), 0, ""

    rp = robotparser.RobotFileParser()
    try:
        rr = sess.get(f"{base}/robots.txt", timeout=10)
        time.sleep(1.0)
        rp.parse(rr.text.splitlines() if rr.status_code == 200 else [])
    except requests.RequestException:
        rp.parse([])
        nota = "robots inaccesibil"

    for path in PATHS:
        url = urljoin(base, path)
        if not rp.can_fetch(UA, url):
            continue
        html = fetch(url)
        if html is None:
            continue
        pages_ok += 1
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select('a[href^="mailto:"]'):
            addr = a["href"][7:].split("?")[0].strip().lower()
            if addr:
                emails.add(addr)
        text = soup.get_text(" ")
        for m in EMAIL_RE.findall(text):
            m = m.lower().rstrip(".")
            if not m.endswith(SKIP_EXT):
                emails.add(m)
        if len(emails) >= 8:
            break

    # pastreaza doar adrese pe domeniul firmei (sau subdomenii)
    emails = {e for e in emails if e.split("@")[-1] == dom or e.split("@")[-1].endswith("." + dom)}
    w.writerow({"id_firma": row["id_firma"], "domeniu": dom,
                "emailuri": ";".join(sorted(emails)), "pagini_ok": pages_ok, "nota": nota})
    fout.flush()
    if (n + 1) % 25 == 0:
        print(f"  {n+1}/{len(todo)}", flush=True)

fout.close()
print("Scraping gata.", flush=True)
