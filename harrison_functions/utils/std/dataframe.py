"""Anything to do with manipulating dataframes
"""

import json
import pandas as pd
import pandasql as ps
import dask.bag as db
from imblearn.under_sampling import RandomUnderSampler

# Functions
# # append_standard_df
# # execute_query_on_df
# # sort_df
# # split_df
# # random_resample
# # count_outcome_pass_fail
# # col_to_list
# # list_to_col
# # dict_to_col
# # cols_to_dict
# # expand_col
# # get_unique_list_items
# # generate_histogram_table
# # create_agg_table
# # make_sankey_df
# # make_link_and_node_df
# # bag_to_df


def append_standard_df(df, columns):
    """
    | Forces a df to have the select_columns
    | If it doesn't fills a column of NA's
    """
    empty_df = pd.DataFrame(columns=columns)
    df = empty_df.append(df)
    return df[columns]


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


def sort_df(df, col:list, row:list):
    return df.loc[row, col]


def split_df(df, x, c=None):
    """
    | Helper function for plot_multiple_scatter and plot_violin

    | Takes a dataframe in the following format:
    
    +-------+---------+
    | cat   | val     |
    +=======+=========+
    | cat_1 | val_1.1 |
    +-------+---------+
    | cat_1 | val_1.2 |
    +-------+---------+
    | ...   |         |
    +-------+---------+
    | cat_2 | val_2.1 |
    +-------+---------+
    | cat_2 | val_2.2 |
    +-------+---------+
    | ...   |         |
    +-------+---------+

    | If you instead have:

    +---------+---------+-----+
    | cat1    | cat2    | ... |
    +=========+=========+=====+
    | val_1.1 | val_2.1 | ... |
    +---------+---------+-----+
    | val_1.2 | val_2.2 | ... |
    +---------+---------+-----+

    | Reshape it into the appropriate format using pd.melt
    | pd.melt(df, value_vars = [cat1, cat2, ...], var_name='category')
    | The order of the value_vars determines the order they appear on the plot.

    """
    df_list = []

    if c is None:
        for cat in df[x].apply(str).unique():
            df_list.append(df[df[x].apply(str) == cat])
        return df_list

    else:
        count_df = df.groupby([x, c]).size().reset_index()
        combo_list = list(zip(count_df[x], count_df[c]))

        for combo in combo_list:
            df_list.append(df[(df[x].apply(str) == combo[0])
                              & (df[c].apply(str) == combo[1])])
        return df_list


def random_resample(df, category_col, input_sampling_lim):
    """
    | Takes a df with numerical columns and a category column
    | Returns a df that has been randomly undersampled
    
    | Example input:

    +---+-----------+-------+--------------+
    |   | conc      | vol   | error        |
    +===+===========+=======+==============+
    | 0 | 101.41532 | 169.6 | "None"       |
    +---+-----------+-------+--------------+
    | 1 | 46.85500  | 167.2 | "Clot Error" |
    +---+-----------+-------+--------------+
    
    | Example sampling limit dictionary

    .. code-block:: python

        sampling_lims = {'None': 100,
                         'Clot Error': 100,
                         ... }

    | Note: should probably rewrite this function using the random module, but this works for now
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


def count_outcome_pass_fail(df):
    """
    | Given a df with the following:

    +----+-------+-----------+-------+-----------+-----+
    | id | val_1 | outcome_1 | val_2 | outcome_2 | ... |
    +====+=======+===========+=======+===========+=====+
    |  1 | true  |   Pass    |  619  |   Pass    | ... |
    +----+-------+-----------+-------+-----------+-----+
    |  2 | false |   Fail    |  222  |   Pass    | ... |
    +----+-------+-----------+-------+-----------+-----+
 
    Counts number of Pass or Fail per row and returns them as extra columns
    
    Returns:
    
    +----+-----+------------+------------+
    | id | ... | total_pass | total_fail |
    +====+=====+============+============+
    |  1 | ... |     2      |     10     |
    +----+-----+------------+------------+
    |  2 | ... |    11      |      1     |
    +----+-----+------------+------------+
    
    """
    outcome_cols = list(filter(lambda x: x.split('_')[-1]=='outcome', df.columns.to_list()))
    pass_fail_df = df[outcome_cols].apply(pd.Series.value_counts, axis=1)
    pass_fail_cols = pass_fail_df.columns.to_list()
    df[[f'total_{cat.lower()}' for cat in pass_fail_cols]] = pass_fail_df.fillna(0)
    return df


def col_to_list(df, index, col, is_dict=False):
    """
    | Takes a dataframe like the following:
    
    +-------+-------------------+
    | index | col_name          |
    +=======+===================+
    | 1     | 1                 |
    +-------+-------------------+
    | 1     | 2                 |
    +-------+-------------------+
    | 2     | 3                 |
    +-------+-------------------+
    | 2     | 3 # duplicate row |
    +-------+-------------------+
    | 2     | 4                 |
    +-------+-------------------+

    | and returns the following:
    
    +-------+--------+
    | index | col    |
    +=======+========+
    | 1     | [1, 2] |
    +-------+--------+
    | 2     | [3, 4] |
    +-------+--------+

    | Note: list items are unique

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
    """
    | Takes a dataframe like the following:
    
    +-----+-----------+
    | idx | list_col  |
    +=====+===========+
    | 1   | [1, 2]    |
    +-----+-----------+
    | 2   | [3, 4, 5] |
    +-----+-----------+

    | and returns the following:
    
    +-----+----------+
    | idx | list_col |
    +=====+==========+
    | 1   | 1        |
    +-----+----------+
    | 1   | 2        |
    +-----+----------+
    | 2   | 3        |
    +-----+----------+
    | 2   | 4        |
    +-----+----------+
    | 2   | 5        |
    +-----+----------+

    """
    return df.explode(list_col).reset_index(drop=True)


def dict_to_col(df, col: str, to_include=False, prefix=None):
    """
    | Expands a single dataframe column containing dictionaries into columns.
    | Input:
    
    +-------+-----+---------------------------------------+
    | idx_1 | ... | new_cols                              |
    +=======+=====+=======================================+
    | idx_1 | ... | {'key_1': val_1, 'key_2': val_2, ...} |
    +-------+-----+---------------------------------------+

    | Returns:
    
    +-------+-----+-------+-------+-----+
    | idx_0 | ... | key_1 | key_2 | ... |
    +=======+=====+=======+=======+=====+
    | val_0 | ... | val_1 | val_2 | ... |
    +-------+-----+-------+-------+-----+

    | This does not work well with 500K rows.
    | If there are too many rows, break the df into chunks:
    
    .. code-block:: python
    
        new_df = pd.DataFrame()
        step = 1000
        for i in tqdm(range(100)):
            new_df = pd.concat([new_df, dict_to_col(df[step*i:step*(i+1)], 'dict')])

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
    """
    | Collapses columns into a single column containing dictionaries.
    | Input:
    
    +-------+-----+-------+-------+------+
    | idx_0 | ... | key_1 | key_2 | ...  |
    +=======+=====+=======+=======+======+
    | val_0 | ... | val_1 | val_2 | ...  |
    +-------+-----+-------+-------+------+
    
    | Returns:
    
    +-------+-----+---------------------------------------+
    | idx_1 | ... | new_col                               |
    +=======+=====+=======================================+
    | idx_1 | ... | {"key_1": val_1, "key_2": val_2, ...} |
    +-------+-----+---------------------------------------+

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
    """
    | Given a dataframe column with a list, returns all the categories in that list.
    
    +-----+-----------------------+
    | idx | df_list_col           |
    +=====+=======================+
    |  0  | [val_1, val_2]        |
    +-----+-----------------------+
    |  1  | [val_2, val_3, val_4] |
    +-----+-----------------------+

    | Returns:
    
    .. code-block:: python

        [val_1, val_2, val_3, val_4, ...]
    
    """
    unique_items = df_list_col.apply(lambda x: sorted(x) if type(x) == list else []).apply(str).unique()  # sort
    unique_items = list(map(lambda x: x.replace("\'", "\""), unique_items))  # jsonify
    unique_items = list(map(lambda x: json.loads(x), unique_items))  # stringify

    return list(set([item for sublist in unique_items for item in sublist]))


def generate_histogram_table(df, bins: list, value: float, category: str):
    """
    | Takes a df with the following columns:
    
    +----------+-------+
    | category | value |
    +==========+=======+
    | cat_1    | 6     |
    +----------+-------+
    | cat_2    | 12    |
    +----------+-------+
    | ...      | ...   |
    +----------+-------+
    
    | and a list of bins: ``bins = [0, 10, 20, ...]``
    
    | And returns a table with the following columns:
    
    +------------+-------+-------+-----+
    | value_bins | cat_1 | cat_2 | ... |
    +============+=======+=======+=====+
    | [0, 10)    |   1   |   0   | ... |
    +------------+-------+-------+-----+
    | [10, 20)   |   0   |   1   | ... |
    +------------+-------+-------+-----+
    | ...        |  ...  |  ...  | ... |
    +------------+-------+-------+-----+

    | Used to convert the input for plot_violin to the input for plot_panel_histogram
    """
    df[f'{value}_bins'] = pd.cut(df[value], bins, right=False)
    df[f'{value}_bins'] = df[f'{value}_bins'].apply(lambda x: str(x))
    histogram_table = pd.DataFrame(df.groupby([f'{value}_bins', category]).size(), columns=['category']).unstack()[
        'category']
    return histogram_table


def create_agg_table(df, group, agg, col_order=None, row_order=None):
    """Shortcut for groupby
    """
    df = df.groupby(group).apply(agg)

    if col_order:
        df = df[col_order]  # Sort columns
    if row_order:
        df = df.reindex(row_order)  # Sort rows
    return df


def make_sankey_df(history_df, dropna=False, fillna='None'):
    """
    | Counts the number of occurences of each line of the history_df
    
    | Takes a history_df in this format:

    +------+-------+-------+-----+
    | idx  |   0   |   1   | ... |
    +======+=======+=======+=====+
    | id_1 | cat_1 | cat_2 | ... |
    +------+-------+-------+-----+
    | id_2 | cat_2 | None  | ... |
    +------+-------+-------+-----+
    
    | Returns: 
    
    +----+-------+-------+-----+-----+-------+-------+-----+
    |    |   0   |   1   | ... | num | idx_0 | idx_1 | ... |
    +====+=======+=======+=====+=====+=======+=======+=====+
    | 1  | cat_1 | cat_2 | ... |  2  |   1   |   8   | ... |
    +----+-------+-------+-----+-----+-------+-------+-----+
    | 2  | cat_2 | None  | ... | 10  |   2   |   9   | ... |
    +----+-------+-------+-----+-----+-------+-------+-----+
    
    | use history_df.pivot to get the history_df after indexing
    
    .. code-block:: python

        history_df = history_df.pivot(index='rq', columns='ib_num', values='specimen_type')
    
    """
    steps = history_df.columns.to_list()
    index = history_df.index.name
    history_df = history_df.fillna(fillna)

    sankey_df = history_df.reset_index().groupby(steps)[index].nunique().reset_index().rename(columns={index: 'num'})

    # generate source-target indices
    idx_start = 0
    if dropna is True:
        sankey_df = sankey_df.replace({fillna: None})
        for step in steps:
            sankey_df[f'step_{step}'] = sankey_df[step].astype('category').cat.codes.replace({-1: None}) + idx_start
            idx_start = sankey_df[f'step_{step}'].max() + 1
    else:
        for step in steps:
            sankey_df[f'step_{step}'] = sankey_df[step].astype('category').cat.codes + idx_start
            idx_start = sankey_df[f'step_{step}'].max() + 1

    return sankey_df


def make_link_and_node_df(sankey_df, num_steps: int, dropna=False):
    """
    | Takes a df in the following format (output of make_sankey_df):
    
    +-----+-------+-------+-----+-----+--------+--------+-----+
    |     |   0   |   1   | ... | num | step_0 | step_1 | ... |
    +=====+=======+=======+=====+=====+========+========+=====+
    |  1  | cat_1 | cat_2 | ... |  2  |   0    |   8    | ... |
    +-----+-------+-------+-----+-----+--------+--------+-----+
    |  2  | cat_2 | None  | ... | 10  |   1    |   9    | ... |
    +-----+-------+-------+-----+-----+--------+--------+-----+

    
    | Returns link_df:

    +---+--------+--------+-----+
    |   | source | target | num |
    +===+========+========+=====+
    | 0 |   0    |   8    | 114 |
    +---+--------+--------+-----+
    | 1 |   1    |   9    |  57 |
    +---+--------+--------+-----+
    
    | Returns node_df:

    +---+--------+-------+--------+
    |   | source | label | step   |
    +===+========+=======+========+
    | 0 |   0    | cat_1 | step_0 |
    +---+--------+-------+--------+
    | 1 |   1    | cat_2 | step_0 |
    +---+--------+-------+--------+

    """
    # reshape into source-target
    steps = range(num_steps)
    link_df = pd.lreshape(sankey_df,
                          groups={'source': [f'step_{step}' for step in steps[:-1]],
                                  'target': [f'step_{step}' for step in steps[1:]]})[['source', 'target', 'num']]
    link_df = link_df.groupby(['source', 'target']).sum().reset_index()

    # get index labels
    node_df = pd.lreshape(sankey_df,
                          groups={'source': [f'step_{step}' for step in steps],
                                  'label': steps})[['source', 'label']].drop_duplicates().sort_values(
        'source').reset_index(drop=True)

    # link source indices to step
    step_source = sankey_df[[f'step_{step}' for step in steps]].to_dict(orient='list')
    step_source = {k: list(set(v)) for k, v in step_source.items()}
    source_step_dict = {}
    for k, v in step_source.items():
        for source in v:
            source_step_dict[source] = k
    node_df['step'] = node_df['source'].apply(lambda x: source_step_dict[x])

    if dropna is True:
        # generate new indices for link_df
        step_stack_df = pd.lreshape(link_df, {'step_stack': ['source', 'target']})[['step_stack']]
        step_stack_df['new_idx'] = step_stack_df['step_stack'].astype('category').cat.codes
        step_stack_df = step_stack_df.drop_duplicates()
        replace_dict = dict(zip(step_stack_df['step_stack'], step_stack_df['new_idx']))
        link_df.loc[:, ['source', 'target']] = link_df.loc[:, ['source', 'target']].replace(
            replace_dict)  # reassign missing keys

        # filter out missing keys from node_df
        node_df = node_df[(node_df['source'].isin(replace_dict.keys()))]
        node_df.loc[:, 'source'] = node_df.loc[:, 'source'].replace(replace_dict)  # reassign missing keys

    return link_df, node_df


def bag_to_df(bag, flatten=None, take=10000):
    """
    | Converts bag to dataframe
    | Make sure the take value is high enough but not too high
    """
    seq = bag.take(take)
    bag = db.from_sequence(seq, npartitions=1) # Converts back to bag for flattening
    if flatten:
        bag = bag.map(flatten)
    
    items = bag.take(take) # Grab important features
    df = pd.json_normalize(items)
    
    return df
