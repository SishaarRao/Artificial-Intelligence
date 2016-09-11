from __future__ import print_function
from NeighborContainer import *
from AllNeighbors import *
import time



def main():
    global elem, word1, word2, wordsVisited, maxLenOfQ
    elem = run()
    wordsVisited = 0
    maxLenOfQ = 0
    while True:
        word1 = input("Word 1: ")
        if word1 == "end":
            quit()
        word2 = input("Word 2: ")
        if word2 == "end":
            quit()
        start_time = time.time()
        trace = aStarSearch()
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Words visited: ", wordsVisited)
        print("Max Length of Queue: ", maxLenOfQ)
        if not trace == None:
            print(len(trace))
            trace.reverse()
            for a in trace:
                print(a.word)


def aStarSearch():
    global elem, word1, word2, queue, wordsVisited, maxLenOfQ
    queue = []
    index = search(elem, word1, len(elem)-1, 0)
    queue.append([distanceTo(word1, word2), [elem[index]]])
    return check()

def check():
    global elem, queue, word1, word2, wordsVisited, maxLenOfQ
    used = {}
    used[word1] = None
    while True:
        if len(queue) == 0:
            print("no path available")
            break
        neighbors = queue[0][1][0].neighbors
        for a in neighbors:
            if len(queue[0]) > maxLenOfQ:
                maxLenOfQ = len(queue[0])
            if a == word2:
                queue[0][1].insert(0, elem[search(elem, a, len(elem) - 1, 0)])
                wordsVisited = len(used.keys())
                return queue[0][1]
            else:
                if not a in used:
                    insert([elem[search(elem, a, len(elem) - 1, 0)]] + queue[0][1])
                    used[a] = None
        queue.pop(0)
    wordsVisited = len(used.keys())

def insert(tempArr):
    global queue, word1
    val = len(tempArr) + distanceTo(tempArr[0].word, word2)#f(n) = g(n) + h(n)
    flag = False
    for i in range (1, len(queue)):
        if val < queue[i][0]:
            queue.insert(i, [val, tempArr])
            flag = True
    if not flag:
        queue.append([val, tempArr])
    
def distanceTo(myWord, target):
    global word2
    count = 0
    for i in range(len(target)):
        if not word2[i] == myWord[i]:
            count = count + 1
    return count
main()
