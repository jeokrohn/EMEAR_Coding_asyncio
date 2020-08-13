#!/usr/bin/env python
import asyncio
import logging
import time
from logging import Logger

TASKS = 5

log: Logger = logging.getLogger(__name__)


async def wait_some_time(wait):
    log.info(f'wait_some_time({wait}): before sleep')
    await asyncio.sleep(wait)
    log.info(f'wait_some_time({wait}): done')


async def main():
    log.info('scheduling tasks')
    await asyncio.wait([wait_some_time(wait=TASKS - i) for i in range(TASKS)])
    log.info('Done')


if __name__ == '__main__':
    f = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    asyncio.run(main())
