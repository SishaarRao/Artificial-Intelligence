from __future__ import print_function
from NeighborContainer import *
from AllNeighbors import *
from collections import OrderedDict

def main():
    global elem, word1, word2
    elem = run()
    while True:
        word1 = input("Word 1: ")
        word2 = input("Word 2: ")
        if word1 == "end" or word2 == "end":
            quit()
        trace = depthFirstSearchStack()
        trace.reverse()
        if not trace == None:
            print(len(trace))
            for a in trace:
                print(a.word)


def depthFirstSearchStack():
    global elem, word1, word2, queue
    queue = []
    index = search(elem, word1, len(elem)-1, 0)
    queue.append([elem[index]])
    return check()

def check():
    global elem, word1, word2
    used = {}
    used[word1] = None
    while True:
        if len(queue) == 0:
            print("no path available")
            break
        pos = len(queue) - 1 #get last value
        neighbors = queue[pos][0].neighbors #neighbors of first term in last pos
        for a in neighbors:
            if a == word2:
                queue[pos].insert(0, elem[search(elem, a, len(elem) - 1, 0)])
                return queue[pos]
                break
            else:
                if not a in used.keys():
                    used[a] = None
                    arr = [elem[search(elem, a, len(elem) - 1, 0)]] + queue[pos]
                    queue.append(arr)
        queue.pop(pos)

main()
