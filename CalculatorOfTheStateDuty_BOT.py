import logging

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, ConversationHandler)

from EconomicCourt_config import choose_instance_ec

from OrdinaryCourt_config import choose_instance_oc

from IntellectualPropertyCourt_config import choose_instance_ipc

from status_log_db.bot_status_log_db import (
    create_table,
    add_new_raw,
    add_column_value
)

from handlers.EconomicCourt_handler import ec_conv_handler_dict

from handlers.OrdinaryCourt_handler import oc_conv_handler_dict

from handlers.IntellectualPropertyCourt_handler import ipc_conv_handler_dict

from CSDB_index import TYPE_COURT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update, _):
    create_table()
    keyboard = [
        [InlineKeyboardButton('Суд общей юрисдикции', callback_data='ordinary_court')],
        [InlineKeyboardButton('Суд по делам интеллектуальной собственности', callback_data='intellectual_property_court')],
        [InlineKeyboardButton('Экономический суд', callback_data='economic_court')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите судебную юрисдикцию:', reply_markup=reply_markup)
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    print(user_id)
    print(user_name)
    add_new_raw(user_id)
    add_column_value(user_id, 'user_name', user_name)
    add_column_value(user_id, 'counter', '0')

    logger.info(f"User {user_id} started to choose some instance")
    return TYPE_COURT


def cancel(update, _):
    user = update.message.from_user
    logger.info(f'User {user.first_name} has canceled process')
    update.message.reply_text(
        'Действие работы бота прервано.\nДля возобновления работы введите /start'
    )
    return ConversationHandler.END


def select_actions_dict():
    base_dict = {TYPE_COURT: [
        CallbackQueryHandler(choose_instance_ec, pattern="^" + 'economic_court' + "$"),
        CallbackQueryHandler(choose_instance_oc, pattern="^" + 'ordinary_court' + "$"),
        CallbackQueryHandler(choose_instance_ipc,
                             pattern="^" + 'intellectual_property_court' + "$")]}
    conv_handler_dict = base_dict | ec_conv_handler_dict | oc_conv_handler_dict | ipc_conv_handler_dict
    return conv_handler_dict


def main():
    updater = Updater("5675091266:AAHbP-X6DxIrQ5FqXwkn9Nt03ayzA74CP1Y")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states=select_actions_dict(),
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
