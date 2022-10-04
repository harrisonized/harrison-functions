"""All paths and connection_uris should be accessed from here
"""

import os
from os.path import realpath, dirname, abspath
from os.path import join as ospj
from ..utils.connections import connection_uri_from_ini
from ..utils.file_io import dirname_n_times

INI_KEY = os.getenv('INI_KEY')  # Make sure this is in your ~/.bashrc


this_dir = realpath(ospj(os.getcwd(), dirname(__file__)))
settings_cfg_path = abspath(ospj(dirname_n_times(this_dir, 2), 'configs/settings.ini'))
databases_cfg_path = abspath(ospj(dirname_n_times(this_dir, 2), 'configs/databases.ini'))

postgres_connection_uri = connection_uri_from_ini(databases_cfg_path,
	                                              ini_key=INI_KEY,
	                                              section='postgres')

heroku_connection_uri = connection_uri_from_ini(databases_cfg_path,
	                                            ini_key=INI_KEY,
	                                            section='heroku-postgres')
