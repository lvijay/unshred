#!/usr/bin/env python
# -*- coding: utf-8 -*-

## shred.py - shred a given image into columns of equal width strips.
##
##            Takes some effort to ensure that adjacent strips don't
##            end up next to each other.
##
## Usage:
##
##    ./shred.py source destination [strip_width=32]
##
##    source - the input file.  Must exist.
##    destination - the destination file.  Will be created or
##                  overwritten if exists.
##
##    strip_width - the width of each column.  Taken as 32 if not
##                  provided.
##
##                  It is the users responsibility to ensure that the
##                  source.size.width is a multiple of strip_width.
##
## Copyright © 2011, Vijay Lakshminarayanan <laksvij@gmail.com>
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3, or (at
## your option) any later version.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with GNU Emacs; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
## Boston, MA 02110-1301, USA.

import sys
from PIL import Image
from random import shuffle

def shred(img, strip_width):
    width, height = img.size
    result = Image.new(img.mode, img.size)
    num_cols = width / strip_width # assume integer

    cs = strip_width
    cols = [img.crop((i*cs, 0, (i+1)*cs, height)) for i in xrange(num_cols)]

    array = []
    while True:
        array = range(num_cols)
        shuffle(array)

        if num_cols < 10: break

        ## assert no two strips are next to each other
        for x, y in zip(array, array[1:]):
            if abs(x - y) == 1: continue

        break

    for i, k in enumerate(array):
        result.paste(cols[k], (i*strip_width, 0))

    return result

def main(argv):
    try:
        filename = argv[1]
        saveto = argv[2]
        width = int(argv[3])
    except IndexError:
        print >> sys.stderr, ('Usage: %s [source] [dest] [width=32]' % argv[0])
        exit(1)

    try:
        image = Image.open(filename)
        shredded_image = shred(image, width)

        shredded_image.save(saveto)
    except IOError, e:
        print >> sys.stderr, e
        exit(2)

if __name__ == '__main__':
    main(sys.argv)

# shred.py ends here
