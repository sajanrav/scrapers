"""
 Script to scrape Year and Class data from USPTO
 website, for a given list of Patent Id's.

 Usage: python webscraper.py <directory> <input-patent-file> <output-scraped-file>
 where <directory>           : location of input and output files
       <input-patent-file>   : file with list of patent ids
       <output-scraped-file> : file with scraped data 

"""

import urllib.request
from lxml import html
import re
from datetime import datetime
import csv
import time
import os
import argparse as ag

def request_response(url):
    """
        Function to fetch response tree for a
        URL
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    resp_tree = html.fromstring(response.read())
    return resp_tree

def parse_data(resp_tree, val):
    """
        Function to extract year and class information
        from response obtained for a given patent id
    """
    
    try:
        data = resp_tree.xpath("//table//text()")
        data = [ val.replace('\n', '') for val in data ]
        data = [ val.strip() for val in data if val != '' or re.search(r'  +', val) is not None ]
        data = [ val for val in data if val != '' ]

        filed_year = ''
        class_text = ''
        classification = ''

        try:
            filed_date = data[data.index('Filed:')+1]
            date_ptr = datetime.strptime(filed_date, '%B %d, %Y')
            filed_year = str(date_ptr.year)
        except:
            print("Filed Date not found. Patent no. : {}".format(val))
            filed_year = ''

        idx_min = data.index('Current U.S. Class:')

        try:
            try:
                idx_max = data.index('Current CPC Class:')
            except:
                print("Patent No. : {}".format(val))
                print("Unable to find CPC Class")
                idx.max = data.index('Current International Class:')    
        except:
            print("Patent No. : {}".format(val))
            print("Unable to find class data")
            return filed_year, 'n/a'

        for val in range(idx_min+1, idx_max):
            text = data[val].replace(';', '').strip()
            class_text = class_text + ' ' + text

        class_vals = [ val.split('/')[0] for val in class_text[1:].split(' ') ]
        classification = '/'.join(class_vals)

        if filed_year == '':
            filed_year = 'n/a'

        if classification == '':
            classification = 'n/a'
    except:
        filed_year = 'n/a'
        classification = 'n/a'
            
    return filed_year, classification

def init_patent_list(PATENT_FILE):
    """
        Function to initialize a list using
        input patent id file
    """
    
    patent_list = []
    with open(PATENT_FILE, 'r') as f_in:
        reader = csv.reader(f_in)
        next(reader)
        for row in reader:
            patent_list.append(row[0])

    return patent_list

def get_patent_data(patent_list):
    """
        Function to generate a master list
        with patent id, year of filing and
        class
    """
    
    patent_details = []
    
    for val in patent_list:
        url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=1&f=G&l=50&co1=AND&d=PTXT&s1=" + str(val) + ".PN.&OS=PN/" + str(val) + "&RS=PN/" + str(val)
        resp_tree = request_response(url)
        filed_year, patent_class = parse_data(resp_tree, val)
        patent_details.append([val, filed_year, patent_class])
        time.sleep(1)
        
    return patent_details

def write_data_to_file(all_patent_data, OUTPUT_FILE):
    """
        Function to write final output
        to file
    """
    
    f_out = open(OUTPUT_FILE, 'w')
    headers = ['Patent Id', 'Year', 'Class']
    header_text = "\"" + '\",\"'.join(headers) + "\""
    f_out.write(header_text)
    f_out.write('\n')

    for val in all_patent_data:
        text_to_write = "\"" + val[0] + "\"," +\
                        "\"" + val[1] + "\"," +\
                        "\"" + val[2] + "\""
            
        f_out.write(text_to_write)
        f_out.write('\n')

    f_out.close()

if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('directory', help="Location of input and output file", type=str)
    parser.add_argument('inputfile', help="Name of input csv file with patent ids", type=str)
    parser.add_argument('outputfile', help="Name of output csv file to hold scraped data", type=str)
    args = parser.parse_args()

    DIR = args.directory
    PATENT_FILE = os.path.join(DIR, args.inputfile)
    OUTPUT_FILE = os.path.join(DIR, args.outputfile)
    
    patent_list = init_patent_list(PATENT_FILE)
    all_patent_data = get_patent_data(patent_list)
    write_data_to_file(all_patent_data, OUTPUT_FILE)    
    
