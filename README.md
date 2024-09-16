<img src="plots/braincharts/dev_ct_brainchain.png">

---

# <a name="top"></a>Regional patterns of human cortex development correlate with underlying neurobiology

This repository accompanies the paper: 

Leon D. Lotter, Amin Saberi, Justine Y. Hansen, Bratislav Misic, Casey Paquola, Gareth J. Barker, Arun L.W. Bokde, Sylvane Desrivières, Herta Flor, Antoine Grigis, Hugh Garavan, Penny Gowland, Andreas Heinz, Rüdiger Brühl, Jean-Luc Martinot, Marie-Laure Paillère, Eric Artiges, Dimitri Papadopoulos Orfanos, Tomáš Paus, Luise Poustka, Sarah Hohmann, Juliane H. Fröhner, Michael N. Smolka, Nilakshi Vaidya, Henrik Walter, Robert Whelan, Gunter Schumann, IMAGEN Consortium, Frauke Nees, Tobias Banaschewski, Simon B. Eickhoff, and Juergen Dukart (2024). *[Regional patterns of human cortex development correlate with underlying neurobiology](https://doi.org/10.1038/s41467-024-52366-7)*. Nature Communications.

[![DOI](https://img.shields.io/badge/Nature_Communications-10.1038/s41467--024--52366--7-E63323)](https://doi.org/10.1038/s41467-024-52366-7)
[![DOI](https://img.shields.io/badge/bioRxiv-10.1101/2023.05.05.539537-BD2736)](https://doi.org/10.1101/2023.05.05.539537)
[![DOI](https://zenodo.org/badge/636815203.svg)](https://zenodo.org/badge/latestdoi/636815203)
[![Twitter](https://img.shields.io/badge/Twitter-Thread-1A8CD8)](https://twitter.com/LeonDLotter/status/1655582681613189120)
[![Mastodon](https://img.shields.io/badge/Mastodon-Thread-6364FF)](https://neuromatch.social/@LeonDLotter/110332987427316809)  

## Abstract

Human brain morphology undergoes complex changes over the lifespan. Despite recent progress in tracking brain development via normative models, current knowledge of underlying biological mechanisms is highly limited. We demonstrate that human cerebral cortex development and aging trajectories unfold along patterns of molecular and cellular brain organization, traceable from popu-lation-level to individual developmental trajectories. During childhood and adolescence, cortex-wide spatial distributions of dopaminergic receptors, inhibitory neurons, glial cell populations, and brain-metabolic features explain up to 50% of variance associated with a lifespan model of regional corti-cal thickness trajectories. In contrast, modeled cortical change patterns during adulthood are best explained by cholinergic and glutamatergic neurotransmitter receptor and transporter distributions. These relationships are supported by developmental gene expression trajectories and translate to individual longitudinal data from over 8,000 adolescents, explaining up to 59% of developmental change at cohort- and 18% at single-subject level. Integrating neurobiological brain atlases with normative modeling and population neuroimaging provides a biologically meaningful path to un-derstand brain development and aging in living humans.

<br>
<img src="plots/prediction_dominance/animation/dev_ct_animation_fm_500_5.gif">  
<br>

## License

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  

Content of this repository is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

Please cite both the publication and the dataset (Zenodo) when using data from this repository. Also, note that third-party data included in this repository requires direct citation if used in other contexts. This applies to all PET imaging and mRNA expression data and to the normative model by Rutherford et al. Please see the manuscript and the supplementary material for references.

## Content

### `Jupyter notebooks`
The Jupyter notebooks contain all the analyses code in sequential order. The code is largely commented, but gets quite complex towards the end of the workflow. Feel free to ask me questions if you try to work with it and got stuck.

### `data_predictors`
Contains the data used as "predictors" in spatial association analyses. I.e, you can find the original PET imaging and extracted data, lists of cell marker genes and extracted ABA gene expression data, and an T1/T2 ratio MRI surface file as a myelination marker. Please find all references in the manuscript's supplementary materials. In the table files, you find the extracted and dimensionality reduced data that was used for the majority of the analyses. Two PET maps (GABAa used in the main analyses, and a mGluR5 map used in temporal stability analyses) cannot be shared and have to be [requested from the authors](https://doi.org/10.26165/JUELICH-DATA/HDVEEF). 

### `model_rutherford`
Contains the [Braincharts model](https://github.com/predictive-clinical-neuroscience/braincharts) by Rutherford et al. (2022).

### `data_rutherford`
Contains the data that were extracted from the Braincharts model to be used for the analyses. The output data of the spatial association analyses performed in "1_predictions_rutherford.ipynb", wrapped into JuSpyce objects, are relatively large (~300 MB per file). Admittedly, this is in part due to inefficient storage and will be fixed in the future. As the data can't be included in a GitHub repo, they are available in a separate [OSF repository](https://osf.io/3n9rt/). There is a code block in the respective notebook that automatically downloads the data from OSF if you uncomment it.  

### `data_expression`
Contains processed developmental gene expression data from the [Human Brain Transcriptome](https://hbatlas.org/) and [Kang et al. (2011)](https://www.nature.com/articles/nature10523), as well as the extracted data used for the present analyses.  

### `data_ABCD-IMGN`
This is empty and would contain the ABCD and IMAGEN in- and output data. These data are protected and thus not included in the repository. If you would like to access the data AND already have ABCD or IMAGEN access approval, feel free to contact us. The code, however, is included in this repository. See also the notes in each notebook.  

### `plots`
All plots generated in the notebooks.

### `scripts`
All analyses scripts. Because the [JuSpyce toolbox](https://github.com/LeonDLotter/JuSpyce) on which we heavily rely here is not on pip yet, I included the used version of JuSpyce in the repository (`/scripts/juspyce`). 

### `templates`
Contains only the Destrieux parcellation as left and right hemisphere gifti files.

### `environment.yml`
This is the conda environment in which the analyses were run, exported via `conda env export > environment.yml`. If you installed Python via Anaconda, you can recreate this environment with `conda env create -f environment.yml`. However, note that this will likely only work on a similar system: macOS Monterey 12.6 on a 2021 MPB with M1 Pro chip. On other systems you might have to take a look at the `environment.yml` file and each individual notebook and install the dependencies manually.   

## Further resources

- [Braincharts model](https://github.com/predictive-clinical-neuroscience/braincharts) by Rutherford et al. (2022)  
- [Neuromaps toolbox](https://github.com/netneurolab/neuromaps)
- [JuSpyce](https://github.com/LeonDLotter/JuSpyce)
- [JuSpace](https://github.com/juryxy/JuSpace) 

## Contact

If you have any problems, questions, comments or suggestions, feel free to open an issue or [contact me](mailto:leondlotter@gmail.com)! 

---
<img src="plots/braincharts/dev_ct_brainchain.png">  

[Back to the top](#top)
