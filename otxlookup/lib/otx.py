import requests as req
import json, sys, os

class otx:
    def __init__(self, key=None, automarshall=False, callback=None, store=True, calldepth=3):
        if key is None: 
            self.key = automagic_key()
            if self.key == False: quit()
        else:
            self.key = key
        self.headers = {
            'X-OTX-API-KEY': self.key,
            'User-Agent': "Nunya Louise Recardio",
            'Content-Type': 'application/json'
        }
        self.allowedSections = ["general", "malware", "url_list", "reputation"]
        self.cyclicbuff = []
        self.automarshall = automarshall
        self.callback = callback
        self.storeage = []
        self.store = store
        self.calldepth = calldepth

    def get_cyclicBuff(self):
        return self.cyclicbuff
    
    def get_storage(self):
        return self.storeage
    
    def get_maxdepth(self):
        return self.calldepth
    
    def __del__(self):
        if len(self.cyclicbuff) > 0 and self.automarshall:
            if self.callback is not None:
                self.callback(self)
            else:
                print("no callback exiting without automarshalling done...", file=sys.stderr)
    

    def test(self):
        result = req.get("https://otx.alienvault.com/api/v1/users/me", headers=self.headers).status_code
        if result==200: return 0
        else: return result

    def get_by_field(self, ip, section):
        if section not in self.allowedSections: 
            print("Section selection not allowed! - please select from the available", file=sys.stderr)
            return -1
        requestURL = "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/{section}".format(ip=ip, section=section)
        fieldData = self.gen_call(requestURL)
        if self.store:
            self.storeage.append(fieldData)
        else:
            return fieldData 

    def gen_call(self, url):
        try:
            request = req.get(url, headers=self.headers)
            if request.status_code >= 200 and request.status_code < 300:
                return json.loads(request.content.decode('utf8'))
            elif request.status_code >= 500:
                newReq = cycReq(url)
                inB = inBuff(newReq, self.cyclicbuff)
                if inB == False:
                    self.cyclicbuff.append(newReq)
                else:
                    inB.inc()
            else:
                return -1
        except:
            print("major request error!", file=sys.stderr)
            return -1
    
    def fin(self):
        buff = self.cyclicbuff
        for v in buff:
            while v is not None:
                if v.get_count() >= self.calldepth:
                    v = None
                    continue
                else:  
                    self.gen_call(v.get_url())
                    v.inc()
        return self.storeage

class cycReq:
    def __init__(self, url):
        self.url = url
        self.count = 0
    
    def inc(self):
        self.count += 1
    
    def get_count(self):
        return self.count

    def get_url(self):
        return self.url

# idk how efficent this method is. Feels like a better datastructure would enable faster searching but ideally this buff doesnt get too big
def inBuff(cyc, buff):
    url = cyc.get_url()
    for c in buff:
        if c.get_url() == url:
            return c
    return False

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
            return False
    return apiKey

