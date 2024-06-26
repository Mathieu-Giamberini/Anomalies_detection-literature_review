from openpyxl import load_workbook

import pyvis
from pyvis.network import Network
import networkx as nx

from colour import Color
import os
import numpy as np
import pandas as pd

import bs4

dirPATH  = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirPATH)


def rangeMax(cell_range:tuple[tuple]):
    return max([[float(cell.value if cell.value is not None else 0.0) for cell in row] for row in cell_range])[0]


def getLoss(graph: nx.Graph, chosen:list[int], lmbd:float=1.0):
    distance = nx.all_pairs_shortest_path_length(graph)
    distance = pd.DataFrame.from_dict(dict(distance))

    chosenPush = np.sum(1/distance[chosen], axis=1)
    rootPull = distance.iloc[0]

    return chosenPush + lmbd*rootPull


colors = [Color("#97C2FC"), Color("#BBFC97"), Color("#FC97C2")]#FCD197
def colorNode(colors, isChosen=False, fact=0.0):
    if isChosen:
        return colors[0].hex
    
    else:
        n = len(colors) - 1

        n_fact = fact*n
        if n_fact < n :
            i = int(n_fact) 
            fact_i = n_fact - i
        
        else :
            i = n-1
            fact_i = 1.0


        colors1_hsl = np.array(colors[i].hsl)
        colors2_hsl = np.array(colors[i+1].hsl)

        diff = colors1_hsl[0] - colors2_hsl[0]

        if abs(diff) > .5:
            if diff > 0:
                colors2_hsl[0] += 1
            else :
                colors1_hsl[0] += 1

        color_res_hsl = colors2_hsl*fact_i + colors1_hsl*(1-fact_i)
        color_res_hsl %= 1

        return Color(hsl=color_res_hsl).hex

def gradStyle(colors:list[str]):
    style = """div.legend {
        position: absolute;
        top: 30px;
        left: 30px;
        width: 50px;
        height: 250px;
        background: linear-gradient(to top in hsl"""

    for i, color in enumerate(colors):

        style += f", {color} {int(100*i/(len(colors) - 1))}%"
        

    style += ")}"

    return style

workbook = load_workbook(filename="Categorie-Methode liste.xlsx", data_only=True)
sheet = workbook.active

print("Workbook loaded")

nx_graph = nx.Graph()
index:dict[str, int] = {} #parent index
children:dict[str, list[int]] = {}#child list

max_depth = rangeMax(sheet[f"K8:K1000"])

i = 8
run = True
chosen = []
while run:
    fullName = sheet[f"H{i}"].value
    name     = sheet[f"I{i}"].value
    parent   = sheet[f"J{i}"].value
    id       = sheet[f"G{i}"].value
    depth = float(sheet[f"K{i}"].value)

    isChosen = sheet[f"P{i}"].value == "x"

    if isChosen or name == "AD":
        chosen.append(i)

    run = not (name is None and parent is None)
    name = id if name is None else name

    if run :
        index[name] = i 

        parent_name = str(parent)
        if parent_name in children.keys():
            children[parent_name].append(i)
        else:
            children[parent_name] = [i]

        if parent is not None or name == "AD":
            nx_graph.add_node(i, title=fullName, label=str(name), shape= "triangle" if isChosen else "dot" )
        i += 1



for parent in children.keys():
    for i_child in children[parent]:    
        depth = float(sheet[f"K{i_child}"].value)

        if not parent == "None" :
            nx_graph.add_edge(index[parent], i_child, weight=max_depth - depth)




loss = getLoss(nx_graph, chosen,0.5)
loss_max = np.max(loss[loss != np.inf])
loss_min = np.min(loss[loss != np.inf])

for node in nx_graph.nodes :
    nx_graph.nodes[node]["color"] = colorNode(colors, node in chosen, (loss[node] - loss_min)/(loss_max - loss_min))

nt = Network('1000px', '100%')

treePath = 'tree.html'

nt.from_nx(nx_graph)
nt.save_graph(treePath)



# load the file
with open(treePath) as file:
    txt = file.read()
    soup = bs4.BeautifulSoup(txt, features="html.parser")

soup.head.style.append(gradStyle(colors))
soup.body.append(soup.new_tag("div", attrs={"class": "legend"}))

with open(treePath, "w") as file:
    file.write(str(soup.prettify()))