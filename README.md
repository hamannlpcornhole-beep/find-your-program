# Find Your Program: Dev Player QR Page

QR-code landing page for Level Up Cornhole's 4 development players and 5 coaches. One page, tracked by `?ref=`, no discount codes. Every product link on the page gets `utm_source=qr&utm_medium=devplayer&utm_campaign={ref}`.

**Live:** https://hamannlpcornhole-beep.github.io/find-your-program/

| Player | Link | QR |
|---|---|---|
| Brandie McCuen | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=brandie | `qrcodes/brandie_qr.png` |
| Kenneth Boucher | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=kenneth | `qrcodes/kenneth_qr.png` |
| Simon Ballard | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=simon | `qrcodes/simon_qr.png` |
| Rylan Brocket | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=rylan | `qrcodes/rylan_qr.png` |
| Richard Nyberg (coach) | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=richard | `qrcodes/richard_qr.png` |
| Colin Hodet (coach) | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=colin | `qrcodes/colin_qr.png` |
| AJ Sims (coach) | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=aj | `qrcodes/aj_qr.png` |
| Hunter Thorson (coach) | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=hunter | `qrcodes/hunter_qr.png` |
| Peyton Haynes (coach) | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=peyton | `qrcodes/peyton_qr.png` |
| General (no person) | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=general | `qrcodes/general_qr.png` |

## Layout
- `index.html`: the whole page. Styles and the quiz script are inline; images load from `assets/img/`
- `assets/img/`: web-sized photos, logo, favicon and link-preview image used by the page
- `qrcodes/`: current QR codes. `qrcodes/old-claude-artifact/` has the retired ones that point at the old claude.ai link
- `scripts/make_qr.py`: regenerates the QR codes and checks each one decodes to the right URL
- `assets/source/`: uncropped coach photos and original logo, for re-cropping
- `docs/HANDOFF.md`: original brief with Shopify handles and variant IDs, quiz logic, crop coordinates, open TODOs. Its design section describes the first version (Anton + Work Sans, white theme, base64 images); the September 2026 redesign replaced that with a dark theme, Barlow Condensed + Barlow, action photo backgrounds and a full-screen quiz pop-up. Product data and quiz routing did not change.
- `preview.html`: redirects to the main page (kept so old preview links still work)

**Don't rename or move this repo.** The printed QR codes point at `/find-your-program/`, so a new name breaks every code.

## Deploying
GitHub Pages serves `main` from the repo root. Push to `main` and it's live in about a minute.
