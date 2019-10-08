#!/bin/bash

calculate(){
    
    # wc -l $1  count lines in file
    # awk '{ print $1 }' : wc return #lines filename. awk filters out filename
    # wc starts counting from 0, so we add 1
    length=$(( $(wc -l $1 | awk '{ print $1 }') +1 ))
    #echo "Lines = $length"

    sum_x=$(awk -F ':' '{s+=$1} END {print s}' $1)
    #echo "SUM_X = $sum_x"

    sum_x2=$(awk -F ':' '{s+=$1*$1} END {print s}' $1)
    #echo "SUM_X2 = $sum_x2"

    sum_y=$(awk -F ':' '{s+=$2} END {print s}' $1)
    #echo "SUM_Y = $sum_y"

    sum_xy=$(awk -F ':' '{s+=$1*$2} END {print s}' $1)
    #echo "SUM_XY = $sum_xy"

    #read w1 w2 w3 w4 <<< $(awk -F ':' '{x+=$1; x2+=$1*$1; y+=$2; xy+=$1*$2} END {print x "\t" x2 "\t" y "\t" xy}' $1)
    #echo "x=$w1 x2=$w2 y=$w3 xy=$w4" 

    a=$( echo "scale=5; ($length * $sum_xy - $sum_x * $sum_y) / ($length * $sum_x2 - $sum_x * $sum_x )" | bc)

    b=$( echo "scale=5; ($sum_y - $a * $sum_x) / $length" | bc)

    c=1

    err=$(awk -F ':' "{s+=(\$2-($a * \$1 + $b))^2 } END {print s}" $1)





    echo "FILE: $1, a=$a b=$b c=$c err=$err"
    return
}

###
# script main body.
###

#For every input file call the function to process it
while [[ $# -gt 0 ]]; do
    calculate $1
    shift #after the shift $1 = $2, $2 = $3 ...
done
