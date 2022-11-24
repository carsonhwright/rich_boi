import requests
import json, re, time
# import prettytable
import pandas as pd
import numpy as np

import data_interpreter.utilities as ut

REQUEST_LIMIT = 25
DAILY_QUERY_LIMIT = 500

"""
What should the purpose of this API be? just to construct the data set? If so, then this needs to
stop at writing CSVs
"""

def set_series_data():
    """"""
    series_table_filepath = "output/series_id_table.txt"
    headers = {'Content-type': 'application/json'}
    # data = json.dumps({"seriesid", "startyear", "endyear", "begin_period", "end_period"})
    out = requests.get('https://download.bls.gov/pub/time.series/cu/cu.series').content.decode('utf-8')
    out = out.replace('\n\n', '\n')
    out = out.replace('\r\n', '\n')
    out = out.replace('\t' , '|')
    out = re.sub('\s{2,}', '', out)
    with open(series_table_filepath, 'w') as f:
        f.write(out)
    read_file = pd.read_csv(series_table_filepath, on_bad_lines='skip', delimiter='|')
    read_file.to_csv("output/series_id_table.csv", index=None)

def get_series_data_pd():
    read_file = pd.read_csv("output/series_id_table.csv")
    return read_file["series_id"]

def get_series_data_list():
    series_data_list = []
    series_id_pd = get_series_data_pd()
    for id in series_id_pd:
        series_data_list.append(id)
    return series_data_list

def get_daily_data():
    """
    Dept. of Labor has a daily limit on how many requests I can make = DAILY_REQUEST_LIMIT, this 
    will need to manage that limit somehow. The database for this project will have to be local to
    some degree. Should use get_api_constrained batch data. 
    NOTE: Perhaps the series_id_table.csv should also have a column in it of when it was last
        updated and when each individual series was pulled.
    """

def pull_test_batch():
    test_series = ['CUSR0000SA0', 'CUSR0000SAC', 'CUSR0000SAH', 
        'CUSR0000SAM', 'CUSR0000SAN1D']
    get_api_pd_batch_data(test_series)

def get_api_pd_batch_data(series_ids):
    """
    This will request batches of CPI series data, 25 (or whatever REQUEST_LIMIT) at a time. And
    will wait 10s between requests. This doesn't work exactly as I would like, because there also
    exists a 500 per day query limit. This will have to be accommodated for as well. See 
    get_daily_data(). Also limits it to maximum time range is 10 years
    """
    headers = {'Content-type': 'application/json'}
    series_general_df = pd.read_csv("output\\series_id_table.csv")
    
    for series_id in series_ids:

        # start_year = str(series_general_df.iloc[np.where(series_general_df["series_id"] == series_id)]["begin_year"][0] + 40)
        # start_year = "2011"
        # end_year = "2014"
        series_id_list_obj = [series_id]
        try:
            end_year = str(series_general_df.iloc[np.where(series_general_df["series_id"] == series_id)]["end_year"].values[0])
        except KeyError:
            breakpoint()
        start_year = str(int(end_year) - 10)
        data = json.dumps({"seriesid": series_id_list_obj,"startyear": start_year, "endyear": end_year})

        # now similarly as I did with the batches of requests, I need to batch the number of years requested
        # in sets of 10

        # ThIs FuCkInG tHiNg OnLy TaKeS lIsTs!!!1!!!!1!one111!11!!11! for the seriesid in the data dict
        proc = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

        json_data = json.loads(proc.text)
        try:
            data = json_data["Results"]["series"][0]["data"]
            for item in data: item["series_id"]=series_id
            df = pd.DataFrame(data=data)
            df.to_csv(f'output/{series_id}.csv', index=None)
        except KeyError:
            print(f"[KeyError] Failed to parse series file: {series_id}")
            time.sleep(5)
def main():
    series_ids = get_series_data_list()
    get_api_constrained_batch_data(series_ids)
