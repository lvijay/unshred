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

def color_diff(c1, c2):
    '''Returns difference between two colors'''
    return tuple([x-y for x, y in zip(c1, c2)])

def rms(cdiff):
    '''Root Mean Square

    Not to be confused with that GNU geek.'''
    return sqrt(sum(x*x for x in cdiff))

def diff(s1, s2):
    ## sufficient to match last column of s1 and first column of s2
    w, h = s1.size

    s1_right = [s1.getpixel((w-1, i)) for i in xrange(h)]
    s1_left = [s1.getpixel((0, i)) for i in xrange(h)]

    s2_left = [s2.getpixel((0, i)) for i in xrange(h)]
    s2_right = [s2.getpixel((w-1, i)) for i in xrange(h)]

    rldiffs = [color_diff(c1, c2) for c1, c2 in zip(s1_right, s2_left)]
    lrdiffs = [color_diff(c1, c2) for c1, c2 in zip(s1_left, s2_right)]

    rldiff = sum([rms(diff) for diff in rldiffs])
    lrdiff = sum([rms(diff) for diff in lrdiffs])

    return (rldiff, lrdiff)

def unshred(src):
    '''unshred(shredded_img) -> unshredded_img'''
    result = Image.new(image.mode, image.size)

    width, height = image.size
    col_size = 32               # assume

    ## step 1, find columns
    num_cols = width / col_size # assume integer

    cs = col_size
    cols = [src.crop((i*cs, 0, (i+1)*cs, height)) for i in xrange(num_cols)]

    ## step 2, find matching columns
    idxs = range(num_cols)      # cache

    matrix = [[diff(cols[i], cols[j]) for j in idxs] for i in idxs]
    for i in idxs: matrix[i][i] = (INFINITY, INFINITY) # by definition

    rmatrix = [[matrix[i][j][0] for j in idxs] for i in idxs]
    lmatrix = [[matrix[i][j][1] for j in idxs] for i in idxs]

    rgraph = idxs[::]         # copy, don't recompute
    lgraph = idxs[::]
    for i in idxs:
        row = rmatrix[i]
        closest = min(row)
        neighbor = row.index(closest)
        rgraph[i] = (i, neighbor, closest)

        row = lmatrix[i]
        closest = min(row)
        neighbor = row.index(closest)
        lgraph[i] = (i, neighbor, closest)

    orgraph = []                # ordered right graph
    olgraph = []                # ordered left graph
    lstart = 0
    rstart = 0
    for i in xrange(num_cols):
        orgraph += [rstart]
        olgraph += [lstart]
        rstart = rgraph[rstart][1]
        lstart = lgraph[lstart][1]

    print orgraph
    print olgraph[::-1]

    ## step 3, merge columns
    for i, k in enumerate(orgraph):
        result.paste(cols[k], (i*col_size, 0))

    return result

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        saveto = sys.argv[2]

        image = Image.open(filename)
        unshredded_image = unshred(image)
        unshredded_image.save(saveto)
    except IndexError:
        print >> sys.stderr, ('Usage: %s [source_image] [dest_image]'
                              % sys.argv[0])
        exit(1)
    except IOError, e:
        print >> sys.stderr, e
        exit(2)
    finally:
        pass

# unshred.py ends here
