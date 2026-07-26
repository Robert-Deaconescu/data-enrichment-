# 06 — Gasirea GRATUITA de site-uri/domenii pentru firmele fara domeniu cunoscut

Cercetare live: 26 iulie 2026. Context: ~1.390 firme din 2.495 nu au domeniu
cunoscut (plafonul actual: doar ~44% din firme au domeniu). Obiectiv: surse
gratuite de domenii/site-uri, potrivite dupa nume firma + CUI.

Legenda: [verificat] = confirmat live azi (robots.txt / pagina / API);
[neverificat] = din surse secundare, neconfirmat direct.

---

## 1. Directoare romanesti gratuite

### 1.1 listafirme.ro
- **Cautare dupa CUI:** DA (cautare dupa CUI, nume, judet, asociati,
  administratori). [verificat — homepage] Sursa: https://www.listafirme.ro/
- **Model de acces:** 20 credite gratuite la inscriere ("evaluare rapida"),
  pachete platite de la 193 lei; datele de contact (telefon, email) sunt in
  spatele sistemului de credite. Site-ul/emailul NU sunt afisate liber pe
  pagina de firma fara credite. [verificat partial — homepage; continutul exact
  al paginii de firma nu a putut fi vazut: **HTTP 403 de pe IP de datacenter**]
- **robots.txt** [verificat, https://www.listafirme.ro/robots.txt]:
  - ~40 de bot-uri SEO (Ahrefs, Semrush etc.): `Disallow: /` (blocate total);
  - motoare mari non-Google (Yandex, Baidu, Applebot...): `Disallow: /*/`;
  - pentru `User-agent: *`: interzise doar `/inc/`, `/frontdesk/`, `/api/`,
    `/cdn-cgi/` — paginile de firma nu sunt interzise formal pentru un bot
    generic, DAR site-ul blocheaza activ IP-urile de datacenter (403 Cloudflare
    la pagina de firma). Practic: **lookup automat nefezabil si nedorit de
    operator**; tonul general al robots.txt (blocarea agresiva a crawlerelor)
    indica pozitie anti-scraping.
- **Concluzie:** inutilizabil gratuit la scara. Cele 20 credite gratuite pot
  acoperi doar cateva firme-test.

### 1.2 topfirme.com
- **Continut per firma (gratuit):** nume, adresa (strada/oras/judet), cifra de
  afaceri, profit, angajati, pozitie in topuri. **Fara site web, fara email,
  fara telefon** in listarile vizibile. [verificat — pagina de top CAEN]
  Sursa: https://www.topfirme.com/caen/1071/
- **Cautare dupa CUI:** exista camp "Cauta o firma"; cautarea dupa CUI
  [neverificat].
- **robots.txt** [verificat]: contine DOAR blocul Cloudflare "content signals"
  (fara Disallow explicit pentru `*`); semnalele indica search=yes, ai-train=no.
  Sursa: https://www.topfirme.com/robots.txt
- **Concluzie:** nu publica domenii → **irelevant pentru obiectivul nostru**.

### 1.3 firme.info
- **Continut per firma (gratuit)** [verificat pe pagina reala
  http://www.firme.info/td-com-srl-cui23687141/]: adresa completa, cod postal,
  **telefon** (ex. "Telefon: 0762202122"), fax, CUI, nr. reg. com., date
  financiare multi-an. **NU afiseaza site web sau email pe pagina gratuita** —
  acestea ("email + telefon + website + cod caen") se vand ca liste
  personalizate contra cost. [verificat — text pe homepage firme.info]
- **URL-uri predictibile dupa CUI:** `firme.info/<slug-nume>-cui<CUI>/` — dar
  slug-ul numelui e necesar; URL doar cu CUI nu functioneaza (redirect la
  homepage). [verificat]
- **robots.txt** [verificat]: aproape totul permis (`Disallow` doar pe
  `/grafic.php`, `/grafic2.php` si un singur profil de firma).
  Sursa: https://www.firme.info/robots.txt
- **Concluzie:** util pentru **telefoane** (nu domenii). Telefonul poate ajuta
  indirect (cautare inversa a numarului pe web poate scoate site-ul firmei) —
  efort mare, randament incert.

### 1.4 romanian-companies.eu
- **Acelasi operator ca listafirme.ro** — robots.txt identic ca structura
  (aceleasi liste de bot-uri blocate, aceleasi `Disallow: /inc/ /frontdesk/
  /api/`). [verificat — http://romanian-companies.eu/robots.txt]
- HTTPS are certificat invalid pe domeniul propriu (mismatch SSL). [verificat]
- **Concluzie:** aceleasi restrictii ca listafirme.ro; nimic in plus gratuit.

### 1.5 cylex.ro
- **Acces automat: blocat dur.** Cloudflare "Sorry, you have been blocked"
  chiar si la robots.txt, de pe IP de datacenter. [verificat]
- Listarile Cylex contin frecvent site web + email (directoriu clasic de tip
  Pagini Aurii) [neverificat direct azi — inaccesibil din acest mediu].
- **Concluzie:** nefezabil automat din acest mediu; doar lookup manual in
  browser pentru un subset mic de firme prioritare.

### 1.6 paginiaurii.ro
- **Functional** (HTTP 200). [verificat]
- **robots.txt** [verificat, https://www.paginiaurii.ro/robots.txt]: interzice
  `/api/*`, `/*search.aspx`, filtre/sortari; **paginile de listare de firma nu
  sunt interzise** si exista sitemap public
  (`https://www.paginiaurii.ro/sitemap_index_ro.xml`).
- Listarile Pagini Aurii afiseaza in mod tipic telefon si, pentru o parte din
  firme, site web [neverificat per-firma azi].
- **Cautare dupa CUI: NU** — doar dupa nume/categorie/localitate.
- **Concluzie:** candidat rezonabil pentru lookup politicos dupa nume+localitate
  (1 req/s), dar rata de acoperire pentru IMM-uri B2B din Transilvania e
  probabil modesta; fara potrivire pe CUI → risc de false-positive, necesita
  validare (nume pe site-ul gasit).

### 1.7 infobel.com (ro)
- **robots.txt** [verificat]: **blocheaza explicit anthropic-ai, ClaudeBot,
  GPTBot, CCBot** etc.; pentru `*` permite paginile businessdetails pe unele
  tari. Semnal clar anti-bot AI → **nu il folosim automat** (regula proiectului:
  robots.txt respectat).
- **Concluzie:** exclus pentru automatizare.

### 1.8 Altele observate
- **targetare.ro** — "cauta firme gratuit, descarca baze cu numere de telefon";
  robots.txt: Cloudflare content-signals, `Allow: /` pentru `*`, ai-train=no.
  [verificat robots; continutul per firma neverificat]. De testat manual: daca
  afiseaza site-ul firmei gratuit, e o sursa buna.
  Sursa: https://targetare.ro/
- **termene.ro, risco.ro, confidas.ro** — freemium, datele de contact sunt in
  planuri platite [neverificat detaliat; in afara scopului "gratuit"].
- **cauta-firma (open source)** — https://github.com/razvandimescu/cauta-firma
  — 4M+ firme, date ANAF; **fara site/email** (doar date fiscale). [verificat
  descriere repo prin cautare]

---

## 2. Seturi de date oficiale (data.gov.ro / ANAF / ONRC / SEAP)

### 2.1 ONRC — OD_FIRME.CSV (data.gov.ro)
- Set actualizat periodic ("Firme inregistrate la Registrul Comertului pana la
  08.12.2025"): denumire, CUI, nr. inmatriculare, EUID, stare, adresa sediu,
  CAEN. **FARA site web, FARA email, FARA telefon.** [verificat prin paginile
  setului; portalul data.gov.ro a raspuns azi cu 503 intermitent]
  Sursa: https://data.gov.ro/dataset/firme-08-12-2025
- Util doar pentru validare stare firma / adresa, nu pentru domenii.

### 2.2 ANAF webservicesp v9 (deja folosit in pipeline)
- Campuri confirmate in doc oficial: `denumire`, `adresa`, **`telefon`**,
  `fax`, adresa sediu detaliata. **Fara email, fara website.** [verificat]
  Sursa: https://static.anaf.ro/static/10/Anaf/Informatii_R/Servicii_web/doc_WS_V9.txt
- Deci: niciun serviciu ANAF public nu expune email/site.

### 2.3 Registrul RO e-Factura
- Registru public, interogabil (per CUI) pe portalul ANAF; contine doar
  statutul de inregistrare in RO e-Factura. **Fara date de contact.**
  [verificat existenta registrului; absenta campurilor de contact — confirmata
  de documentatia procedurala, fara mentiune de email/site]
  Sursa: https://www.anaf.ro/anaf/internet/ANAF/servicii_online/registre/registrul_eFactura

### 2.4 SEAP / SICAP (e-licitatie.ro)
- Exista **API public nedocumentat oficial dar stabil**, folosit de proiecte
  open-source: `e-licitatie.ro/api-pub/DirectAcquisitionCommon/
  GetDirectAcquisitionList/` etc. — documentat in
  https://github.com/ciocan/sicap-parser (colectie Postman) si folosit de
  https://sicap.ai (date sub Open Government License v1.0). [verificat
  existenta repo/documentatie]
- **Emailurile din SEAP sunt in principal ale autoritatilor contractante**, nu
  ale furnizorilor; datele de operator economic expuse public sunt
  nume/CUI/localitate. Nu exista export bulk oficial gratuit cu emailuri de
  furnizori. [neverificat exhaustiv — merita un test pe 10 firme din lista
  noastra care au contracte SEAP]
- data.gov.ro are seturi punctuale de achizitii (ex. unitati sanitare 2024, XLS)
  — fara contacte de furnizori. Sursa:
  https://data.gov.ro/en/dataset/achizitii-derulate-de-unitatile-sanitare-publice-in-anul-2024
- **Concluzie:** randament mic pentru domenii; doar un subset mic din cele
  1.390 de firme sunt furnizori SEAP.

---

## 3. Google Maps / Places API (2026)

- **Schimbare majora din martie 2025:** creditul lunar de 200 USD a fost
  eliminat; acum fiecare SKU are propriul plafon gratuit lunar. [verificat]
  Surse: https://developers.google.com/maps/billing-and-pricing/pricing ,
  https://www.woosmap.com/blog/google-places-api-pricing
- **Campurile `websiteUri` si `nationalPhoneNumber` sunt in SKU-ul ENTERPRISE**
  (Text Search Enterprise / Place Details Enterprise), nu in Essentials/Pro.
  [verificat] Sursa:
  https://developers.google.com/maps/documentation/places/web-service/data-fields
- **Plafon gratuit Enterprise: 1.000 apeluri/luna** (Text Search Enterprise:
  35 USD/1.000 peste plafon; Place Details Enterprise: 20 USD/1.000).
  [verificat] Sursa: https://developers.google.com/maps/billing-and-pricing/pricing
- **Fezabilitate pentru ~1.390 lookup-uri:** NU incap intr-o singura luna
  gratuit (1.000/luna). Variante: (a) 2 luni calendaristice × 1.000 gratuit;
  (b) ~390 apeluri peste plafon ≈ **13,7 USD** cu Text Search Enterprise —
  deci "aproape gratuit", dar:
- **Problema de ToS (importanta):** Termenii Google Maps Platform interzic
  explicit scraping/exportul continutului ("no scraping", "no caching" cu
  exceptii inguste — doar place ID stocabil nelimitat; restul datelor nu pot fi
  stocate permanent) si **crearea de baze de date proprii din continut Google
  Maps**. Folosirea Places pentru a popula permanent coloana "site web" intr-o
  baza de date livrata clientului este **contrara ToS**. [verificat]
  Surse: https://cloud.google.com/maps-platform/terms ,
  https://developers.google.com/maps/documentation/places/web-service/policies
- **Concluzie:** tehnic fezabil si aproape gratuit, dar **neconform ToS pentru
  cazul nostru de folosire** (stocare + livrare catre client). Recomandare:
  NU folosim Places pentru populare in masa. Alternativa conforma: folosirea
  cautarii web clasice (site-ul firmei gasit organic nu e "continut Google
  Maps").

---

## 4. Cautare programatica gratuita (iulie 2026)

- **Bing Search API: RETRAS definitiv la 11 august 2025** (HTTP 410); inlocuit
  de "Grounding with Bing Search" in Azure AI Foundry — mai scump cu 40–483%,
  nu e drop-in. [verificat] Surse:
  https://learn.microsoft.com/en-us/lifecycle/announcements/bing-search-api-retirement ,
  https://ppc.land/microsoft-ends-bing-search-apis-on-august-11-alternative-costs-40-483-more/
- **Google Programmable Search (Custom Search JSON API):** inca functioneaza cu
  **100 interogari/zi gratuit** (apoi 5 USD/1.000, plafon 10.000/zi; max 10
  rezultate/cerere). ATENTIE: rapoarte multiple ca API-ul e **inchis pentru
  clienti noi in 2026 si va fi oprit la 1 ianuarie 2027**; daca avem deja o
  cheie, functioneaza. [partial verificat — deprecarea din surse secundare:
  https://dev.to/nexgendata/google-kills-custom-search-api-on-jan-1-2027-you-have-9-months-1jg1 ,
  https://searlo.tech/google-custom-search-json-api-closed-to-new-customers ;
  oficial: https://developers.google.com/custom-search/v1/overview]
  - 1.390 firme ÷ 100/zi = **14 zile** de rulare gratuita, query tip
    `"NUME FIRMA" judet` cu extragere primul rezultat non-directoriu.
- **Brave Search API:** planul gratuit clasic (2.000 interogari/luna) **a fost
  eliminat pentru conturi noi (~feb 2026)**; conturile noi primesc **5 USD
  credit/luna ≈ 1.000 interogari gratuite**, apoi ~5 USD/1.000. Conturile vechi
  pe plan Free isi pastreaza 2.000/luna. [neverificat direct in dashboard;
  surse: https://costbench.com/software/ai-search-apis/brave-search-api/free-plan/ ,
  https://yangmao.ai/en/providers/brave-search-api/free-api/ ,
  https://api-dashboard.search.brave.com/documentation/pricing]
  - Cu credit lunar: ~1.000 firme luna 1 + restul luna 2 → **gratuit in 2 luni**.
- **DuckDuckGo:** NU are API oficial de cautare web (doar Instant Answers,
  inutil aici); scraping-ul HTML incalca ToS-ul lor. [cunoscut/neverificat azi]
- **Common Crawl:** gratuit, 250+ mld. pagini indexate; index CDXJ
  (index.commoncrawl.org) + index columnar Parquet pe S3. [verificat]
  Surse: https://commoncrawl.org/url-index , https://index.commoncrawl.org/
  - Utilizare practica pentru noi: NU e motor de cautare dupa nume de firma.
    Realist e invers: **verificarea existentei/continutului domeniilor .ro
    ghicite** (interogare index per domeniu) sau extragerea titlurilor
    homepage-urilor .ro din indexul columnar si potrivirea fuzzy cu numele
    firmelor. Efort mare (Athena/S3 sau descarcare parquet), randament mediu.

### Bonus descoperit in cercetare
- **whois RoTLD (whois.rotld.ro / rotld.ro):** whois-ul .ro este gratuit si
  pentru persoane juridice arata registrantul. Nu permite cautare inversa dupa
  nume, dar e excelent pentru **validarea domeniilor ghicite** (registrant =
  denumirea firmei / CUI-ul se potriveste). Rate-limitat, de folosit politicos.
  [neverificat azi campurile exacte returnate]
- **OpenStreetMap / Overpass API:** gratuit, licenta ODbL (compatibila cu
  stocare, cu atribuire). Romania are insa doar **~19.048 obiecte cu tag
  `website`** si ~4.238 cu `contact:website` in toata tara. [verificat]
  Sursa: https://taginfo.geofabrik.de/europe:romania/keys/website (API stats)
  - Pentru 1.390 IMM-uri B2B, suprapunerea estimata e mica (2–5%), dar costul
    de implementare e minim (un singur dump Overpass pe judetele relevante +
    potrivire fuzzy nume/adresa). Legal 100%.

---

## Plan de actiune gratuit (ordonat dupa randament estimat × efort)

| # | Actiune | Domenii noi estimate (din 1.390) | Efort | Cost |
|---|---------|----------------------------------|-------|------|
| 1 | **Google Programmable Search JSON API** (daca putem obtine/avem cheie): 100 interogari/zi × 14 zile, query `"NUME" judet`, primul rezultat organic non-directoriu, apoi validare CUI/nume pe site + MX | **200–400** (15–30% hit-rate realist pe IMM-uri) | Mic (script existent de validare refolosibil) | 0 lei |
| 2 | **Brave Search API** (cont nou, ~1.000 gratis/luna sau cont vechi 2.000/luna) — rulat in paralel/complementar cu #1 pe firmele fara hit | **+100–250** suplimentar | Mic | 0 lei (2 luni) |
| 3 | **whois RoTLD pentru domeniile deja ghicite** (runda 2 pe candidatii respinsi la MX/audit): confirmare registrant=firma → recuperam candidati eliminati gresit | **+30–80** (recuperare) | Mic | 0 lei |
| 4 | **paginiaurii.ro + targetare.ro lookup politicos** (1 req/s, robots OK) dupa nume+localitate, doar pentru firmele ramase; validare stricta a potrivirii numelui | **+50–150** [neverificat hit-rate] | Mediu | 0 lei |
| 5 | **OpenStreetMap/Overpass** dump pe judetele tinta + fuzzy match nume/adresa | **+20–60** | Mic-Mediu | 0 lei |
| 6 | **Common Crawl** (validare domenii ghicite / potrivire titluri homepage .ro) | **+30–100** | Mare | 0 lei (calcul local) |
| 7 | SEAP api-pub: test pe subsetul de firme cu contracte publice | **+0–20** | Mediu | 0 lei |

**Excluse motivat:** Google Places (incalcare ToS la stocare/livrare, desi ar
costa doar ~13 USD), listafirme.ro/romanian-companies.eu (anti-bot + paywall),
cylex.ro si infobel (blocare explicita a botilor), Bing (retras), DuckDuckGo
(fara API).

**Estimare totala realista: +350–700 domenii noi** → acoperirea cu domeniu ar
urca de la ~44% spre **58–72%**, suficient pentru tinta contractuala de 50–70%
nominale doar daca si conversia domeniu→email nominal verificat se mentine.
Pasii 1+2+3 (efort mic, cost zero) ar trebui rulati primii, in aceasta ordine.
