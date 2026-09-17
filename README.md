# Find Your Program: Dev Player QR Page

QR-code landing page for Level Up Cornhole's 4 development players. One page, tracked by `?ref=`, no discount codes. Every product link on the page gets `utm_source=qr&utm_medium=devplayer&utm_campaign={ref}`.

**Live:** https://hamannlpcornhole-beep.github.io/find-your-program/

| Player | Link | QR |
|---|---|---|
| Brandie McCuen | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=brandie | `qrcodes/brandie_qr.png` |
| Kenneth Boucher | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=kenneth | `qrcodes/kenneth_qr.png` |
| Simon Ballard | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=simon | `qrcodes/simon_qr.png` |
| Rylan Brocket | https://hamannlpcornhole-beep.github.io/find-your-program/?ref=rylan | `qrcodes/rylan_qr.png` |

## Layout
- `index.html`: the whole page (images are base64 inline, no build step)
- `qrcodes/`: current QR codes. `qrcodes/old-claude-artifact/` has the retired ones that point at the old claude.ai link
- `scripts/make_qr.py`: regenerates the QR codes and checks each one decodes to the right URL
- `assets/source/`: uncropped coach photos and original logo, for re-cropping
- `docs/HANDOFF.md`: full brief with Shopify handles and variant IDs, quiz logic, design tokens, crop coordinates, open TODOs

## Deploying
GitHub Pages serves `main` from the repo root. Push to `main` and it's live in about a minute.
