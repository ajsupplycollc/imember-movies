"""Generate the 'Member berry icons (512/192/180) with PIL — grape gradient + berry + wordmark."""
from PIL import Image, ImageDraw, ImageFont

def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=radius, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im, (0, 0), mask)
    return out

S = 512
im = Image.new("RGB", (S, S), "#1A0F21")
d = ImageDraw.Draw(im)
# subtle radial-ish glow: concentric ellipses
for i in range(30, 0, -1):
    a = int(3 + i * 1.1)
    d.ellipse([S/2 - i*12, -i*9, S/2 + i*12, i*11], fill=(168, 85, 247, 0))
# top glow band
glow = Image.new("L", (S, S), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([-140, -260, S+140, 200], fill=46)
purple = Image.new("RGB", (S, S), "#A855F7")
im = Image.composite(purple, im, glow)
d = ImageDraw.Draw(im)

# berry cluster: three circles
berry = "#7C3AED"
hi = "#C084FC"
d.ellipse([150, 128, 268, 246], fill="#8B5CF6", outline=hi, width=6)   # left
d.ellipse([244, 128, 362, 246], fill="#7C3AED", outline=hi, width=6)   # right
d.ellipse([196, 196, 316, 316], fill="#9333EA", outline=hi, width=6)   # bottom
# stem + leaf
d.line([256, 132, 256, 84], fill="#4ADE80", width=10)
d.polygon([(256, 92), (300, 66), (268, 110)], fill="#4ADE80")
# eyes (member berries have faces)
d.ellipse([214, 230, 234, 250], fill="#1A0F21")
d.ellipse([278, 230, 298, 250], fill="#1A0F21")
d.arc([224, 248, 288, 292], start=20, end=160, fill="#1A0F21", width=8)

# wordmark
try:
    f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 74)
    f2 = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 40)
except Exception:
    f = f2 = ImageFont.load_default()
d.text((S/2, 392), "'MEMBER", font=f, fill="#F5EDFF", anchor="mm")
d.text((S/2, 452), "M O V I E S", font=f2, fill="#B9A3D0", anchor="mm")

im512 = im
im512.save(r"C:\Users\ajsup\imember_movies\icon-512.png")
im512.resize((192, 192), Image.LANCZOS).save(r"C:\Users\ajsup\imember_movies\icon-192.png")
im512.resize((180, 180), Image.LANCZOS).save(r"C:\Users\ajsup\imember_movies\apple-touch-icon.png")
print("icons written")
