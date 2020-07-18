import argparse
import contextlib
import logging
import os
import fabric
import yaml


logging.basicConfig()
logger = logging.getLogger('spaceman')
logger.setLevel(logging.INFO)


def parse_inputs():
    parser = argparse.ArgumentParser('spaceman')
    parser.add_argument('--configuration', default='default.yml', type=lambda p: yaml.load(open(p), Loader=yaml.FullLoader))

    subparsers = parser.add_subparsers(dest='action')
    exec_parser = subparsers.add_parser('exec')
    exec_parser.add_argument('command', help='command to execute')

    download_parser = subparsers.add_parser('download')
    download_parser.add_argument('remote', help='remote path')
    download_parser.add_argument('local', nargs='?', default=None, help='local path')

    upload_parser = subparsers.add_parser('upload')
    upload_parser.add_argument('local', help='local path')
    upload_parser.add_argument('remote', nargs='?', default=None, help='remote path')

    return parser.parse_args()


def sctl():
    inputs = parse_inputs()
    for node in inputs.configuration['nodes']:
        cnx = fabric.Connection(**node)
        with cnx.cd(inputs.configuration['directory']) if 'directory' in inputs.configuration else contextlib.nullcontext():
            if inputs.action == 'exec':
                logger.info(f'Executing on {node}')
                result = cnx.run(inputs.command)
                logger.info(result.stdout)
                if not result.ok:
                    logger.error(result.stderr)

            elif inputs.action == 'download':
                logger.info(f'Downloading from {node}')
                local = inputs.local
                if local is None and len(inputs.configuration['nodes']) > 1:
                    local = f'{node["host"]}.{os.path.basename(inputs.remote)}'
                result = cnx.get(inputs.remote, local)
                logger.info(f'Downloaded {result.remote} to {result.local}')

            elif inputs.action == 'upload':
                logger.info(f'Uploading to {node}')
                result = cnx.put(inputs.local, inputs.remote)
                logger.info(f'Uploaded {result.local} to {result.remote}')


if __name__ == '__main__':
    main()
