'''
   Script to download BMC Dashboard file
   
   TODO: Set variable for output directory 
   
'''

import urllib.request as ur
from datetime import datetime
import pdf_parser_utils as utils

BASE_URL = "http://stopcoronavirus.mcgm.gov.in/assets/docs/Dashboard.pdf"

def download_file():
    '''
    Function to download BMC COVID War Room
    dashboard file

    args:
    None

    except:
    None

    returns:
    out_file(str): Output file name

    '''
    
    dt_download = datetime.today()
    file_date = datetime.strftime(dt_download, '%Y%m%d')
    out_file = "bmc_war_room_dashboard_" + file_date + ".pdf"
    ur.urlretrieve(BASE_URL, out_file)

    return out_file 

if __name__ == "__main__":
    out_file = download_file()
    
