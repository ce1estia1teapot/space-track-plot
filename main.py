import requests
import matplotlib

from http.client import responses as response_codes
from typing import List, Dict, Any
from requests import Response, session
from requests.auth import HTTPBasicAuth

auth_url: str = 'https://www.space-track.org/ajaxauth/login'

good_url: str = 'https://www.space-track.org/basicspacedata/query/class/satcat/\
PERIOD/1430--1450/CURRENT/Y/DECAY/null-val/orderby/NORAD_CAT_ID/format/json'

test_url: str = 'https://www.space-track.org/basicspacedata/query/class/gp/\
NORAD_CAT_ID/36000,36001--36004, ~~36005,^3600,36010/orderby/NORAD_CAT_ID/format/json'

# Retrieving Login Information
raw_dict: Dict[str, str] = {}
with open('secret.txt', mode='r') as file:
    for line in file:
        name, val = line.partition('=')[::2]
        raw_dict[name] = val

username = raw_dict['username']
password = raw_dict['password']
login_dict: Dict[str, str] = {'identity': username, 'password': password}

# Opening Session, Logging in, querying data, closing session
with requests.Session() as session:
    login_response = session.post(url=auth_url, data=login_dict)
    print(f'Login Response: {login_response.status_code} ({response_codes[login_response.status_code]})')

    data_response: Response = session.get(url=test_url)
    print(data_response.text)

    session.close()
