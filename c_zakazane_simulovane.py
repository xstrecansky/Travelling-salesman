import threading
import matplotlib.pyplot as plt
import random
import time


COORDINATES = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
PERMUTATIONS = []
FITNESS = []
FITNESS_LENGTH = []

fig, axes = plt.subplots(1, 2)

# Inicializujeme pole podla velkosti suradnic
def initPermutations():
    for i in range(len(COORDINATES)):
        PERMUTATIONS.append(i)


# Metoda na vykreslenie grafu
# Musime pridat do pola prve x,y hodnoty aby boli body spojene
def plotGraph(x, y , name, time, state, bestValue):
    if bestValue:
        FITNESS.append(state)
        FITNESS_LENGTH.append(len(FITNESS))

    x.append(x[0])
    y.append(y[0])

    plt.clf()
    plt.ion()

    (plt.figure(1)).set_figwidth(8)
    (plt.figure(1)).set_figheight(4)

    plt.subplot(1, 2, 1)
    plt.plot(x, y, color = "blue", marker = "o")
    plt.title(name)

    plt.subplot(1, 2, 2)
    plt.plot(FITNESS_LENGTH, FITNESS)
    plt.title("Fitness - " + str(int(bestValue)))

    plt.show(block=False)
    plt.pause(time)


# Pomocou permutacie dostaneme pole
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
        item.append(calculateState(item))

    lastItemOnTheList = len(neighborhood[0]) - 1
    neighborhood.sort(key=lambda x: x[lastItemOnTheList])

    return neighborhood


# Vytvorime nahodnu permutaciu a jej hodnotenie
def generateRandomPermutationAndValue():
    state = PERMUTATIONS.copy()
    random.shuffle(state)
    return state, calculateState(state)


# Metoda na najdenie prveho prvku ktory nie je v tabu liste
def findNeighbor(neighborhood, tabuList):
    for i in range(len(neighborhood)):
        bestNeighbor = neighborhood[i][:-1]
        bestNeighborValue = neighborhood[i][-1]
        if bestNeighbor in tabuList:
            continue
        else:
            return bestNeighbor, bestNeighborValue


# Metoda na spustanie zakazaneho prehladavania
def tabuSearch():
    tabuList = []
    state, value = generateRandomPermutationAndValue()
    best = value
    overallBestState = state
    for i in range(100):
        neighborhood = generateNeighborhood(state)
        bestNeighbor, bestNeighborValue = findNeighbor(neighborhood, tabuList)

        if bestNeighborValue >= value:
            tabuList.append(state)
        if best > bestNeighborValue:
            overallBestState = bestNeighbor
            best = bestNeighborValue
        x, y = permutationToXYArray(bestNeighbor)
        plotGraph(x, y ,"Tabu search", 0.05, bestNeighborValue, best)

        if len(tabuList) > 100:
            tabuList.pop(0)
        
        state = bestNeighbor
        value = bestNeighborValue

    x, y = permutationToXYArray(overallBestState)
    plotGraph(x, y ,"Tabu search", 5, None, best)

# Pomocou permutacie dostaneme x a y z povodneho arrayu
def permutationToXYArray(permutation):
    x = []
    y = []
    for item in permutation:
        x.append(COORDINATES[item][0])
        y.append(COORDINATES[item][1])

    return x, y


# Metoda na spustanie simulovaneho zihania
def simulatedAnnealing():
    state, value = generateRandomPermutationAndValue()
    bestValue = value
    overallBestState = state
    run = True
    while run:
        neighborhood = generateNeighborhood(state)
        for i, item in enumerate(neighborhood):
            bestNeighbor = item[:-1]
            bestNeighborValue = item[-1]

            chance = round(bestValue / (bestNeighborValue * 2), 2)
            randomValue = (random.randrange(1, 101) / 100)

            if bestValue > bestNeighborValue:
                overallBestState = bestNeighbor
                bestValue = bestNeighborValue
                state = bestNeighbor

            elif chance  > randomValue:
                x, y = permutationToXYArray(bestNeighbor)
                plotGraph(x, y ,"Simulated annealing", 0.01, bestNeighborValue, bestValue)
                state = bestNeighbor
                break
            else:
                if i > len(neighborhood) - 2:
                    run = False
    x, y = permutationToXYArray(overallBestState)
    plotGraph(x, y ,"Simulated annealing", 5, None, bestValue)


# Hlavna metoda programu
def main():
    initPermutations()
    tabuSearch()
    simulatedAnnealing()

main()