import matplotlib.pyplot as plt
import matplotlib.markers as mks
import numpy as np
import pprint
import random as rn
from itertools import chain
import math

NumOfVehicles = 0
Q = 0
NumOfDepots = 0
NumOfCust = 0
x_Nodes = []
y_Nodes = []
x_Cust = []
y_Cust = []
xDepots = []
yDepots = []
Custs_index = []
Depots_index = []
Nodes_Index = []
Customers = []
Demands = []

# خواندن فایل   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
with open("F:\\MDVRP_DATA_new\pr03", "r", encoding="utf-8") as file:
    lines = file.readlines()

for i, line in enumerate(lines, start=1):
    if i == 1:
        numbers = line.split()
        numbers_array = [int(num) for num in numbers]
        NumOfVehicles = numbers_array[1]
        NumOfCust = numbers_array[2]
        NumOfDepots = numbers_array[3]
    elif i == 2:
        numbers = line.split()
        numbers_array = [int(num) for num in numbers]
        Q = numbers_array[1]
    elif 1+NumOfDepots < i < len(lines)-NumOfDepots+1:
        numbers = line.split()
        numbers_array = [float(num) for num in numbers]
        x_Cust.append(numbers_array[1])
        x_Nodes.append(numbers_array[1])
        y_Cust.append(numbers_array[2])
        y_Nodes.append(numbers_array[2])
        Demands.append(numbers_array[4])

    elif len(lines)-NumOfDepots < i:
        numbers = line.split()
        numbers_array = [float(num) for num in numbers]
        xDepots.append(numbers_array[1])
        x_Nodes.append(numbers_array[1])
        yDepots.append(numbers_array[2])
        y_Nodes.append(numbers_array[2])

print('custs =', NumOfCust, '\n', 'Depots =', NumOfDepots, '\n', 'vehicles of each Depot =',NumOfVehicles, '\n', 'Q =', Q, '\n', 'sumdemands =', sum(Demands))
Custs_index = list(range(1,NumOfCust+1))
Depots_index = list(range(Custs_index[-1]+1,NumOfCust+NumOfDepots+1))
Nodes_Index = list(range(1,NumOfCust+NumOfDepots+1))


# تشکیل مارتیس فواصل    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
Dist_Matrix = np.empty((len(x_Nodes), len(y_Nodes)), dtype=float)
def DistMatrix():
    for i in range(len(x_Nodes)):
        for j in range(len(x_Nodes)):
            Dist_Matrix[i][j] = round( np.sqrt( pow(x_Nodes[i]-x_Nodes[j],2) + pow(y_Nodes[i]-y_Nodes[j],2) ), 2)
    return Dist_Matrix
# pprint.pprint(DistMatrix())
print('shap of distmatrix = ',DistMatrix().shape, '\n\n')
print('custindex = ', Custs_index, '\n\n', 'DepotIndex = ', Depots_index, '\n\n')





def Grouping(numdepots, distmatrix: DistMatrix):
    GD = [['d{}'.format(k+1)] for k in range(numdepots)]
    for i in Custs_index:
        dist_to_depots = []
        for j in Depots_index:
            dist_to_depots.append(distmatrix[i-1][j-1])
        min_index = dist_to_depots.index(min(dist_to_depots))
        for l in range(numdepots):
            if l == min_index:
                GD[l].append(i)
    return GD
print('Grouping: ',Grouping(NumOfDepots,DistMatrix()), '\n\n')






InitialChromosoms = []
# initialpopulation -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def Initialpopulation(paulation_num: int):
    for i in range(paulation_num):
        Chromosom = []
        Selectable = Custs_index.copy()
        while len(Selectable) > 0:
            j = rn.choice(Selectable)
            Chromosom.append(j)
            Selectable.remove(j)
        InitialChromosoms.append(Chromosom)
    return InitialChromosoms
# initialpopulation -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
print('initialpop =', Initialpopulation(100), '\n\n')




def SumDemands(Route):
    sumroute = 0
    for i in Route:
        sumroute = sumroute + Demands[i-1]
    return sumroute

def RouteDist(x:list, y:list):
    sumdist = 0
    for k in range(1,len(x)):
        sumdist = math.sqrt((x[k-1] - x[k])**2 + (y[k-1] - y[k])**2) + sumdist
    return sumdist

def Fitness(Chromosoms: list):
    fitness = []
    d = []
    for index, c in enumerate(Chromosoms):
        oA = 0
        oB = 0
        x = []
        y = []
        x.append(xDepots[oB])
        y.append(yDepots[oB])
        chromosomdist = []
        for index_c, i in enumerate(c):
            # print("index_c = ", index_c, "AND len(c) = ", len(c))
            d.append(i)
            if index_c == len(c)-1:
                x.append(x_Cust[i-1])
                y.append(y_Cust[i-1])
                x.append(xDepots[oB])
                y.append(yDepots[oB])
                chromosomdist.append(RouteDist(x,y))
                d = []
                break

            if SumDemands(d)<=Q:
                x.append(x_Cust[i-1])
                y.append(y_Cust[i-1])

            else:
                oA += 1
                if oA == NumOfVehicles:
                    oA = 0
                    x.append(xDepots[oB])
                    y.append(yDepots[oB])
                    oB += 1
                else:
                    x.append(xDepots[oB])
                    y.append(yDepots[oB])
                chromosomdist.append(RouteDist(x,y))
                x = []
                y = []
                x.append(xDepots[oB])
                y.append(yDepots[oB])
                x.append(x_Cust[i-1])
                y.append(y_Cust[i-1])
                d = []
                d.append(i)
        fitness.append(round(sum(chromosomdist),2))
    return fitness





plt.scatter(x_Cust, y_Cust, s=5)
plt.scatter(xDepots, yDepots, c='r', s=5, marker='s')
for i, txt in enumerate(yDepots):
    plt.text(xDepots[i], yDepots[i], i+1, fontsize=6, color='red', ha='right', va='bottom')
for i, txt in enumerate(y_Cust):
    plt.text(x_Cust[i], y_Cust[i], i+1,fontsize=6, ha='right', va='bottom')




# Route_Plot    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def RoutePlot(x,y):
    # plt.figure()
    plt.scatter(x_Cust, y_Cust, s=5)
    plt.scatter(xDepots, yDepots, c='r', s=5, marker='s')
    for m, txt in enumerate(yDepots):
        plt.text(xDepots[m], yDepots[m], m+1, fontsize=6, color='red', ha='right', va='bottom')
    for n, txt in enumerate(y_Cust):
        plt.text(x_Cust[n], y_Cust[n], n+1, fontsize=6, ha='right', va='bottom')
    plt.plot(x,y)
    plt.xlabel(RouteDist(x,y))
# Route_Plot    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -





# Chromosom_Plot    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def Chromosom_Plot(chromosom):
    oA = 0
    oB = 0
    chromosomdist = []
    x = []
    y = []
    x.append(xDepots[oB])
    y.append(yDepots[oB])
    d = []

    for index, i in enumerate(chromosom):
        # print(i)
        # print('max cust index = ',max(Cust_Index))
        d.append(i)

        if index == len(chromosom)-1:
                x.append(x_Cust[i-1])
                y.append(y_Cust[i-1])
                x.append(xDepots[oB])
                y.append(yDepots[oB])
                RoutePlot(x,y)
                chromosomdist.append(RouteDist(x,y))
                break


        if SumDemands(d)<=Q:
            x.append(x_Cust[i-1])
            y.append(y_Cust[i-1])

        else:
            oA += 1
            if oA == NumOfVehicles:
                oA = 0
                x.append(xDepots[oB])
                y.append(yDepots[oB])
                oB += 1
            else:
                x.append(xDepots[oB])
                y.append(yDepots[oB])
            chromosomdist.append(RouteDist(x,y))
            RoutePlot(x,y)
            # print("x = ",x , "y = ", y)
            x = []
            y = []
            x.append(xDepots[oB])
            y.append(yDepots[oB])
            x.append(x_Cust[i-1])
            y.append(y_Cust[i-1])
            d = []
            d.append(i)
    print(sum(chromosomdist))
    plt.show()
# Chromosom_Plot    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
print(InitialChromosoms[Fitness(InitialChromosoms).index(min(Fitness(InitialChromosoms)))],'\n\n')
print('fitnessValues of chromosoms:',Fitness(InitialChromosoms))
# Chromosom_Plot(InitialChromosoms[Fitness(InitialChromosoms).index(min(Fitness(InitialChromosoms)))])
# plt.show()



# Selection    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
Ranking = range(1,len(InitialChromosoms)+1)
K = len(Ranking)
ChromosomsProb =[]
ProbsRange = []
for i in Ranking:
    if i <= K/2:
        ChromosomsProb.append((12*i)/(5*K*(K+2)))
    else:
        ChromosomsProb.append((28*i)/(5*K*(3*K+2)))
for index, i in enumerate(ChromosomsProb):
    if index == 0:
        ProbsRange.append([0,i])
    else:
        ProbsRange.append([ProbsRange[index-1][1], ProbsRange[index-1][1] + (i)])
def SRS_Selection(Pop: list):
    selectedchromosomforcrossover = []
    SelectedChromosomForCrossOver = []
    ChromosomsFitness = Fitness(Pop)
    ChromosomsFitnessSorted = sorted(Fitness(Pop))
    ChromosomsIndexByFitness = [ChromosomsFitness.index(i) for i in ChromosomsFitnessSorted]
    for i in Ranking:
        r = rn.uniform(0,1)
        for index, j in enumerate(ProbsRange):
            if r > j[0] and r <= j[1]:
                selectedchromosomforcrossover.append(ChromosomsIndexByFitness[index])
                if len(selectedchromosomforcrossover) == 2:
                    SelectedChromosomForCrossOver.append(selectedchromosomforcrossover)
                    selectedchromosomforcrossover = []
    return SelectedChromosomForCrossOver
# Selection    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
print('SelectedChromosomForCrossOver: ',Selection(InitialChromosoms))
