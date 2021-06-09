import pandas as pd


def create_costs_dict(df, id_cols):
    """
    Note:
        This function creates a dictionary from the passed DataFrame, specifically for cost-related DataFrames.

    Parameters:
        df: A DataFrame to be converted to a dictionary.\n
        id_cols: The identifying columns (args) from the DataFrame to use as keys for the returned dictionary.

    Return:
        A dictionary based on the passed DataFrame with keys consisting of id_cols plus Disc-Rate (added) and with id_cols removed.

    """
    dict_df = df.copy()
    # create some keys for the dict; 0 is added to the end of the key for the discount rate if discount rate is not already there
    if 'Disc-Rate' in dict_df.columns:
        if len(id_cols) == 3:
            keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], dict_df['Disc-Rate']))
        if len(id_cols) == 4:
            keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], dict_df[id_cols[3]], dict_df['Disc-Rate']))
        if len(id_cols) == 5:
            keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], dict_df[id_cols[3]],
                                 dict_df[id_cols[4]], dict_df['Disc-Rate']))
        dict_df.drop(columns=id_cols + ['Disc-Rate'], inplace=True)  # these can be put back in after converting back to df
    else:
        if len(id_cols) == 3:
            keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], [0] * len(dict_df)))
        if len(id_cols) == 4:
            keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], dict_df[id_cols[3]], [0] * len(dict_df)))
        if len(id_cols) == 5:
            keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], dict_df[id_cols[3]],
                                 dict_df[id_cols[4]], [0] * len(dict_df)))
        dict_df.drop(columns=id_cols, inplace=True) # these can be put back in after converting back to df
    dict_df.insert(0, 'key', keys)
    dict_df.set_index('key', inplace=True)
    return dict_df.to_dict('index')


def create_effects_dict(df, id_cols):
    """
    Note:
        This function creates a dictionary from the passed DataFrame, specifically for effects-related DataFrames.

    Parameters:
        df: A DataFrame to be converted to a dictionary.\n
        id_cols: The identifying columns (args) from the DataFrame to use as keys for the returned dictionary.

    Return:
        A dictionary based on the passed DataFrame with keys consisting of id_cols and with id_cols removed.

    """
    dict_df = df.copy()
    # create some keys for the dict
    if len(id_cols) == 4:
        keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], dict_df[id_cols[3]]))
    if len(id_cols) == 6:
        keys = pd.Series(zip(dict_df[id_cols[0]], dict_df[id_cols[1]], dict_df[id_cols[2]], dict_df[id_cols[3]],
                             dict_df[id_cols[4]], dict_df[id_cols[5]]))
    dict_df.drop(columns=id_cols, inplace=True)  # these can be put back in after converting back to df
    dict_df.insert(0, 'key', keys)
    dict_df.set_index('key', inplace=True)
    return dict_df.to_dict('index')


def convert_dict_to_df(dict_to_convert, *args):
    """
    Note:
        This function converts a dictionary to a DataFrame.

    Parameters:
        dict_to_convert: A dictionary meant for conversion to a DataFrame.\n
        args: The arguments to use as column names for the separated keys.

    Return:
        A DataFrame containing the passed dictionary of data with additional columns based on args.

    """
    # print('Converting dictionary to DataFrame.')
    df = pd.DataFrame(dict_to_convert).transpose()
    df.reset_index(inplace=True)
    for idx, arg in enumerate(args):
        df.rename(columns={f'level_{idx}': arg}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == '__main__':
    print('This module does not run as a script.')
