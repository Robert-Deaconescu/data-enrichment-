#!/usr/bin/env python3
"""Pasul 1b - Deduplicare.
Nivel 1: dupa CUI (bid curatat). Nivel 2: rapidfuzz token_sort_ratio pe
nume_norm + judet; >=92 duplicat, 85-92 -> work/dedup_de_verificat.csv.
La duplicate se pastreaza randul cel mai complet, iar campurile lipsa se
completeaza din celelalte randuri ale grupului."""
import pandas as pd
from rapidfuzz import fuzz

df = pd.read_csv("work/01_consolidat.csv", dtype=str).fillna("")
df["cui"] = df["cui"].str.replace(r"\D", "", regex=True)

FIELDS = ["persoana", "email1", "email2", "telefon1", "telefon2", "cui",
          "adresa", "judet", "localitate"]


def completeness(row):
    return sum(1 for f in FIELDS if row[f])


# ------- constructie grupuri de duplicate (union-find simplu) -------
parent = list(range(len(df)))


def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i


def union(i, j):
    ri, rj = find(i), find(j)
    if ri != rj:
        parent[rj] = ri


# Nivel 1: CUI identic
by_cui = {}
for i, cui in enumerate(df["cui"]):
    if cui:
        if cui in by_cui:
            union(by_cui[cui], i)
        else:
            by_cui[cui] = i

# Nivel 2: fuzzy pe nume_norm, blocat pe prima litera pentru viteza
review = []
names = df["nume_norm"].tolist()
juds = df["judet"].tolist()
locs = df["localitate"].str.upper().tolist()
buckets = {}
for i, n in enumerate(names):
    buckets.setdefault(n[0] if n else "?", []).append(i)

for _, idxs in buckets.items():
    for a in range(len(idxs)):
        i = idxs[a]
        for b in range(a + 1, len(idxs)):
            j = idxs[b]
            # potrivire geografica: acelasi judet, sau unul lipsa
            if juds[i] and juds[j] and juds[i] != juds[j]:
                continue
            score = fuzz.token_sort_ratio(names[i], names[j])
            if score >= 92:
                union(i, j)
            elif score >= 85:
                review.append({
                    "idx_a": i, "firma_a": df.at[i, "firma"], "jud_a": juds[i],
                    "loc_a": locs[i], "sursa_a": df.at[i, "sursa"],
                    "idx_b": j, "firma_b": df.at[j, "firma"], "jud_b": juds[j],
                    "loc_b": locs[j], "sursa_b": df.at[j, "sursa"],
                    "scor": score,
                })

groups = {}
for i in range(len(df)):
    groups.setdefault(find(i), []).append(i)

# ------- alegere rand pastrat + completare campuri -------
kept_rows = []
for _, members in groups.items():
    members.sort(key=lambda i: (-completeness(df.iloc[i]), i))
    best = df.iloc[members[0]].copy()
    for m in members[1:]:
        r = df.iloc[m]
        for f in FIELDS + ["firma"]:
            if not best[f] and r[f]:
                best[f] = r[f]
        # email diferit de la duplicat -> pastreaza in email2 daca e liber
        if r["email1"] and r["email1"] != best["email1"] and not best["email2"]:
            best["email2"] = r["email1"]
    best["surse"] = ";".join(sorted(set(df.iloc[m]["sursa"] for m in members)))
    best["nr_duplicate"] = len(members)
    kept_rows.append(best)

out = pd.DataFrame(kept_rows).sort_values(["judet", "firma"]).reset_index(drop=True)
out.insert(0, "id_firma", range(1, len(out) + 1))
out.to_csv("work/02_dedup.csv", index=False)

rev = pd.DataFrame(review).sort_values("scor", ascending=False) if review else pd.DataFrame()
rev.to_csv("work/dedup_de_verificat.csv", index=False)

dup_count = len(df) - len(out)
with open("work/stats.md", "a") as f:
    f.write("\n## Pas 1b - Deduplicare\n\n")
    f.write(f"- Randuri intrare: {len(df)}\n")
    f.write(f"- Duplicate eliminate (CUI identic sau scor >= 92): {dup_count}\n")
    f.write(f"- Firme unice: {len(out)}\n")
    f.write(f"- Perechi incerte (85-92) de verificat manual: {len(rev)} -> dedup_de_verificat.csv\n")
    f.write(f"- Firme cu email generic dupa merge: {(out['email1'] != '').sum()}\n")
    f.write(f"- Firme cu persoana dupa merge: {(out['persoana'] != '').sum()}\n")
    f.write(f"- Firme cu posibil CUI: {(out['cui'] != '').sum()}\n")

print(f"unice: {len(out)}, duplicate eliminate: {dup_count}, de verificat: {len(rev)}")
