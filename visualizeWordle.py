from black import main
from matplotlib import pyplot as plt


def visualizeWordle(word_list, word_count_list, title):
    plt.bar(word_list, word_count_list, color='b')
    plt.xlabel("Word")
    plt.ylabel("Round Count")
    plt.title(title)
    plt.show()

def main():
    word_list = []
    roundCountList = []
    with open("distr.txt", "r") as f:
        for line in f:
            word, roundCount = line.strip('\n').split(',')
            word_list.append(word)
            roundCountList.append(int(roundCount))
        f.close()
    # visualizeWordle(word_list, roundCountList, "Wordle Data")
    print("Average Round Count:", sum(roundCountList) / len(roundCountList))


if __name__ == "__main__":
    main()