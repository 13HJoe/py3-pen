import requests
import re
from argparse import ArgumentParser
from collections import deque

def get_args():
    parser = ArgumentParser()
    parser.add_argument("-target",
                        dest="target_url",
                        required=True,
                        help="Target URL")
    parser.add_argument("-wsub",
                        dest = "domain_list",
                        help = "List of possible Subdomains")
    parser.add_argument("-wdir",
                        dest = "directory_list",
                        help = "List of possible subdirectories")
    return parser.parse_args()

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

    visited = set()
    queue = deque([url])
    # BREADTH-FIRST SEARCH GOING CRAZY 
    while queue:
        node = queue.popleft()
        refs = extract_hrefs(node)
        if not refs:
            continue
        for link in refs:
            if '#' in link:
                link = link.split("#")[0]
            if not link:
                continue
            if link[0] != 'h':
                if link[0]==".":
                    link = link[2:]
                link = "https://"+url+"/"+link                    
            
            if link not in visited:
                visited.add(link)
                if url not in link:
                    print("[-] External Link ->", link)
                    continue
                print("[+]",link)
                queue.append(link)
                
    print("[+] Finished Crawling")
            

def get_file_data(filename):
    try:
        f_obj = open(filename,'r')
        ret = []
        for word in f_obj.readlines():
            word = word.strip()
            ret.append(word)
        f_obj.close()
        return ret
    except FileNotFoundError:
        print("[-] Wordlist not found -> ",filename)

def run(url, subdomain_list, directory_list):
    
    #subdomain_enumerate(subdomain_list, url)
    #directory_enumeration(directory_list, url)
    crawl_by_hrefs(url)

#-------------------------MAIN----------------------------
def main():
    args = get_args()
    target_base_url = args.target_url
    subdomain_list, directory_list = [],[]

    if args.domain_list:
        val = get_file_data(args.domain_list)
        subdomain_list.append(val)

    if args.directory_list:
        val = get_file_data(args.directory_list)
        directory_list.append(val)
    
    run(target_base_url, subdomain_list, directory_list)
    exit(0)

if __name__ == "__main__":
    main()
