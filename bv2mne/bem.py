# Authors: David Meunier <david.meunier@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>

import mne

import os.path as op

from bv2mne.directories import read_directories, read_databases

def create_bem(json_fname, subject):

    print('\n---------- Resolving BEM model and BEM soultion ----------\n')


    database, project, db_mne, db_bv, db_fs = read_databases(json_fname)

    raw_dir, prep_dir, trans_dir, mri_dir, src_dir, bem_dir, fwd_dir, hga_dir = read_directories(json_fname)

    fname_bem_model = op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject))
    fname_bem_sol = op.join(bem_dir.format(subject), '{0}-bem-sol.fif'.format(subject))

    # Make bem model: single-shell model. Depends on anatomy only.
    model = mne.make_bem_model(subject, ico=None, conductivity=[0.3], subjects_dir=op.join(db_fs, project))
    mne.write_bem_surfaces(fname_bem_model, model)

    # Make bem solution. Depends on anatomy only.
    bem_sol = mne.make_bem_solution(model)
    mne.write_bem_solution(fname_bem_sol, bem_sol)

    return

def check_bem(json_fname, subject):

    raw_dir, prep_dir, trans_dir, mri_dir, src_dir, bem_dir, fwd_dir, hga_dir = read_directories(json_fname)

    # Check if BEM files exists, return boolean value
    print('\nChecking BEM files\n')
    fname_bem_model = op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject))
    fname_bem_sol = op.join(bem_dir.format(subject), '{0}-bem-sol.fif'.format(subject))

    if op.isfile(fname_bem_model) and op.isfile(fname_bem_sol):
        return True
    else: return False

if __name__ == '__main__':
    create_bem('subject_03')
