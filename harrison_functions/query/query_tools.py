import pandasql as ps


# Functions included in this file:
# # execute_query_on_df


def execute_query_on_df(query, dataframe,
                        index_name=None, index_list=None):
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
