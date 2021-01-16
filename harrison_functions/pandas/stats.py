from imblearn.under_sampling import RandomUnderSampler


# Objects included in this file:
# None

# Functions included in this file:
# # random_resample


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
