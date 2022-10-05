import csv
import re
import ipaddress
from tqdm import tqdm
import requests
import json
import pandas as pd
import requests as req
import argparse

def get_by_ASN(ans):
    print("collecting IP ranges...")
    ipranges = []
    try:
        ripe_url = "https://stat.ripe.net/data/as-routing-consistency/data.json?resource="+ans
        asn_data = req.get(ripe_url).json()
        for prefixes in asn_data['data']['prefixes']:
            ipranges.append(prefixes['prefix'])
        return ipranges
    except:
        print("[!] ASN fetch error [!]")
        return

def get_geo(ip_list):
    try:
        geo_data1 = json.loads(((requests.get('https://geolocation-db.com/jsonp/{}'.format(ip_list[1])).content.decode()).split("(")[1].strip(")")))
        geo_data2 = json.loads(((requests.get('https://geolocation-db.com/jsonp/{}'.format(ip_list[int(len(ip_list)/2)])).content.decode()).split("(")[1].strip(")")))
    except:
        return "Failed"
    if geo_data1['country_code'] == geo_data2['country_code']:
        return geo_data1['country_code']
    elif geo_data1['country_code'] == 'Not found' and geo_data2['country_code'] == 'Not found':
        return 'None'
    elif geo_data1['country_code'] == 'Not found' and geo_data2['country_code'] != 'Not found':
        return geo_data2['country_code']
    elif geo_data1['country_code'] != 'Not found' and geo_data2['country_code'] == 'Not found':
        return geo_data1['country_code']
    else:
        return 'Mixed'

def expand(rangeList, asn, geoflag):
    print("beginning expansion of cidr ranges...")
    asn_list = []
    for ipRange in tqdm(rangeList):
        if re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}', ipRange):
            ip_list = [str(ip) for ip in ipaddress.IPv4Network(ipRange)]
            if geoflag:
                country = get_geo(ip_list)
                asn_list.append(list(zip(ip_list, [country]*len(ip_list), [asn]*len(ip_list))))
            else:
                asn_list.append(list(zip(ip_list, [asn]*len(ip_list))))
    return [item for sublist in asn_list for item in sublist]

def saveout(ofile, data, geoflag):
    print("saving...")
    with open(ofile,'w', newline='') as out:
        csv_out=csv.writer(out)
        if geoflag:
            csv_out.writerow(['IP','Country', "ASN"])
        else:
            csv_out.writerow(['IP', "ASN"])
        for row in tqdm(data):
            csv_out.writerow(row)                


if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-a", "--asn", help="ASN to lookup - in the form AS####")
    p.add_argument("-o", "--outfile", help="Write the output to the file")
    p.add_argument("--nogeo", help="exclude geo IP lookups, speeds up process considerably", action='store_false')
    args = p.parse_args()
    if args.nogeo: geoflag = True
    else: geoflag = False

    if args.asn is not None and args.outfile is not None:
        saveout(args.outfile, expand(get_by_ASN(args.asn), args.asn, geoflag), geoflag)
    else:
        print("Please provide required arguments...")

