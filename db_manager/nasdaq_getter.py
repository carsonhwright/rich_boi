import nasdaqdatalink as ndl
import time
import datetime as dt


ndl.ApiConfig.api_key = \
ndl.read_key("C:\\Users\\User\\data\\.nasdaqkeyfile")

# get todays date
end_date = dt.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
# breakpoint()
mydata = ndl.get("WIKI/FB", start_date="2021-01-01", end_date=end_date)
breakpoint()

# sort of, data stops in 2019, could be used for historical analysis
###############################################################################
########################### PAYWALL DEADEND ###################################
###############################################################################