# ----------------------------------------------------------------------------------------------------------------------
#
# This scripts creates the MNE database and associated json file
#
# Authors: Andrea Brovelli <andrea.brovelli@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>
#
# ----------------------------------------------------------------------------------------------------------------------

# Imports
from bv2mne.config.config import setup_db_info
from bv2mne.directories import create_sbj_db_mne

# Jobs
create_json_file = True
create_db_mne = True

# Directories and params of the project
db = '/hpc/bagamore/brainets/data/'
project = 'meg_te'
json_path = db + 'db_mne/' + project
subjects = ['subject_01', 'subject_04', 'subject_05', 'subject_06', 'subject_07', 'subject_09', 'subject_10',
            'subject_11', 'subject_12', 'subject_13']

# Create json file containing databases directories as a json file. One json file per project
if create_json_file:
    json_fname = setup_db_info(db, project, json_path=json_path, overwrite=True)
else:
    json_fname = json_path + '/db_info.json'

# Create MNE database with all directories and adds necessary files from BrainVISA and Freesurfer
if create_db_mne:
    for sbj in subjects:
        create_sbj_db_mne(sbj, json_fname=json_fname)

# Manual intervention: copy and paste adapted referential.txt and MarsAtlas files into /referential and /marsatlas