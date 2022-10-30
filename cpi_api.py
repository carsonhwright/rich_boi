import requests
import json, re, time
import prettytable
import pandas as pd
import numpy as np

REQUEST_LIMIT = 25
DAILY_QUERY_LIMIT = 500

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

def get_api_constrained_batch_data(series_ids):
    """
    This will request batches of CPI series data, 25 (or whatever REQUEST_LIMIT) at a time. And
    will wait 10s between requests. This doesn't work exactly as I would like, because there also
    exists a 500 per day query limit. This will have to be accommodated for as well. See 
    get_daily_data().
    """
    headers = {'Content-type': 'application/json'}
    num_series_ids = len(series_ids)
    series_batch_list = []
    num_full_batches = int(num_series_ids / REQUEST_LIMIT)
    remainder = num_series_ids % REQUEST_LIMIT
    batch_index = 0
    for full_batch in range(num_full_batches):
        series_batch_list.append(series_ids[batch_index:(batch_index+REQUEST_LIMIT-1)])
        batch_index = batch_index + REQUEST_LIMIT
    series_batch_list.append(series_ids[len(series_ids)-remainder-1:])
    for series_batch in series_batch_list:
        data = json.dumps({"seriesid": series_batch,"startyear":"2011", "endyear":"2014"})
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
        json_data = json.loads(p.text)
        breakpoint()
        # THIS HAS NOT BEEN IMPLEMENTED YET, RIGHT NOW THIS ONLY PROVIDES THE IDS THAT THE API SHOULD BE
        # REQUESTING: the data variable will need to be changed or perhaps removed and the 'p' variable
        # perhaps should request all data and use the series ids to create new data sets individually
        # this will likely get huge
        try:
            for series in json_data['Results']['series']:
                x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
                seriesId = series['seriesID']
                for item in series['data']:
                    year = item['year']
                    period = item['period']
                    value = item['value']
                    footnotes=""
                    for footnote in item['footnotes']:
                        if footnote:
                            footnotes = footnotes + footnote['text'] + ','
                    if 'M01' <= period <= 'M12':
                        x.add_row([seriesId,year,period,value,footnotes[0:-1]])
                output = open(f'output/{seriesId}' + '.txt','w')
                output.write (x.get_string())
                output.close()
        except KeyError:
            print(f"[KeyError] Failed to parse series file in batch: {series_batch}")
            time.sleep(10)
            continue
        time.sleep(10)

def get_daily_data():
    """
    Dept. of Labor has a daily limit on how many requests I can make = DAILY_REQUEST_LIMIT, this 
    will need to manage that limit somehow. The database for this project will have to be local to
    some degree. Should use get_api_constrained batch data. 
    NOTE: Perhaps the series_id_table.csv should also have a column in it of when it was last
        updated and when each individual series was pulled.
    """

def pull_test_batch():
    test_series = ['CUSR0000SA0']
    # , 'CUSR0000SA0L12E4', 'CUSR0000SAC']
    get_api_pd_batch_data(test_series)
    # get_api_constrained_batch_data(test_series)

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

        start_year = str(series_general_df.iloc[np.where(series_general_df["series_id"] == series_id)]["begin_year"][0] + 40)
        # start_year = "2011"
        # end_year = "2014"
        series_id_list_obj = [series_id]
        end_year = str(series_general_df.iloc[np.where(series_general_df["series_id"] == series_id)]["end_year"][0])
        data = json.dumps({"seriesid": series_id_list_obj,"startyear": start_year, "endyear": end_year})

        # now similarly as I did with the batches of requests, I need to batch the number of years requested
        # in sets of 10

        # ThIs FuCkInG tHiNg OnLy TaKeS lIsTs!!!1!!!!1!one111!11!!11! for the seriesid in the data dict
        proc = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

        json_data = json.loads(proc.text)
        try:
            breakpoint()
            data = json_data["data"]
            for item in data: item["series_id"]=series_id
            df = pd.DataFrame(data=data)
            df.to_csv(f'output/{series_id}.csv', index=None)
        except KeyError:
            print(f"[KeyError] Failed to parse series file: {series_id}")
            time.sleep(5)
def main():
    series_ids = get_series_data_list()
    get_api_constrained_batch_data(series_ids)
