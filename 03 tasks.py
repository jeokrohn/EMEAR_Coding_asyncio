#!/usr/bin/env python
import asyncio
import logging
import time

TASKS = 5

log = logging.getLogger(__name__)


async def wait_some_time(wait):
    log.info(f'wait_some_time({wait}): before sleep')
    await asyncio.sleep(wait)
    log.info(f'wait_some_time({wait}): done')


async def main():
    log.info('scheduling tasks')
    tasks = [asyncio.create_task(wait_some_time(wait=TASKS - i)) for i in range(TASKS)]
    log.info('tasks scheduled; sleeping...')

    # sleep some time. Observe: async tasks only start executing as soon as we await!
    time.sleep(10)

    # equivalent to joining threads, ALL_COMPLETED is the default
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

    # instead we could also simply wait for all current tasks .. with the exception of the currently running one
    # You typically use this if coroutines are not awaited for, but simply scheduled by create_task(), and you didn't
    # track the tasks
    current_task = asyncio.current_task()
    tasks = [t for t in asyncio.all_tasks() if t != current_task]
    if tasks:
        done, pending = await asyncio.wait(tasks)
    log.info('Done')


if __name__ == '__main__':
    f = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)

    asyncio.run(main())
