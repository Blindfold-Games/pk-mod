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

def main(font):
    cwd = os.getcwd()
    os.chdir(HOME)
    try:
        repack('', (20, 32, 40, 48, '51r', '51o'), font)
        repack('-xhdpi', (33, 60, 72, 85, '78r', '78o'), font)
        repack('-xxhdpi', (50, 85, 103, 121, '115r', '115o'), font)
        if os.path.exists('res/fonts/%s/coda.ttf' % font):
            if not os.path.exists('build/assets/fonts'):
                os.makedirs('build/assets/fonts')
            shutil.copy('res/fonts/%s/coda.ttf' % font, 'build/assets/fonts/coda.ttf')
    finally:
        os.chdir(cwd)


def repack(name, font_sizes, font='coda'):
    shutil.rmtree('build/assets/data%s' % name, ignore_errors=True)

    # Create dirs
    for f in 'common', 'packed', 'portal_info', 'upgrade':
        os.makedirs('build/assets/data%s/%s' % (name, f))

    # Copy some files
    for f in 'inconsolata-14.fnt', 'inconsolata-14.png', 'inconsolata-28.fnt', 'inconsolata-28.png':
        shutil.copy('app/assets/common/data%s/%s' % (name, f), 'build/assets/data%s/common' % name)

    shutil.copy('app/assets/common/data%s/nemesis.json' % name, 'build/assets/data%s/common/nemesis.json' % name)

    # Copy upgrade/data*/* images
    if os.path.exists('app/assets/upgrade/data%s' % name):
        for f in os.listdir('app/assets/upgrade/data%s' % name):
            shutil.copy('app/assets/upgrade/data%s/%s' % (name, f), 'build/assets/data%s/upgrade/%s' % (name, f))

    # Repack atlases (replace fonts)
    d = tempfile.mkdtemp()
    texture_unpacker.Unpacker('app/assets/%s/data%s/%s.atlas' % ('packed', name, 'common')).unpack(d, 1)
    # For common.atlas copy fonts
    for size, font_name in zip(font_sizes, ('x-small', 'sm', 'med', 'lg', 'outline-red-med', 'outline-orange-med')):
        shutil.copy('res/fonts/%s/coda-%s.fnt' % (font, size),
                    'build/assets/data%s/common/coda-%s.fnt' % (name, font_name))
        shutil.copy('res/fonts/%s/coda-%s_0.png' % (font, size), '%s/coda-%s.png' % (d, font_name))

    shutil.copy('res/lowres/%s-pack.json' % 'common', '%s/pack.json' % d)
    texture_pack(d, 'build/assets/data%s/%s' % (name, 'packed'), 'common')
    texture_unpacker.reprocess_atlas('app/assets/%s/data%s/%s.atlas' % ('packed', name, 'common'), 'build/assets/data%s/%s/%s.atlas' % (name, 'packed', 'common'), 1.0)
    shutil.rmtree(d)

    shutil.copy('app/assets/portal_info/data%s/portal_ui.atlas' % name, 'build/assets/data%s/portal_info/portal_ui.atlas' % name)
    shutil.copy('app/assets/portal_info/data%s/portal_ui.png' % name, 'build/assets/data%s/portal_info/portal_ui.png' % name)

def texture_pack(in_dir, out_dir, name):
    subprocess.check_call(
        'java -cp lib/gdx.jar:lib/gdx-tools.jar com.badlogic.gdx.tools.imagepacker.TexturePacker2 %s %s %s' % (
            in_dir, out_dir, name), shell=True)


def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return filter(pred, t2), filterfalse(pred, t1)


if __name__ == '__main__':
    main('coda' if len(sys.argv) < 2 else sys.argv[1])
