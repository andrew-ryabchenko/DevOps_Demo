"""This module implements functions that peerform tasks reelated to applicants and applications."""

import logging as log
import random
import json
import faker
import requests
from .exceptions import APIError
from .cache import CACHE as cache

def add_application(api_url: str, **kwargs) -> dict:
    """Sends the API call to the server to add an applicant.
    
    Returns: object containing response body."""

    payload = json.dumps(kwargs)
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", api_url, headers=headers, data=payload, timeout=5)

    if response.status_code != 201:
        raise APIError(response)

    return response.json()

def gen_applicant(approved=True) -> dict:
    """Generates a new mock applicant data."""

    fake = faker.Faker()
    fname = fake.first_name()
    lname = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=100).strftime("%Y-%m-%d")
    #Not using faker phone number because it's not in the correct format
    phone = (f"({random.randint(100,999)}) "
            f"{random.randint(100,999)} "
            f"{random.randint(1000,9999)}")
    address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zipcode = fake.postalcode()
    income = random.randint(1_500_000,10_000_000) if approved else random.randint(1_000, 10_000)

    applicant = {
        "firstName": fname,
        "lastName": lname,
        "dateOfBirth": dob,
        "gender": "MALE",
        "email": fake.ascii_email(),
        "phone": phone,
        "socialSecurity": fake.ssn(),
        "driversLicense": str(random.randint(100000000,999999999)),
        "income": income,
        "address": address,
        "city": city,
        "state": state,
        "zipcode": zipcode,
        "mailingAddress": address,
        "mailingCity": city,
        "mailingState": state,
        "mailingZipcode": zipcode
    }

    return applicant

def applicant_report(approved: int, denied: int) -> None:
    """Generates a report of the applicants added."""
    log.info("Added %s approved applicants.", approved)
    log.info("Added %s denied applicants.", denied)

def add_applications(api_url, approved, denied) -> None:
    """Makes the complete application payloads and initiates API calls
    to add the applicants and applications to the database."""
    account_type = random.choice(["CHECKING", "SAVINGS"])
    payload = {
        "applicationType": account_type,
        "noNewApplicants": False,
        "applicantIds": [],
        "applicants": [],
        "applicationAmount": 1000,
        "cardOfferId": 0,
        "depositAccountNumber": "string"
    }

    #Add approved applications
    for _ in range(approved):
        applicant = gen_applicant(approved=True)
        payload["applicants"] = [applicant]
        response = add_application(api_url, **payload)
        cache["applicants"]["approved"].append(response)

    #Add declined applications
    for _ in range(denied):
        applicant = gen_applicant(approved=False)
        payload["applicants"] = [applicant]
        response = add_application(api_url, **payload)
        cache["applicants"]["denied"].append(response)
