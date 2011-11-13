#!/usr/bin/env python
# -*- coding: utf-8 -*-

## shred - shred a given image into columns of equal width strips
##
## Copyright © 2011, Vijay Lakshminarayanan <laksvij@gmail.com>

import sys
from PIL import Image
from random import shuffle
from math import abs

def shred(img, width):
    result = Image.new(image.mode, image.size)
    num_cols = width / strip_width # assume integer

    cs = strip_width
    cols = [src.crop((i*cs, 0, (i+1)*cs, height)) for i in xrange(num_cols)]

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
        result.paste(cols[k], (i*width, 0))

    return result

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        saveto = sys.argv[2]
        strip_width = 32 if len(sys.argv) < 3 else int(sys.argv[3])
    except IndexError:
        print >> sys.stderr, ('Usage: %s [source] [dest] [width=32]' % sys.argv[0])
        exit(1)

    try:
        image = Image.open(filename)
        shredded_image = shred(image, strip_width)

        shredded_image.save(saveto)
    except IOError, e:
        print >> sys.stderr, e
        exit(2)

# shred.py ends here
