# ----------------------------------------------------------------------------------------------------------------------
#
# This scripts creates source model from BrainVISA and Freesurfer results
# and forward models integrating epochs MEG data
#
# Authors: Andrea Brovelli <andrea.brovelli@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>
#
# ----------------------------------------------------------------------------------------------------------------------

# Imports
from bv2mne.source import create_source_models
from bv2mne.forward import create_forward_models

# Jobs

create_source_model = False
create_fwd_model = True

# Directories and params of the project
db = '/hpc/bagamore/brainets/data/'
project = 'meg_te'
json_path = db + 'db_mne/' + project
json_fname = json_path + '/db_info.json'
subjects = ['subject_01', 'subject_04', 'subject_05', 'subject_06', 'subject_07', 'subject_09', 'subject_10',
            'subject_11', 'subject_12', 'subject_13']
sessions = ['1', '2', '3', '4', '5', '6']
event = 'stim'

# Create surfaces/volumes sources and label
if create_source_model:
    for sbj in subjects:
        create_source_models(sbj, save=True, json_fname=json_fname)

# Create forwad models
if create_fwd_model:
    for sbj in subjects:
        for ses in sessions:
            # Pipeline to estimate surfaces/volumes forward models
            create_forward_models(sbj, ses, event, json_fname=json_fname)
