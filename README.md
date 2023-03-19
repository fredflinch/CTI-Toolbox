# CTI-Toolbox
A collection of scripts to make common CTI tasks and enrinchments easier  

---

## asn2lookup
A tool to take an ASN and convert it to a full list of IPs, with pseudo geo-ip lookup function. Outputs as CSV by default.

`Usage: python asn2lookup.py --asn AS1234 --outfile "output.csv" (optional) --nogeo`

---

## otxlookup
Python libary wrapper for OTX that is faster for bulk OTX request processing. Has cyclic buffer resolution as error handling solution to increase speed on failed or timed out requests. 

On good network connections can reach 11k+ requests an hour, faster than the 10k rate limit. 

---

## prep4malware
Collection of functions to prep a win10 host for malware detonation. Designed to prep a Win10/WinServer VPS host or VM in under 5 minutes. 
Functions Supported Currently:
- Fast Wireshark, sysmon and 7-zip install 
- Low Priv User creation
- Log Collection


