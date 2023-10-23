#!/bin/bash

tesseract_lang=$1
# Create the image and paste it in a temp file
SRC_IMG=`mktemp`
trap "rm $SRC_IMG*" EXIT
echo $SRC_IMG
scrot -s $SRC_IMG.png -q 100
# Increate quality
mogrify -modulate 100,0 -resize 400% $SRC_IMG.png

tesseract $SRC_IMG.png $SRC_IMG &> /dev/null
cat $SRC_IMG.txt | xsel -bi

#exit

#xclip -selection clipboard -t image/png -o > $SRC_IMG
