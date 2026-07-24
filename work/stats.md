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
