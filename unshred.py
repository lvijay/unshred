#!/usr/bin/env python
# -*- coding: utf-8 -*-

## unshred.py - form the original image from an image shredded into
##              uniform vertical columns.
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
##                  If the width is not the actual strip width, expect
##                  failures.
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
    return sqrt(sum((x*x for x in cdiff)))

def diff(s1, s2):
    ## match last column of s1 with first column of s2
    w, h = s1.image.size

    s1_right = [s1.getpixel(w-1, i) for i in xrange(h)]
    s2_left = [s2.getpixel(0, i) for i in xrange(h)]

    diffs = [color_diff(c1, c2) for c1, c2 in zip(s1_right, s2_left)]
    diff = sum([rms(diff) for diff in diffs])
    return diff

def order(matrix):
    idxs = range(len(matrix))
    matrix = [[(c, i) for i, c in enumerate(row)] for row in matrix]
    def find_order(start, row, path=[], cost_path=[]):
        if len(path) == len(idxs): return path, cost_path
        while True:             # optimize this loop
            best, nxt = min(row)
            if nxt == start: break
            if nxt in path: row[nxt] = (INFINITY, nxt)
            else: break
        start = nxt
        return find_order(nxt, row, path + [start], cost_path + [best])

    ## find all optimal paths starting from each index
    ## the cheapest optimal path is the best
    orders = [find_order(i, matrix[i]) for i in idxs]
    paths = [ordr[0] for ordr in orders]
    costs = [ordr[1] for ordr in orders]
    print paths

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
    for i in idxs: matrix[i][i] = INFINITY # by definition

    order(matrix)

    ## step 3, merge columns
    # TODO

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
