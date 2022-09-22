from io import StringIO
from itertools import islice
import csv
import json
import pandas as pd


# Functions
# # csv_to_json
# # read_csv_from_txt


def csv_to_json(csv_file):
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
