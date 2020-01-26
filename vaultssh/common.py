import click
import getpass
import hvac
import os

import vaultssh.auth as auth


def authenticate(client, persist):
    """ Attempts to authenticate using the user provided authentication method

    Args:
        client (hvac.Client): The client to authenticate with
        persist (bool): Whether or not to persist the new token

    Returns:
        None
    """
    # List possible authentication methods
    click.echo("Available authentication types:")
    methods = sorted([key.title() for key in auth.AUTH_METHODS])
    for method in methods:
        click.echo(f"* {method}\n")

    # Collect which one to use
    chosen_method = ""
    while chosen_method.lower() not in auth.AUTH_METHODS:
        chosen_method = input("Please select the authentication method to use: ")

    # Attempt to authenticate
    token = auth.AUTH_METHODS[chosen_method](client)

    # Persist the token
    if persist:
        write_token(token)


def write_token(token):
    """ Persists a token by writing it to the default Vault token file

    Args:
        token (string): The token to write

    Returns:
        None
    """
    # Default location as defined by Vault is ~/.vault-token
    user_home = os.path.expanduser("~")
    token_file = os.path.join(user_home, '.vault-token')

    try:
        with open(token_file, 'w') as f:
            f.write(token)
    except:
        click.echo(f"Warning: failed to persist token at {token_file}")
