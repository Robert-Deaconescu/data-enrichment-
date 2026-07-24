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
