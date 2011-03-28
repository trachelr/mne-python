# Authors: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#          Scott Burns <sburns@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

from subprocess import Popen


def _n_items(d, key):
    n = 0
    if key in d:
        n = 1
        if isinstance(d[key], list):
            n = len(d[key])
    return n


def process_raw(**kwargs):
    """Python interface to mne_process_raw

    --cd dir                  change the initial working directory.
    --raw name                input file name.
    --grad number             desired software gradient compensation.
    --allowmaxshield          allow unprocessed MaxShield data to be loaded.
    --events name             read event list from here
    --eventsout name          save event list here
    --allevents               save all trigger line transitions instead of just the raising edges.
    --proj name               projection data file name.
    --projon                  apply SSP to the data.
    --projoff                 do not apply SSP to the data.
    --makeproj                create a new projection operator from
                              the data (--proj will be discarded).
    --projevent no            which event to look for in projector creation
                              (default: use raw data in the time range given)
    --projtmin time/s         start time for projection operator calculation
                              (default = use all data).
    --projtmax time/s         end time for projection operator calculation
                              (default = use all data).
    --projngrad value         how many components to use for planar
                              gradiometers (default = 5)
    --projnmag  value         how many components to use for magnetometers
                              / axial gradiometers (default = 8)
    --projgradrej value/fT/cm rejection limit for planar gradiometers in
                              projection calculation (default = 2000.0 fT/cm)
    --projmagrej value/fT     rejection limit magnetometers / axial
                              gradiometers in projection calculation
                              (default = 3000.0 fT)
    --saveprojtag name        use this as a tag for the projection operator
                              output files (--makeproj will be implied).
    --saveprojaug             save the projection augmented with zeros for
                              compatibility with graph.
    --filtersize size         desired filter length (default = 4096)
    --highpass val/Hz         highpass corner (default = 0.0 Hz)
    --lowpass  val/Hz         lowpass  corner (default = 40.0 Hz)
    --highpassw val/Hz        highpass transition width (default = 0.0 Hz)
    --lowpassw val/Hz         lowpass transition width (default = 5.0 Hz)
    --eoghighpass val/Hz      EOG highpass corner (default = 0.0 Hz)
    --eoglowpass  val/Hz      EOG lowpass  corner (default = 40.0 Hz)
    --eoghighpassw val/Hz     EOG highpass transition width (default = 0.0 Hz)
    --eoglowpassw val/Hz      EOG lowpass transition width (default = 5.0 Hz)
    --filteroff               do not filter the data
    --save name               Destination for saving filtered raw data
    --anon                    Omit subject info from the output
    --decim factor            Decimation factor for saving
    --split size/MB           Split the output file chunks of this many
                              megabytes
    --ave name                Definition for averaging
    --saveavetag name         Use this as a tag for the average output files.
    --gave name               Name of the grand average file.
    --cov name                Definition for covariance matrix calculation
    --savecovtag name         Use this as a tag for the covariance matrix
                              output files.
    --gcov name               Name of the grand average covariance matrix file.
    --savehere                Save the files with automatically generated files
                              here instead of the directory of the corresponding
                              raw data
    --digtrig name            digital trigger channel name
    --digtrigmask value       mask to apply to the digital trigger channel
    --help                    print this info.
    --version                 print version info.
    """

    assert 'raw' in kwargs

    cmd = ['mne_process_raw']

    # handle raw, cov and ave
    n_raw = _n_items(kwargs, 'raw')
    if n_raw == 0:
        raise ValueError('You have to specify a raw file as input')
    n_cov = _n_items(kwargs, 'cov')
    n_ave = _n_items(kwargs, 'ave')
    if n_cov > 0:
        assert n_cov == n_raw
    if n_ave > 0:
        assert n_ave == n_raw

    for key, val in kwargs.iteritems():
        # Handle proj on or off
        if key is 'proj':
            if val:
                cmd += ['--projon']
            else:
                cmd += ['--projoff']
            continue

        # Handle filtering on or off
        if key is 'filter' and not val:
            if val:
                cmd += ['--filteroff']
            continue

        if not isinstance(val, list):
            val = [val]
        for v in val:
            if isinstance(v, str):
                # v = '"%s"' % v
                v = '%s' % v
            cmd += ['--%s' % key, '%s' % v]

    print 'Running : %s' % cmd
    return Popen(cmd).wait()


def check_eeg_locations(fname, dig, fix=False):
    """Python interface to mne_check_eeg_locations

    Check and fix EEG location information.

    fname : string
        The file to be checked / modified.

    dig : string
        File containing the Polhemus data.

    fix : bool
        Fix the locations (default is check only).
    """
    cmd = ['mne_check_eeg_locations']

    cmd += ['--file', fname]
    cmd += ['--dig', dig]
    if fix:
        cmd += ['--fix']

    print 'Running : %s' % cmd
    return Popen(cmd).wait()


def mark_bad_channels(fname, bad_fname):
    """Python interface to mne_mark_bad_channels

    Mark some bad channels in FIF file.

    fname : string
        The file to add the bad channels

    bad_fname : string
        File containing the list of bad channels
    """
    cmd = ['mark_bad_channels']

    cmd += ['--file', fname]
    cmd += ['--dig', dig]
    if fix:
        cmd += ['--fix']

    print 'Running : %s' % cmd
    return Popen(cmd).wait()


def filter_raw(raw_in, raw_out, lowpass=None, highpass=None, decim=None,
               proj=False):
    """Filter raw data

    Parameters
    ----------
    raw_in : string
        Name of input raw file
    raw_out : string
        Name of filtered raw file
    lowpass : float
        Low pass in Hz. No lowpass if None
    highpass : float
        High pass in Hz. No highpass if None
    decim : int
        Decimation factor
    proj : bool
        Apply SSP projection or not.
    """
    params = dict(raw=raw_in, save=raw_out)
    if lowpass is not None:
        params['lowpass'] = lowpass
    if highpass is not None:
        params['highpass'] = highpass
    if decim is not None:
        params['decim'] = decim
    if proj is not None:
        params['proj'] = proj
    return process_raw(**params)


if __name__ == '__main__':

    # fname = './fiff/tests/data/test_raw.fif'
    # eve_fname = 'foo-eve.fif'
    #
    # # Reading events
    # process_raw(raw=fname, eventsout=eve_fname)

    from mne.datasets import sample
    data_path = sample.data_path('../examples')

    ###############################################################################
    # Set parameters
    raw_fname = data_path + '/MEG/sample/sample_audvis_raw.fif'

    out = filter_raw(raw_in=raw_fname, raw_out='foobar_raw.fif', lowpass=40,
                proj=False, decim=4)

    # process_raw(raw=raw_fname, lowpass=40,
    #             save='foobar_raw.fif', proj=False, decim=4)

    # pid = process_raw(raw=['foobar raw.fif', 'foobar_raw.fif', 'foobar_raw.fif'],
    #                   ave=['foobar.ave', 'foobar.ave', 'foobar.ave'],
    #                   proj='on', lowpass=20, gave='gave.fif')
    # print pid