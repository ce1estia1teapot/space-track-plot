import json
import ephem
import requests
import yaml
from matplotlib import pyplot as plt

from http.client import responses as response_codes
from typing import List, Dict, Any
from requests import Response
from requests.auth import HTTPBasicAuth

uriBase = "https://www.space-track.org"
requestLogin = "/ajaxauth/login"
requestCmdAction = "/basicspacedata/query"
requestGEO = "/class/gp_history/NORAD_CAT_ID/25544/orderby/NORAD_CAT_ID/limit/200/format/json"
requestFindStarlinks = "/class/tle_latest/NORAD_CAT_ID/>40000/ORDINAL/1/OBJECT_NAME/STARLINK~~/format/json/orderby/NORAD_CAT_ID%20asc"
requestOMMStarlink1 = "/class/omm/NORAD_CAT_ID/"
requestOMMStarlink2 = "/orderby/EPOCH%20asc/format/json"

m_data: Dict = {}

""" Retrieving Login Information """
with open('secret.json') as file:
    login_dict = json.load(file)

""" Opening Session, Logging in, querying data, closing session """
with requests.Session() as session:
    # Logging in...
    login_response: Response = session.post(uriBase + requestLogin, data=login_dict)

    if login_response.status_code != 200:
        raise Exception(login_response, "POST fail on login")

    # Querying Data...
    # starlink_response = session.get(uriBase + requestCmdAction + requestFindStarlinks)
    # print(f'Starlink Response:\n {starlink_response.text}')
    data_response: Response = session.get(f'{uriBase}{requestCmdAction}{requestGEO}')
    m_data.update(json.loads(data_response.text))
    print(m_data)

    if login_response.status_code != 200:
        raise Exception(data_response, "GET fail on data retrieval")

""" Calculating """
