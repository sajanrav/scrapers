'''
    Script to fetch documents from Mendocino County website

    Usage : python get_mendocino_county_documents.py <Output Directory> <Number of documents>
    Help  : python get_mendocino_county_documents.py -h
    
'''

import urllib.request
import os
import time
import argparse as ag

if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument('dir', help="Output Directory", type=str)
    parser.add_argument('numdocs', help="No. of documents", type=int)
    args = parser.parse_args()

    out_dir = args.dir
    num_docs = args.num_docs
    
    for ind in range(10, num_docs*2, 2):
        file_name = str(ind) + ".pdf"
        try:
            url = "https://www.mendocinocounty.org/home/showdocument?id=" + str(ind)
            print("Download file from URL : {}".format(url))
            urllib.request.urlretrieve(url, file_name)
            time.sleep(1)
        except:
            print("No file present at URL : {}".format(url))
            time.sleep(1)
            continue
