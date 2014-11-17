"""
=======================================================
Time frequency with Stockwell transform in sensor space
=======================================================

This script shows how to compute induced power using the
Stockwell transform, a.k.a. S-Transform.

"""
# Authors: Denis A. Engemann <denis.engemann@gmail.com>
#          Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#
# License: BSD (3-clause)

import mne
from mne import io
from mne.time_frequency import tfr_stockwell
from mne.datasets import somato

###############################################################################
# Set parameters
data_path = somato.data_path()
raw_fname = data_path + '/MEG/somato/sef_raw_sss.fif'
event_id, tmin, tmax = 1, -1., 3.

# Setup for reading the raw data
raw = io.Raw(raw_fname)
baseline = (None, 0)
events = mne.find_events(raw, stim_channel='STI 014')

# picks MEG gradiometers
picks = mne.pick_types(raw.info, meg='mag', eeg=False, eog=True, stim=False)

epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                    baseline=baseline, reject=dict(mag=5e-12, eog=350e-6),
                    preload=True)

###############################################################################
# Calculate power and intertrial coherence

epochs = epochs.pick_channels(epochs.ch_names[81:83])

power, itc = tfr_stockwell(epochs[:60], fmin=6., fmax=30., decim=3, n_jobs=2,
                           width=1.0, return_itc=True)

power.plot([0], baseline=(-0.5, 0), mode=None)

itc.plot([0], baseline=None, mode=None)