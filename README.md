# spaceman

`spaceman` is a simple CLI tool for working within a distributed environment. The goal is to allow batch operations to be easily executed on any number of hosts, whether that means executing commands, downloading or uploading files, or whatever else is needed.

Sample configuration file:

```yaml
directory: /
nodes:
  - host: 'some_host'
    user: 'root'
    connect_kwargs: {
      password: password
    }
  - host: 'mypi'
    user: 'pi'
```

`spaceman` by default will look for a configuration file relative to your current location: `.spaceman/config.yml`. If a file cannot be found, it will look in `~/.spaceman/config.yml`. Alternatively you can specify a path to a configuration using the `-c / --configuration` option. This will be expanded on in the future to allow for multiple "profiles" in a single config.

The keys for each entry of `nodes` are the parameters specified by [`fabric.connection.Connection`](https://docs.fabfile.org/en/2.5/api/connection.html#fabric.connection.Connection) (of the wonderful [`fabric`](https://github.com/fabric/fabric)) library. Any configuration you want to do locally with SSH keys, authorized_keys, etc. is up to you. If you are not familiar (as I was merely 10 hours ago) `fabric` is an awesome wrapper around [`paramiko`](https://github.com/paramiko/paramiko) and some other tools, and it is so easy and clean to use. Check out both of those libraries.

This tool is not complete and is far from it.

## Install

I will eventually get around to making this into a usable package. For now install it yourself.

### Basic

Clone this repository and then run:

```shell
python setup.py install
```

### Directly From GitHub

Install with pip directly from GitHub:

```shell
python -m pip install git+https://github.com/Lnk2past/spaceman.git
```

## Sample Usage

Run `ls` on each node and print the output (the default action is `exec` and may be omitted):

```shell
sctl ls
```

```shell
sctl exec ls
```

Download the `.bashrc` from each node:

```shell
sctl download .bashrc
```

Upload a new `.bashrc` to each node:

```shell
sctl upload .bashrc
```

### Notes

You may omit specifying a `directory` in your configuration; in these cases the default directory is usually the home directory of the user you are logging in as.
