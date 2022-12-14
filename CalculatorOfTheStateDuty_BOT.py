#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
This bot allows you to calculate the state duty for the courts of the Republic of Belarus,
as well as the arbitration fee for the International Arbitration Court at the BelCCI, taking into account the following:
- for all courts;
- for all types of processes;
- for all judicial instances;
- for all types of legal proceedings;
- for all kinds of claims.

The procedure for calculating the state duty (arbitration fee) is determined based on the
Tax Code of the Republic of Belarus, the Civil Procedure Code of the Republic of Belarus,
the Economic Procedure Code of the Republic of Belarus,
the regulations of the International Arbitration Court at the BelCCI,
the resolution of the Council of Ministers of the Republic of Belarus
on the approval of establishing the size of the base value.

The calculation of the state duty (arbitration fee) is approximate.
The calculation made by this bot CAN NOT be used as evidence in court and DOES NOT HAVE legal force.
"""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

from status_log_db.bot_status_log_db import (
    create_table,
    add_new_row,
    add_column_value
)

from configs.EconomicCourt_config import choose_instance_ec

from configs.OrdinaryCourt_config import choose_instance_oc

from configs.IntellectualPropertyCourt_config import choose_instance_ipc

from configs.InternationalArbitrationCourt_config import choose_subject_iac

from handlers.EconomicCourt_handler import ec_conv_handler_dict

from handlers.OrdinaryCourt_handler import oc_conv_handler_dict

from handlers.IntellectualPropertyCourt_handler import ipc_conv_handler_dict

from handlers.InternationalArbitrationCourt_handler import iac_conv_handler_dict

from CSDB_index import TYPE_COURT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, _) -> int:
    create_table()
    keyboard = [
        [InlineKeyboardButton('?????? ?????????? ????????????????????', callback_data='ordinary_court')],
        [InlineKeyboardButton('?????? ???? ?????????? ???????????????????????????????? ??????????????????????????',
                              callback_data='intellectual_property_court')],
        [InlineKeyboardButton('?????????????????????????? ??????', callback_data='economic_court')],
        [InlineKeyboardButton('?????????????????????????? ?????????????????????? ?????? ?????? ????????????',
                              callback_data='international_arbitration_court')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('???????????????? ???????????????? ????????????????????:', reply_markup=reply_markup)
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    print(user_id)
    print(user_name)
    add_new_row(user_id)  # if raw with current user_id exists all values in this row (except user_id value) will clear
    add_column_value(user_id, 'user_name', user_name)
    add_column_value(user_id, 'counter', '0')

    logger.info(f"User {user_id} started to choose some instance")
    return TYPE_COURT


def cancel(update: Update, _) -> int:
    user = update.message.from_user
    logger.info(f'User {user.id} has canceled process')
    update.message.reply_text(
        '???????????????? ???????????? ???????? ????????????????.\n?????? ?????????????????????????? ???????????? ?????????????? /start'
    )
    return ConversationHandler.END


def info(update: Update, _):
    user = update.message.from_user
    logger.info(f'User {user.id} has received info')
    update.message.reply_text('info_check')


def select_actions_dict() -> dict:
    base_dict = {TYPE_COURT: [
        CallbackQueryHandler(choose_instance_oc, pattern="^" + 'ordinary_court' + "$"),
        CallbackQueryHandler(choose_instance_ipc,
                             pattern="^" + 'intellectual_property_court' + "$"),
        CallbackQueryHandler(choose_instance_ec, pattern="^" + 'economic_court' + "$"),
        CallbackQueryHandler(choose_subject_iac,
                             pattern="^" + 'international_arbitration_court' + "$")
    ]}
    conv_handler_dict = \
        base_dict | ec_conv_handler_dict | oc_conv_handler_dict | ipc_conv_handler_dict | iac_conv_handler_dict
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
    info_handler = CommandHandler('info', info)
    dispatcher.add_handler(info_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
