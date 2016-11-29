# assignment 5 task 3
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as lpatches
import web_crawler as crawl

visited, total_links = crawl.report_func()

all = 0
tmplist = []
for item in total_links:
	all += item[0]
	tmplist.append(item[0])
	
average = all/len(total_links)
sortlist = np.sort(tmplist)
medi = np.median(sortlist)

print('total number of webpages: ' + str(visited))
print('total number of links encountered: ' + str(all))
print('average number of links per webpage: ' + str(average))
print('median number of links per webpage: ' + str(medi))

linkCount = [link[0] for link in total_links]

# histogram
plt.figure(1)
plt.subplot(211)
plt.xlabel('links per webpage')
plt.ylabel('frequency')
plt.title('Histogram of distribution of links')
#plt.axis([0, 150, 0, 1500])
plt.grid(True)
plt.hist(linkCount, bins=30, range=(0,150), facecolor='g', alpha=0.75)

# scatterplot
plt.subplot(212)
plt.xlabel('number of internal links')
plt.ylabel('number of external links')
plt.title('scatter plot - relation from internal to external links')
for i in total_links:
	x = i[1]
	y = i[2]
	area = i[0]
	plt.scatter(x, y, s=area, alpha=0.5)
plt.tight_layout()
plt.show()