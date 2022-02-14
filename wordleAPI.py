from fileinput import isfirstline
import random
import sys

from spellchecker import WordFrequency

class WordleGame:
    class EnteredWord:
        def __init__(self, word, information):
            self.word = word
            self.information = information
            self.length = len(word)

    class GameState:
        def __init__(self, validWords, validLetters=None):
            self.__validWords = validWords
            self.__validLetters = set()
            self.__invalidLetters = set()
            self.__validPositions = dict()
            self.__invalidPositions = dict()
            self.__recommendedWordIndex = 0
            if validLetters is not None:
                self.__validLetters = set(validLetters)
                self.__lintWords()

        def getNextRecommendedWord(self):
            self.__recommendedWordIndex %= len(self.__validWords)
            wordToReturn = self.__validWords[self.__recommendedWordIndex]
            self.__recommendedWordIndex += 1
            return wordToReturn

        def update(self, enteredWord):
            for i in range(enteredWord.length):
                letter = enteredWord.word[i]
                information = enteredWord.information[i]
                if information == 'g':
                    if letter not in self.__validLetters:
                        self.__invalidLetters.add(letter)
                    else:
                        self.__addOrAppend(letter, i, self.__invalidPositions)
                elif information == 'G':
                    if letter not in self.__validLetters:
                        self.__validLetters.add(letter)
                    self.__addOrAppend(letter, i, self.__validPositions)
                elif information == 'y':
                    self.__validLetters.add(letter)
                    self.__addOrAppend(letter, i, self.__invalidPositions)
            self.__lintWords()

        def __addOrAppend(self, letter, position, letterMap):
            if position in letterMap:
                if position not in letterMap[letter]:
                    letterMap[letter].append(position)
            else:
                letterMap[letter] = [position]

        def __lintWords(self):
            newValidWords = self.__validWords.copy()
            for word in self.__validWords:
                if not self.__validateWord(word):
                    newValidWords.remove(word)
            if len(newValidWords) == 0:
                print("debug")
            self.__validWords = newValidWords

        def __validateWord(self, wordToValidate):
            # Make sure word contains every valid letter
            for letter in self.__validLetters:
                if letter in wordToValidate:
                    continue
                else:
                    return False

            # Make sure word contains no invalid letters
            for letter in self.__invalidLetters:
                if letter in wordToValidate:
                    return False

            # Check valid positions
            for letter in self.__validPositions:
                for validPosition in self.__validPositions[letter]:
                    if wordToValidate[validPosition] != letter:
                        return False

            # Check invalid positions
            for letter in self.__invalidPositions:
                for invalidPosition in self.__invalidPositions[letter]:
                    if wordToValidate[invalidPosition] == letter:
                        return False
            return True

        def getValidWords(self):
            return self.__validWords.copy()

        def getValidLetters(self):
            return self.__validLetters.copy()

        def getInvalidLetters(self):
            return self.__invalidLetters.copy()

        def getValidPositions(self):
            return self.__validPositions.copy()

        def getInvalidPositions(self):
            return self.__invalidPositions.copy()

    def __init__(self, wordLength, initialGameState=None, wordList=None):
        self.__initialGameState = initialGameState
        self.__wordLength = wordLength
        if wordList is not None:
            self.__wordList = wordList
        else:
            self.__wordList, self.__wordFreqs = self.__loadWords()
        self.__isFirstRound = True
        self.__wordListBackup = self.__wordList.copy()
        if self.__initialGameState is not None:
            self.__gameState = self.GameState(self.__wordList.copy(), self.__initialGameState)
        else:
            self.__gameState = self.GameState(self.__wordList.copy())

    def guessWord(self, word, information):
        enteredWord = self.EnteredWord(word, information)
        self.__gameState.update(enteredWord)

    def getNextRecommendedWord(self):
        wordToReturn = self.__gameState.getNextRecommendedWord()
        if self.__isFirstRound:
            self.__isFirstRound = False
            self.__gameState = self.GameState(self.__wordList.copy())
        return wordToReturn
    
    def getRandomWord(self):
        return self.__wordList[random.randint(0, len(self.__wordList) - 1)]

    def resetGame(self):
        self.__init__(self.__wordLength, self.__initialGameState, self.__wordListBackup)

    def __loadWords(self):
        wordList = []
        wordFreqs = dict()
        with open("./unigram_freq.csv") as f:
            lines = f.readlines()
            for line in lines[1:]:
                word, freq = line.strip('\n').split(',')
                if len(word) == self.__wordLength:
                    wordList.append(word)
                    wordFreqs[word] = int(freq)
            f.close()
            del lines
        return wordList, wordFreqs