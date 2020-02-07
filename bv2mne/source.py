# Authors: David Meunier <david.meunier@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>

import numpy as np

import mne
from mne import SourceSpaces

from bv2mne.directories import *

from bv2mne.surface import get_surface, get_surface_labels
from bv2mne.volume import get_volume, get_volume_labels
from bv2mne.utils import create_trans
from bv2mne.bem import check_bem, create_bem


def create_source_models(subject, database=database, save=False):
    """
    Create cortical and subcortical source models

    Pipeline for:
        i) importing BrainVISA white meshes for positions
        and MarsAtlas textures for areas
        ii) create transformation file from BV to head coordinates
        iii) create source spaces with cortical
        and subcortical dipoles,

    Parameters
    ----------
    subject : str
        Subject name
    database :
        To delete, database reference for trans file, useless from next version
    save : bool | True
        Allows to save source spaces and respective labels in the default directory

    Returns
    -------
    surf_src : instance of SourceSpace
        Cortical surface source spaces, lh and rh
    surf_labels : instance of Labels
        Cortical surfaces labels
    vol_src : instance of VolSourceSpace
        Subcortical volumes source space, lh and rh
    vol_labels : instance of Labels
        Subcortical volumes Labels
    """

    ###########################################################################
    # -------------------------------------------------------------------------
    # BrainVISA anatomical data
    # -------------------------------------------------------------------------

    # BV decimated white meshes (cortical sources)
    fname_surf_L = op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                           'mesh', 'surface_analysis', '{0}_Lwhite_remeshed_hiphop.gii'.format(subject))

    fname_surf_R = op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                           'mesh', 'surface_analysis', '{0}_Rwhite_remeshed_hiphop.gii'.format(subject))

    # BV texture (MarsAtlas labels) for decimated white meshes
    # (cortical sources)
    fname_tex_L = op.join(db_bv, 'hiphop138-multiscale', 'Decimated', '4K',
                          'hiphop138_Lwhite_dec_4K_parcels_marsAtlas.gii')

    fname_tex_R = op.join(db_bv, 'hiphop138-multiscale', 'Decimated', '4K',
                          'hiphop138_Rwhite_dec_4K_parcels_marsAtlas.gii')

    # Labelling xls file
    fname_atlas = op.join(db_mne, project, 'marsatlas', 'MarsAtlas_BV_2015.xls')

    # Color palette (still used???)
    fname_color = op.join(db_mne, project, 'marsatlas', 'MarsAtlas.ima')

    # MarsAtlas volume parcellation
    fname_vol = op.join(db_bv, project, subject, 't1mri', 'default_acquisition', 'default_analysis', 'segmentation',
                        'mesh', 'surface_analysis', '{0}_parcellation.nii.gz'.format(subject))

    # -------------------------------------------------------------------------
    # Transformation files BV to FS
    # -------------------------------------------------------------------------

    # Referential file list
    # (4 transformation files to transform BV meshes to FS space)
    fname_trans_ref = op.join(db_mne, project, 'referential', 'referential.txt')

    # This file contains the transformations for subject_01
    fname_trans_out = op.join(db_mne, project, subject, 'ref', '{0}-trans.trm'.format(subject))

    name_lobe_vol = ['Subcortical']
    # ---------------------------------------------------------------------
    # Setting up the source space from BrainVISA results
    # ---------------------------------------------------------------------
    # http://martinos.org/mne/stable/manual/cookbook.html#source-localization
    # Create .trm file transformation from BrainVisa to FreeSurfer needed
    # for brain.py function for surface only
    create_trans(subject, database, fname_trans_ref, fname_trans_out)

    # Calculate cortical sources and MarsAtlas labels
    print('\n---------- Cortical sources ----------\n')
    surf_src, surf_labels = get_brain_surf_sources(subject, fname_surf_L, fname_surf_R, fname_tex_L, fname_tex_R, None,
                                                  fname_trans_out, fname_atlas, fname_color)

    if save == True:
        print('\nSaving surface source space and labels.....')
        mne.write_source_spaces(op.join(src_dir.format(subject), '{0}_surf-src.fif'.format(subject)), surf_src, overwrite=True)
        for sl in surf_labels:
            mne.write_label(op.join(src_dir.format(subject), '{0}_surf-lab'.format(subject)), sl)
        print('[done]')

    # Create BEM model if needed
    print('\nBEM model is needed for volume source space\n')
    if check_bem(subject):
        pass
    else: create_bem(subject)

    print('\n---------- Subcortical sources ----------\n')

    vol_src, vol_labels = get_brain_vol_sources(subject, fname_vol, name_lobe_vol, fname_trans_out, fname_atlas, space=5.)

    if save == True:
        print('Saving volume source space and labels.....')
        mne.write_source_spaces(op.join(src_dir.format(subject), '{0}_vol-src.fif'.format(subject)), vol_src, overwrite=True)
        for vl in vol_labels:
            mne.write_label(op.join(src_dir.format(subject), '{0}_vol-lab'.format(subject)), vl)
        print('[done]')
    #
    print('\n---------- Sources Completed ----------\n')

    return surf_src, surf_labels, vol_src, vol_labels


def get_brain_surf_sources(subject, fname_surf_L=None, fname_surf_R=None,
                           fname_tex_L=None, fname_tex_R=None, bad_areas=None,
                           trans=False, fname_atlas=None, fname_color=None):
    """compute surface sources
    Parameters
    ----------
    subject : str
        The name of the subject
    fname_surf_L : None | str
        The filename of the surface of the left hemisphere
    fname_surf_R : None | str
        The filename of the surface of the right hemisphere
    fname_tex_L : None | str
        The filename of the texture surface of the right hemisphere
        The texture is used to select areas in the surface
    fname_tex_R : None | str
        The filename of the texture surface of the left hemisphere
    bad_areas : list of int
        Areas that will be excluded from selection
    trans : str | None
        The filename that contains transformation matrix for surface
    fname_atlas : str | None
        The filename of the area atlas
    fname_color : Brain surfer instance
        The filename of color atlas
    Returns
    -------
    figure : Figure object
    -------
    """

    list_hemi = ['lh', 'rh']

    fname_surf = [fname_surf_L, fname_surf_R]
    fname_tex = [fname_tex_L, fname_tex_R]

    print('\nBuilding surface areas.....')

    # Get surfaces
    surfaces = []
    surf_labels = []
    for hemi_surf, hemi_tex, hemi in zip(fname_surf, fname_tex, list_hemi):

        if hemi_surf is not None and hemi_tex is not None:

            # Create surface areas
            surface = get_surface(hemi_surf, subject=subject, hemi=hemi, trans=trans)
            labels_hemi = get_surface_labels(surface, texture=hemi_tex, hemi=hemi, subject=subject,
                                             fname_atlas=fname_atlas, fname_color=fname_color)

            # Delete WM (values of texture 0 and 42)
            bad_areas = [0, 42]
            if bad_areas is not None:
                # bad =
                labels_hemi = list(np.delete(labels_hemi, bad_areas, axis=0))


            # MNE accepts hemispheric labels as a single object that keeps the sum of all single labels
            labels_sum = []
            for l in labels_hemi:
                if type(labels_sum) == list:
                    labels_sum = l
                else:
                    labels_sum += l

            surfaces.append(surface)
            surf_labels.append(labels_sum)

    print('\nSet sources on MarsAtlas cortical areas')
    surf_src = SourceSpaces(surfaces)

    print('[done]')
    return surf_src, surf_labels


def get_brain_vol_sources(subject, fname_vol=None, name_lobe_vol='Subcortical',
                          trans=False, fname_atlas=None, space=5):
    """compute volume sources
    Parameters
    ----------
    subject : str
        The name of the subject
    fname_vol : None | str
        The filename of mri labelized
    name_lobe_vol : None | list of str | str
        Interest lobe names
    trans : str | None
        The filename that contains transformation matrix for surface
    fname_atlas : str | None
        The filename of the area atlas
    Returns
    -------
    figure : Figure object
    -------
    """

    print('build volume areas')

    assert fname_vol is not None, "error , missing volume file"

    vol_src = get_volume(subject, pos=5.0)
    vol_labels = get_volume_labels(vol_src)

    labels_sum = []
    for l in vol_labels:
        if type(labels_sum) == list:
            labels_sum = l
        else:
            labels_sum += l
    vol_labels = [labels_sum.lh, labels_sum.rh]

    print('[done]')

    return vol_src, vol_labels
