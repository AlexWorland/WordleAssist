import os
import signal
import sys
# validLetters = set()
# invalidLetters = set()

wordFrequencies = dict()

class EnteredWord:
    word = ""
    information = ""
    length = 0
    def __init__(self, word, information):
        self.word = word
        self.information = information
        self.length = len(word)
        # for i in range(len(self.word)):
        #     if self.information[i] == 'g':
        #         invalidLetters.add(self.word[i])
        #     elif self.information[i] == 'G' or self.information[i] == 'y':
        #         validLetters.add(self.word[i])

class GameState:
    validWords = []
    validLetters = set()
    invalidLetters = set()
    validPositions = dict()
    invalidPositions = dict()
    def __init__(self, validLetters=None):
        self.validWords = []
        self.validLetters = set()
        self.invalidLetters = set()
        self.validPositions = dict()
        self.invalidPositions = dict()
        if validLetters is not None:
            self.validLetters = set(validLetters)

    def update(self, enteredWord):
        for i in range(enteredWord.length):
            letter = enteredWord.word[i]
            information = enteredWord.information[i]
            if information == 'g':
                if letter not in self.validLetters:
                    self.invalidLetters.add(letter)
                else:
                    addOrAppend(letter, i, self.invalidPositions)
            elif information == 'G':
                if letter not in self.validLetters:
                    self.validLetters.add(letter)
                addOrAppend(letter, i, self.validPositions)
            elif information == 'y':
                self.validLetters.add(letter)
                addOrAppend(letter, i, self.invalidPositions)

def addOrAppend(letter, position, map):
    if position in map:
        if position not in map[letter]:
            map[letter].append(position)
    else:
        map[letter] = [position]

def exitHandler(signum, frame):
    print("\nExiting...")
    exit()

def getInputWord(wordLength):
    validInput = False
    while (not validInput):
        enteredWord = input("Enter the word you typed in: ")
        if len(enteredWord) != wordLength:
            print("Please enter a", wordLength, "letter word.")
        else:
            validInput = True
    return enteredWord

def getInputWordInformation(wordLength):
    validInput = False
    # while not validInput:
    wordInformation = input("Enter the color information for each letter (green: G, gray: g, yellow: y): ")
    return wordInformation

# def isValidWord(wordToVerify, enteredWord, gameState):
#     # Check letter presence
#     for i in range(len(wordToVerify)):
        
#         if enteredWord.information[i] == 'g': # gray
#             if enteredWord.word[i] in wordToVerify:
#                 return False
#         elif enteredWord.information[i] == 'G': # green
#             if enteredWord.word[i] != wordToVerify[i] and enteredWord.word[i]:
#                 return False
#         elif enteredWord.information[i] == 'y': # yellow
#             if enteredWord.word[i] == wordToVerify[i]:
#                 return False
#             else:
#                 if enteredWord.word[i] not in wordToVerify[:i] and enteredWord.word[i] not in wordToVerify[i + 1:]:
#                     return False

#     # Check letter locations
#     for i in range(len(wordToVerify)):
#         if 
#     return True

def validateWord(wordToValidate, gameState):
    # Make sure word contains every valid letter
    for letter in gameState.validLetters:
        if letter in wordToValidate:
            continue
        else:
            return False

    # Make sure word contains no invalid letters
    for letter in gameState.invalidLetters:
        if letter in wordToValidate:
            return False
        
    # Check valid positions
    for letter in gameState.validPositions:
        for validPosition in gameState.validPositions[letter]:
            if wordToValidate[validPosition] != letter:
                return False

    # Check invalid positions
    for letter in gameState.invalidPositions:
        for invalidPosition in gameState.invalidPositions[letter]:
            if wordToValidate[invalidPosition] == letter:
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
    
def getPossibleFirstWords(validWords, gameState):
    return lintWords(validWords, gameState)

def lintWords(validWords, gameState):
    newValidWords = validWords.copy()
    for word in validWords:
        if not validateWord(word, gameState):
            newValidWords.remove(word)
    return newValidWords

def computeGlobalWordFrequencies(wordLength):
    global wordFrequencies
    with open("./unigram_freq.csv") as f:
        lines = f.readlines()
        for line in lines[1:]:
            word, frequency = line.strip('\n').split(",")
            wordFrequencies[word] = int(frequency)
        f.close()
        del lines

    for word in wordFrequencies.copy():
        if len(word) != wordLength:
            del wordFrequencies[word]

def main(wordLength):
    print("Loading...")
    computeGlobalWordFrequencies(wordLength)
    validWords = list(wordFrequencies.keys())
    # list is already sorted in the file
    # validWords = sortBasedOnFrequency(validWords)

    initialGameState = ['e', 'a', 'r', 'i']
    validWords = list(wordFrequencies.keys())
    gameState = GameState(initialGameState)
    isFirstRound = True
    recommendedWordListBackup = validWords.copy()
    recommendedWordList = lintWords(validWords, gameState)
    while (True):
        counter = 0
        options = ['i', 'c', 'r']
        firstRound = True
        while True:
            print("*********************************************************")
            print()
            
            if len(recommendedWordList) == 0:
                print("Zero Words Match Restrictions.")
                print("Resetting.")
                counter = 0
                gameState = GameState(initialGameState)
                recommendedWordList = lintWords(recommendedWordListBackup.copy(), gameState)
                firstRound = True
                continue

            print("########## -> Recommended Word:", recommendedWordList[counter])
            print()

            wordInformation = getInputWordInformation(wordLength)
            if 'c' in wordInformation:
                counter += 1
                counter %= len(recommendedWordList)
            elif 'r' in wordInformation:
                counter = 0
                gameState = GameState(initialGameState)
                recommendedWordList = lintWords(recommendedWordListBackup.copy(), gameState)
                firstRound = True
            else:
                enteredWord = recommendedWordList[counter]
                if firstRound: 
                    gameState = GameState()   
                    gameState.update(EnteredWord(enteredWord, wordInformation))
                    recommendedWordList = lintWords(recommendedWordListBackup.copy(), gameState)
                    firstRound = False
                    counter = 0
                else:
                    gameState.update(EnteredWord(enteredWord, wordInformation))
                    recommendedWordList = lintWords(recommendedWordList, gameState)
                print("Number of Valid Words:", len(recommendedWordList))
                print("Valid Letters:", gameState.validLetters)
                print("Invalid Letters:", gameState.invalidLetters)
                print("Valid Letter Posisitions:", gameState.validPositions)
                print("Invalid Letter Posisitions:", gameState.invalidPositions)
                print()

                
signal.signal(signal.SIGINT, exitHandler)

if __name__ == "__main__":
    wordLength = 5
    if len(sys.argv) > 1:
        wordLength = int(sys.argv[1])
    main(wordLength)