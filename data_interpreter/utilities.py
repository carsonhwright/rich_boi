import matplotlib.pyplot as plt
import matplotlib.dates as mtdate
import pandas as pd
import numpy as np
from pathlib import Path
import datetime, calendar

OUTPUT_PATH = "output"

def basic_plot(df):
    df2 = pd.DataFrame(df, columns=['datetime', 'value'])
    plt.plot(df2["datetime"], df2["value"])
    plt.show()

def set_datetime_df(df):
    """
    This does the same thing that the CpiPlotter does, maybe a little
    cleaner, in any case something needs to be done with these two
    """
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

class CpiPlotter():
    """
    This takes a single series ID which correlates to an already
    existant <series_id>.csv in OUTPUT_PATH, constructs a 
    DataFrame, adds a datetime column, and makes a 
    <series_id>.png in the OUTPUT_PATH

    Parameter
    ---------
    series_ID: str
        example: CUSR0000SA0
    """

    def __init__(self, series_ID:str):
        self.series_id = series_ID
        self.df = self.get_df(self.series_id)
        self.set_datetime_df(self.df)
        self.basic_plot(self.df)

    def get_df(self, series_id):
        filename = Path(f"output/{series_id}.csv")
        df = pd.read_csv(filename)
        return df

    def basic_plot(self, df):
        df2 = pd.DataFrame(
            df.loc[::-1].reset_index(drop=True), 
            columns=['datetime', 'value']
            )
        plt.figure()
        df2["value"].plot()
        plt.xticks(df2.index)
        plt.savefig(
            f"{OUTPUT_PATH}\\{self.series_id}.png"
            )

    def set_datetime_df(self, df):
        month_names = calendar.month_name[:]
        df["datetime"] = pd.to_datetime(
            df["year"].astype(str) 
            + df["period"].str.replace("M", ""),
            format="%Y%m"
            )
