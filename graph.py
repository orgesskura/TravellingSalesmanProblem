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
                    break
            self.perm[counter]=i
            nodes.remove(i)


    def linKernighan(self):
            prevDistance = 0
            newDistance = self.tourValue()
            cond = True
            m = 10
            while cond:
                prevDistance = newDistance
                self.improve()
                newDistance = self.tourValue()
                m -=1
                if newDistance >= prevDistance  or m<0:
                    cond = False

    def improve(self):
            for i in range(self.n):
                self.improveTour(i, False)

    def improveTour(self, node1, cond):
            node2 = 0
            if cond:
                node2 = (node1-1)%self.n
            else:
                node2 = ((node1+1)%self.n)
            node3 = self.getNearestNeighbor(node2)
            if node3!= -1 and self.getDistance(node2,node3) < self.getDistance(node1,node2):
                self.mainAlgorithm(node1,node2,node3)
            else:
                if not cond :
                    self.improveTour(node1, True)

    def getNearestNeighbor(self, idx):
            minimum = 3000000000
            node = -1
            ourNode = self.perm[idx]
            for i in range(self.n):
                if i!=ourNode:
                    dist = self.dists[i][ourNode]
                    if dist < minimum:
                        node = self.getIndex(i)
                        minimum = dist
            return node 
            
            
    def mainAlgorithm(self, node1, node2, node3):
            tIdx = []
            tIdx.insert(0, -1)
            tIdx.insert(1, node1)
            tIdx.insert(2, node2)
            tIdx.insert(3, node3)
            initialGain = self.getDistance(node1,node2) - self.getDistance(node2,node3)
            gStar = 0
            gi = initialGain
            k = 3
            i = 4
            while True:
                newT = self.selectNewT(tIdx)
                if newT == -1:
                    break
                tIdx.insert(i, newT)
                tiplus1 = self.getNextPossibleY(tIdx)
                if tiplus1 == -1:
                    break
                gi+= self.getDistance(tIdx[len(tIdx) - 2],newT)
                if gi - self.getDistance(newT,node1)> gStar:
                    gStar = gi - self.getDistance(newT,node1)
                    k = i
                tIdx.append(tiplus1)
                gi -= self.getDistance(newT,tiplus1)
                i+=2
            if gStar > 0:
                tIdx[k+1] = tIdx[1]
                self.perm = self.getTPrime(tIdx, k)

    def getNextPossibleY(self, tIdx):
            ti = tIdx[len(tIdx)-1]
            ys = []
            for i in range(self.n):
                if self.isDisjunctive(tIdx, i, ti) == False:
                    continue
                if self.isPositiveGain(tIdx, i) == False:
                    continue
                if self.nextXPossible(tIdx, i) == False:
                    continue
                ys.append(i)
            minDist = 3000000000.0
            minNode = -1
            for i in ys:
                if self.getDistance(ti,i) < minDist:
                    minNode = i
                    minDist = self.getDistance(ti,i)
            return minNode

    def nextXPossible(self, tIdx, i):
            return self.isConnected(tIdx, i, (i+1)%self.n) or self.isConnected(tIdx, i, (i-1)%self.n)

    def isConnected(self, tIdx, x, y):
            if x==y:
                return False
            for i in range(1, len(tIdx)-1, 2):
                if tIdx[i]==x and tIdx[i+1]==y:
                    return False
                if tIdx[i]==y and tIdx[i+1]==x:
                    return False
            return True

    def isPositiveGain(self, tIdx, ti):
            gain = 0.0
            for i in range(1, len(tIdx)-2):
                t1 = tIdx[i]
                t2 = tIdx[i+1]
                t3 = 0
                if i==len(tIdx)-3:
                    t3 = ti
                else:
                    t3 = tIdx[i+2]
                gain+=self.getDistance(t2,t3) - self.getDistance(t1,t2)
            if gain>0:
                return True
            return False

    def selectNewT(self, tIdx):
            option1 = (tIdx[len(tIdx)-1]-1)%self.n
            option2 = (tIdx[len(tIdx)-1]+1)%self.n
            tour1 = self.constructNewTour2(self.perm, tIdx, option1)
            if self.isTour(tour1) == True:
                return option1
            else:
                tour2 = self.constructNewTour2(self.perm, tIdx, option2)
                if self.isTour(tour2) == True:
                    return option2
            return (-1)

    def constructNewTour2(self, tour, tIdx, newItem):
            changes = tIdx.copy()
            changes.append(newItem)
            changes.append(changes[1])
            return self.constructNewTour(tour, changes)

    def isTour(self, tour):
            if len(tour) != self.n:
                return False
            for i in range(self.n-1):
                for j in range(i+1,self.n):
                    if tour[i]==tour[j]:
                        return False
            return True

    def getTPrime(self, tIdx, s):
            list1 = [tIdx[i] for i in range(s+2)]
            return self.constructNewTour(self.perm, list1)

    def constructNewTour(self, tour, changes):
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

    def deriveX(self, changes):
            es = []
            for i in range(1, len(changes)-2, 2):
                e = Edge(self.perm[changes[i]], self.perm[changes[i+1]])
                es.append(e)
            return es

    def deriveY(self, changes):
            es = []
            for i in range(2, len(changes)-1, 2):
                e = Edge(self.perm[changes[i]], self.perm[changes[i+1]])
                es.append(e)
            return es

    def deriveEdgesFromTour(self, tour):
            es = []
            for i in range(len(tour)):
                e =Edge(tour[i], tour[(i+1)%len(tour)])
                es.append(e)
            return es

    def isDisjunctive(self, tIdx, x, y):
            if x==y:
                return False
            for i in range(len(tIdx)-1):
                if tIdx[i] == x and tIdx[i+1] == y:
                    return False
                if tIdx[i] == y and tIdx[i+1] == x:
                    return False
            return True

    def getIndex(self, node):
            for i in range(self.n):
                if node == self.perm[i]:
                    return i
            return -1

    def getDistance(self,a,b):
        return self.dists[self.perm[a]][self.perm[b]]


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

               
