import nilearn as nl

from neuromaps import images

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