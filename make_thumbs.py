"""Make the small card images the gallery shows.

Each entry's image_src (a URL, or a path in this repo) is downloaded once and
saved as an 800px-wide WebP in assets/img/thumbs/<card id>.webp -- a card is
about 350px wide, 700px on a high-density screen. Animated GIFs keep their
first frame. assets/img/thumbs/thumbs.json records each thumbnail's source and
size, so generate_html.py can use the thumbnails without needing Pillow, and
this script only redoes entries whose image_src changed.

    pip install Pillow
    python3 make_thumbs.py            # new or changed entries
    python3 make_thumbs.py --force    # all of them

Commit the thumbnails and thumbs.json with the showcases.json change.
"""
import argparse
import io
import json
import os
import urllib.request

from PIL import Image

from generate_html import convert_to_html_id

WIDTH = 800
QUALITY = 80
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, 'assets', 'img', 'thumbs')
MANIFEST = os.path.join(OUT_DIR, 'thumbs.json')


def read_source(src):
    if src.startswith(('http://', 'https://')):
        req = urllib.request.Request(src, headers={'User-Agent': 'madewithslint-thumbnails'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    with open(os.path.join(HERE, src), 'rb') as f:
        return f.read()


def make_thumb(data, dest):
    img = Image.open(io.BytesIO(data))
    img.seek(0)  # first frame of an animated GIF
    img = img.convert('RGBA' if img.mode in ('RGBA', 'LA', 'P') else 'RGB')
    if img.width > WIDTH:
        img = img.resize((WIDTH, round(img.height * WIDTH / img.width)), Image.LANCZOS)
    img.save(dest, 'WEBP', quality=QUALITY, method=6)
    return img.width, img.height


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--json', default=os.path.join(HERE, 'showcases.json'))
    parser.add_argument('--force', action='store_true', help='remake every thumbnail')
    args = parser.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = {}
    if os.path.exists(MANIFEST) and not args.force:
        with open(MANIFEST, encoding='utf-8') as f:
            manifest = json.load(f)

    entries = json.load(open(args.json, encoding='utf-8'))
    wanted = set()
    for app in entries:
        card_id = convert_to_html_id(app['app_title'])
        src = app.get('image_src', '').strip()
        if not src:
            continue
        wanted.add(card_id)
        dest = os.path.join(OUT_DIR, card_id + '.webp')
        known = manifest.get(card_id)
        if known and known['source'] == src and os.path.exists(dest):
            continue
        try:
            width, height = make_thumb(read_source(src), dest)
        except Exception as e:  # keep going; the card falls back to image_src
            print(f'{app["app_title"]}: could not make a thumbnail from {src}: {e}')
            continue
        manifest[card_id] = {'source': src, 'width': width, 'height': height}
        print(f'{app["app_title"]}: {width}x{height}, {os.path.getsize(dest) // 1024} KB')

    # drop thumbnails of entries that are gone
    for card_id in list(manifest):
        if card_id not in wanted:
            manifest.pop(card_id)
            path = os.path.join(OUT_DIR, card_id + '.webp')
            if os.path.exists(path):
                os.remove(path)

    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(manifest.items())), f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
