import math
import graph
import random
from itertools import permutations
def generateGraph(mat):
    #generate the graph object skipping the initialization with filename.
    # I provide this function this dists table and the function will generate
    # a graph object from it

    g = object.__new__(graph.Graph)
    g.n = len(mat)
    #deep copy for the actual dists table
    g.dists = [[mat[i][j] for j in range(g.n)] for i in range(g.n)]
    g.perm = list(range(g.n))
    return g

def generateSmallGraph():
     n = random.randint(6,10)
     visitedCouple = []
     mat = [[0]*n for i in range(n)]
     for i in range(n):
         for j in range(n):
             if (i,j) not in visitedCouple:
                if i==j:
                    mat[i][j] = 0
                else:
                    mat[i][j] = random.randint(10,100)
                    mat[j][i] = mat[i][j]
                visitedCouple.append((i,j))
                visitedCouple.append((j,i))
     g = generateGraph(mat)
     return g

def optimalTour(g):
  minimalPath = math.inf
  perms = permutations(g.perm)
  for perm in perms:
      g.perm = perm
      value = g.tourValue()
      if value < minimalPath:
          minimalPath = value
  g.perm = list(range(g.n))
  return minimalPath

def testSmallGraphs():
    print("nr Orig Swap TwoOPt Togeth Greed MyPart Optimal")
    for i in range(5):
        g = generateSmallGraph()
        res0 = g.n
        res1 = g.tourValue()
        g.swapHeuristic()
        res2 = g.tourValue()
        g.perm = list(range(g.n))
        g.TwoOptHeuristic()
        res3 = g.tourValue()
        g.perm = list(range(g.n))
        g.swapHeuristic()
        g.TwoOptHeuristic()
        res4 = g.tourValue()
        g.perm = list(range(g.n))
        g.Greedy()
        res7 = g.tourValue()
        g.perm = list(range(g.n))
        g.myPartC()
        res5 = g.tourValue()
        res6 = optimalTour(g)
        print(res0," ",res1,res2," " ,res3," ",res4," ",res7," ",res5," ",res6)

def generateBigGraph():
     n = random.randint(50,200)
     visitedCouple = []
     mat = [[0]*n for i in range(n)]
     optimal=0
     for i in range(n):
         for j in range(n):
             if (i,j) not in visitedCouple:
                if i==j :
                    mat[i][j] = 0
                elif j==(i+1)%n :
                    mat[i][j] = random.randint(10,50)
                    mat[j][i] = mat[i][j]
                    optimal+=mat[i][j]
                         
                else :
                    mat[i][j] = random.randint(70,100)
                    mat[j][i] = mat[i][j]    
                visitedCouple.append((i,j))
                visitedCouple.append((j,i))
     optimal+=mat[n-1][0]
     visited = []
     for i in range(n):
        for j in range(n):
         if(i,j) not in visited:
          index = random.randint(0,j)
          if j!=i and index !=i:
              a = mat[i][j]
              mat[i][j] = mat[i][index]
              mat[i][index] = a
              mat[j][i] = mat[i][j]
              mat[index][i] = mat[i][index]
          visited.append((i,j))      
     g = generateGraph(mat)
     return optimal,g                      
               
            

