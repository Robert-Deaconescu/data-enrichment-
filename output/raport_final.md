# Raport final — Imbogatire baza de date B2B Transilvania Business

Data: 27 iulie 2026 · Livrabil: `output/contacte_final.csv` (2.495 firme, format fix tab Contacte)

## 1. Rezultate finale

| Status | Firme | % din total | Ce inseamna |
|---|---|---|---|
| **Nominal verificat (Pending)** | **366** | **14,7%** | Adresa decidentului, confirmata tehnic SMTP (Reoon safe/valid) |
| **Generic verificat (Pending)** | **407** | **16,3%** | Adresa generica (existenta sau office@ pe domeniu validat), confirmata livrabila |
| Catch-all (segment separat) | 380 | 15,2% | Domeniul accepta orice adresa — neconfirmabil prin SMTP; NU intra in campanie fara validare secundara (BounceBan) |
| Incert-mx | 61 | 2,4% | office@ pe domeniu ghicit (MX activ, neconfirmat) — clientul decide |
| Exclus-fara-email | 1.274 | 51,1% | Nicio adresa verificabila |
| Exclus-inactiv | 7 | 0,3% | Radiate/inactive la ANAF |

**In campanie intra 773 de firme (31,0%) cu adrese 100% verificate tehnic** — tinta de bounce < 2% e protejata (trimitere doar pe Status Pending).

### Sursele adreselor nominale (366)

| Sursa (coloana Observatii) | Firme |
|---|---|
| `tipar-verificat` — tipar pe domeniul cunoscut al firmei | 189 |
| `site` — adresa publicata pe site, verificata | 61 |
| `tipar-web` — tipar pe domeniu descoperit prin cautare web + validat CUI/nume | 55 |
| `tipar-mx` — tipar pe domeniu ghicit cu MX activ | 52 |
| `bounceban` — catch-all validat secundar (100 credite client) | 9 |

### Costuri

- **Reoon: 9.029 credite** din pachetul de 10.000 ($11,90). Restul: $0.
- Runda de imbunatatiri gratuite (cautare web domenii, retry unknown, re-validari):
  +57 nominale si +48 generice fata de prima livrare (659 → 773 contacte sigure, incl. 9 din BounceBan).

## 2. Descoperirea de domenii prin cautare web (runda gratuita)

Toate cele **1.385 de firme fara domeniu** au fost cautate pe web (28 de loturi de
agenti, cautare + validare stricta): **533 candidati** → **392 domenii validate**
(CUI-ul sau numele firmei confirmate pe site + server de email activ). Acoperirea
cu domeniu a crescut de la 44% la **~60%**. Tiparele pe aceste domenii au produs
55 nominale si zeci de generice noi; restul domeniilor noi raman in fisierele
`work/17_domenii_web/` pentru rundele viitoare (findere, BounceBan).

## 3. Fata de tinta contractuala (50–70% nominale)

**Rezultat: 14,7% pe totalul bazei.** Tinta de 50–70% ramane structural imposibila
pe acest univers (multe micro-IMM-uri nu au deloc mailbox nominal; benchmarkurile
2026: 40–55% chiar pentru tool-uri comerciale pe SMB-uri UE, aplicat doar firmelor
atacabile). Recomandare neschimbata: re-ancorarea metricii pe (a) firmele cu
domeniu si/sau (b) "contact verificat" (nominal SAU generic verificat + numele
decidentului — disponibil pentru 93% din firme, din ANAF). Pe definitia (b) livram
31,0% + 15,2% recuperabil din catch-all.

## 4. Rezerva de crestere ramasa (necesita conturi create de client)

1. **BounceBan** — primele 100 de credite RULATE: 9 deliverable promovate ca nominale,
   54 undeliverable (tipare eliminate definitiv), 27 risky. Pentru restul de 380 de
   firme catch-all: verificarile single gratuite din planul free (manual) sau alte credite.
2. **Free tiers findere** (Prospeo 75/luna, Dropcontact 50, GetProspect 50/luna
   s.a. — majoritatea taxeaza doar rezultatele valide) pe firmele cu domeniu fara
   nominala: estimat **+150–300 nominale**; cheia Prospeo intra in `.env` si rularea
   e automatizata.
3. Retry-ul pe "unknown" a fost deja executat (+9 firme; majoritatea unknown-urilor
   sunt structural neverificabile pe hosting-ul respectiv).

Proiectia cu tot planul executat: **~900–1.200 contacte sigure (36–48%)**, din care
450–650 nominale.

## 5. Avertisment: infrastructura de trimitere (Make.com)

Cerintele Gmail/Yahoo/Microsoft in vigoare: SPF+DKIM+DMARC aliniat, one-click
unsubscribe RFC 8058, spam rate < 0,3%. "Gmail personal + Make.com" risca
suspendarea si plafonul sigur e ~25/zi. Necesare: Google Workspace pe domeniu
dedicat, DMARC p=none, warmup 14–21 zile, 30–50/zi/inbox, procesare automata a
bounce-urilor. Daca lista sta > 30–60 zile: re-verificare Reoon (creditele ramase
acopera).

## 6. Nota GDPR

Adresele nominale sunt date personale. Pozitia proiectului: surse publice
(administratori ONRC/ANAF, site-ul firmei), interes legitim B2B, opt-out per mesaj,
sursa fiecarei adrese in coloana Observatii. De evitat: liste nominale cumparate.

## 7. Metodologie si trasabilitate

Consolidare 5 fisiere (2.518 randuri) → dedup (2.495 firme) → ANAF (1.958 CUI, 412
administratori, 7 radiate) → descoperire domenii in 2 etape (audit subagenti +
cautare web cu validare CUI/nume: 1.105 → ~1.500 firme cu domeniu) → scraping
pagini contact → tipare nominale RO → verificare Reoon mod power, waterfall paralel
cu checkpoint → export cu trasabilitate completa (fiecare adresa Pending are dovada
in `work/06_verificari.csv`). QA automatizat: format, trasabilitate, statistici —
trecut integral. Scripturile 01–13 + `work/stats.md` reproduc pipeline-ul.
Cercetarea (7 rapoarte cu surse citate) e in `work/research_live/`.
