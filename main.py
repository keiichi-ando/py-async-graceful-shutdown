from datetime import datetime as dt
import random
import time
import asyncio

DEBUG = True
API = 'http://hogehogeo.com/api/test'
SEP = '-' * 30


def log_d(msg: str):
    """ display log for debug mode

    Args:
        msg (str): [description]
    """
    if DEBUG:
        print(f"  {dt.now().strftime('%X')}  {msg}")


async def post_data(seq_no: int, interval_sec: int = 2):
    """ API data post duummy

    Args:
        seq_no (int): sequence number
        interval_sec (int, optional): dummy wait. Defaults to 2.
    """

    log_d(f"async_foo [{seq_no}] started , wait {interval_sec}sec")
    _start_at = dt.now().strftime('%X')

    # async with aiohttp.ClientSession() as session:
    #     async with session.get(API + '/' + str(val)) as resp:
    #         _res = await resp.json()
    #         log_d(f"async_foo [{index}] done. " + json.dumps(_res))

    await asyncio.sleep(interval_sec)
    log_d(f'async_foo [{seq_no}] done. {{"Response" : "OK", "request-at": {_start_at} }}')


async def main():
    _seq = 0

    while True:

        log_d(f"Start [{_seq}] {SEP}")
        _random_wait_sec = random.randint(1, 5)
        asyncio.ensure_future(post_data(_seq, _random_wait_sec))

        await asyncio.sleep(1)  # wait for test run

        _seq += 1

    log_d('loop stop')


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    coro = main()

    try:
        loop.run_until_complete(coro)
    except KeyboardInterrupt:
        coro.close()
        tasks = asyncio.all_tasks(loop)
        expensive_tasks = {task for task in tasks if task._coro.__name__ != coro.__name__}

        print(f" [KeyboardInterrupt] - Pending {len(expensive_tasks)} outstanding tasks")
        loop.run_until_complete(asyncio.gather(*expensive_tasks))

    finally:
        loop.close()
