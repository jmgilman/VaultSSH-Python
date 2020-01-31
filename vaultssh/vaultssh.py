""" Main file """

import getpass
import logging
import os

import click
import hvac
import vaultssh.auth as auth
import vaultssh.common as common


@click.command()
@click.option(
    "--persist/--no-persist",
    help="Whether to persist newly acquired tokens",
    default=True,
)
@click.option(
    "-s", "--server", help="The URL for the Vault server to query against"
)
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

    # Check for url
    client.url = server if server else client.url
    if not client.url:
        logging.info("No url address to Vault server supplied")
        click.echo(
            "No URL found - please set VAULT_ADDR environment variable or manually pass a server url"
        )
        exit(1)

    # Check for authentication
    client.token = token if token else client.token

    logging.debug(f"Token set to {client.token}")
    logging.debug(f"URL set to {client.url}")

    if not client.is_authenticated():
        auth.authenticate(client, persist)

    # Sign key
    try:
        result = client.write(
            "ssh/sign/" + role, public_key=ssh_public_key.read()
        )
    except hvac.exceptions.InvalidRequest:
        logging.fatal("Error signing SSH key", exc_info=True)
        exit(1)

    # Write the signed certificate
    common.write_signed_key(ssh_public_key.name, result["data"]["signed_key"])
