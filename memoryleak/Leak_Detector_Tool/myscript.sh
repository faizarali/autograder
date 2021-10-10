#!/bin/bash
file=$1
gcc -c leak_detector_c.c
gcc -c $file
gcc -o memtest leak_detector_c.o ${file%.*}.o
./memtest > /dev/null 2>&1
cat leak_info.txt
rm *.o