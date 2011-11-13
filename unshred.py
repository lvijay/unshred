#!/usr/bin/env python

## unshred - form original image from an image uniformly shredded into
##           columns
##
## Copyright © 2011, Vijay Lakshminarayanan <laksvij@gmail.com>

import sys
from PIL import Image

def unshred(src, dest):
    # just return the source for now
    return src

if __name__ == '__main__':
    try:
        filename = sys.argv[0]
        saveto = sys.argv[1]

        image = Image.open(filename)
        unshredded_image = Image.new(image.mode, image.size)
        unshred(image, unshredded_image)
        unshredded_image.save(saveto, 'png')
    finally:
        pass

# unshred.py ends here
