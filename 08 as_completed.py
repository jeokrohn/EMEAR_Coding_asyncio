#!/usr/bin/env python
import asyncio
import logging
import random
import time

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
    return id, val


TASKS = 5

log = logging.getLogger(__name__)


async def main():
    coros = [update_counter(_) for _ in range(TASKS)]
    for completed in asyncio.as_completed(coros):
        id, val = await completed
        log.info(f'update_counter({id}) set the counter to {val}')
    log.info(f'Done, final value: {counter}')


if __name__ == '__main__':
    f = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.INFO)
    asyncio.run(main())
