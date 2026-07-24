#!/usr/bin/env python3
"""Pas suplimentar (gratuit) - Descoperirea domeniului web pentru firmele fara
domeniu cunoscut. Genereaza candidati din numele firmei, verifica DNS + MX,
apoi valideaza continutul site-ului (numele firmei sau CUI in pagina).
Checkpoint: work/08_domenii.csv"""
import csv
import os
import re
import time

import dns.resolver
import pandas as pd
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

OUT = "work/08_domenii.csv"
UA = "Mozilla/5.0 (compatible; TB-enrichment/1.0; contact: robertdeaconescu2020@gmail.com)"
GENERIC = {"COM", "PROD", "SERV", "SERVICE", "SERVICII", "GRUP", "GROUP", "TRANS",
           "ROMANIA", "RO", "IMPEX", "EXIM", "COMPANY", "INTERNATIONAL", "INDUSTRY",
           "INDUSTRIES", "CONSTRUCT", "CONSULTING", "TRADING", "HOLDING", "AGRO"}
TLDS = [".ro", ".com", ".eu", ".net"]

resolver = dns.resolver.Resolver()
resolver.timeout = 4
resolver.lifetime = 6

sess = requests.Session()
sess.headers["User-Agent"] = UA


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
    # primul token daca e distinctiv
    if t[0] not in GENERIC and len(t[0]) >= 4:
        bases.append(t[0].lower())
    # primele doua tokenuri
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
    return out[:10]


def has_dns(dom):
    try:
        resolver.resolve(dom, "A")
        return True
    except Exception:
        try:
            resolver.resolve(dom, "AAAA")
            return True
        except Exception:
            return False


def has_mx(dom):
    try:
        return len(resolver.resolve(dom, "MX")) > 0
    except Exception:
        return False


def page_matches(dom, name, cui, judet, localitate):
    """Descarca homepage si cauta numele firmei sau CUI. Conservator:
    - CUI in pagina = acceptare sigura
    - >=2 tokenuri distinctive, toate prezente = nume-complet
    - 1 singur token distinctiv: cere token in titlu SAU pagina + judet/localitate
      in pagina (altfel domeniile generice dau fals-pozitive)"""
    for scheme in ("https", "http"):
        try:
            r = sess.get(f"{scheme}://{dom}", timeout=10, allow_redirects=True)
            if r.status_code != 200:
                continue
            html = r.text[:200000]
            soup = BeautifulSoup(html, "html.parser")
            text = unidecode(soup.get_text(" ")).upper()
            title = unidecode(soup.title.string if soup.title and soup.title.string else "").upper()
            if cui and re.search(rf"\b(RO)?{re.escape(cui)}\b", text):
                return "cui"
            t = [x for x in toks(name) if x not in GENERIC]
            geo = [unidecode(g).upper() for g in (judet, localitate) if g]
            geo_hit = any(g in text for g in geo)
            if len(t) >= 2:
                hits = sum(1 for x in t if x in text)
                if hits == len(t):
                    return "nume-complet"
                if hits >= len(t) - 1 and geo_hit:
                    return "nume-partial+geo"
            elif len(t) == 1:
                if (t[0] in title or t[0] in text) and geo_hit:
                    return "nume+geo"
        except requests.RequestException:
            continue
        finally:
            time.sleep(0.5)
    return ""


df = pd.read_csv("work/04_imbogatit.csv", dtype=str).fillna("")
todo = df[(df["status"] == "Pending") & (df["domeniu"] == "")]

done = set()
if os.path.exists(OUT):
    done = set(pd.read_csv(OUT, dtype=str)["id_firma"].astype(str))

new_file = not os.path.exists(OUT)
f = open(OUT, "a", newline="")
w = csv.DictWriter(f, fieldnames=["id_firma", "domeniu", "mx", "validare"])
if new_file:
    w.writeheader()

todo = todo[~todo["id_firma"].isin(done)]
print(f"De cautat domenii pentru {len(todo)} firme", flush=True)

found = 0
for n, (_, r) in enumerate(todo.iterrows()):
    best = {"id_firma": r["id_firma"], "domeniu": "", "mx": "", "validare": ""}
    for dom in candidates(r["firma"]):
        if not has_dns(dom):
            continue
        m = page_matches(dom, r["firma"], r["cui"], r["judet"], r["localitate"])
        if m:
            best.update(domeniu=dom, mx="da" if has_mx(dom) else "nu", validare=m)
            found += 1
            break
    w.writerow(best)
    f.flush()
    if (n + 1) % 50 == 0:
        print(f"  {n+1}/{len(todo)} firme, {found} domenii gasite", flush=True)

f.close()
print(f"GATA: {found} domenii descoperite din {len(todo)} firme", flush=True)
