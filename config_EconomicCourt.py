import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a message with options for choosing a court using inline buttons"""
    keyboard = [
        [InlineKeyboardButton('Производство в суде первой инстанции', callback_data='first_instance')],
        [InlineKeyboardButton('Производство в суде апелляционной инстанции', callback_data='appeal')],
        [InlineKeyboardButton('Производство в суде кассационной инстанции', callback_data='cassation')],
        [InlineKeyboardButton('Производство по пересмотру судебных постановлений в порядке надзора',
                              callback_data='supervisory')],
        [InlineKeyboardButton('Производство по вновь открывшимся обстоятельствам', callback_data='newly_facts')],
        [InlineKeyboardButton('Иные процессуальные действия', callback_data='other')]
    ]
    logger.info("User %s started to choose some instance", update.message.from_user.first_name)
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите <i><b>судебную</b></i> инстанцию:', reply_markup=reply_markup,
                              parse_mode='HTML')


def button_choose_instance(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery when a court instance is selected, updates the message text,
    and calls the select function of choosing a type of legal proceeding."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer('ASDFGHJKL')  # ВСПЛЫВАЮЩАЯ ПОДСКАЗКА

    if query.data == 'first_instance':
        query.edit_message_text(text='Вы выбрали:\n"Производство в суде первой инстанции"')
    choose_type_of_legal_proceeding(update, context)


def choose_type_of_legal_proceeding(update: Update, context: CallbackContext) -> None:
    """Sends a message with options for choosing a type of legal proceeding."""
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='isk')],
        [InlineKeyboardButton('Приказное производство', callback_data='prikaz')],
    ]
    logger.info("User %s started to choose some type of legal proceeding", update.message.from_user.first_name)
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Наберите (или выберите из меню) /start для начала работы.")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater('5675091266:AAHbP-X6DxIrQ5FqXwkn9Nt03ayzA74CP1Y')

    updater.dispatcher.add_handler(CommandHandler('start', start_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_choose_instance))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
