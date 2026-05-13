"""Crop the certs->speaking->oss band from the full-page CV screenshot."""
from PIL import Image
from pathlib import Path

OUT = Path(r"C:\git\opedal.tech\.audit-shots")

# From the metrics: certs top=4254, oss bottom=6884 (CSS pixels).
# Full page screenshot is at device_scale=1, viewport width=1440.
src = OUT / "desktop_cv_full.png"
img = Image.open(src)
print("desktop_cv_full size:", img.size)

# Pad +/- 30px and stay inside image
top = max(0, 4254 - 30)
bot = min(img.height, 6884 + 30)
crop = img.crop((0, top, img.width, bot))
crop.save(OUT / "desktop_cv_band_certs_to_oss.png")
print("Cropped band size:", crop.size)

# Also crop just the cert-to-speaking gap (4681->4729) with generous padding for visual inspection
top2 = max(0, 4681 - 200)
bot2 = min(img.height, 4729 + 200)
crop2 = img.crop((0, top2, img.width, bot2))
crop2.save(OUT / "desktop_cv_gap_certs_speaking.png")
print("Cert->Speaking gap shot:", crop2.size)

top3 = max(0, 5265 - 200)
bot3 = min(img.height, 5313 + 200)
crop3 = img.crop((0, top3, img.width, bot3))
crop3.save(OUT / "desktop_cv_gap_speaking_oss.png")
print("Speaking->OSS gap shot:", crop3.size)

# Mobile: certifications/speaking/oss approximate. Re-read JSON for mobile sections.
import json
r = json.loads((OUT / "report.json").read_text(encoding="utf-8"))
mobile_secs = r["cv_mobile_metrics"]["sections"]
print("\nMobile section coords:")
for s in mobile_secs:
    print(f"  {s['h2']:<24} top={s['top']} bot={s['bottom']} h={s['height']}")

src_m = OUT / "mobile_cv_full.png"
img_m = Image.open(src_m)
print("mobile_cv_full size (device px):", img_m.size)
# Mobile DPR=3 — page CSS px must be multiplied by 3 to map to image pixels
DPR = 3
def find(name):
    return next(s for s in mobile_secs if s["h2"] == name)

certs_m = find("Certifications")
speak_m = find("Speaking")
oss_m = find("Open Source")

m_top = max(0, (certs_m["top"] - 30) * DPR)
m_bot = min(img_m.height, (oss_m["bottom"] + 30) * DPR)
img_m.crop((0, m_top, img_m.width, m_bot)).save(OUT / "mobile_cv_band_certs_to_oss.png")

m_top2 = max(0, (certs_m["bottom"] - 200) * DPR)
m_bot2 = min(img_m.height, (speak_m["top"] + 200) * DPR)
img_m.crop((0, m_top2, img_m.width, m_bot2)).save(OUT / "mobile_cv_gap_certs_speaking.png")

m_top3 = max(0, (speak_m["bottom"] - 200) * DPR)
m_bot3 = min(img_m.height, (oss_m["top"] + 200) * DPR)
img_m.crop((0, m_top3, img_m.width, m_bot3)).save(OUT / "mobile_cv_gap_speaking_oss.png")

print("Done.")
