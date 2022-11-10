import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler

from decimal import Decimal, ROUND_HALF_UP

from selection_dictionaries.OrdinaryCourt_dictionary import (
    dict_instance,
    dict_proceeding,
    dict_adm_case,
    dict_criminal,
    dict_other,
    dict_claim,
    dict_criminal_order
)

from selection_dictionaries.Court_dictionary import dict_type_court

from OrdinaryCourt_calculating_func import (
    calculate_coefficient,
    calculating_state_duty_for_property_and_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_copy_of_court_order,
    calculating_state_duty_for_get_documents
)

from Court_converting_func import (
    converting_user_amount,
    converting_user_fine,
    converting_user_pages,
    raise_incorrect_value
)

from status_log_db.bot_status_log_db import (
    get_column_value,
    add_column_value,
    get_new_counter_value
)

from CSDB_index import (OC_INSTANCE, OC_PROCEEDING, OC_ADM_CASE, OC_CRIMINAL, OC_OTHER, OC_CLAIM, OC_TYPE_CRIMINAL_SUP,
                        OC_DUTY_PROPERTY_ORDER, OC_DUTY_ADM_CASE, OC_DUTY_COURT_ORDER, OC_DUTY_O_DOCUMENTS)

from BaseValue.base_value import base_value

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def choose_instance_oc(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Первая инстанция (ГП)', callback_data='first_instance')],
        [InlineKeyboardButton('Апелляционная инстанция (ГП)', callback_data='appeal')],
        [InlineKeyboardButton('Производство в порядке надзора (ГП)', callback_data='supervisory')],
        [InlineKeyboardButton('Производство по вновь открывшимся обстоятельствам (ГП)', callback_data='newly_facts')],
        [InlineKeyboardButton('Обжалование постановления по делу об административном правонарушении',
                              callback_data='administrative_appeal')],
        [InlineKeyboardButton('Рассмотрение жалобы по уголовному делу',
                              callback_data='criminal')],
        [InlineKeyboardButton('Иные процессуальные действия', callback_data='other')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите судебную инстанцию для гражданского процесса (ГП) или '
                                             'иной вид процесса (процессуальное действие):',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    type_court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'type_court', type_court)
    logger.info(f"User {user_id} has chosen the type of the court "
                f"{dict_type_court[get_column_value(user_id, 'type_court')]}"
                f"- {dict_type_court[get_column_value(user_id, 'type_court')]}")
    update.callback_query.edit_message_text(text=f"Вы выбрали:\n{counter}. "
                                                 f"{dict_type_court[get_column_value(user_id, 'type_court')]}")
    return OC_INSTANCE


def choose_type_of_legal_proceeding_1in(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        [InlineKeyboardButton('Приказное производство', callback_data='order_proceeding')],
        [InlineKeyboardButton('Производство по делам из административно-правовых отношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('Особое производство', callback_data='special_proceeding')],
        [InlineKeyboardButton('Производство по отмене решения третейского суда',
                              callback_data='appeal_arbitration_proceeding')],
        [InlineKeyboardButton('Производство по выдаче исполнительного листа на исполнение медиативного соглашения',
                              callback_data='executive_doc_proceeding')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {user_id} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return OC_PROCEEDING


def choose_type_of_legal_proceeding_app_sup(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        # del order_proceeding
        [InlineKeyboardButton('Производство по делам из административно-правовых отношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('Особое производство', callback_data='special_proceeding')]
        # del appeal_arbitration_proceeding
        # del executive_doc_proceeding
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {user_id} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return OC_PROCEEDING


def choose_type_of_ruling_on_administrative_case(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('О наложение штрафа', callback_data='fine')],
        [InlineKeyboardButton('О наложении иного административного взыскания', callback_data='other_penalty')],
        [InlineKeyboardButton('Не связанное с наложением административного взыскания (в т.ч. о прекращении ДобАП)',
                              callback_data='non_penalty')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите постановления по делу об административном правонарушении, '
                                             'которое обжалуется:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {user_id} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return OC_ADM_CASE


def choose_type_of_criminal_complaint(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Жалоба на отказ в возбуждении УД, производства по ВОО, прекращении УП',
                              callback_data='appeal_non_court_order')],
        [InlineKeyboardButton('Жалоба на приговор (определение, постановление) суда по УД',
                              callback_data='appeal_court_order')],
        [InlineKeyboardButton('Жалоба в части гражданского иска в уголовном процессе',
                              callback_data='in_part_of_civil_lawsuit')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите характер жалобы, подаваемой по уголовному делу (УД):',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {user_id} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return OC_CRIMINAL


def choose_type_of_another_procedural_action(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Рассмотрение иной жалобы', callback_data='another_complaint')],
        [InlineKeyboardButton('Повторная выдача копий судебных постановлений',
                              callback_data='get_copy_of_court_order')],
        [InlineKeyboardButton('Выдача копии решения о расторжении брака', callback_data='get_first_divorce_order')],
        [InlineKeyboardButton('Выдача копии решения о расторжении повторного брака',
                              callback_data='get_repeat_divorce_order')],
        [InlineKeyboardButton('Выдача дубликатов, копий других документов', callback_data='get_documents')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите иное процессуальное действие:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {user_id} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return OC_OTHER


def choose_type_of_nature_of_claim(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property_claim')],
        [InlineKeyboardButton('Требование о взыскании расходов на содержание детей на государственном обеспечении',
                              callback_data='expenses_for_children')],
        [InlineKeyboardButton('Требование о расторжении брака', callback_data='first_divorce')],
        [InlineKeyboardButton('Требование о расторжении повторного брака',
                              callback_data='repeat_divorce')],
        [InlineKeyboardButton('Требование о расторжении брака c отдельными категориями лиц',
                              callback_data='special_divorce')],
        [InlineKeyboardButton('Требование о заключении, изменении, расторжении, незаключенности договора, '
                              'о недействительности сделки', callback_data='contract_dispute_claim')],
        [InlineKeyboardButton('Требование неимущественного характера', callback_data='non-pecuniary_claim')]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер требования (спора):', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    proceeding = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'proceeding', proceeding)
    logger.info(f"User {user_id} has chosen legal proceeding -"
                f" {dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return OC_CLAIM


def choose_type_of_nature_of_claim_for_order(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property_claim')],
        [InlineKeyboardButton('Требование о взыскании расходов на содержание детей на государственном обеспечении',
                              callback_data='expenses_for_children')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер требования приказного производства:',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    proceeding = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'proceeding', proceeding)
    logger.info(f"User {user_id} has chosen legal proceeding -"
                f" {dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return OC_CLAIM


def choose_type_of_nature_of_claim_for_civil_in_criminal(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property_claim')],
        [InlineKeyboardButton('Требование неимущественного характера', callback_data='non-pecuniary_claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер требования гражданского иска в уголовном процессе:',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    criminal = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'criminal', criminal)
    logger.info(f"User {user_id} has chosen type of criminal complaint -"
                f" {dict_criminal[get_column_value(user_id, 'criminal')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_criminal[get_column_value(user_id, 'criminal')]}")
    return OC_CLAIM


def choose_type_of_appeal_court_criminal_order(update: Update, _) -> int:
    keyboard = [
        [InlineKeyboardButton('Повторная надзорная жалоба, подаваемая в Верховный Суд Республики Беларусь',
                              callback_data='repeat_supreme_sup_criminal')],
        [InlineKeyboardButton('Первичная или иная повторная надзорная жалоба, не казанная в предыдущем пункте',
                              callback_data='other_sup_criminal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер жалобы, на приговор, определение, постановление суда '
                                             'по уголовному делу:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    criminal = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'criminal', criminal)
    logger.info(f"User {user_id} has chosen type_of_criminal_complaint -"
                f" {dict_criminal[get_column_value(user_id, 'criminal')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_criminal[get_column_value(user_id, 'criminal')]}")
    return OC_TYPE_CRIMINAL_SUP


def define_amount(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen nature of claim - "
                f"{dict_claim[get_column_value(user_id, 'claim')]}")

    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text('Укажите цену иска (сумму взыскания, оспариваемую сумму):')
    return OC_DUTY_PROPERTY_ORDER


def define_fine(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    ruling_on_adm = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'ruling_on_adm', ruling_on_adm)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    logger.info(f"User {user_id} has chosen type of a ruling on an administrative case"
                f" - {dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    update.callback_query.message.reply_text(f'Укажите размер штрафа.\n\n\n'
                                             '<i>В случае, если на день расчёта государственной пошлины установлен иной'
                                             f' размер базовой величины ({base_value} BYN), по сравнению с тем, который'
                                             f' существовал на день'
                                             ' наложения административного взыскания в виде штрафа, дполнительно '
                                             'укажите размер базовой величины, существовавшей на день наложения '
                                             'взыскания в формате:\n\n <b>штраф=базовая_величина (например, 290=29)'
                                             '</b></i>\n\n'
                                             'Если размер базовой величины не изменялся,'
                                             'достаточно указать только размер штрафа:', parse_mode='HTML')
    return OC_DUTY_ADM_CASE


def define_number_of_pages_court_order(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    another_action = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'another_action', another_action)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_other[get_column_value(user_id, 'another_action')]}")
    logger.info(f"User {user_id} has chosen another procedural action - "
                f"{dict_other[get_column_value(user_id, 'another_action')]}")
    update.callback_query.message.reply_text('Укажите количество страниц копии(й) судебного(ых) постановления(ий), '
                                             'подлежащих изготовлению:')
    return OC_DUTY_COURT_ORDER


def define_number_of_other_documents(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    another_action = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'another_action', another_action)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_other[get_column_value(user_id, 'another_action')]}")
    logger.info(f"User {user_id} has chosen another procedural action - "
                f"{dict_other[get_column_value(user_id, 'another_action')]}")
    update.callback_query.message.reply_text('Укажите количество страниц документа(ов), подлежащих изготовлению:')
    return OC_DUTY_O_DOCUMENTS


def determine_size_of_state_duty_for_property_and_order_claim(update: Update, _) -> int:
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the price of the claim (amount of recovery) - {update.message.text}")
    try:
        convert_claim_price = converting_user_amount(str(update.message.text))
    except ValueError:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = calculating_state_duty_for_property_and_order(convert_claim_price, base_value, user_id)
        state_duty = float(Decimal(str(state_duty)).quantize(Decimal('1.00'), ROUND_HALF_UP))
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_administrative_case(update: Update, _) -> int:
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the size of fine - {update.message.text}")
    convert_b_v = base_value
    str_to_list_fine = converting_user_fine(str(update.message.text))
    if len(str_to_list_fine) == 2:
        try:
            convert_fine = converting_user_amount(str_to_list_fine[0])
            convert_b_v = converting_user_amount(str_to_list_fine[1])
        except ValueError:
            update.message.reply_text(raise_incorrect_value()[0])
            update.message.reply_text(raise_incorrect_value()[1])
        else:
            state_duty = calculating_state_duty_for_administrative_case(convert_fine, convert_b_v, base_value)
            state_duty = float(Decimal(str(state_duty)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                      parse_mode='HTML')
            return ConversationHandler.END
    elif len(str_to_list_fine) == 1:
        try:
            convert_fine = converting_user_amount(str_to_list_fine[0])
        except ValueError:
            update.message.reply_text(raise_incorrect_value()[0])
            update.message.reply_text(raise_incorrect_value()[1])
        else:
            state_duty = calculating_state_duty_for_administrative_case(convert_fine, convert_b_v, base_value)
            state_duty = float(Decimal(str(state_duty)).quantize(Decimal('1.00'), ROUND_HALF_UP))
            update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                      parse_mode='HTML')
            return ConversationHandler.END
    else:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])


def determine_size_of_state_duty_for_get_copy_of_court_order(update: Update, _) -> int:
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the number of pages - {update.message.text}")
    try:
        convert_pages = converting_user_pages(str(update.message.text))
    except ValueError:
        update.message.reply_text('Значение количества страниц должно быть целым неотрицательным числом')
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = calculating_state_duty_for_get_copy_of_court_order(convert_pages, base_value)
        state_duty = float(Decimal(str(state_duty)).quantize(Decimal('1.00'), ROUND_HALF_UP))
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_get_documents(update: Update, _) -> int:
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the number of pages - {update.message.text}")
    try:
        convert_pages = converting_user_pages(str(update.message.text))
    except ValueError:
        update.message.reply_text('Значение количества страниц должно быть целым неотрицательным числом')
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = calculating_state_duty_for_get_documents(convert_pages, base_value)
        state_duty = float(Decimal(str(state_duty)).quantize(Decimal('1.00'), ROUND_HALF_UP))
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_x01(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    another_action = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'another_action', another_action)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_other[get_column_value(user_id, 'another_action')]}")
    logger.info(f"User {user_id} has chosen another procedural action - "
                f"{dict_other[get_column_value(user_id, 'another_action')]}")
    state_duty = float(Decimal(str(base_value * 0.1)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x1(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)
    if get_column_value(user_id, 'proceeding') and \
            get_column_value(user_id, 'proceeding') in ('lawsuit_proceeding', 'order_proceeding'):
        claim = update.callback_query.data
        add_column_value(user_id, 'claim', claim)
        logger.info(f"User {user_id} has chosen nature of claim - {dict_claim[get_column_value(user_id, 'claim')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_claim[get_column_value(user_id, 'claim')]}")
    elif get_column_value(user_id, 'criminal') and get_column_value(user_id, 'criminal') == 'appeal_court_order':
        criminal_order = update.callback_query.data
        add_column_value(user_id, 'criminal_order', criminal_order)
        update.callback_query.edit_message_text(
            text=f"{counter}. Вы выбрали:\n{dict_criminal_order[get_column_value(user_id, 'criminal_order')]}")
        logger.info(f"User {user_id} has chosen the type of appeal court of criminal order - "
                    f"{dict_criminal_order[get_column_value(user_id, 'criminal_order')]}")
    elif get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'administrative_appeal':
        ruling_on_adm = update.callback_query.data
        add_column_value(user_id, 'ruling_on_adm', ruling_on_adm)
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
        logger.info(f"User {user_id} has chosen type of a ruling on an administrative case"
                    f" - {dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    elif get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'criminal':
        criminal = update.callback_query.data
        add_column_value(user_id, 'criminal', criminal)
        update.callback_query.edit_message_text(
            text=f"{counter}. Вы выбрали:\n{dict_criminal[get_column_value(user_id, 'criminal')]}")
        logger.info(f"User {user_id} has chosen the type of appeal court of criminal order - "
                    f"{dict_criminal[get_column_value(user_id, 'criminal')]}")
    elif get_column_value(user_id, 'instance') and \
            get_column_value(user_id, 'instance') in ('first_instance', 'appeal', 'supervisory'):
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen legal proceeding - "
                    f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = float(Decimal(str(base_value * 1 * coefficient)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x2(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)
    if get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'other':
        another_action = update.callback_query.data
        add_column_value(user_id, 'another_action', another_action)
        logger.info(f"User {user_id} has chosen another procedural action - "
                    f"{dict_other[get_column_value(user_id, 'another_action')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_other[get_column_value(user_id, 'another_action')]}")
    elif get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'criminal':
        criminal_order = update.callback_query.data
        add_column_value(user_id, 'criminal_order', criminal_order)
        logger.info(f"User {user_id} has chosen the type of appeal court of criminal order - "
                    f"{dict_criminal_order[get_column_value(user_id, 'criminal_order')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"""{dict_criminal_order[get_column_value(user_id, 
                                                                                               'criminal_order')]}""")
    elif get_column_value(user_id, 'instance') and \
            get_column_value(user_id, 'instance') in ('first_instance', 'appeal', 'supervisory'):
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen legal proceeding - "
                    f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = float(Decimal(str(base_value * 2 * coefficient)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x3(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)
    if get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') == 'lawsuit_proceeding':
        claim = update.callback_query.data
        add_column_value(user_id, 'claim', claim)
        logger.info(f"User {user_id} has chosen another procedural action - "
                    f"{dict_claim[get_column_value(user_id, 'claim')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_claim[get_column_value(user_id, 'claim')]}")
    if get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'criminal':
        claim = update.callback_query.data
        add_column_value(user_id, 'claim', claim)
        logger.info(f"User {user_id} has chosen nature of claim - {dict_claim[get_column_value(user_id, 'claim')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_claim[get_column_value(user_id, 'claim')]}")
    elif get_column_value(user_id, 'instance') and get_column_value(user_id, 'instance') == 'other':
        another_action = update.callback_query.data
        add_column_value(user_id, 'another_action', another_action)
        logger.info(f"User {user_id} has chosen another procedural action - "
                    f"{dict_other[get_column_value(user_id, 'another_action')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_other[get_column_value(user_id, 'another_action')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = float(Decimal(str(base_value * 3 * coefficient)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x4(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen another procedural action - "
                f"{dict_claim[get_column_value(user_id, 'claim')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = float(Decimal(str(base_value * 4 * coefficient)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x5(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen another procedural action - "
                f"{dict_claim[get_column_value(user_id, 'claim')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = float(Decimal(str(base_value * 5 * coefficient)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x8(update: Update, _) -> int:
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen another procedural action - "
                f"{dict_claim[get_column_value(user_id, 'claim')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = float(Decimal(str(base_value * 8 * coefficient)).quantize(Decimal('1.00'), ROUND_HALF_UP))
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_for_newly_facts(update, _):
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    logger.info(f"User {user_id} has chosen an instance - {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.message.reply_text('Освобождаются от государственной пошлины при обращении в суд организации '
                                             'и физические лица за рассмотрение  заявления о пересмотре (возобновлении)'
                                             ' дела по вновь открывшимся обстоятельствам\n'
                                             '(пп. 1.8.4 ст. 285 Налогового кодекса Республики Беларусь)')
    return ConversationHandler.END