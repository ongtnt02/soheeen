#!/usr/bin/env python3
"""소희엔 OG 공유 미리보기 이미지(1200x630) 생성."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
FONT_DIR = "/usr/share/fonts/pickle-hwp/"
F = FONT_DIR + "NotoSansCJKkr-Regular.otf"
MONO = FONT_DIR + "NotoSansMonoCJKkr-Regular.otf"

BLUE = (36, 86, 240)
NAVY = (15, 27, 45)
GREY = (92, 104, 122)
LIGHT = (246, 248, 252)


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)

# 배경: 아주 옅은 그라데이션 + 그리드
for y in range(H):
    t = y / H
    r = int(255 - 9 * t)
    g = int(255 - 7 * t)
    b = int(255 - 3 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

step = 40
for x in range(0, W, step):
    d.line([(x, 0), (x, H)], fill=(237, 241, 248), width=1)
for y in range(0, H, step):
    d.line([(0, y), (W, y)], fill=(237, 241, 248), width=1)

# 우측 상단 부드러운 블루 글로우
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([W - 420, -220, W + 160, 300], fill=45)
glow = glow.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(90))
img.paste(Image.new("RGB", (W, H), (36, 86, 240)), (0, 0), glow)

d = ImageDraw.Draw(img)

# 로고 마크 (파란 라운드 사각형 + 막대 3개)
mx, my, ms = 128, 104, 84
d.rounded_rectangle([mx, my, mx + ms, my + ms], radius=22, fill=BLUE)
bar_w = 7
bx = mx + 22
for i, (top, bottom) in enumerate([(30, 56), (22, 62), (38, 54)]):
    x0 = bx + i * 14
    d.rounded_rectangle([x0, my + top, x0 + bar_w, my + bottom], radius=3, fill=(255, 255, 255))

# 브랜드명
f_brand = font(F, 62)
d.text((mx + ms + 26, my + 4), "소희엔", font=f_brand, fill=NAVY)
f_sub = font(MONO, 20)
d.text((mx + ms + 30, my + 74), "AD  OPERATIONS", font=f_sub, fill=GREY)

# 칩
chip_text = "광고 운영 대행  ·  LMS  ·  Meta"
f_chip = font(F, 24)
tw = d.textlength(chip_text, font=f_chip)
cy = 236
d.rounded_rectangle([128, cy, 128 + tw + 44, cy + 46], radius=23, outline=(214, 224, 244), width=2, fill=(255, 255, 255))
d.ellipse([144, cy + 19, 152, cy + 27], fill=BLUE)
d.text((166, cy + 9), chip_text, font=f_chip, fill=(44, 60, 84))

# 헤드라인 (두 줄)
f_h = font(F, 58)
d.text((128, 316), "광고는 파트너가 실행하고,", font=f_h, fill=NAVY, stroke_width=1, stroke_fill=NAVY)
d.text((128, 392), "성과는 소희엔이 관리합니다.", font=f_h, fill=NAVY, stroke_width=1, stroke_fill=NAVY)

# 구분선
d.line([(128, 500), (1104, 500)], fill=(222, 230, 242), width=2)

# 하단 설명
f_p = font(F, 26)
d.text((128, 524), "LMS 대량 고객 메시지 · 메타(Meta) 광고의 기획과 총괄 운영", font=f_p, fill=GREY)

# 하단 우측 도메인
f_u = font(MONO, 20)
url = "ongtnt02.github.io/soheeen"
uw = d.textlength(url, font=f_u)
d.text((1104 - uw, 526), url, font=f_u, fill=(120, 132, 150))

# 좌측 하단 포인트 라인
d.rounded_rectangle([72, 104, 76, 560], radius=2, fill=(222, 232, 248))

img.save("og-image.png", "PNG", optimize=True)
print("saved og-image.png", img.size)
