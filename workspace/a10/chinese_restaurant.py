import random
import json
import matplotlib.pyplot as plt
import scipy.integrate as integrate

def gini_coefficient(network):
    network.sort()
    sum = 0
    sumList = []
    equal = [0]
    #This is just a helper-loop in order to get the Line of Equality
    for k in range(1,len(network)):
        equal.append((k * 1000) / (len(network) -1))
    print(equal)
    #This loop calculates the Lorenz Curve
    for i in range(0,len(network)):
        sum += network[i]
        sumList.append(sum)
    #We calculate the Gini coefficient as: G = A / O where A is the area of the Line of equality minus the area of the Lorenz Curve and O the total area beneath the Line of equality. The area beneath the lines are calculated by using the integrate function of scipy
    O = integrate.simps(equal)
    print('O = ' + str(O) +'\n')
    B = integrate.simps(sumList)
    print('B = ' + str(B) + '\n')
    A = O-B
    G = A / O
    print('G = ' + str(G))
    plt.plot(equal)
    plt.plot(sumList)
    plt.axis([0,len(network)-1,0,1000])
    plt.show()
    return G

def generateChineseRestaurant(customers):
    # First customer always sits at the first table
    tables = [1]
    #for all other customers do
    for cust in range(2, customers+1):
            # rand between 0 and 1
            rand = random.random()
            # Total probability to sit at a table
            prob = 0
            # No table found yet
            table_found = False
            # Iterate over tables
            for table, guests in enumerate(tables):
                # calc probability for actual table an add it to total probability
                prob += guests / (cust)
                # If rand is smaller than the current total prob., customer will sit down at current table
                if rand < prob:
                    # incr. #customers for that table
                    tables[table] += 1
                    # customer has found table
                    table_found = True
                    # no more tables need to be iterated, break out for loop
                    break
            # If table iteration is over and no table was found, open new table
            if not table_found:
                tables.append(1)
    print(tables)
    return tables

ginis = [[],[],[],[],[]]
G = gini_coefficient(generateChineseRestaurant(1000))
plt.axis([0,1000,0,1])
#plt.show()