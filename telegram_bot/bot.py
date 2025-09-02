import asyncio
from loader import dp, bot

# --- HANDLERS ---

import callback_queries
import handlers

# --- RUN ---
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
