"""
======================================
Compute LCMV beamformer on evoked data
======================================

Compute LCMV beamformer solution on evoked dataset
and stores the solution in stc files for visualisation.

"""

# Author: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

print __doc__

import pylab as pl
import mne
from mne.datasets import sample
from mne.fiff import Raw, pick_types
from mne.beamformer import lcmv

data_path = sample.data_path('..')
raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
event_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw-eve.fif'
fname_fwd = data_path + '/MEG/sample/sample_audvis-meg-eeg-oct-6-fwd.fif'
fname_cov = data_path + '/MEG/sample/sample_audvis-cov.fif'

###############################################################################
# Get epochs
event_id, tmin, tmax = 1, -0.2, 0.5

# Setup for reading the raw data
raw = Raw(raw_fname)
events = mne.read_events(event_fname)

# Set up pick list: EEG + MEG - bad channels (modify to your needs)
exclude = raw.info['bads'] + ['MEG 2443', 'EEG 053']  # bads + 2 more
picks = pick_types(raw.info, meg=True, eeg=False, stim=True, eog=True,
                            exclude=exclude)

# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,
                    picks=picks, baseline=(None, 0), preload=True,
                    reject=dict(grad=4000e-13, mag=4e-12, eog=150e-6))

forward = mne.read_forward_solution(fname_fwd)
noise_cov = mne.Covariance(fname_cov)

# Compute whitener from noise covariance matrix
whitener = noise_cov.get_whitener(epochs.info, mag_reg=0.1,
                                  grad_reg=0.1, eeg_reg=0.1, pca=True)
# Compute inverse solution
stc = lcmv(epochs, forward, whitener, orientation='loose',
           snr=3, loose=0.2, weight_exp=0.1)

# Save result in stc files
stc.save('mne_lcmv_inverse')

###############################################################################
# View activation time-series
pl.close('all')
pl.plot(1e3 * stc.times, stc.data[::100, :].T)
pl.xlabel('time (ms)')
pl.ylabel('dSPM value')
pl.show()
