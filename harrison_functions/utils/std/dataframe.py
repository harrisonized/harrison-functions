"""Anything to do with manipulating dataframes
"""

import os
import collections
import csv
import json
import pandas as pd
import pandasql as ps
import dask.bag as db
from imblearn.under_sampling import RandomUnderSampler


# Functions
# # sort_df
# # create_agg_table
# # random_resample
# # append_standard_df
# # execute_query_on_df
# # bag_to_df
# # col_to_list
# # list_to_col
# # dict_to_col
# # cols_to_dict
# # expand_col
# # get_unique_list_items
# # generate_histogram_table
# # count_outcome_pass_fail


def sort_df(df, col:list, row:list):
    return df.loc[row, col]


def create_agg_table(df, group, agg, col_order=None, row_order=None):
    """Shortcut for groupby
    """
    df = df.groupby(group).apply(agg)

    if col_order:
        df = df[col_order]  # Sort columns
    if row_order:
        df = df.reindex(row_order)  # Sort rows
    return df


def append_standard_df(df, columns):
    """Forces a df to have the select_columns
    If it doesn't fills a column of NA's
    """
    empty_df = pd.DataFrame(columns=columns)
    df = empty_df.append(df)
    return df[columns]


def random_resample(df, category_col, input_sampling_lim):
    """Takes a df with numerical columns and a category column
    Returns a df that has been randomly undersampled
    
    Example input:
      | conc      | vol   | error
    --+-----------+-------+-------------
    0 | 101.41532 | 169.6 | "None"
    1 | 46.85500  | 167.2 | "Clot Error"
    ...
    
    Example sampling limit dictionary
    sampling_lims = {'None': 100,
                     'Clot Error': 100,
                     ... }

    Note: should probably rewrite this function using the random module, but this works for now
    """
    df = df.dropna()
    max_sampling_lim = dict(df[category_col].value_counts())

    # Make sure input does not exceed number of items
    sampling_lim = {item: min(count for count in (input_sampling_lim.get(item), max_sampling_lim.get(item)) if item)
                    for item in input_sampling_lim.keys() | max_sampling_lim.keys()}

    # Undersampling
    rus = RandomUnderSampler(random_state=0, sampling_strategy=sampling_lim)
    X, y = rus.fit_sample(df.drop(columns=[category_col]), df[category_col])
    X[category_col] = y

    return X


def execute_query_on_df(dataframe,
                        query,
                        index_name=None,
                        index_list=None):
    """Convenience function
    """
    df = ps.sqldf(query, locals())

    # Set index column
    if index_name:
        df = df.set_index(index_name)

    # Reorder index column
    if index_list:
        df = df.reindex(index_list)

    return df


def bag_to_df(bag, flatten=None, take=10000):
    """Converts bag to dataframe
    Make sure the take value is high enough but not too high
    """
    seq = bag.take(take)
    bag = db.from_sequence(seq, npartitions=1) # Converts back to bag for flattening
    if flatten:
        bag = bag.map(flatten)
    
    items = bag.take(take) # Grab important features
    df = pd.json_normalize(items)
    
    return df


def col_to_list(df, index, col, is_dict=False):
    """Takes a dataframe like the following:
    index | col_name
    ------+----------
    1     | 1
    1     | 2
    2     | 3
    2     | 3         # duplicate row
    2     | 4

    and returns the following:
    index | col
    ------+----------
    1     | [1, 2]
    2     | [3, 4]     # list items are unique
    """
    if is_dict:
        df[col] = df[col].apply(lambda x: json.dumps(x) if type(x) == dict else x)

    # Group all entries into a list
    grouped_df = pd.pivot_table(df.drop_duplicates(),
                                index=index, values=col,
                                aggfunc=lambda x: list(x) if list(x) != [None] else None).reset_index()

    if is_dict:
        grouped_df[col] = grouped_df[col].apply(
            lambda list_of_dict: list(map(lambda str_json: json.loads(str_json), list_of_dict)))

    return grouped_df


def list_to_col(df, list_col: str):
    """Takes a dataframe like the following:
    idx | list_col
    ----+----------
    1   | [1, 2]
    2   | [3, 4, 5]

    and returns the following:
    idx | list_col
    ----+----------
    1   | 1
    1   | 2
    2   | 3
    2   | 4
    2   | 5

    """
    return df.explode(list_col).reset_index(drop=True)


def dict_to_col(df, col: str, to_include=False, prefix=None):
    """Expands a single dataframe column containing dictionaries into columns.
    Input:
    idx_1 | ... | new_col
    ------+-----+--------------------------------------
    idx_1 | ... | {'key_1': val_1, 'key_2': val_2, ...}

    Returns:
    idx_0 | ... | key_1 | key_2 | ...
    ------+-----+-------+-------+-----
    val_0 | ... | val_1 | val_2 | ...

    This does not work well with 500K rows.
    If there are too many rows, break the df into chunks:
    new_df = pd.DataFrame()
    step = 1000
    for i in tqdm(range(100)):
        new_df = pd.concat([new_df, dict_to_col(df[step*i:step*(i+1)], 'pull_expr')])
    """
    df = df.reset_index(drop=True) # required for this to work correctly
    if prefix:
        df = df.join(df[col].apply(lambda x: pd.Series(x).add_prefix(f'{prefix}_')))
    else:
        df = df.join(pd.DataFrame(df[col].tolist()))
    
    if to_include:
        return df
    else:
        return df.drop(columns=[col])


def cols_to_dict(df, cols: list, col_name='dict_col', to_include=False):
    """Collapses columns into a single column containing dictionaries.
    Input:
    idx_0 | ... | key_1 | key_2 | ...
    ------+-----+-------+-------+-----
    val_0 | ... | val_1 | val_2 | ...
    
    Returns:
    idx_1 | ... | new_col
    ------+-----+--------------------------------------
    idx_1 | ... | {"key_1": val_1, "key_2": val_2, ...}
    """
    df[col_name] = df[cols].to_dict(orient='records')

    if to_include:
        return df
    else:
        return df.drop(columns=cols)


def expand_col(df, cols: list, to_include=False, to_append_name=False):
    """Applies dict_to_col on multiple columns
    """
    if to_append_name:
        old_cols = df.columns.to_list()
        for col in cols:
            df = dict_to_col(df, col, to_include=to_include)
            new_cols = list(set(df.columns.to_list()) - set(old_cols) - set(col))
            rename_dict = dict(zip(new_cols, list(map(lambda x: f'{col}_' + x, new_cols))))
            df = df.rename(columns=rename_dict)

    else:
        for col in cols:
            df = dict_to_col(df, col, to_include=to_include)

    return df


def get_unique_list_items(df_list_col):
    """Given a dataframe column with a list, returns all the categories in that list.
    idx | df_list_col 
    ----+-----------------------
     0  | [val_1, val_2]
     1  | [val_2, val_3, val_4]
    ...

    Returns:
    [val_1, val_2, val_3, val_4, ...]
    """
    unique_items = df_list_col.apply(lambda x: sorted(x) if type(x) == list else []).apply(str).unique()  # sort
    unique_items = list(map(lambda x: x.replace("\'", "\""), unique_items))  # jsonify
    unique_items = list(map(lambda x: json.loads(x), unique_items))  # stringify

    return list(set([item for sublist in unique_items for item in sublist]))


def generate_histogram_table(df, bins: list, value: float, category: str):
    """Takes a df with the following columns:
    category | value
    ---------+-------
    cat_1    | 6
    cat_2    | 12
    ...      | ...
    and a list of bins:
    bins = [0, 10, 20, ...]
    
    And returns a table with the following columns:
    value_bins | cat_1 | cat_2 | ...
    -----------+-------+-------+-----
    [0, 10)    |   1   |   0   | ...
    [10, 20)   |   0   |   1   | ...
    ...        |  ...  |  ...  | ...

    Used to convert the input for plot_violin to the input for plot_panel_histogram
    """
    df[f'{value}_bins'] = pd.cut(df[value], bins, right=False)
    df[f'{value}_bins'] = df[f'{value}_bins'].apply(lambda x: str(x))
    histogram_table = pd.DataFrame(df.groupby([f'{value}_bins', category]).size(), columns=['category']).unstack()[
        'category']
    return histogram_table


def count_outcome_pass_fail(df):
    """Given a df with the following:
    id | val_1 | outcome_1 | val_2 | outcome_2 | ...
    ---+-------+-----------+-------+-----------+-----
     1 | true  |   Pass    |  619  |   Pass    | ...
     2 | false |   Fail    |  222  |   Pass    | ...
     
    Counts number of Pass or Fail per row and returns them as extra columns
    Returns:
    id | ... | total_pass | total_fail 
    ---+-----+------------+-------------
     1 | ... |     2      |     10
     2 | ... |    11      |      1
    ...
    """
    outcome_cols = list(filter(lambda x: x.split('_')[-1]=='outcome', df.columns.to_list()))
    pass_fail_df = df[outcome_cols].apply(pd.Series.value_counts, axis=1)
    pass_fail_cols = pass_fail_df.columns.to_list()
    df[[f'total_{cat.lower()}' for cat in pass_fail_cols]] = pass_fail_df.fillna(0)
    return df
