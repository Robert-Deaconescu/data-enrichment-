#!/usr/bin/env python3
"""Pasul 1a - Consolidare: citeste cele 5 fisiere din input/, normalizeaza
si scrie work/01_consolidat.csv + log in work/stats.md."""
import re
import pandas as pd
from unidecode import unidecode

pd.set_option("future.no_silent_downcasting", True)

JUD_MAP = {
    "AB": "ALBA", "AR": "ARAD", "AG": "ARGES", "BC": "BACAU", "BH": "BIHOR",
    "BN": "BISTRITA-NASAUD", "BT": "BOTOSANI", "BV": "BRASOV", "BR": "BRAILA",
    "B": "BUCURESTI", "BZ": "BUZAU", "CS": "CARAS-SEVERIN", "CL": "CALARASI",
    "CJ": "CLUJ", "CT": "CONSTANTA", "CV": "COVASNA", "DB": "DAMBOVITA",
    "DJ": "DOLJ", "GL": "GALATI", "GR": "GIURGIU", "GJ": "GORJ", "HR": "HARGHITA",
    "HD": "HUNEDOARA", "IL": "IALOMITA", "IS": "IASI", "IF": "ILFOV",
    "MM": "MARAMURES", "MH": "MEHEDINTI", "MS": "MURES", "NT": "NEAMT",
    "OT": "OLT", "PH": "PRAHOVA", "SM": "SATU MARE", "SJ": "SALAJ",
    "SB": "SIBIU", "SV": "SUCEAVA", "TR": "TELEORMAN", "TM": "TIMIS",
    "TL": "TULCEA", "VS": "VASLUI", "VL": "VALCEA", "VN": "VRANCEA",
}

TITLE_RE = re.compile(
    r"^\s*(D-?LUI|D-?NEI|DOAMNEI|DOMNULUI|DOAMNEI/D-?LUI|D-?NA|DL\.?|DNA\.?)[\s/]+",
    re.I,
)


def clean_text(v):
    if pd.isna(v):
        return ""
    s = re.sub(r"\s+", " ", str(v)).strip()
    return "" if s.lower() in ("nan", "none") else s


def norm_firm(name: str) -> str:
    """Forma juridica unificata: S.R.L. -> SRL, S.A. -> SA etc."""
    s = clean_text(name).upper()
    s = re.sub(r"\bS\.?\s*R\.?\s*L\.?(?=\s|$|\.)", "SRL", s)
    s = re.sub(r"\bS\.?\s*A\.?(?=\s|$|\.)", "SA", s)
    s = re.sub(r"\bP\.?\s*F\.?\s*A\.?(?=\s|$|\.)", "PFA", s)
    s = re.sub(r"\bS\.?\s*C\.?\s+", "", s)  # prefixul "SC "
    s = re.sub(r"[.,]+$", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def norm_key(name: str) -> str:
    """nume_norm: fara diacritice, fara forma juridica, pentru matching."""
    s = unidecode(norm_firm(name)).upper()
    s = re.sub(r"\b(SRL|SA|PFA|SCS|SNC|SRL-D|II|IF)\b", "", s)
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def clean_person(v: str) -> str:
    s = clean_text(v)
    while True:
        s2 = TITLE_RE.sub("", s).strip()
        if s2 == s:
            break
        s = s2
    # "ADMINISTRATOR" singur nu e o persoana
    if not s or unidecode(s).upper() in ("ADMINISTRATOR", "DIRECTOR", "MANAGER"):
        return ""
    return s.title() if s.isupper() else s


def clean_email(v: str) -> str:
    s = clean_text(v).lower().rstrip(".;,")
    if re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", s):
        return s
    return ""


def clean_phone(v) -> str:
    s = clean_text(v)
    s = re.sub(r"\.0$", "", s)
    digits = re.sub(r"\D", "", s)
    if 8 <= len(digits) <= 12:
        if len(digits) == 9 and digits[0] == "7":
            digits = "0" + digits
        return digits
    return ""


def norm_jud(v: str) -> str:
    s = unidecode(clean_text(v)).upper().replace(".", "")
    s = re.sub(r"\s+", " ", s).strip()
    if s in JUD_MAP:
        return JUD_MAP[s]
    if s.startswith("SECTOR"):
        return "BUCURESTI"
    return s


rows = []

# --- 1. ADRESE_2000_134_135_TB.xlsx (fara header; col 0-3 = expeditor, se ignora)
df = pd.read_excel("input/ADRESE_2000_134_135_TB.xlsx", header=None)
n_kept = 0
for _, r in df.iterrows():
    firma = clean_text(r[4])
    if not firma:
        continue
    n_kept += 1
    loc = clean_text(r[7])
    jud = norm_jud(r[9])
    if loc.upper().startswith("SECTOR") and not jud:
        jud = "BUCURESTI"
    rows.append({
        "sursa": "ADRESE_2000",
        "firma": norm_firm(firma),
        "judet": jud,
        "localitate": loc.title(),
        "persoana": clean_person(r[10]),
        "email1": clean_email(r[12]),
        "email2": "",
        "telefon1": clean_phone(r[11]),
        "telefon2": "",
        "cui": "",
        "adresa": ", ".join(x for x in (clean_text(r[5]), clean_text(r[6])) if x),
    })
print(f"ADRESE_2000: {n_kept} randuri cu firma din {len(df)}")

# --- 2. Baza_date_creat_in_mures.xlsx
df = pd.read_excel("input/Baza_date_creat_in_mures.xlsx", sheet_name="firma")
for _, r in df.iterrows():
    firma = clean_text(r["Firma"])
    if not firma:
        continue
    rows.append({
        "sursa": "mures",
        "firma": norm_firm(firma),
        "judet": norm_jud(r["Jud"]),
        "localitate": clean_text(r["Localitate"]).title(),
        "persoana": clean_person(r["Contact"]),
        "email1": clean_email(r["Email1"]),
        "email2": clean_email(r["Email2"]),
        "telefon1": clean_phone(r["Mobil1"]),
        "telefon2": clean_phone(r["Mobil2"]),
        "cui": "",
        "adresa": "",
    })
print(f"mures: {len(df)} randuri")

# --- 3. suplimentar (are bid = posibil CUI)
df = pd.read_excel("input/suplimentar_baza_de +date_creat_in_mures.xlsx", sheet_name="firma")
for _, r in df.iterrows():
    firma = clean_text(r["Firma"])
    if not firma:
        continue
    bid = re.sub(r"\D", "", clean_text(r["bid"]))
    rows.append({
        "sursa": "suplimentar",
        "firma": norm_firm(firma),
        "judet": norm_jud(r["Jud"]),
        "localitate": clean_text(r["Localitate"]).title(),
        "persoana": "",
        "email1": clean_email(r["Email1"]),
        "email2": clean_email(r["Email2"]),
        "telefon1": clean_phone(r["Mobil1"]),
        "telefon2": clean_phone(r["Mobil2"]),
        "cui": bid,  # de validat la pasul ANAF
        "adresa": "",
    })
print(f"suplimentar: {len(df)} randuri")

# --- 4. baza_date_grecia.xlsx (are bid = posibil CUI)
df = pd.read_excel("input/baza_date_grecia.xlsx", sheet_name="firma")
for _, r in df.iterrows():
    firma = clean_text(r["Firma"])
    if not firma:
        continue
    bid = re.sub(r"\D", "", clean_text(r["bid"]))
    adresa = ", ".join(x for x in (
        clean_text(r["Tip"]) + " " + clean_text(r["Strada"]),
        ("NR. " + clean_text(r["Nr"])) if clean_text(r["Nr"]) else "",
    ) if x.strip())
    rows.append({
        "sursa": "grecia",
        "firma": norm_firm(firma),
        "judet": norm_jud(r["Jud"]),
        "localitate": clean_text(r["Localitate"]).title(),
        "persoana": clean_person(r["Contact"]),
        "email1": clean_email(r["Email1"]),
        "email2": clean_email(r["Email2"]),
        "telefon1": "",
        "telefon2": "",
        "cui": bid,
        "adresa": adresa.strip(),
    })
print(f"grecia: {len(df)} randuri")

# --- 5. baza_date_30_ani.xlsx (header la randul 5, doar ~6 firme reale)
df = pd.read_excel("input/baza_date_30_ani.xlsx", header=None)
n_kept = 0
for i, r in df.iterrows():
    firma = clean_text(r[1])
    if i <= 5 or not firma:
        continue
    n_kept += 1
    emails = [clean_email(r[c]) for c in (4, 6, 7)]
    emails = [e for e in emails if e]
    rows.append({
        "sursa": "30_ani",
        "firma": norm_firm(firma),
        "judet": "",
        "localitate": "",
        "persoana": clean_person(r[3]),
        "email1": emails[0] if emails else "",
        "email2": emails[1] if len(emails) > 1 else "",
        "telefon1": "",
        "telefon2": "",
        "cui": "",
        "adresa": "",
    })
print(f"30_ani: {n_kept} randuri reale")

out = pd.DataFrame(rows)
out["nume_norm"] = out["firma"].map(norm_key)
out = out[out["nume_norm"] != ""]
out.to_csv("work/01_consolidat.csv", index=False)

with open("work/stats.md", "w") as f:
    f.write("# Stats pipeline - Baza de date TB\n\n## Pas 1a - Consolidare\n\n")
    f.write(f"| Sursa | Randuri |\n|---|---|\n")
    for s, n in out["sursa"].value_counts().items():
        f.write(f"| {s} | {n} |\n")
    f.write(f"| **TOTAL** | **{len(out)}** |\n\n")
    f.write(f"- Randuri cu email generic existent: {(out['email1'] != '').sum()}\n")
    f.write(f"- Randuri cu persoana de contact: {(out['persoana'] != '').sum()}\n")
    f.write(f"- Randuri cu posibil CUI (bid): {(out['cui'] != '').sum()}\n")

print(f"\nTOTAL consolidat: {len(out)} -> work/01_consolidat.csv")
