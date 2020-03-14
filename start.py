import asyncio
import os
import ctypes
from utilities import colors
from typing import Callable, TypeVar, Any, List

ctypes.windll.kernel32.SetConsoleTitleW("CovidMap - Console")
os.system('mode con: cols=123 lines=40')

#utility for workers
T = TypeVar('T')




#main functions

async def run_jobs(function: Callable[[T], Any], job_data: List[T], max_workers: int = 2):
    running = set()
    count = 0
    while job_data:
        while job_data and len(running) < max_workers:
            count = count + 1
            job = job_data.pop(0)
            task = function(job, count)
            running.add(task)
        finished, running = await asyncio.wait(running, return_when=asyncio.FIRST_COMPLETED)
    if running:
        await asyncio.wait(running, return_when=asyncio.ALL_COMPLETED)


async def start_scripts()