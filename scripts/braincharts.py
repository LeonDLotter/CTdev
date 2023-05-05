import os
import pickle
from os.path import join
import pandas as pd

import numpy as np
from tqdm.auto import tqdm
from pcntoolkit.normative import predict
from pcntoolkit.util.utils import create_design_matrix


def get_adapted_predictions(model_dir,
                            data_test,
                            data_adapt,
                            cols_cov=["age", "sex"],
                            col_site="site",
                            age_bspline_min=-5, age_bspline_max=110, 
                            site_ids_tr=None, idps=None):                      
    
    wd = os.getcwd()
    
    ## output dataframe
    pred = data_test[cols_cov + [col_site]].copy()
   
    ## Create dummy design matrix to extract "ideal" centile data
    X0_dummy = np.zeros((len(data_test), 2))
    X0_dummy[:,0] = data_test.age
    X0_dummy[:,1] = data_test.sex
    # create the design matrix
    X_dummy = create_design_matrix(
        X0_dummy, 
        xmin=age_bspline_min, 
        xmax=age_bspline_max,
        basis="bspline",
        site_ids=None, 
        all_sites=site_ids_tr)
    # save the dummy covariates
    cov_file_dummy = join(model_dir, "cov_bspline_dummy_mean.txt")
    np.savetxt(cov_file_dummy, X_dummy)

    # iterate IDPs
    for i_idp, idp in enumerate(tqdm(idps, desc="Iterating IDPs")): 
        print(f"IDP {i_idp}: {idp}")
        idp_dir = join(model_dir, idp)
        os.chdir(idp_dir)
        
        ###### PREDICT ######
        
        print("Preparing test data")
        
        # extract and save the response variables for the test set
        y_test = data_test[idp].to_numpy()
        y_test = y_test[:, np.newaxis]
        
        # save the variables
        resp_file_test = join(idp_dir, "resp_test.txt") 
        np.savetxt(resp_file_test, y_test)
            
        # configure and save the design matrix
        cov_file_test = os.path.join(idp_dir, "cov_bspline_test.txt")
        X_test = create_design_matrix(
            data_test[cols_cov], 
            site_ids=data_test[col_site],
            all_sites=site_ids_tr,
            basis="bspline", 
            xmin=age_bspline_min, 
            xmax=age_bspline_max)
        np.savetxt(cov_file_test, X_test)
        
        print("Preparing adaptation data")
        
        # save the covariates for the adaptation data
        X_adapt = create_design_matrix(
            data_adapt[cols_cov], 
            site_ids=data_adapt[col_site],
            all_sites=site_ids_tr,
            basis="bspline", 
            xmin=age_bspline_min, 
            xmax=age_bspline_max)
        cov_file_adapt = os.path.join(idp_dir, "cov_bspline_adapt.txt")          
        np.savetxt(cov_file_adapt, X_adapt)
        
        # save the responses for the adaptation data
        resp_file_adapt = os.path.join(idp_dir, "resp_adapt.txt") 
        y_adapt = data_adapt[idp].to_numpy()
        np.savetxt(resp_file_adapt, y_adapt)

        print("Predict")
                
        # save the site ids for the adaptation data
        sitenum_file_adapt = os.path.join(idp_dir, "sitenum_adapt.txt") 
        site_num_adapt = data_adapt[col_site].to_numpy(dtype=int)
        np.savetxt(sitenum_file_adapt, site_num_adapt)
        
        # save the site ids for the test data 
        sitenum_file_test = os.path.join(idp_dir, "sitenum_test.txt")
        site_num_test = data_test[col_site].to_numpy(dtype=int)
        np.savetxt(sitenum_file_test, site_num_test)
        
        # predict
        yhat_test, s2_test, Z = predict(
            cov_file_test, 
            alg="blr", 
            respfile=resp_file_test, 
            model_path=join(idp_dir, "Models"),
            adaptrespfile=resp_file_adapt,
            adaptcovfile=cov_file_adapt,
            adaptvargroupfile=sitenum_file_adapt,
            testvargroupfile=sitenum_file_test)
        
        ###### ADJUST CT DATA ######
        
        print("Adjust CT data for site effects")
        
        # load the normative model
        with open(join(idp_dir, "Models", 'NM_0_0_estimate.pkl'), 'rb') as handle:
            nm = pickle.load(handle) 
        
        # get the warp and warp parameters
        W = nm.blr.warp
        warp_param = nm.blr.hyp[1:nm.blr.warp.get_n_params()+1] 
            
        # adjust the original CT data site-wise based on the adaptation data
        y_test_rescaled = np.zeros((data_test.shape[0]))
        for site in np.unique(site_num_test):
            # first, select the data point belonging to this particular site
            idx = np.where((data_test[col_site] == site).to_numpy())[0] 
            idx_a = np.where((data_adapt[col_site] == site).to_numpy())[0]
            
            # adjust and rescale the data
            y_test_rescaled[idx], s2_rescaled = nm.blr.predict_and_adjust(
                nm.blr.hyp, 
                X_adapt[idx_a,:], 
                np.squeeze(y_adapt[idx_a]), 
                Xs=None, 
                ys=np.squeeze(y_test[idx]))  
        
        ###### GET NORMATIVE DATA ######
        
        # dummy predictions
        yhat_dummy, s2_dummy = predict(
            cov_file_dummy, 
            alg="blr", 
            respfile=None, 
            model_path=join(idp_dir, "Models"), 
            outputsuffix="_dummy")
        
        # get centile predictions (warp to input space)
        p50, _ = W.warp_predictions(
            mu=np.squeeze(yhat_dummy), 
            s2=np.squeeze(s2_dummy), 
            param=warp_param, 
            percentiles=[0.5])
        
        ###### SAVE RESULTS ######
        
        print("Saving results")

        pred[idp] = data_test[idp].astype(np.float32)
        pred[idp+"-rescaled"] = y_test_rescaled.astype(np.float32)
        pred[idp+"-pred50"] = p50.astype(np.float32)
        pred[idp+"-z"] = Z.astype(np.float32)
        pred[idp+"-s2"] = s2_test.astype(np.float32)
        pred = pred.copy()
        
        ###### REMOVE IDP DATA FILES ######
        
        temp = os.listdir(idp_dir)
        temp.remove("Models")
        [os.remove(join(idp_dir, f)) for f in temp]
            
    # remove dummy covariate file to save space
    os.remove(cov_file_dummy)
            
    os.chdir(wd)
    
    return(pred)


# ==================================================================================================

def get_centile_predictions(sex, model_dir, site_ids_tr=None, idps=None, 
                            age_min=-5, age_max=110, age_step=2, 
                            centiles=[0.5]):
    
    wd = os.getcwd()
    
    ## site ids of training data
    if site_ids_tr is None:
        site_ids_tr = list(np.loadtxt(join(model_dir, "site_ids_82sites.txt"), dtype=str))
        
    ## idps
    if idps is None:
        idps = list(np.loadtxt(join(model_dir, "idps_destrieux.txt"), str))
        
    ## create dummy subjects
    # age: 
    # min/max: limits of cubic B-spline basis 
    # step: temporal "resolution" (sampling rate per year)
    age = list(np.arange(age_min, age_max, 1/age_step))
    # sex
    # if sex is string
    if isinstance(sex, str):
        # set to corresponding integer
        if sex in ["F", "f", "fem", "female"]:
            sex = 0
        elif sex in ["M", "m", "male"]:
            sex = 1
    sex = [sex] * len(age)
    # put it together
    X0_dummy = np.zeros((len(age), 2))
    X0_dummy[:,0] = age
    X0_dummy[:,1] = sex

    ## create the design matrix
    X_dummy = create_design_matrix(
        X0_dummy, 
        xmin=age_min, xmax=age_max, 
        site_ids=None, 
        all_sites=site_ids_tr)

    ## save the dummy covariates
    cov_file_dummy = os.path.join(model_dir, "cov_bspline_dummy_mean.txt")
    np.savetxt(cov_file_dummy, X_dummy)

    ## empty 3D array with size parcels x timepoints x percentiles
    predicted_ct = np.zeros((len(idps), len(age), len(centiles)))
    
    ## get the data
    for idp_num, idp in enumerate(tqdm(idps, desc="Iterating IDPs")): 
        print(f"IDP {idp_num}: {idp}")
        idp_dir = join(model_dir, idp)
        os.chdir(idp_dir)
        
        # set up the covariates for the dummy data
        yhat, s2 = predict(cov_file_dummy, 
                        alg = 'blr', 
                        respfile = None, 
                        model_path = join(idp_dir, 'Models'), 
                        outputsuffix = '_dummy')
        
        # load the normative model
        with open(join(idp_dir, 'Models', 'NM_0_0_estimate.pkl'), 'rb') as handle:
            nm = pickle.load(handle) 
        
        # get the warp and warp parameters
        W = nm.blr.warp
        warp_param = nm.blr.hyp[1:nm.blr.warp.get_n_params()+1] 
            
        # get centile predictions (warp to input space)
        _, pr_int = W.warp_predictions(np.squeeze(yhat), np.squeeze(s2), warp_param, percentiles=centiles)
        
        # save
        predicted_ct[idp_num,:,:] = pr_int
        
        # clean IDP directory to save space
        temp = os.listdir(idp_dir)
        temp.remove("Models")
        [os.remove(join(idp_dir, f)) for f in temp]
        
    # remove dummy covariate file to save space
    os.remove(cov_file_dummy)
    
    os.chdir(wd)
           
    # return array
    return predicted_ct, age, sex
     