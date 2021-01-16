import os
import shutil
import re
import zipfile
import gzip
from tqdm.notebook import tqdm


# Functions included in this file:
# # recursive_zip
# # recursive_unzip
# # recursive_rm


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


