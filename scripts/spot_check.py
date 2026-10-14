#!/usr/bin/env python3
"""抽查辅助：裁剪生成图的高风险锚点，并与对应实物图并置对比。

仅依赖 Pillow。坐标用相对值(0~1)，便于不看像素直接按构图比例裁剪。

单区域并置：
  python spot_check.py --gen g.png --real r.png \
      --box 0.30,0.40,0.74,0.58 --out z.jpg

只裁生成图（不并置实物）：
  python spot_check.py --gen g.png --box 0.30,0.40,0.74,0.58 --out z.jpg

多区域（同一图裁多块，纵向拼接；--box 用逗号分隔多组，用 ';' 区隔）：
  python spot_check.py --gen g.png --real r.png \
      --box "0.0,0.27,0.5,0.46;0.5,0.27,1.0,0.46" --out z.jpg \
      --layout vertical

可选 --realbox 指定实物图裁剪区域（默认整图）；--target-width 控制输出宽度。
"""
import argparse
from PIL import Image


def parse_boxes(s):
    groups = [g for g in s.split(";") if g.strip()]
    out = []
    for g in groups:
        vals = [float(x) for x in g.split(",")]
        if len(vals) != 4:
            raise SystemExit(f"box 必须是4个数: {g}")
        out.append(tuple(vals))
    return out


def crop_rel(im, box):
    w, h = im.size
    x0, y0, x1, y1 = box
    return im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", required=True)
    ap.add_argument("--real")
    ap.add_argument("--realbox")
    ap.add_argument("--box", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--layout", choices=["horizontal", "vertical"], default="horizontal")
    ap.add_argument("--target-width", type=int, default=900)
    args = ap.parse_args()

    gen = Image.open(args.gen).convert("RGB")
    real = Image.open(args.real).convert("RGB") if args.real else None
    if real and args.realbox:
        real = crop_rel(real, parse_boxes(args.realbox)[0])

    strips = []
    for box in parse_boxes(args.box):
        g = crop_rel(gen, box)
        if real is not None:
            r = real.copy()
            #统一高度后并排
            H = max(g.height, r.height)
            def fit(im):
                w = int(im.width * H / im.height)
                return im.resize((w, H))
            pair = Image.new("RGB", (fit(g).width + fit(r).width + 20, H), "white")
            pair.paste(fit(g), (0, 0))
            pair.paste(fit(r), (fit(g).width + 20, 0))
            strips.append(pair)
        else:
            strips.append(g)

    if len(strips) == 1:
        canvas = strips[0]
    elif args.layout == "vertical":
        W = max(s.width for s in strips)
        H = sum(s.height for s in strips) + 12 * (len(strips) - 1)
        canvas = Image.new("RGB", (W, H), "white")
        y = 0
        for s in strips:
            canvas.paste(s, (0, y)); y += s.height + 12
    else:
        H = max(s.height for s in strips)
        W = sum(s.width for s in strips) + 12 * (len(strips) - 1)
        canvas = Image.new("RGB", (W, H), "white")
        x = 0
        for s in strips:
            canvas.paste(s, (x, 0)); x += s.width + 12

    if canvas.width > args.target_width:
        canvas = canvas.resize((args.target_width, int(canvas.height * args.target_width / canvas.width)))
    canvas.save(args.out, quality=93)
    print("saved", args.out, canvas.size)


if __name__ == "__main__":
    main()
