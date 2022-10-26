import threading
import matplotlib.pyplot as plt
import random
import time


COORDINATES = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
PERMUTATIONS = []


def initPermutations():
    for i in range(len(COORDINATES)):
        PERMUTATIONS.append(i)


# Metoda na vykreslenie grafu
# Musime pridat do pola prve x,y hodnoty aby boli body spojene
def plotGraph(x, y , name):
    x.append(x[0])
    y.append(y[0])
    plt.clf()
    plt.ion()
    plt.plot(x, y, color = "blue", marker = "o")
    plt.show(block=False)
    plt.title(name)
    plt.pause(0.1)


def arrayByPermutation(permutation):
    tempX = []
    tempY = []
    for number in permutation:
        tempX.append(COORDINATES[number][0])
        tempY.append(COORDINATES[number][1])
    return tempX, tempY


# Metoda na vypocitanie vzdialenosti medzi dvoma bodmi
def calculateDistance(x1, y1, x2, y2): 
    return (((x1 - x2)**2 + (y1 - y2)**2)**0.5)


# Metoda na vypisanie ohodnotenia aktualneho stavu
def calculateState(permutation):
    sumValue = 0
    x, y = arrayByPermutation(permutation)
    x.append(x[0])
    y.append(y[0])
    for i in range(len(x)-1):
        sumValue += calculateDistance(x[i], y[i], x[i+1], y[i+1])

    return sumValue


# Metoda na vygenerovanie vsetkych permutacii 
def generateNeighborhood(solution):
    neighborhood = []
    lenghtOfPermutation = len(solution) 

    for j in range(lenghtOfPermutation):
        for i in range(lenghtOfPermutation):
            temp = solution.copy()
            if i+j+2 < lenghtOfPermutation:
                temp[i+1], temp[i+j+2] = temp[i+j+2], temp[i+1]
                if temp not in neighborhood:
                    neighborhood.append(temp)
                
    for item in neighborhood:
        item.append(calculateState(item[:-1]))

    lastItemOnTheList = len(neighborhood[0]) - 1
    neighborhood.sort(key=lambda x: x[lastItemOnTheList])

    return neighborhood


# Metoda na spustanie zakazaneho prehladavania
def tabuSearch():
    tabuList = []
    startingState = PERMUTATIONS.copy()
    random.shuffle(startingState)
    best = calculateState(startingState)

    for i in range(1000):
        neighborhood = generateNeighborhood(startingState)
        bestNeighbor = neighborhood[0][:-1]
        bestNeighborValue = neighborhood[0][-1]

        if bestNeighborValue < best:
            startingState = bestNeighbor
            best = bestNeighborValue
            x, y = permutationToXYArray(bestNeighbor)
            plotGraph(x, y ,"Tabu search")
            print(bestNeighborValue)

        else:
            random.shuffle(startingState)

    plt.plot(x, y, color = "blue", marker = "o")
    plt.pause(5)


# Pomocou permutacie dostaneme x a y z povodneho arrayu
def permutationToXYArray(permutation):
    x = []
    y = []
    for item in permutation:
        x.append(COORDINATES[item][0])
        y.append(COORDINATES[item][1])

    return x, y


# Metoda na spustanie simulovaneho zihania
def simulatedAnnealing(x, y):
    plotGraph(x, y, "Simmulated annealing")


# Hlavna metoda programu
def main():
    initPermutations()
    #(threading.Thread(target=tabuSearch(x, y))).start()
    #(threading.Thread(target=simulatedAnnealing(x, y))).start()
    tabuSearch()


main()