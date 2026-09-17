# Level Up Cornhole — Development Player QR Funnel — Handoff

## What this is
A single web page, sourced from 4 unique QR codes (one per development player), that lets prospects browse Level Up Cornhole coaching programs and take a diagnostic quiz that recommends a program + coach. All outbound links are UTM-tagged so Gavin can manually trace which dev player drove which sale. **No discount codes are used — attribution is tracking-only.**

**Live published page:** https://claude.ai/artifact/DiJMRpkgVjuYSJHbepptgC
**Main file:** `dev-player-funnel.html` (single self-contained HTML file, ~850KB — all images are base64-embedded inline, no external assets required to run it)

## Business context
- Business: Level Up Cornhole (levelupcornhole.shop), an online cornhole coaching/membership platform run by Gavin Hamann.
- 4 development players are the referral sources: **Brandie McCuen, Kenneth Boucher, Simon Ballard, Rylan Brocket**. Each gets their own QR code linking to the same page with a different `?ref=` param.
- Player QR PNGs are in `/qrcodes/` (brandie_qr.png, kenneth_qr.png, simon_qr.png, rylan_qr.png), each encoding the page URL + that player's ref param.

## Player URLs (ref param pattern)
```
https://claude.ai/artifact/DiJMRpkgVjuYSJHbepptgC?ref=brandie
https://claude.ai/artifact/DiJMRpkgVjuYSJHbepptgC?ref=kenneth
https://claude.ai/artifact/DiJMRpkgVjuYSJHbepptgC?ref=simon
https://claude.ai/artifact/DiJMRpkgVjuYSJHbepptgC?ref=rylan
```
Every outbound product link on the page appends UTM params: `utm_source=qr&utm_medium=devplayer&utm_campaign={ref}` (the `ref` value is read from the incoming URL's `?ref=` query param via JS on page load — see `ref` variable near top of `<script>`).

## Page structure (top to bottom)
1. **Sticky white nav** — logo, Programs/Coaches/Results links, "Find My Program" CTA button
2. **Hero** — 2-column (stacks on mobile): headline, lede, an animated bobbing-arrow callout pointing at the CTA buttons ("Click here to find the program that fits you best!"), trust stats, and a video-placeholder box on the right (Gavin still needs to record/upload a real welcome video — currently a styled placeholder with a play-button icon)
3. **How It Works** — 3 numbered step cards + a "Find My Program →" button that triggers the quiz
4. **Programs** — 3 plan cards (Elite / Compete / Pro) + a Video Breakdown one-time-service strip below them
5. **Coaches** — 4 coach cards with real photos, each with a "View Coach" button and a secondary "Book a call" link for one-time sessions
6. **Results** — full-bleed **dark/black section** (intentionally different background to break up the page's white/gray rhythm) with 2 testimonials
7. **Quiz** — white card, progress bar, multi-step diagnostic (logic below)
8. **Footer** — black bar with logo + nav links + copyright. **Open item:** Gavin hasn't provided social media handles yet — footer currently has no social links. Ask him for Instagram/TikTok/etc. handles if he wants them added.

## Design system
- **Color ratio:** ~70% white, 18% light gray, 8% black, 4% orange. Orange (`--orange: #F36C21`) is reserved for CTAs/accents only — this was a deliberate design-critique fix (earlier version overused orange).
- **Full CSS variable tokens** (in `<style>` `:root`):
  ```css
  --orange: #F36C21;
  --black: #121212;
  --dark-gray: #303030;
  --gray: #6B7280;
  --light-gray: #F3F4F6;
  --border: #E5E1D8;
  --white: #FFFFFF;
  --shadow-card: 0 1px 2px rgba(18,18,18,0.04), 0 12px 28px -14px rgba(18,18,18,0.14);
  --shadow-card-hover: 0 1px 2px rgba(18,18,18,0.05), 0 18px 36px -14px rgba(18,18,18,0.20);
  ```
- **Fonts:** Anton (headlines, `h1`/`h2`) + Work Sans (everything else). Loaded via Google Fonts `<link>` in `<head>`. These were chosen after building and visually comparing 4 pairings (Bebas Neue+Inter, Anton+Work Sans, Oswald+Source Sans 3, Archivo Black+Archivo) — Anton+Work Sans won for looking bold/athletic without the cramped look of Bebas Neue.
- **Cards** all use `box-shadow: var(--shadow-card)` (or `--shadow-card-hover` for the quiz wrap) instead of flat borders — this was a deliberate "make it look less templated" pass. Plan cards, coach cards, testimonial cards, step cards, and the video-strip all follow this pattern; the Compete (popular) card gets an orange-tinted shadow, Pro gets a black-tinted shadow.
- Eyebrow labels (small-caps orange section labels) were intentionally reduced from 6 identical instances down to 3 (kept on Hero/Programs/Coaches, dropped from How-It-Works/Results/Quiz) to reduce the "templated" feel.

## Shopify catalog (levelupcornhole.shop) — products used on this page
Domain constant in JS: `const DOMAIN = 'https://levelupcornhole.shop';`

| Product | Handle | Price | Notes |
|---|---|---|---|
| Elite Plan | `elite-plan-19-99-month` | $20/mo | Self-guided |
| Compete Membership | `compete-membership` | $45/mo | Variant per coach — see variant IDs below |
| Pro Plan w/ Richard Nyberg | `elite-plan-19-99-month-copy` | $100/mo | (Shopify handle is a legacy copy-paste name, not a typo) |
| Roll King Development (Colin, Pro tier) | `roll-king-development` | $100/mo | |
| AJency Monthly (AJ, Pro tier) | `ajency-monthly` | $100/mo | |
| Video Breakdown (Single) | `video-breakdown-24-99` | $25 one-time | Generic, no-coach-preference option |
| Video Breakdown Bundle (3) | `video-breakdown-bundle-3-59-99` | $60 one-time | Upsell from single |
| Elite Annual | `elite-annual-plan` | $199/yr | Mentioned on Elite card only |

**Compete Membership variant IDs** (coach selection at checkout):
```
richard: 48264900608222
colin:   48619376279774
aj:      48619376312542
hunter:  48619376345310
```

**Per-coach one-time session products** (added later — Colin's active/live pair uses the "Roll King" branded names, not his older legacy duplicate products which are still Draft status in Shopify):
| Coach | Quick call | Video + call |
|---|---|---|
| Richard | `richard-1-on-1-add-on-call` — $50 | `richard-video-game-review-call` — $75 |
| Colin | `colin-shot-tune-up` — $50 | `colin-specialty-shot-breakdown` — $75 |
| AJ | `aj-1-on-1-add-on-call` — $50 | `aj-video-game-review-call` — $75 |
| Hunter | `hunter-thorson-1-hour-session` — $45 | *(no video+call bundle live yet — quiz falls back to the call-only product and says so)* |

**Known Shopify catalog quirks worth knowing:**
- Hunter Thorson's Pro-tier subscription program is **not live yet** — anywhere the quiz would route to "Hunter Pro," it instead falls back to Compete Membership w/ Hunter (for ongoing) or his $45 1-hour session (for one-time), with copy that says his full program is "coming soon."
- Colin has an older, separate, still-Draft set of one-time products (`colin-hodet-1-hour-session`, `colin-1-on-1-add-on-call`, `colin-video-shot-review-call`) that were **not** used — the live "Roll King" branded ones were used instead. Worth double-checking with Gavin this was the right call.
- There's also a "Spencer Fabionar" Pro plan product in Shopify (Draft status) — Spencer is a **former** coach, not currently featured on this page.

## Quiz logic (full flow — this is the trickiest part to port correctly)
Panels are numbered 1–7 in the DOM but the JS `answer()` function branches non-linearly:

- **Q1–Q3** (experience, skill level, primary goal): diagnostic only, don't affect the outcome — Gavin was asked if he wants these trimmed to shorten the flow; no decision made yet.
- **Q4** (`style` key): self-guided / structured / intensive-1-on-1 — drives the **ongoing** path's tier.
- **Q5** (`mode` key): "Ongoing monthly coaching" vs "One-time review of my throw or game" — the fork point.
  - If `mode === 'ongoing'` → skip straight to the coach question (panel 7).
  - If `mode === 'onetime'` → go to the new **one-time-type question** (panel 6) first.
- **Panel 6 — one-time-type question** (`onetime` key, only shown when mode=onetime): "Just a video analysis" / "Just a call" / "Both — video + call".
  - If `video` → skip the coach question entirely, go straight to the generic Video Breakdown result (coach doesn't matter for an async review).
  - If `call` or `both` → proceed to the coach question (panel 7), with its heading text dynamically rewritten (see `goToCoachPanel()` in JS) to fit the one-time framing.
- **Panel 7 — coach question** (`coach` key): Colin / Richard / AJ / "Just match me" (`match`). Reused for both the ongoing and one-time paths; heading text and the "match" option's label are rewritten in JS depending on which path led here.
- **Result routing** (`showResult()` function) — full decision table:

| mode | style | onetime | coach | Result |
|---|---|---|---|---|
| ongoing | self | — | (ignored) | Elite Plan $20/mo |
| ongoing | structured | — | Colin/Richard/AJ | Compete w/ that coach $45/mo, shows alt-coach links below |
| ongoing | structured | — | match | Compete w/ Richard (default), others as alt links |
| ongoing | intensive | — | Colin/Richard/AJ | Pro w/ that coach $100/mo |
| ongoing | intensive | — | Hunter | Falls back to Compete w/ Hunter (Pro not live) |
| ongoing | intensive | — | match | Pro w/ Richard (default) |
| onetime | — | video | (skipped) | Video Breakdown $25 + 3-pack upsell link |
| onetime | — | call | Colin/Richard/AJ | That coach's $50 call-only product |
| onetime | — | call | Hunter | Hunter's $45 session |
| onetime | — | call | match | Defaults to Richard's $50 call |
| onetime | — | both | Colin/Richard/AJ | That coach's $75 video+call, with $50 call-only shown as a cheaper alt link |
| onetime | — | both | Hunter | Falls back to his $45 session (video+call not live for him) |
| onetime | — | both | match | Defaults to Richard's $75 video+call |

Every result screen has "Retake the quiz" and "See all programs" links, and the primary CTA carries the UTM params.

## Coach content (names, specialties, taglines used verbatim on the page)
- **Richard Nyberg** — nickname "Mr. 11" — "Complete Game Development" — "Mechanics, strategy, consistency, and the mental side of competing."
- **Colin Hodet** — nickname "The Roll King" — "Precision & Shot-Making" — "Precision rolls and shot-making — building a full arsenal, not one trick."
- **AJ Sims** — "Competition-Focused" — "Direct, no-fluff coaching built for tournament prep and real matchups." (No nickname used.)
- **Hunter Thorson** — "1-on-1 Coaching" — "Personalized coaching from Hunter." + italic note "Pro tier coming soon — available now through Compete"

## Image assets — how they were made (for reproducibility if photos ever need re-cropping)
All 4 coach headshots and the logo are embedded as base64 JPEG/PNG directly in the HTML (search for `data:image/jpeg;base64,` — there are exactly 4 occurrences, in DOM order Richard → Colin → AJ → Hunter). Original high-res source photos are uploaded separately (see Uploads below) in case any need re-cropping.

**Crop method used:** OpenCV Haar-cascade frontal-face detection was run on each original photo to find a face bounding box, then all four were cropped to the **same face-height-to-frame ratio (0.40)** and the **same vertical face position (face center at 45% from top)**, then resized to 480×480px JPEGs. This was necessary because the first pass (manual/eyeballed crops) left AJ's face noticeably larger and Hunter's noticeably smaller than the others — the automated, ratio-matched approach fixed that. Richard's Haar detection box came back oversized (it included his cap+neck) and had to be manually corrected to a tighter box before applying the same ratio math. AJ's crop was subsequently zoomed out slightly further (ratio 0.34 instead of 0.40) at Gavin's request ("make AJ's a little smaller").

**Crop coordinates used (original image pixel coordinates, `(x0, y0, side)` = a square crop of `side`×`side` pixels starting at `x0,y0`, then resized to 480×480):**
- Richard (from `25.jpg`): `x0=1053, y0=364, side=750`
- Colin (from `68.jpg`): `x0=914, y0=413, side=820`
- Hunter (from `70.jpg`): `x0=955, y0=360, side=795`
- AJ (from `AJ_Sims-4647.JPEG`): `x0=659, y0=490, side=1979` (final, zoomed-out version)

The Level Up logo used on the page (`logo_clean.png`, embedded as `data:image/png;base64,` — there's exactly 1 occurrence) was cropped from the original uploaded transparent-background PNG.

## Files included in this handoff
- `dev-player-funnel.html` — the production file, ready to publish as-is
- `HANDOFF.md` — this document
- `/qrcodes/brandie_qr.png`, `kenneth_qr.png`, `simon_qr.png`, `rylan_qr.png` — the 4 player QR codes
- `/uploads_reference/` — copies of the original uncropped source photos and logo, in case coach photos ever need re-cropping (25.jpg = Richard source, 68.jpg = Colin source, 70.jpg = Hunter source, AJ_Sims-4647.JPEG = AJ source, Level_Up_Logo.png = original transparent logo)

## Testing approach used during development
All visual changes were verified with **Playwright** (headless Chromium) — screenshotting the rendered HTML at multiple viewport widths (mobile ~390px, tablet ~760px, desktop 1280px) before publishing each change, and scripting through the quiz's click paths to verify branching logic before shipping. Chromium binary used: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.

## Open items / known TODOs
1. **Hero video placeholder** — Gavin needs to record/upload a real welcome video; currently a styled empty placeholder. This was flagged as the single biggest visual liability on the page (largest, most prominent unfinished-looking element).
2. **Footer social links** — no handles provided yet.
3. **Testimonials are unattributed** — need first names + permission from the two quoted players (one names Richard as coach, the other doesn't name a coach).
4. **Q1–Q3 trimming** — asked, not yet decided, whether to cut the diagnostic-only questions to shorten the quiz to ~3 real questions.
5. **Colin's legacy Draft products** — worth confirming with Gavin that the live "Roll King" branded one-time products are the intended ones over the older Draft duplicates.
6. **General visual polish ideas raised but not yet built:** a wide action/gameplay photo somewhere on the page (currently zero action photography, only headshots); a bigger visual treatment for the testimonials section beyond the dark-background swap already done.
