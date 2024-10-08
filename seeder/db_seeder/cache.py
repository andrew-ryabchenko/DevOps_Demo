"""This module defines global cache objects for the application."""

#Global cache object
CACHE = {
    "applicants": {
        "approved": [],
        "denied": []
    },
    "users": {
        "member": [],
        "admin": []
    },
    "banks": [],
    "branches": [],
    "transactions": []
}

#Global configuration object which also serves as a fallback default configuration
CONFIG = {
    "api_url": "http://localhost:80/api",
    "applicants": {"approved": 0, "denied": 0},
    "users": {"password": "Password@99"},
    "banks": {
        "count": 0,
        "branches_per_bank": 0
    },
    "transactions": {
        "txn_per_account": 0
    },
    "admin_username": "administrator",
    "admin_password": "Password@99"
}
