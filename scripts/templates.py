import nilearn as nl
import pandas as pd
from neuromaps import images
import abagen

def get_destrieux():
    # load destrieux atlas
    destrieux = nl.datasets.fetch_atlas_surf_destrieux()
    destrieux_labels = [l.decode() for l in destrieux['labels']]
    # make labels to fit braincharts model IDPs
    destrieux_idps = [l for l in destrieux_labels if l not in ['Unknown', 'Medial_wall']]
    destrieux_idps = ['lh_' + l.replace('_and_', '&') + '_thickness' for l in destrieux_idps] + \
                    ['rh_' + l.replace('_and_', '&') + '_thickness' for l in destrieux_idps]
    # make gifti from parcellations vectors
    parc_destrieux = images.relabel_gifti(
        (images.construct_shape_gii(destrieux['map_left'], labels=destrieux_labels, intent='NIFTI_INTENT_LABEL'), 
        images.construct_shape_gii(destrieux['map_right'], labels=destrieux_labels, intent='NIFTI_INTENT_LABEL')), 
        background=['Medial_wall'])
    
    return parc_destrieux, destrieux_idps

def get_desikan_killiany():
    # load desikan killiany atlas
    desikan = abagen.fetch_desikan_killiany(surface=True)
    # get labels
    label_dict = images.load_gifti(desikan["image"][0]).labeltable.get_labels_as_dict()
    desikan_labels = [l for _, l in label_dict.items()]
    # make labels for use as IDPs
    desikan_idps = ['lh_' + l for l in desikan_labels[1:]] + ['rh_' + l for l in desikan_labels[1:]]
    # get labeled giftis
    parc_desikan = images.relabel_gifti(
        (images.construct_shape_gii(images.load_data(desikan["image"][0]), labels=desikan_labels, intent='NIFTI_INTENT_LABEL'), 
        images.construct_shape_gii(images.load_data(desikan["image"][1]), labels=desikan_labels, intent='NIFTI_INTENT_LABEL')), 
        background=["Unknown"]
    )
    
    return parc_desikan, desikan_idps