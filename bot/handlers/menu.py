import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from formatters import format_course
from keyboards.course_inline import get_confirm_keyboard, get_course_keyboard
from services.api import ApiService
from states.application import ApplicationStates, CourseStates, ReviewStates

logger = logging.getLogger(__name__)


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

    elif action.startswith("review_course_"):
        course_id = int(action.split("_")[-1])
        await state.update_data(review_course_id=course_id)
        await state.set_state(ReviewStates.course_score)
        await callback.message.answer("Kursni 1 dan 5 gacha baholang:")

    await callback.answer()


async def institution_review_start(message: types.Message, state: FSMContext):
    await state.set_state(ReviewStates.institution_text)
    await message.answer("O'quv markazi haqida uz fikringizni qoldiring:")


async def institution_review_text(message: types.Message, state: FSMContext):
    text = message.text.strip()

    payload = {
        "user_id": str(message.from_user.id),
        "review": text,
    }
    logger.debug("Institution review payload: %s", payload)
    saved = ApiService.post_institution_review(payload)

    if saved:
        await message.answer("Rahmat, sizning fikringiz qabul qilindi!")
    else:
        await message.answer("Ma'lumotni saqlashda xatolik yuz berdi.")

    await state.clear()


async def course_review_score(message: types.Message, state: FSMContext):
    text = (message.text or "").strip()
    if text not in {"1", "2", "3", "4", "5"}:
        await message.answer("Iltimos, 1 dan 5 gacha raqam yuboring.")
        return

    await state.update_data(course_score=int(text))
    await state.set_state(ReviewStates.course_text)
    await message.answer("Endi kurs haqida izoh qoldiring:")


async def course_review_text(message: types.Message, state: FSMContext):
    text = (message.text or "").strip()
    data = await state.get_data()

    payload = {
        "course": int(data["review_course_id"]),
        "user_id": str(message.from_user.id),
        "score": int(data["course_score"]),
        "comment": text,
    }

    logger.debug("Course review payload: %s", payload)
    saved = ApiService.post_course_review(payload)
    if saved:
        await message.answer("Rahmat! Kurs bo'yicha fikringiz saqlandi.")
    else:
        await message.answer("Xatolik yuz berdi. Keyinroq qayta urinib ko'ring.")

    await state.clear()
