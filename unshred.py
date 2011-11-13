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
    '''Returns differences between colors'''
    if type(c1) == type(1):
        return c1 - c2
    return tuple([x-y for x, y in zip(c1, c2)])

def rms(cdiff):
    '''root-mean-square

    Not to be confused with the founder of the Free Software
    Foundation.'''
    if type(cdiff) == type(1): return cdiff
    return sqrt(sum(x*x for x in cdiff))

def right_diff(s1, s2):
    ## sufficient to match last column of s1 and first column of s2
    w, h = s1.size

    s1_col_ends = [s1.getpixel((w-1, i)) for i in xrange(h)]
    s2_col_ends = [s2.getpixel((0, i)) for i in xrange(h)]

    cdiffs = [color_diff(c1, c2) for c1, c2 in zip(s1_col_ends, s2_col_ends)]
    return sum([rms(cdiff) for cdiff in cdiffs])

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

    matrix = [[right_diff(cols[i], cols[j]) for j in idxs] for i in idxs]
    for i in idxs: matrix[i][i] = INFINITY # by definition

    graph = idxs[::]         # copy, don't recompute
    for i in idxs:
        row = matrix[i]
        closest = min(row)
        rneighbor = row.index(closest)
        graph[i] = (i, rneighbor)

    print graph
    ograph = []                 # ordered graph
    start = 0
    for i in xrange(num_cols):
        ograph += [start]
        start = graph[start][1]

    print ograph

    ## step 3, merge columns
    for i, k in enumerate(ograph):
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
