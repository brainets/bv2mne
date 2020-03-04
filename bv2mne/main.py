import os.path as op
# from bv2mne.config.config import setup_db_coords
# setup_db_coords('/hpc/bagamore/brainets/data/', 'meg_causal', overwrite=True)

from bv2mne.source import create_source_models
from bv2mne.forward import create_forward_models

subjects = ['subject_01', 'subject_02', 'subject_03', 'subject_04', 'subject_05', 'subject_06', 'subject_07',
            'subject_08', 'subject_09', 'subject_10', 'subject_11', 'subject_13', 'subject_14', 'subject_15',
            'subject_16', 'subject_17', 'subject_18']

for sbj in subjects:
    # Pipeline for the estimation of surfaces/volumes sources and labels
    # ------------------------------------------------------------------------------------------------------------------
    surf_src, surf_labels, vol_src, vol_labels = create_source_models(sbj, save=True)
    # ------------------------------------------------------------------------------------------------------------------

    # Pipeline to estimate surfaces/volumes forward models
    # ------------------------------------------------------------------------------------------------------------------
    fwds = create_forward_models(sbj, '1', 'outcome')
    # ------------------------------------------------------------------------------------------------------------------
