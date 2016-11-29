# assignment 5 task 2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as lpatches
import web_crawler.py as crawl

visited, total_links = crawl.report_func()
all = 0
tmplist = []
for each item in total_links:
	all += total_links[item[0]]
	tmplist.append(total_links[item[0]])
	
average = all/len(total_links)
sortlist = np.sort(tmplist)
median = sortlist[len(sortlist)]

print('total number of webpages: ' + visited)
print('total number of links encountered: ' + all)
print('average number of links per webpage: ' + average)
print('median number of links per webpage: ' + median)

# histogram
# scatterplot


plt.figure(1)
plt.subplot(211)
plt.xlabel('links per webpage')
plt.ylabel('frequency')
plt.title('Histogram of distribution of links')
plt.axis([0, 150, 0, 150])
plt.grid(True)
plt.hist(sortlist, 30, normed=1, range=(0,150), facecolor='r', alpha=0.75)

plt.subplot(212)
plt.xlabel('number of internal links')
plt.ylabel('number of external links')
plt.title('scatter plot')
for i in total_links:
	x = total_links[i[1]]
	y = total_links[i[2]]
	plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()