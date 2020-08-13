#!/usr/bin/env python
import asyncio
import logging

TASKS = 5

log = logging.getLogger(__name__)


async def wait_some_time(wait):
    log.info(f'wait_some_time({wait}): before sleep')
    # asyncio.sleep instead of time.sleep b/c we want to pass control to other tasks while waiting
    # what happens if we leave out the the "await"?
    await asyncio.sleep(wait)
    log.info(f'wait_some_time({wait}): done')


async def main():
    log.info('scheduling tasks')
    for i in range(TASKS):
        asyncio.create_task(wait_some_time(wait=TASKS - i))
    log.info('Done')


if __name__ == '__main__':
    f = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    asyncio.run(main())

    # Hold on?!?! The code terminates before the tasks actually get executed?
