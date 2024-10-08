"""This module contains fixtures for the tests."""

import pytest
#pylint: disable=import-error
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from db_seeder.users import gen_user_admin
from db_seeder.users import get_admin_auth_token
from db_seeder.cache import CACHE as cache

@pytest.fixture(scope='function')
def refresh_cache():
    """Requesting this fixture makes global cache to refresh and empty."""

    cache["applicants"]["approved"] = []
    cache["applicants"]["denied"] = []
    cache["users"]["member"] = []
    cache["users"]["admin"] = []
    cache["banks"] = []
    cache["branches"] = []

@pytest.fixture(scope='module')
def admin_user():
    """Returns a payload with data for a random admin user."""
    return gen_user_admin()

@pytest.fixture(scope='session')
def test_config():
    """Parses the parsed test configuration file."""
    with open("config-test.yaml", "r", encoding="utf-8") as config_file:
        config = load(config_file, Loader)
        return config

@pytest.fixture(scope='session')
def bearer(test_config) -> str:
    """Logins as admin and returns an admin bearer token."""
    admin_uname = test_config["admin_username"]
    admin_pswd = test_config["admin_password"]
    return get_admin_auth_token(test_config["api_url"] + "/login",
                                admin_uname, admin_pswd)
