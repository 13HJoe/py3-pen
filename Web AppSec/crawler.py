import requests

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

    for subdomain in file_object:
        # strip the extra whitespace chars
        subdomain = subdomain.strip()
        url_build = subdomain + "." +target_base_url
        response = GET(url_build)
        if response:
            print("[+] ", url_build, " | ", response)

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

# subdomain_enumerate("wordlist.txt","google.com")
directory_enumeration("dir.txt","google.com")
