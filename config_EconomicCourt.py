import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a message with options for choosing a court instance using inline buttons"""
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
    and calls the next function."""
    query = update.callback_query

    query.answer('ASDFGHJKL')  # ВСПЛЫВАЮЩАЯ ПОДСКАЗКА
    print('000000000')
    if True:  # choosing a court instance
        if query.data == 'first_instance':
            query.edit_message_text(text='Вы выбрали:\n"Производство в суде первой инстанции"')
            choose_type_of_legal_proceeding(update, context)
        elif query.data == 'appeal':
            query.edit_message_text(text='Вы выбрали:\n"Производство в суде апелляционной инстанции"')
            choose_type_of_legal_proceeding(update, context)
        elif query.data == 'cassation':
            query.edit_message_text(text='Вы выбрали:\n"Производство в суде кассационной инстанции"')
            choose_type_of_legal_proceeding(update, context)
        elif query.data == 'supervisory':
            query.edit_message_text(text='Вы выбрали:\n'
                                         '"Производство по пересмотру судебных постановлений в порядке надзора"')
            choose_type_of_legal_proceeding(update, context)
        elif query.data == 'newly_facts':
            query.edit_message_text(text='Вы выбрали:\n"Производство по вновь открывшимся обстоятельствам"')
        elif query.data == 'other':
            query.edit_message_text(text='Вы выбрали:\n"Иные процессуальные действия"')
    if True:  # choosing a type of legal proceeding
        if query.data == 'lawsuit_proceeding':
            query.edit_message_text(text='Вы выбрали:\n"Исковое производство"')
            choose_nature_of_claim(update, context)
        elif query.data == 'order_proceeding':
            query.edit_message_text(text='Вы выбрали:\n"Приказное производство"')
        elif query.data == 'appeal_NNLA_proceeding':
            query.edit_message_text(
                text='Вы выбрали:\n"Производство по проверке законности ННПА, действий (бездействия) '
                     'государственных органов"')
        elif query.data == 'special_proceeding':
            query.edit_message_text(text='Вы выбрали:\n'
                                         '"Производство об установлении юридических фактов"')
        elif query.data == 'acknowledge_proceeding':
            query.edit_message_text(text='Вы выбрали:\n"Производство по признанию решений инсторанных содов, '
                                         'иностранных арбитражных решений"')
        elif query.data == 'appeal_arbitration_proceeding':
            query.edit_message_text(
                text='Вы выбрали:\n"Производство по обжалованию решений третейских, арбитражных судов"')
        elif query.data == 'bankrupt_proceeding':
            query.edit_message_text(text='Вы выбрали:\n"Производство об экономической несостоятельности (банкротстве)"')
        elif query.data == 'appeal_notarial_proceeding':
            query.edit_message_text(text='Вы выбрали:\n'
                                         '"Производство по делам из административных и иных публичных правоотношений"')
        elif query.data == 'administrative_proceeding':
            query.edit_message_text(text='Производство по делам из административных и иных публичных правоотношений"')
        elif query.data == 'appeal_claim_proceeding':
            query.edit_message_text(text='Вы выбрали:\n"Производство по жалобам '
                                         'на ответы на обращения юридических лиц (ИП, граждан)"')
        elif query.data == 'appeal_bailiff_proceeding':
            query.edit_message_text(text='Вы выбрали:\n'
                                         '"Производство по обжалованию действий (бездействия) судебного исполнителя"')
    if True:  # choosing a type of nature of claim
        if query.data == 'property claim':
            query.edit_message_text(text='Вы выбрали:\n"Требование имущественного характера"')
            sizing_of_state_duty_for_property_claims(update, context)
        elif query.data == 'quality_of_goods':
            query.edit_message_text(text='Вы выбрали:\n"Требование по спору о качестве поставленного товара"')
        elif query.data == 'non-pecuniary_claim':
            query.edit_message_text(text='Вы выбрали:\n"Требование неимущественного характера"')
        elif query.data == 'contract_dispute':
            query.edit_message_text(text='Вы выбрали:\n"Требование по спору, связанному с заключением, изменением '
                                         'или расторжением договора, о признании договора незаключенным, о признании '
                                         'сделки недествительной, об установлении факта ничтожности сделки"')


def choose_type_of_legal_proceeding(update: Update, context: CallbackContext) -> None:
    """Sends a message with options for choosing a type of legal proceeding."""
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        [InlineKeyboardButton('Приказное производство', callback_data='order_proceeding')],
        [InlineKeyboardButton('Производство по проверке законности ННПА, действий (бездействия) '
                              'государственных органов', callback_data='appeal_NNLA_proceeding')],
        [InlineKeyboardButton('Производство об установлении юридических фактов', callback_data='special_proceeding')],
        [InlineKeyboardButton('Производство по признанию решений инсторанных содов, иностранных арбитражных решений',
                              callback_data='acknowledge_proceeding')],
        [InlineKeyboardButton('Производство по обжалованию решений третейских, арбитражных судов',
                              callback_data='appeal_arbitration_proceeding')],
        [InlineKeyboardButton('Производство об экономической несостоятельности (банкротстве)',
                              callback_data='bankrupt_proceeding')],
        [InlineKeyboardButton('Производство по жалобам на нотариальные действия',
                              callback_data='appeal_notarial_proceeding')],
        [InlineKeyboardButton('Производство по делам из административных и иных публичных правоотношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('Производство по жалобам на ответы на обращения юридических лиц (ИП, граждан)',
                              callback_data='appeal_claim_proceeding')],
        [InlineKeyboardButton('Производство по обжалованию действий (бездействия) судебного исполнителя',
                              callback_data='appeal_bailiff_proceeding')],
    ]
    logger.info("User %s started to choose some type of legal proceeding",
                update.callback_query.message.from_user.first_name)
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)


def choose_nature_of_claim(update: Update, context: CallbackContext) -> None:
    """Sends a message with options for choosing a type of nature of claim."""
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property claim')],
        [InlineKeyboardButton('Требование по спору о качестве поставленного товара', callback_data='quality_of_goods')],
        [InlineKeyboardButton('Требование неимущественного характера', callback_data='non-pecuniary_claim')],
        [InlineKeyboardButton('Требование о заключении, изменении, расторжении, незаключенности договора, '
                              'о недействительности сделки', callback_data='contract_dispute')]
    ]
    logger.info("User %s started to choose some type of nature of claim",
                update.callback_query.message.from_user.first_name)
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер требования (спора):', reply_markup=reply_markup)


def sizing_of_state_duty_for_property_claims(update: Update, context: CallbackContext) -> None:
    """-----------------------------------------------------"""
    logger.info("User %s started to indicate the size of the claim",
                update.callback_query.message.from_user.first_name)
    update.callback_query.message.reply_text('Укажите размер требования:')
    dengi(update, context)


def dengi(update: Update, context: CallbackContext) -> None:
    """Sends a message with options for choosing a court instance using inline buttons"""
    logger.info("User %s started to choose some instance", update.message.from_user.first_name)
    size = str(update.callback_query.message.text)
    return size


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
