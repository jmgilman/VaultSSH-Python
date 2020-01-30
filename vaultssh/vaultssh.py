""" Main file """

import click
import getpass
import hvac
import logging
import os

import vaultssh.common as common
import vaultssh.auth as auth


@click.command()
@click.option(
    "--persist/--no-persist",
    help="Whether to persist newly acquired tokens",
    default=True,
)
@click.option("-s", "--server", help="The URL for the Vault server to query against")
@click.option("-t", "--token", help="The Vault token to authenticate with")
@click.option("-v", "--verbose", count=True)
@click.argument("ssh_public_key", type=click.File("r"))
@click.argument("role")
def main(ssh_public_key, role, persist, server, token, verbose):
    """ Sign SSH_PUBLIC_KEY using the given Vault ROLE

    \b
    SSH_PUBLIC_KEY must be a file path to a valid SSH public key file
    ROLE must be a valid configured role in the Vault server
    """
    # Configure logging
    common.configure_logging(verbose)

    # Instantiate client
    client = hvac.Client()

    # Check for authentication
    client.token = token if token else client.token
    client.url = server if server else client.url

    logging.debug(f"Token set to {client.token}")
    logging.debug(f"URL set to {client.url}")

    if not client.is_authenticated():
        auth.authenticate(client, persist)

    # Sign key
    try:
        result = client.write("ssh/sign/" + role, public_key=ssh_public_key.read())
    except hvac.exceptions.InvalidRequest:
        logging.fatal("Error signing SSH key", exc_info=True)
        exit(1)

    # Build path to certificate file
    signed_ssh_public_key = common.build_signed_key_path(ssh_public_key)

    # Write the signed certificate
    logging.info(f"Writing signed key to {signed_ssh_public_key}")
    try:
        with open(signed_ssh_public_key, "w") as f:
            f.write(result["data"]["signed_key"])
    except Exception:
        logging.fatal("Failed to write signed public key", exc_info=True)
        exit(1)

    click.echo("Signed key saved to " + signed_ssh_public_key)
