import os

import vaultssh.common as common


def test_get_signed_key_path():
    test_path = "/home/user/.ssh/id_rsa.pub"
    correct_path = "/home/user/.ssh/id_rsa-cert.pub"

    assert common.get_signed_key_path(test_path) == correct_path


def test_get_token_file():
    path = common.get_token_file()
    assert path == os.path.join(os.path.expanduser("~"), ".vault-token")
