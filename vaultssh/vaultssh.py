""" Main file """

import click
import getpass
import hvac
import os

import vaultssh.common as common


@click.command()
@click.option('--persist/--no-persist', help='Whether to persist newly acquired tokens', default=True)
@click.option('--server', help='The URL for the Vault server to query against')
@click.option("--token", help="The Vault token to authenticate with")
@click.argument('ssh_public_key', type=click.File('r'))
@click.argument('role')
def main(ssh_public_key, role, persist, server, token):
    """ Sign SSH_PUBLIC_KEY using the given Vault ROLE

    \b
    SSH_PUBLIC_KEY must be a file path to a valid SSH public key file
    ROLE must be a valid configured role in the Vault server
    """
    # Instantiate client
    client = hvac.Client()

    # Check for authentication
    client.token = token if token else client.token
    client.url = server if server else client.url
    if not client.is_authenticated():
        common.authenticate(client, persist)

    # Sign key
    try:
        result = client.write("ssh/sign/" + role,
                              public_key=ssh_public_key.read())
    except hvac.exceptions.InvalidRequest as e:
        click.echo(f"Error signing SSH key. Server returned: {e}")
        exit()

    # Build path to certificate file
    signed_ssh_public_key = common.build_signed_key_path(ssh_public_key)

    # Write the signed certificate
    try:
        with open(signed_ssh_public_key, "w") as f:
            f.write(result['data']['signed_key'])
    except Exception as e:
        click.echo(
            "Failed to write signed public key to {signed_ssh_public_key}")
        exit(1)

    click.echo("Signed key saved to " + signed_ssh_public_key)
