import pandas as pd, numpy as np
import glob, datetime, json, re, subprocess

keys = json.loads(open('keys.json').read())

# DATA IMPORTER
# ================================================================================
def import_dataframes():
    """Function that concatinates all data and returns the big df"""
    all_frames = []
    for date in get_existing_days():
        all_frames.append(pd.read_csv('data/alta_hr/'+date+".csv", index_col="time"))
    return pd.concat(all_frames)

# ================================================================================

# DATA UPDATER
# ================================================================================
def update_data_files():
    """Funtion that downloads the most recent csv files in the data directory"""
    for date in get_missing_days():
        get_dataframe(date).to_csv("data/alta_hr/"+date+".csv")
# ================================================================================


# DATA GATHERING FROM THE API
# ================================================================================
def get_data_from_server(date, data_type):
    """Calling subprocess to retrieve the data from fitbit api"""
    get = keys['API_URL'] # api base url
    if data_type == "heart":
        get += "activities/heart/date/"+date+"/1d/1sec.json"
    elif data_type == "sleep":
        get += "sleep/date/"+date+".json"

    output = subprocess.check_output(["curl","-i","-H", keys["AUTH"], get]).decode('ascii')
    
    return json_from_str(output) # return only json object output from the string data

def get_heart_rate_data(date):
    """Returns the dictionary of {time, heart_rate} for the given date"""
    times, heart_rates = [], []
    # get heart data from the data file
    data = get_data_from_server(date, "heart")
    for item in data['activities-heart-intraday']['dataset']:
        times.append(datetime_str_to_object(date+"T"+item['time']+".000"))
        heart_rates.append(item['value'])
            
    return {'time':times, 'heart_rate':heart_rates}

def get_dataframe(date):
    """Returns the df of time(index), heart_rate, sleep_stage, half_mins_passed"""
    # create pandas dataframe from json, resample 30 seconds and write mean(integer) of heart rates
    df = pd.DataFrame(get_heart_rate_data(date)).set_index('time').resample('30s').mean().fillna(0).astype(int)
    df['sleep_stage'] = np.nan # fill sleep_stages with nan values

    # get sleep data from the data file
    data = get_data_from_server(date, "sleep")
    for sleep in data['sleep']:
        if sleep['isMainSleep'] == True: # get the main sleep(night sleep, not naps)
            start_time = datetime_str_to_object(sleep['startTime'])# sleep start time
            end_time = datetime_str_to_object(sleep['endTime'])# sleep end time
            for item in sleep['levels']['data']:
                df.loc[datetime_str_to_object(item['dateTime']), 'sleep_stage'] = item['level']
        
    df = df.loc[start_time:end_time,].fillna(method='ffill')
    df['half_mins_passed'] = np.arange(len(df))
    
    return df[['half_mins_passed','heart_rate','sleep_stage']] # correct order


# HELPERS
# ================================================================================
def json_from_str(s):
    """Helper function to match json object from the string data"""
    match = re.findall(r"{.+[:,].+}|\[.+[,:].+\]", s)
    return json.loads(match[0]) if match else None

def datetime_str_to_object(fitbit_str):
    """Helper function to convert fitbit datetime str into python datetime object"""
    return datetime.datetime.strptime(fitbit_str, "%Y-%m-%dT%H:%M:%S.000")

def get_existing_days():
    """Helper function to get the existing dates from the data directory"""
    existing_days = []
    for i in glob.glob('data/alta_hr/*.csv'):
        existing_days.append(i[13:23]) # get existing days from the data
    return existing_days

def get_missing_days():
    """Helper function to get the missing dates from the data directory"""
    missing_days = []
    existing_days = get_existing_days()
    # sort and get the most recent date
    last_updated = datetime.datetime.strptime(sorted(existing_days, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))[-1], '%Y-%m-%d')
    # find the missing days till today
    for i in range((datetime.datetime.today()-last_updated).days):
        missing_days.append((datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
    return missing_days
