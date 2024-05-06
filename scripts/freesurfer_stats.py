import pandas as pd
import os
from os.path import join
from tqdm.auto import tqdm
from joblib import Parallel, delayed


def get_cx_stats(file, hemi, 
                 measure=["ThickAvg", "SurfArea", "GrayVol"], 
                 suffix=["_thickness", "_area", "_volume"],
                 get_globals=True):
    
    with open(file) as f:
        lines = f.readlines()
        global_metrics = dict()
        
        for i, line in enumerate(lines):
            
            if "MeanThickness" in line: global_metrics[f"{hemi}_MeanThickness"] = float(line.split(", ")[3])
            if "CortexVol" in line: global_metrics["CortexVol"] = float(line.split(", ")[3])
            if ("SupraTentorialVol" in line) & ("NotVent" not in line): global_metrics["SupraTentorialVol"] = float(line.split(", ")[3])
            if "SupraTentorialVolNotVent" in line: global_metrics["SupraTentorialVolNotVent"] = float(line.split(", ")[3])
            if "EstimatedTotalIntraCranialVol" in line: global_metrics[f"EstimatedTotalIntraCranialVol"] = float(line.split(", ")[3])  
            
            if not line.startswith("#"):
                columns = lines[i-1].replace("\n","").split(" ")[2:]
                data = pd.read_csv(
                    file,
                    delim_whitespace=True,
                    names=columns,
                    comment="#"
                )
                data = data.set_index("StructName")
                data = data[measure]
                idx = [f"{hemi}_{idx}{suffix[i]}" for i in range(len(measure)) for idx in data.index]
                data = pd.concat([data[c] for c in data.columns])
                data.index = idx
                if get_globals:
                    data = pd.concat([data, pd.Series(global_metrics)])
                break
    f.close() 
    return data


def get_sc_stats(file, measure="Volume_mm3", suffix=""):
    
    with open(file) as f:
        lines = f.readlines()
        global_metrics = dict()
         
        for i, line in enumerate(lines):
            
            if "lhCortexVol" in line: global_metrics["lhCortexVol"] = float(line.split(", ")[3])
            if "rhCortexVol" in line: global_metrics["rhCortexVol"] = float(line.split(", ")[3])
            if "CortexVol" in line: global_metrics["CortexVol"] = float(line.split(", ")[3])
            if "lhCerebralWhiteMatter" in line: global_metrics["lhCerebralWhiteMatter"] = float(line.split(", ")[3])
            if "rhCerebralWhiteMatter" in line: global_metrics["rhCerebralWhiteMatter"] = float(line.split(", ")[3])
            if "SubCortGrayVol" in line: global_metrics["SubCortGrayVol"] = float(line.split(", ")[3])
            if "TotalGrayVol" in line: global_metrics["TotalGrayVol"] = float(line.split(", ")[3])
            if "SubCortGrayVol" in line: global_metrics["SubCortGrayVol"] = float(line.split(", ")[3])
            if "SubCortGrayVol" in line: global_metrics["SubCortGrayVol"] = float(line.split(", ")[3])
            if "SubCortGrayVol" in line: global_metrics["SubCortGrayVol"] = float(line.split(", ")[3])
            if ("SupraTentorialVol" in line) & ("NotVent" not in line): global_metrics["SupraTentorialVol"] = float(line.split(", ")[3])
            if "SupraTentorialVolNotVent" in line: global_metrics["SupraTentorialVolNotVent"] = float(line.split(", ")[3])
            if "EstimatedTotalIntraCranialVol" in line: global_metrics[f"EstimatedTotalIntraCranialVol"] = float(line.split(", ")[3])  
            if "lhSurfaceHoles" in line: global_metrics["lh_en"] = float(line.split(", ")[3])
            if "rhSurfaceHoles" in line: global_metrics["rh_en"] = float(line.split(", ")[3])
            if "SurfaceHoles" in line: global_metrics["total_en"] = float(line.split(", ")[3])
            
            if not line.startswith("#"):
                columns = lines[i-1].replace("\n","").split(" ")[2:]
                columns = [c for c in columns if c!=""]
                data = pd.read_csv(
                    file,
                    delim_whitespace=True,
                    names=columns,
                    comment="#")
                data = data.set_index(pd.Index([f"{c}{suffix}" for c in data["StructName"]]))
                data = data[measure]
                data = pd.concat([data, pd.Series(global_metrics)])
                break
    f.close() 
    return data


def get_euler(file):
    with open(file) as f:
        lines = f.readlines()
        en = []
        for line in lines:
            for i, hemi in enumerate(["lh", "rh"]):
                if line.startswith(f"# Measure {hemi}SurfaceHoles"):
                    en.append(int(line.split(",")[3]))
                    break
    f.close()
    return en


def collect_fs_stats(subs_dir, subs, parc="destrieux", verbose=True, progress=True, 
                     return_as_df=True, n_proc=-1):

    subs_data = dict()
        
    def par_fun(sub):
        
        sub_data = list()
        
        if parc == "destrieux":
            aparc_file = "%s.aparc.a2009s.stats"
        elif parc == "desikan":
            aparc_file = "%s.aparc.stats"
            
        # aparc
        for hemi in ["lh", "rh"]:
            sub_path = join(subs_dir, sub, "stats", aparc_file % hemi)
            if os.path.exists(sub_path):
                sub_data.append(get_cx_stats(sub_path, hemi))
            else:
                if verbose:
                    print("Sub", sub, "file", aparc_file % hemi, "not found.")
        
        # aseg
        sub_path = join(subs_dir, sub, "stats", "aseg.stats")
        if os.path.exists(sub_path):
            sub_data.append(get_sc_stats(sub_path))
        else:
            if verbose:
                print("Sub", sub, "file aseg.stats not found.")
                
        # collect data
        if sub_data != []:
            return pd.concat(sub_data) #.drop_duplicates()
        else:
            return None
        
    subs_data = Parallel(n_proc)(
        delayed(par_fun)(sub) 
        for sub in tqdm(subs, desc="Subjects/Sessions", disable=not progress)
    )
    subs_data = {sub: subs_data[i] for i, sub in enumerate(subs) if subs_data[i] is not None} 
        
    # collect data
    if return_as_df:
        cols = set()
        for sub in subs_data:
            cols.update(set(subs_data[sub].index.to_list()))
        subs_df = pd.DataFrame(index=subs_data.keys(), columns=list(cols))
        for sub in subs_data:
            cols = subs_data[sub].index.unique()
            subs_df.loc[sub, cols] = subs_data.loc[:, ~subs_data.columns.duplicated()][cols]
        #subs_data = pd.DataFrame(subs_data).T
        subs_data = subs_data.loc[:, ~subs_data.columns.duplicated()]
        new_col_order = \
            ["lh_en", "rh_en", "total_en"] + \
            [c for c in subs_data.columns if c.endswith("_thickness")] + \
            [c for c in subs_data.columns if c.endswith("_area")] + \
            [c for c in subs_data.columns if c.endswith("_volume")]
        new_col_order = new_col_order + [c for c in subs_data.columns if c not in new_col_order]
        subs_data = subs_data[[c for c in new_col_order if c in subs_data]]
    else:
        return subs_data




