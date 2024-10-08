"""This module contains the functions to get the accounts information from the database."""

import requests
from .exceptions import APIError

def get_accounts_num(bearer: str, api_url: str) -> int:
    """Gets the number of accounts in the system."""

    headers = {
        'Authorization': bearer
    }
    response = requests.request("GET", api_url, headers=headers, timeout=5)

    if response.status_code != 200:
        raise APIError(response)

    return response.json()["totalElements"]

def get_accounts(bearer: str, api_url: str, num: int) -> list[dict]:
    """Gets the list of 'num' accounts in the system."""

    accounts = []

    headers = {
        'Authorization': bearer
    }
    retrieved = 0
    i = 1
    while retrieved < num:
        response = requests.request("GET", api_url + f"/{i}", headers=headers, timeout=5)
        if response.status_code == 200:
            accounts.append(response.json())
            retrieved += 1
            i += 1

    return accounts
