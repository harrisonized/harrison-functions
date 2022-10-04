"""All paths and connection_uris should be accessed from here
"""

import os
from os.path import realpath, dirname, abspath, sep
from os.path import join as ospj
from harrison_functions.utils.special.auth.connections import (postgres_connection_from_ini,
	                                                           heroku_postgres_connection_from_ini)

INI_KEY = os.getenv('INI_KEY') or ''  # Make sure this is in your ~/.bashrc

def dirname_n_times(path, n=1):
    for i in range(n):
        path = dirname(path)
    return path

this_dir = realpath(ospj(os.getcwd(), dirname(__file__)))
settings_cfg_path = abspath(ospj(dirname_n_times(this_dir, 2), 'configs/settings.ini'))
databases_cfg_path = abspath(ospj(dirname_n_times(this_dir, 2), 'configs/databases.ini'))
postgres_connection_uri = postgres_connection_from_ini(cfg_path=databases_cfg_path, ini_key=INI_KEY)
heroku_connection_uri = heroku_postgres_connection_from_ini(cfg_path=databases_cfg_path, ini_key=INI_KEY)
