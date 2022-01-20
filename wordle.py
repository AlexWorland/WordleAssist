import functools
from random import random, randrange
import requests
import json

letterWeightMap = dict()
letterWeightMap['A'] = 0.082
letterWeightMap['B'] = 0.015
letterWeightMap['C'] = 0.028
letterWeightMap['D'] = 0.043
letterWeightMap['E'] = 0.13
letterWeightMap['F'] = 0.022
letterWeightMap['G'] = 0.02
letterWeightMap['H'] = 0.061
letterWeightMap['I'] = 0.07
letterWeightMap['J'] = 0.0015
letterWeightMap['K'] = 0.0077
letterWeightMap['L'] = 0.04
letterWeightMap['M'] = 0.025
letterWeightMap['N'] = 0.067
letterWeightMap['O'] = 0.075
letterWeightMap['P'] = 0.019
letterWeightMap['Q'] = 0.00095
letterWeightMap['R'] = 0.06
letterWeightMap['S'] = 0.063
letterWeightMap['T'] = 0.091
letterWeightMap['U'] = 0.028
letterWeightMap['V'] = 0.0098
letterWeightMap['W'] = 0.024
letterWeightMap['X'] = 0.0015
letterWeightMap['Y'] = 0.02
letterWeightMap['Z'] = 0.00074

for weight in letterWeightMap:
    letterWeightMap[weight] = int(letterWeightMap[weight] * (10 ** 5))


def pickMostValuableWordFromList(validWords):
    validWords = sorted(validWords, key=functools.cmp_to_key(compareWordValues), reverse=True)
    return validWords[0]


def compareTupleValues(tuple1, tuple2):
    a = tuple1[0]
    b = tuple2[0]
    return a - b


def compareWordValues(word1, word2):
    word1Value = findWordValue(word1)
    word2Value = findWordValue(word2)
    return word1Value - word2Value


def findWordValue(word):
    wordWeight = 0
    for letter in word:
        wordWeight += letterWeightMap[letter]
    return wordWeight


def main():
    # filePath = "./wordlist.txt"
    filePath = "./words"
    wordList = []

    with open(filePath, 'r') as words:
        for word in words:
            if len(word) == 6:
                wordList.append(word.upper().strip())

    # Populate with most common letters to get most productive first round
    presentLetters = ['E', 'T', 'A']
    nonPresentLetters = ['J', 'Q', 'Z']
    validPositionMap = {}
    invalidPositionMap = {}
    isWinner = False
    isFirstWord = True
    isFirstRount = True
    while True:
        print()
        print("********************")
        print()
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
        validWords.sort(key=functools.cmp_to_key(compareWordValues), reverse=True)
        print("Suggesting", len(validWords), "words out of", len(wordList), "words")

        numCols = 20  # TODO: make adjustable based on terminal length (might not be possible)

        for i in range(0, len(validWords) - 1, numCols):
            tmpWordList = []
            for tmp in range(i, i + numCols, 1):
                if tmp < len(validWords):
                    tmpWordList.append(validWords[tmp])
            print(tmpWordList)

        generateNewRandom = True
        while (generateNewRandom):
            if len(validWords) == 0:
                print("Sorry, something went wrong. I found 0 valid words.")
                exit()
            if isFirstWord:
                goodFirstWords = []
                for word in validWords:
                    isGoodFirstWord = True
                    for i in range(len(word)):
                        if word[i] in word[0:i] or word[i] in word[i + 1:len(word) - 1]:
                            isGoodFirstWord = False
                            break
                    if isGoodFirstWord:
                        goodFirstWords.append(word)
                goodFirstWord = pickMostValuableWordFromList(goodFirstWords)
                print("Recommended Starting Word:", goodFirstWord)

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

            print("Recommended Word:", validWords[0])
            print("Suggested random word: ", randWord)
            if input("New Random? (y/n): ") != 'y':
                generateNewRandom = False

        if isFirstRount:
            isFirstRount = False
            presentLetters = []
            nonPresentLetters = []

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
                value = int(newValidPositions[i + 1])
                if key in validPositionMap:
                    if value not in validPositionMap[key]:
                        validPositionMap[key].append(value)
                else:
                    validPositionMap[key] = [value]
        if len(newInvalidPositions) != 0:
            for i in range(0, len(newInvalidPositions) - 1, 2):
                key = newInvalidPositions[i].upper()
                value = int(newInvalidPositions[i + 1])
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


if __name__ == '__main__':
    main()
