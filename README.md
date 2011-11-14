My solution to the Unshredder problem posted by Instagram. [1]

Motivation
----------

Free tshirt.

Usage
-----

The project contains two scripts

`unshred.py` - unshreds a shredded image.

    ./unshred.py source dest [strip_width=32]

    source - the source image that has been stripped into equal
             columns of strip_width pixels.
    
    dest - the file under which to save the unshredded image.
    
    stript_width - the width of each stripped column.  This is an
                   optional parameter and is assumed to be 32 pixels
                   if not provided.

`shred.py` - shreds an image.  Takes some care to order the strips so
             that adjacent strips do not end up adjacent to each
             other.

    ./shred.py source dest [strip_width=32]
    
    source - the source image to strip into equal columns of width
             strip_width.
    
    dest - the file under which to save the shredded image.
    
    stript_width - the width of each stripped column.  This is an
                   optional parameter and is taken as 32 pixels by
                   default.

How it works
------------

The program works by generating as many strips from the image as
needed and comparing the edges of all strips.  Given two strips `s1`,
`s2` it computes the color differences between all pixels on the right
edge of `s1` and left edge of `s2`, and color differences between all
pixels on the left edge of `s1` and right edge of `s2`.

Strips are ordered by minimal color differences between them.

Caveats
-------

1. My day job involves programming in Java.  Unlike most of proggit and
   HackerNews, I actually like the Java programming language.  I used
   Python in this program because I've used PIL in the past (circa 2007)
   and felt it would be easier than playing with some Java libray I've
   never used.  _The code may not be canonical Python._

2. Unshredding doesn't work under all circumstances.  Specifically, it
   doesn't perform well when many adjacent strips are close to each
   other.

3. The program is not written for speed.  I have made exactly one
   improvement for the sake of speed: a wrapper class around
   `PIL.Image` to speed up pixel access.  The program was around 1.5
   times faster after that adjustment.

Future work
-----------

IMO the algorithm is mostly correct and the edge cases can be fixed by
adding code rather than changing the existing algorithm.

[1]: http://instagram-engineering.tumblr.com/post/12651721845/instagram-engineering-challenge-the-unshredder
