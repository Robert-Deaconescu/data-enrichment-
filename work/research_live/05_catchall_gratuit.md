# Recuperare adrese nominale de pe domenii catch-all - metode GRATUITE

Data cercetarii: 26 iulie 2026. Buget alocat pentru aceasta runda: 0 USD.
Segment tinta: 325 firme cu domeniu catch-all (SMTP accepta orice), din care
317 au un nume de decident cunoscut. Obiectiv: cate adrese nominale putem
CONFIRMA gratuit sau aproape gratuit.

Nota de incredere: fiecare afirmatie are URL sursa. Tot ce nu am putut confirma
live este marcat explicit `[neverificat]`.

---

## Intrebarea 1 - Free tiers / free trials la validatorii specializati pe catch-all

### BounceBan (bounceban.com) - CEA MAI IMPORTANTA descoperire
- Ofera **verificari single (una cate una) GRATUITE si NELIMITATE, "free forever"**,
  care NU consuma credite. Textul de pe site: "Unlimited single email verifications
  free forever" / "Single email verifications in Free Mode are free and won't cost
  your credits."
  Surse: https://bounceban.com/ , https://bounceban.com/pricing
- Tagline oficial pe Product Hunt: **"Free Email verification for accept-all
  (catch-all) domains"** - deci verificarea catch-all este exact ce ofera gratuit
  in modul single. Un review citat: "the free single email verification is also the
  most generous free service in the industry."
  Sursa: https://www.producthunt.com/products/bounceban
- Acuratete pe catch-all: firma sustine ca rezolva deliverabilitatea reala pentru
  **85-95%** din emailurile catch-all / greylisted / protejate SEG, si "97%+
  accuracy in real-time" pe toate tipurile.
  Sursa: https://orbisearch.com/blog/bounceban-vs-zerobounce
- Audit independent (OrbiSearch) pe 538 hard-bounce-uri reale: BounceBan a marcat
  corect **94,6%** ca "bad"; a lasat 5,4% ca "safe" care totusi au dat bounce. Deci
  eroare reziduala ~5% - acceptabila pentru tinta noastra de bounce < 2% daca
  pastram doar verdictele clare.
  Sursa: https://orbisearch.com/blog/bounceban-vs-zerobounce
- LIMITAREA free tier-ului: gratuit este DOAR single (interfata web, una cate una).
  **Bulk, API si Sync (CRM) necesita plan platit.** "Single email verifications are
  free forever; paid plans are required for bulk, API, and Sync features." API =
  planul Professional (~12 USD).
  Sursa: https://coldiq.com/tools/bounceban
- Card necesar la inregistrare pentru free single: NEconfirmat in surse.
  `[neverificat]` - de testat direct la signup.
- Plati (daca am vrea bulk candva): pornesc de la ~21,25 USD; credite de la ~34 USD
  / 10.000, cu -15% pe abonament lunar; 1 credit / verificare reusita, creditele nu
  expira. Sursa: https://bounceban.com/pricing , https://coldiq.com/tools/bounceban

Concluzie pentru cele 325: **teoretic putem verifica toate cele 325 adrese GRATUIT
prin BounceBan, introducandu-le una cate una in interfata single.** Costul e timpul
(manual sau semi-automatizat) si un posibil rate-limit / captcha pe UI-ul gratuit
`[neverificat]`. Aceasta este singura cale prin care intreg segmentul poate fi
validat catch-all pe 0 USD.

### Scrubby (scrubby.io) - specializat pe catch-all/risky, dar NU gratuit pentru volum
- Trial: **7 zile, 200 credite gratuite la inregistrare** (o alta sursa spune "100
  emails free / 200 free credits instantly").
  Surse: https://scrubby.io/pricing/ , https://prospeo.io/s/scrubby-pricing-reviews-pros-and-cons
- Cost credite: 0,008 USD/credit (PAYG). **Quick Verification = 1 credit/email;
  Deep Verification = 3 credite/email** (trimite email real si observa raspunsul
  24-72h). Plan minim: Starter 47 USD/luna (6.000 credite) sau 27 USD/luna in alt
  pachet catch-all. Sursa: https://scrubby.io/pricing/
- Acuratete revendicata pe catch-all: ~93%; "singurul verificator major care chiar
  testeaza adresele catch-all pentru deliverabilitate".
  Sursa: https://skrapp.io/blog/best-email-verifier/
- Aplicat la noi: cu 200 credite trial la Quick (1 cr) am acoperi ~200 din 325 adrese
  gratuit; cu Deep (3 cr) doar ~66. Deci **Scrubby acopera partial**, complementar
  cu BounceBan. Card la trial: `[neverificat]`.

### catchall.io - NU mai exista ca produs
- Domeniul catchall.io **este parcat / scos la vanzare pe GoDaddy** (redirect catre
  forsale.godaddy.com). Nu are legatura activa cu Scrubby si nu ofera nimic.
  Sursa (redirect observat live): https://forsale.godaddy.com/forsale/catchall.io

### Competitori / alternative cu free tier (relevante pentru catch-all)
- **ZeroBounce**: 100 validari gratuite/luna "forever", acuratete revendicata 99,6%.
  In iulie 2026 a lansat clasificare mai buna catch-all pentru M365 / Google
  Workspace / SEG (vezi Intrebarea 3). Surse:
  https://www.zerobounce.net/ , https://prospeo.io/s/catch-all-email-verification
- **Reoon Email Verifier** (deja folosit in proiect): **600 credite gratuite/luna**
  cu acces API complet pe free tier. Util pentru re-verificare, dar pe catch-all da
  in general "unknown/catch-all", nu verdict nominal.
  Sursa: https://hunter.io/email-verification-guide/best-email-verifiers/ (sectiunea free)
- **Prospeo**: 75 emailuri gratuite/luna, cu tratare catch-all.
  Sursa: https://prospeo.io/s/catch-all-email-verification
- **Bouncer**: 100 credite free. **Kickbox**: 100 free. **MailerCheck**: 200 free.
  **Hunter**: 50/luna. Toate au free tier mic, dar NU sunt specializate catch-all
  (dau "risky/unknown"). Sursa: https://www.usebouncer.com/email-verification-software-free/
- **Findymail**: trial 10 credite finder+verify; **Enrow**: 50 credite trial;
  **Icypeas**: email finder gratuit fara card, cu verificare catch-all pentru Google
  Workspace si M365. Surse:
  https://www.findymail.com/blog/best-email-finder-api/ ,
  https://www.icypeas.com/free-tools/email-finder

Total teoretic "gratuit" cumuland free tiers specializate (fara BounceBan single):
~200 (Scrubby trial Quick) + 100 (ZeroBounce) + 75 (Prospeo) + 100 (Bouncer) +
100 (Kickbox) = peste 500 credite, MAI MULT decat cele 325 necesare. In practica
insa multe dintre acestea returneaza "catch-all/unknown" fara verdict util, deci
BounceBan single ramane cea mai fiabila cale gratuita.

---

## Intrebarea 2 - Confirmarea intra-domeniu a pattern-ului (adresa publicata pe acelasi domeniu)

Ideea: daca gasim o adresa nominala reala publicata pe acelasi domeniu catch-all
(ex. `ion.popescu@firma.ro` pe pagina de contact), pattern-ul `prenume.nume` este
dovedit empiric pentru acel domeniu, deci putem genera cu incredere adresa
decidentului nostru dupa acelasi tipar.

Ce am putut confirma live:
- Comunitatea de verificare confirma principiul: **"Addresses that match patterns of
  known-good contacts are likely real."** Verificatoarele moderne (ex. Cleanlist)
  folosesc "pattern data, historical signals and confidence scoring" tocmai pentru
  ca pe catch-all un simplu ping SMTP este dovada slaba.
  Surse: https://www.cleanlist.ai/blog/2026-04-25-what-is-catch-all-email ,
  https://prospeo.io/s/catch-all-email-verification
- Pe catch-all, acceptul SMTP la RCPT TO este "weak evidence"; de aceea o adresa
  reala observata pe acelasi domeniu este un semnal mult mai puternic decat pingul.
  Sursa: https://anymailfinder.com/blog/what-is-a-catch-all-email-and-how-to-verify-it

Ce NU am gasit publicat:
- **Nu exista un studiu public cu procent de fiabilitate** pentru tehnica exacta
  "am gasit o adresa pe domeniu -> pattern confirmat". `[neverificat]` ca cifra.
  Rationamentul de industrie: fiabilitatea depinde de cat de consistent e pattern-ul
  in firma; pentru IMM-uri romanesti (1 domeniu, 1-2 pattern-uri) este de regula
  foarte inalta, dar pentru firme mari cu tipare mixte (ex. si `nume@`, si
  `n.nume@`) scade. Recomandare interna: tratam pattern-ul intra-domeniu ca
  incredere INALTA doar cand (a) adresa-sursa e nominala reala (nu generica de tip
  office@/contact@) si (b) numele decidentului nostru se preteaza fara ambiguitate
  la acelasi tipar (probleme la diacritice, nume compuse, prescurtari).

Concluzie: metoda este solida conceptual si sustinuta de practica industriei, DAR
fara cifra publica de fiabilitate. O folosim ca **semnal de incredere care ridica
prioritatea**, nu ca inlocuitor complet al unei verificari - de aceea o combinam cu
un verdict BounceBan single (Intrebarea 1) inainte de a intra in output.

---

## Intrebarea 3 - Trucuri tehnice gratuite pentru domenii catch-all

### Detectarea hosting-ului Google Workspace / Microsoft 365 prin MX (GRATUIT)
- Multe domenii "par" catch-all doar din cauza platformei. **M365 apare frecvent ca
  catch-all din cauza rutarii la nivel de tenant, nu pentru ca adminul a activat un
  catch-all.** Verificatoarele moderne recunosc "M365 platform signatures" inainte de
  probing si pot clasifica adresa direct valid/invalid.
  Sursa: https://prospeo.io/s/catch-all-email-verification
- Truc gratuit propriu: interogam MX-ul domeniului (`dig MX domeniu.ro` /
  Google Admin Toolbox / MXToolbox). Daca MX arata spre `google.com` / `googlemail.com`
  (Workspace) sau `*.mail.protection.outlook.com` (M365), stim ca e o platforma pe
  care unele verificatoare o pot rezolva DESPITE catch-all.
  Surse: https://www.smartlead.ai/blog/a-complete-guide-for-google-workspace-mx-records-in-2026 ,
  https://toolbox.googleapps.com/apps/main/
- **ZeroBounce (iulie 2026)** a imbunatatit clasificarea catch-all exact pentru M365,
  Google Workspace si SEG: in teste interne numarul de adrese M365 returnate ca
  catch-all a scazut cu **peste 99,98%** - practic acum da verdict valid/invalid
  direct, fara asteptarea de pana la 48h. Disponibil "to all customers" (nu se
  precizeaza clar daca si free tier `[neverificat]`).
  Surse: https://www.manilatimes.net/2026/07/08/tmt-newswire/pr-newswire/zerobounce-improves-catch-all-email-validation-for-microsoft-365-google-workspace-and-more/2380917 ,
  https://www.zerobounce.net/blog/email-resources/email-verification/catch-all-domains
- Actiune la noi: segmentam cele 325 dupa MX. Sub-segmentul Google Workspace / M365
  este candidatul cel mai bun sa fie rezolvat gratuit de BounceBan single + cele 100
  credite ZeroBounce.

### Cautare web a adresei exacte intre ghilimele (OSINT gratuit)
- Cautarea `"prenume.nume@firma.ro"` intre ghilimele in Google/Bing forteaza motorul
  sa returneze paginile unde apare exact acel string (forumuri, PDF-uri, directoare,
  semnaturi) - dovada ca adresa exista si e folosita.
  Surse: https://www.osint.industries/post/inbox-intel-how-to-use-emails-for-osint ,
  https://nixintel.info/osint/12-osint-resources-for-e-mail-addresses/
- Complementar: **Epieos** (epieos.com) automatizeaza cautarea de urme ale unei
  adrese fara cont Google. Util pentru confirmare, nu pentru generare in masa.
  Sursa: https://usersearch.com/resources/intel-hub/blog/reverse-email-osint-guide/
- Alte semnale gratuite: functia de "password reset" pe Google/Facebook confirma
  daca o adresa e inregistrata, fara a alerta userul (a se folosi etic si cu masura).
  Sursa: https://medium.com/@R00tendo/email-osint-techniques-c1e82efb253d
- Semnale LinkedIn / pagina firmei: pattern-ul deducibil din alti angajati publici
  (validare incrucisata cu Intrebarea 2).

### De retinut
- Niciun verificator nu e 100% pe catch-all - "the protocol makes it impossible";
  acuratetea generala se plafoneaza in jur de ~70%, iar pe catch-all pur este si mai
  mica. De aceea combinam mai multe semnale gratuite (MX + BounceBan + OSINT +
  pattern intra-domeniu) pentru a atinge incredere suficienta.
  Sursa: https://prospeo.io/s/catch-all-email-verification

---

## Intrebarea 4 - Semnale de deliverabilitate gratuite (pilot batch cu inbox incalzit)

Da, trimiterea catre catch-all dintr-un inbox incalzit si procesarea bounce-urilor
ramane fallback-ul gratuit standard in 2026, cu conditii clare:

- **Segmentare separata obligatorie**: catch-all-urile se trimit intr-un batch
  propriu, la volum mic, monitorizat izolat. "Segment catch-alls into their own
  batch, send to them carefully and at lower volume, and watch their bounce behavior
  before trusting them at scale."
  Sursa: https://litemail.ai/blog/cold-email-inbox-bounce-rate-thresholds-2026
- **Prag de suprimare**: daca bounce-ul pe segmentul catch-all depaseste **3%**,
  suprimi tot segmentul.
  Sursa: https://litemail.ai/blog/cold-email-inbox-bounce-rate-thresholds-2026
- **Praguri de sanatate inbox (2026)**: bounce/inbox prag de pericol **2%**;
  spam complaint/domeniu **0,08%**; DKIM/SPF/DMARC pass **100%**; plafon volum
  **~50 emailuri/zi/inbox**; Google Postmaster reputatie "Good/High".
  Sursa: https://litemail.ai/blog/cold-email-inbox-health-metrics-2026
- **Inbox incalzit vs proaspat**: inbox-urile pre-incalzite au declansat alerte de
  bounce de ~3x mai rar decat cele proaspete in aceleasi campanii. Rampa recomandata:
  S1 30-50/zi, S2 50-80, S3 80-120, S4 120-150, cu bounce mentinut sub 3%.
  Sursa: https://litemail.ai/blog/cold-email-inbox-bounce-rate-thresholds-2026
- **Fereastra de monitorizare**: suprima orice adresa care ramane "cold" (fara
  engagement) 30-60 zile, ca sa nu strici semnalele la Gmail/Yahoo; re-verificare
  trimestriala.
  Sursa: https://www.allegrow.co/knowledge-base/catch-all-email-verification-guide-for-b2b
- Marimea exacta a batch-ului pilot NU e standardizata public in surse
  `[neverificat]`; comunitatea o lasa la latitudinea practicianului, cu regula ferma
  a pragului de 3% bounce pe segment. Practic pentru noi: pilot de ~30-50 adrese
  catch-all/inbox/zi, fereastra de 48-72h pentru bounce-uri hard inainte de a scala.
  (interpretare interna bazata pe rampa si plafonul de 50/zi de mai sus)

Atentie contractuala: proiectul cere ca NICIO adresa neverificata sa nu intre in
output (tinta bounce < 2%). Deci pilot-send-ul NU e o metoda de a "baga" adrese in
livrabil, ci un mecanism gratuit de a CONFIRMA (prin lipsa bounce-ului) adrese
pentru care avem deja semnal puternic. Adresele confirmate astfel trec in output;
cele care dau bounce raman pe generic / Status Exclus.

---

## Plan de actiune gratuit (ordonat dupa yield asteptat pentru cele 325 firme)

**Pas 0 - Pregatire (gratis).** Segmenteaza cele 325 dupa MX (Google Workspace / M365 /
altele). Sub-segmentul Workspace+M365 e cel mai probabil rezolvabil gratuit direct.
Genereaza pentru cele 317 cu nume adresele-candidat dupa pattern-ul dominant
(prenume.nume@, nume@, p.nume@) cu unidecode pentru diacritice.

**Pas 1 - BounceBan single, gratuit (YIELD CEL MAI MARE).** Verifica una cate una
toate cele ~317 adrese-candidat in modul single gratuit BounceBan (specializat
catch-all, 85-95% rezolvare, ~94,6% acuratete la audit independent). Pastreaza in
output DOAR verdictele clare "deliverable/safe". Aceasta e singura cale care poate
acoperi intreg segmentul pe 0 USD. Risc: rate-limit/captcha pe UI si card la signup -
de testat. (surse: bounceban.com, producthunt, orbisearch)

**Pas 2 - Confirmare intra-domeniu + OSINT (gratis, ridica increderea).** Pentru
domeniile unde am gasit o adresa nominala reala publicata, considera pattern-ul
dovedit si prioritizeaza. Pentru restul, cautare Google/Bing a adresei exacte intre
ghilimele + Epieos ca dovada de existenta. Combina cu semnalul BounceBan din Pas 1.

**Pas 3 - Free tiers complementare (gratis, pentru ce a ramas "unknown").** Ce nu a
primit verdict clar la BounceBan trece prin: Scrubby trial (200 credite Quick ~=200
adrese) pentru catch-all real, apoi ZeroBounce 100/luna si Prospeo 75/luna pentru
M365/Workspace. Cumulat depasesc 325, dar multe dau "unknown" - de aceea sunt Pas 3,
nu Pas 1.

**Pas 4 - Pilot send din inbox incalzit (gratis, confirmare finala prin bounce).**
Doar pentru adresele cu semnal puternic ramase incerte: batch separat de ~30-50/zi
dintr-un inbox incalzit, fereastra 48-72h, suprimare segment daca bounce > 3%, plafon
2% pe inbox. Adresele fara bounce -> output; cele cu bounce -> generic/Exclus.

Estimare realista: Pasii 1-2 ar trebui sa confirme gratuit majoritatea celor 317 cu
nume; Pasii 3-4 recupereaza marginal. `[neverificat]` procentul exact pana nu rulam
Pas 1 pe date reale.
