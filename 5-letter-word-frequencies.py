wordFreq = dict()
filePath = "./unigram_freq.csv"
outFileMap = "./unigram_freq_five_letter_words.csv"
outFileList = "./fiveletterwords.txt"

with open(filePath, 'r') as file:
    info = file.readline() # first line is names
    allLines = file.readlines()
    for pair in allLines:
        pair = pair.strip()
        split = pair.split(",")
        if len(split[0]) == 5:
            wordFreq[split[0]] = split[1]

outContents = []
fiveLetterWords = []

for word in wordFreq:
    outContents.append(word + ',' + wordFreq[word])
    fiveLetterWords.append(word)

with open(outFileMap, 'w') as output:
    for pair in outContents:
        output.write(pair + '\n')

with open(outFileList, 'w') as output:
    for word in fiveLetterWords:
        output.write(word + '\n')