import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8835439811:AAGt1d2m5OYxIrQoJoSwto2KpDDlIP5gQ4s"
PDF_FILE_ID = None

QUESTIONS = [
    {
        "text": "Вопрос 1: Как ты просыпаешься утром?",
        "options": [
            ("Бодро и с энергией, готов/а к новому дню", "П"),
            ("Нужно время и кофе чтобы 'разогнаться'", "Э"),
            ("Устало, как будто и не спал/а", "Э"),
            ("По-разному, зависит от стресса", "И"),
        ]
    },
    {
        "text": "Вопрос 2: Как выглядит твоя кожа?",
        "options": [
            ("Упругая, сияющая, доволен/а", "П"),
            ("Появились первые морщинки, хочу замедлить процесс", "М"),
            ("Сухая, тусклая, заметно постарела", "М"),
            ("Реагирует на стресс — высыпания, покраснения", "И"),
        ]
    },
    {
        "text": "Вопрос 3: Как ты оцениваешь свой уровень энергии в течение дня?",
        "options": [
            ("Стабильно высокий", "П"),
            ("К обеду заметно падает", "Э"),
            ("Постоянно чувствую усталость", "Э"),
            ("Энергия есть, но восстановление после нагрузок медленное", "И"),
        ]
    },
    {
        "text": "Вопрос 4: Как часто ты болеешь?",
        "options": [
            ("Редко, иммунитет крепкий", "П"),
            ("Пару раз в год — простуды", "И"),
            ("Часто, особенно в сезон", "И"),
            ("Не болею, но чувствую что стресс подтачивает изнутри", "Э"),
        ]
    },
    {
        "text": "Вопрос 5: Что тебя беспокоит больше всего прямо сейчас?",
        "options": [
            ("Хочу сохранить здоровье на долгие годы", "П"),
            ("Хочу выглядеть моложе и свежее", "М"),
            ("Хочу больше энергии и фокуса", "Э"),
            ("Хочу укрепить иммунитет и снизить стресс", "И"),
        ]
    },
    {
        "text": "Вопрос 6: Как обстоят дела с волосами и ногтями?",
        "options": [
            ("Всё отлично, крепкие и здоровые", "П"),
            ("Волосы стали тоньше, ногти ломаются", "М"),
            ("Заметное выпадение волос", "М"),
            ("Особо не обращаю внимания", "Э"),
        ]
    },
    {
        "text": "Вопрос 7: Как ты относишься к своему здоровью?",
        "options": [
            ("Уже активно слежу и хочу улучшить", "П"),
            ("Думаю о профилактике, хочу действовать заранее", "П"),
            ("Есть конкретные проблемы которые хочу решить", "И"),
            ("Хочу чувствовать себя лучше каждый день", "Э"),
        ]
    },
    {
        "text": "Вопрос 8: Твой образ жизни:",
        "options": [
            ("Активный спорт, правильное питание", "П"),
            ("Работа за компьютером, мало движения", "Э"),
            ("Высокий уровень стресса, ненормированный график", "И"),
            ("Хочу ухаживать за собой лучше, чем сейчас", "М"),
        ]
    },
]

RESULTS = {
    "М": {
        "title": "💛 М — Молодость и красота",
        "text": (
            "\"Твоё тело просит обновления — и это нормально\"\n\n"
            "Кожа стала чуть менее упругой. Волосы не такие густые как раньше. "
            "Ногти ломаются быстрее. Ты замечаешь эти изменения и чувствуешь что "
            "хочется что-то сделать — но не знаешь с чего начать.\n\n"
            "Это не старение — это сигнал. Твой организм просто нуждается в поддержке изнутри.\n\n"
            "Пептиды работают именно на этом уровне — они запускают естественные процессы "
            "восстановления клеток, стимулируют выработку коллагена и помогают твоему телу "
            "вспомнить как быть молодым.\n\n"
            "Никакой магии — только биохимия которая работает 🧬\n\n"
            "Что дальше? На консультации с Людмилой мы разберём твою ситуацию детально "
            "и подберём именно ту программу которая подходит тебе — с учётом возраста, "
            "образа жизни и твоих целей.\n\n"
            "Запишись на консультацию — онлайн или очно 💛"
        )
    },
    "Э": {
        "title": "⚡ Э — Энергия и продуктивность",
        "text": (
            "\"Ты устаёшь не потому что слабый/ая — а потому что ресурс на исходе\"\n\n"
            "Утром тяжело встать. К обеду энергия падает. Вечером нет сил даже на то "
            "что раньше приносило радость. Ты пьёшь кофе, терпишь, держишься — но внутри "
            "чувствуешь что это не норма.\n\n"
            "И ты прав/права. Это не норма.\n\n"
            "Хроническая усталость, снижение концентрации и медленное восстановление — "
            "это признаки того что клетки работают на износ. Пептиды помогают восстановить "
            "энергетический баланс на клеточном уровне, улучшить качество сна и вернуть "
            "тот самый ресурс который ты давно не чувствовал/а.\n\n"
            "Что дальше? На консультации с Людмилой мы разберём что именно забирает твою "
            "энергию и составим программу восстановления — шаг за шагом, без стресса.\n\n"
            "Запишись на консультацию — онлайн или очно 💛"
        )
    },
    "И": {
        "title": "🛡️ И — Иммунитет и защита",
        "text": (
            "\"Стресс — это не просто усталость. Это удар по всей системе\"\n\n"
            "Ты часто болеешь или чувствуешь что организм работает на пределе. "
            "Стресс стал фоновым — ты уже почти не замечаешь его, но тело замечает всё. "
            "Реакции на погоду, на нагрузки, на эмоции становятся острее.\n\n"
            "Иммунная система — это не просто 'защита от простуды'. Это сложная система "
            "которая регулирует всё — от настроения до скорости восстановления после "
            "болезней и нагрузок.\n\n"
            "Пептиды работают как мягкая но мощная поддержка этой системы — помогают телу "
            "восстановить баланс и снова стать устойчивым к тому что раньше выбивало из колеи.\n\n"
            "Что дальше? На консультации с Людмилой мы посмотрим на твою ситуацию целостно "
            "и подберём программу которая поможет твоему организму снова чувствовать себя защищённым.\n\n"
            "Запишись на консультацию — онлайн или очно 💛"
        )
    },
    "П": {
        "title": "🌿 П — Профилактика и долголетие",
        "text": (
            "\"Ты уже думаешь на шаг вперёд — это твоё главное преимущество\"\n\n"
            "Ты не ждёшь пока что-то сломается. Ты хочешь сохранить то что есть — "
            "энергию, здоровье, молодость — и приумножить это на годы вперёд. "
            "Это самый мудрый и самый редкий подход к здоровью.\n\n"
            "Профилактика с пептидами — это инвестиция в себя которая работает на "
            "долгосрочную перспективу. Ты не лечишь симптомы — ты поддерживаешь систему "
            "пока она работает хорошо, чтобы она работала хорошо как можно дольше.\n\n"
            "Именно такие люди в 50 выглядят на 35 — не потому что повезло, а потому "
            "что начали заботиться о себе заранее 😊\n\n"
            "Что дальше? На консультации с Людмилой мы выстроим твою личную стратегию "
            "здоровья — с учётом твоего образа жизни, целей и того где ты хочешь быть "
            "через 5-10 лет.\n\n"
            "Запишись на консультацию — онлайн или очно 💛"
        )
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [
        [InlineKeyboardButton("🧬 Пройти тест", callback_data="start_test")],
        [InlineKeyboardButton("📄 Часто задаваемые вопросы", callback_data="send_pdf")],
        [InlineKeyboardButton("💬 Связаться с Людмилой", url="https://t.me/Rudnitskaya_L")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Привет! Я помогу тебе узнать какие пептиды подходят именно тебе!\n\n"
        "Выбери с чего хочешь начать:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "send_pdf":
        await send_pdf(query, context)

    elif data == "start_test":
        context.user_data["answers"] = []
        context.user_data["question_index"] = 0
        await send_question(query, context)

    elif data.startswith("answer_"):
        category = data.split("_")[1]
        context.user_data["answers"].append(category)
        context.user_data["question_index"] += 1
        index = context.user_data["question_index"]

        if index < len(QUESTIONS):
            await send_question(query, context)
        else:
            await send_result(query, context)

    elif data == "restart":
        context.user_data.clear()
        keyboard = [
            [InlineKeyboardButton("🧬 Пройти тест", callback_data="start_test")],
            [InlineKeyboardButton("📄 Часто задаваемые вопросы", callback_data="send_pdf")],
            [InlineKeyboardButton("💬 Связаться с Людмилой", url="https://t.me/Rudnitskaya_L")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "👋 Привет! Я помогу тебе узнать какие пептиды подходят именно тебе!\n\n"
            "Выбери с чего хочешь начать:",
            reply_markup=reply_markup
        )


async def send_pdf(query, context: ContextTypes.DEFAULT_TYPE):
    global PDF_FILE_ID
    chat_id = query.message.chat_id
    keyboard = [[InlineKeyboardButton("⬅️ Назад в меню", callback_data="restart")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if PDF_FILE_ID:
            await context.bot.send_document(
                chat_id=chat_id,
                document=PDF_FILE_ID,
                caption="📄 Часто задаваемые вопросы о пептидах",
                reply_markup=reply_markup
            )
        else:
            with open("peptides_faq.pdf", "rb") as pdf_file:
                message = await context.bot.send_document(
                    chat_id=chat_id,
                    document=pdf_file,
                    caption="📄 Часто задаваемые вопросы о пептидах",
                    reply_markup=reply_markup
                )
                PDF_FILE_ID = message.document.file_id
    except Exception as e:
        logger.error(f"Ошибка при отправке PDF: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="😔 Документ временно недоступен. Попробуй позже.",
            reply_markup=reply_markup
        )


async def send_question(query, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data["question_index"]
    question = QUESTIONS[index]
    total = len(QUESTIONS)

    keyboard = [
        [InlineKeyboardButton(option[0], callback_data=f"answer_{option[1]}")]
        for option in question["options"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"📊 Вопрос {index + 1} из {total}\n\n{question['text']}",
        reply_markup=reply_markup
    )


async def send_result(query, context: ContextTypes.DEFAULT_TYPE):
    answers = context.user_data["answers"]
    scores = {"М": 0, "Э": 0, "И": 0, "П": 0}
    for answer in answers:
        scores[answer] += 1

    winner = max(scores, key=scores.get)
    result = RESULTS[winner]

    keyboard = [
        [InlineKeyboardButton("💬 Записаться на консультацию", url="https://t.me/Rudnitskaya_L")],
        [InlineKeyboardButton("🔄 Пройти тест заново", callback_data="restart")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"🎯 Твой результат:\n\n{result['title']}\n\n{result['text']}",
        reply_markup=reply_markup
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
