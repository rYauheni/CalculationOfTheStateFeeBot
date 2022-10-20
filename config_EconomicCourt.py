import logging
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

from dictionary_EconomicCourt import (
    dict_instance,
    dict_proceeding,
    dict_adm_case,
    dict_other,
    dict_claim,
    dict_subject,
    dict_court
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

INSTANCE, PROCEEDING, OTHER, CLAIM, DUTY_PROPERTY, DUTY_ORDER = range(6)
SUBJECT, COURT_1, COURT_2, ADM_CASE, DUTY_ADM_CASE, DUTY_DOCUMENTS = range(6, 12)
base_value = 32
status_log = dict()


def start(update, _):
    status_log.clear()
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

    update.message.reply_text('Выберите судебную инстанцию:', reply_markup=reply_markup)
    status_log['name'] = update.message.from_user.first_name
    logger.info(f"User {status_log['name']} started to choose some instance")
    return INSTANCE


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
    status_log['instance'] = update.callback_query.data
    logger.info(f"User {status_log['name']} has chosen instance - {status_log['instance']}")
    print(status_log)
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_instance[status_log["instance"]]}"')
    return PROCEEDING


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
    status_log['instance'] = update.callback_query.data
    logger.info(f"User {status_log['name']} has chosen instance - {status_log['instance']}")
    print(status_log)
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_instance[status_log["instance"]]}"')
    return PROCEEDING


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
    status_log['instance'] = update.callback_query.data
    logger.info(f"User {status_log['name']} has chosen instance - {status_log['instance']}")
    print(status_log)
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_instance[status_log["instance"]]}"')
    return PROCEEDING


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
    status_log['instance'] = update.callback_query.data
    logger.info(f"User {status_log['name']} has chosen instance - {status_log['instance']}")
    print(status_log)
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_instance[status_log["instance"]]}"')
    return ADM_CASE


def choose_type_of_another_procedural_action(update, _):
    keyboard = [
        [InlineKeyboardButton('Рассмотрение иной жалобы', callback_data='another_complaint')],
        [InlineKeyboardButton('Выдача судом дубликатов, копий документов', callback_data='get_documents')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Выберите иное процессуальное действие:', reply_markup=reply_markup)
    status_log['instance'] = update.callback_query.data
    logger.info(f"User {status_log['name']} has chosen instance - {status_log['instance']}")
    print(status_log)
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_instance[status_log["instance"]]}"')
    return OTHER


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
    status_log['proceeding'] = update.callback_query.data
    logger.info(f"User {status_log['name']} has chosen legal proceeding - {status_log['proceeding']}")
    print(status_log)
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_proceeding[status_log["proceeding"]]}"')
    return CLAIM


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
    if 'proceeding' in status_log:
        status_log['claim'] = update.callback_query.data
        logger.info(f"User {status_log['name']} has chosen nature of claim - {status_log['claim']}")
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_claim[status_log["claim"]]}"')
    else:
        status_log['proceeding'] = update.callback_query.data
        logger.info(f"User {status_log['name']} has chosen legal proceeding - {status_log['proceeding']}")
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_proceeding[status_log["proceeding"]]}"')
    print(status_log)
    return SUBJECT


def choose_court(update, _):
    keyboard = [
        [InlineKeyboardButton('Верховный Суд Республики Беларусь', callback_data='supreme_court')],
        [InlineKeyboardButton('Экономические суды областей (города Минска)',
                              callback_data='regional_court')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите суд, в который подаётся исковое заявление (заявление, жалоба):',
                                             reply_markup=reply_markup)
    if 'claim' in status_log:
        status_log['subject'] = update.callback_query.data
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_subject[status_log["subject"]]}"')
        logger.info(f"User {status_log['name']} has chosen subject - {status_log['subject']}")
        print(status_log)
        return COURT_1
    elif 'proceeding' in status_log and status_log['proceeding'] != 'lawsuit_proceeding':
        status_log['subject'] = update.callback_query.data
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_subject[status_log["subject"]]}"')
        logger.info(f"User {status_log['name']} has chosen subject - {status_log['subject']}")
        print(status_log)
        return COURT_1
    elif 'proceeding' in status_log:
        status_log['claim'] = update.callback_query.data
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_claim[status_log["claim"]]}"')
        logger.info(f"User {status_log['name']} has chosen nature of claim - {status_log['claim']}")
        print(status_log)
        return COURT_1
    else:
        status_log['proceeding'] = update.callback_query.data
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_proceeding[status_log["proceeding"]]}"')
        logger.info(f"User {status_log['name']} has chosen nature of claim - {status_log['proceeding']}")
        print(status_log)
        return COURT_2


def define_price_of_claim(update, _):
    status_log['claim'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_claim[status_log["claim"]]}"')
    logger.info(f"User {status_log['name']} has chosen nature of claim - {status_log['claim']}")
    print(status_log)
    coefficient = calculate_coefficient()
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text('Укажите цену иска (оспариваемую сумму):')
    return DUTY_PROPERTY


def define_amount_for_order_proceeding(update, _):
    status_log['proceeding'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_proceeding[status_log["proceeding"]]}"')
    print(status_log)
    logger.info(f"User {status_log['name']} has chosen legal proceeding - {status_log['proceeding']}")
    update.callback_query.message.reply_text('Укажите сумму взыскания:')
    return DUTY_ORDER


def define_fine(update, _):
    status_log['ruling_on_adm'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_adm_case[status_log["ruling_on_adm"]]}"')
    print(status_log)
    logger.info(f"User {status_log['name']} has chosen type of a ruling on an administrative case"
                f" - {status_log['ruling_on_adm']}")
    update.callback_query.message.reply_text('Укажите размер штрафа.\n\n\n'
                                             '<i>В случае, если на день расчёта государственной пошлины установлен иной'
                                             ' размер базовой величины, по сравнению с тем, который существовал на день'
                                             ' наложения административного взыскания в виде штрафа, дполнительно '
                                             'укажите размер базовой величины, существовавшей на день наложения '
                                             'взыскания в формате:\n\n <b>штраф=базовая_величина (например, 290=29)'
                                             '</b></i>\n\n'
                                             'Если размер базовой величины не изменялся,'
                                             'достаточно указать только размер штрафа:', parse_mode='HTML')
    return DUTY_ADM_CASE


def define_number_of_documents(update, _):
    status_log['another_action'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_other[status_log["another_action"]]}"')
    print(status_log)
    logger.info(f"User {status_log['name']} has chosen another procedural action - {status_log['another_action']}")
    update.callback_query.message.reply_text('Укажите количество страниц документа(ов), подлежащих изготовлению:')
    return DUTY_DOCUMENTS


def determine_size_of_state_duty_for_property_claim(update, _):
    logger.info(f"User {status_log['name']} has specified the price of the claim - {update.message.text}")
    convert_claim_price = converting_user_amount(str(update.message.text))
    print(convert_claim_price)
    if not convert_claim_price:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = round(calculating_state_duty_for_property(convert_claim_price), 2)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_order_claim(update, _):
    logger.info(f"User {status_log['name']} has specified amount of recovery - {update.message.text}")
    convert_amount_of_recovery = converting_user_amount(str(update.message.text))
    print(convert_amount_of_recovery)
    if not convert_amount_of_recovery:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = round(calculating_state_duty_for_order(convert_amount_of_recovery), 2)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_administrative_case(update, _):
    logger.info(f"User {status_log['name']} has specified the size of fine - {update.message.text}")
    str_to_list_fine = converting_user_fine(str(update.message.text))
    convert_fine = converting_user_amount(str_to_list_fine[0])
    print(convert_fine)
    convert_b_v = base_value
    if len(str_to_list_fine) == 2:
        convert_b_v = converting_user_amount(str_to_list_fine[1])
        print(convert_b_v)
    if not convert_fine or not convert_b_v:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = round(calculating_state_duty_for_administrative_case(convert_fine, convert_b_v), 2)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_get_documents(update, _):
    logger.info(f"User {status_log['name']} has specified the number of pages - {update.message.text}")
    convert_pages = converting_user_pages(str(update.message.text))
    print(convert_pages)
    if not convert_pages:
        update.message.reply_text('Значение количества страниц должно быть целым неотрицательным числом')
        update.message.reply_text(raise_incorrect_value()[1])
    else:
        state_duty = round(calculating_state_duty_for_get_documents(convert_pages), 2)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_x05(update, _):
    status_log['another_action'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_other[status_log["another_action"]]}"')
    print(status_log)
    logger.info(f"User {status_log['name']} has chosen another procedural action - {status_log['another_action']}")
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{base_value * 0.5}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x1(update, _):
    status_log['ruling_on_adm'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_adm_case[status_log["ruling_on_adm"]]}"')
    print(status_log)
    logger.info(f"User {status_log['name']} has chosen type of a ruling on an administrative case"
                f" - {status_log['ruling_on_adm']}"),
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{base_value * 1}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x5(update, _):
    status_log['subject'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_subject[status_log["subject"]]}"')
    print(status_log)
    logger.info(f"User {status_log['name']} has chosen subject - {status_log['subject']}")
    coefficient = calculate_coefficient()
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 5 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x10(update, _):
    if 'claim' in status_log:
        status_log['subject'] = update.callback_query.data
        logger.info(f"User {status_log['name']} has chosen subject - {status_log['subject']}")
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_subject[status_log["subject"]]}"')
    elif 'proceeding' in status_log and status_log['proceeding'] in {
        'appeal_NNLA_proceeding', 'administrative_proceeding', 'appeal_claim_proceeding', 'appeal_bailiff_proceeding'
    }:
        status_log['subject'] = update.callback_query.data
        logger.info(f"User {status_log['name']} has chosen subject - {status_log['subject']}")
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_subject[status_log["subject"]]}"')
    elif 'proceeding' in status_log and status_log['proceeding'] == 'special_proceeding':
        status_log['court'] = update.callback_query.data
        logger.info(f"User {status_log['name']} has chosen a court - {status_log['court']}")
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_court[status_log["court"]]}"')
    else:
        status_log['proceeding'] = update.callback_query.data
        logger.info(f"User {status_log['name']} has chosen legal proceeding - {status_log['proceeding']}")
        update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                     f'"{dict_proceeding[status_log["proceeding"]]}"')
    coefficient = calculate_coefficient()
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 10 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x15(update, _):
    status_log['court'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_court[status_log["court"]]}"')
    print(status_log)
    logger.info(f"User {status_log['name']} has chosen a court - {status_log['court']}")
    coefficient = calculate_coefficient()
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 15 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x20(update, _):
    status_log['court'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_court[status_log["court"]]}"')
    logger.info(f"User {status_log['name']} has chosen a court - {status_log['court']}")
    coefficient = calculate_coefficient()
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 20 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x25(update, _):
    status_log['claim'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_claim[status_log["claim"]]}"')
    logger.info(f"User {status_log['name']} has chosen nature of claim - {status_log['claim']}")
    coefficient = calculate_coefficient()
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 25 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x50(update, _):
    status_log['court'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_court[status_log["court"]]}"')
    logger.info(f"User {status_log['name']} has chosen a court - {status_log['court']}")
    coefficient = calculate_coefficient()
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n'
        f'<b>{base_value * 50 * coefficient}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_for_newly_facts(update, _):
    status_log['instance'] = update.callback_query.data
    update.callback_query.edit_message_text(text=f'{len(status_log) - 1}. Вы выбрали:\n'
                                                 f'"{dict_instance[status_log["instance"]]}"')
    logger.info(f"User {status_log['name']} has chosen an instance - {status_log['instance']}")
    update.callback_query.message.reply_text('Освобождаются от государственной пошлины при обращении в суд организации '
                                             'и физические лица за рассмотрение  заявления о пересмотре (возобновлении)'
                                             ' дела по вновь открывшимся обстоятельствам\n'
                                             '(пп. 1.8.4 ст. 285 Налогового кодекса Республики Беларусь)')
    return ConversationHandler.END


def converting_user_amount(amount):
    amount = re.sub(',', '.', amount)
    amount = re.sub(' ', '', amount)
    data_type_check = re.search('^\d+\.*\d*$', amount)
    if data_type_check:
        if float(amount) >= 0:
            return round(float(amount), 2)
        return None
    return None


def converting_user_fine(fine):
    if fine.count('=') == 1:
        return fine.split('=')
    return [fine]


def converting_user_pages(number):
    if number.isdigit() and int(number) >= 0:
        return int(number)
    return None


def calculate_coefficient():
    coefficient = 1
    if 'instance' in status_log and status_log['instance'] in {'appeal', 'cassation', 'supervisory'}:
        coefficient *= 0.8
    if 'claim' in status_log and status_log['claim'] == 'quality_of_goods_claim':
        coefficient *= 0.8
    return coefficient


def calculating_state_duty_for_property(claim_price):
    coefficient = calculate_coefficient()
    if claim_price * 0.05 < base_value * 25:
        return base_value * 25 * coefficient
    if claim_price < base_value * 1000:
        return claim_price * 0.05 * coefficient
    if claim_price < base_value * 10000:
        return base_value * 1000 * 0.05 + (claim_price - (base_value * 1000)) * 0.03 * coefficient
    else:
        if claim_price * 0.01 < base_value * 1000 * 0.05 + base_value * 9000 * 0.03:
            return base_value * 1000 * 0.05 + base_value * 9000 * 0.03 * coefficient
        return claim_price * 0.01 * coefficient


def calculating_state_duty_for_order(amount_of_recovery):
    coefficient = calculate_coefficient()
    if amount_of_recovery < base_value * 100:
        return base_value * 2 * coefficient
    elif base_value * 100 <= amount_of_recovery < base_value * 300:
        return base_value * 5 * coefficient
    elif amount_of_recovery >= base_value * 300:
        return base_value * 7 * coefficient


def calculating_state_duty_for_administrative_case(fine, b_v):
    if fine < b_v * 10:
        return base_value * 0.5
    elif b_v * 10 <= fine < b_v * 100:
        return base_value * 2
    elif fine >= b_v * 100:
        return base_value * 3


def calculating_state_duty_for_get_documents(pages):
    return base_value * 0.2 + pages * base_value * 0.03


def raise_incorrect_value():
    return (
        'Значение указано некорректно.\nФормат ввода значения:\n'
        '1111 (для целочисленных значений)\nили\n1111.11 (для вещественных значений)',
        'Повторно введите значение:'
    )


def cancel(update, _):
    user = update.message.from_user
    logger.info(f'User {user.first_name} has canceled process')
    update.message.reply_text(
        'Действие работы бота прервано.\nДля возобновления работы введите /start'
    )
    return ConversationHandler.END


def main():
    updater = Updater("5675091266:AAHbP-X6DxIrQ5FqXwkn9Nt03ayzA74CP1Y")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INSTANCE: [
                CallbackQueryHandler(choose_type_of_legal_proceeding_1in, pattern="^" + 'first_instance' + "$"),
                CallbackQueryHandler(choose_type_of_legal_proceeding_app, pattern="^" + 'appeal' + "$"),
                CallbackQueryHandler(choose_type_of_legal_proceeding_cas_sup, pattern="^" + 'cassation' + "$"),
                CallbackQueryHandler(choose_type_of_legal_proceeding_cas_sup, pattern="^" + 'supervisory' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_for_newly_facts, pattern="^" + 'newly_facts' + "$"),
                CallbackQueryHandler(choose_type_of_ruling_on_administrative_case,
                                     pattern="^" + 'administrative_appeal' + "$"),
                CallbackQueryHandler(choose_type_of_another_procedural_action, pattern="^" + 'other' + "$")
            ],
            PROCEEDING: [
                CallbackQueryHandler(choose_type_of_nature_of_claim, pattern="^" + 'lawsuit_proceeding' + "$"),
                CallbackQueryHandler(define_amount_for_order_proceeding, pattern="^" + 'order_proceeding' + "$"),
                CallbackQueryHandler(choose_subject, pattern="^" + 'appeal_NNLA_proceeding' + "$"),
                CallbackQueryHandler(choose_court, pattern="^" + 'special_proceeding' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10, pattern="^" + 'bankrupt_proceeding' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10,
                                     pattern="^" + 'appeal_notarial_proceeding' + "$"),
                CallbackQueryHandler(choose_subject, pattern="^" + 'administrative_proceeding' + "$"),
                CallbackQueryHandler(choose_subject, pattern="^" + 'appeal_claim_proceeding' + "$"),
                CallbackQueryHandler(choose_subject, pattern="^" + 'appeal_bailiff_proceeding' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10,
                                     pattern="^" + 'acknowledge_proceeding' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10,
                                     pattern="^" + 'executive_doc_proceeding' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10,
                                     pattern="^" + 'securing_proceeding' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10,
                                     pattern="^" + 'appeal_arbitration_proceeding' + "$"),
            ],
            ADM_CASE: [
                CallbackQueryHandler(define_fine, pattern="^" + 'fine' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'other_penalty' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'non_penalty' + "$")
            ],
            OTHER: [
                CallbackQueryHandler(determine_size_of_state_duty_x05, pattern="^" + 'another_complaint' + "$"),
                CallbackQueryHandler(define_number_of_documents, pattern="^" + 'get_documents' + "$"),
            ],
            CLAIM: [
                CallbackQueryHandler(define_price_of_claim, pattern="^" + 'property_claim' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x25,
                                     pattern="^" + 'subsidiary_liability_claim' + "$"),
                CallbackQueryHandler(define_price_of_claim, pattern="^" + 'quality_of_goods_claim' + "$"),
                CallbackQueryHandler(choose_subject, pattern="^" + 'non-pecuniary_claim' + "$"),
                CallbackQueryHandler(choose_court, pattern="^" + 'contract_dispute_claim' + "$")
            ],
            SUBJECT: [
                CallbackQueryHandler(choose_court, pattern="^" + 'entity' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10, pattern="^" + 'individual_entrepreneur' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x5, pattern="^" + 'individual' + "$")
            ],
            COURT_1: [
                CallbackQueryHandler(determine_size_of_state_duty_x50, pattern="^" + 'supreme_court' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x20, pattern="^" + 'regional_court' + "$"),
            ],
            COURT_2: [
                CallbackQueryHandler(determine_size_of_state_duty_x15, pattern="^" + 'supreme_court' + "$"),
                CallbackQueryHandler(determine_size_of_state_duty_x10, pattern="^" + 'regional_court' + "$"),
            ],
            DUTY_PROPERTY: [
                MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_property_claim)],
            DUTY_ORDER: [MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_order_claim)],
            DUTY_ADM_CASE: [
                MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_administrative_case)],
            DUTY_DOCUMENTS: [
                MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_get_documents)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
