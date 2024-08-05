import requests
import re

def GET(url):
    try:
        return requests.get("http://"+url)
        '''
        get_response = requests.get("http://"+url)
        headers = get_response.headers
        for pair in headers:
            print(pair,":",headers[pair])
        '''
    except requests.exceptions.ConnectionError:
        pass 

def subdomain_enumerate(wordlist,target_base_url):
    file_object = open(wordlist,'r')
    count = 1
    for subdomain in file_object:
        # strip the extra whitespace chars
        subdomain = subdomain.strip()
        url_build = subdomain + "." +target_base_url
        response = GET(url_build)
        if response:
            print("\n[+] ", url_build, " | ", response)
        print("\r[+] Requests sent ->", count, end='')
        count+=1
    file_object.close()

def directory_enumeration(wordlist, target_base_url):
    file_object = open(wordlist, 'r')
    count = 1
    for subdirectory in file_object:
        subdirectory = subdirectory.strip()
        url_build = target_base_url + "/" + subdirectory
        response = GET(url_build)
        if response.status_code != 404:
            print("\n[+] ", response.status_code ," ",url_build)
        print("\r[+] Requests sent ->", count, end='')
        count+=1
    file_object.close()

def extract_hrefs(url):
    response = GET(url)
    if not response:
        return None
    response = response.content
    href_links = re.findall('(?:href=")(.*?)"', response.decode('utf-8'))
    return href_links

def crawl_by_hrefs(url):
    refs = extract_hrefs(url)
    if not refs:
        return
    target_url_refs = set()
    for link in refs:
        if '#' in link:
            link = link.split("#")[0]
        if not link:
            continue
        if link[0] != 'h':
            link = "https://"+url+link
        if link not in target_url_refs:
            target_url_refs.add(link)
            print(link)
            crawl_by_hrefs(link)

 
#-------------------------MAIN----------------------------

# subdomain_enumerate("wordlist.txt","google.com")
# directory_enumeration("dir.txt","zsecurity.org")
crawl_by_hrefs("192.168.1.35/mutillidae")
