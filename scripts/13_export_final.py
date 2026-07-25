#!/usr/bin/env python3
"""Pasul 8 - Exportul final: output/contacte_final.csv
Coloane FIXE: Companie, Persoana, Functie, Email, Status, Data_trimitere, Observatii

Rezolutie per firma (in ordinea prioritatii):
1. Exclus-inactiv (ANAF) - ramane in fisier, nu intra in campanie
2. Nominal verificat (safe/valid): tipar pe domeniu validat > adresa de pe site
   > tipar pe domeniu MX ghicit  -> Status Pending
3. Generic existent verificat -> Status Pending, obs 'generic'
4. office@ pe domeniu MX ghicit, verificat -> Status Incert-mx (domeniul nu e
   confirmat ca apartine firmei; clientul decide)
5. Doar catch-all -> Status Catch-all (segment separat, necesita validare
   secundara ex. BounceBan; NU se trimite din Make.com implicit)
6. Nimic verificabil -> Exclus-fara-email
"""
import pandas as pd

df = pd.read_csv("work/04_imbogatit.csv", dtype=str).fillna("")
ver = pd.read_csv("work/06_verificari.csv", dtype=str).fillna("")

# apartenenta la cozi -> sursa adresei
q_tip = pd.read_csv("work/10_coada_tipare.csv", dtype=str).fillna("")
q_scr = pd.read_csv("work/10_coada_scrape_run.csv", dtype=str).fillna("")
q_gen = pd.read_csv("work/10_coada_generice_run.csv", dtype=str).fillna("")
try:
    q_mx = pd.read_csv("work/10_coada_mx_run.csv", dtype=str).fillna("")
except FileNotFoundError:
    q_mx = pd.DataFrame(columns=["id_firma", "tipare"])

email_src = {}   # (id_firma, email) -> sursa, cu prioritate nominala
for q, src in [(q_gen, "generic"), (q_mx, "tipar-mx"), (q_scr, "site"), (q_tip, "tipar-verificat")]:
    for _, r in q.iterrows():
        for e in r["tipare"].split(";"):
            if e:
                if src == "tipar-mx" and e.startswith("office@"):
                    email_src[(r["id_firma"], e)] = "office-mx"
                else:
                    email_src[(r["id_firma"], e)] = src

SRC_PRIO = {"tipar-verificat": 0, "site": 1, "tipar-mx": 2, "generic": 3, "office-mx": 4}

ver["src"] = ver.apply(lambda r: email_src.get((r["id_firma"], r["email"]), "necunoscut"), axis=1)
ver["prio"] = ver["src"].map(SRC_PRIO).fillna(9)

by_firm = {fid: g.sort_values("prio") for fid, g in ver.groupby("id_firma")}

rows = []
stats = {}
for _, r in df.iterrows():
    fid = r["id_firma"]
    base = {"Companie": r["firma"], "Persoana": r["persoana_fin"] or r["persoana"],
            "Functie": r["functie"], "Email": "", "Status": "", "Data_trimitere": "",
            "Observatii": ""}
    if r["status"] == "Exclus-inactiv":
        base.update(Email=r["email1"], Status="Exclus-inactiv",
                    Observatii="firma radiata/inactiva (ANAF)")
        rows.append(base); stats["Exclus-inactiv"] = stats.get("Exclus-inactiv", 0) + 1
        continue
    g = by_firm.get(fid)
    # valid/safe = verificat plin; *_del = SMTP a acceptat (role_account/unknown
    # livrabile) - acceptat doar pentru adrese generice/office, nu ca nominal
    ok = None
    if g is not None:
        ok = g[g["status"].isin(["valid", "safe"]) |
               (g["status"].str.endswith("_del") & g["src"].isin(["generic", "office-mx"]))]
    if ok is not None and len(ok):
        best = ok.iloc[0]
        if best["src"] in ("tipar-verificat", "site", "tipar-mx"):
            base.update(Email=best["email"], Status="Pending", Observatii=best["src"])
            rows.append(base); stats["Nominal"] = stats.get("Nominal", 0) + 1
            continue
        if best["src"] == "generic":
            base.update(Email=best["email"], Status="Pending", Observatii="generic")
            rows.append(base); stats["Generic"] = stats.get("Generic", 0) + 1
            continue
        if best["src"] == "office-mx":
            base.update(Email=best["email"], Status="Incert-mx",
                        Observatii="office@ pe domeniu ghicit (MX activ, neconfirmat)")
            rows.append(base); stats["Incert-mx"] = stats.get("Incert-mx", 0) + 1
            continue
    ca = g[g["status"].str.startswith("catch_all")] if g is not None else None
    if ca is not None and len(ca):
        best = ca.iloc[0]
        base.update(Email=best["email"], Status="Catch-all",
                    Observatii=f"domeniu catch-all ({best['src']}); necesita validare secundara")
        rows.append(base); stats["Catch-all"] = stats.get("Catch-all", 0) + 1
        continue
    base.update(Email="", Status="Exclus-fara-email",
                Observatii="nicio adresa verificabila" if (r["email1"] or fid in by_firm)
                else "nicio adresa cunoscuta")
    rows.append(base); stats["Exclus-fara-email"] = stats.get("Exclus-fara-email", 0) + 1

out = pd.DataFrame(rows, columns=["Companie", "Persoana", "Functie", "Email",
                                  "Status", "Data_trimitere", "Observatii"])
out.to_csv("output/contacte_final.csv", index=False)

total = len(out)
nom = stats.get("Nominal", 0)
credits = len(ver)
print(f"TOTAL: {total} firme")
for k, v in sorted(stats.items()):
    print(f"  {k}: {v} ({100*v/total:.1f}%)")
print(f"Nominal verificat: {nom} = {100*nom/total:.1f}% din toate firmele")
print(f"Credite Reoon consumate (total istoric): {credits}")

with open("work/stats.md", "a") as f:
    f.write("\n## Pas 8 - Export final\n\n")
    f.write(f"- Total firme: {total}\n")
    for k, v in sorted(stats.items()):
        f.write(f"- {k}: {v} ({100*v/total:.1f}%)\n")
    f.write(f"- Credite Reoon consumate: {credits}\n")
