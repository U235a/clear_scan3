# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 21:15:27 2021

@author: U235
"""

from imageproclib import *
import cv2
import sys

if len(sys.argv)<2:
    print( 'Usage image name as command line argument.\n Example:\n python clear_scan3.py image.tif')
    sys.exit(0)

name=sys.argv[1]

im = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
im=cv2.threshold(im, 127, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)[1]

im_backup=im.copy()
se=cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
se2=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
se3=cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
se5=cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
se6=cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
se7=cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

im=cv2.dilate(im, se5)
opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, se)
opening = cv2.dilate(opening, se6)
skel=bwmorph_thin(im)

endpoints_skel=bwmorph_endpoints(skel)
endpoints_skel=cv2.bitwise_and(endpoints_skel, ~opening)
skel=cv2.bitwise_and(skel, ~opening)

lines=imreconstruct(endpoints_skel, skel)
lines=bwareaopen(lines, 8)
lines=cv2.dilate(lines, se2)

out=cv2.bitwise_and(im, ~lines)
out=cv2.bitwise_and(out, im_backup)
out=bwareaopen(out, 20)
noise=cv2.bitwise_xor(out, im_backup)
noise=cv2.dilate(noise, se7)
out=cv2.compare(im_backup, noise, cv2.CMP_GT)
out=bwareaopen(out, 30)
cv2.imwrite('clear_'+name, ~out)
out_rgb=cv2.cvtColor(~out, cv2.COLOR_GRAY2BGR)
b, g, r =cv2.split(out_rgb)
b, g=~im_backup, ~im_backup
out_rgb=cv2.merge((b, g, r))
cv2.imwrite('clear_rgb_'+name, out_rgb)




