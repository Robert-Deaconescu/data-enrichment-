# Stats pipeline - Baza de date TB

## Pas 1a - Consolidare

| Sursa | Randuri |
|---|---|
| ADRESE_2000 | 1452 |
| suplimentar | 526 |
| mures | 446 |
| grecia | 88 |
| 30_ani | 6 |
| **TOTAL** | **2518** |

- Randuri cu email generic existent: 868
- Randuri cu persoana de contact: 1942
- Randuri cu posibil CUI (bid): 613

## Pas 1b - Deduplicare

- Randuri intrare: 2518
- Duplicate eliminate (CUI identic sau scor >= 92): 23
- Firme unice: 2495
- Perechi incerte (85-92) de verificat manual: 15 -> dedup_de_verificat.csv
- Firme cu email generic dupa merge: 867
- Firme cu persoana dupa merge: 1921
- Firme cu posibil CUI: 613

## Pas 2+3 - ANAF + domenii

- CUI rezolvat: 1958/2495
- Firme excluse (radiate/inactive): 7
- Persoana completata din administratori ANAF: 412
- Total firme cu persoana: 2333
- Firme cu domeniu propriu (din email generic): 650

## Pas 4 - Tipare e-mail

- Firme eligibile (Pending + persoana + domeniu propriu): 587
- Total tipare generate: 3552
- Medie tipare/firma: 6.1

## Pas 5 - Calibrare Reoon (esantion, credite gratuite)

- Firme testate: 33 (esantion din cele 587 eligibile)
- Credite consumate: 146 (toate creditele gratuite disponibile azi)
- Rezultat: 5 firme cu adresa nominala valida (15%), 7 catch-all, 21 fara rezultat
- Cost mediu: 4.4 credite/firma
- Concluzie: tiparele singure au randament scazut; scrapingul + descoperirea
  de domenii sunt necesare pentru a creste acoperirea

## Plafonul structural

- Doar 648/2488 firme Pending au domeniu web propriu (dedus din emailul generic)
- 1840 firme nu au niciun domeniu cunoscut -> nicio adresa nominala posibila
  fara un pas de descoperire a site-urilor
- Tinta contractuala 50-70% nominale = 1244-1742 firme; plafonul actual
  fara descoperire domenii: ~587 firme (24%) chiar la randament 100%

## Pas 2+3 - ANAF + domenii

- CUI rezolvat: 1958/2495
- Firme excluse (radiate/inactive): 7
- Persoana completata din administratori ANAF: 412
- Total firme cu persoana: 2333
- Firme cu domeniu propriu (din email generic): 1185

## Pas 4 - Tipare e-mail

- Firme eligibile (Pending + persoana + domeniu propriu): 1114
- Total tipare generate: 6734
- Medie tipare/firma: 6.0

## Pas 2+3 - ANAF + domenii

- CUI rezolvat: 1958/2495
- Firme excluse (radiate/inactive): 7
- Persoana completata din administratori ANAF: 412
- Total firme cu persoana: 2333
- Firme cu domeniu propriu (din email generic): 1105

## Pas 4 - Tipare e-mail

- Firme eligibile (Pending + persoana + domeniu propriu): 1038
- Total tipare generate: 6268
- Medie tipare/firma: 6.0

## Rezumat pre-verificare (toate procesele gratuite complete)

- Domenii descoperite web: 626 gasite / 1840 firme fara domeniu (568 cu MX)
- Audit subagenti (2 runde): 588 domenii auditate -> 462 corecte, 32 gresite,
  94 incerte; 113 excluse la verificare manuala (domenii_de_verificat_manual.csv)
- Firme cu domeniu validat: 1105 (fata de 648 initial)
- Firme eligibile tipare: 1038 (6268 tipare)
- Scraping 2 runde: 1178 domenii scanate, 612 cu adrese publicate
- Dedup arbitrat de agenti: 1 duplicat confirmat (MATEROM), 12 distincte, 2 incerte
- Necesar credite Reoon: ~6290 (+20% marja = ~7550) -> pachet 10K ($11.90)

## Runda recuperare MX (sugestia clientului)

- 588 firme fara site au totusi domeniu candidat cu server email activ (MX)
- Regula de acceptare: tipar administrator valid = nominal; doar office@ = generic 'incert'
- Plafonul teoretic creste: 1105 + 588 = 1693 firme cu o cale spre adresa (68%)

## Runda MX - coada construita

- Firme candidate: 588; excluse de filtrul de siguranta: 30
- Firme in coada MX: 558; tipare totale (max): 3808

## Pas 8 - Export final

- Total firme: 2495
- Catch-all: 325 (13.0%)
- Exclus-fara-email: 1446 (58.0%)
- Exclus-inactiv: 7 (0.3%)
- Generic: 359 (14.4%)
- Incert-mx: 58 (2.3%)
- Nominal: 300 (12.0%)
- Credite Reoon consumate: 8044

## Pas 8 - Export final

- Total firme: 2495
- Catch-all: 357 (14.3%)
- Exclus-fara-email: 1404 (56.3%)
- Exclus-inactiv: 7 (0.3%)
- Generic: 362 (14.5%)
- Incert-mx: 63 (2.5%)
- Nominal: 302 (12.1%)
- Credite Reoon consumate: 8608

## Pas 8 - Export final

- Total firme: 2495
- Catch-all: 357 (14.3%)
- Exclus-fara-email: 1365 (54.7%)
- Exclus-inactiv: 7 (0.3%)
- Generic: 379 (15.2%)
- Incert-mx: 62 (2.5%)
- Nominal: 325 (13.0%)
- Credite Reoon consumate: 8608

## Pas 8 - Export final

- Total firme: 2495
- Catch-all: 379 (15.2%)
- Exclus-fara-email: 1343 (53.8%)
- Exclus-inactiv: 7 (0.3%)
- Generic: 379 (15.2%)
- Incert-mx: 62 (2.5%)
- Nominal: 325 (13.0%)
- Credite Reoon consumate: 8816

## Pas 8 - Export final

- Total firme: 2495
- Catch-all: 379 (15.2%)
- Exclus-fara-email: 1320 (52.9%)
- Exclus-inactiv: 7 (0.3%)
- Generic: 391 (15.7%)
- Incert-mx: 61 (2.4%)
- Nominal: 337 (13.5%)
- Credite Reoon consumate: 8816

## Pas 8 - Export final

- Total firme: 2495
- Catch-all: 389 (15.6%)
- Exclus-fara-email: 1274 (51.1%)
- Exclus-inactiv: 7 (0.3%)
- Generic: 407 (16.3%)
- Incert-mx: 61 (2.4%)
- Nominal: 357 (14.3%)
- Credite Reoon consumate: 9029

## Runda de imbunatatiri gratuite (finalizata)

- Cautare web: 1.385 firme fara domeniu -> 533 candidati -> 392 domenii validate
- Retry unknown: +9 firme; re-verificare generice ambigue: +6
- Rezultat: 659 -> 764 contacte sigure (357 nominale, 407 generice)
- Credite Reoon: 9.029/10.000; restul actiunilor: $0
