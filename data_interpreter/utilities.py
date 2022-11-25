import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import datetime, calendar

def get_df(series_id):
    filename = Path(f"output/{series_id}.csv")
    df = pd.read_csv(filename)
    return df

def basic_plot(df):
    df2 = pd.DataFrame(df, columns=['datetime', 'value'])
    plt.plot(df2["datetime"], df2["value"])
    plt.show()

def set_datetime_df(df):
    month_names = calendar.month_name[:]
    df["datetime"] = df.apply(
        lambda row: datetime.datetime(year=row["year"], month=month_names.index(row["periodName"]),day=1), 
        axis=1
        )
    return df

def get_df_from_list(series_list):
    series_dict = {}
    for series_id in series_list:
        filename = Path(f"output/{series_id}.csv")
        series_dict[series_id] = pd.read_csv(filename)
    return series_dict

""" I don't know if the following is necessary, retaining for now"""
# def overwrite_series_from_df(df):
#     with open()

def main():
    """ Only retaining for dbugging purposes"""
    test_series = ['CUSR0000SA0', 'CUSR0000SAC', 'CUSR0000SAH', 
        'CUSR0000SAM', 'CUSR0000SAN1D']
    series_dict = get_df_from_list(test_series)
    series_example = series_dict["CUSR0000SA0"]
    date_time_df = set_datetime_df(series_example)
    basic_plot(series_example)