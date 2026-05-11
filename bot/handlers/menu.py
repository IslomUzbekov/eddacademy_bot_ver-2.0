from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from formatters import format_course
from keyboards.course_inline import get_confirm_keyboard, get_course_keyboard
from services.api import ApiService
from states.application import ApplicationStates


class CourseStates(StatesGroup):
    page = State()


async def courses_handler(message: types.Message, state: FSMContext):
    courses = ApiService.get_courses()
    if not courses:
        await message.answer("Kurslar haqida ma'lumotlar vaqtincha mavjud emas.")
        return
    await state.set_state(CourseStates.page)
    await state.update_data(courses=courses, page=0)
    await show_course_page(message, page=0, state=state)


async def show_course_page(message: types.Message, page: int, state: FSMContext):
    data = await state.get_data()
    courses = data.get("courses", [])

    if not courses:
        await message.answer("Kurslar topilmadi.")
        return
    if page < 0 or page >= len(courses):
        return

    course = courses[page]
    rating = course.get("rating", 0.0)
    caption = format_course(course, rating)
    kb = get_course_keyboard(page, course["id"], len(courses))

    # photo_url = (
    #     course.get("photo")
    #     or course.get("image")
    #     or course.get("image_url")
    #     or PLACEHOLDER_URL
    # )
    # if not str(photo_url).startswith(("http://", "https://")):
    #     photo_url = PLACEHOLDER_URL
    # try:
    #     if photo_url:
    #         await message.bot.send_photo(
    #             chat_id=message.chat.id,
    #             photo=photo_url,
    #             caption=caption,
    #             parse_mode="HTML",
    #             reply_markup=kb,
    #         )
    #     else:
    #         await message.answer(caption, parse_mode="HTML", reply_markup=kb)
    # except Exception:
    await message.answer(caption, parse_mode="HTML", reply_markup=kb)

    await state.update_data(page=page, current_course_id=course["id"])


async def news_handler(message: types.Message):
    news = ApiService.get_news()
    if not news:
        await message.answer("Yangiliklar vaqtincha mavjud emas.")
        return

    text = "📰 Oxirgi yangiliklar:\n\n"
    for item in news[:3]:  # первые 3
        text += f"• {item['title']}\n  {item['text'][:150]}...\n\n"

    await message.answer(text)


async def faq_handler(message: types.Message):
    faq = ApiService.get_faq()
    if not faq:
        await message.answer("FAQ vaqtincha mavjud emas.")
        return

    text = "❓ Ko'p so'raladigan savollar:\n\n"
    for item in faq[:5]:  # Показываем только первые 5 вопросов
        text += f"• {item['question']}\n  {item['answer'][:100]}...\n\n"

    await message.answer(text)


async def about_handler(message: types.Message):
    about = ApiService.get_about()
    if not about:
        await message.answer("Biz haqimizda ma'lumotlar vaqtincha mavjud emas.")
        return

    text = "ℹ️ Biz haqimizda:\n\n"
    for item in about[:3]:  # первые 3
        text += f"• {item['title']}\n  {item['content'][:150]}...\n\n"

    await message.answer(text)


async def apply_handler(message: types.Message, state: FSMContext):
    await state.set_state(ApplicationStates.full_name)
    await message.answer("FIO kiriting:")


async def full_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await state.set_state(ApplicationStates.phone)
    await message.answer("Telefon raqamingizni kiriting:")


async def phone_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(ApplicationStates.age)
    await message.answer("Yoshingizni kiriting:")


async def age_handler(message: types.Message, state: FSMContext):
    age_text = message.text.strip()
    if not age_text.isdigit():
        await message.answer("Yosh faqat raqam bo'lishi kerak. Qayta kiriting:")
        return

    await state.update_data(age=int(age_text))
    await state.set_state(ApplicationStates.course)
    await message.answer("Qiziqqan kurs nomini kiriting:")


async def course_handler(message: types.Message, state: FSMContext):
    await state.update_data(course=message.text.strip())
    data = await state.get_data()

    await state.set_state(ApplicationStates.confirm)
    await message.answer(
        "Ma'lumotlarni tasdiqlaysizmi?\n\n"
        f"FIO: {data['full_name']}\n"
        f"Telefon: {data['phone']}\n"
        f"Yosh: {data['age']}\n"
        f"Kurs: {data['course']}",
        reply_markup=get_confirm_keyboard(),
    )

async def confirm_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "confirm_no":
        await state.clear()
        await callback.message.answer("Ariza bekor qilindi.")
        await callback.answer()
        return

    data = await state.get_data()
    payload = {
        "full_name": data["full_name"],
        "phone": data["phone"],
        "age": data["age"],
        "course": data.get("selected_course_id"),
        "comment": f"Requested course: {data['course']}",
    }

    created = ApiService.post_application(payload)
    if not created:
        await callback.message.answer("Ariza yuborishda hatolik yuz berdi.")
        await state.clear()
        await callback.answer()
        return

    await callback.message.answer("Arizangiz qabul qilindi.")
    await state.clear()
    await callback.answer()

# async def confirm_handler(message: types.Message, state: FSMContext):
#     answer = message.text.strip().lower()
#     if answer not in {"ha", "yo'q", "yoq", "yes", "no"}:
#         await message.answer(
#             "Iltimos, `ha` yoki `yo'q` deb javob bering.", parse_mode="Markdown"
#         )
#         return

#     if answer in {"yo'q", "yoq", "no"}:
#         await state.clear()
#         await message.answer("Ariza bekor qilindi.")
#         return

#     data = await state.get_data()
#     payload = {
#         "full_name": data["full_name"],
#         "phone": data["phone"],
#         "age": data["age"],
#         "course": data.get("selected_course_id"),
#         "comment": f"Requested course: {data['course']}",
#     }
#     created = ApiService.post_application(payload)

#     if not created:
#         await message.answer(
#             "Ariza yuborishda xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
#         )
#         await state.clear()
#         return

#     bot = message.bot
#     try:
#         await bot.send_message(
#             settings.ADMIN_CHAT_ID,
#             "📥 Yangi ariza:\n\n"
#             f"FIO: {data['full_name']}\n"
#             f"Telefon: {data['phone']}\n"
#             f"Yosh: {data['age']}\n"
#             f"Kurs: {data['course']}",
#         )
#     except Exception:
#         pass
#     await message.answer("Arizangiz qabul qilindi. Tez orada siz bilan bog'lanamiz.")
#     await state.clear()


async def course_callback(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data

    if action.startswith("course_next_"):
        page = int(action.split("_")[2])
        try:
            await callback.message.delete()
        except Exception:
            pass
        await show_course_page(callback.message, page=page + 1, state=state)

    elif action.startswith("course_prev_"):
        page = int(action.split("_")[2])
        try:
            await callback.message.delete()
        except Exception:
            pass
        await show_course_page(callback.message, page=page - 1, state=state)

    elif action.startswith("apply_"):
        course_id = int(action.split("_")[1])
        await state.update_data(selected_course_id=course_id)
        await state.set_state(ApplicationStates.full_name)
        await callback.message.answer("FIO kiriting:")

    await callback.answer()
