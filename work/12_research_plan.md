# Research: validarea planului (5 subagenti)

> NOTA: agentii nu au avut acces web live (defect de mediu); cifrele sunt din cunostinte pana in ian. 2026 - orientative. Pretul Reoon 10K=$11.90 confirmat LIVE separat.


---

## Verificatoare email

NOTA IMPORTANTA PENTRU ORCHESTRATOR: Toate apelurile de tool (WebSearch, WebFetch, Bash/curl, ToolSearch) esueaza in acest mediu cu eroarea "permission handler returned updatedInput ... failed schema validation" — o problema de configurare a harness-ului (canUseTool/PermissionRequest hook), nu a inputului. NU am putut face cercetare web live. Raportul de mai jos e construit din cunostinte de antrenament (acoperire pana in ian. 2026, preturi de pe parcursul 2025) si trebuie tratat ca ORIENTATIV — verificati cifrele pe paginile de pricing inainte de plata.

# Comparatie servicii de verificare email (~10.000 verificari, pay-as-you-go)

| Serviciu | Pret ~10k PAYG (orientativ, 2025) | $/email | Catch-all | Acuratete raportata | Free tier |
|---|---|---|---|---|---|
| **Reoon** | **~$11.90 (10k instant, nu expira)** | ~$0.0012 | Marcheaza catch-all ca "risky"; poate valida partial inboxuri pe domenii Google Workspace/anumite gazduiri | ~99% (claim) | 100/zi (daily credits) |
| **MyEmailVerifier** | ~$19 | ~$0.0019 | Marcheaza catch-all; nu taxeaza rezultatele "unknown" | 98%+ (claim) | ~100 credite |
| **CaptainVerify** | ~€28–30 | ~$0.003 | Detectie de baza (accept-all → risky) | ~98% | 100 credite |
| **MillionVerifier** | ~$37 | ~$0.0037 | Marcheaza catch-all; nu taxeaza "unknown", reverificari gratuite; reputatie foarte buna (recomandat frecvent de comunitatea cold-email) | 99%+ (claim) | ~200 credite |
| **Emailable** | ~$38 | ~$0.0038 | Standard (risky/unknown) | 99% (claim) | ~250 credite |
| **Bouncer (usebouncer)** | ~$50 | ~$0.005 | **Cel mai bun pe catch-all**: "deliverability kit"/verificare profunda a domeniilor catch-all, scor de toxicitate | 99.5% (claim) | 100 credite |
| **Verifalia** | ~$50–80 (credit packs; scump) | ~$0.005–0.008 | Buna, niveluri de calitate configurabile | 99%+ | ~25/zi |
| **ZeroBounce** | ~$65–80 | ~$0.007–0.008 | Standard + AI scoring (cost extra) | 99%+ (claim, garantie SLA) | 100/luna |
| **NeverBounce** | ~$80 | ~$0.008 | Standard | 99.9% (claim de marketing) | ~1.000 la inregistrare |
| **Truelist** | ~$99/luna unlimited sau PAYG ~$0.004–0.008 | variabil | Slaba/standard; recenzii mixte privind acuratetea | 99% (claim) | ~1.000 credite |

## Observatii cheie pentru cazul vostru

1. **Niciun verificator nu "sparge" cu adevarat catch-all-ul** prin SMTP clasic — un domeniu accept-all raspunde OK la orice adresa. Cele care pretind mai mult (Bouncer deep catch-all, ZeroBounce AI scoring, Reoon pe Google-hosted) fac inferente probabilistice. Decizia voastra de a respinge domeniile catch-all (punctul e) e corecta pentru tinta bounce <2%.
2. **La waterfall pe tipare (prenume.nume@, p.nume@ etc.) volumul de verificari e mare si valoarea per verificare mica** — costul unitar conteaza mai mult decat diferentele marginale de acuratete. Reoon la ~$0.0012/email e de 3–7x mai ieftin decat MillionVerifier/Bouncer/ZeroBounce.
3. Reoon are recenzii bune (AppSumo/comunitatea cold-email), API simplu cu mod "power" (verificare profunda) si creditele instant nu expira — potrivit pentru oprire-la-primul-valid.
4. Singurul rival la buget: **MyEmailVerifier** (~$19/10k) — nu aduce nimic in plus fata de Reoon.

## Recomandare

**Ramaneti pe Reoon la $11.90/10k.** Este cea mai ieftina optiune serioasa din piata, adecvata pipeline-ului (verificare in mod deep/power, oprire la primul valid, excludere catch-all), si se incadreaza in bugetul sub $15. Pentru bounce <2%: trimiteti DOAR statusul "valid/safe" (nu "risky"/"unknown"/catch-all).

**Upgrade optional, doar daca vreti sa recuperati firme de pe domenii catch-all** (frecvente la IMM-uri romanesti pe hosting shared): rulati subsetul de candidati catch-all prin **Bouncer cu verificare deep catch-all** — la ~$0.005/email, 2–3.000 de verificari costa ~$10–15 si ar putea adauga cateva zeci de nominale. Se incadreaza in plafonul de $50 si e singura cheltuiala suplimentara cu ROI plauzibil.

**Avertisment de provenienta a datelor**: cifrele din tabel NU au fost verificate live pe web in aceasta sesiune (toate tool-urile de retea au esuat din cauza unei erori de configurare a permisiunilor in harness); ele reflecta preturile publice cunoscute din 2025. Inainte de achizitie, confirmati pretul exact pe reoon.com si, daca se foloseste, usebouncer.com.

---

## Email findere

Toate apelurile de tool-uri (Bash/curl, WebSearch, ToolSearch) esueaza in acest mediu din cauza unei erori de configurare a permission handler-ului ("updatedInput failed schema validation" pe orice tool). Nu am putut face verificare live pe web. Raspund pe baza cunostintelor la zi (cutoff ianuarie 2026) — preturile se schimba rar, dar verificati inainte de plata.

# Email findere internationale vs. pipeline-ul tipare+Reoon (firme B2B romanesti)

**Nota metodologica:** cercetare din cunostinte pana la ian. 2026; verificarea live a esuat din motive tehnice de mediu (tool-urile de web fetch indisponibile). Cifrele de pret pot varia cu ±10-20%.

## Tabel comparativ

| Tool | Free tier real | Cost ~1000-2500 firme | Domain search | Acoperire IMM-uri RO mici | Observatii |
|---|---|---|---|---|---|
| **Hunter.io** | 25 cautari + 50 verificari/luna | Starter $49/luna (500 cautari) → ~$98-149 pt 2500 | **Da** (punct forte) | Slaba-medie: doar emailuri publicate pe web (le-ati acoperit deja prin scraping) | Baza = crawl web public; pentru firme fara site = zero |
| **Snov.io** | ~50 credite/luna (trial recurent) | Starter $39 (1000 cr) / Pro $99 (5000 cr) | Da | Slaba: baza LinkedIn-centrica | Include verifier propriu; multe rezultate "guessed" |
| **Apollo.io** | ~100 credite email/luna (cere email corporate) | Basic ~$49/luna, credite email generoase | Da (persoane per companie) | Slaba pt micro-IMM: gaseste doar oameni cu LinkedIn; administratorii de SRL-uri vechi rareori sunt acolo | Bounce notoriu mai mare; ar necesita re-verificare Reoon oricum |
| **Prospeo** | 75 credite/luna | $39/luna = 1000 credite; taxeaza doar emailuri valide gasite | Da | Medie: motor pattern+verificare, similar pipeline-ului vostru | **Aveti deja API key in .env** — cel mai natural add-on |
| **Skrapp** | ~100 credite trial | $39/luna (1000) | Da | Slaba (LinkedIn-centric) | Nimic peste Snov/Apollo |
| **FindThatLead** | ~50 credite | $49/luna | Da | Slaba | In mare parte pattern-guessing nemarcat; calitate indoielnica |
| **Anymail Finder** | trial 3 zile, ~90 emailuri verificate | $49/luna ≈ 1000 emailuri **verificate** (plateste doar valide) | Da | Medie: face exact ce faceti voi (tipare+SMTP), la pret mai mare | Nu taxeaza catch-all/negasite — bun ca benchmark |
| **Dropcontact** | fara free tier real (~25 test) | ~€24/luna (1000 cr) | Nu (imbogatire pe liste) | Medie in UE, dar optimizat pe Franta; RO modest | GDPR-clean (fara baza stocata, algoritmic) — argument bun pt client |
| **Icypeas** | ~25-50 cautari gratuite | cel mai ieftin: ~€19-29/luna pt mii de cautari | Da (domain scan) | Medie: tot pattern+verificare | Alternativa low-cost la Anymail Finder |
| **ContactOut** | ~4-5 contacte/zi | scump ($79+/luna) | Nu | Foarte slaba (recrutare, LinkedIn, US-centric) | Irelevant pt acest proiect |
| **RocketReach** | 5 lookups/luna | $39-80/luna | Da | Foarte slaba pe IMM-uri RO | US-centric, irelevant |

## Raspuns la intrebarea cheie

**Nu — niciunul nu ar aduce semnificativ mai multe adrese nominale decat pipeline-ul vostru sub $50.** Motive structurale:

1. **Tool-urile cu baza de date** (Apollo, RocketReach, ContactOut, Hunter-database, Snov, Skrapp) acopera doar persoane cu amprenta web/LinkedIn. Administratorii IMM-urilor romanesti vechi (publicul vostru, 56% fara domeniu gasibil) practic nu exista in aceste baze. Acoperire realista: 5-15% din firme, majoritatea suprapunandu-se cu firmele "usoare" pe care pipeline-ul le rezolva oricum.
2. **Tool-urile algoritmice** (Anymail Finder, Icypeas, Prospeo, Dropcontact) fac exact ce faceti voi — tipare + verificare SMTP — dar la ~$39-49/1000 emailuri, fata de **$11.90/10.000 verificari Reoon** (~30-40x mai scump per rezultat). Voi aveti avantajul unic: **numele reale ale administratorilor din ANAF**, pe care niciun finder nu le are pentru RO.
3. Emailurile din Apollo/Snov ar trebui oricum re-verificate cu Reoon pentru tinta bounce <2%.

## Combinatii istete de free tiers (cost $0)

Merita 1-2 ore, ca plasa de siguranta pe firmele cu domeniu dar fara rezultat din tipare:
- **Prospeo 75 + Apollo 100 + Snov 50 + Hunter 25 + Skrapp ~100 = ~350 cautari gratuite/luna.**
- Rulati-le pe un **esantion de 100-150 domenii esuate** la pasul (d). Daca hit-rate-ul e sub ~10% peste ce a gasit pipeline-ul (predictia mea), inchideti subiectul cu dovada in `work/stats.md`. Daca surprinzator e >20%, o luna de **Prospeo $39** (1000 credite, taxeaza doar validele, API deja integrat in `.env`) ramane sub buget.
- **Hunter free (25 domain search)**: folositi-l pe cele mai valoroase 25 de domenii pentru a prinde emailuri nominale publicate istoric (PDF-uri, pagini vechi) pe care scraperul le-a ratat.

## Recomandare finala

1. **Pastrati pipeline-ul tipare+Reoon ca motor principal** — la $11.90 e imbatabil ca cost/rezultat si e singurul care valorifica numele din ANAF.
2. **Test gratuit pe esantion** cu free tiers (Prospeo + Apollo + Hunter), decizie pe date, cost $0.
3. **Singura cheltuiala eventual justificata sub $50:** Prospeo $39/luna ca fallback pe domeniile unde tiparele au esuat, DOAR daca testul pe esantion o justifica; cereti aprobarea clientului inainte (regula 3 din CLAUDE.md).
4. Pentru domeniile **catch-all respinse** (pierdere reala de nominale): finderele din lista nu rezolva problema (nici ele nu taxeaza/valideaza catch-all); daca volumul e mare, subiectul separat de cercetat sunt serviciile dedicate de verificare catch-all (ex. Scrubby, Bounceban), nu finderele.

**Estimare impact:** free tiers + eventual Prospeo ar adauga realist **20-60 nominale verificate** peste cele ~250-300 estimate — util, dar nu schimba ordinul de marime; tinta de 50-70% nominale nu poate fi atinsa prin findere comerciale pentru acest profil de firme.

---

## Surse de date RO

Nu am putut face research live: mediul are un bug de configurare (permission handler-ul elimină parametrii tuturor tool call-urilor — WebSearch, Bash/curl, chiar și Read eșuează cu "required parameter missing"). Răspund din cunoștințe (cutoff ian. 2026); **prețurile sunt orientative și trebuie verificate pe site înainte de orice achiziție.**

# Surse de date B2B România — evaluare pentru 2.495 CUI-uri

## Tabel comparativ

| Sursă | Email? | Website / Telefon? | Export în masă pe CUI | Preț orientativ | API/CSV | Calitate / prospețime |
|---|---|---|---|---|---|---|
| **listafirme.ro** (Borg Design) | Da, majoritar **generice** (office@) | Da / Da | Da — liste personalizate la comandă, se poate filtra/potrivi pe CUI | ~0,10–0,35 lei/firmă cu câmpuri de contact → **~250–900 lei (~€50–180)** pt. 2.500; API separat pe credite (mai mult date financiare/juridice) | CSV/XLS la comandă + API | Bună; bază ONRC/ANAF actualizată frecvent; emailurile colectate din surse publice, prospețime variabilă |
| **borg.ro** (aceeași firmă) | Da, generice | Da / Da | Da — vinde **toată baza** de firme RO (aplicație + export) | ~1.200–2.000 lei licența cu actualizări; neeconomic pt. doar 2.500 firme | Aplicație desktop + export | Aceeași sursă ca listafirme; multe emailuri vechi/moarte în baza integrală |
| **targetare.ro** | Da, generice + rar nominale | Da / Da | Da — export CSV pe bază de credite; filtrare, dar potrivirea pe listă proprie de CUI e greoaie (nu e gândit ca "enrichment pe listă") | Abonament ~€49–129/lună cu N credite export; **1 lună poate acoperi ~1.000–5.000 firme** | Export CSV; API la planuri mari | Date ANAF + web crawling propriu; websiteuri destul de bune, emailuri neverificate tehnic |
| **risco.ro** | Parțial (generice) | Da / Da | Orientat pe verificare risc per firmă, nu pe export marketing în masă | Abonamente ~100–300 lei/lună; API comercial pe cerere | API REST bun (JSON) | Foarte proaspăt pe date juridice/financiare; slab pe contact |
| **veridion.com** | Rareori (generice) | Da (puncte forte: website, clasificare) / parțial | Da — API de enrichment (match pe nume+adresă, nu direct CUI) | **Enterprise**: mii de $/an, minim mult peste bugetul de $50 | API | Cea mai bună acoperire de websiteuri, dar complet în afara bugetului |
| **topfirme.com** | Uneori generice, afișate pe site | Da / Da | Nu vinde export oficial | — | Nu | Director web static, date vechi; scraping = zonă gri ToS |
| **firme.info** | Rar | Parțial / Da | Nu | Gratuit la vizualizare | Nu | Agregat ONRC, bun pt. administratori (pe care îi ai deja din ANAF) |
| **datelefirmei.ro** | Da, generice | Da / Da | Da — vinde baze de date pe județe/CAEN | ~200–800 lei per pachet | CSV/XLS | Calitate incertă, actualizare neclară, rată mare de bounce raportată de utilizatori |
| **data.gov.ro / ONRC / ANAF** | **Nu** (fără emailuri) | Nu / Nu | ONRC Recom Online: interogări plătite per firmă; ANAF open data gratuit | Recom ~x lei/interogare; ANAF gratuit | CSV/API | Oficial, cel mai proaspăt pe stare firmă — dar l-ați exploatat deja |

## Răspuns la întrebarea cheie

**Nu există sursă românească care să vândă emailuri NOMINALE verificate ale decidenților pentru IMM-uri.** Toate sursele comerciale (listafirme, borg, targetare, datelefirmei) vând în principal **emailuri generice + websiteuri + telefoane**. Nominale apar sporadic (unde firma și-a publicat singură contactele) și **niciodată verificate tehnic** — bounce-ul tipic pe baze cumpărate e 5–15%, peste ținta voastră de <2%, deci oricum ar trebui trecute prin Reoon.

Ce **se poate** cumpăra util: **websiteuri și emailuri generice** pentru cele ~56% firme fără domeniu găsit. Aici o listă personalizată listafirme.ro (potrivită pe CUI) sau 1 lună de targetare.ro (~€49) ar putea adăuga câteva sute de domenii/contacte pe care nu le-ați găsit — input nou pentru pipeline-ul vostru de tipare + Reoon, nu înlocuitor al lui.

## GDPR — atenție la nominale cumpărate

- Emailul nominal (prenume.nume@firma.ro) este **dată cu caracter personal**. Cumpărat dintr-o bază terță, temeiul "interes legitim" e fragil: furnizorul rar poate proba sursa și informarea persoanei (art. 14 GDPR — obligația de informare la colectare indirectă).
- Emailurile **generate de voi din surse publice** (site-ul propriu al firmei, funcție publică de administrator din ONRC) + interes legitim B2B + opt-out clar în fiecare mesaj = poziție mult mai apărabilă decât liste nominale cumpărate.
- Adresele generice (office@) nu sunt date personale — risc zero acolo.
- Recomandare practică: păstrați per adresă câmpul "sursă" (deja regulă de proiect) — e exact ce cere o eventuală verificare ANSPDCP.

## Recomandare

1. **Nu cumpărați "emailuri de decidenți"** — nu există la calitatea cerută; pipeline-ul vostru (ANAF administratori → domeniu → tipare → Reoon) rămâne singura cale spre nominale verificate cu bounce <2%.
2. **Merită testat, în buget:** cere ofertă listafirme.ro pentru o listă personalizată potrivită pe cele ~1.400 CUI-uri fără domeniu, doar câmpurile website + email + telefon (estimat €50–150 — cere aprobare clientului dacă depășește $50). Alternativ 1 lună targetare.ro (~€49) dacă permite exportul segmentului relevant.
3. **Excludeți** Veridion (enterprise, în afara bugetului), borg full-DB (plătiți 1M de firme pentru 2.500), datelefirmei (calitate incertă).
4. Orice email cumpărat intră **obligatoriu** prin Reoon înainte de output — creditele de $11.90 acoperă lejer și acest volum suplimentar.

**Caveat:** toate prețurile sunt din memorie (cutoff ian. 2026), neverificate live din cauza defecțiunii tool-urilor în această sesiune — confirmați pe site/ofertă înainte de decizie.

---

## Metodologie

Nota tehnica: uneltele de acces web (WebSearch/WebFetch/Bash) au esuat in acest mediu din cauza unei erori de configurare a permission handler-ului ("updatedInput failed schema validation" la fiecare apel). Nu am putut face cercetare web live. Raspunsul de mai jos se bazeaza pe cunostinte pana in ianuarie 2026 (acopera practicile 2024-2025); tratati cifrele exacte de pret ca orientative si verificati-le inainte de achizitie.

# Metodologie email-finding B2B 2025-2026 — validare plan

## 1) Pattern-waterfall + verificare SMTP — inca standard?
**Da, ramane metoda standard**, dar cu doua evolutii:
- Industria a trecut la **"waterfall enrichment"** multi-furnizor (Clay, FullEnrich: Prospeo → Findymail → Hunter → Icypeas etc.) — fiecare furnizor incearca, se plateste doar la hit. Pentru IMM-uri romanesti vechi, acoperirea acestor furnizori e slaba (bazele lor sunt construite din LinkedIn/companii cu prezenta digitala), deci pipeline-ul vostru ANAF + pattern + SMTP e alegerea corecta, nu un compromis.
- Verificarea SMTP e tot mai degradata pe Google Workspace si Microsoft 365 (blocheaza probe RCPT TO, raspund ambiguu). Pe domenii romanesti gazduite local (cPanel, hosting .ro clasic) SMTP-ul functioneaza inca bine — segmentul vostru e de fapt favorabil metodei.
- Ordinea tiparelor pentru Romania: `prenume.nume@` >> `prenume@` > `nume@` > `office@`+nume in salutatie > `p.nume@` > `prenumenume@`. "Oprire la primul valid" e corecta.

## 2) Catch-all — tehnici noi
Da, exista o categorie noua de tool-uri (2024-2025) dedicate catch-all:
- **Verificare prin bounce processing real**: Scrubby (catchall.io) — trimite/simuleaza livrare reala de pe domenii-tampon si proceseaza bounce-urile; dureaza 24-72h, cost mic per adresa.
- **BounceBan** — specializat exclusiv pe catch-all, pretinde ~97-99% acuratete fara trimitere, folosit ca strat final in waterfall-uri.
- Unele verificatoare clasice (Bouncer, EmailListVerify) au adaugat scoruri de "deliverability" pe catch-all, dar raman probabilistice.
- Tehnica gratuita si robusta: **inferenta de tipar intra-domeniu** — daca scrapingul (pasul c) a gasit o adresa nominala pe un domeniu catch-all (ex. `ion.popescu@firma.ro` pe pagina de contact), tiparul e confirmat empiric si puteti genera adresa decidentului cu incredere mare, chiar daca SMTP nu poate confirma.
- **Critica planului (e)**: respingerea in bloc a catch-all e sigura pentru bounce <2%, dar aruncati probabil 25-35% din domenii. Recomandare: (1) recuperati catch-all-urile cu tipar confirmat prin scraping — gratuit; (2) pentru restul, un test cu BounceBan/Scrubby pe subsetul catch-all cu nume de administrator cunoscut ar costa orientativ $10-30 si poate adauga 50-150 nominale — se incadreaza in bugetul de $50. Alternativ, segment separat de campanie "risc acceptat" cu volum mic si suprimare automata la bounce.

## 3) LinkedIn pentru decidenti romani
- **Scraping DIY: nu.** Incalca ToS LinkedIn (saga hiQ s-a incheiat in defavoarea scraperului pe breach of contract), iar sub GDPR scrapingul de date personale la scara e greu de justificat pentru un livrabil comercial catre client. Risc reputational si juridic disproportionat.
- **Export ieftin legitim**: furnizori care licentiaza date (Apollo — plan gratuit/Basic ~$49/luna, Kaspr — focus UE, Lusha, ContactOut). Insa acoperirea pentru IMM-uri romanesti vechi e slaba: administratorii acestor firme rar au profil LinkedIn, si aproape niciodata email asociat in aceste baze.
- **Concluzie**: pentru segmentul vostru, ANAF/ONRC bate LinkedIn la nume de decidenti. LinkedIn merita eventual doar pentru subsetul de firme mari/moderne ramase fara adresa dupa pipeline (manual, cateva zeci).
- GDPR: adresele nominale B2B sunt date personale — documentati interesul legitim (Recital 47), includeti opt-out clar in campanie, pastrati evidenta surselor (o faceti deja, regula 8).

## 4) Rate tipice de succes — e 15% sub-par?
**Nu, e normal pentru acest segment.** Benchmarks orientative:
- Waterfall premium pe companii US/enterprise: 60-80% gasire email cand persoana+domeniul sunt cunoscute.
- IMM-uri europene cu domeniu cunoscut: 30-50% tipar valid confirmabil.
- Realitatea IMM-urilor romanesti vechi: **multe nu au deloc cutii postale nominale** — exista doar `office@`/`contact@`. Acesta e plafonul structural, nu o slabiciune a metodei.
- Cu 44% din firme fara domeniu gasibil, estimarea voastra de 10-12% nominale verificate din total e plauzibila, poate usor pesimista (cu recuperarea catch-all: 13-18%).
- **Semnal de alarma contractual**: tinta de 50-70% nominale verificate e nerealista pentru acest univers de firme, indiferent de metoda sau buget. Nicio combinatie de tool-uri nu o atinge cand firma nu are mailbox nominal. Recomand renegocierea/clarificarea urgenta cu clientul: fie tinta se aplica doar firmelor cu domeniu activ (~1.100), unde 50%+ devine atins-abil, fie definitia include "generic verificat + nume decident pentru personalizare" (care acopera contractual "restul raman pe adresa generica").

## 5) Deliverability pentru campania Make.com
- **Cerinte obligatorii 2024-2025 (Google/Yahoo, apoi Microsoft mai 2025)**: SPF + DKIM + DMARC (minim p=none, ideal quarantine), **one-click unsubscribe (RFC 8058)**, rata de spam complaints <0.3% (monitorizata in Google Postmaster Tools).
- **Domeniu separat de trimitere** (subdomeniu sau lookalike, ex. `mail.transilvaniabusiness.ro`) — protejeaza domeniul principal.
- **Warm-up 2-4 saptamani**: start 15-25/zi/inbox, crestere ~25%/saptamana, plafon 50-100/zi/inbox; mai multe inboxuri daca volumul cere.
- **In Make.com**: modul Sleep/throttling intre trimiteri (60-120s, interval randomizat), trimitere prin SMTP/ESP cu webhook de bounce, nu Gmail brut; scenariu separat care proceseaza bounce-urile si marcheaza automat Status Exclus (inchide bucla si cu verificarea catch-all daca alegeti segmentul "risc acceptat").
- Primul email: text simplu, fara imagini/link-uri multe, personalizat cu numele din ANAF; testare seed inainte de lansare (mail-tester.com, GlockApps).
- Igiena: hard bounce = suprimare imediata; re-verificare Reoon daca lista sta >30-60 zile inainte de trimitere.

## Verdict pe plan, punct cu punct
| Pas | Verdict |
|---|---|
| (a) ANAF/demoanaf pentru administratori | Corect, sursa autoritativa, superioara LinkedIn pentru segment |
| (b) Descoperire domenii + validare continut | Corect; validati continutul si pentru cei 588 candidati MX — un domeniu gresit inseamna email catre firma gresita (risc GDPR/spam) |
| (c) Scraping pagini contact | Corect; adresele nominale gasite sunt si cheia de recuperare a catch-all-urilor (tipar confirmat) |
| (d) Reoon 10k/$11.90 + waterfall tipare | Corect si cost-eficient; Reoon e bine cotat, folositi modul "power verification"; ~4-5 tipare × ~1.000 domenii incap in credite; sariti domeniile free-mail (yahoo/gmail nu se ghicesc) |
| (e) Respingere catch-all in bloc | Prea conservator — recuperati intai gratuit prin tipar confirmat, apoi optional BounceBan/Scrubby pe subset ($10-30) |
| Estimare 250-300 nominale | Realista; cu recuperare catch-all: 300-420 |
| Tinta contractuala 50-70% | **Nerealizabila pe universul total — renegociati definitia/baza de calcul acum, nu la livrare** |

---

## SINTEZA CRITICA

# VERDICT FINAL — Consultant sceptic data-enrichment

## (1) Este planul curent cea mai buna alegere sub $15?

**Da, fara echivoc.** Toate cele 4 rapoarte converg independent:
- Reoon $11.90/10k = ~$0.0012/verificare, de 3-7x mai ieftin decat urmatoarea optiune serioasa (MyEmailVerifier ~$19, MillionVerifier ~$37, Bouncer ~$50). Singurul rival de buget (MyEmailVerifier) nu aduce nimic in plus.
- Finderele comerciale (Hunter, Apollo, Snov etc.) costa $39-49/1000 rezultate (~30-40x mai scump) si au acoperire 5-15% pe IMM-uri romanesti vechi fara LinkedIn — exact segmentul vostru.
- Nicio sursa romaneasca (listafirme, targetare, borg) nu vinde nominale verificate — doar generice + site-uri, bounce tipic 5-15%.
- Avantajul vostru structural: numele reale ale administratorilor din ANAF, pe care niciun finder nu le are. Plus segmentul e favorabil SMTP (hosting .ro clasic, nu Google/M365 care blocheaza RCPT TO).

Atentie: toate preturile din rapoarte sunt din memorie (tool-urile web au esuat in toate cele 4 sesiuni) — confirmati $11.90 pe reoon.com inainte de plata.

## (2) Ce aduce concret $30-50 in plus?

In ordinea ROI:

| Cheltuiala | Cost | Castig estimat | Verdict |
|---|---|---|---|
| **BounceBan/Scrubby pe subsetul catch-all cu administrator cunoscut** | $10-30 | **+50-150 nominale** | Cel mai bun ROI platit; servicii dedicate catch-all (bounce processing real), nu probabilistica |
| **Bouncer deep catch-all** (alternativa la cel de sus) | ~$10-15 (2-3k verif.) | +cateva zeci | Doar daca BounceBan/Scrubby nu merg; ramane probabilistic |
| Lista personalizata listafirme.ro pe cele ~1.400 CUI fara domeniu (doar website+email+telefon) | ~€50-150 (peste plafon, cere aprobare) | +cateva sute de domenii noi = input pentru pipeline, indirect +30-80 nominale | Util dar depaseste $50; alternativ targetare.ro ~€49/luna |
| Prospeo $39/luna (API key deja in .env) | $39 | +20-60 nominale | DOAR dupa test gratuit pe esantion (vezi mai jos) |

Nu cumparati: Apollo/Snov/Hunter platit (acoperire RO slaba), Veridion (enterprise), datelefirmei (bounce mare), scraping LinkedIn (ToS + GDPR).

## (3) Top 3 imbunatatiri actionabile

1. **Recuperare catch-all prin tipar confirmat intra-domeniu — COST $0, castig imediat.** Daca scrapingul (pasul c, 612 firme) a gasit o nominala pe un domeniu catch-all (ex. ion.popescu@firma.ro), tiparul e dovedit empiric — generati adresa administratorului cu incredere mare, chiar fara confirmare SMTP. Respingerea in bloc a catch-all (pasul e) arunca probabil 25-35% din domenii. Estimat: +30-80 nominale gratuit. Apoi optional BounceBan/Scrubby pe restul ($10-30, +50-150).
2. **Test pe esantion cu free tiers inainte de orice cheltuiala noua — COST $0.** Prospeo 75 + Apollo 100 + Snov 50 + Hunter 25 ≈ 350 cautari gratuite. Rulati pe 100-150 domenii unde tiparele au esuat. Hit-rate <10% peste pipeline (predictia rapoartelor) → inchideti subiectul cu dovada in work/stats.md; >20% → o luna Prospeo $39.
3. **Renegociati ACUM baza de calcul a tintei 50-70% — cel mai mare castig al proiectului, cost $0.** Cu 56% firme fara domeniu si estimarea realista de 10-12% (13-18% cu catch-all recuperat), tinta pe universul total e matematic imposibila — multe IMM-uri nu au deloc mailbox nominal, indiferent de unealta sau buget. Optiuni de propus clientului: (a) tinta se aplica doar firmelor cu domeniu activ (~1.100, unde 50%+ e atins-abil: 300-420 nominale / 1.100 ≈ 27-38%, tot strans dar negociabil), sau (b) definitia include "generic verificat + nume decident pentru personalizare". Nu la livrare — acum.

## (4) Riscuri trecute cu vederea

- **Riscul contractual e riscul #1** — 300-420 nominale = 12-17% din 2.495, fata de 50-70% promis. Niciun tool nu repara asta; doar renegocierea.
- **588 candidati MX nevalidati pe continut**: un domeniu gresit = email nominal catre firma gresita = incident GDPR + spam complaint. Validati continutul inainte de generarea tiparelor.
- **GDPR pe nominale**: adresa prenume.nume@ e data personala. Pozitia voastra (surse publice ANAF/site propriu + interes legitim + opt-out) e apărabila; liste nominale cumparate nu ar fi (art. 14, informare la colectare indirecta). Pastrati campul "sursa" per adresa (regula 8 — deja acoperit).
- **Verificarea nu garanteaza livrarea**: bounce <2% cere si SPF/DKIM/DMARC, one-click unsubscribe (RFC 8058), subdomeniu separat de trimitere, warm-up 2-4 saptamani, throttling 60-120s in Make.com si scenariu de procesare bounce cu suprimare automata. Fara astea, si o lista perfecta face spam complaints >0.3%.
- **Perisabilitate**: daca lista sta >30-60 zile pana la campanie, re-verificati cu Reoon (creditele nu expira — inca un argument pro-Reoon).
- **In output-ul final**: doar statusul "valid/safe" de la Reoon intra in campanie; "risky"/"unknown"/catch-all neconfirmat = Exclus.

**Bottom line:** pastrati Reoon $11.90 ca motor; cheltuiti intai $0 (recuperare catch-all prin tipar confirmat + free tiers pe esantion), apoi maxim $10-30 pe BounceBan/Scrubby daca subsetul catch-all e mare. Total realist: $12-42, rezultat 300-420+ nominale verificate. Si renegociati tinta contractuala saptamana asta.