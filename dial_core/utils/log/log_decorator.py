# MIT License

# Copyright (c) 2017 sighalt

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#          Repo: https://github.com/sighalt/logdecorator
#

# flake8: noqa

import inspect
import logging
from functools import wraps

from .log import LOG_LEVEL


class DecoratorMixin(object):
    def execute(self, fn, *args, **kwargs):
        return fn(*args, **kwargs)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return self.execute(fn, *args, **kwargs)

        return wrapper


class LoggingDecorator(DecoratorMixin):
    def __init__(self, log_level, message, *, logger=None):
        self.log_level = log_level
        self.message = message
        self._logger = logger

    @staticmethod
    def log(logger, log_level, msg):
        logger.log(log_level, msg)

    def get_logger(self, fn):
        if self._logger is None:
            self._logger = logging.getLogger(fn.__module__)
            self._logger.setLevel(LOG_LEVEL)

        return self._logger

    @staticmethod
    def build_extensive_kwargs(fn, *args, **kwargs):
        function_signature = inspect.signature(fn)
        extensive_kwargs = function_signature.bind_partial(*args, **kwargs)

        return extensive_kwargs.arguments


class log_on_start(LoggingDecorator):
    def _do_logging(self, fn, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        msg = self.message.format(**extensive_kwargs)

        self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        self._do_logging(fn, *args, **kwargs)
        return super().execute(fn, *args, **kwargs)


class log_on_end(LoggingDecorator):
    def __init__(
        self, log_level, message, *, logger=None, result_format_variable="result"
    ):
        super().__init__(log_level, message, logger=logger)
        self.result_format_variable = result_format_variable

    def _do_logging(self, fn, result, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        extensive_kwargs[self.result_format_variable] = result
        msg = self.message.format(**extensive_kwargs)

        self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        result = super().execute(fn, *args, **kwargs)
        self._do_logging(fn, result, *args, **kwargs)

        return result


class log_on_error(LoggingDecorator):
    def __init__(
        self,
        log_level,
        message,
        *,
        logger=None,
        on_exceptions=None,
        reraise=True,
        exception_format_variable="e"
    ):
        super().__init__(log_level, message, logger=logger)
        self.on_exceptions = on_exceptions
        self.reraise = reraise
        self.exception_format_variable = exception_format_variable

    def _do_logging(self, fn, exception, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        extensive_kwargs[self.exception_format_variable] = exception
        msg = self.message.format(**extensive_kwargs)

        self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        try:
            return super().execute(fn, *args, **kwargs)
        except Exception as e:
            self.on_error(fn, e, *args, **kwargs)

    def on_error(self, fn, exception, *args, **kwargs):
        try:
            raise exception
        except self.on_exceptions:
            self._do_logging(fn, exception, *args, **kwargs)

            if self.reraise:
                raise


class log_exception(log_on_error):
    def __init__(
        self,
        message,
        *,
        logger=None,
        on_exceptions=None,
        reraise=True,
        exception_format_variable="e"
    ):
        super().__init__(
            logging.ERROR,
            message,
            logger=logger,
            on_exceptions=on_exceptions,
            reraise=reraise,
            exception_format_variable=exception_format_variable,
        )

    @staticmethod
    def log(logger, log_level, msg):
        logger.exception(msg)
