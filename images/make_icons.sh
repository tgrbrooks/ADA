#!/bin/bash

convert icon.png -resize 16x16 icons/base/16.png
convert icon.png -resize 24x24 icons/base/24.png
convert icon.png -resize 32x32 icons/base/32.png
convert icon.png -resize 48x48 icons/base/48.png
convert icon.png -resize 64x64 icons/base/64.png

convert icons/base/* icons/Icon.ico

convert icon.png -resize 128x128 icons/linux/128.png
convert icon.png -resize 256x256 icons/linux/256.png
convert icon.png -resize 512x512 icons/linux/512.png
convert icon.png -resize 1024x1024 icons/linux/1024.png

convert icon.png -bordercolor none -border 5%x5% -resize 128x128 icons/mac/128.png
convert icon.png -bordercolor none -border 5%x5% -resize 256x256 icons/mac/256.png
convert icon.png -bordercolor none -border 5%x5% -resize 512x512 icons/mac/512.png
convert icon.png -bordercolor none -border 5%x5% -resize 1024x1024 icons/mac/1024.png
