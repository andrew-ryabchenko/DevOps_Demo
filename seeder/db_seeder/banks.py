"""This module implements funcctions responsible for seeding the bank and the branch tables."""

import json
import random
import logging as log
import faker
import requests
from .cache import CACHE as cache
from .users import get_admin_auth_token
from .exceptions import APIError

def gen_bank() -> dict:
    """Generates a new mock bank data."""

    fake = faker.Faker()
    bank = {
        "routingNumber": fake.aba(),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zipcode": fake.postcode()
    }
    return bank

def gen_branch(bank_id: int):
    """Generates a new mock branch data."""

    fake = faker.Faker()

    #Not using faker phone number because it's not in the correct format
    phone = (f"({random.randint(100,999)}) "
            f"{random.randint(100,999)} "
            f"{random.randint(1000,9999)}")

    branch = {
        "name": fake.company(),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zipcode": fake.postcode(),
        "phone": phone,
        "bankID": bank_id
    }
    return branch

def add_bank(api_url: str, bearer: str, **kwargs) -> dict:
    """Sends the API call to the server to add a new bank.
    
    Returns: object containing response body."""

    payload = json.dumps(kwargs)

    headers = {'Content-Type': 'application/json',
               'Authorization': bearer}

    response = requests.post(api_url, headers=headers, data=payload, timeout=5)

    if response.status_code != 201:
        raise APIError(response)

    return response.json()

def add_branch(api_url: str, bearer: str, **kwargs) -> dict:
    """Sends the API call to the server to add a new branch.
    
    Returns: object containing response body."""

    payload = json.dumps(kwargs)

    headers = {'Content-Type': 'application/json',
               'Authorization': bearer}

    response = requests.post(api_url, headers=headers, data=payload, timeout=5)

    if response.status_code != 201:
        raise APIError(response)

    return response.json()
#pylint: disable=too-many-arguments
def add_banks_and_branches(banks_url: str, branches_url: str, login_url: str,
                           banks: int, branches_per_bank: int,
                           admin_uname: str, admin_pswd: str) -> None:
    """Generates random banks and branches data and initiates API calls
    to populate thee database."""
    bearer = get_admin_auth_token(login_url, admin_uname, admin_pswd)
    for _ in range(banks):
        bank = gen_bank()
        bank_id = add_bank(banks_url, bearer, **bank)["id"]
        cache["banks"].append(bank)
        for _ in range(branches_per_bank):
            branch = gen_branch(bank_id)
            branch = add_branch(branches_url, bearer, **branch)
            cache["branches"].append(branch)

def banks_and_branches_report(banks: int, branches: int) -> None:
    """Generates a report of the banks and branches added."""
    log.info("Added %s banks.", banks)
    log.info("Added %s branches.", branches)
