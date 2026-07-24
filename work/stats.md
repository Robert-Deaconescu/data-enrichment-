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
