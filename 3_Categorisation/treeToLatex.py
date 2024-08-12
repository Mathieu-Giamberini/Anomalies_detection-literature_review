import os
import json
os.system(f"pdflatex ")

#Path
dirPATH  = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(dirPATH)

LaTeX_path = "..\\2_theReview\\section\\3_Overview\\1_tree\\"
template_main_path = LaTeX_path + "template\\template.tex"
template_standalone_path = LaTeX_path + "template\\template_standalone.tex"

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
    

def saveToTex(template_path:str, save_path:str, tree_tex:str):
    """Save to a latex file"""
    with open(template_path, "r") as template_file:
        template = template_file.read()

    tex = template.replace("%<tree>", tree_tex)

    with open(save_path, "w") as tree_file:
        tree_file.write(tex)




with open(json_tree_path, "r") as json_tree:
    tree = json.load(json_tree)

tree_forest_tex =dictToTex(treeTotree_rec(tree, "AD"))

#Main
saveToTex(template_main_path, LaTeX_path + "test\\test5.tex", tree_forest_tex)

#Standalone
tex_dir = ".\\tree_tex\\"
file_name = "tree.tex"
saveToTex(template_standalone_path, tex_dir + file_name, tree_forest_tex)
