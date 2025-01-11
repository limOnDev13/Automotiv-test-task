"""The module responsible for receiving information about the CPU, RAM, and ROM."""

from typing import Dict, Tuple

import psutil

from app.utils.human_readable import readable_memory


class PCData(object):
    """
    A class for getting information about the PC load on the CPU, RAM, and ROM.

    Args:
        interval (float) - The time interval during which the CPU usage is measured.
        It cannot be less than 1 second.
    """

    def __init__(self, interval: float = 1):
        """
        Initialize the class.

        :param interval: the time interval during which the CPU usage is measured.
        It cannot be less than 1 second.
        """
        self.__interval = interval
        if self.__interval < 1:
            self.__interval = 1

    @property
    def delay(self) -> float:
        """Get self.__interval."""
        return self.__interval

    @delay.setter
    def delay(self, new_interval: float) -> None:
        """Set self.__interval."""
        if isinstance(new_interval, float | int):
            self.__interval = new_interval
            if self.__interval < 1:
                self.__interval = 1
        else:
            self.__interval = 1

    def __cpu(self) -> float:
        """Return the CPU usage as a percentage."""
        return psutil.cpu_percent(self.__interval)

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
            "CPU": f"{self.__cpu()}",
            "RAM": f"{readable_memory(ram_free)} / {readable_memory(ram_total)}",
            "ROM": f"{readable_memory(rom_free)} / {readable_memory(rom_total)}",
        }
