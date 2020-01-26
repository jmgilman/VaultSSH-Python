""" Main file """

import getpass
import hvac
import os

from os.path import expanduser

def authenticate(client):
    success = False

    while not success:
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        try:
            result = client.auth.radius.login(username, password)
        except hvac.exceptions.InvalidRequest:
            print("Invalid username/password")
            continue

    success = True

    # Set the token
    os.environ['VAULT_TOKEN'] = result['auth']['client_token']

    with open(token_file, 'w') as f:
        f.write(result['auth']['client_token'])

def main():
    # Load environment variables
    #url = os.getenv('VAULT_ADDR')
    home = expanduser("~")

    token = os.getenv('VAULT_TOKEN')
    token_file = os.path.join(home, ".vault-token")

    ssh_key = os.path.join(home, ".ssh/id_rsa.pub")
    ssh_user = "josh"

    # Load token file if not ENV is not set
    if not token and os.path.isfile(token_file):
        with open(token_file) as f:
            token = f.read()

    # Defaults to using VAULT_ADDR and VAULT_TOKEN
    client = hvac.Client(token=token)

    # Check if authenticated
    if not client.is_authenticated():
        authenticate(client)

    # Sign key
    with open(ssh_key) as f:
        public_key = f.read()

    try:
        result = client.write("ssh/sign/" + ssh_user, public_key=public_key)
    except hvac.exceptions.InvalidRequest:
        print("Error signing SSH key. Do you have the right permissions?")
        exit()

    cert_path = "/home/josh/.ssh/id_rsa-cert.pub"
    with open(cert_path, "w") as f:
        f.write(result['data']['signed_key'])


if __name__ == "__main__":
    main()