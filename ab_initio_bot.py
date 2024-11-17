from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, filters

# Этапы выбора
START, LANGUAGE, ACTION, SELECTION_STAGE = range(4)

# Словари для сообщений
texts = {
    'ru': {
        'start': 'Выберите язык / Тілді таңдаңыз:',
        'select_action': 'Выберите действие:',
        'requirement': (
            "Требования:\n"
            "- Гражданство: Гражданство Казахстана\n"
            "- Возраст: 18-34 года\n"
            "- Образование: Среднее или среднеспециальное образование\n"
            "- Уровень английского: Intermediate (IELTS Academic 6.0 или TOEFL IBT 79)\n"
            "- Знания: Базовые знания математики и физики (школьный уровень)\n"
            "- Здоровье: Соответствие медицинским требованиям (ВЛЭК)\n"
            "- Паспорт: Действующий паспорт\n"
            "- Виза: Соответствие требованиям для получения шенгенской визы"
        ),
        'stages': 'ЭТАПЫ ОТБОРА:',
        'vlek': (
            "ВЛЭК — врачебно-лётная экспертная комиссия, определяющая соответствие здоровья авиаспециалиста "
            "требованиям гражданской авиации.\n"
            "Адреса и контакты:\n"
            "Алматы: ул. Беимбета Майлина 32, терапевт: 257-31-56\n"
            "Астана: ул. Туркестан 8/1, контакты: 87754549398\n"
            "Сертификат 1 класса необходимо предоставить до финального этапа отбора."
        ),
        'final_selection': (
            "Финальный отбор:\n"
            "День 1: Лётный симулятор Boeing 737\n"
            "День 2: Групповое задание и персональное интервью\n"
            "Место проведения: Алматы, 2 дня\n"
            "Язык: английский\n"
            "Организатор: EPST (European Pilot Selection & Training)\n"
            "Необходимые документы: сертификаты IELTS 6.0/TOEFL 79, ВЛЭК, справка о несудимости, паспорт.\n"
            "Результаты: Pass — успешно прошёл, Back in one year — повторная подача через год, Fail — не прошёл."
        ),
        'after_selection': (
            "После прохождения отбора:\n"
            "В случае успеха, вы будете отправлены в одну из лётных школ Европы:\n"
            "1. AFTA (Ирландия)\n"
            "2. FTE (Испания)\n"
            "3. PATRIA (Финляндия)\n"
            "Выбор школы невозможен, распределение зависит от свободных мест."
        ),
        'contact': 'Связь: @maxverstappenabinitio - @tsaruse.',
        'file_description': 'Вот файл с информацией на русском языке.',
        'stages_buttons': ['Тест английского языка', 'SHL', 'COMPASS тест', 'CPP'],
        'stages_buttons_map': {
            'Тест английского языка': (
                "Тест по английскому языку (Intermediate) проводится при отсутствии сертификата IELTS 6.0 или TOEFL 79.\n"
                "Тест: 35 вопросов, 30 минут, грамматика и словарный запас.\n"
                "Для Алматы и Астаны — в офисах Air Astana, для других городов — онлайн."
            ),
            'SHL': (
                "SHL тесты: психометрические тесты на вербальные и числовые способности.\n"
                "Вербальный тест: анализ текстов и выбор правильных ответов.\n"
                "Числовой тест: математические операции и выбор правильного ответа.\n"
                "Подробности и пробный тест на сайте www.shltools.com."
            ),
            'COMPASS тест': (
                "COMPASS тест: проверка ключевых способностей пилота.\n"
                "Модули: координация рук/глаз, память, математика, пространственное ориентирование,\n"
                "выполнение нескольких задач одновременно.\n"
                "Также тест по авиационному английскому и технический тест по физике."
            ),
            'CPP': (
                "CPP тест: психологический тест для выявления личностных качеств.\n"
                "Продолжительность: 3 часа.\n"
                "Рекомендация: не думать долго над вопросом и не пытаться обмануть систему."
            ),
        }
    },
    'kz': {
        'start': 'Тілді таңдаңыз / Выберите язык:',
        'select_action': 'Әрекетті таңдаңыз:',
        'requirement': (
            "Талаптар:\n"
            "- Азаматтық: Қазақстан азаматтығы\n"
            "- Жасы: 18-34 жас\n"
            "- Білім: Орта немесе орта арнаулы білім\n"
            "- Ағылшын тілі деңгейі: Intermediate (IELTS Academic 6.0 немесе TOEFL IBT 79)\n"
            "- Білімдер: Математика және физика негіздері (мектеп деңгейі)\n"
            "- Денсаулық: ВЛЭК талаптарына сәйкестігі\n"
            "- Паспорты: Қазіргі уақытта жарамды паспорт\n"
            "- Виза: Шенген визасын алу талаптарына сәйкестігі"
        ),
        'stages': 'ІРІКТЕУ КЕЗЕҢДЕРІ:',
        'vlek': (
            "ВЛЭК — дәрігерлік-ұшқыштық сараптамалық комиссия, авиация қызметкерінің денсаулығын "
            "азаматтық авиация талаптарына сәйкестігін анықтайды.\n"
            "Мекенжайлар мен байланыс деректері:\n"
            "Алматы: Бейімбет Майлин көшесі 32, терапевт: 257-31-56\n"
            "Астана: Түркістан көшесі 8/1, байланыс: 87754549398\n"
            "1-ші класс сертификатын финалдық іріктеу кезеңіне дейін ұсыну қажет."
        ),
        'final_selection': (
            "Қорытынды іріктеу:\n"
            "1-күн: Лёттік симулятор Boeing 737\n"
            "2-күн: Топтық тапсырмалар мен жеке сұхбат\n"
            "Өтетін орны: Алматы, 2 күн\n"
            "Тіл: ағылшын\n"
            "Ұйымдастырушы: EPST (European Pilot Selection & Training)\n"
            "Қажетті құжаттар: IELTS 6.0/TOEFL 79 сертификаттары, ВЛЭК, қылмыстық істің жоқтығы туралы анықтама, паспорт.\n"
            "Нәтижелер: Pass — табысты өтті, Back in one year — бір жылдан кейін қайтадан өту, Fail — өтпеді."
        ),
        'after_selection': (
            "Іріктеуден өткеннен кейін:\n"
            "Егер іріктеу сәтті өтсе, сізді Еуропаның бір лёттік мектебіне жіберіледі:\n"
            "1. AFTA (Ирландия)\n"
            "2. FTE (Испания)\n"
            "3. PATRIA (Финляндия)\n"
            "Мектеп таңдау мүмкін емес, бөлісу мектептегі бос орындарға байланысты жүргізіледі."
        ),
        'contact': 'Байланыс: @maxverstappenabinitio - @tsaruse.',
        'file_description': 'Қазақ тілінде ақпарат бар файл.',
        'stages_buttons': ['Ағылшын тілінен тест', 'SHL', 'COMPASS тест', 'CPP'],
        'stages_buttons_map': {
            'Ағылшын тілінен тест': (
                "Ағылшын тілінен тест (Intermediate) сертификаты жоқ жағдайда өтеді.\n"
                "Тест: 35 сұрақ, 30 минут, грамматика және лексика.\n"
                "Алматы және Астана қалаларында — Air Astana кеңселерінде, басқа қалаларда — онлайн."
            ),
            'SHL': (
                "SHL тесттері: психометриялық тесттер, вербалды және сандық қабілеттерді тексереді.\n"
                "Вербалды тест: мәтіндер талдауы және дұрыс жауапты таңдау.\n"
                "Сандық тест: математикалық операциялар және дұрыс жауапты таңдау.\n"
                "Толық мәлімет және сынақ тесті www.shltools.com сайтында."
            ),
            'COMPASS тест': (
                "COMPASS тесті: ұшқыштың негізгі қабілеттерін тексеретін тест.\n"
                "Модульдер: қол-көз координациясы, есте сақтау, математика, кеңістіктік бағдарлау,\n"
                "бірнеше тапсырмаларды қатар орындау.\n"
                "Сондай-ақ авиациялық ағылшын және физика пәнінен тест болады."
            ),
            'CPP': (
                "CPP тесті: жеке тұлғаның қасиеттерін анықтайтын психологиялық тест.\n"
                "Ұзақтығы: 3 сағат.\n"
                "Ұсыныс: сұраққа ұзақ ойланбаңыз, жүйені алдауға тырыспаңыз."
            ),
        }
    }
}

# Кнопки
language_buttons = [['Русский', 'Қазақша']]
action_buttons = {
    'ru': [['Требование', 'Этапы отбора', 'ВЛЭК'], ['Финальный отбор', 'После прохождения отбора', 'Связаться'], ['Назад']],
    'kz': [['Талаптар', 'Іріктеу кезеңдері', 'ВЛЭК'], ['Қорытынды іріктеу', 'Өткеннен кейін', 'Байланыс'], ['Артқа']]
}

stages_buttons = {
    'ru': [['Тест английского языка', 'SHL'], ['COMPASS тест', 'CPP'], ['Назад']],
    'kz': [['Ағылшын тілінен тест', 'SHL'], ['COMPASS тест', 'CPP'], ['Артқа']]
}

# Хранение выбранного языка
user_language = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        texts['ru']['start'],
        reply_markup=ReplyKeyboardMarkup(language_buttons, one_time_keyboard=True)
    )
    return LANGUAGE

async def select_language(update: Update, context: CallbackContext):
    lang = 'ru' if update.message.text == 'Русский' else 'kz'
    user_language[update.message.chat_id] = lang
    await update.message.reply_text(
        texts[lang]['select_action'],
        reply_markup=ReplyKeyboardMarkup(action_buttons[lang], one_time_keyboard=True)
    )
    return ACTION

async def select_action(update: Update, context: CallbackContext):
    lang = user_language.get(update.message.chat_id, 'ru')
    text = update.message.text

    if text in ['Назад', 'Артқа']:
        # Return to the language selection screen
        await update.message.reply_text(
            texts[lang]['start'],
            reply_markup=ReplyKeyboardMarkup(language_buttons, one_time_keyboard=True)
        )
        # Remove language from the user_language dictionary to restart the process
        del user_language[update.message.chat_id]
        return LANGUAGE

    actions_map = {
        'Требование': 'requirement',
        'Этапы отбора': 'stages',
        'ВЛЭК': 'vlek',
        'Финальный отбор': 'final_selection',
        'После прохождения отбора': 'after_selection',
        'Связаться': 'contact',
        'Талаптар': 'requirement',
        'Іріктеу кезеңдері': 'stages',
        'Қорытынды іріктеу': 'final_selection',
        'Өткеннен кейін': 'after_selection',
        'Байланыс': 'contact'
    }

    if text in actions_map:
        if text in ['Этапы отбора', 'Іріктеу кезеңдері']:
            await update.message.reply_text(
                texts[lang]['stages'],
                reply_markup=ReplyKeyboardMarkup(stages_buttons[lang], one_time_keyboard=True)
            )
            return SELECTION_STAGE
        else:
            await update.message.reply_text(texts[lang][actions_map[text]])

    return ACTION

# Modify the select_stage function to handle the "Back" button
async def select_stage(update: Update, context: CallbackContext):
    lang = user_language.get(update.message.chat_id, 'ru')
    text = update.message.text

    # If "Back" button is pressed, go back to action selection
    if text in ['Назад', 'Артқа']:
        await update.message.reply_text(
            texts[lang]['select_action'],
            reply_markup=ReplyKeyboardMarkup(action_buttons[lang], one_time_keyboard=True)
        )
        return ACTION

    if text in texts[lang]['stages_buttons_map']:
        await update.message.reply_text(texts[lang]['stages_buttons_map'][text])
    else:
        await update.message.reply_text("Извините, информация не найдена.")

    return SELECTION_STAGE

async def select_stage(update: Update, context: CallbackContext):
    lang = user_language.get(update.message.chat_id, 'ru')
    text = update.message.text

    # Обработка выбора этапа
    if text in ['Назад', 'Артқа']:
        await update.message.reply_text(
            texts[lang]['select_action'],
            reply_markup=ReplyKeyboardMarkup(action_buttons[lang], one_time_keyboard=True)
        )
        return ACTION

    if text in texts[lang]['stages_buttons_map']:
        await update.message.reply_text(texts[lang]['stages_buttons_map'][text])
    else:
        await update.message.reply_text("Извините, информация не найдена.")
    
    return SELECTION_STAGE

def main():
    application = ApplicationBuilder().token("7928398483:AAFHo09PCsG0KkleEgXh7N3TS8DLy0s2ZcY").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_language)],
            ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_action)],
            SELECTION_STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_stage)]
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
