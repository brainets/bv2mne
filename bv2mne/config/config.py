import warnings
import json
import os.path as op


def setup_db_coords(database_name, project_name, overwrite=True):

    if not op.exists(database_name):
        raise NotADirectoryError('The specified direcory {0} does not exist, '
                                 'please check database position'.format(database_name))
    if (not op.exists(op.join(database_name, 'db_brainvisa')) and
        not op.exists(op.join(database_name, 'db_freesurfer'))):
        warnings.warn('The specified directory lacks of one or more needed databases, please check')
    if (not op.exists(op.join(database_name, 'db_brainvisa', project_name)) and
        not op.exists(op.join(database_name, 'db_freesurfer', project_name))):
        warnings.warn('Project not detected in one ore more databases, please check')

    save_dir = op.abspath(__file__).replace('config.py', '')
    coords = {'db_name': database_name,
              'p_name': project_name}

    if op.exists(op.join(save_dir, 'db_coords.json')):
        if not overwrite: raise ValueError('Coordinate file exist, to change the values set \'overwrite=True\'')
        else:
            with open(op.join(save_dir, 'db_coords.json'), 'w') as cf:
                json.dump(coords, cf)
    else:
        with open(op.join(save_dir, 'db_coords.json'), 'w') as cf:
            json.dump(coords, cf)

    print('Database coordinates saved in {0}'.format(op.join(save_dir, 'db_coords.json')))
    return


def read_db_coords():
    read_dir = op.abspath(__file__).replace('config.py', '')
    json_fname = op.join(read_dir, 'db_coords.json')

    if op.exists(json_fname):
        print('Loading database coordinates...')
        with open(json_fname, 'r') as open_file:
            coords = json.load(open_file)
            database = coords['db_name']
            project = coords['p_name']
        return database, project
    else:
        raise FileExistsError('Database coordinates file do not exist, please set them using '
                                '\'setup_db_coords()\' function, specifying the folder that '
                              'contains BrainVISA and FreeSurfer databases, and the project name')
