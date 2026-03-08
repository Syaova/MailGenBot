import aiosqlite
import time
from config import DB

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            requests INTEGER,
            last_reset INTEGER
        )
        """)
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return await cursor.fetchone()

async def create_user(user_id: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, 0, int(time.time())))
        await db.commit()

async def update_user_requests(user_id: int, requests: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET requests=? WHERE user_id=?", (requests, user_id))
        await db.commit()

async def reset_limit_if_needed(user_id: int, limit_reset_hours: int):
    user = await get_user(user_id)
    if user:
        last_reset = user[2]
        if time.time() - last_reset >= limit_reset_hours*3600:
            await update_user_requests(user_id, 0)
            async with aiosqlite.connect(DB) as db:
                await db.execute("UPDATE users SET last_reset=? WHERE user_id=?", (int(time.time()), user_id))
                await db.commit()
