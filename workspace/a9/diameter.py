import sys
import pandas as pd
import math
from queue import *

#this creates a dictionary with the article name as the node of the graph and its outgoing links as the connection between the nodes.
#Note: the connections between the nodes are one-directional, because an outgoing link may appear in one article
#but there may not be an outgoing link to the previous article.
#The nodes are the keys and the lists of connections are the values in our dictionary.

def create_graph():
    graph = {}
    if(len(df2.name) == len(df2.out_links)):
        
        for i in range(0,len(df2.name)):
            graph.update({df2.name[i]:df2.out_links[i]})
    else:
        graph = 'unequal length'
    
    return graph

# This is the actual calculation of the shortest path from a given article to every other article
# using all possible combinations of outgoing links
# it returns a dictionary with the name of the destination article and the length of its path
    
def shortest_path(start, edges):
    q = Queue()
    distance = {}
    previous = {}
    visited = [start]
    distance[start] = 0
    q.put(start)
    
    while (q.empty() is False):
        x = q.get()
        try:
            for edge in graph.get(x):
                if (edge not in visited):
                    distance[edge] = distance[x] + 1
                    previous[edge] = x
                    q.put(edge)
                    visited.append(edge)
        except TypeError:
            pass
    return distance

# This method gets the dictionary with all the shortest paths as an argument and simply has to iterate over it
# in order to find the largest value. That largest value is the diameter of the graph    
    
def get_diameter(dict):
    start = ''
    end = ''
    diameter = 0
    for (key, path) in dict.items():
        for(link, val) in path.items():
            if (val > diameter):
                diameter = val
                start = key
                end = link
    return (diameter, start, end)
#This method simply stores every possible edge (starting and end point) in the whole graph into a single list    
def get_edges(name):
    edges = []
    for edge in graph.get(name):
        edges.append((name,edge))
    return edges

#Note: This program takes very long to terminate, since it has a complexity of O(V * (V + E)), where V is the number of Articles and E is the total number of outgoing links. The algorithm for calculating the shortest path uses the Breadth-First Search Algorithm. It may take several hours to calculate the diameter.     
# That being said, since the longest shortest path possible can only be as large as the amount of articles - 1, the diameter can not exceed that value 
def main():
    global df1, df2, graph
    if(len(sys.argv) > 1):
        fileName = sys.argv[1]
    else:
        fileName = 'store2.h5'
    store = pd.HDFStore(fileName)
    df1 = store['df1']
    df2 = store['df2']
    
    graph = create_graph()
    
    edges = []
    distance = {}
    for name in df2.name:
        edges += get_edges(name)
    for name in df2.name:
        distance[name] = shortest_path(name, edges)
    (diam, start, end) = get_diameter(distance)
    print('The diameter is: \nFrom: ' + start + '\nTo: ' + end +'\nValue: ' + str(diam))

    
    
if __name__ == '__main__':
    main() 