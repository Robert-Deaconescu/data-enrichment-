---
name: email-enrichment
description: Use this skill for the Transilvania Business data enrichment project or any Romanian B2B contact database task - consolidating company lists from multiple Excel/CSV files, deduplicating Romanian companies (by CUI or fuzzy name), finding administrators/decision-makers via Romanian public APIs (demoanaf, ANAF), generating and verifying nominal email addresses (pattern waterfall + Reoon verification + website scraping), and exporting to the campaign spreadsheet format. Trigger on mentions of "imbogatire", "enrichment", "baza de date TB", "consolidare firme", "adrese nominale", or when the user provides Romanian company list files to process.
---

# Email Enrichment - firme romanesti (pipeline waterfall)

Obiectiv: dintr-o lista de firme romanesti, produce o baza finala cu adrese de
e-mail nominale ale decidentilor, VERIFICATE TEHNIC, pentru 50-70% din firme.
Restul pastreaza adresa generica existenta. Nicio adresa neverificata nu intra
in fisierul final.

## Reguli generale (obligatorii)

- Fiecare pas scrie un fisier intermediar in `work/` (ex: `work/01_consolidat.csv`)
  si un log de statistici in `work/stats.md`. Niciun pas nu suprascrie inputul.
- Inainte de ORICE apel API platit (Reoon peste creditele gratuite, Prospeo):
  afiseaza numarul de credite necesare si costul estimat si CERE APROBAREA userului.
- API-urile gratuite se apeleaza cu rate limiting politicos si retry cu backoff.
- La final raporteaza: nr. firme, % adrese nominale verificate, % generice,
  % fara nicio adresa, comparat cu tinta contractuala 50-70%.

## Pasul 1 - Consolidare si deduplicare

Biblioteci: pandas, openpyxl, rapidfuzz, unidecode.

1. Citeste toate fisierele sursa din `input/`. Normalizeaza: trim, un singur
   spatiu, forma juridica unificata (S.R.L. -> SRL, S.A. -> SA), diacritice
   pastrate in numele persoanelor dar coloana auxiliara `nume_norm` fara
   diacritice (unidecode) pentru matching.
2. Dedup nivel 1: dupa CUI (daca exista coloana; curata prefixul RO si spatiile).
3. Dedup nivel 2 (fara CUI): rapidfuzz `token_sort_ratio` pe
   `nume_norm + judet/localitate`; prag >= 92 = duplicat; 85-92 = lista de
   verificat manual, scrisa in `work/dedup_de_verificat.csv`.
4. La duplicate, pastreaza randul cu cele mai multe campuri completate.

## Pasul 2 - Date oficiale + administratori (GRATUIT)

Sursa principala: `GET https://demoanaf.ro/api/company/{CUI}` - JSON, fara cheie,
max 300 cereri/minut (foloseste 200/min ca marja). Extrage:
- administratorii -> completeaza coloana Persoana unde lipseste
- starea firmei -> firmele radiate/inactive primesc Status `Exclus-inactiv`
  si NU intra in campanie
- statusul TVA (informativ, coloana Observatii)

Fallback daca demoanaf nu raspunde: pyAnaf / `webservicesp.anaf.ro` (fara
administratori, doar stare + denumire + adresa).

Pentru firmele fara CUI: incearca intai cautarea dupa nume pe demoanaf; ce nu
se gaseste ramane cu datele din fisierele sursa.

## Pasul 3 - Domeniul web al firmei

Ordine: (a) coloana site din fisiere; (b) domeniul adresei generice existente
(office@firma.ro -> firma.ro), EXCLUDE domeniile publice (gmail, yahoo etc.);
(c) fara domeniu -> firma ramane pe adresa generica existenta sau fara email.

## Pasul 4 - Generarea tiparelor de e-mail

Pentru fiecare firma cu Persoana + domeniu propriu, genereaza IN ACEASTA ORDINE
(probabilitate descrescatoare in Romania):
1. prenume.nume@domeniu
2. prenume@domeniu
3. nume.prenume@domeniu
4. nume@domeniu
5. prenumenume@domeniu
6. p.nume@domeniu (initiala)

Reguli: totul lowercase; diacriticele se translitereaza (s,t,a,a,i - fara
virgulite/caciuli); la prenume compuse (Ana-Maria) foloseste primul token; la
nume de familie duble foloseste ambele unite cu punct si separat ca variante.

## Pasul 5 - Verificare (Reoon)

API key in `.env`: `REOON_API_KEY`. Planul gratuit are 600 credite/luna cu API -
foloseste-le intai pe un esantion de 100-200 ca sa calibrezi; pentru volum,
pachetul instant (cere aprobarea inainte de cumparare/consum masiv).

- Verifica tiparele IN ORDINE si OPRESTE-TE la primul rezultat `valid`/`safe`
  per firma (economie de credite ~50%).
- `catch-all`/`risky`: NU conteaza ca nominal verificat; firma trece la pasul 6.
- `invalid`: incearca urmatorul tipar.
- Marcheaza in Observatii sursa: `tipar-verificat`.

## Pasul 6 - Scraping site-uri (GRATUIT, pentru firmele ramase)

Pentru firmele fara adresa nominala dupa pasul 5, viziteaza paginile
`/contact`, `/contacte`, `/echipa`, `/despre-noi`, `/despre` ale domeniului:
- requests + BeautifulSoup; 1 cerere/secunda; respecta robots.txt; user-agent
  onest; daca site-ul e JS-only, foloseste Playwright MCP.
- Extrage adrese din mailto: si din text (regex), prefera-le pe cele care contin
  numele persoanei din coloana Persoana.
- Orice adresa gasita trece OBLIGATORIU prin verificarea de la pasul 5 inainte
  de acceptare. Sursa in Observatii: `site`.

## Pasul 7 (OPTIONAL, platit) - Prospeo pentru firmele valoroase ramase

Doar cu aprobarea explicita a userului. `PROSPEO_API_KEY` in `.env`,
~$10/1000 credite (finder+verifier combinat). Ruleaza doar pe subsetul ramas
fara adresa nominala, eventual filtrat la firmele mari. Sursa: `prospeo`.

## Pasul 8 - Verificarea finala si exportul

1. TOATE adresele din fisierul final (nominale + generice preexistente) trec
   printr-o verificare finala; adresele generice invalide se elimina (firma
   ramane fara email -> Status `Exclus-fara-email`).
2. Export `output/contacte_final.csv` cu EXACT aceste coloane, in aceasta ordine:
   `Companie, Persoana, Functie, Email, Status, Data_trimitere, Observatii`
   - Status = `Pending` pentru toate randurile care intra in campanie
   - Data_trimitere = gol
   - Observatii = sursa adresei (tipar-verificat / site / prospeo / generic)
3. Raporteaza statistica finala vs tinta 50-70% si numarul de credite consumate.
