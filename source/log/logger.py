# -*- coding: utf-8 -*-
# author: Tac
# contact: cookiezhx@163.com

import sys
import traceback
import logging


class Logger(logging.Logger):

    def log_last_except(self, skip_frame: int = 0, max_frame: int = 30) -> str:
        stack = ['\n>>>>>>>>>> TRACEBACK >>>>>>>>>>\n', 'Traceback\n']
        exception, arg, tb = sys.exc_info()
        if exception:
            stack.append(f'{exception.__name__}: {arg}\n')
        if tb:
            stack.extend(traceback.format_tb(tb, max_frame))
        else:
            stack.extend(traceback.format_stack(None, max_frame))
            skip_frame += 1
        if skip_frame > 0:
            stack = stack[:-skip_frame]
        stack.append('<<<<<<<<<<<<< END <<<<<<<<<<<<<\n')
        stack_str = ''.join(stack)
        self.error(stack_str)
        return stack_str


logging.setLoggerClass(Logger)
