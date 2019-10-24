#!/bin/bash
   
   #h eisodos xorizetai se stiles me tous diaxoristes "-" h ":"
   awk -F"-|:"  \
   '
      $3>$4 { score1=3; score2=0} 
      $3<$4 { score1=0; score2=3} 
      $3==$4 {score1=1; score2=1} 
      {print $1 "\t" score1 "\t" $3 "\t" $4 "\n" $2 "\t" score2 "\t" $4 "\t" $3}' $1 `#gia kathe agona upologizontai oi bathmoi kathe omadas`\
|  sort \
| awk -F"\t"   \
  '{
    arr1[$1]+=$2;
    arr2[$1]+=$3;
    arr3[$1]+=$4


    if (length($1) > width)
        width = length($1)
 
   }
   END {
     for (key in arr1) printf("\t%-*s\t%3s\t%3s -%3s\n",width, key, arr1[key], arr2[key], arr3[key])
   }'\
|  sort -k2,2nr -k1,1 \
|  nl -n ln -w1 -s "."

