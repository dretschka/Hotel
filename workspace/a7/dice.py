# assignment 7 task 3
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import numpy as np
import matplotlib.pyplot as plt
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
		t1 = roll()
		t2 = roll()
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
		if i < 7:
			if i < 4:
				if i == 2:
					c2 += 1
				else:
					c3 += 1
			elif i < 6:
				if i == 4:
					c4 += 1
				else:
					c5 += 1
			else:
				c6 += 1
		else:
			if i < 11:
				if i < 9:
					if i == 7:
						c7 += 1
					else:
						c8 += 1
				elif i == 9:
					c9 += 1
				else:
					c10 += 1
			elif i == 11:
				c11 +=1
			else:
				c12 +=1
#calculate probabilities
	prob2 = c2/len(rollResults)
	prob3 = c3/len(rollResults)
	prob4 = c4/len(rollResults)
	prob5 = c5/len(rollResults)
	prob6 = c6/len(rollResults)	
	prob7 = c7/len(rollResults)
	prob8 = c8/len(rollResults)
	prob9 = c9/len(rollResults)
	prob10 = c10/len(rollResults)
	prob11 = c11/len(rollResults)
	prob12 = c12/len(rollResults)
	
	cumProb = prob2 + prob3 + prob4 + prob5 + prob6 + prob7 + prob8 + prob9 + prob10 + prob11 + prob12
	cumList = [prob2, prob3, prob4, prob5, prob6, prob7, prob8, prob9, prob10, prob11, prob12]
	
	plt.hist(cumList, bins=11, range=(2,12), facecolor='g', alpha=0.75)
	plt.title("cumulative distribustion")
	plt.xlabel("Value")
	plt.ylabel("cumulated probabilities")
	
	plt.show()
	
# CDF plot (median, probability of dice sum <10)

# max point-wise distance
	
def main():	
	firstRound = []
	firstRound = listIt(100)
	simpleHist(firstRound)
	cumulative(firstRound)

if __name__ == '__main__':
    main()

	

