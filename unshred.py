#!/usr/bin/env python
# -*- coding: utf-8 -*-

## unshred - form original image from an image uniformly shredded into
##           columns
##
## Copyright © 2011, Vijay Lakshminarayanan <laksvij@gmail.com>

import sys
from PIL import Image

def unshred(src):
    # for now, just create a new image and return
    result = Image.new(image.mode, image.size)
    return result

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        saveto = sys.argv[2]

        image = Image.open(filename)
        unshredded_image = unshred(image)
        unshredded_image.save(saveto, 'png')
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
