'''
   Script to fetch data given a set of Sanskrit
   keywords
'''

import csv
import lxml
from urllib import request
from lxml import html
import argparse as ag

def dev_dhatu_list():
    '''
    Function to get list of all terms from website

    args:
    None

    except:
    None

    returns:
    dhatu_list(list): List of Sanskrit terms
    
    '''
    
    url = "http://sanskrit.uohyd.ac.in/scl/skt_gen/verb/verb_gen.html"
    response = request.urlopen(url).read()
    tree = html.fromstring(response)
    dhatu_raw_list = tree.xpath("//option/@value")
    dhatu_list = [ val.replace(" ","+") for val in dhatu_raw_list ]

    return dhatu_list

def write_karwari_file(dhatu_list):
    '''
    Function to fetch 'karwari' terms
    given a set of terms or 'dhatus' and
    write to file

    args:
    dhatu_list(list): List of terms or 'dhatus'

    except:
    None

    returns:
    None

    '''

    print("In Karwari function")

    url = "http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi?encoding=EX&prayoga=karwari&vb=" + dhatu_list[2]
    response = request.urlopen(url).read()
    tree = html.fromstring(response)
    verb_list = tree.xpath("//table//text()")

    f_out = open("out_karwari.txt","w")
    for val in verb_list:
        if val != "\n":
            val.encode('utf-8')
            f_out.write(val)
   
def write_karmani_file(dhatu_list):
    '''
    Function to fetch 'karmani' terms
    given a set of terms or 'dhatus' and
    write output to file

    args:
    dhatu_list(list): List of terms or 'dhatus'

    except:
    None

    returns:
    None

    '''

    print("In Karmani function")

    url = "http://sanskrit.uohyd.ac.in/cgi-bin/scl/skt_gen/verb/verb_gen.cgi?encoding=EX&prayoga=karmani&vb=" + dhatu_list[2]
    response = request.urlopen(url).read()
    tree = html.fromstring(response)
    verb_list = tree.xpath("//table//text()")

    f_out = open("out_karmani.txt","w")
    for val in verb_list:
        if val != "\n":
            val.encode('utf-8')
            f_out.write(val)
   
if __name__ == "__main__":
    parser = ag.ArgumentParser()
    parser.add_argument("type", help="karwari/karmani", type=str)
    args = parser.parse_args()
    data_type = args.type
    
    dhatu_list = []
    dhatu_list = dev_dhatu_list()
    if data_type == "karwari":
        write_kartari_file(dhatu_list)
    else:
        write_karmani_file(dhatu_list)
