#!/usr/bin/env python3
"""尺寸标注辅助：在白底多视图（建议先用图像模型生成无文字版）上叠加
细灰色尺寸线与正确数字。数字由脚本绘制，避免模型写错。仅依赖 Pillow。

坐标用相对值(0~1)。示例：
  python make_size_chart.py --base views.png --out size.jpg --title "焦糖花8葫芦碗" \
   --hline "0.05,0.62,0.40,0.62,直径 20.6cm" \
   --vline "0.72,0.30,0.72,0.60,高 10.1cm"

可重复 --hline/--vline。字体自动寻找常见中文字体。
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(size):
    import os
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def parse(s):
    parts = s.split(",")
    if len(parts) != 5:
        raise SystemExit(f"需要 x0,y0,x1,y1,文字 : {s}")
    x0, y0, x1, y1 = map(float, parts[:4])
    return x0, y0, x1, y1, parts[4]


def dim_line(d, W, H, spec, vertical, font):
    x0, y0, x1, y1, text = spec
    p0, p1 = (x0 * W, y0 * H), (x1 * W, y1 * H)
    gray = (110, 110, 110)
    tick = 10
    d.line([p0, p1], fill=gray, width=2)
    if vertical:
        for (x, y) in (p0, p1):
            d.line([(x - tick, y), (x + tick, y)], fill=gray, width=2)
        pos = (p1[0] + 8, (p0[1] + p1[1]) / 2 - 12)
    else:
        for (x, y) in (p0, p1):
            d.line([(x, y - tick), (x, y + tick)], fill=gray, width=2)
        tw = d.textlength(text, font=font)
        pos = ((p0[0] + p1[0]) / 2 - tw / 2, p1[1] + 6)
    d.text(pos, text, fill=(70, 70, 70), font=font)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title")
    ap.add_argument("--hline", action="append", default=[])
    ap.add_argument("--vline", action="append", default=[])
    args = ap.parse_args()

    im = Image.open(args.base).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    tfont = load_font(int(H * 0.035))
    sfont = load_font(int(H * 0.024))

    if args.title:
        tw = d.textlength(args.title, font=tfont)
        d.text(((W - tw) / 2, H * 0.02), args.title, fill=(40, 40, 40), font=tfont)
    for s in args.hline:
        dim_line(d, W, H, parse(s), False, sfont)
    for s in args.vline:
        dim_line(d, W, H, parse(s), True, sfont)

    im.save(args.out, quality=93)
    print("saved", args.out, im.size)


if __name__ == "__main__":
    main()
