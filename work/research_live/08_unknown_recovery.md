# 08 — Recuperarea rezultatelor "unknown" din verificarea Reoon

Data cercetarii: 26 iulie 2026 (research live, surse verificate la zi).
Context local: `work/06_verificari.csv` contine **3.445 unknown** (in fisierul curent; cifra
de 3.458 din discutie include probabil si backup-ul/rulari partiale), distribuite pe
**655 firme**, din care **590 firme nu au niciun rezultat "safe"** (3.263 adrese unknown).
Credite Reoon ramase (estimare interna): ~1.634 — dar vezi §1.1, cifra reala poate fi mai mare.

---

## 1. Specificul Reoon

### 1.1 Reoon NU taxeaza creditele pentru rezultate "unknown"
- Politica oficiala: "If an email returns an Unknown status, the credit is automatically
  refunded" — creditul este returnat automat.
  Sursa: https://www.reoon.com/articles/quick-mode-vs-power-mode/
- Confirmat si in articolul despre statusuri: pentru unknown "Your credits are
  automatically refunded for such results."
  Sursa: https://www.reoon.com/articles/meaning-of-different-email-verification-statuses/
- **Implicatie practica majora #1:** fisierul nostru intern (`06_verificari.csv`) a
  contabilizat 1 credit pentru fiecare din cele 3.445 unknown-uri. Daca Reoon a aplicat
  refund-ul automat, soldul real din dashboard ar trebui sa fie cu pana la ~3.445 credite
  mai mare decat estimarea noastra de 1.634. **De verificat soldul real in dashboard-ul
  emailverifier.reoon.com inainte de orice plan.** [neverificat — necesita login]
- **Implicatie practica majora #2:** re-verificarea unknown-urilor chiar in Reoon este
  aproape gratuita: platim credit doar pentru cele care se rezolva (safe/invalid/catch-all),
  iar cele care raman unknown sunt din nou refundate.

### 1.2 Reoon recomanda explicit re-verificarea unknown-urilor
- "Unknown doesn't mean bad — it means 'not confirmed.' You can try re-verifying Unknown
  emails after 15–30 minutes." (recomandare oficiala Reoon)
  Sursa: https://www.reoon.com/articles/quick-mode-vs-power-mode/
- Definitia oficiala a unknown: serverul destinatie nu a raspuns la momentul verificarii
  sau nu s-au obtinut suficiente semnale pentru un verdict cu incredere suficienta.
  Sursa: https://www.reoon.com/articles/meaning-of-different-email-verification-statuses/
- Reoon afirma ca "in many cases, you'll get more successfully verified results on the
  second attempt" (citat aparut in rezultatele de cautare pe paginile Reoon; formularea
  exacta pe pagina — [neverificat]).

### 1.3 Power mode si greylisting
- Power mode = verificare "in depth", identica cu verificarea din dashboard, poate dura
  de la cateva secunde la peste un minut per adresa, in functie de serverul destinatie.
  Sursa: https://www.reoon.com/articles/quick-mode-vs-power-mode/
- Articolul oficial Quick vs Power NU mentioneaza explicit retry pe greylisting.
  Afirmatia ca Reoon "includes greylisting retry logic making multiple SMTP connection
  attempts" apare in surse terte/agregate, nu intr-o pagina oficiala Reoon pe care am
  putut-o confirma. [neverificat pe pagina oficiala]
- Concluzie: chiar daca power mode face retry-uri scurte, un volum de 3.445 unknown din
  8.366 verificari (41%) sugereaza ca fereastra de retry din timpul rularii nu acopera
  greylisting-ul tipic; re-verificarea la distanta de ore/zile ramane utila.

### 1.4 Free tier Reoon (bonus)
- Cont gratuit Reoon: 20 credite/zi regenerabile + ~100 credite instant la inregistrare
  (fara card). Sursa: https://www.reoon.com/email-verifier/ si
  https://www.saasworthy.com/product/reoon-email-verifier/pricing

---

## 2. Practica din industrie: cate unknown-uri devin valide la retry

- **Greylisting = cauza principala a unknown-urilor pe liste B2B.** "You might have
  hundreds or thousands of genuinely valid email addresses in your list that return
  'unknown' purely because their mail servers use greylisting."
  Sursa: https://bulkemailchecker.com/blog/email-greylisting-verification-unknown-results/
- **Durata tipica a greylisting-ului este scurta:** 5–30 minute, implicit ~15 minute la
  majoritatea implementarilor. Recomandarea articolului: asteapta 30–60 de minute si
  re-verifica. Sursa: https://bulkemailchecker.com/blog/email-greylisting-verification-unknown-results/
- **"Retry almost always resolves greylisted results to passed"** — recomandarea corecta
  este acceptarea provizorie + re-verificare dupa 5–15 minute, nu respingerea adresei.
  Sursa: https://emailverifierapi.com/blog/greylisting-email-verification-unknown-results/
- ZeroBounce si Clearout documenteaza tehnologii anti-greylisting dedicate (retry
  automat in fereastra de acceptare).
  Surse: https://www.zerobounce.net/anti-greylisting ,
  https://clearout.io/blog/greylisting-and-anti-greylisting-technology/
- **Procent publicat de recuperare:** Clearout afirma ca un verificator dedicat de
  catch-all poate rezolva **30–40% din adresele "risky"**. Sursa (via cautare, pagina
  exacta Clearout): https://clearout.io/blog/greylisting-and-anti-greylisting-technology/ [neverificat exact pe pagina]
- Novoslo (ghid tools cold email 2026): pe o lista unde prima trecere lasa 5.000 de
  catch-all/risky, o a doua trecere cu un tool specializat "often recovers 1,000 to
  2,000 usable leads" (adica **20–40% recuperare**), iar cine sterge risky-urile fara a
  doua verificare arunca "20% to 30% of your leads, many of which are perfectly sendable".
  Sursa: https://www.novoslo.com/blog/best-email-verification-tools-for-cold-email
- **Nu exista un studiu publicat cu procent exact pentru fereastra 24–72h** — sursele
  converg pe retry la minute/ore, plus re-verificare dupa cateva zile pentru esecuri
  temporare de server ("for soft bounces or 'unknown' results, consider retrying
  verification after a few days"). Consens de interval: **10–40% din unknown-uri se
  rezolva la retry**, cu partea de greylisting rezolvandu-se aproape integral.
  [interval estimat din surse multiple, nu o cifra unica verificata]

---

## 3. Capacitate gratuita de cross-check (alte verificatoare, iulie 2026)

| Serviciu | Credite gratuite | Tip | API gratuit? | Sursa |
|---|---|---|---|---|
| **MillionVerifier** | 100 la inregistrare ("No credit card required · 100 free credits") | o singura data | da (nu taxeaza risky la API) | https://www.millionverifier.com/ |
| — politica MV | unknown + catch-all NU consuma credite (refund automat la fisiere; la API nu se scad deloc) | permanent | — | https://help.millionverifier.com/payments-credits/refund-for-risky-emails |
| **MyEmailVerifier** | **100/zi, se reseteaza zilnic** (necesita verificare telefon); credite platite nu expira | zilnic | da (JSON, detectie greylist) | https://myemailverifier.com/ , https://github.com/pat-myemailverifier/myemailverifier-api |
| **Verifalia** | **25/zi permanent** (reset la miezul noptii GMT, nu se cumuleaza) | zilnic | da, inclus pe planul Free | https://verifalia.com/help/billing-pricing/how-do-daily-free-credits-work , https://verifalia.com/pricing |
| **ZeroBounce** | 100/luna (reset lunar; statutul Freemium se pierde la prima achizitie) | lunar | da | https://www.zerobounce.net/docs/getting-started/freemium-terms-and-conditions |
| **VerifyRight** | 200/luna | lunar | da ("100% Free API Access") | https://verifyright.io/en [cifra 200/luna via https://prospeo.io/s/free-email-verification-api — neverificat pe site-ul propriu] |
| **Emailable** | 250 la inregistrare, fara card | o singura data | da | https://emailable.com/pricing/ , https://prospeo.io/s/emailable-pricing-reviews-pros-and-cons |
| **Bouncer (usebouncer)** | 100 la inregistrare, fara card | o singura data | da | https://www.usebouncer.com/free-email-checker/ |
| **CaptainVerify** | 100 la deschiderea contului (activare din butonul portocaliu din emailul de bun venit) | o singura data | da | https://captainverify.com/faq.html |
| **EmailListVerify** | 100 la inregistrare | o singura data | da | https://emaillistverify.com/pricing |
| **Mails.so** | 75/luna (+100 credite extensie Chrome) | lunar | da | https://mails.so/ [detaliu 75/luna via https://prospeo.io/s/mailsso-pricing-reviews-pros-and-cons — neverificat pe site-ul propriu, pagina /pricing a dat 404] |

**Total capacitate gratuita realista (fara costuri):**
- One-time: MillionVerifier 100 + Emailable 250 + Bouncer 100 + CaptainVerify 100 +
  EmailListVerify 100 = **~650 verificari**.
- Recurent lunar: ZeroBounce 100 + VerifyRight ~200 + Mails.so 75 = **~375/luna**.
- Recurent zilnic: MyEmailVerifier 100/zi (~3.000/luna) + Verifalia 25/zi (~750/luna) =
  **~125/zi**.
- **Cel mai valoros pentru volumul nostru: MyEmailVerifier (100/zi prin API) si
  MillionVerifier (risky nu consuma credite → cele 100 de credite se refolosesc in
  bucle pentru batch-uri in care majoritatea ies unknown/catch-all).**

Nota MillionVerifier: la upload de fisier creditele se retin intai pentru toate
adresele unice si se returneaza dupa finalizare pentru risky — deci cu 100 credite
gratuite se pot procesa maximum ~100 adrese per batch, iterativ.
Sursa: https://help.millionverifier.com/payments-credits/refund-for-risky-emails

---

## 4. Consensul multi-verificator (2-din-3) — este o practica solida?

- **Da, este practica documentata in industrie:**
  - Novoslo recomanda explicit pentru liste valoroase "double verification, meaning two
    different tools, and trusting the consensus"; regula descrisa: daca 2 verificatoare
    independente claseaza adresa ca deliverable → pastreaza; daca oricare o marcheaza
    risky → excludere din batch.
    Sursa: https://www.novoslo.com/blog/best-email-verification-tools-for-cold-email
  - **Benchmark-ul Anymail Finder 2026** (5.000 contacte B2B, 15 tooluri) foloseste exact
    aceasta metodologie ca "ground truth": fiecare email returnat a fost verificat cu
    **3 servicii independente** (BounceBan, ZeroBounce, MillionVerifier), set de date
    anonimizat publicat. Rezultat de referinta: acoperire 86,4% la **0,9% false-positive
    rate** — adica un pipeline validat prin consens multi-verificator tine bounce-ul
    sub 1%. Sursa: https://anymailfinder.com/email-finder-benchmark
  - Fluxul "pasa generala → specialist catch-all pentru risky" este recomandat si de
    ghidurile de cold outreach 2026.
    Surse: https://zapmail.ai/blog/ultimate-guide-email-verification-cold-outreach/ ,
    https://prospeo.io/s/cold-email-verification
- **Pragul de siguranta din industrie:** bounce total <2%, hard bounce <1%.
  Surse: https://prospeo.io/s/cold-email-bounce-rate ,
  https://hunter.io/email-verification-guide/email-verification-best-practices
- **Nuanta importanta:** regula sanatoasa nu este "2 din 3 spun valid → trimit orice",
  ci varianta conservatoare: **acceptam doar daca cel putin 2 verificatoare independente
  spun explicit valid/deliverable SI niciunul nu spune invalid**. Un rezultat
  "catch-all/accept-all" la oricare dintre ele NU conteaza ca "valid" — raman pe
  circuitul separat de catch-all (pasul 09 din pipeline). O regula "2-din-3" formal
  denumita astfel nu am gasit-o ca standard publicat [neverificat ca termen standard],
  dar echivalentul ei functional este exact metodologia Anymail Finder si recomandarea
  Novoslo de mai sus.

---

## Plan de actiune gratuit (pentru cele 3.445 unknown)

**Pasul 0 — azi (5 min):** Verifica soldul real de credite in dashboard-ul Reoon.
Conform politicii oficiale de refund pe unknown (§1.1), soldul ar trebui sa fie
semnificativ peste estimarea interna de 1.634. Corecteaza `stats.md` si
`10_necesar_credite.md` cu cifra reala.

**Pasul 1 — prioritizare (azi):** Construieste coada de re-verificare in ordinea:
1. **Tipare nominale la cele 590 de firme fara niciun rezultat "safe"** (3.263 adrese) —
   aici o recuperare inseamna direct o firma noua cu adresa nominala (impact maxim pe
   tinta contractuala de 50–70%). In interiorul acestui set, incepe cu tiparul cel mai
   probabil per domeniu (prenume.nume@ / prenume@), nu toate cele ~5-6 variante — daca
   tiparul principal iese valid, restul variantelor nu mai trebuie verificate.
2. Unknown-urile de la firme care au deja un "safe" (182 adrese) — prioritate minima,
   doar daca raman credite.

**Pasul 2 — re-verificare in Reoon, la 24–72h de la prima rulare (cost net ~0 pe
esecuri):** Re-ruleaza in power mode intreaga coada prioritara. Platim doar pentru
adresele care se rezolva (exact cele pe care le vrem), iar cele ramase unknown sunt
refundate din nou. Asteptare recomandata de Reoon: minim 15–30 min; noi rulam la 24h+
pentru a acoperi si greylisting agresiv/timeouts de server. Estimare de recuperare pe
baza surselor: 10–40% din unknown-uri se rezolva (o parte ca invalid — si asta e
informatie utila).

**Pasul 3 — cross-check gratuit pentru unknown-urile persistente (ziua 2+):**
Ordine tooluri, toate prin API unde exista:
1. **MyEmailVerifier** — 100/zi gratuit, are detectie greylist explicita; ruleaza zilnic
   batch-uri din coada prioritara (~700/saptamana).
2. **MillionVerifier** — cont gratuit 100 credite; risky (unknown+catch-all) nu consuma
   credite, deci creditele se refolosesc; ruleaza batch-uri de ≤100.
3. **Emailable (250) + Bouncer (100) + CaptainVerify (100) + EmailListVerify (100)** —
   capacitate one-time (~550) pentru subsetul cu cea mai mare valoare (decidenti la
   firme mari, fara alternativa generica valida).
4. **Verifalia (25/zi) + ZeroBounce (100/luna) + VerifyRight (~200/luna)** — rezervate
   ca "al treilea vot" pentru adresele aflate in dezacord intre Reoon si primul
   cross-check.

**Pasul 4 — regula de decizie (tinta bounce <2%):**
- Reoon safe (la re-verificare) → intra in output ca verificat (regula existenta).
- Reoon unknown persistent + **2 verificatoare independente "valid/deliverable"** si
  **zero verdicte "invalid"** → acceptat, marcat in coloana de sursa
  "consens 2-verificatoare" pentru trasabilitate.
- Orice verdict "invalid" la oricare tool → exclus definitiv.
- "Catch-all" la oricare tool → NU conteaza ca valid; ramane pe fluxul separat catch-all.
- Unknown persistent peste tot → ramane pe adresa generica a firmei (conform contract).

**Cost total plan: 0 lei** (creditele Reoon consumate doar pe rezolvari sunt oricum in
soldul existent; toate cross-check-urile sunt pe tier-uri gratuite). Capacitate gratuita
totala in ~30 zile: ~650 one-time + ~375/luna + ~125/zi ≈ **4.700+ verificari**, adica
acopera integral cele 3.445 unknown-uri daca e nevoie.
