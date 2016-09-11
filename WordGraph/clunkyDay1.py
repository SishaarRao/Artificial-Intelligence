from __future__ import print_function
from NeighborContainer import *

def compare(word, a):# 0= no different letters 1= 1 different letter 2=more than 1
   flag = False
   for i in range (0, len(a)):
      if flag == False and not a[i] == word[i]:
         flag = True
      elif flag == True and not a[i] == word[i]:
         return 2
   return 1

def main():
   words = open("words.txt").read().split()
   word = input("Prompt: ")
   for temp in words:
      if compare(word, temp) == 1:
         print(temp)
main()
