### About
`db_seeder` seeds the Aline Financial database with a test data. 

### Usage 
- Provide configurations in `config.yaml`
- Execute `db_seeder` package as a module by running `python -m db_seeder` 
- To create admin user run `python -m db_seeder admin`

### Configuration
The program attempts to read `config.yaml` configuration file from the current working directory.
The top-level attribute `api_url` must be present at all times in any configuration setup.
The rest of the top-level attributes must also be present. 

Malfomed or missing configuration file will result in using the following fall-back configuration values:
```
api_url: "http://localhost:80/api"
applicants:
  approved: 0
  denied: 0
users:
  password: "Password@99"
banks:
  count: 0
  branches_per_bank: 0
transactions:
  txn_per_account: 0
admin_username: "administrator"
admin_password: "Password@99"
```