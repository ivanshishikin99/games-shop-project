import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy import select

from core.config import settings
from core.models.verification_token import VerificationToken
from utils.db_helper import db_helper


async def delete_tokens(interval: int = 3600):
    logging.basicConfig(
        level=settings.logging_config.log_level,
        format=settings.logging_config.log_format,
    )
    log = logging.getLogger()
    while True:
        async with db_helper.session_maker() as session:
            statement = select(VerificationToken).where(
                datetime.now() - VerificationToken.created_at > timedelta(hours=1)
            )
            tokens = await session.execute(statement)
            tokens = tokens.scalars().all()
            for i in tokens:
                await session.delete(i)
                await session.commit()
            log.info("Verification table has been cleaned.")
        await asyncio.sleep(delay=interval)
