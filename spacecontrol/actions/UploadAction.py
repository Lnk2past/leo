import contextlib
from spacecontrol.utilities.logger import logger, logger_format_fields


class UploadAction:
    def __init__(self, local, remote, *, directory=None):
        self.local = local
        self.remote = remote
        self.directory = directory

    def __call__(self, connection):
        logger_format_fields['host'] = connection.host
        with connection.cd(self.directory) if self.directory else contextlib.nullcontext():
            logger.critical(f'Uploading "{self.local}"', extra=logger_format_fields)
            result = connection.put(self.local, self.remote)
            logger.debug(f'Uploaded: "{result.remote}"', extra=logger_format_fields)
