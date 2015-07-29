.. title:: Home

.. raw:: html

    <div class="container"><div class="row">
    <div class="col-md-8"><div style="float: center">
    <a href="index.html"><img src="_static/mne_logo.png"" border="0" alt="MNE"/></a>
    </div></div>
    <div class="col-md-4"><div style="float: left">
    <a href="index.html"><img src="_static/institutions.png"" border="0" alt="Institutions"/></a>
    </div></div>
    </div></div>

.. raw:: html

   <div class="container-fluid">
   <div class="row">
   <div class="col-md-8">
   <br>

MNE is a community-driven software package designed for for **processing
electroencephalography (EEG) and magnetoencephalography (MEG) data**
providing comprehensive tools and workflows for:

1. Preprocessing
2. Source estimation
3. Time–frequency analysis
4. Statistical testing
5. Estimation of functional connectivity
6. Applying machine learning algorithms
7. Visualization of sensor- and source-space data

MNE includes a comprehensive Python package (provided under the simplified
BSD license), supplemented by tools compiled from C code for the LINUX and
Mac OSX operating systems, as well as a MATLAB toolbox.

**From raw data to source estimates in about 30 lines of code:**

.. code:: python

    >>> import mne
    >>> raw = mne.io.Raw('raw.fif', preload=True)  # load data
    >>> raw.info['bads'] = ['MEG 2443', 'EEG 053']  # mark bad channels
    >>> raw.filter(l_freq=None, h_freq=40.0)  # low-pass filter data
    >>> # Extract epochs and save them:
    >>> picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=True,
    >>>                        exclude='bads')
    >>> events = mne.find_events(raw)
    >>> reject = dict(grad=4000e-13, mag=4e-12, eog=150e-6)
    >>> epochs = mne.Epochs(raw, events, event_id=1, tmin=-0.2, tmax=0.5,
    >>>                     proj=True, picks=picks, baseline=(None, 0),
    >>>                     preload=True, reject=reject)
    >>> # Compute evoked response and noise covariance
    >>> evoked = epochs.average()
    >>> cov = mne.compute_covariance(epochs, tmax=0)
    >>> evoked.plot()  # plot evoked
    >>> # Compute inverse operator:
    >>> fwd_fname = 'sample_audvis−meg−eeg−oct−6−fwd.fif'
    >>> fwd = mne.read_forward_solution(fwd fname, surf ori=True)
    >>> inv = mne.minimum_norm.make_inverse_operator(raw.info, fwd,
    >>>                                              cov, loose=0.2)
    >>> # Compute inverse solution:
    >>> stc = mne.minimum_norm.apply_inverse(evoked, inv, lambda2=1./9.,
    >>>                                      method='dSPM')
    >>> # Morph it to average brain for group study and plot it
    >>> stc_avg = mne.morph_data('sample', 'fsaverage', stc, 5, smooth=5)
    >>> stc_avg.plot()

The MNE development is supported by National Institute of Biomedical Imaging and Bioengineering 
grants 5R01EB009048 and P41EB015896 (Center for Functional Neuroimaging Technologies) as well as 
NSF awards 0958669 and 1042134. It has been supported by the
NCRR *Center for Functional Neuroimaging Technologies* P41RR14075-06, the
NIH grants 1R01EB009048-01, R01 EB006385-A101, 1R01 HD40712-A1, 1R01
NS44319-01, and 2R01 NS37462-05, ell as by Department of Energy
under Award Number DE-FG02-99ER62764 to The MIND Institute.

.. raw:: html

   <div style="width: 40%; float: left; padding: 20px;">
       <script type="text/javascript" src="http://www.ohloh.net/p/586838/widgets/project_basic_stats.js"></script>
   </div>


.. raw:: html

   </div>
   <div class="col-md-4">
   <h2>Documentation</h2>

.. toctree::
   :maxdepth: 1

   getting_started
   whats_new
   cite
   references
   tutorials
   auto_examples/index
   manual/index
   python_reference
   generated/commands
   faq
   advanced_setup
   mne_cpp

.. raw:: html

   <h2>Community</h2>

* | Analysis talk: join the
  | `MNE mailing list <http://mail.nmr.mgh.harvard.edu/mailman/listinfo/mne_analysis>`_

* | Feature requests and bug reports:
  | `GitHub issues <https://github.com/mne-tools/mne-python/issues/>`_

* | Chat with developers:
  | `Gitter <https://gitter.im/mne-tools/mne-python>`_

* :ref:`Contribute to MNE! <contributing>`

.. raw:: html

   <h2>Versions</h2>

   <ul>
      <li><a href=http://martinos.org/mne/stable>Stable</a></li>
      <li><a href=http://martinos.org/mne/dev>Development</a></li>
   </ul>

   <div style="float: left; padding: 10px; width: 100%;">
       <a class="twitter-timeline" href="https://twitter.com/mne_python" data-widget-id="317730454184804352">Tweets by @mne_python</a>
   </div>

   </div>
   </div>
   </div>
