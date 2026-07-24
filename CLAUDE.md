# Proiect: Imbogatire baza de date B2B - Transilvania Business (Dezvolt AI)

## Context
Contract semnat: consolidarea a 5 fisiere (~3.000 randuri, ~2.500 firme unice
dupa dedup) si identificarea adreselor de e-mail nominale ale decidentilor
(administrator, director general, director marketing) pentru 50-70% din firme,
VERIFICATE TEHNIC. Restul raman pe adresa generica existenta. Rezultatul se
incarca in Google Sheets "Baza de date TB" (tabul Contacte), care alimenteaza
un sistem de trimitere automata in Make.com.

## Structura proiectului
- `input/` - cele 5 fisiere sursa primite de la client (NU se modifica)
- `work/` - fisiere intermediare + `stats.md` (log per pas)
- `output/contacte_final.csv` - livrabilul
- `.env` - REOON_API_KEY, PROSPEO_API_KEY (optional)

## Regulile proiectului
1. Foloseste skill-ul `email-enrichment` pentru orice pas din pipeline.
2. NICIO adresa neverificata nu intra in output. Tinta bounce < 2%.
3. Inainte de orice consum de credite platite: arata costul si cere aprobare.
4. API-uri gratuite folosite: demoanaf.ro (300 req/min max, foloseste 200),
   webservicesp.anaf.ro (fallback). Rate limiting politicos peste tot.
5. Scraping: 1 cerere/secunda, robots.txt respectat, doar pagini de contact.
6. Formatul de iesire este FIX (coloanele din tabul Contacte) - nu-l redesena.
7. Firmele radiate/inactive si adresele generice invalide se exclud din campanie
   (Status Exclus-*), dar raman in fisier pentru evidenta clientului.
8. La final: raport cu % nominale verificate vs tinta contractuala 50-70%,
   surse per adresa si credite consumate.

## Biblioteci
pandas, openpyxl, rapidfuzz, unidecode, requests, beautifulsoup4, python-dotenv.
Playwright MCP doar pentru site-uri JS-only.
