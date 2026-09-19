"""Regenerate the QR codes for the 4 dev players and 5 coaches.

Usage:
  python3 -m venv .venv && .venv/bin/pip install "qrcode[pil]" opencv-python-headless
  .venv/bin/python scripts/make_qr.py
"""
from pathlib import Path

import cv2
import qrcode

BASE_URL = "https://hamannlpcornhole-beep.github.io/find-your-program/"
PLAYERS = ["brandie", "kenneth", "simon", "rylan", "richard", "colin", "aj", "hunter", "peyton"]
OUT = Path(__file__).resolve().parent.parent / "qrcodes"

for name in PLAYERS:
    url = f"{BASE_URL}?ref={name}"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=16, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=(10, 10, 10), back_color=(255, 255, 255))
    path = OUT / f"{name}_qr.png"
    img.save(path)
    decoded = cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(path)))[0]
    assert decoded == url, f"{name}: decoded {decoded!r}, expected {url!r}"
    print(f"{path.name}: {img.size[0]}px -> {decoded}")
