import contextlib
from spacecontrol.utilities.logger import logger, logger_format_fields


class DownloadAction:
    def __init__(self, remote, local, *, directory=None):
        self.remote = remote
        self.local = local
        self.directory = directory

    def __call__(self, connection):
        logger_format_fields['host'] = connection.host
        with connection.cd(self.directory) if self.directory else contextlib.nullcontext():
            logger.critical(f'Downloading: "{self.remote}"', extra=logger_format_fields)
            result = connection.get(self.remote, self.local)
            logger.debug(f'Downloaded: "{result.local}"', extra=logger_format_fields)
