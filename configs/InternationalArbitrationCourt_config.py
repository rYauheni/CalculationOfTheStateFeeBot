import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler

from decimal import Decimal, ROUND_HALF_UP

from selection_dictionaries.InternationalArbitrationCourt_dictionary import (
    dict_subject,
    dict_proceeding,
    dict_instance,
    dict_claim
)

from selection_dictionaries.Court_dictionary import dict_type_court

from calc_n_convert_func.InternationalArbitrationCourt_calculating_func import (
    calculate_coefficient,
    calculating_state_duty_for_property_for_resident,
    calculating_state_duty_for_property_for_non_resident
)

from calc_n_convert_func.Court_converting_func import (
    converting_user_amount,
    raise_incorrect_value
)

from status_log_db.bot_status_log_db import (
    get_column_value,
    add_column_value,
    get_new_counter_value
)

from CSDB_index import (IAC_SUBJECT, IAC_PROCEEDING, IAC_INSTANCE, IAC_CLAIM, IAC_A_FEE_PROPERTY)

from BaseValue.base_value import base_value

note = '\n\n<i>*Арбитражный сбор определён без учёта его увеличения на сумму налога на добавленную стоимость.\n' \
       'Необходимость увеличения арбитражного сбора на сумму НДС следует уточнять в МАС</i>'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def choose_subject_iac(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Резиденты Республики Беларусь (обе стороны)', callback_data='resident')],
        [InlineKeyboardButton('Одна из сторон (или обе) - нерезидент', callback_data='non-resident')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите статус субъектов, являющихся сторонами спора:',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    type_court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'type_court', type_court)
    logger.info(f"User {user_id} has chosen the type of the court "
                f"- {get_column_value(user_id, 'type_court')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_type_court[get_column_value(user_id, 'type_court')]}")
    return IAC_SUBJECT


def choose_type_of_legal_proceeding(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Обычная процедура', callback_data='ordinary')],
        [InlineKeyboardButton('Упрощённая процедура', callback_data='simplified')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите вид процедуры рассмотрения споров:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    subject = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'subject', subject)
    logger.info(f"User {user_id} has chosen legal proceeding -"
                f" {get_column_value(user_id, 'subject')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_subject[get_column_value(user_id, 'subject')]}")
    return IAC_PROCEEDING


def choose_instance(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Единоличное разрешение (1 арбитр)', callback_data='one')],
        [InlineKeyboardButton('Коллегиальное разрешение (3 арбитра)', callback_data='collegial')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите состав арбитражного суда (количество арбитров) '
                                             'для разрешения спора:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)
    if get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'resident':
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen legal proceeding -"
                    f" {get_column_value(user_id, 'proceeding')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    else:
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {user_id} has chosen subject -"
                    f" {get_column_value(user_id, 'subject')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
    return IAC_INSTANCE


def choose_type_of_nature_of_claim(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property_claim')],
        [InlineKeyboardButton('Требование неимущественного характера', callback_data='non-pecuniary_claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер требования (спора):', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)
    if get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') == 'ordinary' or \
            get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'non-resident':
        instance = update.callback_query.data
        add_column_value(user_id, 'instance', instance)
        logger.info(f"User {user_id} has chosen instance (composition of the court) -"
                    f" {get_column_value(user_id, 'instance')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_instance[get_column_value(user_id, 'instance')]}")
    else:
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen legal proceeding -{get_column_value(user_id, 'proceeding')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return IAC_CLAIM


def define_amount(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    logger.info(f"User {user_id} has chosen nature of claim {get_column_value(user_id, 'claim')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")

    if get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'resident':
        update.callback_query.message.reply_text('Укажите цену иска в белорусских рублях (BYN):')
    elif get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'non-resident':
        update.callback_query.message.reply_text('Укажите цену иска в Евро (EUR):')
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")

    return IAC_A_FEE_PROPERTY


def determine_size_of_arbitration_fee_for_property_claim(update: Update, _) -> int:
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the price of the claim - {update.message.text}")
    try:
        convert_claim_price = converting_user_amount(str(update.message.text))
    except ValueError:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        if get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'resident':
            arbitration_fee = calculating_state_duty_for_property_for_resident(convert_claim_price, base_value, user_id)
            arbitration_fee = float(Decimal(str(arbitration_fee)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            update.message.reply_text(f'Размер арбитражного сбора составляет:\n\n<b>{arbitration_fee}</b> BYN*{note}',
                                      parse_mode='HTML')
        elif get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'non-resident':
            arbitration_fee = calculating_state_duty_for_property_for_non_resident(convert_claim_price, user_id)
            arbitration_fee = float(Decimal(str(arbitration_fee)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            update.message.reply_text(f'Размер арбитражного сбора составляет:\n\n<b>{arbitration_fee}</b> EUR*{note}',
                                      parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_arbitration_fee_for_non_pecuniary_claim(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    logger.info(f"User {user_id} has chosen nature of claim - {get_column_value(user_id, 'claim')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")

    if get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'resident':
        arbitration_fee = float(Decimal(str(base_value * 50)).quantize(Decimal('1.00'), ROUND_HALF_UP))
        update.callback_query.message.reply_text(f'Размер арбитражного сбора составляет:\n\n'
                                                 f'<b>{arbitration_fee}</b> BYN*{note}', parse_mode='HTML')
    elif get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'non-resident':
        update.callback_query.message.reply_text(f'Если иск не имеет цены, размер арбитражного сбора определяет '
                                                 f'Председатель МАС в сумме не менее\n700 EUR', parse_mode='HTML')
    return ConversationHandler.END
