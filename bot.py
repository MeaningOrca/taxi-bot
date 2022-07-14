from aiogram import executor
from dispatcher import dp
from database import Database
import handlers
import filters

db = Database('data.db')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=db.con.close)
