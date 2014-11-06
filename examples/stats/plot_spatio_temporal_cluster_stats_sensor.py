"""
======================================================
Spatio-temporal permutation F-test on full sensor data
======================================================

Tests for differential evoked responses in at least
one condition.
"""

# Authors: Denis Engemann <denis.engemann@gmail.com>
#
# License: BSD (3-clause)

print(__doc__)

import numpy as np

import mne
from mne import io
from mne.stats import spatio_temporal_cluster_test
from mne.datasets import sample

###############################################################################
# Set parameters
data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
event_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw-eve.fif'
event_id = {'Aud_L': 1, 'Aud_R': 2, 'Vis_L': 3, 'Vis_R':4}
tmin = -0.2
tmax = 0.5

#   Setup for reading the raw data
raw = io.Raw(raw_fname, preload=True)
raw.filter(1, 30)
events = mne.read_events(event_fname)

###############################################################################
# Read epochs for the channel of interest

picks = mne.pick_types(raw.info, meg='mag', eog=True)

reject = dict(mag=4e-12, eog=150e-6)
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks,
                     baseline=None, reject=reject, preload=True)

epochs.drop_channels(['EOG 061'])
epochs.equalize_event_counts(event_id, copy=False)

condition_names = 'Aud_L', 'Aud_R', 'Vis_L', 'Vis_R'
X = [epochs[k].get_data() for k in condition_names] # as 3D matrix
X = [np.transpose(x, (0, 2, 1)) for x in X] # transpose for clustering

from mne.channels import read_ch_connectivity

connectivity = read_ch_connectivity('neuromag306mag_neighb.mat')

###############################################################################
# Compute statistic

# set family-wise p-value
p_accept = 0.001
threshold = 50.0 # unrealistic high, but the test is sensitive on this data

cluster_stats = spatio_temporal_cluster_test(X, n_permutations=1000,
                                             threshold=threshold, tail=1,
                                             n_jobs=2,
                                             connectivity=connectivity)

T_obs, clusters, p_values, _ = cluster_stats
good_cluster_inds = np.where(p_values < p_accept)[0]

# get sensor positions via layout
pos = mne.layouts.find_layout(epochs.info).pos


###############################################################################
# Visualize clusters

# load viz libraries
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# configure variables for visualization
times = epochs.times * 1e3
colors = 'r', 'r', 'steelblue', 'steelblue'
linestyles = '-', '--', '-', '--'

# grand average as numpy arrray
grand_ave = np.array(X).mean(1)

for i_clu, clu_idx in enumerate(good_cluster_inds):
    good_clu = np.squeeze(clusters[clu_idx])
    time_inds, space_inds = good_clu

    title = 'Cluster #{0}'.format(i_clu + 1)

    # get unique indices from cluster
    ch_inds = np.unique(space_inds)
    time_inds = np.unique(time_inds)

    # get topography for F stat
    f_map = T_obs[time_inds, ...].mean(0)

    # get signals at significant sensors
    signals = grand_ave[..., ch_inds].mean(-1)
    sig_times = times[time_inds]

    # create spatial mask
    mask = np.zeros((f_map.shape[0], 1), dtype=bool)
    mask[ch_inds, :] = True

    fig, ax_topo = plt.subplots(1, 1, figsize=(20, 5))
    fig.suptitle(title, fontsize=20)

    # plot topo image
    image, _ = mne.viz.plot_topomap(f_map, pos, mask=mask, axis=ax_topo,
                                    cmap='Reds', vmin=np.min, vmax=np.max)

    # advanced matplotlib for showing image with figure and colorbar
    # in one plot
    divider = make_axes_locatable(ax_topo)

    # add axes for colorbar
    ax_colorbar = divider.append_axes('right', size='5%', pad=0.05)
    plt.colorbar(image, cax=ax_colorbar)

    ax_topo.set_xlabel('Averaged F-map ({:0.1f} - {:0.1f} ms)'.format(
        *sig_times[[0, -1]]
    ))

    # add new axis for time courses
    ax_signals = divider.append_axes('right', size='300%', pad=1.2)

    # plot time courses
    for signal, name, col, ls in zip(signals,
                                     condition_names,
                                     colors,
                                     linestyles):
        ax_signals.plot(times, signal, color=col,
                    linestyle=ls, label=name)

    # add information
    ax_signals.axvline(0, color='k', linestyle=':', label='stimulus onset')
    ax_signals.set_xlim(*times[[0, -1]])
    ax_signals.set_xlabel('time [ms]')
    ax_signals.set_ylabel('evoked magnetic fields [fT]')

    ymin, ymax = ax_signals.get_ylim()
    ax_signals.fill_betweenx((ymin, ymax), sig_times[0],
                         sig_times[-1],
                         color='orange', alpha=0.3)
    ax_signals.legend(loc='lower right')
    ax_signals.set_ylim(ymin, ymax)

    # clean up viz
    mne.viz.tight_layout(fig=fig)
    fig.subplots_adjust(bottom=.05)
    plt.show()