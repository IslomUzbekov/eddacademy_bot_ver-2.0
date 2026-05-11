from html import escape


def get_course_badges(course: dict) -> str:
    if course.get("is_free"):
        return "🟩 Free course"
    if course.get("is_career_path"):
        return "🟦 Career path"
    if course.get("is_skill_path"):
        return "🟪 Skill path"
    if course.get("is_cert_path"):
        return "🟨 Certification path"
    return "⬜ Course"


def format_course(course: dict, rating: float) -> str:
    badge = get_course_badges(course)
    title = course.get("title", "Course")
    desc = (course.get("description") or "").strip()
    short = desc[:220] + ("..." if len(desc) > 220 else "")

    level = course.get("level") or "Beginner"
    duration = course.get("duration") or "-"
    price = course.get("price") or "-"

    includes_courses = course.get("includes_courses")
    has_certificate = course.get("has_certificate")

    dots = "-" * 26

    lines = []
    lines.append(f"<code>{badge:}          | Rating: {rating:.1f}</code>")
    lines.append("")
    lines.append(f"<b>{title}</b>")
    lines.append(short)
    lines.append("")
    lines.append(f"Narx: <b>{price} so'm</b>")

    if includes_courses > 1:
        lines.append(dots)
        lines.append(f"Includes: <b>{includes_courses} Courses</b>")

    if has_certificate:
        lines.append(dots)
        lines.append("🏅 With <b>Certificate</b>")

    lines.append(dots)
    lines.append(f"<code><b>{level:}</b>          | <b>{duration} oy</b></code>")

    return "\n".join(lines)


def format_news(news: dict) -> str:

    title = escape(news["title"])
    text = escape(news["text"])
    date = escape(news["date"])

    return (
        "📰 Yangiliklar\n"
        f"🗓 <b>{date}</b>\n\n"
        f"🚀 <b>{title}</b>\n\n"
        f"{text}\n\n"
        "━━━━━━━━━━━━━━━"
    )


def format_faq(faq: dict) -> str:

    question = escape(faq["question"])
    answer = escape(faq["answer"])

    return "❓ FAQ\n" f"❓ <b>{question}</b>\n\n" f"{answer}"


def format_about(about: dict) -> str:

    title = escape(about["title"])
    description = escape(about["description"])

    return (
        "🏛 Biz haqimizda\n"
        f"🔥 <b>{title}</b>\n\n"
        f"{description}\n\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🚀 Engineering • Design • Development"
    )
