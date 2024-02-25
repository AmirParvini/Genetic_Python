
import matplotlib.pyplot as plt
import matplotlib.markers as mks
import numpy as np
import pprint
import random as rn
from itertools import chain

Q = 100
x_Cust = []
y_Cust = []
Cust_Index = list(range(2,81))
Customers = []
Demands = []

# خواندن فایل   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
with open("F:\\A-n80-k10.txt", "r", encoding="utf-8")as file:
    for i, line in enumerate(file, start=1):
        if 7 < i < 88:

            numbers = line.split()
            numbers_array = [int(num) for num in numbers]

            if i == 8:
                xDepot = numbers_array[1]
                yDepot = numbers_array[2]
            else:
                x_Cust.append(numbers_array[1])
                y_Cust.append(numbers_array[2])
        
        if 89 < i < 169:
            demands = line.split()
            demands_array = [int(num) for num in demands]
            Demands.append(demands_array[1])


# مختصات همه مشتری ها + انبار   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   
x_Nodes = x_Cust.copy()
y_Nodes = y_Cust.copy()
x_Nodes.insert(0,xDepot)
y_Nodes.insert(0,yDepot)


Dist_Matrix = np.empty((len(x_Nodes), len(y_Nodes)), dtype=float)


# نمودار
plt.scatter(x_Cust, y_Cust, s=5)
plt.scatter(xDepot, yDepot, c='r', s=30, marker='s')

for i, txt in enumerate(y_Cust):
    plt.text(x_Cust[i], y_Cust[i], i+2, ha='right', va='bottom')
# plt.show()



# تشکیل مارتیس فواصل    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def DistMatrix():
    for i in range(len(x_Nodes)):
        for j in range(len(x_Nodes)):
            Dist_Matrix[i][j] = round( np.sqrt( pow(x_Nodes[i]-x_Nodes[j],2) + pow(y_Nodes[i]-y_Nodes[j],2) ), 2)
    return Dist_Matrix



# pprint.pprint(DistMatrix())

# print(min(np.ma.masked_values(Dist_Matrix[0][0:], [0])))
# print(min(Dist_Matrix[0, 1:]))




Cust_Index_Demands = np.empty((len(x_Cust), 2), dtype=int)

j = 0
for i in range(len(x_Cust)):
    Cust_Index_Demands[i]= [Cust_Index[j], Demands[j]]
    j = j+1




# مجموع تقاضاهای مشتری هایی که یک ماشین آن ها را بازدید می کند
def Sum(Route):
    sumroute = 0
    for i in Route:
        sumroute = sumroute + Demands[Cust_Index.index(i)]
    return sumroute


def del_selectable_index(array, j):
    for row_index, row in enumerate(array):
        if np.array_equal(row, j):
            return row_index
        else:
            continue




InitialPapulation = np.empty((100, 0), dtype=int)
Route = list([])
Chromosoms = []
# initialpopulation -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def initialpopulation(paulation_num: int):

    Chromosom = []
    Route = []

    for i in range(paulation_num):
        Selectable = Cust_Index.copy()
        t = 2
        while len(Selectable) > 0:
            j = rn.choice(Selectable)
            Chromosom.append(j)
            Route.append(j)

            if Sum(Route) > 100:
                Chromosom.pop()
                Chromosom.append(len(x_Cust)+t)
                t = t+1
                Route = []
            else:
                # Selectable.remove(j)
                Selectable = np.delete(Selectable, del_selectable_index(Selectable, j), axis=0)
                # if i==0:
                #     print(j)
                #     print(Selectable)

            if len(Selectable) == 0 :
                Route = []

        Chromosoms.append(Chromosom)
        Chromosom = []

    return Chromosoms
# initialpopulation -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -




initialpopulation(100)
# print(Chromosoms[5])
# print(len(Chromosoms[5]))




# Chromosom_Plot    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def Chromosom_Plot(chromosom):
    x = []
    y = []
    x.append(xDepot)
    y.append(yDepot)

    for index, i in enumerate(chromosom):
        # print(i)
        # print('max cust index = ',max(Cust_Index))

        if i <= max(Cust_Index):

            x.append( x_Cust[Cust_Index.index(i)])
            y.append( y_Cust[Cust_Index.index(i)])
        else:
            x.append(xDepot)
            y.append(yDepot)

            # plt.figure()
            plt.scatter(x_Cust, y_Cust, s=5)
            plt.scatter(xDepot, yDepot, c='r', s=30, marker='s')
            for i, txt in enumerate(y_Cust):
                plt.text(x_Cust[i], y_Cust[i], i+2, ha='right', va='bottom')

            plt.plot(x,y)
            x = []
            y = []
            x.append(xDepot)
            y.append(yDepot)

    plt.show()
# Chromosom_Plot    -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

# print(Chromosoms[5])
# Chromosom_Plot(Chromosoms[5])




# OXCrossOver   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
def OX_CrossOver(Chromosoms: list):

    childs = []

    while(len(Chromosoms) > 0):

        p1: list = rn.choice(Chromosoms)
        Chromosoms.remove(p1)
        p2: list = rn.choice(Chromosoms)
        Chromosoms.remove(p2)

        if len(p1)!=len(p2):
            print('continue', f"len p1 = {len(p1)} AND ", f"len p2 = {len(p2)}")
            print('p1 = ',p1, '\n', 'p2 = ', p2)
            continue

        child = [1]*len(p1)
        crossoverindex = rn.sample(list(range(len(p1))),2)
        child[min(crossoverindex):max(crossoverindex)+1] = p1[min(crossoverindex):max(crossoverindex)+1]

        j = 0
        Chain = chain(range(min(crossoverindex)), range(max(crossoverindex)+1, len(child)))
        for i in Chain:

            if i < min(crossoverindex) or i > max(crossoverindex):
                while p2[j] in child[min(crossoverindex):max(crossoverindex)]:
                    j += 1
                child[i] = p2[j]
            j += 1

        childs.append(child)
        crossoverindex = []

    return childs
# OXCrossOver   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -



childs = OX_CrossOver(Chromosoms)
print(childs, '\n', len(childs))
















# i = 0
# qt = 0
# x = []; y = []
# while qt < Q:
#     print(i)
#     c = np.where(Dist_Matrix != 0, Dist_Matrix[i] == min(Dist_Matrix[i, 0:]))[0][0]
#     qt = qt+Demands[c]
#     x.append(x_Nodes[i]); x.append(x_Nodes[c])
#     y.append(y_Nodes[i]); y.append(y_Nodes[c])
#     i = c

# print(x)
# plt.plot(x,y,'g')
# plt.show()