import click
import getpass
import hvac
import os


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
    user_home = os.path.expanduser("~")
    token_file = os.path.join(user_home, '.vault-token')

    try:
        with open(token_file, 'w') as f:
            f.write(result['auth']['client_token'])
    except:
        click.echo(f"Warning: failed to persist token at {token_file}")
