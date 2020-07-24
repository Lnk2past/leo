import logging
import os

import fabric

from spacecontrol.actions import *
from spacecontrol.configuration.parser import parse_inputs
from spacecontrol.utilities.logger import logger, logger_format_fields, setup_logger


def sctl():
    inputs = parse_inputs()
    inputs.configuration.setdefault('directory', inputs.directory)
    setup_logger(inputs.verbose)
    logger_format_fields['host'] = 'local'
    directory = inputs.directory if inputs.directory else inputs.configuration['directory'] if 'directory' in inputs.configuration else None

    actions = []
    if inputs.action == 'exec':
        actions.append(ExecAction(inputs.command, directory=directory))
    elif inputs.action == 'download':
        actions.append(DownloadAction(inputs.remote, inputs.local, directory=directory))
    elif inputs.action == 'upload':
        actions.append(UploadAction(inputs.local, inputs.remote, directory=directory))
    else:
        def baction(action, actions_list):
            if action['action'] == 'exec':
                actions_list.append(ExecAction(action['command'], directory=directory))
            elif action['action'] == 'download':
                actions_list.append(DownloadAction(action['remote'], action.get('local', None), directory=directory))
            elif action['action'] == 'upload':
                actions_list.append(UploadAction(action['local'], action.get('remote', None), directory=directory))

        for action in inputs.configuration['actions'][inputs.action]:
            baction(action, actions)

    nodes = [node for node in inputs.configuration['nodes'] if inputs.nodes.match(node['host'])]
    for node in nodes:
        cnx = fabric.Connection(**node)
        for action in actions:
            if isinstance(action, DownloadAction):
                if action.local is None and len(nodes) > 1:
                    action.local = f'{node["host"]}.{os.path.basename(action.remote)}'
            action(cnx)

if __name__ == '__main__':
    main()
