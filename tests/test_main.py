import os

from click.testing import CliRunner
from vaultssh.vaultssh import main


def test_main(mocker):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main)
        assert 'Missing argument "SSH_PUBLIC_KEY"' in result.output

        with open("test.pub", "w") as f:
            f.write("Fake key data")
        result = runner.invoke(main, ["test.pub"])
        assert 'Missing argument "ROLE".' in result.output

        os.environ["VAULT_ADDR"] = ""
        result = runner.invoke(main, ["test.pub", "role"])
        assert "No URL found" in result.output

        os.environ["VAULT_ADDR"] = "htttp://foo.bar"
        mocker.patch("vaultssh.auth.authenticate", return_value=None)
        mocker.patch("hvac.Client.is_authenticated", return_value=True)
        mocker.patch(
            "hvac.Client.write", return_value={"data": {"signed_key": "test"}}
        )
        mocker.patch(
            "vaultssh.common.get_signed_key_path", return_value="test.txt"
        )

        result = runner.invoke(main, ["test.pub", "role"])
        assert "Signed key saved to test.txt" in result.output
        with open("test.txt", "r") as f:
            assert f.read() == "test"
        assert result.exit_code == 0
