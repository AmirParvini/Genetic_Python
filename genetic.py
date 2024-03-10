import matplotlib.pyplot as plt
import matplotlib.markers as mks
import numpy as np
import pprint
import random as rn
from itertools import chain
import math

Q = 60
Num_Depot = 4
x_Nodes = []
y_Nodes = []
x_Cust = []
y_Cust = []
xDepots = []
yDepots = []
Cust_Index = list(range(1,161))
Customers = []
Demands = []

# خواندن فایل   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
with open("F:\\p15", "r", encoding="utf-8") as file:
    lines = file.readlines()

for i, line in enumerate(lines, start=1):
    if 1+Num_Depot < i < len(lines)-Num_Depot+1:
        numbers = line.split()
        numbers_array = [int(num) for num in numbers]
        x_Cust.append(numbers_array[1])
        x_Nodes.append(numbers_array[1])
        y_Cust.append(numbers_array[2])
        y_Nodes.append(numbers_array[2])
        Demands.append(numbers_array[4])

    if len(lines)-Num_Depot < i:
        numbers = line.split()
        numbers_array = [int(num) for num in numbers]
        xDepots.append(numbers_array[1])
        x_Nodes.append(numbers_array[1])
        yDepots.append(numbers_array[2])
        y_Nodes.append(numbers_array[2])


# تشکیل مارتیس فواصل    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
Dist_Matrix = np.empty((len(x_Nodes), len(y_Nodes)), dtype=float)
def DistMatrix():
    for i in range(len(x_Nodes)):
        for j in range(len(x_Nodes)):
            Dist_Matrix[i][j] = round( np.sqrt( pow(x_Nodes[i]-x_Nodes[j],2) + pow(y_Nodes[i]-y_Nodes[j],2) ), 2)
    return Dist_Matrix
