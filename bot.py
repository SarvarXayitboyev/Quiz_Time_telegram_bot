import requests
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from deep_translator import GoogleTranslator
import time
from datetime import datetime, timedelta

translator = GoogleTranslator(source="auto", target="uz")
print(translator.translate("Hello world"))
import asyncio, html

import os
from dotenv import load_dotenv

load_dotenv()  # .env faylni avtomatik o‘qiydi

TOKEN = os.getenv("TOKEN")
print("TOKEN:", TOKEN)



# Til sozlamalari
LANGUAGES = {
    'uz': {
        'name': '🇺🇿 O\'zbekcha',
        'code': 'uz',
        'google_code': 'uz'
    },
    'en': {
        'name': '🇺🇸 English',
        'code': 'en',
        'google_code': 'en'
    },
    'ru': {
        'name': '🇷🇺 Русский',
        'code': 'ru',
        'google_code': 'ru'
    }
}

# Tarjimalar
TRANSLATIONS = {
    'uz': {
        'welcome_title': '🎯 Savol-Javob Botga xush kelibsiz!\n',
        'welcome_text': 'Eslatma! Savollarning darajasi mavjud\n  oson:🟢\n  o`rta:🟡\n  qiyin:🔴\n___________________________________________',
        'select_language': '🌐 Tilni tanlang:',
        'select_category': '📚 Kategoriya tanlang:',
        'loading': '⏳ Savollar tayyorlanmoqda...\nIltimos biroz kuting ⏰',
        'error_loading': '❌ Xatolik yuz berdi!\n\nSavollar yuklanmadi. Internet aloqangizni tekshiring va qayta urinib ko\'ring.',
        'retry': '🔄 Qayta urinish',
        'main_menu': '🏠 Bosh menyu',
        'question': 'Savol',
        'correct': '✅ To\'g\'ri! Barakalla!',
        'incorrect': '❌ Noto\'g\'ri!',
        'correct_answer': 'To\'g\'ri javob',
        'next_question': '➡️ Keyingi savol',
        'stop_questions': '❌ Savollarni bekor qilish',
        'category': '🏷️ Kategoriya:',
        'stopped': '⏹️ Savollar to\'xtatildi',
        'answered_questions': 'ta savolga javob berdingiz.',
        'restart': '🔄 Qayta boshlash',
        'no_active_session': '❌ Faol sessiya topilmadi. /start ni bosing.',
        'invalid_answer': '❌ Noto\'g\'ri javob indeksi',
        'page_info': 'ℹ️ Bu faqat sahifa raqami',
        'previous': '⏮️ Oldingi',
        'next': '⏭️ Keyingi',
        'loading_next': '⏳ Keyingi savollar yuklanmoqda...'
    },
    'en': {
        'welcome_title': '🎯 Welcome to Q&A Bot!\n',
        'welcome_text': 'Attention! There is a level of questions\n  easy:🟢\n  medium:🟡\n  hard:🔴\n___________________________________________',
        'select_language': '🌐 Select language:',
        'select_category': '📚 Select category:',
        'loading': '⏳ Preparing questions...\nPlease wait a moment ⏰',
        'error_loading': '❌ An error occurred!\n\nQuestions could not be loaded. Check your internet connection and try again.',
        'retry': '🔄 Retry',
        'main_menu': '🏠 Main menu',
        'question': 'Question',
        'correct': '✅ Correct! Well done!',
        'incorrect': '❌ Incorrect!',
        'correct_answer': 'Correct answer',
        'next_question': '➡️ Next question',
        'stop_questions': '❌ Stop questions',
        'category': '🏷️ Category:',
        'stopped': '⏹️ Questions stopped',
        'answered_questions': 'questions answered.',
        'restart': '🔄 Restart',
        'no_active_session': '❌ No active session found. Press /start.',
        'invalid_answer': '❌ Invalid answer index',
        'page_info': 'ℹ️ This is just page number',
        'previous': '⏮️ Previous',
        'next': '⏭️ Next',
        'loading_next': '⏳ Loading next questions...'
    },
    'ru': {
        'welcome_title': '🎯 Добро пожаловать в Q&A Bot!\n',
        'welcome_text': 'Внимание! Есть уровень вопросов\n лёгкий:🟢\n средний:🟡\n сложный:🔴\n___________________________________________',
        'select_language': '🌐 Выберите язык:',
        'select_category': '📚 Выберите категорию:',
        'loading': '⏳ Подготовка вопросов...\nПожалуйста, подождите немного ⏰',
        'error_loading': '❌ Произошла ошибка!\n\nВопросы не загружены. Проверьте подключение к интернету и попробуйте снова.',
        'retry': '🔄 Повторить',
        'main_menu': '🏠 Главное меню',
        'question': 'Вопрос',
        'correct': '✅ Правильно! Молодец!',
        'incorrect': '❌ Неправильно!',
        'correct_answer': 'Правильный ответ',
        'next_question': '➡️ Следующий вопрос',
        'stop_questions': '❌ Остановить вопросы',
        'category': '🏷️ Категория:',
        'stopped': '⏹️ Вопросы остановлены',
        'answered_questions': 'вопросов отвечено.',
        'restart': '🔄 Перезапустить',
        'no_active_session': '❌ Активная сессия не найдена. Нажмите /start.',
        'invalid_answer': '❌ Неверный индекс ответа',
        'page_info': 'ℹ️ Это только номер страницы',
        'previous': '⏮️ Предыдущая',
        'next': '⏭️ Следующая',
        'loading_next': '⏳ Загрузка следующих вопросов...'
    }
}

# Kategoriyalarning tarjimalari
CATEGORIES_TRANSLATIONS = {
    'uz': [
        {"name": "📘 Umumiy bilimlar", "id": 9},
        {"name": "📚 Adabiyot, kitoblar", "id": 10},
        {"name": "🎬 Filmlar", "id": 11},
        {"name": "🎵 Musiqa", "id": 12},
        {"name": "🎭 Myuzikllar va teatr", "id": 13},
        {"name": "📺 Televideniye", "id": 14},
        {"name": "🎮 Video o'yinlar", "id": 15},
        {"name": "🎲 Stol o'yinlari", "id": 16},
        {"name": "🔬 Fan va tabiat", "id": 17},
        {"name": "💻 Kompyuter fani", "id": 18},
        {"name": "➗ Matematika", "id": 19},
        {"name": "🧙‍♂️ Mifologiya", "id": 20},
        {"name": "🏅 Sport", "id": 21},
        {"name": "🗺️ Geografiya", "id": 22},
        {"name": "📜 Tarix", "id": 23},
        {"name": "🏛️ Siyosat", "id": 24},
        {"name": "🎨 San'at", "id": 25},
        {"name": "🌟 Mashhurlar", "id": 26},
        {"name": "🐾 Hayvonlar", "id": 27},
        {"name": "🚗 Transport vositalari", "id": 28},
        {"name": "📖 Komikslar", "id": 29},
        {"name": "📱 Texnik qurilmalar", "id": 30},
        {"name": "🍥 Yapon anime va manga", "id": 31},
        {"name": "🐭 Multfilm va animatsiyalar", "id": 32},
    ],
    'en': [
        {"name": "📘 General Knowledge", "id": 9},
        {"name": "📚 Books", "id": 10},
        {"name": "🎬 Films", "id": 11},
        {"name": "🎵 Music", "id": 12},
        {"name": "🎭 Musicals & Theatre", "id": 13},
        {"name": "📺 Television", "id": 14},
        {"name": "🎮 Video Games", "id": 15},
        {"name": "🎲 Board Games", "id": 16},
        {"name": "🔬 Science & Nature", "id": 17},
        {"name": "💻 Computers", "id": 18},
        {"name": "➗ Mathematics", "id": 19},
        {"name": "🧙‍♂️ Mythology", "id": 20},
        {"name": "🏅 Sports", "id": 21},
        {"name": "🗺️ Geography", "id": 22},
        {"name": "📜 History", "id": 23},
        {"name": "🏛️ Politics", "id": 24},
        {"name": "🎨 Art", "id": 25},
        {"name": "🌟 Celebrities", "id": 26},
        {"name": "🐾 Animals", "id": 27},
        {"name": "🚗 Vehicles", "id": 28},
        {"name": "📖 Comics", "id": 29},
        {"name": "📱 Gadgets", "id": 30},
        {"name": "🍥 Japanese Anime & Manga", "id": 31},
        {"name": "🐭 Cartoons & Animations", "id": 32},
    ],
    'ru': [
        {"name": "📘 Общие знания", "id": 9},
        {"name": "📚 Книги", "id": 10},
        {"name": "🎬 Фильмы", "id": 11},
        {"name": "🎵 Музыка", "id": 12},
        {"name": "🎭 Мюзиклы и театр", "id": 13},
        {"name": "📺 Телевидение", "id": 14},
        {"name": "🎮 Видеоигры", "id": 15},
        {"name": "🎲 Настольные игры", "id": 16},
        {"name": "🔬 Наука и природа", "id": 17},
        {"name": "💻 Компьютеры", "id": 18},
        {"name": "➗ Математика", "id": 19},
        {"name": "🧙‍♂️ Мифология", "id": 20},
        {"name": "🏅 Спорт", "id": 21},
        {"name": "🗺️ География", "id": 22},
        {"name": "📜 История", "id": 23},
        {"name": "🏛️ Политика", "id": 24},
        {"name": "🎨 Искусство", "id": 25},
        {"name": "🌟 Знаменитости", "id": 26},
        {"name": "🐾 Животные", "id": 27},
        {"name": "🚗 Транспорт", "id": 28},
        {"name": "📖 Комиксы", "id": 29},
        {"name": "📱 Гаджеты", "id": 30},
        {"name": "🍥 Японское аниме и манга", "id": 31},
        {"name": "🐭 Мультфильмы", "id": 32},
    ]
}
STATISTICS_TRANSLATIONS = {
    'uz': {
        'session_ended': '🏁 Sessiya yakunlandi!',
        'quiz_statistics': '📊 Quiz statistikasi',
        'total_questions': 'Jami savollar',
        'correct_answers': 'To\'g\'ri javoblar',
        'wrong_answers': 'Xato javoblar',
        'skipped_questions': 'O\'tkazib yuborilgan',
        'quiz_duration': 'Quiz davomiyligi',
        'start_time': 'Boshlangan vaqti',
        'end_time': 'Yakunlangan vaqti',
        'accuracy': 'Aniqlik',
        'excellent_result': 'Ajoyib natija!',
        'good_result': 'Yaxshi natija!',
        'keep_trying': 'Davom eting!',
        'no_questions_answered': 'Hech qanday savolga javob berilmadi'
    },
    'en': {
        'session_ended': '🏁 Session ended!',
        'quiz_statistics': '📊 Quiz Statistics',
        'total_questions': 'Total questions',
        'correct_answers': 'Correct answers',
        'wrong_answers': 'Wrong answers',
        'skipped_questions': 'Skipped questions',
        'quiz_duration': 'Quiz duration',
        'start_time': 'Start time',
        'end_time': 'End time',
        'accuracy': 'Accuracy',
        'excellent_result': 'Excellent result!',
        'good_result': 'Good result!',
        'keep_trying': 'Keep trying!',
        'no_questions_answered': 'No questions answered'
    },
    'ru': {
        'session_ended': '🏁 Сессия завершена!',
        'quiz_statistics': '📊 Статистика викторины',
        'total_questions': 'Всего вопросов',
        'correct_answers': 'Правильные ответы',
        'wrong_answers': 'Неправильные ответы',
        'skipped_questions': 'Пропущенные вопросы',
        'quiz_duration': 'Длительность викторины',
        'start_time': 'Время начала',
        'end_time': 'Время окончания',
        'accuracy': 'Точность',
        'excellent_result': 'Отличный результат!',
        'good_result': 'Хороший результат!',
        'keep_trying': 'Продолжайте!',
        'no_questions_answered': 'Не отвечено ни на один вопрос'
    }
}
for lang in TRANSLATIONS:
    TRANSLATIONS[lang].update(STATISTICS_TRANSLATIONS[lang])

ITEMS_PER_PAGE = 8
BUTTONS_PER_ROW = 2

# Foydalanuvchi sozlamalari va quiz sessiyalari
user_settings = {}  # user_id: {'language': 'uz'}
user_quiz_sessions = {}


class QuizSession:
    def __init__(self, user_id, category_name, category_id, language='uz'):
        self.user_id = user_id
        self.category_name = category_name
        self.category_id = category_id
        self.language = language
        self.question_number = 1
        self.questions_queue = []
        self.translated_questions_queue = []
        self.current_question_data = None
        self.loading_next_batch = False

        # Statistika uchun yangi o'zgaruvchilar
        self.start_time = datetime.now()
        self.end_time = None
        self.correct_answers = 0
        self.wrong_answers = 0
        self.skipped_questions = 0
        self.total_questions_answered = 0
        self.session_active = True

    async def get_next_question(self):
        # Agar navbatda tarjima qilingan savollar bo'lsa, undan olish
        if self.translated_questions_queue:
            self.current_question_data = self.translated_questions_queue.pop(0)
            self.question_number += 1
            return self.current_question_data

        # Agar original savollar navbatda bo'lsa, tarjima qilish
        if self.questions_queue:
            original_question = self.questions_queue.pop(0)
            translated_question = await self.translate_question(original_question)
            self.current_question_data = translated_question
            self.question_number += 1
            return self.current_question_data

        return None

    async def translate_question(self, question_data):
        # Matnlarni HTML entities dan tozalash
        question_text = html.unescape(question_data['question'])
        correct_answer = html.unescape(question_data['correct_answer'])
        incorrect_answers = [html.unescape(ans) for ans in question_data['incorrect_answers']]

        # Agar til ingliz tili bo'lmasa, tarjima qilish
        if self.language != 'en':
            try:
                question_text = await translate_text_async(question_text, self.language)
                correct_answer = await translate_text_async(correct_answer, self.language)

                # Noto'g'ri javoblarni tarjima qilish
                translated_incorrect = []
                for ans in incorrect_answers:
                    translated_ans = await translate_text_async(ans, self.language)
                    translated_incorrect.append(translated_ans)
                incorrect_answers = translated_incorrect

            except Exception as e:
                print(f"Tarjima xatosi: {e}")

        # Javob variantlarini aralashtirish
        all_answers = [correct_answer] + incorrect_answers
        random.shuffle(all_answers)

        return {
            'question': question_text,
            'answers': all_answers,
            'correct_answer': correct_answer,
            'difficulty': question_data.get('difficulty', 'medium')
        }

    def add_questions_batch(self, questions):
        """Savollar to'plamini qo'shish"""
        self.questions_queue.extend(questions)

    async def preload_next_questions(self):
        """Keyingi savollarni fon rejimda tarjima qilish"""
        if not self.loading_next_batch and len(self.translated_questions_queue) < 3 and self.questions_queue:
            # Oldingi 3 ta savolni tarjima qilish
            questions_to_translate = self.questions_queue[:3]
            self.questions_queue = self.questions_queue[3:]

            for question_data in questions_to_translate:
                translated = await self.translate_question(question_data)
                self.translated_questions_queue.append(translated)

    def should_load_more_questions(self):
        """Ko'proq savollar yuklash kerakligini tekshirish"""
        total_remaining = len(self.questions_queue) + len(self.translated_questions_queue)
        return total_remaining < 3

    def mark_answer(self, is_correct):
        """Javobni belgilash"""
        self.total_questions_answered += 1
        if is_correct:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

    def mark_skipped(self):
        """O'tkazib yuborilgan savolni belgilash"""
        self.skipped_questions += 1

    def end_session(self):
        """Sessiyani tugatish"""
        self.end_time = datetime.now()
        self.session_active = False

    def get_duration(self):
        """Sessiya davomiyligini hisoblash"""
        end = self.end_time if self.end_time else datetime.now()
        duration = end - self.start_time
        return duration

    def get_statistics(self):
        """Statistika ma'lumotlarini qaytarish"""
        duration = self.get_duration()

        # Vaqtni formatlash
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60

        if hours > 0:
            duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            duration_str = f"{minutes}:{seconds:02d}"

        return {
            'total_answered': self.total_questions_answered,
            'correct': self.correct_answers,
            'wrong': self.wrong_answers,
            'skipped': self.skipped_questions,
            'duration': duration_str,
            'start_time': self.start_time.strftime("%H:%M"),
            'end_time': self.end_time.strftime("%H:%M") if self.end_time else datetime.now().strftime("%H:%M")
        }


# Statistika xabarini yaratish funksiyasi
def create_statistics_message(stats, session, language):
    """Statistika xabarini yaratish"""
    t = TRANSLATIONS[language]

    # Agar hech qanday savolga javob berilmagan bo'lsa
    if stats['total_answered'] == 0:
        return f"📊 <b>{t['no_questions_answered']}</b>\n\n🏠 {t['main_menu']}"

    # Aniqlikni hisoblash
    accuracy = (stats['correct'] / stats['total_answered']) * 100 if stats['total_answered'] > 0 else 0

    # Motivatsion xabar
    if accuracy >= 80:
        motivation = f"🏆 {t['excellent_result']}"
    elif accuracy >= 60:
        motivation = f"👍 {t['good_result']}"
    else:
        motivation = f"💪 {t['keep_trying']}"

    # Asosiy statistika xabari
    message = f"""🎯 <b>{t['session_ended']}</b>

📊 <b>{t['quiz_statistics']}</b>
━━━━━━━━━━━━━━━━━━━━━

📝 <b>{t['category']}</b> {session.category_name}

📈 <b>Natijalar:</b>
  • 📊 {t['total_questions']}: <b>{stats['total_answered']}</b>
  • ✅ {t['correct_answers']}: <b>{stats['correct']} ta</b>
  • ❌ {t['wrong_answers']}: <b>{stats['wrong']} ta</b>
  • ⏭️ {t['skipped_questions']}: <b>{stats['skipped']} ta</b>

🎯 <b>{t['accuracy']}:</b> <code>{accuracy:.1f}%</code>

⏰ <b>Vaqt ma'lumotlari:</b>
  • 🚀 {t['start_time']}: <b>{stats['start_time']}</b>
  • 🏁 {t['end_time']}: <b>{stats['end_time']}</b>
  • ⏱️ {t['quiz_duration']}: <b>{stats['duration']}</b>

{motivation}"""

    return message
# Savol darajalari uchun belgilar
DIFFICULTY_LEVELS = {
    'easy': '🟢 Oson',
    'medium': '🟡 O‘rtacha',
    'hard': '🔴 Qiyin'
}

async def show_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchiga navbatdagi savolni chiqarish"""
    chat_id = update.effective_chat.id
    state = context.user_data.get("state", {})

    # Agar savollar tugagan bo‘lsa
    if not state.get("questions"):
        await context.bot.send_message(chat_id, "🎉 Savollar tugadi!")
        return

    # Navbatdagi savolni olish
    question_data = state["questions"].pop(0)

    # Savol darajasi
    difficulty = question_data.get("difficulty", "easy")
    difficulty_text = DIFFICULTY_LEVELS.get(difficulty, "❔ Noma’lum")

    # Savol matni
    question_text = html.unescape(question_data["question"])
    answers = question_data["answers"]

    # Inline tugmalar (variantlar)
    keyboard = [
        [InlineKeyboardButton(ans, callback_data=ans)] for ans in answers
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Xabar matni
    message = (
        f"❓ <b>Savol:</b> {question_text}\n\n"
        f"📊 <b>Daraja:</b> {difficulty_text}\n\n"
        f"A) {answers[0]}\n"
        f"B) {answers[1]}\n"
        f"C) {answers[2]}\n"
        f"D) {answers[3]}"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    # Keyingi tekshirish uchun to‘g‘ri javobni saqlaymiz
    state["correct_answer"] = question_data["correct_answer"]
    context.user_data["state"] = state



# Tarjima funksiyasi
def translate_text_sync(text, target_language):
    try:
        if target_language == 'en':
            return text
        decoded_text = html.unescape(text)
        translated = GoogleTranslator(source="auto", target=target_language).translate(decoded_text)
        return translated
    except Exception as e:
        print(f"Tarjima xatosi: {e}")
        return text


async def translate_text_async(text, target_language):
    try:
        if target_language == 'en':
            return text
        decoded_text = html.unescape(text)
        loop = asyncio.get_event_loop()
        translated = await loop.run_in_executor(
            None,
            lambda: GoogleTranslator(source="auto", target=target_language).translate(decoded_text)
        )
        return translated
    except Exception as e:
        print(f"Async tarjima xatosi: {e}")
        return text


# Til tanlash keyboard
def create_language_keyboard():
    keyboard = []
    for lang_code, lang_info in LANGUAGES.items():
        keyboard.append([InlineKeyboardButton(lang_info['name'], callback_data=f"lang_{lang_code}")])
    return InlineKeyboardMarkup(keyboard)


# API dan savollarni olish
async def fetch_questions(category_id, amount=10):
    try:
        url = f"https://opentdb.com/api.php?amount={amount}&category={category_id}&type=multiple"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data['response_code'] == 0:
            return data['results']
        else:
            return None
    except Exception as e:
        print(f"API xatosi: {e}")
        return None


# Kategoriya nomi topish
def get_category_name(category_id, language='uz'):
    categories = CATEGORIES_TRANSLATIONS.get(language, CATEGORIES_TRANSLATIONS['uz'])
    for cat in categories:
        if cat['id'] == category_id:
            return cat['name']
    return "Unknown category"


# Savolni formatlash
def format_question_display(question_data, question_num, language='uz'):
    # Qiyinlik darajasi emoji
    difficulty_emoji = {
        'easy': '🟢',
        'medium': '🟡',
        'hard': '🔴'
    }

    difficulty = difficulty_emoji.get(question_data.get('difficulty', 'medium'), '🟡')
    question_label = TRANSLATIONS[language].get('question', 'Question')

    text = f"❓ <b>{question_label} {question_num}</b> {difficulty}\n\n"
    text += f"<b>{question_data['question']}</b>\n\n"

    return text


# Savol uchun keyboard yaratish
def create_question_keyboard(answers, language='uz', show_next=True):
    keyboard = []

    # Har bir javob uchun tugma (2 tadan qatorda)
    row = []
    for i, answer in enumerate(answers):
        # Javob uzun bo'lsa qisqartirish
        display_text = answer if len(answer) <= 35 else answer[:32] + "..."
        callback_data = f"answer_{i}"

        row.append(InlineKeyboardButton(display_text, callback_data=callback_data))

        if len(row) == 2 or i == len(answers) - 1:
            keyboard.append(row)
            row = []

    # Boshqaruv tugmalari
    t = TRANSLATIONS[language]
    control_buttons = []

    # O'tkazib yuborish tugmasi qo'shish
    control_buttons.append(InlineKeyboardButton(
        f"⏭️ O'tkazib yuborish",
        callback_data="skip_question"
    ))

    control_buttons.append(InlineKeyboardButton(
        t['stop_questions'],
        callback_data="stop_questions"
    ))

    keyboard.append(control_buttons)

    return InlineKeyboardMarkup(keyboard)


def create_question_keyboard_with_skip(answers, language='uz'):
    """Savollar uchun keyboard (o'tkazib yuborish tugmasi bilan)"""
    keyboard = []

    # Javob variantlari
    row = []
    for i, answer in enumerate(answers):
        display_text = answer if len(answer) <= 35 else answer[:32] + "..."
        callback_data = f"answer_{i}"
        row.append(InlineKeyboardButton(display_text, callback_data=callback_data))

        if len(row) == 2 or i == len(answers) - 1:
            keyboard.append(row)
            row = []

    # Boshqaruv tugmalari
    t = TRANSLATIONS[language]
    control_buttons = [
        InlineKeyboardButton(f"⏭️ {t.get('skip_question', 'O`tkazib yuborish')}", callback_data="skip_question"),
        InlineKeyboardButton(t['stop_questions'], callback_data="stop_questions")
    ]
    keyboard.append(control_buttons)

    return InlineKeyboardMarkup(keyboard)



async def handle_skip_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_quiz_sessions:
        language = user_settings.get(user_id, {}).get('language', 'en')
        t = TRANSLATIONS[language]
        await query.answer(t['no_active_session'], show_alert=True)
        return

    session = user_quiz_sessions[user_id]
    language = session.language
    t = TRANSLATIONS[language]

    # O'tkazib yuborilgan savolni belgilash
    session.mark_skipped()

    await query.answer("⏭️ Savol o'tkazib yuborildi", show_alert=False)

    # Keyingi savolni ko'rsatish
    await show_next_question(query, session)

# TRANSLATIONS ga o'tkazib yuborish tarjimasini qo'shish
skip_translations = {
    'uz': {'skip_question': "O'tkazib yuborish"},
    'en': {'skip_question': "Skip question"},
    'ru': {'skip_question': "Пропустить вопрос"}
}

for lang in TRANSLATIONS:
    TRANSLATIONS[lang].update(skip_translations[lang])


# Kategoriya tanlash uchun keyboard
def build_keyboard(page: int = 0, language='uz', show_language_button=False):
    categories = CATEGORIES_TRANSLATIONS.get(language, CATEGORIES_TRANSLATIONS['uz'])
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    chunk = categories[start:end]

    keyboard = []

    # har qatorida 2 tadan tugma
    row = []
    for i, category in enumerate(chunk):
        callback_data = f"select_{category['id']}"
        row.append(InlineKeyboardButton(category['name'], callback_data=callback_data))
        if len(row) == BUTTONS_PER_ROW:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Navigatsiya tugmalari
    nav_row = []
    total_pages = (len(categories) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    if page > 0:
        prev_text = TRANSLATIONS[language].get('previous', '⏮️ Previous')
        nav_row.append(InlineKeyboardButton(prev_text, callback_data=f"page_{page - 1}"))

    nav_row.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))

    if end < len(categories):
        next_text = TRANSLATIONS[language].get('next', '⏭️ Next')
        nav_row.append(InlineKeyboardButton(next_text, callback_data=f"page_{page + 1}"))

    keyboard.append(nav_row)

    # Til o'zgartirish tugmasini faqat kerak bo'lganda qo'shish
    if show_language_button:
        keyboard.append([InlineKeyboardButton("  🇺🇸 Language  |  🇷🇺 язык  |  🇺🇿 Til  ",
                                              callback_data="change_language")])

    return InlineKeyboardMarkup(keyboard)

# Restart keyboard
def create_restart_keyboard(language='uz'):
    t = TRANSLATIONS[language]
    keyboard = [
        [InlineKeyboardButton(t['restart'], callback_data="restart_session")],
        [InlineKeyboardButton(t['main_menu'], callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


# Handler'lar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Agar faol quiz sessiyasi bo'lsa, uni to'xtatish
    if user_id in user_quiz_sessions:
        del user_quiz_sessions[user_id]

    # Foydalanuvchi sozlamalarini tekshirish
    if user_id not in user_settings:
        # Til tanlash
        await update.message.reply_text(
            "🌐 <b>Welcome! | Добро пожаловать! | Xush kelibsiz!</b>\n\n"
            "Please select your language:\n"
            "Пожалуйста, выберите ваш язык:\n"
            "Iltimos, tilni tanlang:",
            parse_mode="HTML",
            reply_markup=create_language_keyboard(),
        )
    else:
        # Til allaqachon tanlangan - til tugmasini ko'rsatmaslik
        language = user_settings[user_id]['language']
        t = TRANSLATIONS[language]
        await update.message.reply_text(
            f"<b>{t['welcome_title']}</b>\n\n{t['welcome_text']}",
            parse_mode="HTML",
            reply_markup=build_keyboard(0, language, show_language_button=True),  # Faqat bosh menyuda ko'rsatish
        )


# handle_language_selection funksiyasini o'zgartiring:

async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    language = query.data.split("_")[1]

    # Foydalanuvchi sozlamalarini saqlash
    user_settings[user_id] = {'language': language}

    t = TRANSLATIONS[language]

    await query.answer(f"Language set to {LANGUAGES[language]['name']}", show_alert=False)
    await query.edit_message_text(
        f"<b>{t['welcome_title']}</b>\n\n{t['welcome_text']}",
        parse_mode="HTML",
        reply_markup=build_keyboard(0, language, show_language_button=True),  # Bosh menyuda ko'rsatish
    )


async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    language = query.data.split("_")[1]

    # Foydalanuvchi sozlamalarini saqlash
    user_settings[user_id] = {'language': language}

    t = TRANSLATIONS[language]

    await query.answer(f"Language set to {LANGUAGES[language]['name']}", show_alert=False)
    await query.edit_message_text(
        f"<b>{t['welcome_title']}</b>\n\n{t['welcome_text']}",
        parse_mode="HTML",
        reply_markup=build_keyboard(0, language),
    )


async def handle_change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🌐 <b>Select language | Выберите язык | Tilni tanlang:</b>",
        parse_mode="HTML",
        reply_markup=create_language_keyboard(),
    )


async def handle_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_settings:
        await query.answer("Please select language first", show_alert=True)
        return

    language = user_settings[user_id]['language']
    await query.answer()

    page = int(query.data.split("_")[1])
    # Til tugmasini ko'rsatmaslik
    await query.edit_message_reply_markup(reply_markup=build_keyboard(page, language, show_language_button=False))

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_settings:
        await query.answer("Please select language first", show_alert=True)
        return

    language = user_settings[user_id]['language']
    t = TRANSLATIONS[language]

    category_id = int(query.data.split("_")[1])
    category_name = get_category_name(category_id, language)

    await query.answer(t['loading'].split('\n')[0], show_alert=False)

    # Loading message
    await query.edit_message_text(
        f"⏳ <b>{category_name}</b>\n\n{t['loading']}",
        parse_mode="HTML"
    )

    # API dan savollarni olish
    questions = await fetch_questions(category_id, 10)

    if not questions:
        await query.edit_message_text(
            t['error_loading'],
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(t['retry'], callback_data=f"select_{category_id}"),
                InlineKeyboardButton(t['main_menu'], callback_data="main_menu")
            ]])
        )
        return

    # Quiz sessiyasini yaratish
    session = QuizSession(user_id, category_name, category_id, language)
    session.add_questions_batch(questions)
    user_quiz_sessions[user_id] = session

    # Birinchi savolni ko'rsatish
    await show_next_question(query, session)


async def show_next_question(query, session):
    # Keyingi savolni olish
    question_data = await session.get_next_question()

    if not question_data:
        # Agar savollar tugagan bo'lsa, yangi savollarni yuklash
        if session.should_load_more_questions():
            await load_more_questions(session)
            question_data = await session.get_next_question()

        if not question_data:
            # Hali ham savol yo'q bo'lsa, xatolik
            language = session.language
            t = TRANSLATIONS[language]
            await query.edit_message_text(
                t['error_loading'],
                parse_mode="HTML",
                reply_markup=create_restart_keyboard(language)
            )
            return

    # Keyingi savollarni fon rejimda tarjima qilish
    asyncio.create_task(session.preload_next_questions())

    # Agar keyingi savollar tugab qolsa, yangi batch yuklash
    if session.should_load_more_questions():
        asyncio.create_task(load_more_questions(session))

    question_text = format_question_display(question_data, session.question_number - 1, session.language)
    keyboard = create_question_keyboard(question_data['answers'], session.language)

    await query.edit_message_text(
        question_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def load_more_questions(session):
    if session.loading_next_batch:
        return

    session.loading_next_batch = True
    try:
        new_questions = await fetch_questions(session.category_id, 10)
        if new_questions:
            session.add_questions_batch(new_questions)
    except Exception as e:
        print(f"Keyingi savollarni yuklashda xatolik: {e}")
    finally:
        session.loading_next_batch = False


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_quiz_sessions:
        if user_id in user_settings:
            language = user_settings[user_id]['language']
            t = TRANSLATIONS[language]
            await query.answer(t['no_active_session'], show_alert=True)
        else:
            await query.answer("❌ No active session found. Press /start.", show_alert=True)
        return

    session = user_quiz_sessions[user_id]
    language = session.language
    t = TRANSLATIONS[language]

    answer_index = int(query.data.split("_")[1])
    question_data = session.current_question_data

    if not question_data or answer_index >= len(question_data['answers']):
        await query.answer(t['invalid_answer'], show_alert=True)
        return

    user_answer = question_data['answers'][answer_index]
    is_correct = user_answer == question_data['correct_answer']

    # Statistikani yangilash
    session.mark_answer(is_correct)

    # Javob natijasini ko'rsatish
    if is_correct:
        result_text = f"✅ {t['correct']}"
        await query.answer(result_text, show_alert=False)
    else:
        result_text = f"❌ {t['incorrect']}\n{t['correct_answer']}: {question_data['correct_answer']}"
        await query.answer(result_text, show_alert=False)

    # Keyingi savolga o'tish keyboard yaratish
    keyboard = create_next_question_keyboard(session.language)

    # Savolni yangilash - javob berilganini ko'rsatish
    question_text = format_question_display(question_data, session.question_number - 1, session.language)

    if is_correct:
        question_text += f"✅ <b>{t['correct']}</b>\n\n"
    else:
        question_text += f"❌ <b>{t['incorrect']}</b>\n"
        question_text += f"<b>{t['correct_answer']}:</b> {question_data['correct_answer']}\n\n"

    await query.edit_message_text(
        question_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


def create_next_question_keyboard(language='uz'):
    t = TRANSLATIONS[language]
    keyboard = [
        [InlineKeyboardButton(t['next_question'], callback_data="next_question")],
        [InlineKeyboardButton(t['stop_questions'], callback_data="stop_questions")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def handle_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_quiz_sessions:
        if user_id in user_settings:
            language = user_settings[user_id]['language']
            t = TRANSLATIONS[language]
            await query.answer(t['no_active_session'], show_alert=True)
        else:
            await query.answer("❌ No active session found. Press /start.", show_alert=True)
        return

    session = user_quiz_sessions[user_id]
    await query.answer()

    # Keyingi savolni ko'rsatish
    await show_next_question(query, session)


async def handle_stop_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id in user_quiz_sessions:
        session = user_quiz_sessions[user_id]
        language = session.language
        t = TRANSLATIONS[language]

        # Sessiyani tugatish
        session.end_session()

        # Statistikani olish
        stats = session.get_statistics()

        # Statistika xabarini tayyorlash
        stats_message = create_statistics_message(stats, session, language)

        del user_quiz_sessions[user_id]

        await query.answer(t['session_ended'], show_alert=False)
        await query.edit_message_text(
            stats_message,
            parse_mode="HTML",
            reply_markup=create_restart_keyboard(language)
        )
    else:
        if user_id in user_settings:
            language = user_settings[user_id]['language']
            t = TRANSLATIONS[language]
            await query.answer(t['no_active_session'], show_alert=True)
        else:
            await query.answer("No active session found", show_alert=True)


def create_statistics_message(stats, session, language):
    """Statistika xabarini yaratish"""
    t = TRANSLATIONS[language]

    # Agar hech qanday savolga javob berilmagan bo'lsa
    if stats['total_answered'] == 0:
        return f"📊 <b>{t['no_questions_answered']}</b>\n\n🏠 {t['main_menu']}"

    # Aniqlikni hisoblash
    accuracy = (stats['correct'] / stats['total_answered']) * 100 if stats['total_answered'] > 0 else 0

    # Motivatsion xabar
    if accuracy >= 80:
        motivation = f"🏆 {t['excellent_result']}"
    elif accuracy >= 60:
        motivation = f"👍 {t['good_result']}"
    else:
        motivation = f"💪 {t['keep_trying']}"

    # Asosiy statistika xabari
    message = f"""🎯 <b>{t['session_ended']}</b>

📊 <b>{t['quiz_statistics']}</b>
━━━━━━━━━━━━━━━━━━━━━

📝 <b>{t['category']}:</b> {session.category_name}

📈 <b>Natijalar:</b>
  • 📊 {t['total_questions']}: <b>{stats['total_answered']}</b>
  • ✅ {t['correct_answers']}: <b>{stats['correct']} ta</b>
  • ❌ {t['wrong_answers']}: <b>{stats['wrong']} ta</b>
  • ⏭️ {t['skipped_questions']}: <b>{stats['skipped']} ta</b>

🎯 <b>{t['accuracy']}:</b> <code>{accuracy:.1f}%</code>

⏰ <b>Vaqt ma'lumotlari:</b>
  • 🏁 {t['start_time']}: <b>{stats['start_time']}</b>
  • 🏁 {t['end_time']}: <b>{stats['end_time']}</b>
  • ⏱️ {t['quiz_duration']}: <b>{stats['duration']}</b>

{motivation}"""

    return message

async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_settings:
        await query.answer("Please select language first", show_alert=True)
        await query.edit_message_text(
            "🌐 <b>Select language | Выберите язык | Tilni tanlang:</b>",
            parse_mode="HTML",
            reply_markup=create_language_keyboard(),
        )
        return

    language = user_settings[user_id]['language']
    t = TRANSLATIONS[language]

    # Eski sessiyani tozalash
    if user_id in user_quiz_sessions:
        del user_quiz_sessions[user_id]

    await query.answer()
    await query.edit_message_text(
        f"🎯 <b>{t['select_category']}</b>\n\n{t['select_category']}",
        parse_mode="HTML",
        reply_markup=build_keyboard(0, language, show_language_button=False),  # Til tugmasini yashirish
    )



async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_settings:
        await query.answer("Please select language first", show_alert=True)
        await query.edit_message_text(
            "🌐 <b>Select language | Выберите язык | Tilni tanlang:</b>",
            parse_mode="HTML",
            reply_markup=create_language_keyboard(),
        )
        return

    language = user_settings[user_id]['language']
    t = TRANSLATIONS[language]

    # Eski sessiyani tozalash
    if user_id in user_quiz_sessions:
        del user_quiz_sessions[user_id]

    await query.answer()
    await query.edit_message_text(
        f"🏠 <b>{t['main_menu']}</b>\n\n{t['select_category']}",
        parse_mode="HTML",
        reply_markup=build_keyboard(0, language, show_language_button=True),  # Bosh menyuda ko'rsatish
    )



async def handle_noop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id

    if user_id in user_settings:
        language = user_settings[user_id]['language']
        t = TRANSLATIONS[language]
        await update.callback_query.answer(t['page_info'], show_alert=False)
    else:
        await update.callback_query.answer("ℹ️ This is just page number", show_alert=False)


async def developer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Agar foydalanuvchi tili tanlangan bo'lsa, shu tilda javob berish
    if user_id in user_settings:
        language = user_settings[user_id]['language']

        if language == 'uz':
            message = (
                "👨‍💻 <b>Bot Dasturchi</b>\n\n"
                "<b>Ism:</b> Xayitboyev Sarvar\n"
                "<b>Yaratilgan sana:</b> <code>09.07.2025</code>\n"
                "<b>Soha:</b> Backend Development (PHP Laravel, Python, Django, Telegram Botlar)\n"
                "<b>Tajriba:</b> IT sohasida amaliy loyihalar va avtomatlashtirish yechimlari\n\n"
                "<b>Aloqa:</b> <a href='https://t.me/SarvarXayitboyev'>@SarvarXayitboyev</a>\n\n"
                "<i>Yaxshi kod — bu san'at, mukammal kod esa falsafa.</i>\n\n"
                "<i>Davom etish uchun /start buyrug'i!</i>"
            )
        elif language == 'en':
            message = (
                "👨‍💻 <b>Bot Developer</b>\n\n"
                "<b>Name:</b> Xayitboyev Sarvar\n"
                "<b>Created:</b> <code>09.07.2025</code>\n"
                "<b>Field:</b> Backend Development (PHP Laravel, Python, Django, Telegram Bots)\n"
                "<b>Experience:</b> Practical projects and automation solutions in IT\n\n"
                "<b>Contact:</b> <a href='https://t.me/SarvarXayitboyev'>@SarvarXayitboyev</a>\n\n"
                "<i>Good code is art, perfect code is philosophy.</i>\n\n"
                "<i>Use /start command to continue!</i>"
            )
        else:  # ru
            message = (
                "👨‍💻 <b>Разработчик бота</b>\n\n"
                "<b>Имя:</b> Хайитбоев Сарвар\n"
                "<b>Создан:</b> <code>09.07.2025</code>\n"
                "<b>Область:</b> Backend разработка (PHP Laravel, Python, Django, Telegram боты)\n"
                "<b>Опыт:</b> Практические проекты и автоматизационные решения в IT\n\n"
                "<b>Связь:</b> <a href='https://t.me/SarvarXayitboyev'>@SarvarXayitboyev</a>\n\n"
                "<i>Хороший код — это искусство, совершенный код — философия.</i>\n\n"
                "<i>Используйте команду /start для продолжения!</i>"
            )
    else:
        # Agar til tanlanmagan bo'lsa, default inglizcha
        message = (
            "👨‍💻 <b>Bot Developer</b>\n\n"
            "<b>Name:</b> Xayitboyev Sarvar\n"
            "<b>Created:</b> <code>09.07.2025</code>\n"
            "<b>Field:</b> Backend Development (PHP Laravel, Python, Django, Telegram Bots)\n"
            "<b>Experience:</b> Practical projects and automation solutions in IT\n\n"
            "<b>Contact:</b> <a href='https://t.me/SarvarXayitboyev'>@SarvarXayitboyev</a>\n\n"
            "<i>Good code is art, perfect code is philosophy.</i>\n\n"
            "<i>Use /start command to continue!</i>"
        )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📬 Bog'lanish | Contact | Связаться", url="https://t.me/SarvarXayitboyev")],
        [InlineKeyboardButton("🏠 Bosh menyu | Main menu | Главное меню", callback_data="main_menu")]
    ])

    await update.message.reply_text(
        text=message,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=keyboard
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Default inglizcha xabar
    message = (
        "🆘 <b>Help</b>\n\n"
        "<b>Available commands:</b>\n"
        "• /start - Start the bot\n"
        "• /developer - Developer information\n"
        "• /help - This help text\n\n"
        "<b>About bot:</b>\n"
        "This bot asks you questions on various topics and tests your knowledge.\n"
        "3 difficulty levels available: Easy🟢, Medium🟡, Hard🔴\n\n"
        "Press /start to continue!"
    )

    # Agar foydalanuvchi tili mavjud bo'lsa
    if user_id in user_settings:
        language = user_settings[user_id]['language']

        if language == 'uz':
            message = (
                "🆘 <b>Yordam</b>\n\n"
                "<b>Mavjud buyruqlar:</b>\n"
                "• /start - Botni ishga tushirish\n"
                "• /developer - Dasturchi haqida ma'lumot\n"
                "• /help - Bu yordam matni\n\n"
                "<b>Bot haqida:</b>\n"
                "Bu bot sizga turli mavzularda savollar beradi va bilimingizni sinaydi.\n"
                "3 ta qiyinlik darajasi mavjud: Oson🟢, O'rtacha🟡, Qiyin🔴\n\n"
                "Davom etish uchun /start ni bosing!"
            )
        elif language == 'ru':
            message = (
                "🆘 <b>Помощь</b>\n\n"
                "<b>Доступные команды:</b>\n"
                "• /start - Запустить бота\n"
                "• /developer - Информация о разработчике\n"
                "• /help - Этот текст помощи\n\n"
                "<b>О боте:</b>\n"
                "Этот бот задает вам вопросы на различные темы и тестирует ваши знания.\n"
                "Доступно 3 уровня сложности: Легкий🟢, Средний🟡, Сложный🔴\n\n"
                "Нажмите /start для продолжения!"
            )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Bosh menyu | Main menu | Главное меню", callback_data="main_menu")]
    ])

    await update.message.reply_text(
        text=message,
        parse_mode="HTML",
        reply_markup=keyboard
    )



# main() funksiyasiga qo'shish kerak bo'lgan handler
# Menu tugmasi handler'i (main() dan oldin qo'shing)
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_settings:
        # Agar til tanlanmagan bo'lsa, til tanlash
        await update.message.reply_text(
            "🌐 <b>Welcome! | Добро пожаловать! | Xush kelibsiz!</b>\n\n"
            "Please select your language:\n"
            "Пожалуйста, выберите ваш язык:\n"
            "Iltimos, tilni tanlang:",
            parse_mode="HTML",
            reply_markup=create_language_keyboard(),
        )
        return

    language = user_settings[user_id]['language']
    t = TRANSLATIONS[language]

    # Menu xabari
    menu_text = f"📋 <b>{t.get('main_menu', 'Main Menu')}</b>\n\n"
    menu_text += f"{t.get('select_category', 'Select category to start quiz!')}"

    # Menu keyboard
    keyboard = [
        [
            InlineKeyboardButton("🎯 Quiz", callback_data="start_quiz"),
            InlineKeyboardButton("🆘 Yordam", callback_data="help_inline")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", callback_data="developer_inline"),
            InlineKeyboardButton("🌐 Til | Lang", callback_data="change_language")  # Menuda til o'zgartirish tugmasi
        ]
    ]

    await update.message.reply_text(
        text=menu_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Inline callback'lar uchun handler'lar
async def handle_help_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # help_command'ni chaqirish
    update.message = query.message
    await help_command(update, context)


async def handle_developer_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # developer'ni chaqirish
    update.message = query.message
    await developer(update, context)



async def handle_start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_settings:
        await query.answer("Please select language first", show_alert=True)
        return

    language = user_settings[user_id]['language']
    t = TRANSLATIONS[language]

    await query.answer()
    await query.edit_message_text(
        f"🎯 <b>{t.get('select_category', 'Select Category')}</b>",
        parse_mode="HTML",
        reply_markup=build_keyboard(0, language, show_language_button=False)  # Til tugmasini yashirish
    )



# main() funksiyasiga qo'shing:
def main():
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("developer", developer))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))  # ← Yangi qator

    # Callback handlers
    app.add_handler(CallbackQueryHandler(handle_language_selection, pattern=r"^lang_\w+$"))
    app.add_handler(CallbackQueryHandler(handle_change_language, pattern=r"^change_language$"))
    app.add_handler(CallbackQueryHandler(handle_page, pattern=r"^page_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_category_selection, pattern=r"^select_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_answer, pattern=r"^answer_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_next_question, pattern=r"^next_question$"))
    app.add_handler(CallbackQueryHandler(handle_stop_questions, pattern=r"^stop_questions$"))
    app.add_handler(CallbackQueryHandler(handle_restart, pattern=r"^restart_session$"))
    app.add_handler(CallbackQueryHandler(handle_main_menu, pattern=r"^main_menu$"))
    app.add_handler(CallbackQueryHandler(handle_noop, pattern=r"^noop$"))
    app.add_handler(CallbackQueryHandler(handle_skip_question, pattern=r"^skip_question$"))


    # Yangi inline handler'lar
    app.add_handler(CallbackQueryHandler(handle_help_inline, pattern=r"^help_inline$"))
    app.add_handler(CallbackQueryHandler(handle_developer_inline, pattern=r"^developer_inline$"))
    app.add_handler(CallbackQueryHandler(handle_start_quiz, pattern=r"^start_quiz$"))

    # Bot menu'ni sozlash
    async def setup_bot_menu():
        from telegram import BotCommand
        commands = [
            BotCommand("start", "🎯 Start the bot"),
            BotCommand("menu", "📋 Main menu"),
            BotCommand("help", "🆘 Help"),
            BotCommand("developer", "👨‍💻 Developer info")
        ]
        await app.bot.set_my_commands(commands)

    # Bot ishga tushganda menu'ni sozlash
    app.job_queue.run_once(lambda context: setup_bot_menu(), when=1)

    print("🤖 Ketma-ket Savollar Bot ishga tushdi...")
    print("🌐 Tillar: O'zbekcha, English, Русский")
    print("📚 Kategoriyalar: 24 ta")
    print("❓ Savollar: Ketma-ket chiqadi")
    print("🔄 Tarjima: Google Translate API")
    print("🌐 API: OpenTrivia Database")
    print("⚡ Xususiyyat: Fon rejimda tarjima")

    app.run_polling()
if __name__ == "__main__":
    main()
