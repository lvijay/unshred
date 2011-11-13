#!/usr/bin/env python
# -*- coding: utf-8 -*-

## unshred - form original image from an image uniformly shredded into
##           columns
##
## Copyright © 2011, Vijay Lakshminarayanan <laksvij@gmail.com>

import sys
from PIL import Image

def unshred(src):
    '''unshred(shredded_img) -> unshredded_img'''
    result = Image.new(image.mode, image.size)

    width, height = image.size
    col_size = 32               # assume

    ## step 1, find columns
    num_cols = width / col_size # assume integer

    cs = col_size
    strips = [src.crop((i*cs, 0, (i+1)*cs, height)) for i in xrange(num_cols)]

    ## step 2, find matching columns
    ## step 3, merge columns
    for i, strip in enumerate(strips):
        result.paste(strip, (i*col_size, 0))

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
