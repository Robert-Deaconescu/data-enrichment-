# 07 — Findere de e-mail comerciale: tiere gratuite (cercetare LIVE, 26 iulie 2026)

Scop: pentru ~800 de firme cu domeniu propriu validat si numele administratorului
cunoscut (~93%), cat putem stoarce din tierele gratuite ale finderelor comerciale,
la cost $0. Toate cifrele verificate LIVE pe paginile de pricing acolo unde a fost
posibil; unde pagina nu a putut fi citita direct (JS-only sau 403), am folosit
surse secundare recente si am marcat **[neverificat direct]**.

## 1. Tabel comparativ — tiere gratuite (iulie 2026)

| Tool | Credite gratuite | E-mail corporate la signup? | Taxeaza catch-all / negasit? | API pe free? | Nume+domeniu? | Sursa |
|---|---|---|---|---|---|---|
| **Prospeo** | **75/luna** + 100 credite extensie, fara card **[neverificat direct — pagina de pricing e JS-only; confirmat din 2 surse secundare 2026]** | nespecificat | nu — doar rezultate valide consuma credit | da (toate planurile, cf. sursa secundara) | DA | https://prospeo.io/pricing (gol la fetch); https://coldiq.com/blog/prospeo-pricing |
| **Hunter.io** | 25 cautari + 50 verificari/luna (afisat ca "50 credits/mo" pe pagina) | istoric DA (fara gmail); surse mai noi (mai 2026) spun ca gmail e acceptat — de testat | nespecificat pe pagina **[neverificat]** | pagina indica API doar pe planuri platite | DA (Email Finder) | https://hunter.io/pricing |
| **Snov.io** | 50 credite / 30 zile (trial reinnoibil) | nespecificat (gmail acceptat in practica) | nespecificat **[neverificat]** | NU (API/webhooks blocate pe trial) | DA (Email Search) | https://snov.io/pricing |
| **Apollo.io** | ~100 credite e-mail/luna pe cont gmail (fair-use); tierul free a fost taiat de la 10.000 la 100/luna la restructurarea din finalul lui 2025 **[neverificat direct — pagina nu afiseaza cifra]** | free = doar Gmail (Microsoft/altele cer plan platit) | n/a | NU (API doar pe Custom) | DA (People Search + enrichment, doar din UI) | https://www.apollo.io/pricing ; https://phantombuster.com/blog/ai-automation/apollo-pricing/ |
| **Skrapp** | 50 credite one-time (fara reinnoire lunara) | nespecificat | ATENTIE: taxeaza Valid **si Catch-all**; Invalid/Unknown nu se taxeaza | NU (API doar Enterprise) | DA ("name and company") | https://skrapp.io/pricing |
| **Icypeas** | 50 credite la signup (promo one-time) | nespecificat | nespecificat **[neverificat]** | pagina afirma API "in toate tierurile" | DA | https://www.icypeas.com/pricing |
| **Anymail Finder** | 100 credite trial / 14 zile — **cere card** (verificat, nu debitat) | nu | NU — "if a search doesn't return a verified email, it's free"; catch-all verificat suplimentar inainte de a fi taxat | creditele de trial merg si pe API/bulk | DA ("name and domain or company name", 1 credit) | https://anymailfinder.com/pricing |
| **Findymail** | 10 credite one-time, fara card | nespecificat | NU — doar rezultate gasite/functionale | nemarcat pe free **[neverificat]** | DA (si bulk) | https://www.findymail.com/pricing/ |
| **Dropcontact** | 50 credite one-time | **DA — e-mail profesional obligatoriu** | NU — negasitele se re-crediteaza; verificare catch-all inclusa | DA (API inclus si pe free) | DA (nume+prenume+site) | https://www.dropcontact.com/pricing |
| **VoilaNorbert** | 50 credite one-time la creare cont | nespecificat | NU — "count only successful email founds" | nu pe free (Bulk+API doar pe planuri platite) | DA | https://www.voilanorbert.com/pricing |
| **Tomba.io** | 25 cautari/luna, fara card | nespecificat | nespecificat **[neverificat]** | nespecificat pe free **[neverificat]** | DA | https://tomba.io/pricing |
| **Kaspr** | 15 credite e-mail B2B + 5 telefon + 5 direct email /luna | nespecificat | n/a | NU | **NU** — practic doar extensie Chrome pe profiluri LinkedIn | https://www.kaspr.io/pricing |
| **GetProspect** | 50 e-mailuri valide + 100 verificari/luna, permanent **[neverificat direct — pagina a dat 403; confirmat din 3 surse 2026]** | nu | catch-all ("accept-all") NElimitate, nu consuma din cele 50 valide | nespecificat pe free **[neverificat]** | DA | https://getprospect.com/pricing (403); https://getprospect.com/ ; https://getpulsesignal.com/pricing/getprospect |
| **Wiza** | 20 e-mailuri valide + 5 telefoane one-time | nespecificat | NU — plateste doar valide | NU (API doar Team) | partial — orientat LinkedIn/Sales Nav | https://wiza.co/pricing |
| **Muraena** | 50 credite e-mail/luna | nespecificat | nespecificat | NU (API doar Business) | NU chiar — e cautare in baza proprie (AI search), nu finder nume+domeniu; acoperire Europa de Est incerta | https://muraena.ai/pricing |
| **Enrow** (nou, FR) | 50 credite/luna, fara card (o sursa: 50 e-mailuri valide + 200 verificari/luna) | nespecificat | NU — taxeaza doar date verificate; verificare catch-all inclusa | nemarcat pe free **[neverificat]** | DA | https://enrow.io/pricing ; https://syncgtm.com/blog/enrow-review |
| **LeadMagic** (nou) | 100 credite trial, fara card | nespecificat | NU — taxeaza doar valide | DA (tool API-first) **[neverificat pe trial]** | DA | https://leadmagic.io ; https://maildoso.ai/blog/catalog/data-enrichment/leadmagic |
| **BetterContact** (waterfall) | trial gratuit (numar credite neafisat) **[neverificat]** | nespecificat | NU — taxeaza doar valide | — | DA | https://g2.com/compare/bettercontact-vs-fullenrich |
| **FullEnrich** (waterfall) | trial gratuit mic; fara free tier real (de la $59/luna) | nespecificat | — | — | DA | https://derrick-app.com/tools/fullenrich-review |

Nota importanta: la toolurile care **taxeaza doar rezultatele valide** (Anymail
Finder, Prospeo, Dropcontact, VoilaNorbert, Findymail, Enrow, Wiza, GetProspect),
un credit = un e-mail GASIT, nu o incercare. La un hit-rate realist de 25-40% pe
firme romanesti mici, 100 de credite acopera de fapt 250-400 de incercari.

## 2. Cine functioneaza pe firme mici europene / romanesti?

Doua benchmarkuri mari recente (ambele de la vendori, deci cu bias, dar cu
metodologie publicata):

**Dropcontact — "Email Finder Benchmark 2025", 20.000 contacte reale, din care
9.700 europene** (https://www.dropcontact.com/email-finder-benchmark):
- Rata efectiva de imbogatire (e-mailuri reale, testate prin trimitere):
  Dropcontact 54,9% (bounce 0,9%), Enrow 40,9%, Findymail 39,9% (bounce 1,1%),
  Icypeas 31,6%, FullEnrich 48,3% dar bounce 3,6%.
- Codasi: FindThatLead 14,2%, LeadMagic 22,6%, GetProspect 26,1%.
- Constatare cheie: **ratele pe contacte europene sunt cu 5-10 puncte procentuale
  mai mici decat pe SUA** la aproape toate toolurile — acoperirea EU e mai slaba.

**Anymail Finder — "Email Finder Benchmark 2026", 5.000 decidenti (SUA/UK/FR/DE)**
(https://anymailfinder.com/email-finder-benchmark):
- Anymail Finder 86,4% acoperire verificata, 0,9% fals-pozitive; Icypeas ~49%
  acoperire dar bounce ~1,0%; Prospeo si Snov mult mai jos pe acest esantion.
- 36% din esantion erau domenii catch-all — relevant pentru Europa, unde
  catch-all e frecvent (si la firmele noastre .ro).

Alte semnale calitative (2025-2026):
- Toolurile **europene (FR)** — Dropcontact, Enrow, Icypeas, Findymail — sunt
  citate constant ca mai bune pe companii EU/GDPR decat bazele LinkedIn-centrice
  US (Apollo, Wiza, Kaspr, Muraena). Sursa: https://www.dropcontact.com/email-finder-benchmark ,
  https://derrick-app.com/en/email-finder-2025/
- Acoperirea pe **Europa de Est** e explicit mai slaba la furnizorii de baze de
  date; pentru Romania, finderele algoritmice (pattern + verificare SMTP:
  Dropcontact, Anymail Finder, Enrow, Icypeas) bat bazele statice.
  Sursa: https://www.saleshandy.com/blog/european-email-database/
- Kaspr/Wiza/Muraena depind de LinkedIn/baze proprii → slabe pentru IMM-uri
  romanesti fara prezenta LinkedIn; utile doar marginal la noi.
- Niciun benchmark gasit nu include explicit firme romanesti; pentru IMM-uri .ro
  asteptam hit-rate sub media EU din benchmarkuri (estimare: 20-40% per tool,
  mai mult cumulat in cascada).

## 3. Capacitate totala gratuita realista (o luna)

**Recurente lunare** (se reinnoiesc): Prospeo 75 + Apollo ~100 + GetProspect 50 +
Snov 50 + Enrow 50 + Muraena 50 (marginal) + Hunter 25 + Tomba 25 + Kaspr 15
(marginal) ≈ **440 credite/luna** (≈390 utilizabile pe nume+domeniu).

**One-time** (o singura data): Anymail Finder 100 (card!) + Dropcontact 50 +
Icypeas 50 + Skrapp 50 + VoilaNorbert 50 + Wiza 20 + Findymail 10 + LeadMagic
100 ≈ **430 credite one-time**.

**Total luna 1 ≈ 850-870 credite la $0** — nominal cat tot lotul de ~800 firme.
Dar pentru ca majoritatea toolurilor bune taxeaza doar e-mailurile GASITE,
numarul de **incercari** posibile e mult mai mare (usor 1.500+); limita practica
devine numarul de randuri, nu creditele. In luna 2 se reinnoiesc inca ~440.

## 4. Bulk/CSV gratuit pentru cateva sute de randuri

- **Anymail Finder**: bulk CSV disponibil in trial (creditele merg pe single,
  bulk si API) — cel mai potrivit pentru o trecere masiva; se opreste cand se
  consuma cele 100 de credite (adica ~100 gasite, deci posibil 250-400 randuri
  procesate). Cere card la trial.
- **Dropcontact**: procesare de fisiere inclusa + API pe free (50 credite,
  negasitele re-creditate).
- **Icypeas**: bulk prin fisier + integrare Make/n8n; API declarat pe toate
  tierurile.
- **Prospeo**: bulk + API pe toate planurile [neverificat direct pe free].
- **GetProspect / Snov / Hunter**: import CSV in UI, dar pe free volumele mici
  (25-50) fac bulk-ul irelevant; Snov blocheaza operatiile bulk pe trial.

## Plan de actiune gratuit (~800 nume+domeniu)

Ordinea de stivuire optima (criterii: acoperire EU, taxare doar-pe-valid,
volum liber, bulk disponibil):

1. **Anymail Finder (trial 100, bulk CSV)** — prima trecere pe TOT lotul de 800,
   in bulk, in fereastra de 14 zile. Taxeaza doar verificatele → asteptat
   150-300 randuri procesate pana la epuizarea celor 100 de credite, ~100
   e-mailuri verificate. Atentie: cere card; setati reminder de anulare.
2. **Dropcontact (50, API, re-creditare negasite)** — pe restul, incepand cu
   firmele cele mai valoroase: cel mai bun scor EU din benchmarkul pe 20k
   (54,9% real). Cere e-mail profesional la signup (avem domeniul Dezvolt AI).
3. **Prospeo (75/luna, API)** — a treia trecere pe rest; se reinnoieste lunar.
4. **Icypeas (50, bulk + Make/n8n)** — a patra trecere.
5. **Enrow (50/luna)** + **GetProspect (50/luna, catch-all gratuite)** +
   **Snov (50/luna, doar UI)** — impartite pe restul cozii.
6. **VoilaNorbert (50)**, **LeadMagic (100 trial)**, **Wiza (20)**,
   **Findymail (10)** — curatare finala pe cazurile ramase.
7. **Skrapp (50)** — ultimul, DOAR cu filtrare: taxeaza si catch-all, deci il
   folosim numai pe domenii care NU sunt catch-all (avem verdictele MX/Reoon).
8. **Hunter (25/luna) + Tomba (25/luna)** — rezerve; Apollo (~100/luna, doar UI,
   cont gmail) ca sursa suplimentara manuala daca mai raman goluri.
9. Tot ce iese, indiferent de tool, trece prin **verificarea Reoon existenta**
   inainte de a intra in output (regula proiectului: nimic neverificat).

**Randament asteptat**: benchmarkurile EU dau 30-55% per tool pe contacte
europene, cu -5..-10pp fata de SUA si probabil inca mai putin pe IMM-uri .ro
fara LinkedIn. In cascada (fiecare tool vede doar ce n-au gasit precedentele),
estimare realista pentru cele ~800 de firme: **200-350 de adrese nominale noi
verificate (25-45%) la cost $0** in luna 1, plus o coada de ~440 credite
reinnoite in luna 2 pentru inca 50-100 de adrese.

Riscuri: cifrele de free tier se schimba des (Apollo tocmai a taiat de la
10.000 la 100/luna); trialul Anymail Finder cere card; Skrapp taxeaza catch-all;
benchmarkurile citate apartin vendorilor (bias pro-domo) — tratati procentele ca
ordine de marime, nu ca garantii.

*Cercetare efectuata live la 26.07.2026. Surse per rand in tabel.*
