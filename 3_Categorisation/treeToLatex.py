import os
import json

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


def dictToTex(tree_rec:dict, info:dict, depth:int = 0) -> str:
    """Convert dict tree to forest (LaTeX) tree"""
    tree_tex = ""

    for name, sub_tree in tree_rec.items():
        if not info[name]["hideTex"]:
            tree_tex += treeSyntax(name, dictToTex(sub_tree, info, depth+1), depth, 4)

    return tree_tex


def treeSyntax(node:str, child:str, depth:int, nIndent:int = 0):
    """Get the tree syntax base on the depth"""
    indent = " "*4*nIndent
    match depth:
        case 0:
            return f"[{node} [, grow subtree=south{child}\n]]"
        case 1:
            return f"\n{indent}[{node}, grow subtree=east, calign=last  {child}]"
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

tree_forest_tex =dictToTex(treeTotree_rec(tree, "AD"), tree)

#Main
saveToTex(template_main_path, LaTeX_path + "gen\\tree.tex", tree_forest_tex)

#Standalone
tex_dir = ".\\tree_tex\\"
file_name = "tree.tex"
saveToTex(template_standalone_path, tex_dir + file_name, tree_forest_tex)
