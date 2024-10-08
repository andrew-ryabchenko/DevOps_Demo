"""This module implements functions pereform tasks related to users in the database."""
#pylint: disable=duplicate-code
import random
import json
import logging as log
import faker
import requests
from .cache import CACHE as cache, CONFIG as config
from .exceptions import APIError

def add_admin_user(api_url: str, **kwargs) -> dict:
    """Sends the API call to the server to add new admin user.
    
    Returns: object containing the response body."""
    payload = json.dumps(kwargs)
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, timeout=5)

    if response.status_code != 201:
        raise APIError(response)

    return kwargs

def add_user(api_url, **kwargs) -> dict:
    """Sends the API call to the server to add new user.
    
    Returns: object containing the response body."""
    payload = json.dumps(kwargs)
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, timeout=5)

    #This particular request always fails with a 422 status code.
    #However, it still adds the user to the system.
    if response.status_code != 422:
        raise APIError(response)

    return kwargs

def gen_user_admin() -> dict:
    """Generates payload data for a new admin user."""

    fake = faker.Faker()

    fname = fake.first_name()
    lname = fake.last_name()
    #Not using faker phone number because it's not in the correct format
    phone = (f"({random.randint(100,999)}) "
             f"{random.randint(100,999)} "
             f"{random.randint(1000,9999)}")

    payload = {
        "firstName": fname,
        "lastName": lname,
        "email": fake.ascii_email(),
        "phone": phone,
        "username": fname + "." + lname,
        "password": config["users"]["password"],
        "role": "admin"
    }

    return payload

def gen_user_member(membership_id: str, last_four_ssn: str, fname: str, lname: str) -> dict:
    """Generates payload data for a new member user."""

    payload = {
        "lastFourOfSSN": last_four_ssn,
        "membershipId": membership_id,
        "username": fname + "." + lname,
        "password": config["users"]["password"],
        "role": "member"
    }

    return payload

def add_users(api_url: str) -> None:
    """Adds new member users to the system."""

    for approved_member in cache["applicants"]["approved"]:
        membership_id = approved_member["createdMembers"][0]["membershipId"]
        last_four_ssn = approved_member["applicants"][0]["socialSecurity"][-4:]
        fname = approved_member["applicants"][0]["firstName"]
        lname = approved_member["applicants"][0]["lastName"]
        user = gen_user_member(membership_id, last_four_ssn, fname, lname)
        response = add_user(api_url, **user)
        cache["users"]["member"].append(response)

def user_report(members, admins) -> None:
    """Generates a report of the users added."""
    log.info("Added %s member users.", len(members))
    for member in members:
        log.info("Username: %s, Password: %s, Role: member.",
                 member['username'], config['users']['password'])

    log.info("Added %s admin users.", len(admins))
    for admin in admins:
        log.info("Username: %s, Password: %s, Role: admin.",
                 admin['username'], config['users']['password'])

def get_admin_auth_token(api_url: str, username: str, password: str) -> str:
    """Gets the authentication token for the admin user."""

    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, timeout=5)

    if response.status_code != 200:
        raise APIError(response)

    return response.headers["Authorization"]
