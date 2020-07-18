# spaceman

`spaceman` is a simple CLI tool for working within a distributed environment. The goal is to allow batch operations to be easily executed on any number of hosts, whether that means executing commands, downloading or uploading files, or whatever else is needed.

Sample configuration file:

```yaml
nodes:
  - hostname: 'some_host'
    username: 'root'
    password: 'password'
  - hostname: 'mypi'
    username: 'pi'
```

The keys for each entry of `nodes` are the parameters specified by [`paramiko.client.SSHClient.connect`](http://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient.connect) method. Any configuration you want to do locally with SSH keys, authorized_keys, etc. is up to you.

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
