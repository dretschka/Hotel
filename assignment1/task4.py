# assignment 1 task4
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de


import random
import math
import matplotlib.pyplot as plt
import matplotlib.patches as lpatches

sin = []
cosin = []
xcoord = []

plt.axis([0, 90, 0, 1])
plt.xlabel('x [radiant]')
plt.ylabel('y')

for i in range(0, 10):
    x = random.randint(0,90)
    xcoord.append(x)
    sin.append(math.sin(math.radians(x)))
    cosin.append(math.cos(math.radians(x))) 

plt.plot(xcoord, sin, "ro",  label = "sinus")
plt.plot(xcoord, cosin, "g^", label = "cosinus")

plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0)

plt.show()