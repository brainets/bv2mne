# Authors: David Meunier <david.meunier@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>

import mne

from bv2mne.directories import *

def create_bem(subject):

    print('\n---------- Resolving BEM model and BEM soultion ----------\n')

    fname_bem_model = op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject))
    fname_bem_sol = op.join(bem_dir.format(subject), '{0}-bem-sol.fif'.format(subject))

    # Make bem model: single-shell model. Depends on anatomy only.
    model = mne.make_bem_model(subject, ico=None, conductivity=[0.3], subjects_dir=op.join(db_mne, project))
    mne.write_bem_surfaces(fname_bem_model, model)

    # Make bem solution. Depends on anatomy only.
    bem_sol = mne.make_bem_solution(model)
    mne.write_bem_solution(fname_bem_sol, bem_sol)

    return

def check_bem(subject):

    # Check if BEM files exists, return boolean value
    print('\nChecking BEM files\n')
    fname_bem_model = op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject))
    fname_bem_sol = op.join(bem_dir.format(subject), '{0}-bem-sol.fif'.format(subject))

    if op.isfile(fname_bem_model) and op.isfile(fname_bem_sol):
        return True
    else: return False
