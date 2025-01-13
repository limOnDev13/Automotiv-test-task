"""The module responsible for model descriptions in the database."""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import JSON, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Stat(Base):
    """An ORM model for representing CPU, RAM, and ROM data."""

    __tablename__ = "stat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pc_stats: Mapped[dict] = mapped_column(JSON, nullable=False)

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return "[{time}] | {stats}".format(
            time=self.time,
            stats="; ".join(
                (f"{key}: {value}" for key, value in self.pc_stats.items())
            ),
        )

    def to_hash(self) -> Dict[str, Any]:
        """Return a one-dimensional dictionary with all fields."""
        result: Dict[str, Any] = {"time": self.time}
        result.update(self.pc_stats)
        return result
