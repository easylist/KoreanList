import requests
import re
import urllib3

def readSourceFromABPFilters(url, target):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = response.data.decode('utf-8')

    target= target.replace("http://", "")
    target= target.replace("https://", "")

    number_of_domain= extract_number(target)
    _pattern= target.replace(str(number_of_domain), "\d{1,3}")

    for line in data.splitlines():
        searched= re.search(_pattern, line)
        # found a domain
        if(searched):
            substringed= line[searched.start():searched.end()]
            extracted= extract_number(substringed)
            # number of the written filter is old.
            if(extracted < number_of_domain):
                renewed_filter= line.replace(str(extracted), str(number_of_domain))
                print("Filter update suggestion: " + line + " --> " + renewed_filter)
    print("")

def extract_number(url):
    parsed_int_list= re.findall("\d+", url)
    if len(parsed_int_list) == 0:
        raise Exception("no any digits in url")
    parsed_int= int(parsed_int_list[0])
    return parsed_int

def url_ok(url):
    if "http" not in url:
        url = "https://"+ url

    working_domains= []
    parsed_int= extract_number(url)
    found_domain_works= False
    which_number_latest_works = 0
    i= parsed_int-1

    while True:
        if found_domain_works and i > parsed_int+1 and not which_number_latest_works == i-1:
            break
        try:
            replaced= url.replace(str(parsed_int), str(i))
            r = requests.head(replaced)
            if r.status_code != 200:
                print(replaced + ": status("+r.status_code+")")
            else:
                print(replaced+": working great")
                found_domain_works= True
                which_number_latest_works= i
                working_domains.append(replaced)
            i=i+1
        except Exception:
            print(replaced+": not working")
            i=i+1
            continue
    return working_domains

file1 = open('domain_checklist.txt', 'r') 
Lines = file1.readlines() 
count = 0 
for line in Lines: 
    if(line.startswith("#")): # ignore comments
        continue

    working_domains= url_ok(line.strip())
    for domain in working_domains:
        readSourceFromABPFilters("https://easylist-downloads.adblockplus.org/koreanlist+easylist.txt", domain)
