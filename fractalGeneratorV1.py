from PIL import Image
from fractions import Fraction
import random
import time

# Function generates a fibonacci sequence that will suite the generator.
def g_fibonacci(genCenterY):
    fibonacciList = [1]
    previousNum = 1
    currentNum = 1
    while (currentNum < genCenterY):
        nextNum = currentNum + previousNum
        fibonacciList.append(nextNum)
        previousNum = currentNum
        currentNum = nextNum
    print(fibonacciList)
    return fibonacciList

# Function draws the given image from the given array.
def drawFractal(fractalSpace, saveBoolean, saveLocation):
    fractalSpace.show()
    if (saveBoolean == True):
        fractalSpace.save(saveLocation)

def generateBoundList(radius, genCenterX, genCenterY):
    bounds = []
    yMin = genCenterY - radius
    yMax = genCenterY + radius
    xMin = genCenterX - radius
    xMax = genCenterX + radius
    for i in range(0, int(radius)+1):
        y = yMin - (i + yMin) + genCenterY
        bounds.append([xMin + i, y])
        bounds.append([xMax - i, y])
        y = i + genCenterY
        bounds.append([xMin + i, y])
        bounds.append([xMax - i, y])
    return bounds

# Function checks for adjacency between two verticies in a graph.
def adjacency(vert1, vert2):
    if ((vert1[0] + 1 == vert2[0]) and (vert1[1] == vert2[1])):
        return True
    if ((vert1[0] - 1 == vert2[0]) and (vert1[1] == vert2[1])):
        return True
    if ((vert1[0] + 1 == vert2[0]) and (vert1[1] + 1 == vert2[1])):
        return True
    if ((vert1[0] - 1 == vert2[0]) and (vert1[1] + 1 == vert2[1])):
        return True
    if ((vert1[0] == vert2[0]) and (vert1[1] + 1 == vert2[1])):
        return True
    if ((vert1[0] == vert2[0]) and (vert1[1] - 1 == vert2[1])):
        return True
    if ((vert1[0] - 1 == vert2[0]) and (vert1[1] - 1 == vert2[1])):
        return True
    if ((vert1[0] + 1 == vert2[0]) and (vert1[1] - 1 == vert2[1])):
        return True
    else:
        return False

# Terrible checkNeighbor implementation. Just for showcasing the need for well thought out algorithms. Will be addressed in version 2.
def checkNeighbor(nodeIndex, nodes):
    # For each vertex in the node,
    for i in range(0, len(nodes[nodeIndex])):
        # for each node in the space,
        for j in range(0, len(nodes)):
            # If the node we are checking is the current node, skip it.
            if (nodeIndex == j):
                continue
            # For each vertex in the node we are checking,
            for k in range(0, len(nodes[j])):
                # Check for adjacency between the current vertex of the current node, and the vertices of all other nodes in the space.
                if (adjacency(nodes[nodeIndex][i], nodes[j][k])):
                    # J is the index of an adjacent node.
                    return j
    return -1

# Function generates the fractal over a set number of iterations, the largest fractal graph is returned.
def growFractal(nodes, iterations, fractalSpaceXY):
    index = 0
    while (index < iterations):
        print("Progress = " + str(index/iterations))
        i = 0
        print(len(nodes))
        nodeCount = len(nodes)
        while i < nodeCount:
            print("Progress = " + str(index/iterations) + str(i/nodeCount)[2:])
            moveNodeXY = random.randint(0, 1)
            direction = random.randint(0, 1)
            if (direction == 0):
                direction = -1
            if (moveNodeXY == 0):
                nodeXDirection = 1*direction
                nodeYDirection = 0
            else:
                nodeYDirection = 1*direction
                nodeXDirection = 0
            for j in range(0, len(nodes[i])):
                if (nodeXDirection == 1 and nodes[i][j][0] == fractalSpaceXY[0]-1):
                    continue
                if (nodeYDirection == 1 and nodes[i][j][1] == fractalSpaceXY[1]-1):
                    continue
                if (nodeXDirection == -1 and nodes[i][j][0] == 0):
                    continue
                if (nodeYDirection == -1 and nodes[i][j][1] == 0):
                    continue
                nodes[i][j][0] = nodes[i][j][0] + nodeXDirection
                nodes[i][j][1] = nodes[i][j][1] + nodeYDirection

            # If there are neighbors created by the translation,
            neighborIndice = checkNeighbor(i, nodes)
            while (neighborIndice != -1):
                print("inLoop")
                # Concatenate the adjacent node to the current node
                nodes[i] = nodes[i] + nodes[neighborIndice]
                # Remove the adjacent node from nodes.
                del nodes[neighborIndice]
                nodeCount -= 1
                if (neighborIndice < i):
                    i -= 1
                neighborIndice = checkNeighbor(i, nodes)
            i += 1
        index += 1

    # Uncomment if you wish to view the entire space.
    '''
    flattenedNodes = []
    for subnodes in nodes:
        for node in subnodes:
            flattenedNodes.append(node)
    return flattenedNodes
    '''
    
    largestFractalNodeIndex = 0
    for index in range(1, len(nodes)):
        if (len(nodes[index]) > len(nodes[largestFractalNodeIndex])):
            largestFractalNodeIndex = index
    return nodes[largestFractalNodeIndex]

# Clears any existing content in the space.
# In this case, the spawn boundaries.
def clearFractal(fractalArray, fractalSpaceXY):
    for i in range(0, fractalSpaceXY[0]):
        for j in range(0, fractalSpaceXY[1]):
            if (fractalArray[i, j] == 255):
                fractalArray[i, j] = 0
    return fractalArray

# Occupies fractal array with the selected fractal.
def occupyFractalArray(fractalArray, fractal, fractalSpaceXY, showDistribution):
    if showDistribution == False:
        fractalArray = clearFractal(fractalArray, fractalSpaceXY)
    # Places the fractal into the space.
    for index in range(0, len(fractal)):
        fractalArray[fractal[index][0], fractal[index][1]] = 255
    return fractalArray

# Function normalizes and reverses a sorted list.
def normalize(fibonacciList):
    normalizedList = []
    min = fibonacciList[0]
    max = fibonacciList[-1]
    for item in fibonacciList:
        # 0.001 offset is used to prevent 0% probability.
        normalizedList.append(((item - min)/(max - min)) + 0.001)
    normalizedList.reverse()
    return normalizedList

# Function spawns and distributes nodes via the fibonacci distribution.
def generateInitialSpawn(fractalArray, fractalSpaceXY, spawnScaling):
    genCenterX = int(fractalSpaceXY[0]/2)
    genCenterY = int(fractalSpaceXY[1]/2)
    xDexMax = fractalSpaceXY[0]
    yDexMax = fractalSpaceXY[1]

    # Determine which axis is longer and create the appropriate fibonacci sequence that satisfies the bounds.
    if genCenterX < genCenterY:
        fibonacciList = g_fibonacci(genCenterX)
    else:
        fibonacciList = g_fibonacci(genCenterY)
        
    # Generate the fibonacci bounds for the spawn process.
    for i in range(0, len(fibonacciList)):
        currentBounds = generateBoundList(int(fibonacciList[i]/2), genCenterX, genCenterY)
        # Insert temporary bounding line
        for j in range(0, len(currentBounds)):
            fractalArray[currentBounds[j][0], currentBounds[j][1]] = 255

    # Generate the initial nodes.
    nodes = []
    fibonacciNormalized = normalize(fibonacciList)
    print(fibonacciNormalized)
    for yIndex in range(0, yDexMax):
        indexModifier = -1
        # Set the current spawn probability.
        fibIndex = len(fibonacciNormalized)-1
        spawnProbability = fibonacciNormalized[fibIndex]*spawnScaling
        for xIndex in range(0, xDexMax):
            # If the current node passes the fibonacci bound, change the probability.
            if (fractalArray[xIndex, yIndex] == 255):
                fibIndex += indexModifier
                spawnProbability = fibonacciNormalized[fibIndex]*spawnScaling
            # If the xIndex has spanned half of the space, negate the indexModifier.
            if (xIndex == int(xDexMax/2)):
                indexModifier *= -1
            # Determine if a node should be spawned, if so, spawn it.
            if (random.random() < spawnProbability):
                # 2d list created so that nodes may become larger graphs in the iteration / fractal building process.
                nodes.append([[xIndex, yIndex]])
    print(len(nodes))
    return nodes

def main(fractalSpaceXY, iterations, spawnScaling, showDistribution, saveBoolean, saveLocation):
    # Creating new gray scale type image, empty color param so we can fill ourselves.
    fractalSpace = Image.new('L', fractalSpaceXY)
    # Loading the empty image into a readable/writable array format.
    fractalArray = fractalSpace.load()
    nodes = generateInitialSpawn(fractalArray, fractalSpaceXY, spawnScaling)
    # Develop the fractal from the spawn.
    fractal = growFractal(nodes, iterations, fractalSpaceXY)
    #print("Here is the longest fractal")
    #print(fractal)
    # Fill the fractalArray (subsequently the fractalSpace) with the generated fractal.
    fractalArray = occupyFractalArray(fractalArray, fractal, fractalSpaceXY, showDistribution)
    drawFractal(fractalSpace, saveBoolean, saveLocation)

fractalSpaceXY = (250, 250)
spawnScaling = 8
showDistribution = False
iterations = 0
saveBoolean = True
saveLocation = "D:/Downloads/fractal.png"

main(fractalSpaceXY, iterations, spawnScaling, showDistribution, saveBoolean, saveLocation)
