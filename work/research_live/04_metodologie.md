# Raport LIVE: catch-all, validare, hit-rate si deliverability (iulie 2026)

> Cercetare cu web live (WebSearch + WebFetch), surse citate per afirmatie.
> Marcajele [neverificat] indica inferente fara sursa directa.

## 1. Tratarea domeniilor CATCH-ALL in cold email (consens 2025–2026)

**Consensul comunitatii: nu se arunca, dar nici nu se trimit "orbeste" — se segmenteaza si se testeaza cu volum limitat.**

- Recomandarea standard (Smartlead & ghiduri asociate): adresele catch-all se pun in **campanie separata, cu volum redus si monitorizare stricta**; invalide/risky merg in fisier de supresie. Verificare inainte de import; peste 2% bounce domeniul e marcat suspect, peste 5% mail-ul ajunge in Promotions/Spam. (smartlead.ai/blog/verify-emails-in-bulk-using-smartlead, smartlead.ai/blog/how-to-verify-email-address)
- Prospeo (ghid 2026): excluderea totala a catch-all elimina **15–30% din lista B2B accesibila**; workflow recomandat: segment dedicat → **test de 50–100 emailuri de pe domeniu incalzit → monitorizare 48h → scalare doar daca bounce < 2%**; suprima segmentul catch-all daca bounce-ul lui depaseste ~3%. (prospeo.io/s/catch-all-emails, prospeo.io/s/catch-all-domain)
- Rate de bounce observate la catch-all: Hunter estimeaza ca bounce-ul adreselor accept-all e **~jumatate din rata de invalide a listei** (lista cu 10% invalide → ~5% bounce pe accept-all). (hunter.io/cold-email-guide/email-bounce-rate) Alte surse citeaza **~23% hard bounce pe catch-all neverificate** — semnificativ peste pragul de 2%. (prospeo.io/s/catch-all-emails) ~15–20% din domeniile B2B sunt catch-all. (prospeo.io/s/cold-email-bounce-rate)
- Benchmark-uri bounce 2026: bun **<3%**, best-in-class **<1.5%** (Amplemarket); acceptabil hard bounce **<2%**; pauza campanie la 2% hard / 5% total. (amplemarket.com/blog/cold-email-benchmarks, mailwarm.com/blog/cold-email-bounce-rate-acceptable-reduction)
- Pozitia conservatoare (Clay, ghiduri deliverability): implicit **nu trimite** la catch-all — livrarea "reusita" fara citire scade engagement si reputatia. (clay.com/blog/b2b-cold-email-deliverability)
- [neverificat] Fire concrete r/coldemail nu au putut fi accesate direct; sinteza se bazeaza pe blogurile tool-urilor si agregatoare.

## 2. Validarea catch-all: servicii/tehnici 2025–2026

- **BounceBan** (specialist catch-all, fara trimitere de email): pretinde verificare fiabila pentru **85–95%** din adresele catch-all/SEG cu **97%+ acuratete**. (bounceban.com) Recenzie independenta Sparkle.io: test pe 470 adrese business → **0.2% bounce observat**; pret de la $34/luna; recomandat ca **"second-pass verifier"** dupa ce verificatorul principal marcheaza catch-all/unknown. (sparkle.io/blog/bounceban-review) Alt test independent (LeadHaste): prinde ~94.6/100 din bounce-urile reale scapate de alte stack-uri. (leadhaste.com/tools/bounceban)
- **Scrubby** (validare prin conturi "burner" / semnale reale): pretinde **98% acuratete**; 4.8/5 pe G2 (45 recenzii), dar zero recenzii Capterra si un raport Reddit de **false-negative masiv** (700/1700 marcate invalid desi spot-check-urile sugerau ca multe erau livrabile). (g2.com/products/scrubby/reviews, toksta.com/products/scrubby)
- Validitate de piata: benchmark-ul Anymail Finder 2026 foloseste **BounceBan ca arbitru pentru domeniile catch-all** (ZeroBounce + MillionVerifier + BounceBan, consens 2-din-3). (anymailfinder.com/email-finder-benchmark)
- Tehnica alternativa: **bounce processing real** (trimiti si procesezi bounce-urile ca semnal) — abordarea "test batch 50–100 + monitor 48h". [neverificat] — fara studii independente cantitative dincolo de recenziile citate.

## 3. Hit-rate normal pentru emailuri nominale verificate la IMM-uri europene mici

- "Un tool cu 90% acuratete pe VP-uri tech din SUA poate da **60% pe patroni de IMM-uri europene**" (calitativ). (leadbomb.io/blog/how-accurate-are-email-finders)
- Hit-rate "Valid" raportat: **40–55% pentru SMB SUA + piete UE secundare**; 55–70% enterprise SUA/mid-market vest-european; fondatorii de SMB si firmele foarte mici la baza intervalelor. (syncgtm.com/blog/best-b2b-email-finder-tools)
- Benchmark Anymail Finder (iunie 2026, 5.000 contacte US/UK/FR/DE): coverage 49–87% intre tool-uri, fara defalcare SMB/tari; tool-urile bune dau 60–75% pe liste B2B standard. (anymailfinder.com/email-finder-benchmark)
- **Concluzie: 25–40% nominale verificate pe firmele cu domeniu propriu, cu pattern+SMTP si catch-all respins, este realist** — cifra exacta pentru micro-IMM-uri romanesti este [neverificat] (nu exista benchmark public RO; inferenta din intervalele de mai sus).

## 4. Deliverability 2026 pentru campania clientului

**Cerinte oficiale:**
- **Google** (enforcement dur din nov. 2025, respingeri 550): toti expeditorii — SPF sau DKIM, PTR valid, TLS, **spam rate <0.3% in Postmaster Tools**; bulk (5.000+/zi catre @gmail.com) — **DMARC (macar p=none) + aliniere SPF/DKIM + one-click unsubscribe (RFC 8058)**. Tinta practica: **<0.1%**. (support.google.com/a/answer/81126, gmass.co/blog/gmail-bulk-sender-guidelines)
- **Yahoo**: echivalent, spam complaint <0.3%. (emailwarmup.com)
- **Microsoft Outlook.com** (din 5 mai 2025): 5.000+/zi → SPF + DKIM pass + DMARC minim p=none aliniat, altfel respingere 550 5.7.15. (techcommunity.microsoft.com, dmarcwise.io/blog/outlook-new-requirements-2025)

**Volum recomandat cold email 2026:** 20–50 emailuri/zi/inbox (inclusiv warmup), plafon ~50; scalare prin inboxuri/domenii suplimentare (2–3 inboxuri/domeniu, 40–90 sends/domeniu/zi); peste 100–150/inbox → +43% spam rate; warmup 14–21 zile (94% inbox placement vs 61% fara). (mailreach.co, howmanycoldemailsperday.com, maildeck.co)

**Make.com + Gmail personal: configuratie riscanta.** Limita tehnica 500/zi, dar sigur ~25/zi/inbox pentru cold email; fara SPF/DKIM/DMARC pe domeniu propriu; risc suspendare. Recomandare unanima: **Google Workspace pe domeniu separat dedicat**. (smartlead.ai/blog/gmail-sending-limits, prospeo.io/s/cold-email-gmail, mailmeteor.com) Make.com e doar orchestrator — warmup, throttling per-inbox si bounce handling trebuie construite manual in scenariu [neverificat — concluzie proprie].

## Implicatii concrete pentru proiectul nostru

1. **Nu respinge catch-all-urile de tot**: pipeline-ul actual arunca probabil 15–30% din tinta atinsibila. Reclasificare in segment "Catch-all — netrimis inca" + second-pass specializat (BounceBan: ~$34/luna, 0.2% bounce in test independent; cere aprobarea clientului inainte).
2. **Daca clientul accepta risc controlat**: catch-all validate BounceBan → campanie separata Make.com, pilot 50–100, monitorizare 48h, oprire automata la 2–3% bounce.
3. **Reancoreaza asteptarile contractuale**: 50–70% pe toate firmele e peste benchmark-urile 2026 pentru SMB-uri UE mici (40–55% chiar cu tool-uri comerciale). Raporteaza separat % pe firmele cu domeniu vs % pe total.
4. **Infrastructura de trimitere trebuie schimbata inainte de campanie**: Google Workspace pe domeniu dedicat (nu domeniul principal TB), DMARC p=none aliniat, one-click unsubscribe RFC 8058, warmup 14–21 zile, max 30–50/zi/inbox → campanie esalonata pe saptamani sau 2–3 inboxuri.
5. **Monitorizare obligatorie**: Google Postmaster Tools cu tinta spam rate <0.1% + procesare reala a bounce-urilor in Make.com (suprimare automata la hard bounce).
