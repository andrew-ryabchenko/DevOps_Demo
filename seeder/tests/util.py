"""This module implements utility functions that support various tests."""

import json
import requests
from db_seeder.cache import CACHE as cache
from db_seeder.accounts import get_accounts_num

def search_user(search: str, bearer: str, config: dict) -> int | None:
    """Searches for a user in the database.
    
    Returns the number of users found."""

    payload = json.dumps({
            "unpaged": "true",
            "pageNumber": 0,
            "pageSize": 1,
            "unsorted": "true",
            "offset": 0
    })
    headers = {"Authorization": bearer}
    endpoint = config["api_url"] + "/users"
    response = requests.get(endpoint, json=payload, params={"search": search},
                            headers=headers, timeout=5)

    if response.status_code == 200:
        return response.json()["numberOfElements"]

def confirm_users_added(bearer: str, config: dict) -> bool:
    """Confirms that the users have been added to the database."""
    for user in cache["users"]["member"]:
        found =  search_user(user["username"], bearer, config)
        if found == 0:
            return False

    for user in cache["users"]["admin"]:
        found =  search_user(user["username"], bearer, config)
        if found == 0:
            return False

    return True

def confirm_banks_and_branches_added(config: dict) -> bool:
    """Confirms that the banks and branches have been added to the database."""
    banks_added = len(cache["banks"])
    branches_added = len(cache["branches"])
    expected_banks_added = config["banks"]["count"]
    expected_branches_added = config["banks"]["branches_per_bank"] * expected_banks_added

    return banks_added == expected_banks_added and branches_added == expected_branches_added

def confirm_applicants_added(config: dict) -> bool:
    """Confirms that the applicants have been added to the database."""
    applicants_approved = len(cache["applicants"]["approved"])
    applicants_denied = len(cache["applicants"]["denied"])
    expected_applicants_approved = config["applicants"]["approved"]
    expected_applicants_denied = config["applicants"]["denied"]

    return (applicants_approved == expected_applicants_approved) and \
            (applicants_denied == expected_applicants_denied)

def confirm_transactions_added(api_url: str, bearer: str, txn_per_account: int) -> bool:
    """Confirms that the transactions have been added to the database."""
    accounts_num = get_accounts_num(bearer, api_url)
    return len(cache["transactions"]) == accounts_num * txn_per_account