#!/bin/bash

echo "Am alive"


awk -F"-|:"  '{print $1 "\t" $2 "\t" $3 "\t" $4}'

awk -F"-|:"  '$3>$4 {print $1 "\t" 3} $3<$4 {print $2 "\t" 3} $3==$4 {print $1 "\t" 1 "\n" $2 "\t" 1 }' input





awk -F"-|:"  '$3>$4 { score1=3; score2=0 } $3<$4 {score1=0; score2=3} $3==$4 {score1=1; score2=1} {print $1 "\t" score1 "\t" $3 "\t" $4 "\n" $2 "\t" score2 "\t" $4 "\t" $3}' input




   awk -F"-|:"  '$3>$4 { score1=3; score2=0 } $3<$4 {score1=0; score2=3} $3==$4 {score1=1; score2=1} {print $1 "\t" score1 "\t" $3 "\t" $4 "\n" $2 "\t" score2 "\t" $4 "\t" $3}' input \
|  sort \
| awk '{
    arr1[$1]+=$2;
    arr2[$1]+=$3;
    arr3[$1]+=$4
   }
   END {
     for (key in arr1) printf("\t%s\t%s\t%s-%s\n", key, arr1[key], arr2[key], arr3[key])
   }'\
|  sort -k2,2nr -k1,1r \
|  nl -w2 -s "."

