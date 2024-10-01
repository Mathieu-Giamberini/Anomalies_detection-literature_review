# -*- coding: utf-8 -*-
import os
import json

import re

#Path
dirPATH  = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(dirPATH)

#Tree
LaTeX_path_tree = "..\\2_theReview\\section\\3_Overview\\1_tree\\"
tree_template_main_path = LaTeX_path_tree + "template\\template.tex"
tree_template_standalone_path = LaTeX_path_tree + "template\\template_standalone.tex"

#Acronyms
LaTeX_path_acr = "..\\2_theReview\\section\\9_Appendices\\1_Acronyms\\"
acr_main_path  = LaTeX_path_acr + "acronyms.tex"

json_tree_path = "tree.json"

def treeTotree_rec(tree:dict, root:str, depth:int=0) -> dict:
    """Convert a linear tree to a recursive one"""
    tree_rec = {root:{}}

    for child in tree[root]["children"]:
        tree_rec[root].update(treeTotree_rec(tree, child, depth+1))

    return tree_rec


def infoToTex(tree_rec:dict, infos:dict, depth:int = 0) -> str:
    """Convert dict tree to forest (LaTeX) tree"""
    tree_tex = ""

    for name, sub_tree in tree_rec.items():
        if not infos[name]["hideTex"]:
            tree_tex += treeSyntax(name, infos[name], infoToTex(sub_tree, infos, depth+1), depth, 4)

    return tree_tex


def treeSyntax(node:str, info:dict ,child:str, depth:int, nIndent:int = 0):
    """Get the tree syntax base on the depth"""
    indent = " "*4*nIndent

    name = node if info['fullName'] is None else f"\\acused{{{node}}}\\ac{{{node}}}"

    match depth:
        case 0:
            return f"[{name} [, grow subtree=south{child}\n{indent}]]"
        case 1:
            return f"\n{indent}[\\textbf{{{name}}}, grow subtree=east, calign=last {child}]"
        case _: 
            return f"[{name} {child}] "
    

def saveTreeToTex(template_path:str, save_path:str, tree_tex:str):
    """Save to a latex file"""
    with open(template_path, "r") as template_file:
        template = template_file.read()

    tex = template.replace("%<tree>", tree_tex)

    with open(save_path, "w") as tree_file:
        tree_file.write(tex)


def infoToAcrTex(infos:dict, nIndent:int=0, indent=4*" ", display_log:bool = True):
    res = ""
    warning_log = False
    
    for name, info in infos.items():
        if not info['hideTex'] :
            if info['fullName'] is None:
                if display_log:
                    print(name, "as no full name")
                elif not warning_log:
                    print("Warning: Failed to log")
                    warning_log = True
            else:
                res += indent*nIndent + f"\\acro{{{name}}}{{{info['fullName']}}}\n"
    
    res += indent*nIndent
    return res


def findKeyPos(key:str, string:str):
    start = f"<{key}>"
    end = f"</{key}>"

    allStart = [m.end()   + 1 for m in re.finditer(start, string)]
    allEnds  = [m.start() - 1 for m in re.finditer(end,   string)]
    
    return zip(allStart, allEnds)


def insertInFile(PATH:str, key:str, text:str) :
    with open(PATH, "r+") as file:
        file_str = file.read()

        Is = findKeyPos(key, file_str)
        o = 0
        for i_s, i_e in Is:
            old_str = file_str[i_s:i_e]
            file_str = file_str[: i_s+o] + text + file_str[i_e+o:]

            o += len(text) - len(old_str)
        
        file.seek(0)
        file.write(file_str)
        file.truncate()




with open(json_tree_path, "r") as json_tree:
    tree = json.load(json_tree)


tree_forest_tex =infoToTex(treeTotree_rec(tree, "AD"), tree)

#Main
saveTreeToTex(tree_template_main_path, LaTeX_path_tree + "gen\\tree.tex", tree_forest_tex)

#Standalone
tex_dir = ".\\tree_tex\\"
file_name = "tree.tex"
saveTreeToTex(tree_template_standalone_path, tex_dir + file_name, tree_forest_tex)

#Acronym
insertInFile(acr_main_path, "tree", infoToAcrTex(tree, 3, display_log=False))
