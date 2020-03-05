import warnings
import json
import os.path as op


def setup_db_coords(database_name, project_name, json_path='default', overwrite=True):
    """ Setup database coordinates for the specific project

    Parameters
    ----------
    database_name : str
        The folder where the databases of freesurfer and brainvisa are stored
    project_name : str
        The name of the current project
    json_path : str | 'default'
        Where the json file containing coordinates will be stored. The json file will be called 'db_coords.json'
        If 'default, the json file will be saved in the same location of bv2mne package.
    overwrite : bool
        If True, overwrite the 'db_coords.json' file if it already exist

    Returns:
    -------
    json_fname : str
        The path of the json file
    -------
    """


    assert type(database_name) == str, 'The path of the database should be a type str'
    assert type(project_name) == str, 'The name of the project should be a type str'
    assert type(json_path) == str, 'The path to the json file should be a type str'

    if not op.exists(database_name):
        raise NotADirectoryError('The specified direcory {0} does not exist, '
                                 'please check database position'.format(database_name))
    if (not op.exists(op.join(database_name, 'db_brainvisa')) and
        not op.exists(op.join(database_name, 'db_freesurfer'))):
        warnings.warn('The specified directory lacks of one or more needed databases, please check')
    if (not op.exists(op.join(database_name, 'db_brainvisa', project_name)) and
        not op.exists(op.join(database_name, 'db_freesurfer', project_name))):
        warnings.warn('Project not detected in one ore more databases, please check')

    if json_path == 'default':
        save_dir = op.join(op.abspath(__package__), 'config')
    else: save_dir = json_path

    coords = {'db_name': database_name,
              'p_name': project_name}

    json_fname = op.join(save_dir, 'db_coords.json')
    if op.exists(json_fname):
        if not overwrite: raise ValueError('Coordinate file exist, to change the values set \'overwrite=True\'')
        else:
            with open(json_fname, 'w') as cf:
                json.dump(coords, cf)
    else:
        with open(json_fname, 'w') as cf:
            json.dump(coords, cf)

    print('Database coordinates saved in {0}'.format(json_fname))
    return json_fname


def read_db_coords(json_fname='default'):
    """  Read the coordinates of the database and the project

    Parameters
    ----------
    json_fname : str | 'default
        The path of the json file with the database coordinates

    Returns
    -------
    database : str
        Database coordinates
    project : str
        Project name
    """

    if json_fname == 'default':
        read_dir = op.join(op.abspath(__package__), 'config')
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
