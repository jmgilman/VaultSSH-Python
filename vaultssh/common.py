import click
import getpass
import hvac
import logging
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
        chosen_method = input(
            "Please select the authentication method to use: ")

    # Attempt to authenticate
    logging.debug(f"Calling function for {chosen_method.lower()}")
    token = auth.AUTH_METHODS[chosen_method.lower()](client)

    # Persist the token
    if persist:
        write_token(token)


def build_signed_key_path(key_file):
    """ Builds the correct path for a signed SSH public key

    Takes a file object pointing towards an SSH public key and breaks it down
    to build the correct path for the associated signed SSH public key. By
    default, SSH expects the file to be named as: <pub_key_name>-cert.pub

    Args:
        key_file (file): The SSH public key file to base the cert file off of

    Returns:
        A string file path to the correct SSH public key cert file
    """
    key_dir = os.path.dirname(key_file.name)
    key_parts = os.path.splitext(os.path.basename(key_file.name))
    new_name = key_parts[0] + '-cert' + key_parts[1]

    return os.path.join(key_dir, new_name)


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

    logging.info("Persisting token to {token_file}")

    try:
        with open(token_file, 'w') as f:
            f.write(token)
    except:
        logging.warning(f"Failed to persist token at {token_file}", exc_info=True)
