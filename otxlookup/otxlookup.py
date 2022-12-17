from tqdm import tqdm
import ipaddress, time
from lib.otx import otx
import pandas as pd
import re, sys,argparse
## Required Data ##
# Malware - if it exists and roughly what 
# HTTP scans - if available
# Pulses - for adversaries
#
# all = ['whois', 'reputation', 'indicator', 'type', 'type_title', 'base_indicator', 'pulse_info', 'false_positive', 'validation', 'asn', 'city_data', 'city', 'region', 'continent_code', 'country_code3', 'country_code2', 'subdivision', 'latitude', 'postal_code', 'longitude', 'accuracy_radius', 'country_code', 'country_name', 'dma_code', 'charset', 'area_code', 'flag_url', 'flag_title', 'sections']
# mal = ['data', 'size', 'count']
# url = ['url_list', 'page_num', 'limit', 'paged', 'has_next', 'full_size', 'actual_size']
# rep = ['reputation']

def process(data, mode):
    if mode == "all":
        for otxret in data:
            print(otxret['reputation'])
        pass
    elif "mal" in mode:
        pass
    elif mode == "url":
        pass
    elif "rep" in mode:
        pass
    else:
        print("Unsupported mode - please select from all, mal, url, rep", file=sys.stderr)
        return -1

def read_ips_from_txt(fpath):
    iplst=[]    
    with open(fpath, 'r') as f:
        iplst.append(f.readlines())
    return iplst

def read_ips_from_csv(fpath, colname='IPs'):
    ip_df = pd.read_csv(fpath)
    return ip_df[colname].tolist()

def is_cidr(ipStr):
    if re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}', ipStr):
        return  [str(ip) for ip in ipaddress.IPv4Network(ipStr)]
    else:
        return [ipStr]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--infile", help="Path to ipfile\nSupported modes: txt, csv")
    p.add_argument("--ip", help="Single ip or subnet to scan")
    p.add_argument("-o", "--outfile", help="Write the output to the file\nSupported modes: csv")
    p.add_argument("-m", "--mode", help="Lookup modes available: ")
    args = p.parse_args()

    otxrequester = otx()

    ## current best: 32.51 secs for 100 requests -- means approx 11k requests an hour, greater than the 10k limit ## 
    ## TODO: we must go faster ##
    ## TODO: off load processing intelligently (e.g. not inline) ## 
    
    otxrequester.get_by_field(args.ip, otxrequester.allowedSections[0])
    process(otxrequester.fin(), "all")




