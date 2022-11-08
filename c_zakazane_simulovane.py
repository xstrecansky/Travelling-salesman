import matplotlib.pyplot as plt
import random


COORDINATES = [] #[(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
INIT_PERMUTATION = []
INIT_PERMUTATION_VALUE = []
PERMUTATIONS = []
FITNESS = []
FITNESS_LENGTH = []
SIZE = 40

fig, axes = plt.subplots(1, 2)


# Inicializujeme pole podla velkosti suradnic
def initPermutations():
    while len(COORDINATES) < SIZE:
        x = random.randrange(1, 21) * 10
        y = random.randrange(1, 21) * 10
        coordinates = (x, y)
        if coordinates not in COORDINATES:
            COORDINATES.append((x,y))
        
        permutation = len(COORDINATES) - 1
        if permutation not in PERMUTATIONS:
            PERMUTATIONS.append(permutation)

    state = PERMUTATIONS.copy()
    random.shuffle(state)
    for city in state:
        INIT_PERMUTATION.append(city)
    INIT_PERMUTATION_VALUE.append(calculateState(state))

    x, y = permutationToXYArray(INIT_PERMUTATION)
    plotGraph(x, y ,"First state", 3, None, INIT_PERMUTATION_VALUE[0])


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
            if i+j+1 < lenghtOfPermutation:
                temp[i], temp[i+j+1] = temp[i+j+1], temp[i]
                if temp not in neighborhood and temp != solution:
                    neighborhood.append(temp)
    
    for item in neighborhood:
        item.append(calculateState(item))

    lastItemOnTheList = len(neighborhood[0]) - 1
    neighborhood.sort(key=lambda x: x[lastItemOnTheList])

    return neighborhood


# Metoda na najdenie prveho prvku ktory nie je v tabu liste
def findNeighbor(neighborhood, tabuList):
    for i in range(len(neighborhood)):
        bestNeighbor = neighborhood[i][:-1]
        bestNeighborValue = neighborhood[i][-1]
        if bestNeighbor in tabuList:
            continue
        else:
            return bestNeighbor, bestNeighborValue


# Pomocou permutacie dostaneme x a y z povodneho arrayu
def permutationToXYArray(permutation):
    x = []
    y = []
    for item in permutation:
        x.append(COORDINATES[item][0])
        y.append(COORDINATES[item][1])

    return x, y


# Metoda na spustanie zakazaneho prehladavania
def tabuSearch():
    tabuList = []
    state = INIT_PERMUTATION.copy()
    value = INIT_PERMUTATION_VALUE[0]
    best = value
    overallBestState = state

    x, y = permutationToXYArray(state)
    plotGraph(x, y ,"Tabu search", 0.001, best, best)
    for i in range(100):
        neighborhood = generateNeighborhood(state)
        bestNeighbor, bestNeighborValue = findNeighbor(neighborhood, tabuList)

        if bestNeighborValue >= value:
            tabuList.append(state)
        if best > bestNeighborValue:
            overallBestState = bestNeighbor
            best = bestNeighborValue

        x, y = permutationToXYArray(bestNeighbor)
        plotGraph(x, y ,"Tabu search", 0.001, bestNeighborValue, best)

        if len(tabuList) > 10:
            tabuList.pop(0)
        
        state = bestNeighbor
        value = bestNeighborValue

    x, y = permutationToXYArray(overallBestState)
    plotGraph(x, y ,"Tabu search", 3, None, best)


# Metoda na spustanie simulovaneho zihania
def simulatedAnnealing():
    state = INIT_PERMUTATION.copy()
    value = INIT_PERMUTATION_VALUE[0]
    bestValue = value
    overallBestState = state

    x, y = permutationToXYArray(state)
    plotGraph(x, y ,"Simulated annealing", 0.001, value, value)
    for j in range(100):
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
                plotGraph(x, y ,"Simulated annealing", 0.001, bestNeighborValue, bestValue)
                state = bestNeighbor
                break

    x, y = permutationToXYArray(overallBestState)
    plotGraph(x, y ,"Simulated annealing", 3, None, bestValue)


# Hlavna metoda programu
def main():
    initPermutations()
    tabuSearch()
    simulatedAnnealing()

main()