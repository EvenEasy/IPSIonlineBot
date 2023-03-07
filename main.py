import create_bot, config, asyncio
from aiogram import executor, types
from create_bot import dp
from handlers import user, admin

user.register_handlers(dp)
admin.register_handlers(dp)

async def coro():

    gc = await create_bot.agcm.authorize()
    sh = await gc.open_by_key(config.GOOGLESHEETSKEY)
    create_bot.user_workspace = await sh.get_worksheet(0)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(coro())
    executor.start_polling(
        dp,
        loop=loop,
        skip_updates=True
    )