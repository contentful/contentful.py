from __future__ import annotations

import functools
import logging
import random
import time
from typing import Callable

from contentful.client.transport import errors

"""
contentful.client.transport.retry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements automatic retry with jitter and backoff when receiving errors from the Contentful API.

Complete API Documentation: https://www.contentful.com/developers/docs/references/content-delivery-api/

:copyright: (c) 2016 by Contentful GmbH.
:license: MIT, see LICENSE for more details.
"""


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


__all__ = ("BaseRetry", "Retry", "AsyncRetry")


class BaseRetry:
    def __init__(
        self,
        *,
        max_retries: int = 1,
        max_wait_seconds: int = 60,
    ):
        self.max_retries = max_retries
        self.max_wait_seconds = max_wait_seconds

    def __call__(
        self,
        func: Callable,
        *args,
        **kwargs,
    ):
        raise NotImplementedError()

    def _report_error(
        self, error: errors.TransientHTTPError, *, tries: int, reset_time: int
    ) -> None:
        prefix = (
            "Contentful API Rate Limit Hit! "
            if isinstance(error, errors.RateLimitExceededError)
            else "Contentful API Server Error! "
        )
        retry_message = (
            f"Retrying - Retries left: {self.max_retries - tries} "
            f"- Time until reset (seconds: {reset_time})"
        )
        logger.debug(
            f"{prefix}{retry_message}",
            extra={"tries": tries, "reset_time": reset_time},
        )


class Retry(BaseRetry):
    """
    Decorator to retry function calls in case they raise transient exceptions
    """

    def __call__(
        self,
        func: Callable,
        *args,
        **kwargs,
    ):
        call = functools.partial(func, *args, **kwargs)
        try:
            return call()
        except errors.TransientHTTPError as error:
            tries = 1
            while tries < self.max_retries:
                reset_time = error.reset_time()
                if reset_time > self.max_wait_seconds:
                    raise

                self._report_error(error, tries=tries, reset_time=reset_time)
                real_reset_time = reset_time * random.uniform(1.0, 1.2)
                time.sleep(real_reset_time)
                try:
                    return call()
                except errors.TransientHTTPError:
                    tries += 1

            raise


class AsyncRetry(BaseRetry):
    """
    Decorator to retry async function calls in case they raise transient exceptions
    """

    async def __call__(
        self,
        func: Callable,
        *args,
        **kwargs,
    ):
        call = functools.partial(func, *args, **kwargs)
        try:
            return await call()
        except errors.TransientHTTPError as error:
            tries = 1
            while tries < self.max_retries:
                reset_time = error.reset_time()
                if reset_time > self.max_wait_seconds:
                    raise

                self._report_error(error, tries=tries, reset_time=reset_time)
                real_reset_time = reset_time * random.uniform(1.0, 1.2)
                time.sleep(real_reset_time)
                try:
                    return await call()
                except errors.TransientHTTPError:
                    tries += 1

            raise
