"""
io_concurrency.py
-----------------
Demonstration of I/O-bound concurrency in Python: the *other* major way to speed
up a program. Where ``parallel.py`` fights a **CPU-bound** problem (heavy number
crunching) with multiple cores, this notebook fights an **I/O-bound** problem
(waiting on the network) by overlapping the waiting.

We download the same site ``N`` times four ways and time each:
synchronous, threading, asyncio, and multiprocessing.

Adapted from Real Python, "Speed Up Your Python Program With Concurrency"
(https://realpython.com/python-concurrency/). Structured as a notebook for
students new to concurrency.
"""

# %% [markdown]
# # I/O-bound Concurrency: Synchronous vs. Threading vs. Asyncio vs. Multiprocessing
# When a program spends its time **waiting** (network requests, disk, a database)
# rather than **computing**, adding CPU cores barely helps — the cores would just
# sit idle waiting too. Instead we want to *overlap the waiting*: start the next
# download before the previous one has finished.
#
# The key fact that makes this work: while a thread waits on I/O, Python **releases
# the GIL**, so other threads can run. That is why threading — useless for the
# CPU-bound work in `parallel.py` — is a big win here.

# %%
# --- 1. Imports ---
import asyncio
import concurrent.futures
import multiprocessing
import threading
from time import time

import aiohttp
import requests

# %% [markdown]
# ## The workload
# Download two small pages many times. Real network latency is what we are
# overlapping, so the same URLs repeated is a perfectly good benchmark.

# %%
# --- 2. The list of sites to download ---
SITES = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
] * 80

# %% [markdown]
# ## 1) Synchronous version (baseline)
# One request at a time. Each `session.get(...)` blocks until the whole response
# has arrived before the next one even starts, so the total time is the *sum* of
# all the waits. A reused `Session` keeps the TCP connection open across requests.

# %%
def download_site_sync(url, session):
    with session.get(url) as response:
        return len(response.content)


def download_all_sites_sync(sites):
    with requests.Session() as session:
        return [download_site_sync(url, session) for url in sites]


# %% [markdown]
# ## 2) Threading version
# A `ThreadPoolExecutor` runs several downloads at once. While one thread waits on
# the network the GIL is free, so the others make progress — the waits overlap.
# `requests.Session` is **not** thread-safe, so we give each thread its own via
# `threading.local()`.

# %%
thread_local = threading.local()


def get_session_for_thread():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site_threaded(url):
    session = get_session_for_thread()
    with session.get(url) as response:
        return len(response.content)


def download_all_sites_threaded(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        return list(executor.map(download_site_threaded, sites))


# %% [markdown]
# ## 3) Asyncio version
# A single thread runs an event loop. Each `await session.get(...)` voluntarily
# hands control back to the loop while it waits, so one thread juggles hundreds of
# in-flight requests. `asyncio.gather` schedules them all and waits for the lot.
# This needs an async HTTP library (`aiohttp`) — plain `requests` cannot `await`.

# %%
async def download_site_async(session, url):
    async with session.get(url) as response:
        return len(await response.read())


async def download_all_sites_async(sites):
    async with aiohttp.ClientSession() as session:
        tasks = [download_site_async(session, url) for url in sites]
        return await asyncio.gather(*tasks, return_exceptions=True)


# %% [markdown]
# ## 4) Multiprocessing version — the *wrong* tool here
# This is the hero of `parallel.py` (CPU-bound work), shown here for contrast.
# Each process gets its own Python interpreter and its own `Session`. It *does*
# overlap the downloads, but spawning processes and shipping data between them is
# pure overhead when the real cost is network waiting — so it loses to threads and
# asyncio. The worker and its session live at module top level so they can be
# pickled and inherited by the pool workers.

# %%
session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site_mp(url):
    with session.get(url) as response:
        return len(response.content)


def download_all_sites_mp(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        return pool.map(download_site_mp, sites)


# %% [markdown]
# ## Race them
# Expect roughly: **Synchronous ≫ Multiprocessing > Threading ≈ Asyncio**.
# The lesson: for I/O-bound work, overlap the *waiting* (threads / asyncio); for
# CPU-bound work, add *cores* (multiprocessing) — see `parallel.py`.

# %%
if __name__ == "__main__":
    for name, run in [
        ("Synchronous", lambda: download_all_sites_sync(SITES)),
        ("Threading", lambda: download_all_sites_threaded(SITES)),
        ("Asyncio", lambda: asyncio.run(download_all_sites_async(SITES))),
        ("Multiprocessing", lambda: download_all_sites_mp(SITES)),
    ]:
        start = time()
        run()
        print(f"{name:16s}: downloaded {len(SITES)} sites in {time() - start:.2f} s")
