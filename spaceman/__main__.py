import argparse
import paramiko
import yaml


def parse_inputs():
    parser = argparse.ArgumentParser('spaceman')
    parser.add_argument('--configuration', default='test.yml', type=lambda p: yaml.load(open(p), Loader=yaml.FullLoader))

    subparsers = parser.add_subparsers(dest='action')
    exec_parser = subparsers.add_parser('exec')
    exec_parser.add_argument('command', help='command to execute')

    download_parser = subparsers.add_parser('download')
    download_parser.add_argument('src', help='remote path')
    download_parser.add_argument('dest', help='local path')

    upload_parser = subparsers.add_parser('upload')
    upload_parser.add_argument('src', help='local path')
    upload_parser.add_argument('dest', help='remote path')

    return parser.parse_args()


def get_ssh_client(node):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(**node)
    return ssh_client


def get_ftp_client(node):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(**node)
    ftp_client = ssh_client.open_sftp()
    return ftp_client


def main():
    inputs = parse_inputs()
    if inputs.action == 'exec':
        for node in inputs.configuration['nodes']:
            print(f'Executing on {node}')
            ssh_client = get_client(node)
            stdin, stdout, stderr = ssh_client.exec_command(inputs.command)
            print(stdout.read().decode())
            print(stderr.read().decode())
    elif inputs.action == 'download':
        for node in inputs.configuration['nodes']:
            print(f'Downloading from {node}')
            ftp_client = get_ftp_client(node)
            ftp_client.get(inputs.src, f'{node["hostname"]}.{inputs.dest}')
            ftp_client.close()
    elif inputs.action == 'upload':
        for node in inputs.configuration['nodes']:
            print(f'Uploading to {node}')
            ftp_client = get_ftp_client(node)
            ftp_client.put(inputs.src, inputs.dest)
            ftp_client.close()

if __name__ == '__main__':
    main()
