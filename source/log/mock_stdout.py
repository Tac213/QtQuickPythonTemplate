# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import enum

import bridge


@enum.unique
class ChannelType(enum.Enum):
    STDOUT = 1
    STDERR = 2


class MockStdout(object):
    """
    Mock stdout to write output string to output window
    """

    def __init__(self, channel: ChannelType, origin) -> None:
        self.channel = channel
        self.origin = origin
        self._buffer = ''

    def __getattr__(self, attr_name: str):
        return object.__getattribute__(self.origin, attr_name)

    def write(self, text):
        self.origin.write(text)

        self._buffer += text
        if self._buffer.endswith('\n'):
            self._buffer = self._buffer.rstrip('\n')
            if bridge.output_window_bridge_object:
                if self.channel == ChannelType.STDOUT:
                    bridge.output_window_bridge_object.show_normal_message.emit(self._buffer)
                else:
                    bridge.output_window_bridge_object.show_error_message.emit(self._buffer)
            self._buffer = ''


sys.stdout = MockStdout(ChannelType.STDOUT, sys.__stdout__)
sys.stderr = MockStdout(ChannelType.STDERR, sys.__stderr__)
