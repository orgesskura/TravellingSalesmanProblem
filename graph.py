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
        for i in range(self.n):
          tour_value+=self.dists[self.perm[i]][self.perm[(i+1)%self.n]]
        return tour_value  

        

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    

    #implement in case we have 2 or 3 nodes
    def trySwap(self,i):
        previous = self.perm[(i-1)%self.n]
        first = self.perm[i]
        second = self.perm[(i+1)%self.n]
        next = self.perm[(i+2)%self.n]
        firstTime = self.dists[previous][first] + self.dists[first][second] + self.dists[second][next]
        secondTime = self.dists[previous][second] + self.dists[second][first] + self.dists[first][next]
        if(firstTime <= secondTime):
            return False
        else:
            self.perm[i] = second
            self.perm[(i+1)%self.n] = first
            return True    
        


    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def  tryReverse(self,i,j):
     currentTour = 0
     probableTour=0
     currentTour+=self.dists[self.perm[(i-1)%self.n]][self.perm[i]]
     probableTour+=self.dists[self.perm[(i-1)%self.n]][self.perm[j]]
     currentTour+=self.dists[self.perm[j]][self.perm[(j+1)%self.n]]
     probableTour+=self.dists[self.perm[i]][self.perm[(j+1)%self.n]]
     perm=[self.perm[i] for i in range(self.n)]
     first=i
     second=j
     while(first<second):
           perm[first] = self.perm[second]
           perm[second] = self.perm[first]
           first=(first+1)%self.n
           second= (second-1)%self.n
        
     if currentTour <= probableTour :
            return False
     else :
            while i<=j:
              self.perm[i] = perm[i]
              i+=1
            return True    
 
            





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
        nodes = [i for i in range(1,self.n)]
        counter = 0
        i = 0
        self.perm[0] = 0
        while len(nodes)>0:
            counter+=1
            min_nr = 0
            min_nr = min([self.dists[i][j] for j in nodes])
            #i = self.dists[i].index(min_nr)
            minimum=[j  for j in nodes if self.dists[i][j]==min_nr]
            for k in nodes:
                if k in minimum:
                    i = k
            self.perm[counter]=i
            nodes.remove(i)

               
