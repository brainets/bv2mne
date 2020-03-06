from bv2mne.directories import read_directories
import os.path as op
import numpy as np
import mne
from visbrain.objects import *


# def visualize_objects(subject, brain=True, bem=False, surf_src=False)

def visualize_bem(bem_dir, subject, vis_as='src', color='green', preview=True):
    bem = mne.read_bem_surfaces(op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject)))
    if vis_as == 'src':
        im_bem = SourceObj('bem', bem[0]['rr'], color=color, alpha=1., symbol='diamond', radius_min=3.)
    elif vis_as == 'vol':
        im_bem = BrainObj('vol_bem', vertices=bem[0]['rr'], faces=bem[0]['tris'], normals=bem[0]['nn'],
                              translucent=True)
    if preview == True:
        im_bem.preview(bgcolor='black')

    return im_bem


def visualize_cortical_src(src_dir, subject, hemi='both', color='marsatlas', preview=True):
    src = mne.read_source_spaces(op.join(src_dir.format(subject), '{0}_surf-src.fif'.format(subject)))
    if hemi == 'both':
        rr = np.vstack((src[0]['rr'], src[1]['rr']))
    elif hemi == 'lh':
        rr = src[0]['rr']
    elif hemi == 'rh':
        rr = src[1]['rr']

    if color == 'marsatlas':
        color = set_marsatlas(subject, src, hemi=hemi)

    im_cort_src = SourceObj('cort_src', rr, color=color, symbol='disc', radius_min=15.)

    if preview == True:
        im_cort_src.preview(bgcolor='black')

    return im_cort_src


def visualize_brain(src_dir, subject, hemi='both', translucent=False, preview=True):
    src = mne.read_source_spaces(op.join(src_dir.format(subject), '{0}_surf-src.fif'.format(subject)))
    if hemi == 'both':
        rr = np.vstack((src[0]['rr'], src[1]['rr']))
        tris = np.vstack((src[0]['tris'], src[1]['tris'] + src[0]['rr'].shape[0]))
        nn = np.vstack((src[0]['nn'], src[1]['nn']))
    elif hemi == 'lh':
        rr = src[0]['rr']
        tris = src[0]['tris']
        nn = src[0]['nn']
    elif hemi == 'rh':
        rr = src[1]['rr']
        tris = src[1]['tris']
        nn = src[1]['nn']

    im_brain = BrainObj('brain', vertices=rr, faces=tris, normals=nn, invert_normals=True, translucent=translucent)

    if preview == True:
        im_brain.preview(bgcolor='black')

    return im_brain


def set_marsatlas(subject, src, hemi='both', json_fname='default'):

    if json_fname == 'default':
        read_dir = op.join(op.abspath(__package__), 'config')
        json_fname = op.join(read_dir, 'db_coords.json')

    raw_dir, prep_dir, trans_dir, mri_dir, src_dir, bem_dir, fwd_dir, hga_dir = read_directories(json_fname)

    read_dir = op.abspath(__file__).replace('vis.py', 'textures')
    cortical_text = np.load(op.join(read_dir, 'cortical.npy'))
    subcort_text = np.load(op.join(read_dir, 'subcortical.npy'))

    rgb_marsatlas = []
    for s in src:
        if s['type'] == 'surf':
            textures = cortical_text
            if (hemi == 'both' or hemi == 'lh') and s['id'] == 101:
                labels_lh = mne.read_label(op.join(src_dir.format(subject),
                                                   '{0}_{1}-lab-lh.label'.format(subject, s['type'])))
                all_src = np.full((s['np'], 3), 1.)
                for v, p in zip(labels_lh.vertices, labels_lh.values - 1):
                    all_src[int(v), :] = textures[int(p), :]
                rgb_marsatlas.append(all_src)

            if (hemi == 'both' or hemi == 'rh') and s['id'] == 102:
                labels_rh = mne.read_label(op.join(src_dir.format(subject),
                                                   '{0}_{1}-lab-rh.label'.format(subject, s['type'])))
                all_src = np.full((s['np'], 3), 1.)
                for v, p in zip(labels_rh.vertices, labels_rh.values - 101):
                    all_src[int(v), :] = textures[int(p), :]
                rgb_marsatlas.append(all_src)

        if s['type'] == 'vol':
            textures = subcort_text
            if (hemi == 'both' or hemi == 'lh') and s['seg_name'].endswith('lh'):
                labels_lh = mne.read_label(op.join(src_dir.format(subject),
                                                   '{0}_{1}-lab-lh.label'.format(subject, s['type'])))
                all_src = np.full((labels_lh.pos.shape[0], 3), 1.)
                for v, p in zip(labels_lh.vertices, labels_lh.values - 200):
                    all_src[int(v), :] = textures[int(p), :]
                rgb_marsatlas.append(all_src)

            if (hemi == 'both' or hemi == 'rh') and s['seg_name'].endswith('rh'):
                labels_rh = mne.read_label(op.join(src_dir.format(subject),
                                                   '{0}_{1}-lab-rh.label'.format(subject, s['type'])))
                all_src = np.full((labels_rh.pos.shape[0], 3), 1.)
                for v, p in zip(labels_rh.vertices, labels_rh.values - 208):
                    all_src[int(v), :] = textures[int(p), :]
                rgb_marsatlas.append(all_src)

    rgb_marsatlas = np.vstack(tuple(rgb_marsatlas))
    rgb_marsatlas = list(rgb_marsatlas)

    return rgb_marsatlas

def visualize_objects(subject, bem, sources, brain, color='marsatlas', json_fname='default'):

    if json_fname == 'default':
        read_dir = op.join(op.abspath(__package__), 'config')
        json_fname = op.join(read_dir, 'db_coords.json')

    raw_dir, prep_dir, trans_dir, mri_dir, src_dir, bem_dir, fwd_dir, hga_dir = read_directories(json_fname)

    so = SceneObj()
    im_objects = []
    if bem == True:
        im_bem = visualize_bem(bem_dir, subject, vis_as='src', color='green', preview=False)
        im_objects.append(im_bem)
    if brain == True:
        im_brain = visualize_brain(src_dir, subject, hemi='both', translucent=True, preview=False)
        im_objects.append(im_brain)
    if sources == True:
        im_cort_src = visualize_cortical_src(src_dir, subject, hemi='both', color=color, preview=False)
        im_objects.append(im_cort_src)

    for im in im_objects:
        so.add_to_subplot(im)


    so.preview()
    return so



# src = mne.read_source_spaces('D:\\Databases\\toy_db\\db_mne\\meg_causal\\subject_02\\src\\subject_02_cortical')
# rr = src[0]['rr']
#
# fname_mesh = op.join(db_bv, 'hiphop138-multiscale', 'Decimated', '4K', 'hiphop138_Lwhite_dec_4K_parcels_marsAtlas.gii')
# giftiImage = gifti.giftiio.read(fname_mesh)
# values = giftiImage.darrays[0].data
# parcels, counts = np.unique(values, return_counts=True)
#
# trans = mne.read_trans('D:\\Databases\\toy_db\\db_mne\\meg_causal\\subject_02\\trans\\subject_02-trans.fif')
# trans = trans['trans']
#
# mt = MatrixTransform(trans)
# rr = mt.map(rr*1000)[:, 0:-1]
#
# cmap = np.zeros(rr.shape)
# col = np.vstack((np.linspace(1,0,len(parcels)), np.linspace(0,1,len(parcels)), np.roll(np.linspace(1,0,len(parcels)), 21))).T
# for p in parcels:
#     cmap[values == p] = col[parcels == p]
#
# se = SceneObj(bgcolor='black')
# brain = BrainObj('D:\\Databases\\toy_db\\db_mne\\meg_causal\\subject_02\\surf\\subject_02_Lwhite.gii')
# src = SourceObj('coords', rr, color=cmap)
# se.add_to_subplot(brain)
# se.add_to_subplot(src)
# se.preview()

if __name__ == '__main__':
    # visualize_cortical_src('subject_02', hemi='both', color='marsatlas', preview=True)
    json_fname = ""
    visualize_objects(json_fname, 'subject_18', bem=True, sources=True, brain=True, color='marsatlas')

    # src = visualize_cortical_src('subject_02', hemi='both', color='red', preview=False)
    # src.animate()
    # src.preview()

    # bem = visualize_bem('subject_02', vis_as='src', color='green', preview=False)
    # bem.animate()
    # bem.preview()
