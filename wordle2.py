validLetters = set()
invalidLetters = set()

wordFrequencies = dict()
with open("./unigram_freq_five_letter_words.csv") as f:
    for line in f:
        word, frequency = line.split(",")
        wordFrequencies[word] = int(frequency)
    f.close()

class EnteredWord:
    word = ""
    information = ""
    def __init__(self, word, information):
        self.word = word
        self.information = information
        for i in range(len(self.word)):
            if self.information[i] == 'g':
                invalidLetters.add(self.word[i])
            elif self.information[i] == 'G' or self.information[i] == 'y':
                validLetters.add(self.word[i])

def getInputWord():
    validInput = False
    while (not validInput):
        enteredWord = input("Enter the word you typed in: ")
        if len(enteredWord) != 5:
            print("Please enter a 5 letter word.")
        else:
            validInput = True
    return enteredWord

def getInputWordInformation():
    validInput = False
    while not validInput:
        wordInformation = input("Enter the color information for each letter (green: G, gray: g, yellow: y): ")
        counter = 0
        for letter in wordInformation:
            if letter != 'g' and letter != 'G' and letter != 'y':
                print("Invalid input")
                break
            counter += 1
        if counter == 5:
            validInput = True
    return wordInformation

def isValidWord(wordToVerify, enteredWord):
    for i in range(len(wordToVerify)):
        if enteredWord.information[i] == 'g': # gray
            if enteredWord.word[i] in wordToVerify:
                return False
        elif enteredWord.information[i] == 'G': # green
            if enteredWord.word[i] != wordToVerify[i]:
                return False
        elif enteredWord.information[i] == 'y': # yellow
            if enteredWord.word[i] == wordToVerify[i]:
                return False
            else:
                if enteredWord.word[i] not in wordToVerify[:i] and enteredWord.word[i] not in wordToVerify[i + 1:]:
                    return False
    return True

def printWithNumColumns(list, numColumns):
    for i in range(0, len(list), numColumns):
        print(list[i:i + numColumns])

def sortBasedOnFrequency(wordList):
    wordList.sort(key=lambda x: wordFrequencies[x], reverse=True)
    return wordList

def verifyInput(enteredWord, wordInformation):
    print()
    print("Entered Word:" ,enteredWord)
    print("Entered Information:", wordInformation)
    while True:
        verify = input("Is this correct? (y/n): ")
        if verify == 'y':
            return True
        elif verify == 'n':
            return False
    
def main():
    validWords = list(wordFrequencies.keys())
    while (True):
        verify = False
        while not verify:
            enteredWord = getInputWord().lower()
            wordInformation = getInputWordInformation()
            verify = verifyInput(enteredWord, wordInformation)

        enteredWord = EnteredWord(enteredWord, wordInformation)

        validWordsCopy = validWords.copy()
        for word in validWords:
            if not isValidWord(word, enteredWord):
                validWordsCopy.remove(word)
        validWords = validWordsCopy

        printWithNumColumns(validWords, 5)
        print()
        print("Valid Letters:", validLetters)
        print("Invalid Letters:", invalidLetters)
        print()
        
        if len(validWords) == 0:
            print("No words found.")
            exit()
        elif len(validWords) == 1:
            print("The only word left is: " + validWords[0])
            exit()
        else:
            print("Recommended:", validWords[0])

if __name__ == "__main__":
    main()