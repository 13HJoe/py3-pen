import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
    
def get_response(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass
    
url = "http://192.168.1.34/mutillidae/index.php?page=dns-lookup.php"
response = get_response(url)
response = response.content

# BS allows for the extraction of HTML elements and tags from the pages
parsed_html = BeautifulSoup(response)
# to get elements from parser HTML 
forms_list = parsed_html.findAll("form")

print("\n\n\n")
for form in forms_list:
    # to get attributes from elements
    action = form.get("action")
    post_url = urljoin(url,action)
    method = form.get("method")


    data_dict = {}
    # find input elements
    inputs_list = form.findAll("input")
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value") # default set to button placeholder
        if input_type == "text":
            input_value = "test"
        data_dict[input_name] = input_value
    
    result = requests.post(post_url, data=data_dict)
    print(result.content.decode('utf-8'))
