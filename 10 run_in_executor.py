#!/usr/bin/env python
import asyncio
import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor


counter = 0


async def update_counter(id):
    """
    Update the global counter
    """
    global counter

    log.info(f'{id}: doing some preparation')
    await asyncio.sleep(random.uniform(0, TASKS))

    val = counter
    log.info(f'{id}: previous value: {val}')

    # the sleep() below is there to represent some random processing time
    # what happens if instead og time.sleep() we use asycio.sleep()?
    time.sleep(random.uniform(1.5, 1.6))
    # await asyncio.sleep(random.uniform(1.5, 1.6))

    # now we update the counter with a new value
    val += 1
    counter = val

    log.info(f'{id}: set new value: {val}')
    log.info(f'{id}: Done!')

async def noop():
    pass

def slow_sync_call():
    time.sleep(4)

async def blocking_sync_call():
    log.info(f'blocking_sync_call: awaiting noop')
    await noop()
    log.info(f'blocking_sync_call: before blocking call')

    with ThreadPoolExecutor() as pool:
        await asyncio.get_running_loop().run_in_executor(pool, slow_sync_call)
    # instead this also works (if None is passed as pool then ThredPoolExecutor is the default
    await asyncio.get_running_loop().run_in_executor(None, slow_sync_call)

    log.info(f'blocking_sync_call: after blocking call')
    log.info(f'blocking_sync_call: awaiting noop again')
    await noop()
    log.info(f'blocking_sync_call: Done!')

TASKS = 5

log = logging.getLogger(__name__)


async def main():
    log.info('scheduling tasks')
    tasks = [asyncio.create_task(blocking_sync_call())] + [asyncio.create_task(update_counter(_)) for _ in range(TASKS)]
    log.info('tasks scheduled')

    # wait for all tasks to complete
    await asyncio.wait(tasks)
    log.info(f'Done, final value: {counter}')


if __name__ == '__main__':
    f = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)
    asyncio.run(main())
