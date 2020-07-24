# space-control

`space-control`, or `sctl`, is a simple CLI tool for working within a distributed environment. The goal is to allow batch operations to be easily executed on any number of hosts, whether that means executing commands, downloading or uploading files, or whatever else is needed.

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

`sctl` by default will look for a configuration file relative to your current location: `.sctl/config.yml`. If a file cannot be found, it will look in `~/.sctl/config.yml`. Alternatively you can specify a path to a configuration using the `-c / --configuration` option. This will be expanded on in the future to allow for multiple "profiles" in a single config.

The keys for each entry of `nodes` are the parameters specified by [`fabric.connection.Connection`](https://docs.fabfile.org/en/2.5/api/connection.html#fabric.connection.Connection) (of the wonderful [`fabric`](https://github.com/fabric/fabric)) library. Any configuration you want to do locally with SSH keys, authorized_keys, etc. is up to you. If you are not familiar (as I was merely 10 hours ago) `fabric` is an awesome wrapper around [`paramiko`](https://github.com/paramiko/paramiko) and some other tools, and it is so easy and clean to use. Check out both of those libraries.

This tool is not complete and is far from it.

## Install

Install via pip:

```shell
pip install sctl
```

Or for latest and greatest, clone this repository and then run:

```shell
python setup.py install
```

or install directly from GitHub with pip:

```shell
python -m pip install git+https://github.com/Lnk2past/space-control.git
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

## Configurable Actions

`space-control` refers to executing commands and transferring files as *actions*. While you can certainly specify actions directly on the CLI (as shown above), you can also provide custom sets of actions in your configuration file. The added benefit here is that configurable actions are designed to allow you to chain multiple actions together (something you cannot do directly with the CLI). So for example, you can upload a file, run a command to produce a new file, and download that new file all by configuring a single set of actions.

```yaml
nodes:
  - host: 'somehost'
    user: 'root'
actions:
  pgdump:
    - action: 'exec'
      command: 'docker exec postgres pg_dump -f pg_data.txt -t my_table my_db'
    - action: 'exec'
      command: 'docker cp postgres:pg_data.txt pg_data.txt'
    - action: 'download'
      remote: 'pg_data.txt'
```

The custom action `pgdump` here will execute `pg_dump` within the `postgres` container, copy the file from the `postgres` container, and then download it locally.

## Filtering Nodes

Sometimes you may want to run an action on specific nodes in your configuration. This can be done using the `-n` / `--nodes` input options. This option takes a regex pattern and will filter nodes on that pattern. For example, given the following config:

```yaml
nodes:
  - host: 'foo'
    user: 'root'
  - host: 'bar'
    user: 'root'
  - host: 'foobar'
    user: 'root'
```

We can run an action against the `foo` and `foobar` nodes only using:

```shell
sctl -n foo ls
```

Here the pattern `foo` will be partial matches for both `foo` and `foobar` and will both be included in the set of nodes to run against.
