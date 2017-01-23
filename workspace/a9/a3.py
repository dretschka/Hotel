import sys
import pandas as pd
import math

def create_graph():
    graph = {}
    if(len(df2.name) == len(df2.out_links)):
        
        for i in range(0,len(df2.name)):
            graph.update({df2.name[i]:df2.out_links[i]})
    else:
        graph = 'unequal length'
    
    return graph
    
def get_edges(name):
    edges = []
    for edge in graph.get(name):
        edges.append((name,edge))
    return edges
    
def shortest_path(start, edges):
    distance = {}
    previous = {}
    
    for name in df2.name:
        distance.update({name : math.inf })
        previous.update({name : None})
    distance[start] = 0
    print(len(distance))
    for (u,v) in edges:
        if (u not in distance):
            distance.update({u : math.inf})
        elif (v not in distance):
            distance.update({v : math.inf})
    
    for i in range(1, len(df2.name)-1):
        for (u,v) in edges:
            if distance[u] + 1 < distance[v]:
                distance[v] = distance[u] +1
                previous[v] = u
    
    print(distance)
    return distance
def main():
    global df1, df2, graph
    if(len(sys.argv) > 1):
        fileName = sys.argv[1]
    else:
        fileName = 'store2.h5'
    store = pd.HDFStore(fileName)
    df1 = store['df1']
    df2 = store['df2']
    df2name = df2.name[0]
    graph = create_graph()
    paths = {}
    edges = []
    distance = {}
    for name in df2.name:
        edges += get_edges(name)
    fobj = open('pathList.txt', 'w')
    for name in df2.name:
        distance += shortest_path(name, edges)
        fobj.write(name + ' : ' + str(distance))
    fobj.close()
if __name__ == '__main__':
    main() 