# assignment 7 task 3
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime


# use sytem time (only microseconds) as seed to generate random nubers[1,6]
def roll():
	dt = datetime.now()
	dt = dt.microsecond
	tmp1 = 13.1211*np.log(np.sqrt(dt*0.75456))
	tmp2 = round(tmp1)
	result = tmp2 % 6
	return int(result +1)

# do the roll n times and store it in a list
def listIt(n):
	diceList = []
	for k in range(n):
		k += 1
#		t1 = roll()
#		t2 = roll()
		t1 = random.randint(1, 6)
		t2 = random.randint(1, 6)
		sum = t1 + t2
		diceList.append(sum)
	return diceList
	
# plot histigram with frequencies of dice sum outcomes
def simpleHist(rollResults):
	plt.hist(rollResults, bins=11, range=(2,12), facecolor='g', alpha=0.75)
	plt.title("frequency of dice sum outcomes")
	plt.xlabel("Value")
	plt.ylabel("Frequency")
	
	plt.show()

# cumulative distribution
def cumulative(rollResults):
# count how many occurences of each number
	c2 = 0
	c3 = 0
	c4 = 0
	c5 = 0
	c6 = 0
	c7 = 0
	c8 = 0
	c9 = 0
	c10 = 0
	c11 = 0
	c12 = 0

	for i in range(len(rollResults)):
		if rollResults[i] < 7:
			if rollResults[i] < 4:
				if rollResults[i] == 2:
					c2 += 1
				else:
					c3 += 1
			elif rollResults[i] < 6:
				if rollResults[i] == 4:
					c4 += 1
				else:
					c5 += 1
			else:
				c6 += 1
		else:
			if rollResults[i] < 11:
				if rollResults[i] < 9:
					if rollResults[i] == 7:
						c7 += 1
					else:
						c8 += 1
				elif rollResults[i] == 9:
					c9 += 1
				else:
					c10 += 1
			elif rollResults[i] == 11:
				c11 +=1
			else:
				c12 +=1

#calculate probabilities
	prob2 = c2/len(rollResults)
	cprob2 = prob2
	prob3 = c3/len(rollResults)
	cprob3 = cprob2 + prob3
	prob4 = c4/len(rollResults)
	cprob4 = cprob3 + prob4
	prob5 = c5/len(rollResults)
	cprob5 = cprob4 + prob5
	prob6 = c6/len(rollResults)	
	cprob6 = cprob5 + prob6
	prob7 = c7/len(rollResults)
	cprob7 = cprob6 + prob7
	prob8 = c8/len(rollResults)
	cprob8 = cprob7 + prob8
	prob9 = c9/len(rollResults)
	cprob9 = cprob8 + prob9
	prob10 = c10/len(rollResults)
	cprob10 = cprob9 + prob10
	prob11 = c11/len(rollResults)
	cprob11 = cprob10 + prob11
	prob12 = c12/len(rollResults)
	cprob12 = cprob11 + prob12
	cumList = [cprob2, cprob3, cprob4, cprob5, cprob6, cprob7, cprob8, cprob9, cprob10, cprob11, cprob12]

#probability of dice sum <10	
	print('Probability of <= 9: ' + str(cprob9))

#median
	rollResults.sort()
	middle = int(np.round(len(rollResults)/2))
	medi = rollResults[middle]
	print('median: ' + str(medi))
	
	if medi == 2:
		ymedi = cporb2
	elif medi == 3:
		ymedi = cprob3
	elif medi == 4:
		ymedi = cprob4
	elif medi == 5:
		ymedi = cprob5
	elif medi == 6:
		ymedi = cprob6
	elif medi == 7:
		ymedi = cprob7
	elif medi == 8:
		ymedi = cprob8		
	elif medi == 9:
		ymedi = cprob9
	elif medi == 10:
		ymedi = cprob10		
	elif medi == 11:
		ymedi = cprob11
	elif medi == 12:
		ymedi = cprob12	
	return cumList, medi, ymedi, cprob9
		
		
		
# CDF plot
def plotCDF(cumList, medi, ymedi, cprob9):
	xlab = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	plt.axis([2, 12, 0, 1])
	plt.plot(xlab, cumList)
	plt.plot(medi, ymedi, 'ro', label = 'median')
	plt.plot(9, cprob9, 'gd', label = 'probabitily of <= 9')
	plt.title("cumulative distribustion")
	plt.xlabel("Value")
	plt.ylabel("cumulated probabilities")
	plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0)
	
	plt.show()

def plot2CDF(cumList1, cumList2, medi, ymedi, cprob9):
	xlab = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	plt.axis([2, 12, 0, 1])
	plt.plot(xlab, cumList1, 'g', label = 'first round')
	plt.plot(xlab, cumList2, 'c', label = 'second round')
	plt.plot(medi, ymedi, 'ro', label = 'median')
	plt.plot(9, cprob9, 'bd', label = 'probabitily of <= 9')
	plt.title("cumulative distribustion")
	plt.xlabel("Value")
	plt.ylabel("cumulated probabilities")
	plt.legend(loc = 4)	
	maxP, pos = maxPointDistance(cumList1, cumList2)
	print('maximum point-wise distance = ' + str(maxP))
	print('position of maximum point-wise distance = ' + str(pos))
	plt.show()

	
# max point-wise distance
def maxPointDistance(list1, list2):
	maxP = 0
	for i in range(len(list1)):
		tmp = abs(list1[i] - list2[i])
		if tmp > maxP:
			maxP = tmp
			pos = i + 2
	return maxP, pos
		
		
def main():	
	# n = 100
	firstRound = []
	firstRound = listIt(100)
	simpleHist(firstRound)
	a, b, c, d = cumulative(firstRound)
	secondRound = []
	secondRound = listIt(100)
	e, f, g, h = cumulative(secondRound)
	plot2CDF(a, e, b, c, d)
	
	# n = 1000
	thirdRound = []
	thirdRound = listIt(1000)
	simpleHist(thirdRound)
	a3, b3, c3, d3 = cumulative(thirdRound)
	fourthRound = []
	fourthRound = listIt(1000)
	e3, f3, g3, h3 = cumulative(fourthRound)
	plot2CDF(a3, e3, b3, c3, d3)
	
	
if __name__ == '__main__':
    main()

	

