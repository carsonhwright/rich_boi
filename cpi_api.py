import requests
import json, re
import prettytable
import pandas as pd
def get_series_ids():
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
    return read_file["series_id"]

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CUUR0000SA0','SUUR0000SA0'],"startyear":"2011", "endyear":"2014"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
# THIS HAS NOT BEEN IMPLEMENTED YET, RIGHT NOW THIS ONLY PROVIDES THE IDS THAT THE API SHOULD BE
# REQUESTING: the data variable will need to be changed or perhaps removed and the 'p' variable
# perhaps should request all data and use the series ids to create new data sets individually
# this will likely get hug
gork = get_series_ids()
breakpoint()
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
