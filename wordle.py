from random import random, randrange
import requests
import json

filePath = "./wordlist.txt"
# filePath = "./words"
wordList = []

with open(filePath, 'r') as words:
    for word in words:
        if len(word) == 6:
            wordList.append(word.upper().strip())

presentLetters = []
nonPresentLetters = []
validPositionMap = {}
invalidPositionMap = {}
isWinner = False
isFirstWord = True
while not isWinner:
    validWords = []
    for word in wordList:
        wordPassesValidLetters = True
        for letter in presentLetters:
            if letter not in word:
                wordPassesValidLetters = False
                break
        
        if not wordPassesValidLetters:
            continue
        
        wordPassesInvalidLetters = True
        for letter in word:
            if letter in nonPresentLetters:
                wordPassesInvalidLetters = False
                break
        
        if not wordPassesInvalidLetters:
            continue

        wordPassesLetterPositions = True
        for letter in validPositionMap:
            letterPositions = validPositionMap[letter]
            for position in letterPositions:
                if letter != word[position]:
                    wordPassesLetterPositions = False
                    break
        
        if not wordPassesLetterPositions:
            continue

        wordPassesInvalidLetterPositions = True
        for letter in invalidPositionMap:
            letterPositions = invalidPositionMap[letter]
            for position in letterPositions:
                if letter == word[position]:
                    wordPassesInvalidLetterPositions = False
                    break
        
        if not wordPassesInvalidLetterPositions:
            continue

        validWords.append(word)

    print("Suggesting", len(validWords), "words out of", len(wordList), "words")

    numCols = 20

    for i in range(0, len(validWords) - 1, numCols):
        tmpWordList = []
        for tmp in range(i, i + numCols, 1):
            if tmp < len(validWords):
                tmpWordList.append(validWords[tmp])
        print(tmpWordList)

    generateNewRandom = True
    while (generateNewRandom):
        randIndex = randrange(len(validWords))
        randWord = validWords[randIndex]
        while isFirstWord:
            isFirstWord = False
            for i in range(len(randWord)):
                if randWord[i] in randWord[0:i] or randWord[i] in randWord[i + 1:len(randWord) - 1]:
                    randIndex = randrange(len(validWords))
                    randWord = validWords[randIndex]
                    isFirstWord = True
                    break
                    
        print("Suggested random word: ", randWord)
        if input("New Random? (y/n): ") != 'y':
            generateNewRandom = False

    isContinue = input("Continue? (y/n): ")
    if isContinue != 'y':
        break

    print()
    print("Valid Letters:", presentLetters)
    print("Invalid Letters:", nonPresentLetters)
    print("Valid Letter Positions:", validPositionMap)
    print("Invalid Letter Positions:", invalidPositionMap)
    print()
    # Update word lists
    newValidLetters = input("New Valid Letters: ")
    newInvalidLetters = input("New Invalid Letters: ")
    newValidPositions = input("New Valid Letter Positions - ex A3I4B1: ")
    newInvalidPositions = input("New Invalid Positions: ")
    
    for ch in newValidLetters:
        presentLetters.append(ch.upper())
    for ch in newInvalidLetters:
        nonPresentLetters.append(ch.upper())
    if len(newValidPositions) != 0:
        for i in range(0, len(newValidPositions) - 1, 2):
            key = newValidPositions[i].upper()
            value = int(newValidPositions[i+1])
            if key in validPositionMap:
                if value not in validPositionMap[key]:
                    validPositionMap[key].append(value)
            else:
                validPositionMap[key] = [value]
    if len(newInvalidPositions) != 0:
        for i in range(0, len(newInvalidPositions) - 1, 2):
            key = newInvalidPositions[i].upper()
            value = int(newInvalidPositions[i+1])
            if key in invalidPositionMap:
                if value not in invalidPositionMap[key]:
                    invalidPositionMap[key].append(value)
            else:
                invalidPositionMap[key] = [value]
    print()
    print("Valid Letters:", presentLetters)
    print("Invalid Letters:", nonPresentLetters)
    print("Valid Letter Positions:", validPositionMap)
    print("Invalid Letter Positions:", invalidPositionMap)
    print()
definitions = input("Would you like definitions? (y/n): ")
if definitions == 'y' or definitions == 'yes':
    print("getting definitions...")
    # print("********** Getting Definitions **********")

    definitionMap = {}
    for word in validWords:
        # print("Getting definition for:", word)
        try:
            response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
            jsonResponse = response.json()        
            if 'title' in jsonResponse and jsonResponse['title'] == 'No Definitions Found':
                # print("error getting definition for", word)
                continue
            else:
                definitionMap[word] = jsonResponse[0]['meanings'][0]['definitions'][0]['definition']
        except:
            print("Something went wrong while getting definition for", word)

    print("********** Definitions **********")
    for word in validWords:
        if word in definitionMap:
            print(word, ":", definitionMap[word])
        else:
            print(word, "No definition found")
else:
    exit()

