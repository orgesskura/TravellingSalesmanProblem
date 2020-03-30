import math
import random


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
            minimum=[j  for j in nodes if self.dists[i][j]==min_nr]
            for k in nodes:
                if k in minimum:
                    i = k
                    break
            self.perm[counter]=i
            nodes.remove(i)

    # algorithm for part C : I chose Lin-Kerninghan Heuristic for Part C
    # this is the main method where we constanly try to improve the tour value
    def myPartC(self):
            prevDistance = 0
            newDistance = self.tourValue()
            cond = True
            while cond:
                prevDistance = newDistance
                self.improveAll()
                newDistance = self.tourValue()
                if newDistance >= prevDistance:
                    cond = False

    # improves the tour
    def improveAll(self):
            for i in range(self.n):
                self.improveTour(i, False)

    # improves the tour starting from node1
    def improveTour(self, node1, cond):
            node2 = 0
            if cond:
                node2 = (node1-1)%self.n
            else:
                node2 = ((node1+1)%self.n)
            node3 = self.nearestNeighbor(node2)
            if node3!= -1 and self.getDistance(node2,node3) < self.getDistance(node1,node2):
                self.mainAlgorithm(node1,node2,node3)
            else:
                if not cond :
                    self.improveTour(node1, True)
    #get index of the nearest neighbor of idx which is the index of the node we want in self.perm
    def nearestNeighbor(self, idx):
            minimum = math.inf
            node = -1
            ourNode = self.perm[idx]
            for i in range(self.n):
                if i!=ourNode:
                    dist = self.dists[i][ourNode]
                    if dist < minimum:
                        node = self.getIndex(i)
                        minimum = dist
            return node 
            
    #This function is actually the step four from the lin-kernighan's origainnal paper       
    def mainAlgorithm(self, node1, node2, node3):
            list1 = []
            list1.insert(0, -1)
            list1.insert(1, node1)
            list1.insert(2, node2)
            list1.insert(3, node3)
            initialGain = self.getDistance(node1,node2) - self.getDistance(node2,node3)
            g = 0
            gain = initialGain
            k = 3
            i = 4
            while True:
                tour = self.selectTour(list1)
                if tour == -1:
                    break
                list1.insert(i, tour)
                tiplus1 = self.getNextPossibleY(list1)
                if tiplus1 == -1:
                    break
                gain+= self.getDistance(list1[len(list1) - 2],tour)
                if gain - self.getDistance(tour,node1)> g:
                    g = gain - self.getDistance(tour,node1)
                    k = i
                list1.append(tiplus1)
                gain -= self.getDistance(tour,tiplus1)
                i+=2
            if g > 0:
                list1[k+1] = list1[1]
                self.perm = self.getNewTour(list1, k)

    #This function gets all the ys that fit the criterion for step 4
    def getNextPossibleY(self, list1):
            ti = list1[len(list1)-1]
            ys = []
            for i in range(self.n):
                if self.isDisjunctive(list1, i, ti) == False:
                    continue
                if self.isPositiveGain(list1, i) == False:
                    continue
                if self.nextXPossible(list1, i) == False:
                    continue
                ys.append(i)
            minDist = math.inf
            minNode = -1
            for i in ys:
                if self.getDistance(ti,i) < minDist:
                    minNode = i
                    minDist = self.getDistance(ti,i)
            return minNode
    #This function implements the part e from the point 4 of the paper
    def nextXPossible(self, list1, i):
            return self.isConnected(list1, i, (i+1)%self.n) or self.isConnected(list1, i, (i-1)%self.n)

    
    def isConnected(self, list1, x, y):
            if x==y:
                return False
            for i in range(1, len(list1)-1, 2):
                if list1[i]==x and list1[i+1]==y:
                    return False
                if list1[i]==y and list1[i+1]==x:
                    return False
            return True

    def isPositiveGain(self, list1, ti):
            gain = 0.0
            for i in range(1, len(list1)-2):
                t1 = list1[i]
                t2 = list1[i+1]
                t3 = 0
                if i==len(list1)-3:
                    t3 = ti
                else:
                    t3 = list1[i+2]
                gain+=self.getDistance(t2,t3) - self.getDistance(t1,t2)
            if gain>0:
                return True
            return False
    #This function gets a new tour with the characteristics described in the paper in step 4.a.
    def selectTour(self, list1):
            option1 = (list1[len(list1)-1]-1)%self.n
            option2 = (list1[len(list1)-1]+1)%self.n
            tour1 = self.constructtourour2(self.perm, list1, option1)
            if self.isTour(tour1) == True:
                return option1
            else:
                tour2 = self.constructtourour2(self.perm, list1, option2)
                if self.isTour(tour2) == True:
                    return option2
            return (-1)

    def constructtourour2(self, tour, list1, newItem):
            changes = list1.copy()
            changes.append(newItem)
            changes.append(changes[1])
            return self.constructtourour(tour, changes)

    # this function determines if a sequence of nodes is a tour
    def isTour(self, tour):
            if len(tour) != self.n:
                return False
            for i in range(self.n-1):
                for j in range(i+1,self.n):
                    if tour[i]==tour[j]:
                        return False
            return True
    
    # construct a new tour out of tIndex
    def getNewTour(self, tIndex, s):
            list1 = [tIndex[i] for i in range(s+2)]
            return self.constructtourour(self.perm, list1)

    #This function constructs a new Tour deleting the X sets and adding the Y sets
    def constructtourour(self, tour, changes):
            currentEdges = self.deriveEdgesFromTour(tour)
            X = self.deriveX(changes)
            Y = self.deriveY(changes)
            s = len(currentEdges)
            for i in X:
                for j in range(len(currentEdges)):
                    m = currentEdges[j]
                    if i==m:
                        s-=1
                        del currentEdges[j]
                        break
            for i in Y:
                s+=1
                currentEdges.append(i)
            return self.createTourFromEdges(currentEdges, s)

    #This function takes a list of edges and converts it into a tour
    def createTourFromEdges(self, edges, s):
            tour = []
            i = 0
            last = (-1)
            while i<len(edges):
                if edges[i] is not None:
                    tour.append(edges[i].getPoint1())
                    tour.append(edges[i].getPoint2())
                    last = tour[1]
                    break
                i+=1
            del edges[i]
            k = 2
            cond = True
            while cond:
                j = 0
                while j<len(edges):
                    e = edges[j]
                    if e is not None and e.getPoint1() == last:
                        last = e.getPoint2()
                        break
                    else:
                        if e is not None and e.getPoint2() == last:
                            last = e.getPoint1()
                            break
                    j+=1
                if j == len(edges):
                    break
                del edges[j]
                if k>=s:
                    break
                tour.append(last)
                k+=1
            return tour

    #Get the list of edges from the tour index and this will be the list of edges that will be deleted
    def deriveX(self, changes):
            es = []
            for i in range(1, len(changes)-2, 2):
                e = Edge(self.perm[changes[i]], self.perm[changes[i+1]])
                es.append(e)
            return es

    #get the list from the tour index and this will be the list of edges that will be added
    def deriveY(self, changes):
            es = []
            for i in range(2, len(changes)-1, 2):
                e = Edge(self.perm[changes[i]], self.perm[changes[i+1]])
                es.append(e)
            return es
    
    # get a list of the edges of the tour given a tour
    def deriveEdgesFromTour(self, tour):
            es = []
            for i in range(len(tour)):
                e =Edge(tour[i], tour[(i+1)%len(tour)])
                es.append(e)
            return es
    
    #This function allows to check if an edge is already on either X or Y
    def isDisjunctive(self, list1, x, y):
            if x==y:
                return False
            for i in range(len(list1)-1):
                if list1[i] == x and list1[i+1] == y:
                    return False
                if list1[i] == y and list1[i+1] == x:
                    return False
            return True

    # given a specific node we can find the index of that node in the current self.perm
    def getIndex(self, node):
            for i in range(self.n):
                if node == self.perm[i]:
                    return i
            return -1
    # return distance between 2 nodes gainven their indeces in self.perm
    def getDistance(self,a,b):
        return self.dists[self.perm[a]][self.perm[b]]
    
    #create a random tour using the Drunken Sailor Algorithm
    def randomTour(self):
        for i in range(self.n):
            index = random.randint(0,i)
            nr = self.perm[index]
            self.perm[index] = self.perm[i]
            self.perm[i] = nr
    
    # run tests when random tour is used
    def runRandomTours(self):
        for i in range(15):
            self.randomTour()
            self.myPartC()
            print(self.tourValue())
            self.perm = list(range(self.n))

# create an edge object as it is essential to the heuristic to have an edge object
#since we do comparisons with edge values, __eq__,__lt__, and __gt__ are added to edge object to support comparisons
class Edge:
	point1 = 0
	point2 = 0

	def __init__(self, a, b):
		self.point1 = max(a,b)
		self.point2 = min(a,b)

	def __eq__(self, e2):
		return self.equals(e2)

	def __lt__(self, e2):
		if self.getPoint1()<e2.getPoint1() or self.getPoint1() == e2.getPoint1() and self.getPoint2()<e2.getPoint2():
			return True
		return False

	def __gt__(self, e2):
		return e2.__lt__(self)

	def getPoint1(self):
		return self.point1

	def getPoint2(self):
	 	return self.point2

	def equals(self, e2):
		if e2 is None:
			return False
		if self.getPoint1()==e2.getPoint1() and self.getPoint2()==e2.getPoint2():
			return True
		return False

               
