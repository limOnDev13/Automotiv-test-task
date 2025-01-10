from typing import Tuple

import psutil


class PCData(object):
    @classmethod
    def cpu(cls, interval: float = 1) -> float:
        if interval < 1:
            interval = 1
        return psutil.cpu_percent(interval)

    @classmethod
    def ram(cls) -> Tuple[int, int]:
        memory: psutil.svmem = psutil.virtual_memory()
        return memory.available, memory.total

    @classmethod
    def rom(cls) -> Tuple[int, int]:
        used: int = 0
        total: int = 0

        for disk in psutil.disk_partitions(all=False):
            disk_usage = psutil.disk_usage(disk.mountpoint)
            used += disk_usage.used
            total += disk_usage.total

        return used, total
