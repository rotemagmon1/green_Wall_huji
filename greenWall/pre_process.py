import pandas as pd
import glob

# Ranges of all sensors without light
validation_ranges = {'RH': [0, 100], 'RH_2': [0, 100], 'T Soil Temp': [-30, 70], 'T Soil Volume': [0, 100],
                'T Soil Permitivity': [0, 100], 'TScon': [0, 100], 'TC_2': [-30, 70], 'Co2': [0, 1000],
                'T 2m': [-30, 70]}


def create_df(test=False):
    """
    create data frame from specific csv (for test) or from this folder: /cs/labs/gavish/green_wall/data/
    contains all daily CSV files of sensors data
    :return:
    """
    if test:
        df = pd.read_csv('data_sample.CSV', skiprows=6, delimiter=',', quotechar='"')
    else:
        # get all data from '/cs/labs/gavish/green_wall/data/'
        file_list = glob.glob('/cs/labs/gavish/green_wall/data/*.CSV')
        df_list = []
        for file in file_list:
            df_list.append(pd.read_csv(file, skiprows=6, delimiter=',', quotechar='"'))
        # Concatenate the data frames into a single data frame
        df = pd.concat(df_list)

    # remove blank columns
    unnamed_cols = [col for col in df.columns if "Unnamed" in col]  # get unnamed columns
    df = df.drop(columns=unnamed_cols)  # drop them
    df = df.dropna(axis=0, how='all')  # drop full null rows

    # edit Date and Hour columns
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%b/%Y %H:%M')
    df['Hour'] = df['Date'].dt.hour
    df['Date'] = df['Date'].dt.date
    # remove last day - serval minutes of the last day that are countered also
    last_date = df['Date'].max()
    df = df[df['Date'] != last_date]

    # ranges of sensors - if not in range or replace by means
    for col in validation_ranges.keys():
        col_mean = df[col].mean()
        min_range = validation_ranges[col][0]
        max_range = validation_ranges[col][1]
        df[col] = df[col].apply(lambda x: x if min_range <= x <= max_range else col_mean)

    return df
