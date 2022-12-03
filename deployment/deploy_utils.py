# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import os
import threading
from importlib import machinery


def iterate_all_modules(source_dir):
    validate_suffixes = tuple(machinery.SOURCE_SUFFIXES + machinery.EXTENSION_SUFFIXES)
    for root, _, file_names in os.walk(source_dir):
        for file_name in file_names:
            if not file_name.endswith(validate_suffixes):
                continue
            file_path = os.path.join(root, file_name)
            module_name = os.path.splitext(os.path.relpath(file_path, source_dir))[0].replace(os.path.sep, '.')
            if module_name.endswith('__init__'):
                module_name = module_name.rpartition('.')[0]
            yield module_name


class LogPipe(threading.Thread):

    def __init__(self, log_function) -> None:
        super().__init__()
        self.daemon = False
        self.fd_read, self.fd_write = os.pipe()
        self.pipe_reader = os.fdopen(self.fd_read)
        self._log_function = log_function
        self.start()

    def fileno(self) -> int:
        """
        Return the write file descriptor of the pipe
        """
        return self.fd_write

    def run(self):
        """
        Run the thread, logging everything.
        """
        for line in iter(self.pipe_reader.readline, ''):
            self._log_function(line.strip('\n'))
        self.pipe_reader.close()

    def close(self):
        """
        Close the write end of the pipe.
        """
        os.close(self.fd_write)
