from __future__ import print_function
from NeighborContainer import *
#
#
#
#

def search(elem, target, upper, lower):
   index = int((upper + lower)/2)
   if upper - lower == 1 and not elem[upper] == target and not elem[lower] == target:
      return -1
   if elem[index].word > target:
      return search(elem, target, index, lower)
   elif elem[index].word < target:
      return search(elem, target, upper, index)
   elif elem[index].word == target:
      return index
   else:
      return -1

def manipulateFirst(elem, index):
   for a in "abcdefghijklmnopqrstuvwxyz":
      tempIndex = search(elem, a + elem[index].word[1:], len(elem)-1, 0)
      if not tempIndex == -1 and not elem[index] == elem[tempIndex]:
         elem[index].neighbors.append(elem[tempIndex].word)

def honeUpper(elem, index, key):
   temp1 = index
   while elem[temp1].word[:key] == elem[index].word[:key] and temp1>=0:#while keys match
      temp1 = temp1 - 10
   for i in range(11):
      if elem[temp1+i].word[:key] == elem[index].word[:key]:
         return temp1+i
   return temp1

def honeLower(elem, index, key):
   temp1 = index
   #print(index)
   while temp1< len(elem) and (elem[temp1].word[:key] == elem[index].word[:key]):#while keys match
      temp1 = temp1 + 10
   for i in range(11):
      if temp1 - i < len(elem) and temp1 - i >= 0 and elem[temp1-i].word[:key] == elem[index].word[:key]:
         return temp1-i
   return temp1


def run():
   words = open("words.txt").read().split()
   
   elem = []
   #print(words)
   for i in range(0, len(words)):
      elem.append(NeighborContainer(words[i]))
   myInput = input("Prompt: ") + ""
   print(myInput)
   index = search(elem, myInput, len(elem)-1, 0)
   #word has been located at index
   manipulateFirst(elem, index)
   for i in range(1, len(elem[index].word)):
      upper = honeUpper(elem, index, i)
      lower = honeLower(elem, index, i)
      for j in range(upper, lower):
         if elem[index].compare(elem[j].word) == 1 and not elem[j].word in elem[index].neighbors:
            elem[index].neighbors.append(elem[j].word)
   print(elem[index].neighbors)


def getNeighbors(elem, myInput):
   index = search(elem, myInput, len(elem)-1, 0)
   #word has been located at index
   manipulateFirst(elem, index)
   for i in range(1, len(elem[index].word)):
      upper = honeUpper(elem, index, i)
      lower = honeLower(elem, index, i)
      for j in range(upper, lower):
         if elem[index].compare(elem[j].word) == 1 and not elem[j].word in elem[index].neighbors:
            elem[index].neighbors.append(elem[j].word)
   return elem[index].neighbors

#run()
#
#
