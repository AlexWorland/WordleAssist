awk '{ print length($0) " " $0; }' words | sort -n | cut -d ' ' -f 2- > words_sorted_by_length
echo "" > 
wordCount=`cat words | wc -l`
counter=$((1))
while read p; do
    length=`echo $p | wc -c`
    if [ $length == 6 ]; then
        echo $p >> five_letter_words
    elif [ $length -gt 6 ]; then
        break
    fi
    echo "$length : $counter / $wordCount"
    ((counter=counter+1))
    let "counter=counter+1"
done <words_sorted_by_length

