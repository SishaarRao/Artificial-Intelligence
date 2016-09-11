from __future__ import print_function
from NeighborContainer import *
from day1v1 import *



def main():
    words = open("words.txt").read().split()
    elem = []
    nums = []
    data = [None]*16
    dataCorrespondence = [None]*16
    for i in range(0, len(words)):
        elem.append(NeighborContainer(words[i]))
    for i in range(0, len(elem)):
        myData = getNeighbors(elem, elem[i].word)
        if data[len(myData)] == None:
            data[len(myData)] = 1
            dataCorrespondence[len(myData)] = [i]
        else:
            data[len(myData)] = data[len(myData)] + 1
            dataCorrespondence[len(myData)].append(i)
    for i in range(0, len(data)):
        if data[i] == None:
            print(i, " ", 0)
        elif data[i] > 3:
            print(i, " ", data[i])
        else:
            print(i, " ", data[i])
            for a in dataCorrespondence[i]:
                print(elem[a].word, " ",elem[a].neighbors)

def run():
    words = open("words.txt").read().split()
    elem = []
    nums = []
    data = [None]*16
    dataCorrespondence = [None]*16
    for i in range(0, len(words)):
        elem.append(NeighborContainer(words[i]))
    for i in range(0, len(elem)):
        getNeighbors(elem, elem[i].word)
    return elem
        
#main()
