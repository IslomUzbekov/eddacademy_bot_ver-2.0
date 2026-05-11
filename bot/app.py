import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers.menu import (
    about_handler,
    age_handler,
    apply_handler,
    # confirm_handler,
    confirm_callback,
    course_callback,
    course_handler,
    courses_handler,
    faq_handler,
    full_name_handler,
    news_handler,
    phone_handler,
)
from handlers.start import start_handler
from states.application import ApplicationStates

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрируем хендлеры
dp.message.register(start_handler, Command(commands=["start", "help"]))

dp.message.register(courses_handler, F.text == "📚 Kurslar")
dp.message.register(news_handler, F.text == "📰 Yangiliklar")
dp.message.register(
    apply_handler,
    F.text == "📝 Kursga yozilish",
)
dp.message.register(about_handler, F.text == "🏛 Biz haqimizda")
dp.message.register(faq_handler, F.text == "❓ FAQ")
dp.message.register(full_name_handler, ApplicationStates.full_name)
dp.message.register(phone_handler, ApplicationStates.phone)
dp.message.register(age_handler, ApplicationStates.age)
dp.message.register(course_handler, ApplicationStates.course)
# dp.message.register(confirm_handler, ApplicationStates.confirm)
dp.callback_query.register(confirm_callback, F.data.in_(["confirm_yes", "confirm_no"]))
dp.callback_query.register(course_callback, F.data.startswith(("course_", "apply_")))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
