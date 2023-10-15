import requests as req
import argparse 
import re 


def get_links(base):
    collect_re = r'<a href=(\"|\')(?P<link>([^\"]*|[^\']*))\">'
    reg = re.compile(collect_re)
    r = req.get(base)
    if r.status_code < 400: content = (r.content).decode('utf-8')
    
    links = [m['link'] for m in reg.finditer(content)]

    for link in links:
        if link == "/"+"/".join(base.split("/")[3:-2])+"/": continue 
        if (link[-1] == "/") and (link not in dirs):
            r = req.get(base+link) 
            if r.status_code < 400:
                dirs.append(link)
                get_links(base+link)
        else:
            if link[0] == "?": continue
            extc = link.split(".")
            if len(extc) > 1:
                ext = extc[-1]
                if not ext in filter_ext:
                    items.append(base+link)
            else: items.append(base+link)

dirs = []
items = []
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-u", "--url", help="url to index page - will traverse")
    p.add_argument("-f", "--filter", help="perform custom filtering of specific types by name (comma sep list)")
    p.add_argument('-a', "--all", action='store_true', help="Switch argument - if used no filtering of output will be performed")

    args = p.parse_args()

    if args.filter is not None:
        filter_ext = [m.strip(" ") for m in (args.filter).split(",")] 
    elif args.all == False: filter_ext = []
    else: filter_ext = ["jpg", "jpeg", "gif", "webp", "png", "js", "css", "mp4"]
    get_links(args.url)
    
    for i in items:
        print(i)