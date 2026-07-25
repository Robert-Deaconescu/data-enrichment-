#!/usr/bin/env python3
"""Pasii 2(merge)+3 - Aplica datele ANAF pe baza dedup si determina domeniul web.
- completeaza Persoana din administratori ANAF unde lipseste
- marcheaza firmele radiate/inactive -> Status Exclus-inactiv
- domeniu: din adresa generica existenta (exclude domenii publice)
Scrie work/04_imbogatit.csv"""
import json
import re

import pandas as pd

PUBLIC_DOMAINS = {
    "gmail.com", "yahoo.com", "yahoo.ro", "yahoo.co.uk", "hotmail.com",
    "outlook.com", "icloud.com", "aol.com", "mail.com", "protonmail.com",
    "ymail.com", "live.com", "msn.com", "zappmobile.ro", "clicknet.ro",
    "rdslink.ro", "rdsmail.ro", "personal.ro", "xnet.ro", "k.ro", "go.ro",
    "home.ro", "email.ro", "mymail.ro", "posta.ro", "pcnet.ro", "fx.ro",
    "canad.ro", "apropo.ro", "rol.ro", "from.ro", "mail.ru",
}

import os

df = pd.read_csv("work/02_dedup.csv", dtype=str).fillna("")
cmap = pd.read_csv("work/03_cui_map.csv", dtype=str).fillna("")

# domenii descoperite la pasul 8 (doar cele validate si cu MX activ),
# din checkpointul principal + shardurile paralele
import glob as globmod

discovered = {}
for p8 in ["work/08_domenii.csv"] + globmod.glob("work/08_domenii.csv.shard*"):
    if not os.path.exists(p8):
        continue
    d8 = pd.read_csv(p8, dtype=str).fillna("")
    for _, r8 in d8[(d8["domeniu"] != "") & (d8["mx"] == "da")].iterrows():
        discovered[r8["id_firma"]] = (r8["domeniu"], r8["validare"])

# auditul subagentilor: 'gresit' se elimina; 'incert' se pastreaza numai daca
# validarea a fost prin CUI gasit in pagina (dovada decisiva); restul merg la
# verificare manuala (fara tipare, fara campanie)
manual_review = []
if os.path.exists("work/09_audit_domenii.csv"):
    aud = pd.read_csv("work/09_audit_domenii.csv", dtype=str).fillna("")
    for _, ra in aud.iterrows():
        fid = ra["id_firma"]
        if fid not in discovered:
            continue
        dom, val = discovered[fid]
        if ra["verdict"] == "gresit" or (ra["verdict"] == "incert" and val != "cui"):
            manual_review.append({"id_firma": fid, "domeniu": dom,
                                  "verdict": ra["verdict"], "motiv": ra["motiv"]})
            del discovered[fid]
pd.DataFrame(manual_review).to_csv("work/domenii_de_verificat_manual.csv", index=False)
anaf = {}
with open("work/03_anaf_data.jsonl") as f:
    for line in f:
        try:
            d = json.loads(line)
            anaf[str(d.get("cui", ""))] = d
        except Exception:
            pass

df = df.merge(cmap[["id_firma", "cui", "anaf_name", "metoda"]],
              on="id_firma", how="left", suffixes=("_sursa", ""))
df = df.fillna("")

status, persoana_fin, functie, obs, domenii = [], [], [], [], []
n_admin_filled = 0

for _, r in df.iterrows():
    o = []
    st = "Pending"
    cui = r["cui"]
    a = anaf.get(cui) if cui else None

    # stare firma
    if a and not a.get("error"):
        rs = (a.get("registrationState") or "").upper()
        if a.get("inactive") or "RADIAT" in rs or "INTRERUPERE" in rs or "SUSPENDAT" in rs:
            st = "Exclus-inactiv"
            o.append(f"stare ANAF: {a.get('registrationState') or 'inactiv fiscal'}")
        if a.get("vatRegistered") is False:
            o.append("neplatitor TVA")
    elif not cui:
        o.append("CUI nerezolvat ANAF")

    # persoana: sursa are prioritate; altfel primul administrator ANAF
    p = r["persoana"]
    fn = "Contact" if p else ""
    if p:
        pass
    elif a and a.get("administrators"):
        adm = a["administrators"][0]
        nm = adm["name"].title()
        # numele ANAF sunt NUME PRENUME; pastram ordinea, titlecase
        p = nm
        fn = adm.get("role", "administrator") or "administrator"
        o.append("persoana din ANAF")
        n_admin_filled += 1
    if p and fn == "Contact":
        fn = "Contact"

    # domeniu din email generic; daca lipseste, din descoperirea web (pas 8)
    dom = ""
    for e in (r["email1"], r["email2"]):
        if e and "@" in e:
            d2 = e.split("@", 1)[1].lower()
            if d2 not in PUBLIC_DOMAINS:
                dom = d2
                break
    if not dom and r["id_firma"] in discovered:
        dom, valid8 = discovered[r["id_firma"]]
        o.append(f"domeniu descoperit web ({valid8})")

    status.append(st)
    persoana_fin.append(p)
    functie.append(fn if p else "")
    obs.append("; ".join(o))
    domenii.append(dom)

df["status"] = status
df["persoana_fin"] = persoana_fin
df["functie"] = functie
df["obs_anaf"] = obs
df["domeniu"] = domenii

df.to_csv("work/04_imbogatit.csv", index=False)

excl = (df["status"] != "Pending").sum()
with open("work/stats.md", "a") as f:
    f.write("\n## Pas 2+3 - ANAF + domenii\n\n")
    f.write(f"- CUI rezolvat: {(df['cui'] != '').sum()}/{len(df)}\n")
    f.write(f"- Firme excluse (radiate/inactive): {excl}\n")
    f.write(f"- Persoana completata din administratori ANAF: {n_admin_filled}\n")
    f.write(f"- Total firme cu persoana: {(df['persoana_fin'] != '').sum()}\n")
    f.write(f"- Firme cu domeniu propriu (din email generic): {(df['domeniu'] != '').sum()}\n")

print(f"CUI: {(df['cui']!='').sum()}, exclusi: {excl}, "
      f"persoana ANAF: {n_admin_filled}, cu persoana: {(df['persoana_fin']!='').sum()}, "
      f"cu domeniu: {(df['domeniu']!='').sum()}")
