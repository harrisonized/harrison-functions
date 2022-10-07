"""Functions to manipulate datetimes
"""

import dateutil
import pytz
import pandas as pd

# Functions
# # utc_to_pacific
# # timestamp_to_datetime
# # group_date_range_by_week
# # group_date_range_by_day
# # create_week_list
# # create_day_list
# # stringify_date
# # round_date_to_week


def utc_to_pacific(df, date_cols=None):
    """
    | Converts type ``pytz.timezone('America/Los_Angeles')`` to ``pytz.timezone('America/Los_Angeles')``
    | If no date_cols specified, converts all columns with dtype ``'datetime64[ns, tzutc()]'``
    """
    if not date_cols:
        date_cols = [col for col in df.columns if df[col].dtype == 'datetime64[ns, tzutc()]']
        
    for col in date_cols:
        df[col] = df[col].apply(
            lambda x: dateutil.parser.parse(str(x)).astimezone(tz=pytz.timezone('America/Los_Angeles')) if pd.isnull(x) is False else x)
    return df


def timestamp_to_datetime(df, date_cols=None, dtype='<M8[ns]', tz=pytz.timezone('UTC')):
    """
    | Converts type ``pandas._libs.tslibs.timestamps.Timestamp`` to datetime
    | Use ``tz=pytz.timezone('America/Los_Angeles')`` for Pacific time
    
    | If no date_cols specified, converts all datetime columns with input dtype
    | Note: this is the same as utc_to_pacific with different default options
    """
    if not date_cols:
        date_cols = [col for col in df.columns if df[col].dtype == dtype]
        
    for col in date_cols:
        df[col] = df[col].apply(
            lambda x: dateutil.parser.parse(str(x)).astimezone(tz=tz) if pd.isnull(x) is False else x)
    return df


def group_date_range_by_week(date_range_idx):
    """Used with create_week_list
    """
    week_list = []
    for date in date_range_idx:
        date_start, date_end = date, date + pd.Timedelta(days=7)
        date_start_s, date_end_s = date_start.strftime('%Y-%m-%d'), date_end.strftime('%Y-%m-%d')
        week_list.append({'date_start': date_start_s, 'date_end': date_end_s})
    return week_list


def group_date_range_by_day(date_range_idx):
    """Used with create_day_list
    """
    day_list = []
    for date in date_range_idx:
        date_start, date_end = date, date + pd.Timedelta(days=1)
        date_start_s, date_end_s = date_start.strftime('%Y-%m-%d'), date_end.strftime('%Y-%m-%d')
        day_list.append({'date_start': date_start_s, 'date_end': date_end_s})

    return day_list


def create_week_list(date_start: str, date_end: str, week_start="SUN"):
    """
    | Given a date_start and date_end, creates a list of dictionaries
    

    .. code-block:: python
    
        >>> create_week_list('2020-08-01', '2020-09-01')
    
        [{'date_start': '2020-07-26', 'date_end': '2020-08-02'},
         {'date_start': '2020-08-02', 'date_end': '2020-08-09'},
         ...
         {'date_start': '2020-08-30', 'date_end': '2020-09-06'}]

    | Weeks start on SUN by default
    """
    day_shift = {"SAT": -1, "SUN": 0, "MON": 1}
    days = day_shift[week_start]
    date_start_t = dateutil.parser.parse(date_start)
    date_end_t = dateutil.parser.parse(date_end)
    date_range_idx = pd.date_range(date_start_t-pd.Timedelta(days=7), date_end_t,
                                   freq='W', normalize=True)
    date_range_idx = date_range_idx+pd.Timedelta(days=days)
    return group_date_range_by_week(date_range_idx)


def create_day_list(date_start: str, date_end: str):
    """
    | Given a date_start and date_end, creates a list of dictionaries
    
    .. code-block:: python

        >>> create_day_list('2020-09-01', '2020-09-07')
    

        [{'date_start': '2020-08-31', 'date_end': '2020-09-01'},
         {'date_start': '2020-09-01', 'date_end': '2020-09-02'},
         ...
         {'date_start': '2020-09-07', 'date_end': '2020-09-08'}]

    """
    date_start_t = dateutil.parser.parse(date_start)
    date_end_t = dateutil.parser.parse(date_end)
    date_range_idx = pd.date_range(date_start_t-pd.Timedelta(days=1), date_end_t,
                                   freq='D', normalize=True)

    return group_date_range_by_day(date_range_idx)


def round_date_to_week(x:"pd.Timestamp", week_start="SUN"):
    """
    | Example usage:

    .. code-block:: python

        df[f'{date_col}_w'] = df[date_col].apply(round_date_to_week)

    | Week starts on Sunday
    """
    day_shift = {"SAT": 2, "SUN": 1, "MON": 0}
    days = day_shift[week_start]
    if x:
        return (x - pd.Timedelta(days=x.dayofweek + days)).strftime("%Y-%m-%d")
    else:
        return None


def stringify_date(x:"pd.Timestamp"):
    """
    | Converts a column with ``Timestamp('2020-06-11 00:38:45+0000', tz='UTC')`` to ``'2020-06-11'``
    | Example usage: 

    .. code-block:: python

        df['date_col'] = df['date_col'].apply(stringify_date)
    """
    if x:
        return str(x).split(' ')[0]
    else:
        return None
