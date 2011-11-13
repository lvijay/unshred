#!/usr/bin/env python
# -*- coding: utf-8 -*-

## unshred - form original image from an image uniformly shredded into
##           columns
##
## Copyright © 2011, Vijay Lakshminarayanan <laksvij@gmail.com>

import sys
from PIL import Image
from math import sqrt

INFINITY = 1e308

class WImage(object):
    def __init__(self, image):
        self.image = image
        self.data = image.getdata()
        self.w = image.size[0]
    def getpixel(self, x, y):
        return self.data[self.w * y + x]

def color_diff(c1, c2):
    '''Returns difference between two colors'''
    return tuple([x-y for x, y in zip(c1, c2)])

def rms(cdiff):
    '''Root Mean Square

    Not to be confused with that GNU geek.'''
    return sqrt(sum(x*x for x in cdiff))

def diff(s1, s2):
    ## match last column of s1 and first column of s2
    ##   and first column of s1 and last column of s2
    w, h = s1.image.size

    s1_right = [s1.getpixel(w-1, i) for i in xrange(h)]
    s1_left = [s1.getpixel(0, i) for i in xrange(h)]

    s2_left = [s2.getpixel(0, i) for i in xrange(h)]
    s2_right = [s2.getpixel(w-1, i) for i in xrange(h)]

    rldiffs = [color_diff(c1, c2) for c1, c2 in zip(s1_right, s2_left)]
    lrdiffs = [color_diff(c1, c2) for c1, c2 in zip(s1_left, s2_right)]

    rldiff = sum([rms(diff) for diff in rldiffs])
    lrdiff = sum([rms(diff) for diff in lrdiffs])

    return (rldiff, lrdiff)

def unshred(src, strip_width):
    '''unshred(shredded_img) -> unshredded_img'''
    result = Image.new(src.mode, src.size)

    width, height = src.size

    ## step 1, find columns
    num_cols = width / strip_width # assume integer

    cs = strip_width
    cols = [WImage(src.crop((i*strip_width, 0, (i+1)*strip_width, height)))
            for i in xrange(num_cols)]

    ## step 2, find matching columns
    idxs = range(num_cols)      # cache

    matrix = [[diff(cols[i], cols[j]) for j in idxs] for i in idxs]
    for i in idxs: matrix[i][i] = (INFINITY, INFINITY) # by definition

    rgraph = idxs[::]         # copy, don't recompute
    lgraph = idxs[::]
    for i in idxs:
        row = matrix[i]
        rclosest = min(row, key=lambda x: x[0])
        lclosest = min(row, key=lambda x: x[1])
        rneighbor = row.index(rclosest)
        lneighbor = row.index(lclosest)
        rgraph[i] = (i, rneighbor)
        lgraph[i] = (i, lneighbor)

    # find node without a neighbor
    rfilled = idxs[::]
    lfilled = idxs[::]
    for i in idxs:
        rfilled[rgraph[i][1]] = None
        lfilled[lgraph[i][1]] = None
    left_end = filter(None, lfilled)
    right_end = filter(None, rfilled)

    if left_end: start, left_side = left_end[0], True
    elif right_end: start, left_side = right_end[0], False
    else: start, left_side = 0, False

    sgraph = lgraph if left_side else rgraph # source graph
    ograph = []                # ordered graph
    for i in xrange(num_cols):
        ograph += [start]
        start = sgraph[start][1]

    ograph = ograph[::-1] if left_side else ograph

    ## step 3, merge columns
    for i, k in enumerate(ograph):
        result.paste(cols[k].image, (i*strip_width, 0))

    return result

def main(argv):
    try:
        filename = argv[1]
        saveto = argv[2]
        strip_width = 32 if len(argv) <= 3 else int(argv[3])
    except IndexError:
        print >> sys.stderr, ('Usage: %s [source] [dest] [width=32]' % argv[0])
        exit(1)

    try:
        image = Image.open(filename)
        unshredded_image = unshred(image, strip_width)

        unshredded_image.save(saveto)
    except IOError, e:
        print >> sys.stderr, e
        exit(2)

if __name__ == '__main__':
    main(sys.argv)

# unshred.py ends here
