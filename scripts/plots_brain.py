import nilearn as nl
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
from surfplot import Plot

from .templates import get_destrieux


# functions to make parcellated gifti from input vector
def get_parc_gifti(data, 
                   parc_gifti=None):
    
    if parc_gifti is None:
        parc_gifti = get_destrieux()[0]
    lh = np.zeros(parc_gifti[0].darrays[0].data.shape)
    rh = np.zeros(parc_gifti[1].darrays[0].data.shape)
    for parcel_idx, parcel_val  in enumerate(data, start=1):
        lh[parc_gifti[0].darrays[0].data==parcel_idx] = parcel_val
        rh[parc_gifti[1].darrays[0].data==parcel_idx] = parcel_val
    lh[parc_gifti[0].darrays[0].data==0] = np.nan
    rh[parc_gifti[1].darrays[0].data==0] = np.nan
    return lh, rh

def get_parc_gifti_region(region_lh, 
                          region_rh, 
                          parc_gifti=None):
    
    if parc_gifti is None:
        parc_gifti = get_destrieux()[0]
    lh = np.zeros(parc_gifti[0].darrays[0].data.shape)
    rh = np.zeros(parc_gifti[1].darrays[0].data.shape)
    lh[parc_gifti[0].darrays[0].data==region_lh] = 1
    rh[parc_gifti[1].darrays[0].data==region_rh] = 1
    lh[parc_gifti[0].darrays[0].data==0] = np.nan
    rh[parc_gifti[1].darrays[0].data==0] = np.nan
    return lh, rh


# brain plot function
def plot_surf_ax(ax, 
                 lh=None, 
                 rh=None, 
                 fig=None,
                 template="pial", 
                 views=["lateral", "medial"], 
                 size=(2000,400), 
                 layout="row", 
                 plot="map",
                 c="viridis_r",
                 c_fill=None, 
                 c_outline=None, 
                 zoom=1.6, 
                 scale=(2, 2),
                 c_lims=None,
                 cbar=False, 
                 cbar_orientation="horizontal",
                 cbar_symm=False,
                 cbar_width=0.45,
                 rotate_labels=False, 
                 cbar_kws=dict()):

        
    fsaverage = nl.datasets.fetch_surf_fsaverage()
    
    p = Plot(
        surf_lh=fsaverage[f"{template}_left"] if lh is not None else None, 
        surf_rh=fsaverage[f"{template}_right"] if rh is not None else None, 
        layout=layout, size=size, zoom=zoom, views=views
    )
    
    if (lh is not None) | (rh is not None): 
        
        if (lh is not None) & (rh is not None):
            gifti_dict = dict(left=lh, right=rh)
        elif (lh is not None) & (rh is None):
            gifti_dict = dict(left=lh)
        else:
            gifti_dict = dict(right=rh)
        
        if c_lims is None:
            if cbar_symm==False:
                c_lims = (np.nanmin(lh), np.nanmax(lh))
            elif cbar_symm==True:
                c_lims = (-np.nanmax(np.abs(lh)), np.nanmax(np.abs(lh)))
                
        if plot == "map":
            p.add_layer(gifti_dict, cmap=c, color_range=c_lims)
        elif plot in ["region", "parcel", "roi"]:
            if c_fill is None:
                c_fill = ListedColormap([0.8392156862745098,0.15294117647058825,0.1568627450980392,1.0])
            if c_outline is None:
                c_outline = ListedColormap([0,0,0,1])
            p.add_layer(gifti_dict, cmap=c_fill, as_outline=False, cbar=False)
            p.add_layer(gifti_dict, cmap=c_outline, as_outline=True, cbar=False) 
            
    p.build(fig=fig, ax=ax, colorbar=False)
    
    # legend
    if cbar==True:
        if cbar_orientation=="horizontal":
            cbar = fig.colorbar(
                cm.ScalarMappable(
                    norm=Normalize(c_lims[0], c_lims[1]), 
                    cmap=c), 
                cax=ax.inset_axes([(1-cbar_width)/2, 0.05, cbar_width, 0.06]),
                orientation="horizontal",
                **cbar_kws
            )
        elif cbar_orientation=="vertical":
            cbar = fig.colorbar(
                cm.ScalarMappable(
                    norm=Normalize(c_lims[0], c_lims[1]), 
                    cmap=c), 
                cax=ax.inset_axes([1.04, 0.1, 0.03, 0.8]),
                orientation="vertical",
                **cbar_kws
            )
        if rotate_labels:
            plt.setp(cbar.ax.get_xticklabels(), rotation=-40, ha="left", rotation_mode="anchor")
            cbar.ax.tick_params(axis="x", which="major", pad=2)