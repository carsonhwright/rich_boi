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
    df2 = pd.DataFrame(df, columns=['year', 'periodName'])

    for i in df2.values:
        breakpoint()
        i["datetime"] = datetime.datetime(str(i["year"].values[0]), str(i["periodName"].values[0]))
    df.plot()

def set_datetime_df(df):
    month_names = calendar.month_name[:]
    breakpoint()
    df["datetime"] = datetime.datetime(df["year"], month_names.index(df["periodName"]))
    # THIS DOESN'T WORK YET, SEE:
    # https://towardsdatascience.com/create-new-column-based-on-other-columns-pandas-5586d87de73d#:~:text=98%20False%2098.1-,Using%20apply()%20method,method%20should%20do%20the%20trick.

def main():
    df = get_df('CUSR0000SA0')
    set_datetime_df(df)
    breakpoint()
    basic_plot(df)