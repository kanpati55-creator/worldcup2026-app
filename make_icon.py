# サッカーボールのホーム画面アイコンを生成するスクリプト
from PIL import Image, ImageDraw
import math

S = 720  # 4倍サイズで描いて縮小(なめらかにするため)
img = Image.new('RGB', (S, S))
d = ImageDraw.Draw(img)

# 背景: アプリと同じ紺色グラデーション
top = (26, 58, 92); bottom = (13, 33, 55)
for y in range(S):
    t = y / S
    c = tuple(int(top[i] + (bottom[i]-top[i])*t) for i in range(3))
    d.line([(0, y), (S, y)], fill=c)

cx = cy = S/2
R = S*0.36  # ボール半径

# ボール本体
d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=(250,250,250), outline=(20,20,20), width=int(S*0.018))

def pent(cx0, cy0, r, rot):
    return [(cx0 + r*math.cos(math.radians(rot+72*i)),
             cy0 + r*math.sin(math.radians(rot+72*i))) for i in range(5)]

# 中央の黒五角形
r1 = R*0.38
center_pent = pent(cx, cy, r1, -90)
d.polygon(center_pent, fill=(25,25,25))

# 縫い目ラインと外周パッチ(円でクリップして描く)
mask = Image.new('L', (S, S), 0)
md = ImageDraw.Draw(mask)
md.ellipse([cx-R, cy-R, cx+R, cy+R], fill=255)
patches = Image.new('RGB', (S, S), (250,250,250))
pd = ImageDraw.Draw(patches)
pd.ellipse([cx-R, cy-R, cx+R, cy+R], fill=(250,250,250))
for (px, py) in center_pent:
    ang = math.atan2(py-cy, px-cx)
    bx = cx + R*1.08*math.cos(ang); by = cy + R*1.08*math.sin(ang)
    pd.regular_polygon((bx, by, R*0.30), n_sides=5, rotation=-math.degrees(ang), fill=(25,25,25))
pd.polygon(center_pent, fill=(25,25,25))
for (px, py) in center_pent:
    ang = math.atan2(py-cy, px-cx)
    ex = cx + R*math.cos(ang); ey = cy + R*math.sin(ang)
    pd.line([(px,py),(ex,ey)], fill=(25,25,25), width=int(S*0.016))
img.paste(patches, (0,0), mask)

# 輪郭線を描き直し
d = ImageDraw.Draw(img)
d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=(20,20,20), width=int(S*0.018))

icon = img.resize((180, 180), Image.LANCZOS)
icon.save('apple-touch-icon.png', optimize=True)
print('apple-touch-icon.png generated')
