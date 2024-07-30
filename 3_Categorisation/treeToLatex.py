import os
import json

#Path
dirPATH  = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(dirPATH)

LaTeX_path = "..\\2_theReview\\section\\3_Overview\\1_tree\\"
template_path = LaTeX_path + "template\\template.tex"

json_tree_path = "tree.json"

def treeTotree_rec(tree:dict, root:str, depth:int=0) -> dict:
    """Convert a linear tree to a recursive one"""
    tree_rec = {root:{}}

    for child in tree[root]["children"]:
        tree_rec[root].update(treeTotree_rec(tree, child, depth+1))

    return tree_rec


def dictToTex(tree_rec:dict, depth:int = 0) -> str:
    """Convert dict tree to forest (LaTeX) tree"""
    tree_tex = ""

    for name, sub_tree in tree_rec.items():
        tree_tex += treeSyntax(name, dictToTex(sub_tree, depth+1), depth)

    return tree_tex


def treeSyntax(node:str, child:str, depth:int):
    """Get the tree syntax base on the depth"""

    match depth:
        case 0:
            return f"[{node} [, grow subtree=south {child}]]"
        case 1:
            return f"\n[{node}, grow subtree=east {child}]"
        case _: 
            return f"[{node} {child}] "
    



with open(json_tree_path, "r") as json_tree:
    tree = json.load(json_tree)

with open(template_path, "r") as template_file:
    template = template_file.read()

tex = template.replace("%<tree>", dictToTex(treeTotree_rec(tree, "AD")))

with open(LaTeX_path + "test\\test5.tex", "w") as tree_file:
    tree_file.write(tex)