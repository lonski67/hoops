#!/usr/bin/env python3
"""Generate pixel-art city backgrounds for Hoops game."""
import os
import math
import random
from PIL import Image, ImageDraw

W, H = 480, 270
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'backgrounds')
os.makedirs(OUT_DIR, exist_ok=True)

random.seed(42)  # Deterministic

def lerp_color(c0, c1, t):
    return tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))

def gradient_sky(draw, stops):
    """Draw a vertical gradient sky from color stops [(y_frac, (r,g,b)), ...]"""
    for y in range(H):
        t = y / H
        # Find surrounding stops
        c0, c1 = stops[0], stops[-1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i+1][0]:
                c0, c1 = stops[i], stops[i+1]
                break
        if c0[0] == c1[0]:
            lt = 0
        else:
            lt = (t - c0[0]) / (c1[0] - c0[0])
        color = lerp_color(c0[1], c1[1], lt)
        draw.line([(0, y), (W, y)], fill=color)

def draw_windows(draw, bx, by, bw, bh, lit_color, off_color, spacing=5, win_w=2, win_h=2):
    for wy in range(by + 4, by + bh - 3, spacing):
        for wx in range(bx + 3, bx + bw - 3, spacing):
            lit = random.random() > 0.3
            draw.rectangle([wx, wy, wx + win_w - 1, wy + win_h - 1],
                           fill=lit_color if lit else off_color)

# ============================================================
# PARIS
# ============================================================
def draw_paris():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)

    gradient_sky(d, [
        (0, (255, 140, 80)),
        (0.3, (255, 180, 130)),
        (0.6, (220, 200, 180)),
        (1.0, (180, 200, 160)),
    ])

    # Distant buildings
    for x in range(0, W, 22):
        h = 25 + ((x * 7 + 13) % 30)
        by = H - 50 - h
        d.rectangle([x, by, x + 19, H - 40], fill=(139, 115, 85))
        d.rectangle([x - 1, by - 3, x + 20, by - 1], fill=(107, 91, 69))
        d.rectangle([x + 2, by - 5, x + 17, by - 4], fill=(107, 91, 69))
        for wy in range(by + 5, by + h, 7):
            for wx in range(x + 2, x + 18, 5):
                lit = random.random() > 0.4
                d.rectangle([wx, wy, wx + 1, wy + 2],
                            fill=(255, 228, 160) if lit else (122, 106, 80))

    # Mid buildings
    for x in range(5, W, 28):
        h = 35 + ((x * 11 + 7) % 35)
        by = H - 45 - h
        d.rectangle([x, by, x + 23, H - 30], fill=(107, 81, 53))
        d.rectangle([x - 1, by - 3, x + 24, by], fill=(90, 64, 48))
        d.rectangle([x + 3, by - 6, x + 20, by - 4], fill=(90, 64, 48))
        if (x * 3) % 5 < 2:
            d.rectangle([x + 8, by - 12, x + 10, by - 7], fill=(90, 64, 48))
        for wy in range(by + 5, by + h + 5, 6):
            for wx in range(x + 3, x + 21, 5):
                lit = random.random() > 0.3
                d.rectangle([wx, wy, wx + 1, wy + 2],
                            fill=(255, 208, 128) if lit else (74, 58, 40))

    # Near buildings
    for x in range(-2, W, 32):
        h = 40 + ((x * 13 + 3) % 40)
        by = H - 38 - h
        d.rectangle([x, by, x + 27, H - 18], fill=(74, 55, 40))
        d.rectangle([x - 1, by - 4, x + 28, by - 1], fill=(58, 42, 28))
        d.rectangle([x + 4, by - 7, x + 23, by - 5], fill=(58, 42, 28))
        for wy in range(by + 6, by + h + 8, 7):
            for wx in range(x + 3, x + 25, 6):
                lit = random.random() > 0.25
                d.rectangle([wx, wy, wx + 2, wy + 3],
                            fill=(255, 228, 160) if lit else (42, 30, 20))
        d.rectangle([x + 11, by + h + 10, x + 16, by + h + 17], fill=(42, 30, 20))

    # Eiffel Tower
    tx, tBase = 160, H - 38
    tc = (92, 64, 51)
    tl = (122, 96, 80)
    for y in range(0, tBase - 12):
        t = y / (tBase - 12)
        spread = int(t * 32)
        d.rectangle([tx - spread - 3, y + 12, tx - spread, y + 12], fill=tc)
        d.rectangle([tx + spread - 1, y + 12, tx + spread + 2, y + 12], fill=tc)
    for i in range(5):
        y = 45 + i * 35
        t = y / (tBase - 12)
        spread = int(t * 32)
        d.rectangle([tx - spread, y, tx + spread + spread - 1, y + 2], fill=tc)
        d.rectangle([tx - spread + 2, y, tx + spread + spread - 5, y], fill=tl)
    d.rectangle([tx - 22, 75, tx + 21, 79], fill=tc)
    d.rectangle([tx - 14, 48, tx + 13, 51], fill=tc)
    d.rectangle([tx - 8, 28, tx + 7, 30], fill=tc)
    d.rectangle([tx - 1, 2, tx, 11], fill=tc)
    d.rectangle([tx, 0, tx, 2], fill=tl)

    # Clouds
    for cx, cy in [(60, 30), (320, 45), (420, 25)]:
        d.rectangle([cx, cy, cx + 17, cy + 4], fill=(255, 210, 175))
        d.rectangle([cx + 3, cy - 3, cx + 14, cy - 1], fill=(255, 210, 175))
        d.rectangle([cx + 6, cy - 5, cx + 11, cy - 4], fill=(255, 215, 185))

    # Tree line
    for x in range(0, W, 8):
        th = 6 + ((x * 7) % 5)
        d.rectangle([x, H - 38 - th, x + 6, H - 39], fill=(74, 107, 58))
        d.rectangle([x + 1, H - 38 - th - 2, x + 5, H - 38 - th], fill=(58, 90, 42))

    # Ground
    d.rectangle([0, H - 38, W - 1, H - 1], fill=(107, 142, 90))
    for x in range(0, W, 6):
        d.rectangle([x, H - 38, x + 4, H - 37], fill=(122, 158, 106))

    return img

# ============================================================
# SAN FRANCISCO
# ============================================================
def draw_san_francisco():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)

    gradient_sky(d, [
        (0, (140, 165, 190)),
        (0.4, (175, 195, 210)),
        (0.7, (200, 215, 225)),
        (1.0, (160, 190, 210)),
    ])

    # Distant hills
    for x in range(W):
        h1 = int(math.sin(x * 0.012) * 25 + math.sin(x * 0.025) * 15 + 100)
        d.rectangle([x, h1, x, H - 1], fill=(106, 154, 90))

    # Fog wisps
    for x in range(0, W, 6):
        fy = int(85 + math.sin(x * 0.03) * 10)
        d.rectangle([x, fy, x + 5, fy + 1], fill=(210, 220, 230))

    # Mid hills
    for x in range(W):
        h2 = int(math.sin(x * 0.008 + 1) * 20 + math.sin(x * 0.02 + 2) * 12 + 130)
        d.rectangle([x, h2, x, H - 1], fill=(90, 138, 74))

    # Bay water
    d.rectangle([0, H - 65, W - 1, H - 31], fill=(58, 107, 140))
    for x in range(0, W, 8):
        wy = H - 65 + 5 + ((x * 3) % 25)
        d.rectangle([x, wy, x + 4, wy], fill=(74, 123, 156))
        d.rectangle([x + 2, wy + 8, x + 5, wy + 8], fill=(74, 123, 156))

    # Golden Gate Bridge
    br = (192, 57, 43)
    bd = (150, 45, 34)
    d.rectangle([80, 140, 359, 145], fill=br)
    d.rectangle([80, 146, 359, 147], fill=bd)
    # Left tower
    d.rectangle([140, 40, 146, 147], fill=br)
    d.rectangle([138, 40, 139, 147], fill=bd)
    d.rectangle([136, 60, 148, 62], fill=br)
    d.rectangle([136, 90, 148, 92], fill=br)
    d.rectangle([136, 120, 148, 122], fill=br)
    # Right tower
    d.rectangle([295, 40, 301, 147], fill=br)
    d.rectangle([293, 40, 294, 147], fill=bd)
    d.rectangle([291, 60, 303, 62], fill=br)
    d.rectangle([291, 90, 303, 92], fill=br)
    d.rectangle([291, 120, 303, 122], fill=br)
    # Main cables
    for x in range(140, 299):
        t = (x - 140) / (298 - 140)
        sag = 80 * (t - 0.5) ** 2 * 4 - 80 + 42
        cy = int(40 + sag * 0.6)
        d.rectangle([x, cy, x, cy + 1], fill=br)
    # Suspender cables
    for x in range(150, 295, 10):
        t = (x - 140) / (298 - 140)
        sag = 80 * (t - 0.5) ** 2 * 4 - 80 + 42
        cy = int(40 + sag * 0.6)
        for y in range(cy, 140, 2):
            d.point((x, y), fill=bd)

    # Near hills
    for x in range(W):
        h3 = int(math.sin(x * 0.015 + 3) * 10 + H - 35)
        d.rectangle([x, h3, x, H - 1], fill=(74, 122, 58))

    # Ground
    d.rectangle([0, H - 30, W - 1, H - 1], fill=(90, 138, 74))
    return img

# ============================================================
# BERLIN
# ============================================================
def draw_berlin():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)

    gradient_sky(d, [
        (0, (120, 135, 155)),
        (0.3, (140, 155, 170)),
        (0.6, (160, 170, 185)),
        (1.0, (150, 160, 170)),
    ])

    # Cloud layer
    for x in range(0, W, 4):
        cy = int(20 + math.sin(x * 0.02) * 8)
        d.rectangle([x, cy, x + 3, cy + 2], fill=(170, 180, 195))

    # TV Tower
    tvx = 380
    d.rectangle([tvx, 8, tvx + 1, 187], fill=(138, 138, 138))
    for dy in range(-6, 7):
        w = int(math.sqrt(max(0, 36 - dy * dy)) * 2)
        if w > 0:
            d.rectangle([tvx + 1 - w // 2, 65 + dy, tvx + 1 + w // 2, 65 + dy], fill=(160, 160, 160))
    d.rectangle([tvx - 4, 62, tvx + 5, 63], fill=(176, 176, 176))
    d.rectangle([tvx, 2, tvx, 9], fill=(153, 153, 153))

    # Far buildings
    for x in range(0, W, 24):
        h = 30 + ((x * 11 + 5) % 40)
        by = H - 35 - h
        d.rectangle([x, by, x + 19, H - 36], fill=(122, 122, 122))
        draw_windows(d, x, by, 20, h, (204, 204, 170), (90, 90, 90))

    # Mid buildings
    for x in range(8, W, 30):
        h = 40 + ((x * 7 + 13) % 45)
        by = H - 33 - h
        is_modern = (x % 60) < 30
        d.rectangle([x, by, x + 25, H - 34], fill=(106, 106, 106) if is_modern else (154, 144, 128))
        if not is_modern:
            d.rectangle([x - 1, by - 2, x + 26, by], fill=(176, 160, 144))
        draw_windows(d, x, by, 26, h, (221, 221, 187), (74, 74, 74), spacing=6, win_h=3)

    # Brandenburg Gate
    gx, gBase = 180, H - 33
    stone = (212, 197, 160)
    stone_dk = (176, 160, 128)
    d.rectangle([gx - 5, gBase - 2, gx + 84, gBase + 1], fill=stone_dk)
    for i in range(6):
        d.rectangle([gx + i * 14 + 2, gBase - 68, gx + i * 14 + 7, gBase - 1], fill=stone)
        d.rectangle([gx + i * 14 + 1, gBase - 68, gx + i * 14 + 1, gBase - 1], fill=stone_dk)
    d.rectangle([gx - 2, gBase - 73, gx + 83, gBase - 68], fill=stone)
    d.rectangle([gx - 3, gBase - 75, gx + 84, gBase - 73], fill=stone_dk)
    d.rectangle([gx + 5, gBase - 82, gx + 76, gBase - 76], fill=stone)
    d.rectangle([gx + 28, gBase - 92, gx + 53, gBase - 83], fill=(184, 160, 96))
    d.rectangle([gx + 36, gBase - 98, gx + 45, gBase - 93], fill=(184, 160, 96))
    d.rectangle([gx + 22, gBase - 90, gx + 29, gBase - 86], fill=(168, 144, 80))
    d.rectangle([gx + 52, gBase - 90, gx + 59, gBase - 86], fill=(168, 144, 80))

    # Bare trees
    for tx in [40, 130, 350, 440]:
        d.rectangle([tx + 2, H - 55, tx + 3, H - 36], fill=(90, 74, 58))
        d.rectangle([tx, H - 58, tx + 5, H - 56], fill=(106, 90, 74))
        d.rectangle([tx - 2, H - 62, tx, H - 61], fill=(90, 74, 58))
        d.rectangle([tx + 5, H - 60, tx + 7, H - 59], fill=(90, 74, 58))

    # Ground
    d.rectangle([0, H - 33, W - 1, H - 1], fill=(122, 122, 106))
    for x in range(0, W, 12):
        d.rectangle([x, H - 33, x, H - 1], fill=(106, 106, 90))
    return img

# ============================================================
# TOKYO
# ============================================================
def draw_tokyo():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)

    gradient_sky(d, [
        (0, (30, 15, 70)),
        (0.25, (80, 30, 100)),
        (0.5, (180, 70, 140)),
        (0.75, (230, 110, 90)),
        (1.0, (255, 180, 80)),
    ])

    # Stars
    for sx, sy in [(30,12),(85,25),(150,8),(210,30),(280,15),(340,5),(400,22),(450,10),(50,40),(380,38)]:
        d.point((sx, sy), fill=(255, 255, 255))

    # Far skyline
    for x in range(0, W, 14):
        h = 35 + ((x * 13 + 7) % 55)
        by = H - 35 - h
        d.rectangle([x, by, x + 11, H - 31], fill=(26, 26, 46))
        for wy in range(by + 5, H - 35, 5):
            for wx in range(x + 2, x + 10, 4):
                if random.random() > 0.5:
                    d.rectangle([wx, wy, wx, wy + 1], fill=(255, 224, 102))

    # Mid skyline
    neon_colors = [(255, 105, 180), (0, 191, 255), (57, 255, 20)]
    sign_colors = [(255, 20, 147), (0, 206, 209), (255, 69, 0), (127, 255, 0)]
    for x in range(3, W, 18):
        h = 45 + ((x * 11 + 3) % 60)
        by = H - 33 - h
        d.rectangle([x, by, x + 14, H - 29], fill=(18, 18, 42))
        for wy in range(by + 5, H - 33, 4):
            for wx in range(x + 2, x + 13, 3):
                if random.random() > 0.3:
                    neon = random.random() > 0.85
                    c = random.choice(neon_colors) if neon else (255, 224, 102)
                    d.rectangle([wx, wy, wx + 1, wy + 1], fill=c)
        if random.random() > 0.6:
            ny = by + 8
            nc = random.choice(sign_colors)
            d.rectangle([x + 2, ny, x + 11, ny + 3], fill=nc)

    # Near buildings
    for x in range(-5, W, 22):
        h = 55 + ((x * 17 + 11) % 50)
        by = H - 30 - h
        d.rectangle([x, by, x + 18, H - 26], fill=(13, 13, 32))
        for wy in range(by + 5, H - 30, 5):
            for wx in range(x + 2, x + 17, 4):
                if random.random() > 0.25:
                    d.rectangle([wx, wy, wx + 1, wy + 2], fill=(255, 224, 102))

    # Tokyo Tower
    tx, tBase = 85, H - 30
    for y in range(15, tBase):
        t = (y - 15) / (tBase - 15)
        spread = int(t * 22)
        is_white = ((y - 15) % 16) < 4
        col = (255, 255, 255) if is_white else (255, 68, 68)
        d.rectangle([tx - spread - 2, y, tx - spread, y], fill=col)
        d.rectangle([tx + spread, y, tx + spread + 2, y], fill=col)
    for i in range(7):
        y = 40 + i * 25
        t = (y - 15) / (tBase - 15)
        spread = int(t * 22)
        is_white = (i % 2) == 0
        col = (255, 255, 255) if is_white else (255, 68, 68)
        d.rectangle([tx - spread, y, tx + spread + spread - 1, y + 1], fill=col)
    d.rectangle([tx - 16, 80, tx + 15, 83], fill=(255, 68, 68))
    d.rectangle([tx - 10, 50, tx + 9, 52], fill=(255, 255, 255))
    d.rectangle([tx - 1, 5, tx, 14], fill=(255, 68, 68))
    d.rectangle([tx, 2, tx, 5], fill=(255, 255, 255))

    # Cherry blossom branch
    d.rectangle([360, 70, 439, 71], fill=(74, 42, 26))
    d.rectangle([360, 68, 361, 71], fill=(74, 42, 26))
    d.rectangle([400, 65, 401, 71], fill=(74, 42, 26))
    d.rectangle([430, 62, 431, 71], fill=(74, 42, 26))
    blossom_colors = [(255, 183, 197), (255, 154, 174), (255, 204, 213), (255, 143, 163)]
    for _ in range(40):
        bx = int(355 + random.random() * 100)
        by = int(52 + random.random() * 25)
        d.rectangle([bx, by, bx + 2, by + 2], fill=random.choice(blossom_colors))
    for _ in range(8):
        px = int(370 + random.random() * 90)
        py = int(80 + random.random() * 60)
        d.rectangle([px, py, px + 1, py + 1], fill=(255, 183, 197))

    # Ground
    d.rectangle([0, H - 30, W - 1, H - 1], fill=(26, 26, 46))
    return img

# ============================================================
# RIO
# ============================================================
def draw_rio():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)

    gradient_sky(d, [
        (0, (30, 120, 220)),
        (0.4, (80, 170, 240)),
        (0.7, (140, 210, 250)),
        (1.0, (180, 230, 250)),
    ])

    # Clouds
    for cx, cy, w in [(50, 35, 40), (200, 25, 30), (380, 40, 35)]:
        d.rectangle([cx, cy, cx + w - 1, cy + 5], fill=(240, 240, 255))
        d.rectangle([cx + 4, cy - 4, cx + w - 5, cy - 1], fill=(235, 235, 250))
        d.rectangle([cx + 8, cy - 7, cx + w - 9, cy - 5], fill=(230, 230, 245))

    # Distant mountains
    for x in range(200):
        mh = int(math.sin(x * 0.02 + 1) * 20 + math.sin(x * 0.01) * 30 + 120)
        d.rectangle([x, mh, x, H - 1], fill=(58, 138, 90))

    # Sugarloaf
    for x in range(80, 180):
        t = (x - 80) / 100
        mh = int(80 - math.sin(t * math.pi) * 55)
        d.rectangle([x, mh, x, H - 1], fill=(46, 139, 87))
        if mh < 60:
            d.rectangle([x, mh, x, mh + 1], fill=(58, 155, 103))

    # Corcovado
    for x in range(280, 430):
        t = (x - 280) / 150
        mh = int(30 + (1 - math.sin(t * math.pi)) * 110)
        d.rectangle([x, mh, x, H - 1], fill=(46, 139, 87))
    for x in range(300, 420, 4):
        t = (x - 280) / 150
        mh = int(30 + (1 - math.sin(t * math.pi)) * 110)
        d.rectangle([x, mh + 5, x + 2, mh + 8], fill=(38, 138, 74))

    # Christ the Redeemer
    cx, cy = 355, 28
    d.rectangle([cx, cy + 4, cx + 3, cy + 19], fill=(232, 232, 232))
    d.rectangle([cx - 12, cy + 6, cx + 15, cy + 8], fill=(232, 232, 232))
    d.rectangle([cx, cy, cx + 3, cy + 4], fill=(232, 232, 232))
    d.rectangle([cx + 1, cy - 1, cx + 2, cy], fill=(216, 216, 216))
    d.rectangle([cx + 1, cy + 12, cx + 2, cy + 17], fill=(208, 208, 208))

    # Ocean
    d.rectangle([0, H - 60, W - 1, H - 36], fill=(30, 144, 255))
    for x in range(0, W, 6):
        wy = H - 58 + ((x * 3) % 18)
        d.rectangle([x, wy, x + 3, wy], fill=(58, 160, 255))
    for x in range(0, 280, 8):
        d.rectangle([x, H - 37, x + 4, H - 37], fill=(255, 255, 255))

    # Beach
    d.rectangle([0, H - 38, 279, H - 31], fill=(244, 227, 178))
    for x in range(0, 280, 5):
        d.rectangle([x, H - 36, x + 1, H - 36], fill=(232, 216, 162))

    # Palm trees
    for px_base, py in [(20, H - 85), (450, H - 75)]:
        for y in range(py, H - 30):
            sway = int(math.sin(y * 0.05) * 2)
            d.rectangle([px_base + sway, y, px_base + sway + 2, y], fill=(90, 58, 26))
        for i in range(6):
            angle = (i / 6) * math.pi * 2
            for dd in range(20):
                fx = int(px_base + math.cos(angle) * dd)
                fy = int(py - 2 + math.sin(angle) * dd * 0.5 + dd * 0.3)
                d.rectangle([fx, fy, fx + 1, fy], fill=(42, 106, 42) if dd < 15 else (58, 138, 58))

    # Ground
    d.rectangle([0, H - 30, W - 1, H - 1], fill=(107, 142, 90))
    return img

# ============================================================
# NEW YORK
# ============================================================
def draw_new_york():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)

    gradient_sky(d, [
        (0, (200, 80, 30)),
        (0.3, (240, 140, 60)),
        (0.5, (255, 190, 90)),
        (0.7, (255, 210, 130)),
        (1.0, (200, 180, 150)),
    ])

    # Clouds
    for cx, cy in [(80, 30), (300, 20), (420, 40)]:
        d.rectangle([cx, cy, cx + 24, cy + 3], fill=(255, 210, 165))
        d.rectangle([cx + 5, cy - 3, cx + 19, cy - 1], fill=(255, 210, 165))

    # Far skyline
    for x in range(0, W, 18):
        h = 40 + ((x * 13 + 7) % 50)
        by = H - 45 - h
        d.rectangle([x, by, x + 14, H - 46], fill=(58, 58, 58))
        draw_windows(d, x, by, 15, h, (255, 224, 102), (42, 42, 42))

    # Mid buildings
    for x in range(5, W, 24):
        h = 50 + ((x * 7 + 11) % 65)
        by = H - 43 - h
        d.rectangle([x, by, x + 19, H - 40], fill=(44, 44, 44))
        if h > 80:
            d.rectangle([x + 5, by - 5, x + 14, by - 1], fill=(44, 44, 44))
            d.rectangle([x + 7, by - 8, x + 12, by - 6], fill=(44, 44, 44))
        draw_windows(d, x, by, 20, h, (255, 224, 102), (26, 26, 26))

    # Empire State Building
    esx, esBase = 200, H - 40
    d.rectangle([esx, esBase - 150, esx + 21, esBase - 1], fill=(44, 44, 44))
    d.rectangle([esx + 4, esBase - 165, esx + 17, esBase - 151], fill=(44, 44, 44))
    d.rectangle([esx + 7, esBase - 175, esx + 14, esBase - 166], fill=(44, 44, 44))
    d.rectangle([esx + 10, esBase - 195, esx + 11, esBase - 176], fill=(60, 60, 60))
    d.rectangle([esx + 10, esBase - 200, esx + 10, esBase - 193], fill=(76, 76, 76))
    d.rectangle([esx - 1, esBase - 150, esx + 22, esBase - 149], fill=(60, 60, 60))
    d.rectangle([esx + 3, esBase - 165, esx + 18, esBase - 164], fill=(60, 60, 60))
    for wy in range(esBase - 148, esBase, 4):
        for wx in range(esx + 2, esx + 20, 3):
            if random.random() > 0.2:
                d.rectangle([wx, wy, wx + 1, wy + 1], fill=(255, 224, 102))

    # Freedom Tower
    wtcx = 320
    d.rectangle([wtcx, esBase - 140, wtcx + 15, esBase - 1], fill=(58, 74, 90))
    d.rectangle([wtcx + 4, esBase - 155, wtcx + 11, esBase - 141], fill=(58, 74, 90))
    d.rectangle([wtcx + 6, esBase - 165, wtcx + 9, esBase - 156], fill=(58, 74, 90))
    d.rectangle([wtcx + 7, esBase - 175, wtcx + 8, esBase - 166], fill=(74, 90, 106))
    for wy in range(esBase - 138, esBase, 3):
        d.rectangle([wtcx + 1, wy, wtcx + 14, wy], fill=(74, 106, 138))

    # Near buildings
    for x in range(-3, W, 28):
        if abs(x - esx) < 30 or abs(x - wtcx) < 20:
            continue
        h = 60 + ((x * 19 + 5) % 55)
        by = H - 38 - h
        d.rectangle([x, by, x + 23, H - 39], fill=(34, 34, 34))
        draw_windows(d, x, by, 24, h, (255, 224, 102), (17, 17, 17))

    # East River
    d.rectangle([0, H - 42, W - 1, H - 31], fill=(42, 74, 106))
    for x in range(0, W, 6):
        d.rectangle([x, H - 40, x + 2, H - 40], fill=(180, 160, 80))
        d.rectangle([x + 2, H - 36, x + 3, H - 36], fill=(160, 140, 70))

    # Ground
    d.rectangle([0, H - 30, W - 1, H - 1], fill=(74, 74, 74))
    for x in range(0, W, 8):
        d.rectangle([x, H - 30, x, H - 28], fill=(90, 90, 90))
    return img

# ============================================================
# GENERATE ALL
# ============================================================
if __name__ == '__main__':
    generators = [
        ('paris', draw_paris),
        ('san_francisco', draw_san_francisco),
        ('berlin', draw_berlin),
        ('tokyo', draw_tokyo),
        ('rio', draw_rio),
        ('new_york', draw_new_york),
    ]
    for name, func in generators:
        print(f'Generating {name}...')
        img = func()
        path = os.path.join(OUT_DIR, f'{name}.png')
        img.save(path, 'PNG', optimize=True)
        size = os.path.getsize(path)
        print(f'  Saved {path} ({size} bytes)')
    print('Done!')
