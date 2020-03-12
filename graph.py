import math


def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)
                
class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):
         self.dists = []
         points = []
         if n==-1 :
              a = 0
              file = open(filename)
              for line in file:
                  point=[0]*2
                  x,y= line.strip().split()
                  point[0] = int(x)
                  point[1] = int(y)
                  points.append(point)
                  a+=1
              self.n = a
              for i in range(a):
                dist = []
                for j in range(a):
                  dist.append(euclid(points[i],points[j]))
                self.dists.append(dist)
         else :
              self.dists = [[0]*n for i in range(n)]
              self.n = n
              file = open(filename)
              for line in file:
                  x,y,c = line.strip().split()
                  des = int(c)
                  x = int(x)
                  y = int(y)
                  self.dists[x][y] = des
                  self.dists[y][x] = des
         self.perm = [0] * self.n
         for i in range(self.n):
            self.perm[i] = i        








            
        


    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        tour_value=0
        for i in range(self.n-1):
          tour_value+=self.dists[self.perm[i]][self.perm[i+1]]
        tour_value+=self.dists[self.perm[self.n-1]][self.perm[0]]
        return tour_value  

        

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        return 0


    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def  tryReverse(self,i,j):


     def swapHeuristic(self):
        better = True
        while better:
            better = False
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self):
        better = True
        while better:
            better = False
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True
                

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        return 0
