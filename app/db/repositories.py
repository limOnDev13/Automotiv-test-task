"""The module responsible for database queries."""

from typing import Any, Dict, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .models import Stat


class HistoryRepository(object):
    """Repository for queries to the stat table."""

    @connection
    async def save(self, data: Dict[str, Any], session: AsyncSession) -> None:
        """Save data about the CPU, RAM, and ROM in the database."""
        stat = Stat(**data)
        session.add(stat)
        await session.commit()

    @connection
    async def get_all(self, session: AsyncSession) -> Sequence[Stat]:
        """Get time-sorted records from the database."""
        history_q = await session.execute(select(Stat).order_by(Stat.c.time))
        return history_q.scalars().all()
