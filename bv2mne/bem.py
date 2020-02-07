# Authors: David Meunier <david.meunier@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>

import mne

from bv2mne.directories import *

def create_bem(subject):
    """ Create the BEM model from FreeSurfer files

    Parameters:
    ----------
    subject : str
        Name of the subject to calculate the BEM model

    Returns:
    -------
    surfaces : list of dict
        BEM surfaces
    bem : instance of ConductorModel
        BEM model
    -------
    """

    print('\n---------- Resolving BEM model and BEM soultion ----------\n')

    fname_bem_model = op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject))
    fname_bem_sol = op.join(bem_dir.format(subject), '{0}-bem-sol.fif'.format(subject))

    # Make bem model: single-shell model. Depends on anatomy only.
    bem_model = mne.make_bem_model(subject, ico=None, conductivity=[0.3], subjects_dir=op.join(db_fs, project))
    mne.write_bem_surfaces(fname_bem_model, bem_model)

    # Make bem solution. Depends on anatomy only.
    bem_sol = mne.make_bem_solution(bem_model)
    mne.write_bem_solution(fname_bem_sol, bem_sol)

    return bem_model, bem_sol

def check_bem(subject):
    """ Check if the BEM model exists

    Parameters
    ----------
    subject : str
        The name of the subject to check the BEM model

    Returns:
    -------
    True/False : bool
        True if the BEM model exists for the subject, otherwise False
    -------
    """

    # Check if BEM files exists, return boolean value
    print('\nChecking BEM files\n')
    fname_bem_model = op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject))
    fname_bem_sol = op.join(bem_dir.format(subject), '{0}-bem-sol.fif'.format(subject))

    if op.isfile(fname_bem_model) and op.isfile(fname_bem_sol):
        return True
    else: return False

if __name__ == '__main__':
    create_bem('subject_03')