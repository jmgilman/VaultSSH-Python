# VaultSSH
> CLI tool for signing SSH public keys using the Vault SSH endpoint

VaultSSH is a simple command line tool written in Python which automates the process of signing SSH public keys using the [Hashicorp Vault](https://www.vaultproject.io/) SSH backend. In environments which have configured Vault as a trusted CA and use it to issue signed keys for authenticating against SSH servers, this tool provides a simple wrapper which handles all the backend communication and produces a signed public key ready for the end-user to authenticate with.

This tool assumes that your Vault environment has been properly configured for signing SSH keys. Hashicorp provides extensive documentation along with examples on how to perform this configuration [in their docs](https://www.vaultproject.io/docs/secrets/ssh/signed-ssh-certificates/).

![](header.png)

## Installation

```sh
pip install vaultssh
```

## Usage example

VaultSSH takes two arguments: a path to the public SSH key to sign and the [Vault role](https://learn.hashicorp.com/vault/identity-access-management/iam-policies) that should be used to sign it. Please refer to the [Vault documentation](https://www.vaultproject.io/docs/secrets/ssh/signed-ssh-certificates/) to learn more about configuring SSH key signing. 

```sh
$ vaultssh ~/.ssh/id_rsa.pub myrole
```

VaultSSH will automatically detect if you had previously authenticated with the Vault server by looking for an existing token in the default Vault environment variable (`VAULT_TOKEN`) or Vault token file (~/.vault-token). You can override this behavior and provide your own token by passing the --token flag. If a token is not found, or has expired, the tool will prompt you to authenticate with the Vault backend to fetch a new token (Note: only RADIUS is currently supported). By default the tool will persist the newly acquired token in the Vault token file, however this can be disabled by passing the --no-persist flag.

VaultSSH will automatically detect the location of the Vault server by using the default Vault environment variable (`VAULT_ADDR`). You can override this behavior by passing the --server flag.

```sh
$ vaultssh --server https://myvault.com:8200 ~/.ssh/id_rsa.pub myrole
```

If the signing process succeeds, VaultSSH will automatically write the signed certificate to the same directory as the given public key:

```sh
$ vaultssh ~/.ssh/id_rsa.pub myrole
Signed key saved to /home/josh/.ssh/id_rsa-cert.pub
```

## Development setup

This project was developed using Pipenv as the virtual environment wrapper. To install all dependencies, run the following command at the root of the project:

```sh
pipenv install --dev
```

## Release History

* 0.1.0
    * Initial prototype

## Meta

Joshua Gilman – joshuagilman@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/jmgilman](https://github.com/jmgilman)

## Contributing

1. Fork it (<https://github.com/jmgilman/vaultssh/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request