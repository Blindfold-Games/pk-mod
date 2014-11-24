#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys
import tempfile
from itertools import tee, filterfalse
from PIL import Image

from common import HOME
import texture_unpacker


PAT_NEMESIS_COMPASS = re.compile(
'''^    compass: \{
      height: ([\d.]+),
      width: ([\d.]+),
      x: ([\d.]+),
      y: ([\d.]+)
    }$''', re.MULTILINE)


def main(font):
    cwd = os.getcwd()
    os.chdir(HOME)
    try:
        resize('hvga', .6, (20, 24, 30, 36, '39r', '39o'), font)
        resize('qvga', .4, (16, 16, 20, 24, '27r', '27o'), font)
    finally:
        os.chdir(cwd)


def resize(name, scale, coda_sizes, font='coda'):
    shutil.rmtree('build/assets/data-%s' % name, ignore_errors=True)

    # Create dirs
    for f in 'common', 'packed', 'portal_info', 'upgrade', 'levelup', 'verify':
        os.makedirs('build/assets/data-%s/%s' % (name, f))

    # Copy some files
    for f in 'inconsolata-14.fnt', 'inconsolata-14.png', 'inconsolata-28.fnt', 'inconsolata-28.png':
        shutil.copy('app/assets/common/data/%s' % f, 'build/assets/data-%s/common' % name)
    shutil.copy('app/assets/portal_info/data/portal_ui.json', 'build/assets/data-%s/portal_info' % name)

    # nemesis.json
    def _repl(m):
        return \
'''    compass: {
      height: %d.0,
      width: %d.0,
      x: %d.0,
      y: %d.0
    }''' % tuple([round(float(m.group(i)) * scale) for i in range(1, 5)])

    s = open('app/assets/common/data/nemesis.json').read()
    s = PAT_NEMESIS_COMPASS.sub(_repl, s, 1)
    open('build/assets/data-%s/common/nemesis.json' % name, 'w').write(s)

    # Resize upgrade/data*/* images
    for f in os.listdir('app/assets/upgrade/data'):
        im = Image.open('app/assets/upgrade/data/%s' % f)
        im.resize((round(im.size[0] * scale), round(im.size[1] * scale)), Image.ANTIALIAS).save(
            'build/assets/data-%s/upgrade/%s' % (name, f))

    # Resize levelup/data*/* images
    for f in os.listdir('app/assets/levelup/data'):
        im = Image.open('app/assets/levelup/data/%s' % f)
        im.resize((round(im.size[0] * scale), round(im.size[1] * scale)), Image.ANTIALIAS).save(
            'build/assets/data-%s/levelup/%s' % (name, f))

    # Resize verify/data*/* images
    for f in os.listdir('app/assets/verify/data'):
        im = Image.open('app/assets/verify/data/%s' % f)
        im.resize((round(im.size[0] * scale), round(im.size[1] * scale)), Image.ANTIALIAS).save(
            'build/assets/data-%s/verify/%s' % (name, f))

    # Resize atlases
    d = tempfile.mkdtemp()
    texture_unpacker.Unpacker('app/assets/%s/data/%s.atlas' % ('packed', 'common')).unpack(d, scale)
    # For common.atlas copy fonts
    for size, font_name in zip(coda_sizes, ('x-small', 'sm', 'med', 'lg', 'outline-red-med', 'outline-orange-med')):
        shutil.copy('res/fonts/%s/coda-%s.fnt' % (font, size),
                    'build/assets/data-%s/common/coda-%s.fnt' % (name, font_name))
        shutil.copy('res/fonts/%s/coda-%s_0.png' % (font, size), '%s/coda-%s.png' % (d, font_name))

    shutil.copy('res/lowres/%s-pack.json' % 'common', '%s/pack.json' % d)
    texture_pack(d, 'build/assets/data-%s/%s' % (name, 'packed'), 'common')
    texture_unpacker.reprocess_atlas('app/assets/%s/data/%s.atlas' % ('packed', 'common'), 'build/assets/data-%s/%s/%s.atlas' % (name, 'packed', 'common'), scale)
    shutil.rmtree(d)

    # Resize "magic" portal_ui.atlas
    # Repack portal, energy-alien and energy-resistance images only, then readd additional "images" to the atlas file
    u = texture_unpacker.Unpacker('app/assets/portal_info/data/portal_ui.atlas')
    u.parse_atlas()
    page = u.atlas.pages[0]
    page.images, images2 = partition(lambda im: im.name in ('portal', 'energy-alien', 'energy-resistance'), page.images)
    page.images = list(page.images)
    d = tempfile.mkdtemp()
    u.unpack(d, scale)
    shutil.copy('res/lowres/portal_ui-pack.json', '%s/pack.json' % d)
    texture_pack(d, 'build/assets/data-%s/portal_info' % name, 'portal_ui')

    u = texture_unpacker.Unpacker('build/assets/data-%s/portal_info/portal_ui.atlas' % name)
    u.parse_atlas()
    page = u.atlas.pages[0]
    for im in images2:
        p = im.params
        p['xy'] = round(p['xy'][0] * scale), round(p['xy'][1] * scale)
        p['size'] = round(p['size'][0] * scale), round(p['size'][1] * scale)
        p['orig'] = round(p['orig'][0] * scale), round(p['orig'][1] * scale)
        page.images.append(im)
    u.save_atlas('build/assets/data-%s/portal_info/portal_ui.atlas' % name)

def texture_pack(in_dir, out_dir, name):
    subprocess.check_call(
        'java -cp lib/gdx.jar:lib/gdx-tools.jar com.badlogic.gdx.tools.imagepacker.TexturePacker2 %s %s %s' % (
            in_dir, out_dir, name), shell=True)


def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return filter(pred, t2), filterfalse(pred, t1)

if __name__ == '__main__':
    main('coda' if len(sys.argv) < 2 else sys.argv[1])
