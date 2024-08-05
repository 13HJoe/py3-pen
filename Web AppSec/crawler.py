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

subdomain_enumerate("wordlist.txt","google.com")
