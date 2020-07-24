import contextlib
from spacecontrol.utilities.logger import logger, logger_format_fields


class ExecAction:
    def __init__(self, command, *, directory=None):
        self.command = command
        self.directory = directory

    def __call__(self, connection):
        logger_format_fields['host'] = connection.host
        with cnx.cd(self.directory) if self.directory else contextlib.nullcontext():
            logger.critical(f'Executing: "{self.command}"', extra=logger_format_fields)
            result = connection.run(self.command, hide=True)
            if result.stdout:
                logger.critical(result.stdout, extra=logger_format_fields)
            if not result.ok:
                logger.critical(result.stderr, extra=logger_format_fields)
