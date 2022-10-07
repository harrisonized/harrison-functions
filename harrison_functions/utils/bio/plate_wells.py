import string
import itertools
import numpy as np
import pandas as pd


# Objects
# # rows_96
# # cols_96
# # wells_96
# # rows_384
# # cols_384
# # wells_384

# Functions:
# # draw_plate


#:
rows_96 = list(string.ascii_uppercase[0:8])

#: 
cols_96 = list(range(1, 13))

#: 
wells_96 = [row + '{col:02d}'.format(col=col) for row, col in list(itertools.product(rows_96, cols_96))]

#: 
rows_384 = list(string.ascii_uppercase[0:16])

#: 
cols_384 = list(range(1, 25))

#: 
wells_384 = [row + '{col:02d}'.format(col=col) for row, col in list(itertools.product(rows_384, cols_384))]


def draw_plate(position_obj, num_rows=8, num_cols=12, fillna=False):
    """
    | Takes a dictionary with the following format:
    
    .. code-block:: python

        {'A1': 2.1,
         'A2': 1.9, ...}
    
    | and converts it to a dataframe with the following structure:
    
    +-----+-----+-----+-----+
    |     |  1  |  2  | ... |
    +=====+=====+=====+=====+
    | 'A' | 2.1 | 1.9 | ... |
    +-----+-----+-----+-----+
    | 'B' | ... |     |     |
    +-----+-----+-----+-----+
    
    """

    # Initialize empty dataframe
    if fillna is False:
        val = None
    else:
        val = 0

    rows = list(string.ascii_uppercase[val:num_rows])
    df = pd.DataFrame(dict(zip(rows, [[val] * num_cols] * num_rows)), dtype=np.float64)

    df.index += 1

    if type(position_obj) == list:
        for position in position_obj:
            df[position[0]][int(position[1:])] = 1
    elif type(position_obj) == dict:
        for key in position_obj.keys():
            df[key[0]][int(key[1:])] = position_obj[key]
    elif type(position_obj) == str:
        df[position_obj[0]][int(position_obj[1:])] = 1
    else:
        raise TypeError('Please enter a str, list, or dict object.')

    table_df = df.transpose()

    return table_df
