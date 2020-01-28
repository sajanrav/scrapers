'''
    Script to fetch Henry Hub Natural Gas Spot Prices
'''

import pandas as pd
import argparse as ag
from datetime import datetime, timedelta

URL = "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"

def day_num(x):
    '''
    Function to return day number given a
    day name abbr. for a week. 0 is Monday,
    4 is Friday.

    args:
    x(int): Day of week

    except:
    None

    returns:
    0/1/2/3/4(int): Day of week
    
    '''
    
    if x == 'Mon':
        return 0
    elif x == 'Tue':
        return 1
    elif x == 'Wed':
        return 2
    elif x == 'Thu':
        return 3
    elif x == 'Fri':
        return 4
    else:
        return 'Invalid day'

def gen_date(x, y):
    '''
    Function to add days to a given
    date

    args:
    x(datetime.datetime): First business day of week
    y(int): Day of week

    except:
    None

    returns:
    dt(datetime.datetime): Date for a day of week
    
    '''

    dt = x + timedelta(days=y)
    
    return dt

if __name__ == "__main__":
    all_data = pd.read_html(URL)
    tab_data = all_data[5]
    tab_data = tab_data.dropna(axis=0, how='all')
    tab_data['Week Of'] = tab_data['Week Of'].str.replace(r'to[\d|\D]+', '', regex=True).str.replace('- ', '-0')
    tab_data['Week Of'] = pd.to_datetime(tab_data['Week Of'], format='%Y %b-%d ')
    stacked_data = pd.melt(tab_data, id_vars=['Week Of'], var_name='Day Name', value_name='Price')
    stacked_data['Day Num'] = stacked_data['Day Name'].apply(lambda x: day_num(x))
    stacked_data = stacked_data.sort_values(['Week Of', 'Day Num'], ascending=True)
    stacked_data['Date'] = stacked_data.apply(lambda x: gen_date(x['Week Of'], x['Day Num']), axis=1)
    stacked_data = stacked_data[['Date', 'Price']]
    stacked_data = stacked_data.fillna('n/a')
    stacked_data.to_csv('henry_hub_daily_gas_prices.csv', index=False)
