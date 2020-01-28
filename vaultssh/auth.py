import click
import getpass
import hvac
import logging

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
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        try:
            result = client.auth.radius.login(username, password)
        except hvac.exceptions.InvalidRequest: # Thrown when a login fails
            click.echo("Invalid username/password")
            logging.debug("Server threw InvalidRequest", exc_info=True)
            continue

        success = True

    logging.info(f"Server returned token: {result['auth']['client_token']}")
    return result['auth']['client_token'] # Newly retrieved token

AUTH_METHODS = {
    "radius": radius,
}