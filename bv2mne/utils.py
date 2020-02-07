# Authors: David Meunier <david.meunier@univ-amu.fr>
#          Ruggero Basanisi <ruggero.basanisi@gmail.com>

import mne
import numpy as np
from numpy.linalg import inv

from nibabel.affines import apply_affine

from mne.transforms import write_trans, read_trans
from vispy.visuals.transforms import MatrixTransform

from bv2mne.directories import *


def create_trans(subject, database, fname, fname_out):
    """
       Get transformations of the surface from a file that containes filename
       matrix transformations
    """
    trans_list = []

    print(fname)

    with open(fname, 'r') as textfile:
        trans_name = textfile.read().strip().split("\n")
        print(trans_name)

        for name in trans_name:
            split = name.split()
            inv_bool = ('inv' == split[0])
            if inv_bool:
                name = split[1]
            else:
                name = split[0]

            print(name)
            format_name = name.format(subject)
            print(format_name)

            if not os.path.exists(format_name):
                print("error, {} is not an existing path, will try to add \
                      subject_dir {}".format(format_name, database))

                format_name = os.path.join(database, format_name)
                print(format_name)
                assert os.path.exists(format_name), "Breaking, even when add \
                    subject_dir, file {} do not exists".format(name)

            with open(format_name, 'r') as matfile:
                lines = matfile.read().strip().split("\n")
                lines_list = [l.split() for l in lines]
                translation = lines_list.pop(0)

                # transpose the rotations
                transpose = list(zip(*lines_list))

                # append translations
                transpose.append(translation)

                # create the matrix
                mat_str = np.array(list(zip(*transpose)))
                mat = mat_str.astype(np.float)
                mat = np.vstack([mat, [0, 0, 0, 1]])

                if inv_bool:
                    mat = inv(mat)

                # add line por computing translation
                trans_list.append(mat)

        trans = None
        for trans_cour in trans_list:
            if trans is None:
                trans = trans_cour
            else:
                trans = np.dot(trans, trans_cour)

    if fname_out.endswith('fif'):
        write_trans(fname_out, trans)

    else:
        with open(fname_out, 'w') as matfile:
            # un autre nom semblerait judiceiux pour eviter la confuction
            # avec le matfile de la partie precedente de la fonction
            for i in range(len(trans)):
                for j in range(len(trans[i])):
                    matfile.write(str(trans[i][j])+' ')
                matfile.write('\n')

    return trans


def compute_trans(pos, trans):
    pos = pos.copy()
    if isinstance(trans, str):
        if trans.endswith('fif'):
            trans = read_trans(trans)['trans']
        else:
            with open(trans, 'r') as matfile:
                lines = matfile.read().strip().split("\n")
                trans = [l.split() for l in lines]
                trans = np.array(trans).astype(np.float)

    pos = apply_affine(trans, pos)
    return pos


def tranform(pos, trans):
    pos = pos.copy()
    if isinstance(trans, str):
        if trans.endswith('fif'):
            trans = mne.read_trans(trans)
            trans = trans['trans']
        else:
            with open(trans, 'r') as matfile:
                lines = matfile.read().strip().split("\n")
                trans = [l.split() for l in lines]
                trans = np.array(trans).astype(np.float)

    mt = MatrixTransform(trans)
    pos = mt.map(pos)[:, 0:-1]
    return pos


def read_texture_info(filename, hemi):
    """
        Read file with informations for each parcels
        (DM): fonction un peu bizarre,
        pandas serait plus adapté, mais on veut eviter la dependandace
    """
    info_dict = {}
    if filename is not None:
        list_hemi = ['lh', 'rh']
        if hemi not in list_hemi:
            raise ValueError('hemi must be lh or rh')

        fileformat = filename.split('.')[-1]

        def search_xlsx(header, hemi):
            try:
                index_roi = header.index('Index ' + hemi)
                label = header.index('Label')
                lobe = header.index('Lobe / Région')
                name = header.index('Full name')
                broadman = header.index('Brodman Area')
            except ValueError:
                raise (
                    'header Label, Hemisphere, Lobe, Name, must be label file')
            return index_roi, label, name, lobe, broadman

        def search_xls(header):
            try:
                label = header.index('Label')
                hemi = header.index('Hemisphere')
                lobe = header.index('Lobe')
                name = header.index('Name')
            except ValueError:
                raise (
                    'header Label, Hemisphere, Lobe, Name, must be label file')
            return label, hemi, name, lobe

        # previous version (still used now)
        if fileformat == 'xls':
            import xlrd
            wb = xlrd.open_workbook(filename)
            sh = wb.sheet_by_index(0)
            header = sh.row_values(0)
            index = search_xls(header)
            info = [sh.col_values(ind)[1:] for ind in index]

            # reverse
            info = list(zip(*info))
            hemi_exclude = list_hemi[list_hemi.index(hemi)-1][0].upper()
            info = [l for l in info if l[1] != hemi_exclude]
            try:
                for l in info:
                    info_dict[int(l[0])] = [l[2], l[3]]
            except ValueError:
                raise('every elements in first colonne must be integer')

        elif fileformat == 'xlsx':
            import xlrd
            wb = xlrd.open_workbook(filename)
            sh = wb.sheet_by_index(0)
            header = sh.row_values(0)

            hemi = {'lh': "Left", 'rh': "Right"}[hemi]
            index_col = search_xlsx(header, hemi)

            info = [sh.col_values(ind)[1:] for ind in index_col]
            info = list(zip(*info))

            try:
                for l in info:
                    info_dict[int(l[0])] = [l[1], l[3], l[2], l[4]]
            except ValueError:
                raise('every elements in first colonne must be integer')

        else:
            with open(filename, 'r') as textfile:
                lines = textfile.read().strip().split("\n")
                info = [l.split() for l in lines]
                header = info[0]
                label, hemi, name, lobe = search_xls(header)
                info.pop(0)

                info = [line for line in info if line[hemi] != hemi_exclude]
                try:
                    for line in info:
                        info_dict[int(line[label])] = [line[name], line[lobe]]
                except ValueError:
                    raise('every elements in first colonne must be integer')

                textfile.close()

    return info_dict


def create_param_dict(obj, hemi=None):

    param = {}
    hemi_keys = ['lh', 'rh']
    if len(obj) > 2:
        raise ValueError('obj size must less than 2')

    if hemi is not None:
        if hemi not in hemi_keys:
            raise ValueError('hemi must be None | lh | rh')

    if isinstance(obj, list):
        if hemi is not None:
            if len(obj) == 1:
                param[hemi] = obj[0]
            else:
                param[hemi] = obj[hemi_keys.index(hemi)]
        else:
            if len(obj) == 2:
                param = dict(lh=obj[0], rh=obj[1])
            else:
                try:
                    key = obj[0][0].hemi
                except Exception:
                    key = 'lh'
                param[key] = obj[0]
    elif isinstance(obj, dict):
        for key in obj.keys():
            if key in hemi_keys:
                param[key] = obj[key]
    else:
        raise TypeError('obj must be list or dict')

    return param


def compute_mean_centroids(vertex_pos, cluster_labels):
    """compute centroids for each cluster
    in replacement of Pycluster.clustercentroids
    """

    print("compute_mean_centroids")
    print(vertex_pos.shape, cluster_labels.shape)

    assert vertex_pos.shape[0] == cluster_labels.shape[0], \
        ("Error, not the vertices for positions and cluster_labels")

    centroids = np.array([np.mean(
        vertex_pos[cluster_labels == cluster_id, :], axis=0)
            for cluster_id in np.unique(cluster_labels)])

    print(centroids.shape)

    return centroids
