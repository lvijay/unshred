#!/usr/bin/env python
# -*- coding: utf-8 -*-

## shred - shred a given image into columns of equal width strips
##
## Copyright © 2011, Vijay Lakshminarayanan <laksvij@gmail.com>

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
