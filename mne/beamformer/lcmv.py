"""Compute Linearly constrained minimum variance (LCMV) beamformer.
"""

# Authors: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

import numpy as np
from scipy import linalg

from ..minimum_norm import minimum_norm


def lcmv(epochs, forward, whitener,
         orientation='fixed', snr=3, loose=0.2, depth=True,
         weight_exp=0.5, weight_limit=10):
    """Linearly Constrained Minimum Variance (LCMV) beamformer.

    Compute LCMV on evoked data starting from
    a forward operator.

    Parameters
    ----------
    evoked : Evoked
        Evoked data to invert
    forward : dict
        Forward operator
    whitener : Whitener
        Whitening matrix derived from noise covariance matrix
    method : 'wmne' | 'dspm' | 'sloreta'
        The method to use
    orientation : 'fixed' | 'free' | 'loose'
        Type of orientation constraints 'fixed'.
    snr : float
        Signal-to noise ratio defined as in MNE (default: 3).
    loose : float in [0, 1]
        Value that weights the source variances of the dipole components
        defining the tangent space of the cortical surfaces.
    depth : bool
        Flag to do depth weighting (default: True).
    weight_exp : float
        Order of the depth weighting. {0=no, 1=full normalization, default=0.8}
    weight_limit : float
        Maximal amount depth weighting (default: 10).
    fmri : array of shape [n_sources]
        Vector of fMRI values are the source points.
    fmri_thresh : float
        fMRI threshold. The source variances of source points with fmri smaller
        than fmri_thresh will be multiplied by fmri_off.
    fmri_off : float
        Weight assigned to non-active source points according to fmri
        and fmri_thresh.

    Returns
    -------
    stc : dict
        Source time courses

    Notes
    -----
    The original reference is:
    Van Veen et al. Localization of brain electrical activity via linearly
    constrained minimum variance spatial filtering.
    Biomedical Engineering (1997) vol. 44 (9) pp. 867--880

    Computation is done using the MNE solver following:
    Mosher et al. Equivalence of linear approaches in bioelectromagnetic
    inverse solutions. Statistical Signal Processing (2003)
    """
    assert orientation in ['fixed', 'free', 'loose']

    fwd_ch_idx = [forward['sol']['row_names'].index(c)
                  for c in epochs.ch_names if c in forward['sol']['row_names']]
    ch_names = [forward['sol']['row_names'][i] for i in fwd_ch_idx]
    data_ch_idx = [epochs.ch_names.index(c) for c in ch_names]
    lead_field = forward['sol']['data'][fwd_ch_idx]

    data = epochs.get_data()
    data = np.swapaxes(data, 0, 1)[data_ch_idx]
    data = data.reshape(data.shape[0], -1)
    data_cov = np.cov(data)

    # Compute sqrt(data_cov) taking into account rank deficiency
    _, s, Vh = linalg.svd(data_cov)
    rank = np.sum(s > 1e-8 * s[0])
    sqrt_data_cov = np.sqrt(s[:rank])[:, None] * Vh[:rank]
    print 'Data rank: %d' % rank
    src_var = 1.0 / np.sum(np.power(np.dot(sqrt_data_cov,
                                           lead_field), 2),
                           axis=0)

    evoked = epochs.average()

    return minimum_norm(evoked, forward, whitener, method='wmne',
             orientation=orientation, snr=snr, loose=loose, depth=depth,
             weight_exp=weight_exp, weight_limit=weight_limit, fmri=src_var,
             fmri_thresh=None, fmri_off=0.1)
