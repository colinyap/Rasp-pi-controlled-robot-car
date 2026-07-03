"""
POSIX SharedMemory helpers for the frame buffer.
One segment is created by the main process; camera and AI attach by name.
"""

import numpy as np
from multiprocessing import shared_memory
from . import config as cfg


def create_frame_shm(name):
    """Create a new SHM segment for one RGB frame.  Returns (shm, np_array)."""
    shape = (cfg.FRAME_H, cfg.FRAME_W, 3)
    nbytes = int(np.prod(shape))
    try:
        stale = shared_memory.SharedMemory(name=name, create=False)
        stale.close()
        stale.unlink()
    except FileNotFoundError:
        pass
    shm = shared_memory.SharedMemory(name=name, create=True, size=nbytes)
    arr = np.ndarray(shape, dtype=np.uint8, buffer=shm.buf)
    arr[:] = 0
    return shm, arr


def open_frame_shm(name):
    """Attach to an existing SHM segment.  Returns (shm, np_array)."""
    shape = (cfg.FRAME_H, cfg.FRAME_W, 3)
    shm = shared_memory.SharedMemory(name=name, create=False)
    arr = np.ndarray(shape, dtype=np.uint8, buffer=shm.buf)
    return shm, arr


def read_frame(arr, lock):
    """Copy the frame out of SHM under a lock."""
    with lock:
        return arr.copy()


def write_frame(arr, frame, lock):
    """Write a captured frame into SHM under a lock."""
    with lock:
        np.copyto(arr, frame)
