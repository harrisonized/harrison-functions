"""All functions related to reading files or writing files or folders
"""

from io import StringIO
import os
from os.path import realpath, dirname, abspath, sep
from os.path import join as ospj
import shutil
import zipfile
import gzip
import json
import re
import pandas as pd
import pandas.io.sql as pd_sql
from itertools import islice
from tqdm.notebook import tqdm
from configparser import ConfigParser
from .std.dataframe import execute_query_on_df
from .std.dict import build_nested_dict, merge_dict_with_subdicts
from ..etc.default_paths import dirname_n_times


# Functions
# # dirname_n_times  # imported
# # walk
# # read_folder_as_dict
# # read_sql_or_csv
# # read_json
# # read_csv_as_json
# # read_csv_from_text
# # create_nested_folder
# # recursive_zip
# # recursive_unzip
# # recursive_rm
# # read_gzipped_tsv
# # unzip_gzipped_file


def walk(main_dir):
    """
    | Returns a list of files
    | Slightly faster than recursive_walk
    """
    files = []
    for root, dirs, filenames in os.walk(main_dir, topdown=False):
        files.extend([f'{root}{sep}{filename}' for filename in filenames])
    return files


def read_folder_as_dict(dirpath, ext='.sql'):
    """
    | Enter the path of a directory, the folders become keys, text files become values
    | Nested directories become nested keys
    """

    if dirpath[-1] == sep:
        dirpath = dirpath[:-1]

    files = [path.replace(f'{dirpath}{sep}', "") for path in walk(dirpath) if ext in path]

    text_dict = {}
    for file in sorted(files):

        # get new data
        keys = file.replace(ext, '').split(sep)
        # print(keys)
        with open(f"{dirpath}{sep}{file}") as f:
            val = f.read()
        sub_dict = build_nested_dict(keys, val)

        # add nested sub_dict to text_dict
        text_dict = merge_dict_with_subdicts(text_dict, sub_dict)

    return text_dict


def read_csv_from_txt(filepath,
                      encoding='utf-16', sep='\t',
                      skiprows:int=None, nrows:int=None,
                      skipcols:int=None, ncols:int=None,
                      index:list=None,
                      columns:list=None,
                     ):
    """Convenience function for reading text files where csv may be embedded
    
    Use the following settings for 96-well plates:
    df = read_csv_from_txt(
        filepath,
        skiprows=3, nrows=8,
        skipcols=2, ncols=12,
        index=[i for i in string.ascii_uppercase[:8]],
        columns=[i for i in range(1, 13)],
    )
    
    Could come back and add header and index identifiers
    """
    
    row_start = skiprows or 0
    row_end = None if nrows is None else row_start + nrows
    col_start = skipcols or 0
    col_end = None if ncols is None else col_start + ncols
    
    with open(filepath, mode='r', encoding='utf-16') as f:
        lines = []
        for line in islice(f, row_start, row_end):
            lines.append([col for col in islice(line.split(sep), col_start, col_end)])
            
    return pd.DataFrame(lines, index=index, columns=columns)


def read_sql_or_csv(db_query,
                    df_query=None,
                    csv_filepath=None,
                    default_columns=None,
                    connection_uri=None):

    """Swtich case to get data from database or csv
    """

    try:
        df = pd_sql.read_sql(db_query, connection_uri)
        assert df.empty is False, 'No data returned'
    
    except:
        try:
            df = pd.read_csv(csv_filepath)
        except:
            df = pd.DataFrame(columns=default_columns)  # empty data
            
        if df_query:
            df = execute_query_on_df(dataframe=df, query=df_query)

    return df


def read_json(filepath, debug=False):
    """Retrieves figure from hardcoded path
    """
    if os.path.exists(filepath):
        with open(filepath) as f:
            fig = json.load(f)
        filename = os.path.basename(filepath)

        if debug:
            print(f'{filename} generated from tmp')

        return fig


def read_csv_as_json(csv_file):
    """
    Input:
    [header1, header2, ...]
    [data1, data2, ...]
    
    Output:    
    '[{"header1": "data1",
       "header2": "data2", 
       ...}
      ...]'

    Parses QD objects from LIMS
    """
    f = StringIO(csv_file)
    reader = csv.DictReader(f, delimiter=',')
    data = []
    
    for row in reader:
        data.append(dict(row))
        
    return json.dumps(data)


def create_nested_folder(current_dir, new_dir):
    """Example:
    current_dir = data/folder_1/folder_2
    new_dir = folder_3/folder_4

    Output: data/folder_1/folder_2/folder_3/folder_4
    """
    new_folder_list = new_dir.strip('/').split('/')
    for new_folder in new_folder_list:
        new_dir = f'{current_dir}/{new_folder}'
        try:
            os.mkdir(new_dir)
        except:
            pass
        current_dir=new_dir


def recursive_zip(main_dir):
    """Zips all individual items in a folder structure
    If item is a file and not .zip, zip it
    Else if item is a subdirectory, repeat
    """
    for item in tqdm(os.listdir(main_dir)):
        if os.path.isfile(f'{main_dir}/{item}') and item.split('.')[-1] != 'zip':
            # print(f'{main_dir}/{item}')
            with zipfile.ZipFile(f"{main_dir}/{item}.zip", mode='w', compression=zipfile.ZIP_DEFLATED) as z:
                z.write(filename=f'{main_dir}/{item}', arcname=item.split('/')[-1], compress_type=zipfile.ZIP_DEFLATED)
        elif os.path.isdir(f'{main_dir}/{item}') and item.split('.')[-1] != 'zip':
            sub_dir = f'{main_dir}/{item}'
            recursive_zip(sub_dir)


def recursive_unzip(main_dir):
    """Unzips all individual items in a folder structure
    If item is a file and .zip, unzip it
    Else if item is a subdirectory, repeat
    """
    for item in tqdm(os.listdir(main_dir)):
        if os.path.isfile(f'{main_dir}/{item}') and item.split('.')[-1] == 'zip':
            # print(f'{main_dir}/{item}')
            with zipfile.ZipFile(f'{main_dir}/{item}', mode='r') as z:
                z.extractall(path=main_dir)
        elif os.path.isdir(f'{main_dir}/{item}'):
            sub_dir = f'{main_dir}/{item}'
            recursive_unzip(sub_dir)


def recursive_rm(main_dir, ext):
    """Removes all files in a folder structure with a given extension
    If item is a file with extension ext
    Else if item is a subdirectory, repeat
    """
    for item in tqdm(os.listdir(main_dir)):
        if os.path.isfile(f'{main_dir}/{item}') and item.split('.')[-1] == ext:
            # print(f'{main_dir}/{item}')
            os.remove(f'{main_dir}/{item}')
        elif os.path.isdir(f'{main_dir}/{item}'):
            sub_dir = f'{main_dir}/{item}'
            recursive_rm(sub_dir, ext)


def read_gzipped_tsv(path, strip='!\n', sep='\t'):
    """Use this to read a single file
    """
    
    array = []
    with gzip.open(path, 'rb') as f:
        for row in f:
            array.append(list(map(lambda x: x.strip("\""), row.decode().strip("!\n").split(sep))))
    
    return array


def unzip_gzipped_file(path):
    """Use this to unzip a single file
    """
    
    filename = re.match(r'(?P<filename>.*).gz', path)['filename']
    with gzip.open(path, 'rb') as infile:
        with open(filename, 'wb') as outfile:
            shutil.copyfileobj(infile, outfile)
            
    print(f'{path} unzipped!')
