""" Main file """

import click
import getpass
import hvac
import os

from os.path import expanduser

def authenticate(client, persist):
    success = False

    while not success:
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        try:
            result = client.auth.radius.login(username, password)
        except hvac.exceptions.InvalidRequest:
            click.echo("Invalid username/password")
            continue

        success = True

    # Persist the token
    if persist:
        write_token(result['auth']['client_token'])

def write_token(token):
    user_home = expanduser("~")
    token_file = os.path.join(user_home, '.vault-token')

    with open(token_file, 'w') as f:
        f.write(result['auth']['client_token'])

@click.command()
@click.option('--persist/--no-persist', help='Whether to persist newly acquired tokens', default=True)
@click.option("--token", help="The Vault token to authenticate with")
@click.argument('ssh_public_key', type=click.File('r'))
@click.argument('role', default='default', required=False)
def main(ssh_public_key, role, persist, token):
    # Instantiate client
    client = hvac.Client()

    # Check for authentication
    client.token = token if token else client.token
    if not client.is_authenticated():
        authenticate(client, persist)

    # Sign key
    try:
        result = client.write("ssh/sign/" + role, public_key=ssh_public_key.read())
    except hvac.exceptions.InvalidRequest as e:
        click.echo("Error signing SSH key. Server returned: " + str(e))
        exit()

    # Build new file name
    key_dir = os.path.dirname(ssh_public_key.name)
    key_parts = os.path.splitext(os.path.basename(ssh_public_key.name))
    new_name = key_parts[0] + '-cert' + key_parts[1]

    signed_ssh_public_key = os.path.join(key_dir, new_name)
    with open(signed_ssh_public_key, "w") as f:
        f.write(result['data']['signed_key'])

    click.echo("Signed key saved to " + signed_ssh_public_key)

if __name__ == '__main__':
    main()