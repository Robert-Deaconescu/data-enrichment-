# Raport final — Imbogatire baza de date B2B Transilvania Business

Data: 25 iulie 2026 · Livrabil: `output/contacte_final.csv` (2.495 firme, format fix tab Contacte)

## 1. Rezultate

| Status | Firme | % din total | Ce inseamna |
|---|---|---|---|
| **Nominal verificat (Pending)** | **300** | **12,0%** | Adresa decidentului, confirmata tehnic SMTP (Reoon safe/valid) |
| **Generic verificat (Pending)** | **359** | **14,4%** | Adresa generica existenta, confirmata livrabila |
| Catch-all (segment separat) | 325 | 13,0% | Domeniul accepta orice adresa — neconfirmabil prin SMTP; NU intra in campanie fara validare secundara |
| Incert-mx | 58 | 2,3% | office@ pe domeniu ghicit (MX activ) — clientul decide |
| Exclus-fara-email | 1.446 | 58,0% | Nicio adresa verificabila (majoritatea: firme fara domeniu propriu, generice invalide/moarte) |
| Exclus-inactiv | 7 | 0,3% | Radiate/inactive la ANAF |

**In campanie intra 659 de firme (26,4%) cu adrese 100% verificate tehnic** — tinta de bounce < 2% este protejata (trimitere doar pe Status Pending).

### Sursele adreselor nominale (300)

| Sursa (coloana Observatii) | Firme |
|---|---|
| `tipar-verificat` — tipar generat pe domeniul validat al firmei | 187 |
| `site` — adresa publicata pe site, verificata | 61 |
| `tipar-mx` — tipar pe domeniu descoperit (MX activ, filtru de siguranta) | 52 |

### Credite consumate

- **Reoon: 8.366 credite** din pachetul de 10.000 ($11,90) — raman ~1.634 pentru re-verificari inainte de campanie.
- Toate celelalte surse (ANAF/demoanaf, scraping site-uri, descoperire domenii): gratuite.

## 2. Fata de tinta contractuala (50–70% nominale)

**Rezultat: 12,0% pe totalul bazei / 27,4% pe firmele cu domeniu propriu (1.103).**

Tinta de 50–70% este structural imposibila pe acest univers de firme, indiferent de unealta sau buget:

1. **Doar 44% din firme au domeniu propriu** (1.103 dupa descoperirea si auditarea a 626 domenii noi). Fara domeniu propriu nu exista adresa nominala — firmele folosesc yahoo/gmail. Plafonul teoretic era deci 44%, nu 100%.
2. Benchmarkurile 2026 verificate live (Anymail Finder, SyncGTM, Leadbomb): tool-urile comerciale ating **40–55% pe SMB-uri din piete UE secundare** — pe firmele *atacabile*, nu pe total. Rezultatul nostru de 27,4% pe firmele cu domeniu e in norma pietei pentru micro-IMM-uri, obtinut la ~1/30 din costul finderelor comerciale.
3. Multe IMM-uri mici pur si simplu **nu au cutii postale nominale** — exista doar office@.

**Recomandare pentru discutia cu clientul** (de purtat acum, nu la livrare): re-ancorarea metricii pe (a) firmele cu domeniu propriu si/sau (b) "contact verificat" (nominal SAU generic verificat + numele decidentului pentru personalizare — numele exista pentru 93% din firme, din ANAF). Pe definitia (b), livram deja 26,4% adrese sigure + 13% recuperabile din catch-all.

## 3. Rezerva de crestere: segmentul Catch-all (325 firme, 317 cu decident cunoscut)

Consensul industriei 2026 (cercetare live, surse in `work/research_live/04_metodologie.md`): catch-all nu se arunca — se valideaza cu servicii specializate si se trimite in segment separat.

- **BounceBan** (~$34/luna, teste independente: 0,2% bounce observat; arbitrul de catch-all in benchmarkul Anymail Finder): validarea celor ~325 de adrese ar recupera realist **50–150 nominale suplimentare** → total nominale 350–450 (14–18% din total, 32–41% din firmele cu domeniu).
- Alternativ, gratuit dar partial: campanie-pilot separata (50–100 emailuri, domeniu incalzit, oprire automata la 2–3% bounce).

## 4. Avertisment important: infrastructura de trimitere (Make.com)

Cerintele Gmail/Yahoo/Microsoft in vigoare (verificate live, enforcement din nov. 2025): SPF+DKIM+DMARC aliniat, one-click unsubscribe RFC 8058, spam rate < 0,3% (tinta practica < 0,1%). Configuratia "Gmail personal + Make.com" risca suspendarea contului si plafonul sigur e ~25 emailuri/zi.

**Necesare inainte de campanie:** Google Workspace pe domeniu dedicat (nu domeniul principal TB), DMARC minim p=none aliniat, warmup 14–21 zile, 30–50 emailuri/zi/inbox, procesare automata a bounce-urilor in Make.com (hard bounce → suprimare imediata). Daca lista sta > 30–60 zile, re-verificare Reoon inainte de trimitere (creditele ramase acopera).

## 5. Nota GDPR

Adresele nominale sunt date personale. Pozitia proiectului e apărabila: surse publice (administratori ONRC/ANAF, site-ul propriu al firmei), interes legitim B2B, opt-out in fiecare mesaj, iar coloana Observatii pastreaza sursa fiecarei adrese (exact ce ar cere o verificare ANSPDCP). De evitat: liste nominale cumparate de la terti (temei fragil, art. 14).

## 6. Metodologie (pe scurt) si reproducere

Consolidare 5 fisiere (2.518 randuri) → dedup CUI + fuzzy (2.495 firme) → ANAF/demoanaf (1.958 CUI rezolvate, 412 administratori adaugati, 7 radiate) → descoperire + audit domenii (650 → 1.103 firme cu domeniu validat) → scraping pagini contact (1.178 domenii, robots.txt respectat, 1 req/s) → tipare nominale RO (6 variante/persoana) → **verificare Reoon mod power, waterfall cu oprire la primul valid** (8.366 credite, 0 erori nerecuperate) → runda de recuperare MX cu filtru de siguranta nume-domeniu (558 firme, 30 domenii riscante excluse) → export cu trasabilitate completa (fiecare adresa Pending are dovada verificarii in `work/06_verificari.csv`).

Scripturile 01–13 din `scripts/` reproduc integral pipeline-ul; `work/stats.md` logheaza fiecare pas.
