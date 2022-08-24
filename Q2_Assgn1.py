#!/usr/bin/env python
# coding: utf-8


# Importing libraries
import json
import pandas as pd

# Opening Modified neighbor district JSON file into dictionary
with open("neighbor-districts-modified.json") as neighbor_json:
    neighbor_districts_modified_data = json.load(neighbor_json)

# Creating list of lists of district and its each neighbor district
neighbor_dist_graph = []
for k in neighbor_districts_modified_data.keys():
    for n in neighbor_districts_modified_data[k]:
        neighbor_dist_graph.append([k,n])

# Removing reverse edge (neighbor district - district pair) from above list
# Example if A is neighbor of B present in the list then its reverse B is neighbor of A should be removed
for dList in neighbor_dist_graph:
    rdList = [dList[1],dList[0]]
    if rdList in neighbor_dist_graph:
        neighbor_dist_graph.remove(rdList)

# Converting above list to edge_graph DataFrame
edge_graph = pd.DataFrame(neighbor_dist_graph, columns=['District','Neighbor_District'])

# Generating output edge-graph.csv file from above DataFrame
edge_graph.to_csv('edge-graph.csv', index=False)
