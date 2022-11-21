import requests as req
import json

class otx:
    def __init__(self, key):
        self.key = key
        self.headers = {
            'X-OTX-API-KEY': self.key,
            'User-Agent': "Nunya Louise Recardio",
            'Content-Type': 'application/json'
        }
        self.allowedSections = ["general", "malware", "url_list", "reputation"]

    
    def test(self):
        result = req.get("https://otx.alienvault.com/api/v1/users/me", headers=self.headers).status_code
        if result==200: return 0
        else: return result

    def get_by_field(self, ip, section):
        requestURL = "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/{section}".format(ip=ip, section=section)
        try:
            request = req.get(requestURL, headers=self.headers)
            if request.status_code >= 200 and request.status_code < 300:
                return json.loads(request.content.decode('utf8'))
            else: print(request.status_code)
        except:
            print("error!")
