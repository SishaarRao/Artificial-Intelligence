from __future__ import print_function
import time


def main():
   global currPuzzle
   puzzles = open("sudoku128.txt").read().split("\n")
   max1 = (-1, 0)
   max2 = (-1, 0)
   max3 = (-1, 0)
   
   #for j in [56, 78, 84]:
   for j in range(16, 17):
      string = puzzles[j]
      currPuzzle = []
      for i in range(0,len(string)):
         currPuzzle.append(string[i])
   
      #puzzlePrint(currPuzzle)
      start_time = time.time()
      solved = solve2(currPuzzle)
      s = (time.time() - start_time)
      #puzzlePrint(solved)
      if solved == False:
         print("failure")
      print(j, "  --- %s seconds ---" % s)
      if s > max1[1]:
         max1 = (j, s)
      elif s > max2[1]:
         max2 = (j, s)
      elif s > max3[1]:
         max3 = (j, s)
   print(max1, max2, max3)

def possibilitiesList():
   global currPuzzle, myMin
   possibilities = {}
   for i in range(0, len(currPuzzle)):
      if currPuzzle[i] == ".":
         d = genPossibilities(i)
         possibilities[i] = d
         #print(i, "---", d)
         if len(d) < len(myMin[1]) and not len(d) < 2:
            myMin = (i, d)
   return possibilities


def solve2(currPuzzle):
   #puzzlePrint(currPuzzle)
   if isSolution():
      return currPuzzle
   myMin = (-1, 9) #(pos, value)
   for i in range (0, len(currPuzzle)):
      if currPuzzle[i] == ".":
         d = genPossibilities(i, currPuzzle)
         if myMin[1] > len(d):
               myMin = (i, len(d))
               #print(myMin)
         if len(d) == 1:
            currPuzzle[i] = (list(d.keys()))[0]
            #print("Placed ", (list(d.keys()))[0], " in pos ", i)
            temp = solve2(currPuzzle)
            if not temp == False:
               return temp
            currPuzzle[i] = "."
            return False
         if len(d) == 0:
            return False
         ######
         temp2 = forced1(i, currPuzzle)
         if not temp2 == False:
            currPuzzle[i] = temp2
            temp3 = solve2(currPuzzle)
            if not temp3 == False:
               return temp3
            currPuzzle[i] = "."
            return False
         ########
   #at this point, you have to guess
   if isSolution():
      return currPuzzle
   
   for a in genPossibilities(myMin[0], currPuzzle):
      currPuzzle[myMin[0]] = a
      #print("Guessed ", a, " in pos ", myMin[0])
      temp = solve2(currPuzzle)
      if not temp == False:
         return temp
      print("Wrong Guess: ", a, " in pos ", myMin[0])
   currPuzzle[myMin[0]] = "."
   return False

def puzzlePrint(curr):
   print("-----------------------")
   for i in range(0, 9):
      toPrint = "| "
      for j in range(0, 9):
         toPrint = toPrint + str(curr[i*9 + j]) + " "
         if (j + 1)%3 == 0:
            toPrint = toPrint + "|"
      print(toPrint)
      if (i + 1)%3 == 0:
         print("-----------------------")


def forced1(pos, currPuzzle):
   rows = genRowsPossibilities(pos, currPuzzle)
   currPossibilities = genPossibilities(pos, currPuzzle)
   for a in rows:
      if a in currPossibilities:
         del currPossibilities[a]
   if len(currPossibilities) == 1:
      return (list(currPossibilities.keys()))[0]
   cols = genColsPossibilities(pos, currPuzzle)
   currPossibilities = genPossibilities(pos, currPuzzle)
   for a in cols:
      if a in currPossibilities:
         del currPossibilities[a]
   if len(currPossibilities) == 1:
      return (list(currPossibilities.keys()))[0]
   square = genSquarePossibilities(pos, currPuzzle)
   currPossibilities = genPossibilities(pos, currPuzzle)
   for a in square:
      if a in currPossibilities:
         del currPossibilities[a]
   if len(currPossibilities) == 1:
      return (list(currPossibilities.keys()))[0]
   return False

def isSolution():
   global currPuzzle
   if "." in currPuzzle:
      return False
   for r in range(0, 9):
      rowPoss = {}
      for i in range (1, 10):
         rowPoss[i] = 0
      for c in range(0, 9):
         if int(currPuzzle[r*9 + c]) in rowPoss:
            rowPoss[int(currPuzzle[r*9 + c])] = rowPoss[int(currPuzzle[r*9 + c])] + 1
         if rowPoss[int(currPuzzle[r*9 + c])] > 1:
            return False
   for c in range(0, 9):
      colPoss = {}
      for i in range (1, 10):
         colPoss[i] = 0
      for r in range(0, 9):
         if int(currPuzzle[r*9 + c]) in colPoss:
            colPoss[int(currPuzzle[r*9 + c])] = colPoss[int(currPuzzle[r*9 + c])] + 1
         if colPoss[int(currPuzzle[r*9 + c])] > 1:
            return False
   return True

def genPossibilities(pos, currPuzzle):
   possibilities = {}
   for i in range(1, 10):
      possibilities[i] = None
   nbrs = genNbrs(pos)
   for i in nbrs:
      if not str(currPuzzle[i[0]*9 + i[1]]) == "." and int(currPuzzle[i[0]*9 + i[1]]) in possibilities:
         del possibilities[int(currPuzzle[i[0]*9 + i[1]])]
   return possibilities

def genNbrs(pos):
   index = []
   row = int(pos / 9)
   col = pos % 9
   for i in range(0, 9):
      if not row == i:
         index.append((i, col))
      if not col == i:
         index.append((row, i))
   rowPos = row%3
   colPos = col%3
   for i in range(row - rowPos, row - rowPos + 3):
      for j in range(col - colPos, col - colPos + 3):
         if not i == row or not j == col:
            index.append((i, j))
   return index

def genRowsPossibilities(pos, currPuzzle):
   index = {}
   row = int(pos / 9)
   col = pos % 9
   for i in range(0, 9):
      if not row == i:
         d = genPossibilities(i*9 + col, currPuzzle)
         for a in d:
            if not a in index:
               index[a] = None
   return index
   
def genColsPossibilities(pos, currPuzzle):
   index = {}
   row = int(pos / 9)
   col = pos % 9
   for i in range(0, 9):
      if not col == i:
         d = genPossibilities(row*9 + i, currPuzzle)
         for a in d:
            if not a in index:
               index[a] = None
   return index

def genSquarePossibilities(pos, currPuzzle):
   index = {}
   row = int(pos / 9)
   col = pos % 9
   rowPos = row%3
   colPos = col%3
   for i in range(row - rowPos, row - rowPos + 3):
      for j in range(col - colPos, col - colPos + 3):
         if not i == row or not j == col:
            d = genPossibilities(i*9 + j, currPuzzle)
            for a in d:
               if a in index:
                  index[a] = None
   return index 

main()
