from tqdm import tqdm
import ipaddress
from lib.otx import otx


if __name__ == "__main__":
    ip_list = [str(ip) for ip in ipaddress.IPv4Network("10.0.0.0/8")]
    results = [] 
    otxrequester = otx()
    ## Required Data ##
    # Malware - if it exists and roughly what 
    # HTTP scans - if available
    # Pulses - for adversaries
    #  
    ## current best: 32.51 secs for 100 requests -- means approx 11k requests an hour, greater than the 10k limit ## 
    ## TODO: we must go faster ##
    ## TODO: off load processing intelligently (e.g. not inline) ##
    
    for ip in tqdm(ip_list[0:10]):
        otxrequester.get_by_field(ip, otxrequester.allowedSections[0])

    print(otxrequester.fin())



