from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu():
    keyboard = [
        [KeyboardButton(text="📚 Kurslar")],
        [KeyboardButton(text="📰 Yangiliklar")],
        [KeyboardButton(text="📝 Kursga yozilish")],
        [KeyboardButton(text="🏫 Biz haqimizda")],
        [KeyboardButton(text="❓ FAQ")],
        [KeyboardButton(text="🗫 Kommentlar")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
