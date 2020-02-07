# Authors: David Meunier <david.meunier@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>

import mne

from bv2mne.directories import *
from bv2mne.bem import check_bem, create_bem

def create_forward_models(subject, session=1, event='', src=None):
    """ Create the forward model

    Parameters:
    ----------
    subject : str
        Name of the subject
    session : int | str
         Number of the session
    event : str
        Name of the event of the epoch file
    src : str | None, default None
        Path of the sources file, if None the 'src.fif' file is automatically searched

    Returns:
    -------
        forward models : list of forward models
    -------
    """

    # File to align coordinate frames meg2mri computed using mne.analyze
    # (computed with interactive gui)
    fname_trans = op.join(trans_dir.format(subject), '{0}-trans.fif'.format(subject))

    # MEG Epoched data to recover position of channels
    fname_event = op.join(prep_dir.format(subject, session), '{0}_{1}-epo.fif'.format(subject, event))
    if event == '' or event == None:
        fname_event.replace('_-', '-')

    # Take info from epochs, and then free some space
    epochs_event = mne.read_epochs(fname_event)
    info = epochs_event.info
    del epochs_event

    # Find and read source space files
    if src is None:
        src = [n for n in os.listdir(src_dir.format(subject)) if n.endswith('src.fif')]
        src = [mne.read_source_spaces(op.join(src_dir.format(subject), n)) for n in src]
    elif src is str:
        if op.isfile(src): src = [mne.read_source_spaces(src)]
    elif src is list:
        if src[0] == str:
            src = [mne.read_source_spaces(n) for n in src]
        if src[0] == mne.source_space.SourceSpaces:
            pass
    elif src is mne.source_space.SourceSpaces: src = [src]
    else: raise Exception('\nSource space dtype not recognized, use str, list of str, list of SourceSpaces, '
                          'or None to automatic research\n')

    # Calculate forward model for each source space
    fwds = []
    for sp in src:

        if sp[0]['type'] == 'surf':
            print('\n---------- Forward Model for cortical sources ----------\n')
            f_fixed = True
            name = 'surf'
        elif sp[0]['type'] == 'vol':
            print('\n---------- Forward Model for cortical sources ----------\n')
            f_fixed = False
            name = 'vol'
        else: raise ValueError('Unknown Source Space type, it should be \'surf\' or \'vol\'')

        fwd = forward_model(subject, info, fname_trans, sp, force_fixed=f_fixed, name=name)
        fwds.append(fwd)

    print('\n---------- Forward Models Completed ----------\n')

    return fwds


def forward_model(subject, info, fname_trans, src, force_fixed=False, name='model'):
    """construct forward model

    Parameters
    ----------
    subject : str
        The name of subject
    raw : instance of rawBTI
        functionnal data
    fname_trans : str
        The filename of transformation matrix
    src : instance of SourceSpaces | list
        Sources of each interest hemisphere
    subjects_dir : str
        The subjects directory
    force_fixed: Boolean
        Force fixed source orientation mode
    name : str
        Use to save output

    Returns
    -------
    fwd : instance of Forward
    -------
    """
    # Files to save
    fname_bem_sol = op.join(bem_dir.format(subject), '{0}-bem-sol.fif'.format(subject))
    fname_fwd = op.join(fwd_dir.format(subject), '{0}-{1}-fwd.fif'.format(subject, name))

    # Making BEM model and BEM solution if it was not done before
    if check_bem(subject):
        pass
    else: create_bem(subject)

    # Compute forward, commonly referred to as the gain or leadfield matrix.
    fwd = mne.make_forward_solution(info=info, trans=fname_trans, src=src, bem=fname_bem_sol, mindist=0.0)

    # Set orientation of cortical sources to surface normals
    if force_fixed:
        # Surface normal
        fwd = mne.forward.convert_forward_solution(fwd, surf_ori=True, force_fixed=True)

    # Save fwd model
    mne.write_forward_solution(fname_fwd, fwd, overwrite=True)

    return fwd


if __name__ == '__main__':
    fwds = create_forward_models('subject_02', '1', 'action')