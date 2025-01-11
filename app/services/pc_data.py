from typing import Tuple, Dict

import psutil

from app.utils.human_readable import readable_memory


class PCData(object):
    def __init__(self, interval: float = 1):
        self.interval = interval
        if self.interval < 1:
            self.interval = 1

    @property
    def delay(self) -> float:
        return self.interval

    @delay.setter
    def delay(self, new_interval: float) -> None:
        self.interval = new_interval
        if self.interval < 1:
            self.interval = 1

    def __cpu(self, interval: float = 1) -> float:
        return psutil.cpu_percent(self.interval)

    @classmethod
    def __ram(cls) -> Tuple[int, int]:
        memory: psutil.svmem = psutil.virtual_memory()
        return memory.available, memory.total

    @classmethod
    def __rom(cls) -> Tuple[int, int]:
        free: int = 0
        total: int = 0

        for disk in psutil.disk_partitions(all=False):
            disk_usage = psutil.disk_usage(disk.mountpoint)
            free += disk_usage.free
            total += disk_usage.total

        return free, total

    @property
    def data_dict(self) -> Dict[str, str]:
        ram_free, ram_total = self.__ram()
        rom_free, rom_total = self.__rom()
        return {
            "CPU": f"{self.__cpu()}",
            "RAM": f"{readable_memory(ram_free)} / {readable_memory(ram_total)}",
            "ROM": f"{readable_memory(rom_free)} / {readable_memory(rom_total)}",
        }
