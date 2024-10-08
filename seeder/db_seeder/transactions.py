"""This module contains functions responsible for seeding the transactions table."""
import json
import random
import logging as log
import requests
from faker import Faker
from .accounts import get_accounts, get_accounts_num
from .users import get_admin_auth_token
from .exceptions import APIError
from .cache import CACHE as cache

def add_transaction(api_url: str, payload: dict) -> None:
    """Posts a transaction to the database."""

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", api_url, headers=headers,
                                data=json.dumps(payload), timeout=5)

    if response.status_code != 200:
        raise APIError(response)

    return response.json()

def add_transactions(transactions_url: str, accounts_url: str,
                     login_url: str, txn_per_account: int,
                     admin_uname: str, admin_pswd: str) -> None:
    """Posts mock transactions to the database."""
    #Get admin auth token
    bearer = get_admin_auth_token(login_url, admin_uname, admin_pswd)
    #Get number of existing accounts
    num_accounts = get_accounts_num(bearer, accounts_url)
    #Get existing accounts
    accounts = get_accounts(bearer, accounts_url, num_accounts)

    fake = Faker()

    for account in accounts:
        for _ in range(1, txn_per_account+1):
            payload = {
                    "type": random.choice(["WITHDRAWAL", "DEPOSIT"]),
                    "method": "ACH",
                    "date": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
                    "amount": random.randint(10000, 100000),
                    "merchantCode": "ALINE",
                    "merchantName": fake.company(),
                    "description": "string",
                    "accountNumber": account["accountNumber"],
                    "hold": "true"
                    }
            response = add_transaction(transactions_url, payload)
            cache["transactions"].append(response)

def transaction_report(transactions: list[dict]) -> None:
    """Generates a report of the transactions added."""
    approved = 0
    denied = 0
    for transaction in transactions:
        if transaction["status"] == "APPROVED":
            approved += 1
        else:
            denied += 1

    log.info("Added %s approved transactions.", approved)
    log.info("Added %s denied transactions.", denied)
