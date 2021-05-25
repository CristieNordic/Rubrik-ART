# Cristie Rubrik-ART
Small Automatic Restore tester for Rubrik Cloud Data Management (CDM)

## Prerequisites
Make sure you have installed `requests` and `argparse`.
Easiest way to install it us by running `pip install -r requirements.txt`
You need to have a credentials and privileged on your Rubrik Cluster.
The script is based on Python 3

## Run Restore Test
### Using Config File
Open `config.py` and fillout the two required fields
- `RUBRIK_AUTH` you need to use a base64 encoded string with your username:password format.
- `RUBRIK_URL` insert a full qualified domain name or IP address to your Rubrik Cluster, example `rubrik.company.com` or `10.0.0.1`

When the configuration file is filled out you can then just run `python rubrik-art.py`

### Using CLI
To get full help, please run `python rubrik-art.py --help`
But you can either use both base64 encoded key or clear text username and password.
To use username and password you need to specifiy `--url`, `--username` and `--password`

As example could you use local accounts or LDAP accounts like follow example
`python rubrik-art.py --url rubrik.company.com --username your.ldap_account@company.com --password YourSecretPassword`

### Using System variable
Export both `RUBRIK_URL` and `RUBRIK_AUTH` as system variable.
- `RUBRIK_AUTH` you need to use a base64 encoded string with your username:password format.
- `RUBRIK_URL` insert a full qualified domain name or IP address to your Rubrik Cluster, example `rubrik.company.com` or `10.0.0.1`

When the configuration file is filled out you can then just run `python rubrik-art.py`

## Change Log
Please read the [CHANGELOG.md](https://github.com/CristieNordic/Rubrik-ART/blob/main/CHANGELOG.md) file.

## Known Issues
Please read the [ISSUES.md](https://github.com/CristieNordic/Rubrik-ART/blob/main/ISSUES.md) file.

## License
Please read the [LICENSE.md](https://github.com/CristieNordic/Rubrik-ART/blob/main/LICENSE.md) file.
