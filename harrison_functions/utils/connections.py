import psycopg2 as pg
from .file_io import read_ini_as_dict

# Functions
# # postgres_connect_fetch_close
# # connection_uri_from_ini


def postgres_connect_fetch_close(query, connection_uri, db_name=None):
    """Opens a new connection, fetches the data, then closes the connection
    Provide the connection_uri returned by postgres_connection
    Use dbname to change the database
    """
    connection = pg.connect(dsn=connection_uri, dbname=db_name)  # connect
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    
    return results


def connection_uri_from_ini(
        filepath,
        section='postgres',  # or 'heroku-postgres'
        ini_key=None,  # enter if encrypted, otherwise leave blank 
    ):
    """Given an INI file with a ['postgres'] section
    Returns the sqlalchemy connection args 

    Make sure the config.ini file exists in your project
    """
    ini_dict = read_ini_as_dict(filepath, ini_key, sections=[section]).get(section, {})
    username, password, host, port, db_name = [
        ini_dict.get(key)
        for key in ['username', 'password', 'host', 'port', 'db_name']
    ]
    
    if db_name:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}/{db_name}'
    else:
        connection_uri = f'postgres://{username}:{password}@{host}:{port}'

    return connection_uri
