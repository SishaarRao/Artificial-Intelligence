from __future__ import print_function
from NeighborContainer import *
from AllNeighbors import *
from collections import OrderedDict

def main():
    global elem, word1, word2
    elem = run()
    while True:
        word1 = input("Word 1: ")
        if word1 == "end":
            quit()
        word2 = input("Word 2: ")
        if word2 == "end":
            quit()
        trace = depthFirstSearchIterDeep()
        
        if not trace == None:
            trace.reverse()
            print(len(trace))
            for a in trace:
                print(a.word)
        else:
            print("No path available")


def depthFirstSearchIterDeep():
    global elem, word1, word2, queue, recDepths

    recDepths = {}
    recDepths[word1] = 1
    for i in range(1,50):
        queue = []
        index = search(elem, word1, len(elem)-1, 0)
        queue.append([elem[index]])
        num = check(i)
        if not num == -1:
            return num
    return None

def check(depth):
    global elem, word1, word2, recDepths
    used = {}
    used[word1] = None
    while True:
        if len(queue) == 0:
            return -1
        pos = len(queue) - 1 #get last value
        if len(queue[pos]) < depth:
            neighbors = queue[pos][0].neighbors #neighbors of first term in last pos
            for a in neighbors:
                if a == word2:
                    queue[pos].insert(0, elem[search(elem, a, len(elem) - 1, 0)])
                    return queue[pos]
                    break
                else:
                    if not a in used.keys():
#                        used[a] = None                       
                        if not a in recDepths.keys() or (len(queue[pos]) + 1) <= recDepths[a]:
                            used[a]=None
                            recDepths[a] = len(queue[pos]) + 1
                            arr = [elem[search(elem, a, len(elem) - 1, 0)]] + queue[pos]
                            queue.append(arr)
                                
        queue.pop(pos)
            
    return -1

main()
