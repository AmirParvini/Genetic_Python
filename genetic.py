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






Chromosoms = []
# initialpopulation -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def Initialpopulation(paulation_num: int):
    for i in range(paulation_num):
        Chromosom = []
        Selectable = Custs_index.copy()
        while len(Selectable) > 0:
            j = rn.choice(Selectable)
            Chromosom.append(j)
            Selectable.remove(j)
        Chromosoms.append(Chromosom)
    return Chromosoms
# initialpopulation -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
print('initialpop =', Initialpopulation(100), '\n\n')






plt.scatter(x_Cust, y_Cust, s=5)
plt.scatter(xDepots, yDepots, c='r', s=5, marker='s')
for i, txt in enumerate(yDepots):
    plt.text(xDepots[i], yDepots[i], i+1, fontsize=6, color='red', ha='right', va='bottom')
for i, txt in enumerate(y_Cust):
    plt.text(x_Cust[i], y_Cust[i], i+1,fontsize=6, ha='right', va='bottom')
plt.show()