import getpass
import logging
import os

import click
import hvac
import vaultssh.common as common


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
    methods = sorted([key.title() for key in AUTH_METHODS])
    for method in methods:
        click.echo(f"* {method}\n")

    # Collect which one to use
    chosen_method = ""
    while chosen_method.lower() not in AUTH_METHODS:
        chosen_method = click.prompt(
            "Please select the authentication method to use: "
        )

    # Attempt to authenticate
    logging.debug(f"Calling function for {chosen_method.lower()}")
    token = AUTH_METHODS[chosen_method.lower()](client)

    # Persist the token
    if persist:
        common.write_token(token)


def radius(client):
    """ Attempts to authenticate against a Vault RADIUS backend 

    Args:
        client (hvac.Client): The hvac client to authenticate with

    Returns:
        The newly retrieved token
    """
    success = False
    result = []

    # Attempt to login using provided username/password
    while not success:
        click.echo("Please enter your RADIUS username and password:")
        username = click.prompt("Username: ")
        password = getpass.getpass("Password: ")

        try:
            result = client.auth.radius.login(username, password)
        except hvac.exceptions.InvalidRequest:  # Thrown when a login fails
            click.echo("Invalid username/password")
            logging.debug("Server threw InvalidRequest", exc_info=True)
            continue

        success = True

    logging.info(f"Server returned token: {result['auth']['client_token']}")
    return result["auth"]["client_token"]  # Newly retrieved token


AUTH_METHODS = {
    "radius": radius,
}
