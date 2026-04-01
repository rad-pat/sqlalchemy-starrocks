import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

async def check_connect_query():
    eng = create_async_engine("starrocks+asyncmy://root:@localhost:9030/test_db")

    async with eng.connect() as conn:
        result = await conn.execute(sqlalchemy.text("SHOW TABLES"))
        print(result.fetchall())


asyncio.run(check_connect_query())