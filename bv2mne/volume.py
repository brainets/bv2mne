# Authors: David Meunier <david.meunier@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>

from bv2mne.directories import *

import numpy as np

import mne

aseg_labels = ['Left-Accumbens-area',
               'Left-Amygdala',
               'Left-Caudate',
               'Left-Hippocampus',
               'Left-Pallidum',
               'Left-Putamen',
               'Left-Thalamus-Proper',
               # 'Left-Cerebellum-Cortex',
               # 'Brain-Stem',
               'Right-Accumbens-area',
               'Right-Amygdala',
               'Right-Caudate',
               'Right-Hippocampus',
               'Right-Pallidum',
               'Right-Putamen',
               'Right-Thalamus-Proper']
               # 'Right-Cerebellum-Cortex']

marsatlas_labels = ['NAc_lh',
                    'Amyg_lh',
                    'Cd_lh',
                    'Hipp_lh',
                    'GP_lh',
                    'Put_lh',
                    'Thal_lh',
                    # 'Crb_lh',
                    # 'BStem',
                    'NAc_rh',
                    'Amyg_rh',
                    'Cd_rh',
                    'Hipp_rh',
                    'GP_rh',
                    'Put_rh',
                    'Thal_rh']
                    # 'Crb_rh']


# def get_volume(mri, fname_atlas, lobe_name, subject, hemi, space=5, reduce_volume=True):
#     """get volumes
#
#         Parameters
#         ----------
#         mri : None | str
#             The filename of mri labelized
#         fname_atlas : str | None
#             The filename of the area atlas
#         lobe_name : float | None
#             Interest lobe names
#         subject : str
#             The name of the subject
#         hemi : str
#             The name of hemi  of interest
#         reduce_volume : bool
#             If True, get just the volume including
#             the strucure of interest
#
#         Returns
#         -------
#         vol : instance of Volume
#         -------
#         Author : Alexandre Fabre / modif David Meunier
#         """
#     # Load the volume
#     img = nib.load(mri)
#
#     # Get 3D matrix
#     voxels = img.get_data()
#     affine = img.get_affine()
#     header = img.get_header()
#
#     # Get voxel dimension
#     pix_dim = header['pixdim'][2:5]
#     n_sag, n_axi, n_cor = voxels.shape
#
#     # hack to get a correct translation
#     # affine[:3, -1] = [n_sag // 2, -n_axi // 2, n_cor // 2]
#
#     volumes = []
#
#     if isinstance(lobe_name, str):
#         lobe_name = [lobe_name]
#
#     info = read_texture_info(fname_atlas, hemi)
#
#     label = []
#
#     for name in lobe_name:
#
#         # get dictionary
#         val = np.where(np.array(list(info.values()))[:, -1] == name)
#         lab = np.take(list(info.keys()), val)[0].tolist()
#         label += lab
#
#     # reverse arrays
#     all_points = list(zip(*np.where(voxels >= 0)))
#     # get structure positions
#     all_pos = nib.affines.apply_affine(affine, all_points)
#     rr = all_pos * 1e-3
#
#     for lab in label:
#
#         # reverse arrays
#         point_pos = list(zip(*np.where(voxels == lab)))
#
#         if point_pos:
#             # get structure positions
#             pos = nib.affines.apply_affine(affine, point_pos)
#
#             remains, removes = get_number_volume_sources(pos, space=space)
#
#             if remains == 0:
#                 raise ValueError('Error, 0 source created')
#
#             with warnings.catch_warnings():
#                 warnings.simplefilter("ignore")
#                 # create clusters
#                 km = MiniBatchKMeans(n_clusters=remains)
#
#             # get cluster labels
#             cluster_id = km.fit(pos).labels_
#
#             # (DM) new function, replacing the Pycluster one (see in utils.py)
#             centroids = compute_mean_centroids(pos, cluster_labels=cluster_id)
#
#             dist = euclidean_distances(centroids, all_pos)
#
#             # get indices of closest points of centroids
#             arg_min = np.argmin(dist, axis=1)
#
#             inuse = np.zeros(len(rr))
#             inuse[arg_min] = 1
#             inuse = inuse.astype(int)  # Need to be int
#         #
#         #     vox = np.where(voxels == lab, lab, 0)
#         #
#         #     if reduce_volume:
#         #         x, y, z = np.nonzero(vox)
#         #         vox = vox[x.min():x.max() + 1,
#         #                   y.min():y.max() + 1,
#         #                   z.min():z.max() + 1]
#
#         name, lobe = info[lab]
#         normals = np.zeros((len(pos), 3))
#         # vol = {"pos": pos, "voxels": voxels, "lab": lab, "name": name,
#         #        "lobe": lobe, "subject": subject, "pix_dim": pix_dim,
#         #        "hemi": hemi, "normals": normals}
#
#         if hemi == 'lh':
#             Id = 101
#         elif hemi == 'rh':
#             Id = 102
#
#         vol = {'rr': rr, 'coord_frame': np.array((FIFF.FIFFV_COORD_MRI), np.int32),
#                'type': 'vol', 'id': Id, 'np': len(rr), 'subject_his_id': subject,
#                'nn': normals, 'inuse': inuse, 'nuse': remains, 'seg_name': name,
#                'mri_width': n_sag, 'mri_height': n_axi, 'mri_depth': n_cor,
#                'dist': None, 'nearest': None, 'use_tris': None, 'nuse_tris': 0,
#                'vertno': arg_min, 'patch_inds': None, 'tris': None,
#                'dist_limit': None, 'pinfo': None, 'ntri': 0, 'nearest_dist': None,
#                'removes': removes}
#         # vol = mne.surface.complete_surface_info(vol)
#
#
#         volumes.append(vol)
#
#     # volumes = mne.SourceSpaces(volumes)
#     return volumes


# def get_number_volume_sources(volume, space=5,):
#     """get number sources in region (volume only)
#
#     Parameters
#     ----------
#     obj : Surface object | Volume object
#         The region where sources is computing
#     space : float
#         The distance between sources
#     Returns
#     -------
#     sol : int
#         Number of sources
#     diff :
#         Number points that are not sources
#     -------
#     Author : Alexandre Fabre / modif David Meunier
#     """
#
#     if space < 0:
#         raise ValueError('the space number must be positive')
#
#     # the number of selected vertices mustn't exceed the number of vertices
#     _max = len(volume)
#     print(_max)
#
#     # compute on the volume:
#     # we divide the volume by a sphere volume to know the number of sources
#     space = float(4 / 3 * pi * ((space / 2) ** 3))
#     sol = _max
#
#     # avoid division by zero
#     sol = int(sol / (max(space, 1e-5)))
#     sol = int(min(_max, sol))
#
#     # number of points that have not been selected
#     diff = _max - sol
#
#     return sol, diff
#
#
def get_volume_labels(volume):
    labels = []
    for val, vol in enumerate(volume):
        vertices = np.sort(vol['vertno'])

        pos = vol['rr'][vertices]

        values = np.full(len(vertices), 200 + val)

        if vol['seg_name'].endswith('lh'):
            hemi = 'lh'
        elif vol['seg_name'].endswith('rh'):
            hemi = 'rh'
        lab = mne.Label(vertices=vertices, pos=pos, values=values, hemi=hemi,
                        comment=vol['seg_name'], name=vol['seg_name'], filename=None,
                        subject=vol['subject_his_id'], verbose=None)
        labels.append(lab)

    return labels


def get_volume(subject, pos=5.0):

    fname_bem_model = op.join(bem_dir.format(subject), '{0}-bem-model.fif'.format(subject))

    fname_aseg = op.join(mri_dir.format(subject), 'aseg.mgz')

    vol_src_space = []
    for al, ml in zip(aseg_labels, marsatlas_labels):
        vol_label = mne.setup_volume_source_space(subject,
                                                  mri=fname_aseg,
                                                  pos=pos,
                                                  bem=fname_bem_model,
                                                  volume_label=al,
                                                  subjects_dir=op.join(db_mne, project))

        vol_label[0]['seg_name'] = ml

        if type(vol_src_space) == list:
            vol_src_space = vol_label
        else: vol_src_space += vol_label

    return vol_src_space
