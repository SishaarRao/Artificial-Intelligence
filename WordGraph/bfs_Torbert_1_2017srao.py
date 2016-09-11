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
        word2 = input("Word 2: ")
        if word1 == "end" or word2 == "end":
            quit()
        start_time = time.time()
        trace = breadthFirstSearch()
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Words visited: ", wordsVisited)
        print("Max Length of Queue: ", maxLenOfQ)
        if not trace == None:
            print(len(trace))
            trace.reverse()
            for a in trace:
                print(a.word)


def breadthFirstSearch():
    global elem, word1, word2, queue, wordsVisited, maxLenOfQ
    queue = []
    index = search(elem, word1, len(elem)-1, 0)
    queue.append([elem[index]])
    return check()

def check():
    global elem, queue, word1, word2, wordsVisited, maxLenOfQ
    used = {}
    used[word1] = None
    while True:
        if len(queue) == 0:
            print("no path available")
            break
        neighbors = queue[0][0].neighbors
        for a in neighbors:
            if len(queue[0]) > maxLenOfQ:
                maxLenOfQ = len(queue[0])
            if a == word2:
                queue[0].insert(0, elem[search(elem, a, len(elem) - 1, 0)])
                wordsVisited = len(used.keys())
                return queue[0]
            else:
                if not a in used.keys():
                    queue.append([elem[search(elem, a, len(elem) - 1, 0)]] + queue[0])
                    used[a] = None
        queue.pop(0)
    wordsVisited = len(used.keys())

main()
