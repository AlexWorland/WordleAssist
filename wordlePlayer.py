import multiprocessing
import random
import string
import sys
import itertools

from numpy import average, choose
import wordleAPI
import signal
from multiprocessing import Pool
import re

def wordleMultiProcessing(args):
    word = args[0]
    initialGameState = args[1]
    wordList = args[2]
    wordLength = 5
    maxRounds = 6
    wordleGame = wordleAPI.WordleGame(wordLength, initialGameState, wordList)
    printGuesses = False
    wordleAnswer = word
    round = 0
    for i in range(maxRounds):
        round += 1
        guess = wordleGame.getNextRecommendedWord()
        if guess == wordleAnswer:
            break
        information = getWordInformation(guess, wordleAnswer)
        if printGuesses:
            print("\tRound:", round + 1)
            print("\t\tActual Answer\t:", wordleAnswer)
            print("\t\tGuess\t\t:", guess)
            print("\t\tInformation\t:", information)
        wordleGame.guessWord(guess, information)
    print("Played:", word, "in", round, "rounds")
    return (initialGameState, word, round)

def wordleSingleWord(word):
    wordLength = len(word)
    maxRounds = 6
    initialGameState = ['r', 'a', 'e', 'i']
    wordleGame = wordleAPI.WordleGame(wordLength, initialGameState)
    wordleAnswer = word
    printGuesses = True
    print("*********************************************************")
    print("Answer:", wordleAnswer)
    # print("Max Rounds:", maxRounds)
    round = 0
    for i in range(maxRounds):
        round = i
        guess = wordleGame.getNextRecommendedWord()
        if guess == wordleAnswer:
            break
        information = getWordInformation(guess, wordleAnswer)
        if printGuesses:
            print("\tRound:", round + 1)
            print("\t\tActual Answer\t:", wordleAnswer)
            print("\t\tGuess\t\t:", guess)
            print("\t\tInformation\t:", information)
        wordleGame.guessWord(guess, information)

    if round >= maxRounds:
        print("\t\t\tLose!")
    else:
        print("\t\t\tCorrect!", "|", "Rounds:", round + 1)

    wordleGame.resetGame()
def main():
    wordLength = 5
    maxRounds = 6
    maxGames = 100
    initialGameState = ['r', 'a', 'e', 'i']
    if len(sys.argv) > 1:
        wordLength = int(sys.argv[1])
    wordleGame = wordleAPI.WordleGame(wordLength, initialGameState)
    wordleAnswers = loadWordleSet()
    currentGame = 0
    winCount = 0
    loseCount = 0
    roundDistribution = []
    for i in range(maxRounds):
        roundDistribution.append(0)
    printGuesses = True
    answerIndex = 0
    while currentGame < len(wordleAnswers):
        currentGame += 1
        # wordleAnswer = wordleGame.getRandomWord()
        # wordleAnswer = "aarez"
        wordleAnswer = wordleAnswers[answerIndex]
        answerIndex += 1
        print("*********************************************************")
        print("Game:", currentGame)
        print("Answer:", wordleAnswer)
        # print("Max Rounds:", maxRounds)
        round = 0
        for i in range(maxRounds):
            round = i
            guess = wordleGame.getNextRecommendedWord()
            if guess == wordleAnswer:
                break
            information = getWordInformation(guess, wordleAnswer)
            if printGuesses:
                print("\tRound:", round + 1)
                print("\t\tActual Answer\t:", wordleAnswer)
                print("\t\tGuess\t\t:", guess)
                print("\t\tInformation\t:", information)
            wordleGame.guessWord(guess, information)

        if round >= maxRounds:
            loseCount += 1
            print("\t\t\tLose!")
        else:
            winCount += 1
            print("\t\t\tCorrect!", "|", "Rounds:", round + 1)
        roundDistribution[round] += 1
        wordleGame.resetGame()
    print("*********************************************************")
    print("Win:", winCount)
    print("Lose:", loseCount)
    print("Win Rate:", winCount / maxGames)
    print("Round Distribution:", roundDistribution)
def getWordInformation(guess, wordleAnswer):
    information = ""
    letterCountMap = dict()
    wordLength = len(guess)
    for i in range(wordLength):
        if guess[i] == wordleAnswer[i]:
            information += "G"
        elif guess[i] in wordleAnswer:
            if guess[i] not in letterCountMap or letterCountMap[guess[i]] != wordleAnswer.count(guess[i]):
                information += "y"
            else:
                information += "g"
        else:
            information += 'g'

        if guess[i] in letterCountMap:
            letterCountMap[guess[i]] += 1
        else:
            letterCountMap[guess[i]] = 1

    return information
def exitHandler(signum, frame):
    print("\nExiting...")
    exit()

def loadAllNLetterWords(wordLength):
        wordList = []
        wordFreqs = dict()
        with open("./unigram_freq.csv") as f:
            lines = f.readlines()
            for line in lines[1:]:
                word, freq = line.strip('\n').split(',')
                if len(word) == wordLength:
                    wordList.append(word)
                    wordFreqs[word] = int(freq)
            f.close()
            del lines
        return wordList, wordFreqs

def loadWordleSet():
    wordleWords = []
    with open("./wordle-answers-alphabetical.txt", 'r') as f:
        wordleWords = f.readlines()
    f.close()
    for i in range(len(wordleWords)):
        wordleWords[i] = wordleWords[i].strip('\n')
    return wordleWords

def getAverageRoundCount(returnList):
    if len(returnList) == 0:
        return 0
    averageRoundCount = 0
    for i in range(len(returnList)):
        averageRoundCount += returnList[i][1]
    averageRoundCount /= len(returnList)
    return averageRoundCount


if __name__ == "__main__":
    args = []
    wordLength = 5
    initialLength = 4
    wordList = loadWordleSet()
    wordListBackup = wordList.copy()
    nLetterWords = loadAllNLetterWords(wordLength)[0]
    returnList = []
    funcArgs = []
    alphabetAsList = list(string.ascii_lowercase)
    initialGameStates = []
    for subset in itertools.combinations(alphabetAsList, initialLength):
        initialGameStates.append(subset)
    returnList = []
    averages = []
    for gameState in initialGameStates:
        with open("wordleResults.txt", 'w') as f:
            f.write("")
        f.close()   

        for word in wordList:
            funcArgs.append((word, gameState, nLetterWords))

        with Pool(16) as p:
            for x in p.imap(wordleMultiProcessing, funcArgs):
                with open("wordleResults.txt", 'a') as lf:
                    returnList.append(x)
                    stringToWrite = ""
                    for i in range(len(x)):
                        stringToWrite += str(x[i])
                        if i < len(x) - 1:
                            stringToWrite += " | "
                    stringToWrite += "\n"
                    lf.write(stringToWrite)
                lf.close()

        gameStates = dict()
        tmpRoundCounts = []
        stringsToWrite = []
        with open("wordleResults.txt") as wrf:
            lines = wrf.readlines()
            for line in lines:
                gameState, word, roundCount = line.strip('\n').split(' | ')
                if gameState not in gameStates and tmpRoundCounts != 0:
                    avg = tmpRoundCounts.sum() / len(tmpRoundCounts)
                    strToWrite = gameState + ' | ' + str(avg) + '\n'
                    stringsToWrite.append(gameState)
                    tmpRoundCounts.clear()
                else:
                    tmpRoundCounts.append(int(roundCount))

            wrf.close()