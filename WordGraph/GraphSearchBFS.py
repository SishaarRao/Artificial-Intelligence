from __future__ import print_function
from NeighborContainer import *
from AllNeighbors import *

def main():
    global elem, word1, word2
    elem = run()
    while True:
        word1 = input("Word 1: ")
        word2 = input("Word 2: ")
        if word1 == "end" or word2 == "end":
            quit()
        trace = breadthFirstSearch()
        if not trace == None:
            print(len(trace))
            for a in trace:
                print(a.word)


def breadthFirstSearch():
    global elem, word1, word2, queue
    queue = []
    index = search(elem, word1, len(elem)-1, 0)
    queue.append([elem[index], None])
    return check()

def check():
    global elem, queue
    index = 0
    while True:
        if index >= len(queue):
            print("no path available")
            break
        neighbors = queue[index][0].neighbors
        for a in neighbors:
            if a == word2:
                queue.append([elem[search(elem, a, len(elem) - 1, 0)], index])
                return traceBack()
                break
            else:
                if not alreadyIn(a):
                    queue.append([elem[search(elem, a, len(elem) - 1, 0)], index])
                #print(queue[len(queue)-1][0].word,": ", queue[len(queue)-1][1])
        index = index + 1

def traceBack():
    global queue
    pos = len(queue) - 1
    trace = []
    while not queue[pos][1] == None:
        trace.insert(0, queue[pos][0])
        pos = queue[pos][1]
    trace.insert(0, queue[pos][0])
    return trace

def alreadyIn(a):
    global queue
    for packet in queue:
        if packet[0].word == a:
            return True
    return False

main()
