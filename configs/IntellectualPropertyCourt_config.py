import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler

from selection_dictionaries.IntellectualPropertyCourt_dictionary import (
    dict_instance,
    dict_proceeding,
    dict_other,
    dict_claim,
    dict_subject
)

from selection_dictionaries.Court_dictionary import dict_type_court

from calc_n_convert_func.IntellectualPropertyCourt_calculating_func import (
    calculate_coefficient,
    calculating_state_duty_for_property,
    calculating_state_duty_for_get_copy_of_court_order_for_entity,
    calculating_state_duty_for_get_copy_of_court_order_for_individual
)

from calc_n_convert_func.rounding_func import round_dec

from calc_n_convert_func.exceptions import FormatError, SizeError

from calc_n_convert_func.Court_converting_func import (
    converting_user_amount,
    converting_user_pages,
    raise_incorrect_value,
    raise_incorrect_size,
    raise_exception
)

from orm.orm_functions import (
    get_column_value,
    add_column_value,
    get_new_counter_value
)

from CSDB_index import (IPC_INSTANCE, IPC_PROCEEDING, IPC_OTHER, IPC_CLAIM, IPC_SUBJECT_1, IPC_SUBJECT_2,
                        IPC_DUTY_PROPERTY, IPC_DUTY_COURT_ORDER)

from settings.settings import BASE_VALUE

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def choose_instance_ipc(update: Update, _) -> int:
    """ type_court -> instance """
    keyboard = [
        [InlineKeyboardButton('Первая инстанция', callback_data='first_instance')],
        [InlineKeyboardButton('Производство в порядке надзора', callback_data='supervisory')],
        [InlineKeyboardButton('Производство по вновь открывшимся обстоятельствам', callback_data='newly_facts')],
        [InlineKeyboardButton('Иные процессуальные действия', callback_data='other')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите судебную инстанцию или иное процессуальное действие:',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    type_court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'type_court', type_court)
    logger.info(f"User {user_id} has chosen the type of the court - {get_column_value(user_id, 'type_court')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_type_court[get_column_value(user_id, 'type_court')]} *\n\n"
                                                 f"<i>* При обращении <b>нерезидентов</b> в судебную коллегию по делам"
                                                 f"интеллектуальной собственности Верховного Суда Республики Беларусь"
                                                 f" государственная пошлина уплачивается в иностранной валюте \n"
                                                 f"(статья 289 Налогового кодекса Республики Беларусь)</i>",
                                            parse_mode='HTML')
    return IPC_INSTANCE


def choose_type_of_legal_proceeding(update: Update, _) -> int:
    """ type_court -> instance (first, supervisory) -> legal_proceeding """
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        [InlineKeyboardButton('Обжалование решения органа по вопросам интеллектуальной собственности',
                              callback_data='appealing_decision_on_ipi')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {user_id} has chosen instance - {get_column_value(user_id, 'instance')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return IPC_PROCEEDING


def choose_type_of_another_procedural_action(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action """
    keyboard = [
        [InlineKeyboardButton('Рассмотрение иной жалобы', callback_data='another_complaint')],
        [InlineKeyboardButton('Повторная выдача копий судебных постановлений',
                              callback_data='get_copy_of_court_order')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите иное процессуальное действие:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {user_id} has chosen instance - {get_column_value(user_id, 'instance')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return IPC_OTHER


def choose_type_of_nature_of_claim(update: Update, _) -> int:
    """ type_court -> instance (first, supervisory) -> legal_proceeding (lawsuit) -> claim """
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property_claim')],
        [InlineKeyboardButton('Требование неимущественного характера', callback_data='non-pecuniary_claim')]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер требования (спора):', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    proceeding = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'proceeding', proceeding)
    logger.info(f"User {user_id} has chosen legal proceeding - {get_column_value(user_id, 'proceeding')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return IPC_CLAIM


def choose_subject(update: Update, _) -> int:
    """ type_court ->
        [instance (first, supervisory) ->
            [legal_proceeding (lawsuit) -> claim (non-pecuniary)] or [legal_proceeding (appealing_decision)]] or
        [instance (other)] ->
         subject """
    keyboard = [
        [InlineKeyboardButton('Юридическое лицо (организация)', callback_data='entity')],
        [InlineKeyboardButton('Физическое лицо', callback_data='individual')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите юридический статус лица, подающего исковое заявление '
                                             '(заявление, жалобу):', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)

    if get_column_value(user_id, 'instance') and \
            get_column_value(user_id, 'instance') in ('first_instance', 'supervisory'):
        if get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') == 'lawsuit_proceeding':
            claim = update.callback_query.data
            add_column_value(user_id, 'claim', claim)
            logger.info(f"User {user_id} has chosen nature of claim - {get_column_value(user_id, 'claim')}")
            update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                         f"{dict_claim[get_column_value(user_id, 'claim')]}")
        elif get_column_value(user_id, 'instance') and \
                get_column_value(user_id, 'instance') in ('first_instance', 'supervisory'):
            proceeding = update.callback_query.data
            add_column_value(user_id, 'proceeding', proceeding)
            logger.info(f"User {user_id} has chosen legal proceeding - {get_column_value(user_id, 'proceeding')}")
            update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                         f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        return IPC_SUBJECT_1
    elif get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'other':
        another_action = update.callback_query.data
        add_column_value(user_id, 'another_action', another_action)
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_other[get_column_value(user_id, 'another_action')]}")
        logger.info(f"User {user_id} has chosen another procedural action - "
                    f"{get_column_value(user_id, 'another_action')}")
        return IPC_SUBJECT_2


def define_amount(update: Update, _) -> int:
    """ type_court -> instance (first, supervisory) -> legal_proceeding (lawsuit) -> claim (property) -> amount """
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen nature of claim - {get_column_value(user_id, 'claim')}")

    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text('Укажите цену иска:')
    return IPC_DUTY_PROPERTY


def define_number_of_pages_court_order(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action (get_copy_of_court_order) -> define_pages """
    user_id = update.callback_query.from_user.id
    subject = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'subject', subject)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_subject[get_column_value(user_id, 'subject')]}")
    logger.info(f"User {user_id} has chosen another procedural action - {get_column_value(user_id, 'subject')}")
    update.callback_query.message.reply_text('Укажите количество страниц копии(й) судебного(ых) постановления(ий), '
                                             'подлежащих изготовлению:')
    return IPC_DUTY_COURT_ORDER


def determine_size_of_state_duty_for_property_claim(update: Update, _) -> int:
    """ type_court -> instance (first, supervisory) -> legal_proceeding (lawsuit) -> claim (property) -> amount ->
    state_duty_property """
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the price of the claim - {update.message.text}")
    try:
        convert_claim_price = converting_user_amount(str(update.message.text))
    except FormatError:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    except SizeError:
        update.message.reply_text(raise_incorrect_size()[0])
        update.message.reply_text(raise_incorrect_size()[1])
    except Exception:
        update.message.reply_text(raise_exception()[0])
        update.message.reply_text(raise_exception()[1])
    else:
        state_duty = calculating_state_duty_for_property(convert_claim_price, BASE_VALUE, user_id)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_get_copy_of_court_order(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action (get_copy_of_court_order) -> define_pages ->
    state_duty_get_copy """
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the number of pages - {update.message.text}")
    try:
        convert_pages = converting_user_pages(str(update.message.text))
    except FormatError:
        update.message.reply_text('Значение количества страниц должно быть целым неотрицательным числом')
        update.message.reply_text(raise_incorrect_value()[1])
    except SizeError:
        update.message.reply_text(raise_incorrect_size()[0])
        update.message.reply_text(raise_incorrect_size()[1])
    except Exception:
        update.message.reply_text(raise_exception()[0])
        update.message.reply_text(raise_exception()[1])
    else:
        if get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'entity':
            state_duty = calculating_state_duty_for_get_copy_of_court_order_for_entity(convert_pages, BASE_VALUE)
            update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                      parse_mode='HTML')
        elif get_column_value(user_id, 'subject') and get_column_value(user_id, 'subject') == 'individual':
            state_duty = calculating_state_duty_for_get_copy_of_court_order_for_individual(convert_pages, BASE_VALUE)
            update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                      parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_x05(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action (another_complaint) -> state_duty_x05 """
    user_id = update.callback_query.from_user.id
    another_action = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'another_action', another_action)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_other[get_column_value(user_id, 'another_action')]}")
    logger.info(f"User {user_id} has chosen another procedural action - {get_column_value(user_id, 'another_action')}")
    state_duty = round_dec(BASE_VALUE * 0.5)
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x20(update: Update, _) -> int:
    """ type_court -> instance (first, supervisory) -> legal_proceeding -> [claim (non-pecuniary)] ->
    subject (individual) - state_duty_x20 """
    user_id = update.callback_query.from_user.id
    subject = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'subject', subject)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_subject[get_column_value(user_id, 'subject')]}")
    logger.info(f"User {user_id} has chosen subject - {get_column_value(user_id, 'subject')}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 20) * coefficient)
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x50(update: Update, _) -> int:
    """ type_court -> instance (first, supervisory) -> legal_proceeding -> [claim (non-pecuniary)] ->
    subject (entity) - state_duty_x50 """
    user_id = update.callback_query.from_user.id
    subject = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'subject', subject)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_subject[get_column_value(user_id, 'subject')]}")
    logger.info(f"User {user_id} has chosen subject - {get_column_value(user_id, 'subject')}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 50) * coefficient)
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_for_newly_facts(update, _):
    """ type_court -> instance (newly_facts) -> state_duty_newly_facts """
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    logger.info(f"User {user_id} has chosen an instance - {get_column_value(user_id, 'instance')}")
    update.callback_query.message.reply_text('Освобождаются от государственной пошлины при обращении в суд организации '
                                             'и физические лица за рассмотрение  заявления о пересмотре (возобновлении)'
                                             ' дела по вновь открывшимся обстоятельствам\n'
                                             '(пп. 1.8.4 ст. 285 Налогового кодекса Республики Беларусь)')
    return ConversationHandler.END
