import requests as req
from tqdm import tqdm
import os, ipaddress, json, time
from lib.otx import otx

def automagic_key():
    if 'apikey.txt' in os.listdir():
        with open('apikey.txt', 'r') as f:
            apiKey = f.readlines()
        apiKey = apiKey[0]
    else:
        try:
            apiKey = os.environ['OTXKEY']
        except:
            print('Key doesnt exist in env var OTXKEY or on disk... address and re-run')
            quit()
    return apiKey


if __name__ == "__main__":
    ip_list = [str(ip) for ip in ipaddress.IPv4Network("164.97.0.0/16")]
    results = [] 
    otxrequester = otx(automagic_key())

    ## current best: 32.51 secs for 100 requests -- means approx 11k requests an hour, greater than the 10k limit ## 
    ## TODO: we must go faster ##
    ## TODO: off load processing intelligently (e.g. not inline) ##
    for ip in tqdm(ip_list[0:10]):
        resp = otxrequester.get_by_field(ip, otxrequester.allowedSections[0])
        results.append(resp['pulse_info']['count']) 




