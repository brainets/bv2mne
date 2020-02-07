import os.path as op
from bv2mne.config.config import setup_db_coords
# setup_db_coords(op.join('D:\\', 'Databases', 'toy_db'), 'meg_causal', overwrite=True)
# setup_db_coords(op.join('G:\\', 'data'), 'meg_causal', overwrite=True)

from bv2mne.source import create_source_models
from bv2mne.forward import create_forward_models

subjects = ['subject_16']

for sbj in subjects:
    # Pipeline for the estimation of surfaces/volumes sources and labels
    # ------------------------------------------------------------------------------------------------------------------
    surf_src, surf_labels, vol_src, vol_labels = create_source_models(sbj, save=True)
    # ------------------------------------------------------------------------------------------------------------------

    # Pipeline to estimate surfaces/volumes forward models
    # ------------------------------------------------------------------------------------------------------------------
    fwds = create_forward_models(sbj, '3', 'outcome')
    # ------------------------------------------------------------------------------------------------------------------
