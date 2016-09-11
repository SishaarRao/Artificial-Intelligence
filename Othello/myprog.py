##################################################
#
# Torbert, 18 December 2015
#
##################################################
#
from sys import argv
from sys import stdout
#
##################################################
#
theE = ' '
theX = '+'
theO = 'O'

def pr( x ) :
   #
   print( x )       # index = 0 or 1 or ... or 63
   #
   stdout . flush() # so the moderator can see it
   #
#
##################################################
#

def inbounds(pos):
   r = int(pos / 8)
   c = pos % 8
   return 0 <= r < 8 and 0 <= c < 8

def surrounded(myboard, mypiece, pos, pattern):
   otherpiece = theX
   if otherpiece == mypiece:
      otherpiece = theO
   if inbounds(pos):
      temp = pos + pattern
      if myboard[temp] == otherpiece:
         while inbounds(temp):
            temp = temp + pattern
            if myboard[temp] == mypiece:
               return (False, -1)
            if myboard[temp] == theE:
               return (True, temp)
   return (False, -1)
   
def change(myboard, mypiece, pos, pattern):
   otherpiece = theX
   if otherpiece == mypiece:
      otherpiece = theO
   pos = pos + pattern
   while not myboard[pos] == mypiece:
      myboard[pos] = mypiece
      pos = pos + pattern

def genPossibilities(myboard, mypiece):
   possibilities = []   
   pattern = {"n": -8, "s": 8, "e": 1, "w": -1, "nw": -7, "sw": 7, "ne": -9, "se":9}
   for pos in range (0, len(myboard)):
      if myboard[pos] == mypiece:         
         for j in pattern:
            temp = surrounded(myboard, mypiece, pos, pattern[j])
            if temp[0]:
               possibilities.append(temp[1])
               #break
   return possibilities

def score(myboard):
   count = 0
   for i in myboard:
      if i == theX:
         count = count + 1
      else:
         count = count - 1
   #theX - theO
   return count

def moveAlphaBeta2(myboard, depth, alpha, beta, player):
   poss = genPossibilities(myboard, player)
   #theX = maximizing player
   #theO = minimizing player
   if depth == 0 or len(poss) == 0:
      return score(myboard)
   if player == theX:
      temp = -1000
      for a in poss:
         tempboard = myboard
         tempboard[a] = theX
         temp = max(temp, moveAlphaBeta2(myboard, depth - 1, alpha, beta, theO))
         alpha = max(alpha, temp)
         if beta <= alpha:
            break
      return temp
   else:
      temp = 1000
      for a in poss:
         tempboard = myboard
         tempboard[a] = theO
         temp = min(temp, moveAlphaBeta2(myboard, depth - 1, alpha, beta, theX))
         beta = min(beta, temp)
         if beta <= alpha:
            break
      return temp


def moveAlphaBeta(myboard, depth, alpha, beta, player):
   poss = genPossibilities(myboard, player)
   #theX = maximizing player
   #theO = minimizing player
   print(poss)
   if depth == 0 or len(poss) == 0:
      return score(myboard)
   if player == theX:
      temp = -1000
      move = 0
      for a in poss:
         tempboard = myboard
         tempboard[a] = theX
         moveVal = (moveAlphaBeta(tempboard, depth - 1, alpha, beta, theO))[0]
         if temp > moveVal:
            temp = moveVal
            move = a
         alpha = max(alpha, temp)
         if beta <= alpha:
            break
      return (temp, move)
   else:
      temp = 1000
      move = 0
      for a in poss:
         tempboard = myboard
         tempboard[a] = theO
         moveVal = (moveAlphaBeta(tempboard, depth - 1, alpha, beta, theX))[0]
         if temp < moveVal:
            temp = moveVal
            move = a
         beta = min(beta, temp)
         if beta <= alpha:
            break
      return (temp, move)
   
      
#
def display(theboard):
   print("-------------------")
   for i in range (0, 8):
      toPrint = "| "
      for j in range(0, 8):
         toPrint = toPrint + theboard[(i * 8) + j] + " "
      print(toPrint + "|")
   print("-------------------")
#
def main( mypiece ) :
   #
   # myboard = list of 64 chars
   # mypiece =          1 char
   #
   # row-major order ...  8 x  8
   # zero-indexed    ...  0 - 63
   #
   # print out the index where we place "mypiece"
   #
   #pr( 0 ) # corner at the top-left
   #pr(  7 ) # corner at the top-right
   #pr( 63 ) # corner at the bottom-right
   #pr(  0 )
   #pr(  0 ) # only thei last-printed move is made
   #
   myboard = [ theE ] * 64
#
   myboard[27] = theX
   myboard[36] = theX
   myboard[28] = theO
   myboard[35] = theO
   val = moveAlphaBeta(myboard, 0, -1000, 1000, mypiece)
   myboard[val] = mypiece
   display(myboard)
#
##################################################
#
##if len( argv ) == 3 :
##   #
##   myboard = argv[1] # 64 chars
##   mypiece = argv[2] #  1 char
##   #
##   n = len( myboard )
##   m = len( mypiece )
##   #
##   if n == 64 and m == 1 :
##      #
##      myboard = list( myboard )
##      #
##      main( myboard , mypiece )
      #
   #
#
main(theO)
##################################################
#
# end of file
#
##################################################
