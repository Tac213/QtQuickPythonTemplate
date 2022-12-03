# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import logging
import enum

import bridge


@enum.unique
class ChannelType(enum.Enum):
    STDOUT = 1
    STDERR = 2


class MockStdout(object):
    """
    Mock stdout to write output string to output window and file
    """

    def __init__(self, channel: ChannelType, origin, file_handler: logging.FileHandler) -> None:
        self.channel = channel
        self.origin = origin
        self._file_handler = file_handler
        self._buffer = ''

    def __getattr__(self, attr_name: str):
        return object.__getattribute__(self.origin, attr_name)

    def write(self, text):
        if self.origin:
            self.origin.write(text)

        self._buffer += text
        if self._buffer.endswith('\n'):
            self._buffer = self._buffer.rstrip('\n')
            if bridge.output_window_bridge_object:
                if self.channel == ChannelType.STDOUT:
                    bridge.output_window_bridge_object.show_normal_message.emit(self._buffer)
                else:
                    bridge.output_window_bridge_object.show_error_message.emit(self._buffer)
            self._file_handler.emit(
                logging.LogRecord('std', logging.INFO if self.channel == ChannelType.STDOUT else logging.ERROR, '', 0, self._buffer, (),
                                  None))
            self._buffer = ''
