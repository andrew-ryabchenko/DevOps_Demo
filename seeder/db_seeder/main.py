"""This module is the entry point of the application. It defines main()
function that implements the high-level logic of the application."""
#pylint: disable=too-many-return-statements disable=too-many-locals
import json
import sys
import logging as log
#pylint: disable=import-error
from yaml import load, scanner
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from .exceptions import ConfigurationError, APIError
from .applicants import add_applications, applicant_report
from .users import add_users, user_report, gen_user_admin, add_admin_user
from .banks import add_banks_and_branches, banks_and_branches_report
from .transactions import add_transactions, transaction_report
from .cache import CACHE as cache, CONFIG as config
#pylint: disable=redefined-outer-name
def parse_config() -> tuple[dict, int]:
    """Parses the configuration file and replaces default configuration with user-defined values.
    
    Returns: the configuration object based on the config file or the default configuration object
    if the config file is malformed."""
    user_conf = None
    try:
        with open('config.yaml', "r", encoding="utf-8") as conf_file:
            user_conf = load(conf_file, Loader)
            match user_conf:
                case {"api_url": _,
                      "applicants": {"approved": _, "denied": _},
                      "users": {"password": _},
                      "banks": {"count": _, "branches_per_bank": _},
                      "transactions": {"txn_per_account": _},
                      "admin_username": _,
                      "admin_password": _
                      }:
                    return user_conf
                case _:
                    raise ConfigurationError("Malformed configuration file")

    except FileNotFoundError:
        log.warning("Configuration file config.yaml not found. Using default values.")
        return config

    except ConfigurationError as e:
        log.warning("%s. Using default values.", e)
        return config
    except scanner.ScannerError:
        log.warning("Malformed configuration file. Using default values.")
        return config

def main():
    """The entry point of the application."""

    log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Attempts to parsee user configuration file and returns
    # the code that denotes the execution branch

    config = parse_config()

    if "admin" in sys.argv:
        #Create admin and exit
        admin = gen_user_admin()
        try:
            api_url = config["api_url"] + "/users/registration"
            response = add_admin_user(api_url, **admin)
            cache["users"]["admin"].append(response)
            members = cache["users"]["member"]
            admins = cache["users"]["admin"]
            user_report(members, admins)
        except APIError as e:
            log.error(e)

        return

    try:
        login_url = config["api_url"] + "/login"
        applications_url = config["api_url"] + "/applications"
        banks_url = config["api_url"] + "/banks"
        branches_url = config["api_url"] + "/branches"
        users_url = config["api_url"] + "/users/registration"
        transactions_url = config["api_url"] + "/transactions"
        accounts_url = config["api_url"] + "/accounts"
        approved = config["applicants"]["approved"]
        denied = config["applicants"]["denied"]
        banks = config["banks"]["count"]
        branches_per_bank = config["banks"]["branches_per_bank"]
        admin_uname = config["admin_username"]
        admin_pswd = config["admin_password"]
        txn_per_account = config["transactions"]["txn_per_account"]

        add_banks_and_branches(banks_url, branches_url, login_url, banks,
                                branches_per_bank, admin_uname, admin_pswd)

        add_applications(applications_url, approved, denied)

        add_users(users_url)

        add_transactions(transactions_url, accounts_url, login_url,
                         txn_per_account, admin_uname, admin_pswd)

    except APIError as e:
        log.error(e)
    except Exception as e:
        log.error(e)
    finally:
        #Print reports
        approved = len(cache["applicants"]["approved"])
        denied = len(cache["applicants"]["denied"])
        members = cache["users"]["member"]
        admins = cache["users"]["admin"]
        banks = len(cache["banks"])
        branches = len(cache["branches"])
        transactions = cache["transactions"]

        applicant_report(approved, denied)
        banks_and_branches_report(banks, branches)
        user_report(members, admins)
        transaction_report(transactions)

        #Write cache to file
        with open("cache.json", "w", encoding="utf-8") as cache_file:
            cache_file.write(json.dumps(cache, indent=4))

if __name__ == "__main__":
    main()
