#
#
#Neighbor data structure
class NeighborContainer:
   word = ""
   neighbors = []

   def __init__(self, a):
      self.word = a
      self.neighbors = []
   
   def compare(self, a):# 1 = 1 letter in common 2 = more than one letter
      flag = 0
      for i in range (0, len(a)):
         if not a[i] == self.word[i]:
            flag = flag + 1
         if flag > 1:
            return 2
      return flag
	    
         
   
      
   
   


#
#
