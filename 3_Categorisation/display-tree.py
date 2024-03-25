from dash import Dash, html
import dash_cytoscape as cyto
from openpyxl import load_workbook

from pyvis.network import Network
import networkx as nx

import os

dirPATH  = os.path.dirname(os.path.realpath(__file__))

def rangeMax(cell_range:tuple[tuple]):
    return max([[float(cell.value) for cell in row] for row in cell_range])[0]

workbook = load_workbook(filename=dirPATH + "/Categorie-Methode liste.xlsx", data_only=True)
sheet = workbook.active

nx_graph = nx.Graph()
index = {}

i = 8
run = True
while run:
    name = sheet[f"I{i}"].value
    parent = sheet[f"J{i}"].value
    
    run = not (name is None and parent is None)
    name = str(i) if name is None else name

    if run :
        index[name] = i 

        nx_graph.add_node(i, title=name, label=name, )
        i += 1

i = 8
run = True
while run:
    name = sheet[f"I{i}"].value
    parent = sheet[f"J{i}"].value

    run = not (name is None and parent is None)
    
    if run:
        depth = float(sheet[f"K{i}"].value)
        max_depth = rangeMax(sheet[f"K8:K1000"])

        if parent is not None :
            nx_graph.add_edge(index[parent], i, weight=max_depth - depth)
        i += 1

nt = Network('1000px', '100%')

nt.from_nx(nx_graph)
nt.save_graph(dirPATH + '/tree.html')