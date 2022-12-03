# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import logging
import bridge


class OutputWindowHandler(logging.Handler):
    """
    log to output window
    """

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        if bridge.output_window_bridge_object:
            if record.levelno >= logging.ERROR:
                bridge.output_window_bridge_object.show_error_message.emit(message)
            elif record.levelno == logging.WARNING:
                bridge.output_window_bridge_object.show_warning_message.emit(message)
            else:
                bridge.output_window_bridge_object.show_normal_message.emit(message)
        try:
            if record.levelno >= logging.ERROR and sys.__stderr__:
                sys.__stderr__.write(f'{message}\n')
            elif sys.__stdout__:
                sys.__stdout__.write(f'{message}\n')
            self.flush()
        except RecursionError as e:
            raise e
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)

    def flush(self) -> None:
        self.acquire()
        try:
            sys.stderr.flush()
        except AttributeError as e:
            if e.name != 'flush':
                raise e
        finally:
            self.release()
