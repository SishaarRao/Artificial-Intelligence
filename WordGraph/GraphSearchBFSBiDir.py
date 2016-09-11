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
    global elem, word1, word2, queue, queue2
    queue = []
    queue2 = []
    index = search(elem, word1, len(elem)-1, 0)
    index2 = search(elem, word2, len(elem)-1, 0)
    queue.append([elem[index], None])
    queue2.append([elem[index2], None])
    return check()

def check():
    global elem, queue, queue2, word2, word1
    index = 0
    while True:
        if index >= len(queue) or index > len(queue2):
            print("no path available")
            break
        neighbors = queue[index][0].neighbors
        for a in neighbors:
            if a == word2:
                queue.append([elem[search(elem, a, len(elem) - 1, 0)], index])
                return traceBack(queue)
                break
            else:
                if not alreadyIn(a):
                    queue.append([elem[search(elem, a, len(elem) - 1, 0)], index])

        if queue[len(queue)-1][0] == queue2[len(queue2)-1][0]:
            arr = traceback(queue2)
            arr.reverse()
            return traceback(queue) + arr

        
        neighbors = queue2[index][0].neighbors
        for a in neighbors:
            if a == word1:
                queue2.append([elem[search(elem, a, len(elem) - 1, 0)], index])
                return traceBack(queue2)
                break
            else:
                if not alreadyIn(a):
                    queue2.append([elem[search(elem, a, len(elem) - 1, 0)], index])
        index = index + 1

def traceBack(queue):
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
