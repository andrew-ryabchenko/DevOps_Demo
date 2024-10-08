import json
import sys

if sys.argv[1] == "username":
    secret_object = sys.stdin.read()
    secret_object = json.loads(secret_object)

    secret_string = secret_object["SecretString"]
    secret_data = json.loads(secret_string)

    print(secret_data["username"])

if sys.argv[1] == "password":
    secret_object = sys.stdin.read()
    secret_object = json.loads(secret_object)

    secret_string = secret_object["SecretString"]
    secret_data = json.loads(secret_string)

    print(secret_data["password"])