import os
import os.path as op
import shutil
from bv2mne.config.config import read_db_coords

# Defining database coordinates

def read_databases(json_fname):
    database, project = read_db_coords(json_fname)

    ## Coordinates for raw files
    #db_raw = op.join('/', 'envau', 'work', 'bagamore', 'brovelli.a', 'Data', 'Neurophy', 'MEG_CausaL')
    #fname_bti = 'c,rfDC'
    #fname_config = 'config'
    #fname_hs = 'hs_file'

    # Coordinates for database
    db_mne = op.join(database, 'db_mne')
    db_bv = op.join(database, 'db_brainvisa')
    db_fs = op.join(database, 'db_freesurfer')

    return database, project, db_mne, db_bv, db_fs

def read_directories(json_fname):

    database, project, db_mne, db_bv, db_fs = read_databases(json_fname)

    # mne database subdirectories
    raw_dir = op.join(db_mne, project, '{0}', 'raw', '{1}')
    prep_dir = op.join(db_mne, project, '{0}', 'prep', '{1}')
    trans_dir = op.join(db_mne, project, '{0}', 'trans')
    mri_dir = op.join(db_mne, project, '{0}', 'mri')
    src_dir = op.join(db_mne, project, '{0}', 'src')
    bem_dir = op.join(db_mne, project, '{0}', 'bem')
    fwd_dir = op.join(db_mne, project, '{0}', 'fwd')
    hga_dir = op.join(db_mne, project, '{0}', 'hga', '{1}')

    return raw_dir, prep_dir, trans_dir, mri_dir, src_dir, bem_dir, fwd_dir, hga_dir

def create_sbj_db_mne(json_fname, subject):

    database, project, db_mne, db_bv, db_fs = read_databases(json_fname)

    # Create MNE database
    if not op.exists(db_mne):
        os.mkdir(db_mne)

    # Create project specific database in MNE
    if not op.exists(op.join(db_mne, project)):
        os.mkdir(op.join(db_mne, project))

    # Create folders for labels and referentials
    if not op.exists(op.join(db_mne, project, 'label')):
        os.mkdir(op.join(db_mne, project, 'label'))
    # if not op.exists(op.join(db_mne, project, 'marsatlas')):
    #     os.mkdir(op.join(db_mne, project, 'marsatlas'))
    if not op.exists(op.join(db_mne, project, 'referential')):
        os.mkdir(op.join(db_mne, project, 'referential'))

    # Create subject folder and sub-folders tree
    if not op.exists(op.join(db_mne, project, subject)):
        os.mkdir(op.join(db_mne, project, subject))

    if not op.exists(op.join(db_mne, project, subject, 'bem')):
        os.mkdir(op.join(db_mne, project, subject, 'bem'))
    if not op.exists(op.join(db_mne, project, subject, 'fwd')):
        os.mkdir(op.join(db_mne, project, subject, 'fwd'))
    if not op.exists(op.join(db_mne, project, subject, 'hga')):
        os.mkdir(op.join(db_mne, project, subject, 'hga'))
    if not op.exists(op.join(db_mne, project, subject, 'mri')):
        os.mkdir(op.join(db_mne, project, subject, 'mri'))
    if not op.exists(op.join(db_mne, project, subject, 'prep')):
        os.mkdir(op.join(db_mne, project, subject, 'prep'))
    if not op.exists(op.join(db_mne, project, subject, 'raw')):
        os.mkdir(op.join(db_mne, project, subject, 'raw'))
    if not op.exists(op.join(db_mne, project, subject, 'ref')):
        os.mkdir(op.join(db_mne, project, subject, 'ref'))
    if not op.exists(op.join(db_mne, project, subject, 'src')):
        os.mkdir(op.join(db_mne, project, subject, 'src'))
    if not op.exists(op.join(db_mne, project, subject, 'surf')):
        os.mkdir(op.join(db_mne, project, subject, 'surf'))
    if not op.exists(op.join(db_mne, project, subject, 'tex')):
        os.mkdir(op.join(db_mne, project, subject, 'tex'))
    if not op.exists(op.join(db_mne, project, subject, 'trans')):
        os.mkdir(op.join(db_mne, project, subject, 'trans'))
    if not op.exists(op.join(db_mne, project, subject, 'vol')):
        os.mkdir(op.join(db_mne, project, subject, 'vol'))

    # Copy FreeSurfer MRI
    shutil.copy2(op.join(db_fs, project, subject, 'mri', 'T1.mgz'),
                 op.join(db_mne, project, subject, 'mri', 'T1.mgz'))
    shutil.copy2(op.join(db_fs, project, subject, 'mri', 'aseg.mgz'),
                 op.join(db_mne, project, subject, 'mri', 'aseg.mgz'))

    # Copy FreeSurfer BEM
    bem_files = os.listdir(op.join(db_fs, project, subject, 'bem'))
    for bf in bem_files:
        shutil.copy2(op.join(db_fs, project, subject, 'bem', bf),
                     op.join(db_mne, project, subject, 'bem'))

    # Copy BrainVISA cortical meshes
    shutil.copy2(op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                         'mesh', '{0}_Lwhite.gii'.format(subject)),
                 op.join(db_mne, project, subject, 'surf'))
    shutil.copy2(op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                         'mesh', '{0}_Rwhite.gii'.format(subject)),
                 op.join(db_mne, project, subject, 'surf'))

    # Copy FreeSurfer cortical meshes
    shutil.copy2(op.join(db_fs, project, subject, 'surf', 'lh.white'),
                 op.join(db_mne, project, subject, 'surf', 'lh.white'))
    shutil.copy2(op.join(db_fs, project, subject, 'surf', 'rh.white'),
                 op.join(db_mne, project, subject, 'surf', 'rh.white'))
    shutil.copy2(op.join(db_fs, project, subject, 'surf', 'lh.white.gii'),
                 op.join(db_mne, project, subject, 'surf', 'lh.white.gii'))
    shutil.copy2(op.join(db_fs, project, subject, 'surf', 'rh.white.gii'),
                 op.join(db_mne, project, subject, 'surf', 'rh.white.gii'))

    # Copy BrainVISA textures
    shutil.copy2(op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                         'mesh', 'surface_analysis', '{0}_Lwhite_parcels_marsAtlas.gii'.format(subject)),
                 op.join(db_mne, project, subject, 'tex'))
    shutil.copy2(op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                         'mesh', 'surface_analysis', '{0}_Rwhite_parcels_marsAtlas.gii'.format(subject)),
                 op.join(db_mne, project, subject, 'tex'))

    # Copy BrainVISA complete parcellation volume
    shutil.copy2(op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                         'mesh', 'surface_analysis', '{0}_parcellation.nii.gz'.format(subject)),
                 op.join(db_mne, project, subject, 'vol'))
