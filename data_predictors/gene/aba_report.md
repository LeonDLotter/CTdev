Regional microarry expression data were obtained from 6 post-mortem brains (1 female, ages 24.0--57.0, 42.50 +/- 13.38) provided by the Allen Human Brain Atlas (AHBA, https://human.brain-map.org; [H2012N]). Data were processed with the abagen toolbox (version 0.1.3; https://github.com/rmarkello/abagen) using a 148-region surface-based atlas in MNI space.

First, microarray probes were reannotated using data provided by [A2019N]; probes not matched to a valid Entrez ID were discarded. Next, probes were filtered based on their expression intensity relative to background noise [Q2002N], such that probes with intensity less than the background in >=50.00% of samples across donors were discarded , yielding 31,569 probes . When multiple probes indexed the expression of the same gene, we selected and used the probe with the most consistent pattern of regional variation across donors (i.e., differential stability; [H2015N]), calculated with:

$$ \Delta_{{S}}(p) = \frac{{1}}{{\binom{{N}}{{2}}}} \, \sum_{{i=1}}^{{N-1}} \sum_{{j=i+1}}^{{N}} \rho[B_{{i}}(p), B_{{j}}(p)] $$

where $ \rho $ is Spearman's rank correlation of the expression of a single probe, p, across regions in two donors $B_{{i}}$ and $B_{{j}}$, and N is the total number of donors. Here, regions correspond to the structural designations provided in the ontology from the AHBA. 

The MNI coordinates of tissue samples were updated to those generated via non-linear registration using the Advanced Normalization Tools (ANTs; https://github.com/chrisfilo/alleninf). To increase spatial coverage, tissue samples were mirrored bilaterally across the left and right hemispheres [R2018N]. Samples were assigned to brain regions by minimizing the Euclidean distance between the MNI coordinates of each sample and the nearest surface vertex. Samples where the Euclidean distance to the nearest vertex was more than 2 standard deviations above the mean distance for all samples belonging to that donor were excluded. To reduce the potential for misassignment, sample-to-region matching was constrained by hemisphere and gross structural divisions (i.e., cortex, subcortex/brainstem, and cerebellum, such that e.g., a sample in the left cortex could only be assigned to an atlas parcel in the left cortex; [A2019N]). All tissue samples not assigned to a brain region in the provided atlas were discarded. 

Inter-subject variation was addressed by normalizing tissue sample expression values across genes using a robust sigmoid function [F2013J]:

$$ x_{{norm}} = \frac{{1}}{{1 + \exp(-\frac{{(x-\langle x \rangle)}} {{\text{{IQR}}_{{x}}}})}} $$

where $\langle x \rangle$ is the median and $\text{{IQR}}_{{x}}$ is the normalized interquartile range of the expression of a single tissue sample across genes. Normalized expression values were then rescaled to the unit interval: 

$$ x_{{scaled}} = \frac{{x_{{norm}} - \min(x_{{norm}})}} {{\max(x_{{norm}}) - \min(x_{{norm}})}} $$

Gene expression values were then normalized across tissue samples using an identical procedure. Samples assigned to the same brain region were averaged separately for each donor and then across donors, yielding a regional expression matrix with 148 rows, corresponding to brain regions, and 15,633 columns, corresponding to the retained genes .

REFERENCES
----------
[A2019N]: Arnatkevic̆iūtė, A., Fulcher, B. D., & Fornito, A. (2019). A practical guide to linking brain-wide gene expression and neuroimaging data. Neuroimage, 189, 353-367.
[F2013J]: Fulcher, B. D., Little, M. A., & Jones, N. S. (2013). Highly comparative time-series analysis: the empirical structure of time series and their methods. Journal of the Royal Society Interface, 10(83), 20130048.
[H2012N]: Hawrylycz, M. J., Lein, E. S., Guillozet-Bongaarts, A. L., Shen, E. H., Ng, L., Miller, J. A., ... & Jones, A. R. (2012). An anatomically comprehensive atlas of the adult human brain transcriptome. Nature, 489(7416), 391-399.
[H2015N]: Hawrylycz, M., Miller, J. A., Menon, V., Feng, D., Dolbeare, T., Guillozet-Bongaarts, A. L., ... & Lein, E. (2015). Canonical genetic signatures of the adult human brain. Nature Neuroscience, 18(12), 1832.
[Q2002N]: Quackenbush, J. (2002). Microarray data normalization and transformation. Nature Genetics, 32(4), 496-501.
[R2018N]: Romero-Garcia, R., Whitaker, K. J., Váša, F., Seidlitz, J., Shinn, M., Fonagy, P., ... & NSPN Consortium. (2018). Structural covariance networks are coupled to expression of genes enriched in supragranular layers of the human cortex. NeuroImage, 171, 256-267.
