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
        #this prevents division by 0, if k is 1
        if k is 1:
            bot = 1
        else:
            bot = len(network) -1
        equal.append((k * 1000) / (len(network) -1))
    #This loop calculates the Lorenz Curve
    for i in range(0,len(network)):
        sum += network[i]
        sumList.append(sum)
    #We calculate the Gini coefficient as: G = A / O where A is the area of the Line of equality minus the area of the Lorenz Curve and O the total area beneath the Line of equality. The area beneath the lines are calculated by using the integrate function of scipy
    O = integrate.simps(equal)
    B = integrate.simps(sumList)
    A = O-B
    G = A / O
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
    return tables

ginis = [[],[],[],[],[]]

for i in range(0,5):
    for j in range(1,1000):
        ginis[i].append(gini_coefficient(generateChineseRestaurant(j)))
    plt.plot(ginis[i])
    plt.xlabel('# of customers')
    plt.ylabel('Gini-coefficient')
    plt.axis([0,1000,0,1])
    plt.show()