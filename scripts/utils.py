import pandas as pd
import numpy as np


# p-to-asterisk function
def p_to_ast(p_data, pc_data):
    p_1d = np.array(p_data).flatten()
    pc_1d = np.array(pc_data).flatten()
    ast = list()
    for (p, pc) in zip(p_1d, pc_1d):
        if (pc < 0.05): ast.append("★")
        elif (p < 0.05) & (pc >= 0.05): ast.append("☆")
        else: ast.append("")
    return pd.DataFrame(np.array(ast).reshape(p_data.shape), index=p_data.index, columns=p_data.columns)


# reorder dataframes and idps
def reorder_vars(first_vars, df, idps):
    idp_vars = []
    for i in idps:
        idp_vars += [c for c in df.columns if i in c]
    return df[first_vars + [c for c in df.columns if c not in first_vars+idp_vars] + idp_vars].copy()


# helper to add pre/suffix to IDP (surface region) names
def alt_idps(suffix="", idp=None, prefix=""):
    return [prefix + idp + suffix for idp in idp]


# helper to add pre/suffix to predictor names
def alt_preds(prefix="", pred=None, suffix=""):
    return [prefix + p + suffix for p in pred]


def na():
    return slice(None)


def replace(ls, replace_what="", replace_with=""):
    return [l.replace(replace_what, replace_with) for l in ls] 
    
    
def sel_ls(ls, starts=None, ends=None, isin=None, isnotin=None):
    if starts is not None:
        ls = [i for i in ls if i.startswith(starts)]
    if ends is not None:
        ls = [i for i in ls if i.endswith(ends)]
    if isin is not None:
        ls = [i for i in ls if isin in i]
    if isnotin is not None:
        ls = [i for i in ls if isnotin not in i]
    return ls
    
    
def sel_cols(df, starts=None, ends=None, isin=None, isnotin=None):
    return sel_ls(df.columns, starts=starts, ends=ends, isin=isin, isnotin=isnotin)


def add_to_str(string, prefix="", suffix="", delim=""):
    if isinstance(string, str):
        return prefix + delim + string + delim + suffix
    elif isinstance(string, (list, pd.Index)):
        return [prefix + delim + s + delim + suffix for s in string]