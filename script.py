
stringList = []
with open("five_letter_word_list_in_order_of_frequency.txt", 'r') as f:
    lines = f.readlines()
    for word in lines:
        stringList.append("\"" + word.strip() + "\",\n")

with open("jsWordList.txt", 'w') as f:
    for word in stringList:
        f.write(word)