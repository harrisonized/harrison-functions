import os
from os.path import realpath, dirname, abspath
from os.path import join as ospj
from configparser import ConfigParser
import psycopg2 as pg
from .encryption_tools import decrypt_message


# Functions included in this file:
# # postgres_connection_fetch_close
# # read_section_from_ini
# # postgres_connection_from_ini
# # heroku_postgres_connection_from_ini


def postgres_connect_fetch_close(query, connection_uri, dbname=None):
    """Opens a new connection, fetches the data, then closes the connection
    Provide the connection_uri returned by postgres_connection
    Use dbname to change the database
    """
    connection = pg.connect(dsn=connection_uri, dbname=dbname)  # connect
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    
    return results


def read_section_from_ini(cfg_path, section='default'):
    """To be used with conf/settings.ini"""
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)

    assert cfg.has_section(section), f'Missing section at [{section}]'

    return cfg[section]


def postgres_connection_from_ini(
        cfg_path,
        ini_key,
        section='postgres',  # or 'heroku-postgres'
        username=None, password=None, host=None, port=None, database=None,
    ):
    """Given an INI file with a ['postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'
    
    for key in ['username', 'password', 'host', 'port']:
        assert cfg.has_option(section, key), f'Missing key at {key}'

    if username is None:
        username = decrypt_message(cfg.get(section, 'username'), ini_key)
    if password is None:
        password = decrypt_message(cfg.get(section, 'password'), ini_key)
    if host is None:
        host = decrypt_message(cfg.get(section, 'host'), ini_key)
    if port is None:
        port = decrypt_message(cfg.get(section, 'port'), ini_key)

    if database:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}/{database}'
    else:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}'

    return connection_uri


def heroku_postgres_connection_from_ini(
    cfg_path,
    ini_key,
    section='heroku-postgres',
):
    """Given an INI file with a ['heroku-postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    assert os.path.exists(cfg_path), f'Missing file at {cfg_path}'
    
    cfg = ConfigParser()
    cfg.read(cfg_path)
    
    assert cfg.has_section(section), f'Missing section at [{section}]'
    
    for key in ['username', 'password', 'host', 'port', 'db_name']:
        assert cfg.has_option(section, key), f'Missing key at {key}'

    username, password, host, port, database = (
        decrypt_message(cfg.get(section, key), ini_key)
        for key in ['username', 'password', 'host', 'port', 'db_name']
    )

    connection_uri = f'postgres://{username}:{password}@{host}:{port}/{database}'

    return connection_uri
