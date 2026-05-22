from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_course_keyboard(page: int, course_id: int, total_courses: int):

    nav_row = []
    if page > 0:
        nav_row.append(
            InlineKeyboardButton(text="🡄 Orqaga", callback_data=f"course_prev_{page}")
        )
    if page < total_courses - 1:
        nav_row.append(
            InlineKeyboardButton(text="Oldinga 🡆", callback_data=f"course_next_{page}")
        )

    rows = []
    if nav_row:
        rows.append(nav_row)

    rows.append(
        [
            InlineKeyboardButton(
                text="⭐ Kursni baholash", callback_data=f"review_course_{course_id}"
            )
        ]
    )

    rows.append(
        [InlineKeyboardButton(text="📝 Yozilish", callback_data=f"apply_{course_id}")]
    )

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes")],
            [InlineKeyboardButton(text="❎ Yo`q", callback_data="confirm_no")],
        ]
    )
