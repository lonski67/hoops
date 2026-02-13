#!/usr/bin/env python3
"""
Download real city photos from Unsplash and apply a pixel art filter.
Produces 480x270 pixel-art-style backgrounds for the Hoops game.

Usage:
    python3 tools/pixelate_backgrounds.py
"""
import os
import io
import urllib.request
from PIL import Image, ImageEnhance

W, H = 480, 270
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'backgrounds')
os.makedirs(OUT_DIR, exist_ok=True)

# Each city: (filename, unsplash_photo_url, pixel_size, num_colors, saturation_boost)
# pixel_size: how many game pixels per "block" (lower = more detail)
# num_colors: palette size after quantization
# saturation_boost: multiplier for color vibrancy
CITIES = [
    {
        'key': 'paris',
        # Eiffel Tower towering over Paris cityscape at dusk
        'url': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=960&h=540&fit=crop',
        'pixel_size': 3,
        'num_colors': 48,
        'saturation': 1.3,
    },
    {
        'key': 'san_francisco',
        'url': 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=960&h=540&fit=crop',
        'pixel_size': 3,
        'num_colors': 48,
        'saturation': 1.2,
    },
    {
        'key': 'berlin',
        'url': 'https://images.unsplash.com/photo-1560969184-10fe8719e047?w=960&h=540&fit=crop',
        'pixel_size': 3,
        'num_colors': 48,
        'saturation': 1.2,
    },
    {
        'key': 'tokyo',
        # Tokyo cityscape at night with neon lights
        'url': 'https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=960&h=540&fit=crop',
        'pixel_size': 3,
        'num_colors': 64,
        'saturation': 1.4,
    },
    {
        'key': 'rio',
        'url': 'https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=960&h=540&fit=crop',
        'pixel_size': 3,
        'num_colors': 48,
        'saturation': 1.3,
    },
    {
        'key': 'new_york',
        # Manhattan skyline at sunset across the water
        'url': 'https://images.unsplash.com/photo-1518235506717-e1ed3306a89b?w=960&h=540&fit=crop',
        'pixel_size': 3,
        'num_colors': 48,
        'saturation': 1.3,
    },
]


def download_image(url):
    """Download image from URL and return as PIL Image."""
    print(f'  Downloading from Unsplash...')
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) HoopsGame/1.0'
    })
    with urllib.request.urlopen(req) as response:
        data = response.read()
    return Image.open(io.BytesIO(data))


def pixelate(img, pixel_size=6, num_colors=32, saturation_boost=1.2):
    """
    Apply pixel art filter to a photo:
    1. Crop/resize to game aspect ratio
    2. Boost saturation for vibrancy
    3. Downscale to tiny size (creates the pixel blocks)
    4. Quantize colors for retro palette
    5. Upscale back to game resolution with nearest-neighbor
    """
    # Ensure RGB mode
    img = img.convert('RGB')

    # Crop to 16:9 aspect ratio if needed
    target_ratio = W / H  # 1.778
    img_ratio = img.width / img.height
    if img_ratio > target_ratio:
        # Too wide, crop sides
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    elif img_ratio < target_ratio:
        # Too tall, crop top/bottom
        new_h = int(img.width / target_ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))

    # Resize to game resolution first
    img = img.resize((W, H), Image.LANCZOS)

    # Boost saturation
    if saturation_boost != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(saturation_boost)

    # Slightly boost contrast too
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)

    # Calculate small size for pixel blocks
    small_w = W // pixel_size
    small_h = H // pixel_size

    # Downscale (this creates the pixelation)
    img_small = img.resize((small_w, small_h), Image.LANCZOS)

    # Quantize colors for retro palette
    img_quantized = img_small.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
    img_small = img_quantized.convert('RGB')

    # Upscale back to game resolution with nearest-neighbor (crisp pixel edges)
    img_final = img_small.resize((W, H), Image.NEAREST)

    return img_final


if __name__ == '__main__':
    for city in CITIES:
        key = city['key']
        print(f'Processing {key}...')

        # Download source photo
        src = download_image(city['url'])
        print(f'  Source: {src.size[0]}x{src.size[1]}')

        # Apply pixel art filter
        result = pixelate(
            src,
            pixel_size=city['pixel_size'],
            num_colors=city['num_colors'],
            saturation_boost=city['saturation'],
        )

        # Save
        path = os.path.join(OUT_DIR, f'{key}.png')
        result.save(path, 'PNG', optimize=True)
        size = os.path.getsize(path)
        print(f'  Saved {path} ({size} bytes)')

    print('Done! All backgrounds generated.')
