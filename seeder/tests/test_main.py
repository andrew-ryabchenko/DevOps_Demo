"""This module implements tests for the main.py module."""
#pylint: disable=unused-argument
from db_seeder.main import main, parse_config
from .util import search_user, confirm_users_added
from .util import confirm_banks_and_branches_added,\
    confirm_applicants_added, confirm_transactions_added

def test_main_add_admin_user(admin_user, bearer, mocker, test_config):
    """Tests adding an admin user."""
    test_config = test_config
    mocker.patch("db_seeder.main.gen_user_admin", return_value=admin_user)
    mocker.patch("db_seeder.main.sys.argv", ["_", "admin"])

    main()
    # Search for a the newly created admin user to confirm that it was added to the database
    assert search_user(admin_user["username"], bearer, test_config) is not None

def test_main_all(bearer, test_config, mocker):
    """Tests adding applicants, users, banks, and branches."""

    # Version of config file with all data to be added
    mocker.patch("db_seeder.main.parse_config", return_value=test_config)

    main()

    assert confirm_users_added(bearer, test_config)
    assert confirm_applicants_added(test_config)
    assert confirm_banks_and_branches_added(test_config)
    assert confirm_transactions_added(test_config["api_url"] + "/accounts",
                                      bearer, test_config["transactions"]["txn_per_account"])

# def test_main_applicants_users(bearer, test_config, mocker, refresh_cache):
#     """Tests execution branch that adds applicants and users."""
#     # Version of config file with only applicants and users
#     config = test_config["two"]

#     mocker.patch("db_seeder.main.parse_config", return_value=(config, 2))

#     main()

#     assert confirm_users_added(bearer, config) is True
#     assert confirm_applicants_added(config) is True

# def test_main_applicants_banks(test_config, mocker, refresh_cache):
#     """Tests execution branch that adds applicants and banks."""

#     # Version of config file with only applicants and banks
#     config = test_config["three"]

#     mocker.patch("db_seeder.main.parse_config", return_value=(config, 3))

#     main()

#     assert confirm_banks_and_branches_added(config) is True
#     assert confirm_applicants_added(config) is True

# def test_main_applicants(test_config, mocker, refresh_cache):
#     """Tests execution branch that adds applicants."""

#     # Version of config file with only applicants
#     config = test_config["four"]

#     mocker.patch("db_seeder.main.parse_config", return_value=(config, 4))

#     main()

#     assert confirm_applicants_added(config) is True

# def test_main_banks(test_config, mocker, refresh_cache):
#     """Tests execution branch that adds banks and branches."""

#     # Version of config file with only banks
#     config = test_config["five"]

#     mocker.patch("db_seeder.main.parse_config", return_value=(config, 5))

#     main()

#     assert confirm_banks_and_branches_added(config) is True

# def test_main_parse_config_all(test_config, mocker):
#     """Tests parsing and interpreting config file with all data to be added."""
#     mocker.patch("db_seeder.main.load", return_value=test_config["one"])

#     _, code = parse_config()
#     assert code == 1

# def test_main_parse_config_applicants_users(test_config, mocker):
#     """Tests parsing and interpreting config file with only applicants and users."""
#     mocker.patch("db_seeder.main.load", return_value=test_config["two"])

#     _, code = parse_config()
#     assert code == 2

# def test_main_parse_config_applicants_banks(test_config, mocker):
#     """Tests parsing and interpreting config file with only applicants and banks."""
#     mocker.patch("db_seeder.main.load", return_value=test_config["three"])

#     _, code = parse_config()
#     assert code == 3

# def test_main_parse_applicants(test_config, mocker):
#     """Tests parsing and interpreting config file with only applicants."""
#     mocker.patch("db_seeder.main.load", return_value=test_config["four"])

#     _, code = parse_config()
#     assert code == 4

# def test_main_parse_config_banks(test_config, mocker):
#     """Tests parsing and interpreting config file with only banks."""
#     mocker.patch("db_seeder.main.load", return_value=test_config["five"])

#     _, code = parse_config()
#     assert code == 5

# def test_main_parse_config_invalid(test_config, mocker):
#     """Tests parsing and interpreting config file with invalid data."""
#     mocker.patch("db_seeder.main.load", return_value=test_config["invalid"])

#     _, code = parse_config()
#     assert code == 1

# def test_main_parse_config_missing(test_config, mocker):
#     """Tests parsing and interpreting config file that is missing."""
#     mocker.patch("db_seeder.main.open", side_effect=FileNotFoundError)

#     _, code = parse_config()
#     assert code == 1
