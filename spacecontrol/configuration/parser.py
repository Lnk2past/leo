import argparse
import re
import yaml


def sctl_configuration(path):
    try:
        return yaml.load(open(path), Loader=yaml.FullLoader)
    except FileNotFoundError:
        try:
            return yaml.load(open('~/.sctl/config.yml'), Loader=yaml.FullLoader)
        except FileNotFoundError:
            raise argparse.ArgumentError('No configuration can be found!')


def parse_inputs():
    parser = argparse.ArgumentParser('sctl')
    parser.add_argument('-c', '--configuration', default='.sctl/config.yml', type=sctl_configuration)
    parser.add_argument('-d', '--directory')
    parser.add_argument('-n', '--nodes', default='.*', type=re.compile)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)

    action_parser = argparse.ArgumentParser('sctl')
    action_subparsers = action_parser.add_subparsers(required=True, dest='action')

    exec_parser = action_subparsers.add_parser('exec')
    exec_parser.add_argument('command', help='command to execute')

    download_parser = action_subparsers.add_parser('download')
    download_parser.add_argument('remote', help='remote path')
    download_parser.add_argument('local', nargs='?', default=None, help='local path')

    upload_parser = action_subparsers.add_parser('upload')
    upload_parser.add_argument('local', help='local path')
    upload_parser.add_argument('remote', nargs='?', default=None, help='remote path')

    args, extras = parser.parse_known_args()
    if extras and extras[0] in ['exec','download', 'upload']:
        return action_parser.parse_args(extras, namespace=args)

    if 'actions' in args.configuration and extras and extras[0] in args.configuration['actions']:
        args.action = extras[0]
        return args

    extras.insert(0, 'exec')
    return action_parser.parse_args(extras, namespace=args)
