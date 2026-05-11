from aiogram import types
from keyboards.main import get_main_menu


async def start_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Bu - eddacademy_bot!\n"
        "Bu bot orqali siz bizning kurslarimiz haqida ma'lumot olishingiz va yangiliklarimizni kuzatib borishingiz mumkin.\n\n"
        "Iltimos, o'zingizga kerakli bo'lgan bo'limni tanlang:",
        reply_markup=get_main_menu(),
    )
