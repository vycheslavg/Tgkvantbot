import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext import Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

questions = [
    ("Какой из этих аспектов технологий вас больше всего интересует?\n"
     "A) Виртуальная реальность и дополненная реальность\n"
     "B) Медиа и контент\n"
     "C) Анализ данных и статистика\n"
     "D) Энергетические технологии\n"
     "E) Дизайн и эстетика\n"
     "F) Новые технологии и их внедрение\n"
     "G) Робототехника и автоматизация\n"
     "H) Программирование и разработка ПО", 8),
    
    ("Какое ваше любимое занятие в свободное время?\n"
     "A) Играть в видеоигры или исследовать VR-опыт\n"
     "B) Смотреть фильмы или создавать контент\n"
     "C) Работать с данными или решать логические задачи\n"
     "D) Изучать новые источники энергии или экологии\n"
     "E) Рисовать, проектировать или заниматься рукоделием\n"
     "F) Чтение научной литературы или изучение новых технологий\n"
     "G) Собирание моделей или программирование роботов\n"
     "H) Создание приложений или веб-сайтов", 8),

    ("Какую проблему вы бы хотели решить с помощью технологий?\n"
     "A) Создание более увлекательного опыта для пользователей\n"
     "B) Улучшение качества медиа-контента и его распространения\n"
     "C) Оптимизация процессов обработки данных\n"
     "D) Разработка устойчивых энергетических решений\n"
     "E) Создание функционального и красивого дизайна продуктов\n"
     "F) Инновации в технологиях и их применение в жизни\n"
     "G) Упрощение задач с помощью автоматизации и робототехники\n"
     "H) Разработка программного обеспечения для различных нужд", 8),

    ("Какой тип работы вам более всего подходит?\n"
     "A) Креативная работа с технологиями\n"
     "B) Работа в сфере медиа и коммуникаций\n"
     "C) Аналитическая работа с данными\n"
     "D) Исследовательская работа в области энергетики\n"
     "E) Дизайнерская работа с продуктами\n"
     "F) Техническая работа с новыми технологиями\n"
     "G) Практическая работа с роботами и автоматизацией\n"
     "H) Программирование и разработка программных решений", 8)
]
user_answers = {}

def start(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение при команде /start."""
    update.message.reply_text('Привет! Я бот для тестирования. Напиши /test, чтобы пройти тест.')

def test(update: Update, context: CallbackContext) -> None:
    """Начинает тест."""
    user_id = update.message.from_user.id
    user_answers[user_id] = []
    
    update.message.reply_text(questions[0][0])
    context.user_data['question_index'] = 0

def answer(update: Update, context: CallbackContext) -> None:
    """Обрабатывает ответы пользователя."""
    user_id = update.message.from_user.id
    question_index = context.user_data.get('question_index', 0)

    if user_id not in user_answers:
        update.message.reply_text('Пожалуйста, начните тест с команды /test.')
        return

    if question_index < len(questions):
        answer = update.message.text.strip().upper()
        if answer in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            user_answers[user_id].append(answer)
            question_index += 1
            context.user_data['question_index'] = question_index
            
            if question_index < len(questions):
                                update.message.reply_text(questions[question_index][0])
            else:
                calculate_result(update)
        else:
            update.message.reply_text('Пожалуйста, выберите правильный вариант ответа (A-H).')
    else:
        update.message.reply_text('Тест уже завершен. Напишите /test, чтобы пройти его снова.')

def calculate_result(update: Update) -> None:
    """Подсчитывает результат теста."""
    user_id = update.message.from_user.id
    answers = user_answers[user_id]
    
    score = {letter: 0 for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']}
    
    for answer in answers:
        score[answer] += 1

    result = max(score, key=score.get)
    
    if result == 'A':
        update.message.reply_text('Вы склонны к VR/AR-квантуму.')
    elif result == 'B':
        update.message.reply_text('Вы склонны к Медиаквантуму.')
    elif result == 'C':
        update.message.reply_text('Вы склонны к Data-квантуму.')
    elif result == 'D':
        update.message.reply_text('Вы склонны к Энерджиквантуму.')
    elif result == 'E':
        update.message.reply_text('Вы склонны к Промышленному дизайну.')
    elif result == 'F':
        update.message.reply_text('Вы склонны к Хайтеку.')
    elif result == 'G':
        update.message.reply_text('Вы склонны к Промробоквантуму.')
    elif result == 'H':
        update.message.reply_text('Вы склонны к IT-квантуму.')

def main() -> None:
    """Запускает бота."""
    updater = Updater("7970839685:AAHDPwdD38U7S4oLITCT3n5XxVE4OBguLCE")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("test", test))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, answer))

    # Запуск бота
    updater.start_polling()
    
    updater.idle()

if __name__ == '__main__':
    main()
