import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from selection_dictionaries.EconomicCourt_dictionary import (
    dict_instance,
    dict_proceeding,
    dict_adm_case,
    dict_other,
    dict_claim,
    dict_subject,
    dict_court
)

from selection_dictionaries.Court_dictionary import dict_type_court

from EconomicCourt_calculating_func import (
    calculate_coefficient,
    calculating_state_duty_for_property,
    calculating_state_duty_for_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_documents
)

from Court_converting_func import (
    converting_user_amount,
    converting_user_fine,
    converting_user_pages
)

from status_log_db.bot_status_log_db import *

from CSDB_index import (EC_INSTANCE, EC_PROCEEDING, EC_OTHER, EC_CLAIM, EC_DUTY_PROPERTY, EC_DUTY_ORDER, EC_SUBJECT,
                        EC_COURT_1, EC_COURT_2, EC_ADM_CASE, EC_DUTY_ADM_CASE, EC_DUTY_DOCUMENTS)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

base_value = 32.0

status_log = {}


def choose_instance(update, _):
    keyboard = [
        [InlineKeyboardButton('Производство в суде первой инстанции', callback_data='first_instance')],
        [InlineKeyboardButton('Производство в суде апелляционной инстанции', callback_data='appeal')],
        [InlineKeyboardButton('Производство в суде кассационной инстанции', callback_data='cassation')],
        [InlineKeyboardButton('Производство по пересмотру судебных постановлений в порядке надзора',
                              callback_data='supervisory')],
        [InlineKeyboardButton('Производство по вновь открывшимся обстоятельствам', callback_data='newly_facts')],
        [InlineKeyboardButton('Обжалование постановления по делу об административном правонарушении',
                              callback_data='administrative_appeal')],
        [InlineKeyboardButton('Иные процессуальные действия', callback_data='other')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите судебную инстанцию:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    type_court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'type_court', type_court)
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen the type of the court "
                f"- {dict_type_court[get_column_value(user_id, 'type_court')]}")
    update.callback_query.edit_message_text(text=f"Вы выбрали:\n{counter}. "
                                                 f"{dict_type_court[get_column_value(user_id, 'type_court')]}")
    return EC_INSTANCE


def choose_type_of_legal_proceeding_1in(update, _):
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        [InlineKeyboardButton('Приказное производство', callback_data='order_proceeding')],
        [InlineKeyboardButton('Производство по проверке законности ННПА, действий (бездействия) '
                              'государственных органов', callback_data='appeal_NNLA_proceeding')],
        [InlineKeyboardButton('Производство об установлении юридических фактов', callback_data='special_proceeding')],
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
        [InlineKeyboardButton('Производство по признанию и исполнению решений инсторанных содов',
                              callback_data='acknowledge_proceeding')],
        [InlineKeyboardButton('Производство по выдаче исполнительного документа на исполнение решения третейского суда,'
                              ' медиативного соглашения', callback_data='executive_doc_proceeding')],
        [InlineKeyboardButton('Производство по обеспечению иска, рассматриваемого третейским судом, '
                              'медиавтивного соглашения', callback_data='securing_proceeding')],
        [InlineKeyboardButton('Производство по отмене решений третейских, арбитражных судов',
                              callback_data='appeal_arbitration_proceeding')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return EC_PROCEEDING


def choose_type_of_legal_proceeding_app(update, _):
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        # del order
        [InlineKeyboardButton('Производство по проверке законности ННПА, действий (бездействия) '
                              'государственных органов', callback_data='appeal_NNLA_proceeding')],
        [InlineKeyboardButton('Производство об установлении юридических фактов', callback_data='special_proceeding')],
        # del bankrupt
        [InlineKeyboardButton('Производство по жалобам на нотариальные действия',
                              callback_data='appeal_notarial_proceeding')],
        [InlineKeyboardButton('Производство по делам из административных и иных публичных правоотношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('Производство по жалобам на ответы на обращения юридических лиц (ИП, граждан)',
                              callback_data='appeal_claim_proceeding')],
        [InlineKeyboardButton('Производство по обжалованию действий (бездействия) судебного исполнителя',
                              callback_data='appeal_bailiff_proceeding')],
        # del acknowledge
        [InlineKeyboardButton('Производство по выдаче исполнительного документа на исполнение решения третейского суда,'
                              ' медиативного соглашения', callback_data='executive_doc_proceeding')],
        [InlineKeyboardButton('Производство по обеспечению иска, рассматриваемого третейским судом, '
                              'медиавтивного соглашения', callback_data='securing_proceeding')],
        [InlineKeyboardButton('Производство по отмене решений третейских, арбитражных судов',
                              callback_data='appeal_arbitration_proceeding')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return EC_PROCEEDING


def choose_type_of_legal_proceeding_cas_sup(update, _):
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        # del order
        [InlineKeyboardButton('Производство по проверке законности ННПА, действий (бездействия) '
                              'государственных органов', callback_data='appeal_NNLA_proceeding')],
        [InlineKeyboardButton('Производство об установлении юридических фактов', callback_data='special_proceeding')],
        # del bankrupt
        [InlineKeyboardButton('Производство по жалобам на нотариальные действия',
                              callback_data='appeal_notarial_proceeding')],
        [InlineKeyboardButton('Производство по делам из административных и иных публичных правоотношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('Производство по жалобам на ответы на обращения юридических лиц (ИП, граждан)',
                              callback_data='appeal_claim_proceeding')],
        [InlineKeyboardButton('Производство по обжалованию действий (бездействия) судебного исполнителя',
                              callback_data='appeal_bailiff_proceeding')],
        [InlineKeyboardButton('Производство по признанию и исполнению решений инсторанных содов',
                              callback_data='acknowledge_proceeding')],
        [InlineKeyboardButton('Производство по выдаче исполнительного документа на исполнение решения третейского суда,'
                              ' медиативного соглашения', callback_data='executive_doc_proceeding')],
        [InlineKeyboardButton('Производство по обеспечению иска, рассматриваемого третейским судом, '
                              'медиавтивного соглашения', callback_data='securing_proceeding')],
        [InlineKeyboardButton('Производство по отмене решений третейских, арбитражных судов',
                              callback_data='appeal_arbitration_proceeding')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите вид судопроизводства:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return EC_PROCEEDING


def choose_type_of_ruling_on_administrative_case(update, _):
    keyboard = [
        [InlineKeyboardButton('О наложение штрафа', callback_data='fine')],
        [InlineKeyboardButton('О наложении иного административного взыскания', callback_data='other_penalty')],
        [InlineKeyboardButton('Не связанное с наложением административного взыскания (в т.ч. о прекращении)',
                              callback_data='non_penalty')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите постановления по делу об административном правонарушении, '
                                             'которое обжалуется:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return EC_ADM_CASE


def choose_type_of_another_procedural_action(update, _):
    keyboard = [
        [InlineKeyboardButton('Рассмотрение иной жалобы', callback_data='another_complaint')],
        [InlineKeyboardButton('Выдача судом дубликатов, копий документов', callback_data='get_documents')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите иное процессуальное действие:', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    instance = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'instance', instance)
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen instance -"
                f" {dict_instance[get_column_value(user_id, 'instance')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return EC_OTHER


def choose_type_of_nature_of_claim(update, _):
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property_claim')],  # +
        [InlineKeyboardButton('Требование о привлечении к субсидиарной ответственности по долгам юридического лица',
                              callback_data='subsidiary_liability_claim')],
        [InlineKeyboardButton('Требование по спору о качестве поставленного товара',
                              callback_data='quality_of_goods_claim')],
        [InlineKeyboardButton('Требование неимущественного характера', callback_data='non-pecuniary_claim')],
        [InlineKeyboardButton('Требование о заключении, изменении, расторжении, незаключенности договора, '
                              'о недействительности сделки', callback_data='contract_dispute_claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите характер требования (спора):', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    proceeding = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'proceeding', proceeding)
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen legal proceeding -"
                f" {dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return EC_CLAIM


def choose_subject(update, _):
    keyboard = [
        [InlineKeyboardButton('Юридическое лицо', callback_data='entity')],
        [InlineKeyboardButton('Индивидуальный предприниматель',
                              callback_data='individual_entrepreneur')],
        [InlineKeyboardButton('Физическое лицо', callback_data='individual')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите юридический статус лица, подающего исковое заявление '
                                             '(заявление, жалобу):', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)

    if get_column_value(user_id, 'proceeding'):
        claim = update.callback_query.data
        add_column_value(user_id, 'claim', claim)
        logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen nature of claim - "
                    f"{dict_claim[get_column_value(user_id, 'claim')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_claim[get_column_value(user_id, 'claim')]}")
    else:
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen legal proceeding - "
                    f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return EC_SUBJECT


def choose_court(update, _):
    keyboard = [
        [InlineKeyboardButton('Верховный Суд Республики Беларусь', callback_data='supreme_court')],
        [InlineKeyboardButton('Экономические суды областей (города Минска)',
                              callback_data='regional_court')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите суд, в который подаётся исковое заявление (заявление, жалоба):',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)

    if get_column_value(user_id, 'claim'):
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen subject - "
                    f"{dict_subject[get_column_value(user_id, 'subject')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
        return EC_COURT_1
    elif get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') != 'lawsuit_proceeding':
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen subject - "
                    f"{dict_subject[get_column_value(user_id, 'subject')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
        return EC_COURT_1
    elif get_column_value(user_id, 'proceeding'):
        claim = update.callback_query.data
        add_column_value(user_id, 'claim', claim)
        logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen nature of claimt - "
                    f"{dict_claim[get_column_value(user_id, 'claim')]}")
        update.callback_query.edit_message_text(text=f"{len(status_log) - 1}. Вы выбрали:\n"
                                                     f"{dict_claim[get_column_value(user_id, 'claim')]}")
        return EC_COURT_1
    else:
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen proceeding - "
                    f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        return EC_COURT_2


def define_price_of_claim(update, _):
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen nature of claim - "
                f"{dict_claim[get_column_value(user_id, 'claim')]}")

    coefficient = calculate_coefficient(
        user_id)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ОН ЖЕ ЕСТЬ В ФОРМУЛЕ НАФИГА ОН ЕЩЁ И ЗДЕСЬ??????
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text('Укажите цену иска (оспариваемую сумму):')
    return EC_DUTY_PROPERTY


def define_amount_for_order_proceeding(update, _):
    user_id = update.callback_query.from_user.id
    proceeding = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'proceeding', proceeding)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen legal proceeding - "
                f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    update.callback_query.message.reply_text('Укажите сумму взыскания:')
    return EC_DUTY_ORDER


def define_fine(update, _):
    user_id = update.callback_query.from_user.id
    ruling_on_adm = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'ruling_on_adm', ruling_on_adm)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen type of a ruling on an administrative case"
                f" - {dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    update.callback_query.message.reply_text('Укажите размер штрафа.\n\n\n'
                                             '<i>В случае, если на день расчёта государственной пошлины установлен иной'
                                             ' размер базовой величины, по сравнению с тем, который существовал на день'
                                             ' наложения административного взыскания в виде штрафа, дполнительно '
                                             'укажите размер базовой величины, существовавшей на день наложения '
                                             'взыскания в формате:\n\n <b>штраф=базовая_величина (например, 290=29)'
                                             '</b></i>\n\n'
                                             'Если размер базовой величины не изменялся,'
                                             'достаточно указать только размер штрафа:', parse_mode='HTML')
    return EC_DUTY_ADM_CASE


def define_number_of_documents(update, _):
    user_id = update.callback_query.from_user.id
    another_action = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'another_action', another_action)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_other[get_column_value(user_id, 'another_action')]}")
    logger.info(f"User {get_column_value(user_id, 'user_id')} has chosen another procedural action - "
                f"{dict_other[get_column_value(user_id, 'another_action')]}")
    update.callback_query.message.reply_text('Укажите количество страниц документа(ов), подлежащих изготовлению:')
    return EC_DUTY_DOCUMENTS


def determine_size_of_state_duty_for_property_claim(update, _):
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the price of the claim - {update.message.text}")
    try:
        convert_claim_price = converting_user_amount(str(update.message.text))
    except ValueError:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = round(calculating_state_duty_for_property(convert_claim_price, base_value, user_id), 2)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_order_claim(update, _):
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified amount of recovery - {update.message.text}")
    try:
        convert_amount_of_recovery = converting_user_amount(str(update.message.text))
    except ValueError:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = round(calculating_state_duty_for_order(convert_amount_of_recovery, base_value, user_id), 2)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_administrative_case(update, _):
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
            state_duty = round(calculating_state_duty_for_administrative_case(convert_fine, convert_b_v, base_value), 2)
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
            state_duty = round(calculating_state_duty_for_administrative_case(convert_fine, convert_b_v, base_value), 2)
            update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                      parse_mode='HTML')
            return ConversationHandler.END
    else:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])


def determine_size_of_state_duty_for_get_documents(update, _):
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the number of pages - {update.message.text}")
    try:
        convert_pages = converting_user_pages(str(update.message.text))
    except ValueError:
        update.message.reply_text('Значение количества страниц должно быть целым неотрицательным числом')
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = round(calculating_state_duty_for_get_documents(convert_pages, base_value), 2)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_x05(update, _):
    user_id = update.callback_query.from_user.id
    another_action = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'another_action', another_action)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_other[get_column_value(user_id, 'another_action')]}")
    logger.info(f"User {user_id} has chosen another procedural action - "
                f"{dict_other[get_column_value(user_id, 'another_action')]}")
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{base_value * 0.5}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x1(update, _):
    user_id = update.callback_query.from_user.id
    ruling_on_adm = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'ruling_on_adm', ruling_on_adm)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    logger.info(f"User {user_id} has chosen type of a ruling on an administrative case"
                f" - {dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}"),
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{base_value * 1}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x5(update, _):
    user_id = update.callback_query.from_user.id
    subject = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'subject', subject)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_subject[get_column_value(user_id, 'subject')]}")
    logger.info(f"User {user_id} has chosen subject - {dict_subject[get_column_value(user_id, 'subject')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 5 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x10(update, _):
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)
    if get_column_value(user_id, 'claim'):
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {user_id} has chosen subject - {dict_subject[get_column_value(user_id, 'subject')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
    elif get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') in {
        'appeal_NNLA_proceeding', 'administrative_proceeding', 'appeal_claim_proceeding', 'appeal_bailiff_proceeding'
    }:
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {user_id} has chosen subject - {dict_subject[get_column_value(user_id, 'subject')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
    elif get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') == 'special_proceeding':
        court = update.callback_query.data
        add_column_value(user_id, 'court', court)
        logger.info(f"User {user_id} has chosen a court - {dict_court[get_column_value(user_id, 'court')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_court[get_column_value(user_id, 'court')]}")
    else:
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen legal proceeding - "
                    f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 10 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x15(update, _):
    user_id = update.callback_query.from_user.id
    court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'court', court)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_court[get_column_value(user_id, 'court')]}")
    logger.info(f"User {user_id} has chosen a court - {dict_court[get_column_value(user_id, 'court')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 15 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x20(update, _):
    user_id = update.callback_query.from_user.id
    court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'court', court)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_court[get_column_value(user_id, 'court')]}")
    logger.info(f"User {user_id} has chosen a court - {dict_court[get_column_value(user_id, 'court')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 20 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x25(update, _):
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen nature of claim - {dict_claim[get_column_value(user_id, 'claim')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 25 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x50(update, _):
    user_id = update.callback_query.from_user.id
    court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'court', court)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_court[get_column_value(user_id, 'court')]}")
    logger.info(f"User {user_id} has chosen a court - {dict_court[get_column_value(user_id, 'court')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 50 * coefficient}</b> BYN', parse_mode='HTML')
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


def raise_incorrect_value():
    return (
        'Значение указано некорректно.\nФормат ввода значения:\n'
        '1111 (для целочисленных значений)\nили\n1111.11 (для вещественных значений)',
        'Повторно введите значение:'
    )
