#!/usr/bin/env python

import asyncio
import inspect


async def main():
    print('inside main!')


if __name__ == '__main__':
    # main is not awaitable
    print(main)
    print(f'awaitable(main) {inspect.isawaitable(main)}')
    # but main is a corouting function: calling main returns a coroutine object
    print(f'iscoroutinefunction(main) {asyncio.iscoroutinefunction(main)}')
    print('=' * 80)

    # let's call main and look at the result
    a = main()
    print(a)
    print(f'iscoroutine(main()) {asyncio.iscoroutine(a)}')
    print(f'awaitable(main()) {inspect.isawaitable(a)}')

    # a coroutine object can be run
    # observe that the print() statement inside main only gets executed now!
    print('running the coroutine!')
    asyncio.run(a)
