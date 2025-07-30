import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://dlc.lib.de.us/client/en_US/default/search/results"
params = {
    "qu": "everything is tuberculosis john green",
    "qf": "AUTHOR	Author	Green, John	Green, John",
    "te": "ERC_ST_DEFAULT"
}
headers = {
    "User-Agent": "GoodreadsLibraryChecker/1.0"
}

response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
print("Status:", response.status_code)
print("URL:", response.url)
print("Length of response:", len(response.text))