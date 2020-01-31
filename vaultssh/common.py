import getpass
import logging
import os

import click
import hvac


def configure_logging(verbosity):
    """ Configures the root logger 
    
    Args:
        verbosity (int): The level of verbosity specified by the user

    Returns:
        None
    """
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]

    # Ignore values higher than 2
    verbosity = 2 if verbosity >= 3 else verbosity

    format = "%(levelname)s: %(message)s"
    logging.basicConfig(format=format, level=levels[verbosity])


def get_signed_key_path(key_file):
    """ Builds the correct path for a signed SSH public key

    Takes a file object pointing towards an SSH public key and breaks it down
    to build the correct path for the associated signed SSH public key. By
    default, SSH expects the file to be named as: <pub_key_name>-cert.pub

    Args:
        key_file (str): The SSH public key file to base the cert file off of

    Returns:
        A string file path to the correct SSH public key cert file
    """
    key_dir = os.path.dirname(key_file)
    key_parts = os.path.splitext(os.path.basename(key_file))
    new_name = key_parts[0] + "-cert" + key_parts[1]

    return os.path.join(key_dir, new_name)


def get_token_file():
    """ Returns the default location for the Vault token file

    Default location as defined by Vault is ~/.vault-token

    Returns:
        A string path to the token file
    """
    user_home = os.path.expanduser("~")
    return os.path.join(user_home, ".vault-token")


def write_signed_key(public_key_path, contents):
    """ Writes a signed SSH public key to the correct path

    Given the path to the original SSH public key, determines the correct
    location to write the signed SSH public key and then writes the contents to
    that location.

    Args:
        public_key_path (str): The path to the original SSH public key
        contents (str): The contents of the signed public SSH key

    Returns:
        None
    """
    path = get_signed_key_path(public_key_path)

    logging.info(f"Writing signed key to {path}")
    try:
        with open(path, "w") as f:
            f.write(contents)
    except Exception:
        logging.fatal("Failed to write signed public key", exc_info=True)
        exit(1)

    click.echo("Signed key saved to " + path)


def write_token(token):
    """ Persists a token by writing it to the default Vault token file

    Args:
        token (string): The token to write

    Returns:
        None
    """
    token_file = get_token_file()
    logging.info(f"Persisting token to {token_file}")

    try:
        with open(token_file, "w") as f:
            f.write(token)
    except:
        logging.warning(
            f"Failed to persist token at {token_file}", exc_info=True
        )
