import config, gspread_asyncio, logging
from aiogram import Dispatcher, Bot
from basedata import BaseData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from google.oauth2.service_account import Credentials 

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = BaseData('basedata.db')
logging.basicConfig(level=logging.INFO)

user_workspace : gspread_asyncio.AsyncioGspreadSpreadsheet = None
sh : gspread_asyncio.AsyncioGspreadSpreadsheet = None

def get_creds():
    creds = Credentials.from_service_account_file("credentials.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

