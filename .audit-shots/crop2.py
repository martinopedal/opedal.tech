"""Crop a true above-fold (~hero) shot of mobile_home_full + check work/blog visuals."""
from PIL import Image
from pathlib import Path

OUT = Path(r"C:\git\opedal.tech\.audit-shots")

# Mobile home: DPR=3, viewport 390x844 → image height row 844*3=2532 covers above-fold
img = Image.open(OUT / "mobile_home_full.png")
print("mobile_home_full size:", img.size)
top_crop = img.crop((0, 0, img.width, min(img.height, 2532)))
top_crop.save(OUT / "mobile_home_hero.png")

# About section on mobile starts at y=509 css px, so 1527 device px.
# Crop the about section (with portrait) on mobile
about_top = 509 * 3 - 60
about_bot = (509 + 876) * 3 + 60
img.crop((0, max(0, about_top), img.width, min(img.height, about_bot))).save(OUT / "mobile_home_about.png")

# Desktop home — about section
img_d = Image.open(OUT / "desktop_home_full.png")
print("desktop_home_full size:", img_d.size)
about_top_d = 482 - 30
about_bot_d = 482 + 531 + 30
img_d.crop((0, max(0, about_top_d), img_d.width, min(img_d.height, about_bot_d))).save(OUT / "desktop_home_about.png")

# Hero section (above About) — 0 to 482 desktop
img_d.crop((0, 0, img_d.width, 482)).save(OUT / "desktop_home_hero.png")

# OSS section to surface the language pill colors
oss_top_d = 1907 - 30
oss_bot_d = 1907 + 1534 + 30
img_d.crop((0, max(0, oss_top_d), img_d.width, min(img_d.height, oss_bot_d))).save(OUT / "desktop_home_oss.png")

print("Done.")
