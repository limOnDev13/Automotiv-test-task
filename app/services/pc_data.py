"""The module responsible for receiving information about the CPU, RAM, and ROM."""

from typing import Dict, Tuple

import psutil

from app.utils.human_readable import readable_memory


class PCData(object):
    """A class for getting information about the PC load on the CPU, RAM, and ROM."""

    @classmethod
    def __cpu(cls) -> float:
        """Return the CPU usage as a percentage."""
        return psutil.cpu_percent()

    @classmethod
    def __ram(cls) -> Tuple[int, int]:
        """Return free and total ram."""
        memory: psutil.svmem = psutil.virtual_memory()
        return memory.available, memory.total

    @classmethod
    def __rom(cls) -> Tuple[int, int]:
        """Return free and total rom."""
        free: int = 0
        total: int = 0

        for disk in psutil.disk_partitions(all=False):
            disk_usage = psutil.disk_usage(disk.mountpoint)
            free += disk_usage.free
            total += disk_usage.total

        return free, total

    @property
    def data_dict(self) -> Dict[str, str]:
        """Return information about CPU, RAM, and ROM usage as a dictionary."""
        ram_free, ram_total = self.__ram()
        rom_free, rom_total = self.__rom()
        return {
            "CPU": f"{self.__cpu()}%",
            "RAM": f"{readable_memory(ram_free)} / {readable_memory(ram_total)}",
            "ROM": f"{readable_memory(rom_free)} / {readable_memory(rom_total)}",
        }
