# Sinteza: planul de crestere GRATUITA a rezultatelor (cercetare live, iulie 2026)

> Sinteza celor 4 rapoarte live: `05_catchall_gratuit.md`, `06_domenii_gratuit.md`,
> `07_findere_gratuit.md`, `08_unknown_recovery.md`. Toate actiunile de mai jos: $0.

Punct de plecare: 300 nominale (12,0%) + 359 generice verificate (14,4%) = 659 contacte sigure.

## Actiuni ordonate dupa castig estimat / efort

| # | Actiune | Castig estimat | Efort | Cine o poate face |
|---|---|---|---|---|
| 1 | **Retry Reoon pe "unknown"** — Reoon REDA creditele pentru unknown (politica oficiala), deci re-verificarea e aproape gratuita; 10–40% din unknowns se rezolva la retry (greylisting) | **+50–150 contacte** (nominale si generice) | Zero — rulat automat | **IN CURS (pipeline)** |
| 2 | **BounceBan free-forever pe segmentul Catch-all** — verificari single gratuite nelimitate la specialistul catch-all (94,6% acuratete la audit independent); toate cele 317 adrese-candidat se pot valida manual la $0. Toate cele 311 domenii catch-all sunt pe hosting clasic .ro (nu M365/Google — verificat MX local), deci BounceBan e singura cale gratuita | **+100–200 nominale** | ~2–4h munca manuala (UI, una cate una) | Client / operator uman (necesita cont) |
| 3 | **Waterfall pe free tiers de findere** — ~850 credite gratuite luna 1 (Anymail Finder 100, Dropcontact 50, Prospeo 75/luna, GetProspect 50, Snov 50 s.a.; majoritatea taxeaza doar rezultatele gasite) pe cele ~800 firme cu domeniu fara nominala; benchmarkurile 2026 dau 25–45% pe SMB-uri europene | **+200–350 nominale** (necesita re-verificare Reoon la primire) | Cateva ore (signup-uri; unele cer card/email de firma) | Client (conturi) + pipeline (rulare) |
| 4 | **Descoperire domenii gratuita** pentru cele 1.390 firme fara site: Google Programmable Search (100 interogari/zi gratuit → 14 zile pentru tot lotul), Brave Search API (~1.000/luna), RoTLD whois pentru re-validarea candidatelor respinse | **+350–700 domenii noi** → dupa re-rulare pipeline: **+40–120 nominale** indirecte | Mediu (chei API gratuite, script exista) | Client (chei) + pipeline |
| 5 | **Tipar confirmat empiric pe catch-all** — 13 firme unde o adresa reala prenume.nume@ e publicata pe acelasi domeniu catch-all (`work/14_catchall_tipar_confirmat.csv`) → adresa administratorului cu incredere ridicata, de trimis prioritar la BounceBan | inclus in #2 | Gata calculat | — |

Ce NU merge (verificat live, ca sa nu se piarda timp): directoarele romanesti nu dau site/email gratuit la scara (listafirme = paywall + blocare IP datacenter; topfirme fara contacte; cylex/infobel blocheaza botii); niciun set de date ANAF/ONRC/data.gov.ro nu contine email/site; Google Places interzice prin ToS stocarea datelor in baza livrata clientului; Bing API a murit (aug 2025); catchall.io nu mai exista.

## Proiectia daca se executa tot planul

| Scenariu | Nominale | Contacte sigure total |
|---|---|---|
| Acum | 300 (12,0%) | 659 (26,4%) |
| + retry unknown (in curs) | ~330–400 | ~750–850 |
| + BounceBan catch-all | ~430–600 | ~850–1.050 |
| + findere free tiers | ~630–950 | ~1.050–1.400 |
| + domenii noi re-rulate | ~670–1.070 | **~1.100–1.500 (44–60%)** |

Nota de onestitate: intervalele largi reflecta incertitudinea benchmarkurilor; chiar si scenariul maxim ramane sub tinta contractuala de 50–70% NOMINALE pe total — dar "contacte verificate total" poate atinge 44–60%, inca un argument pentru re-ancorarea metricii pe definitia "contact verificat".

## Reguli pastrate

Orice adresa noua (findere, BounceBan "valid", domenii noi) trece OBLIGATORIU prin
verificarea Reoon inainte de a intra in output (regula 2). Sursa fiecarei adrese
ramane in Observatii (GDPR/trasabilitate). Creditele Reoon ramase + refundurile
pe unknown acopera lejer re-verificarile.
