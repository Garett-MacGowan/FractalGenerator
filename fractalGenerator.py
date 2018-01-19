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
    return fibonacciList

# Function draws the given image from the given array.
def drawFractal(fractalSpace, saveBoolean, saveLocation):
    fractalSpace.show()
    if (saveBoolean == 1):
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


# Function removes adjacent nodes from set of initially spawned nodes.
# could further improve this function's searching capability.
def preventOverspawn(nodes, xIndex, yIndex):
    for index in range(0, len(nodes)):
        if (nodes[index] == [xIndex - 1, yIndex]):
            del nodes[index]
        if (nodes[index] == [xIndex -1, yIndex - 1]):
            del nodes[index]
        if (nodes[index] == [xIndex, yIndex-1]):
            del nodes[index]
        if (nodes[index] == [xIndex + 1, yIndex -1]):
            del nodes[index]
    return nodes

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

# Function checks for neighbor nodes, returns node index of neighbors if found, -1 if none found.
def checkNeighbor(nodeIndex, nodes):
    neighboringIndexList = []
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
                    # J is the index of an adjacent node, if it is not already in the neighboringIndexList, add it.
                    if (j not in neighboringIndexList):
                        neighboringIndexList.append(j)
    if (len(neighboringIndexList) == 0):
        return -1
    else:
        return neighboringIndexList

# Function generates the fractal over a set number of iterations, the largest fractal graph is returned.
def growFractal(nodes, iterations, fractalSpaceXY):
    index = 0
    while (index < iterations):
        print("Progress = " + str(index/iterations))
        i = 0
        nodeCount = len(nodes)
        while i < nodeCount:
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
            i += 1
            
        neighborIndices = checkNeighbor(i, nodes)
        # If there are neighbors created by the translation,
        if (neighborIndices != -1):
             # For each neighbor,
             for k in range(0, len(neighborIndices)):
                 # Concatenate the adjacent node to the current node
                '''
                print("")
                print(nodes[neighborIndices[k]])
                print(nodes[i])
                '''
                nodes[i] = nodes[i] + nodes[neighborIndices[k]]
                #print(nodes[i])
                #time.sleep(1)
                # Remove the adjacent node from nodes.
                del nodes[neighborIndices[k]]
                nodeCount -= 1
                if (i < neighborIndices[k]):
                    i -= 1
        index += 1

    largestFractalNodeIndex = 0
    for index in range(1, len(nodes)):
        if (len(nodes[index]) > len(nodes[largestFractalNodeIndex])):
            largestFractalNodeIndex = index
    return nodes[largestFractalNodeIndex]

# Occupies fractal array with the selected fractal.
def occupyFractalArray(fractalArray, fractal, fractalSpaceXY):
    '''
    for i in range(0, fractalSpaceXY[0]):
        for j in range(0, fractalSpaceXY[1]):
            if (fractalArray[i, j] == 255):
                fractalArray[i, j] = 0
    '''
    for index in range(0, len(fractal)):
        fractalArray[fractal[index][0], fractal[index][1]] = 255
    return fractalArray

# Function spawns and distributes nodes via the fibonacci distribution.
def generateInitialSpawn(fractalArray, fractalSpaceXY):
    genCenterX = int(fractalSpaceXY[0]/2)
    genCenterY = int(fractalSpaceXY[1]/2)
    xDexMax = fractalSpaceXY[0]# check bounding, may have to subtract one
    yDexMax = fractalSpaceXY[1]

    # Determine which axis is longer and create the appropriate fibonacci sequence that satisfies the bounds.
    if genCenterX < genCenterY:
        fibonacciList = g_fibonacci(genCenterX)
    else:
        fibonacciList = g_fibonacci(genCenterY)

    # Generate the fibonacci bounds for the spawn process.
    for i in range(0, len(fibonacciList)):
        currentBounds = generateBoundList(int(fibonacciList[i]/2), genCenterX, genCenterY)
        # Generate temporary bounding line
        for j in range(0, len(currentBounds)):
            fractalArray[currentBounds[j][0], currentBounds[j][1]] = 255

    # Generate the initial node position vectors.
    nodes = []
    for yIndex in range(0, yDexMax):
        indexModifier = -1
        # Set the current spawn probability.
        fibIndex = len(fibonacciList)-1
        spawnProbability = 1/(fibonacciList[fibIndex]/10)
        for xIndex in range(0, xDexMax):
            # If the current node passes the fibonacci bound, change the probability.
            if (fractalArray[xIndex, yIndex] == 255):
                fibIndex += indexModifier
                spawnProbability = 1/(fibonacciList[fibIndex]/10)
            # If the xIndex has spanned half of the space, negate the indexModifier.
            if (xIndex == int(xDexMax/2)):
                indexModifier *= -1
            # Determine if a node should be spawned, if so, spawn it.
            if (random.random() <= spawnProbability):
                # 2d list created so that nodes may become larger graphs in the iteration / fractal building process.
                nodes.append([[xIndex, yIndex]])
                # To prevent overspawning, remove any possible spawn in the node directly left, and or above, the spawned node.
                nodes = preventOverspawn(nodes, xIndex, yIndex)
    return nodes

def main(fractalSpaceXY, iterations, saveBoolean, saveLocation):
    # Creating new gray scale type image, empty color param so we can fill ourselves.
    fractalSpace = Image.new('L', fractalSpaceXY)
    # Loading the empty image into a readable/writable array format.
    fractalArray = fractalSpace.load()
    nodes = generateInitialSpawn(fractalArray, fractalSpaceXY)
    # Develop the fractal from the spawn.
    fractal = growFractal(nodes, iterations, fractalSpaceXY)
    print("Here is the longest fractal")
    print(fractal)
    # Fill the fractalArray (subsequently the fractalSpace) with the generated fractal.
    fractalArray = occupyFractalArray(fractalArray, fractal, fractalSpaceXY)
    drawFractal(fractalSpace, saveBoolean, saveLocation)

fractalSpaceXY = (100, 100)
saveBoolean = 1
saveLocation = "D:/Downloads/fractal.png"
iterations = 35

main(fractalSpaceXY, iterations, saveBoolean, saveLocation)
