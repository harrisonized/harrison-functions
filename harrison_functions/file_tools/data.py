import pandas as pd
import dask.bag as db

# Functions included in this file:
# # bag_to_df


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
