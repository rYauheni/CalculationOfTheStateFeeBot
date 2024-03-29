import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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

from calc_n_convert_func.EconomicCourt_calculating_func import (
    calculate_coefficient,
    calculating_state_duty_for_property,
    calculating_state_duty_for_order,
    calculating_state_duty_for_administrative_case,
    calculating_state_duty_for_get_documents
)

from calc_n_convert_func.rounding_func import round_dec

from calc_n_convert_func.exceptions import FormatError, SizeError

from calc_n_convert_func.Court_converting_func import (
    converting_user_amount,
    converting_user_fine,
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

from CSDB_index import (EC_INSTANCE, EC_PROCEEDING, EC_OTHER, EC_CLAIM, EC_DUTY_PROPERTY, EC_DUTY_ORDER, EC_SUBJECT,
                        EC_COURT_1, EC_COURT_2, EC_ADM_CASE, EC_DUTY_ADM_CASE, EC_DUTY_DOCUMENTS)

from settings.settings import BASE_VALUE

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def choose_instance_ec(update: Update, _) -> int:
    """ type_court -> instance """
    keyboard = [
        [InlineKeyboardButton('Первая инстанция (ХП)', callback_data='first_instance')],
        [InlineKeyboardButton('Апелляционная инстанция (ХП)', callback_data='appeal')],
        [InlineKeyboardButton('Кассационная инстанция (ХП)', callback_data='cassation')],
        [InlineKeyboardButton('Производство в порядке надзора (ХП)',
                              callback_data='supervisory')],
        [InlineKeyboardButton('Производство по вновь открывшимся обстоятельствам (ХП)', callback_data='newly_facts')],
        [InlineKeyboardButton('Обжалование постановления по делу об административном правонарушении',
                              callback_data='administrative_appeal')],
        [InlineKeyboardButton('Иные процессуальные действия', callback_data='other')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите судебную инстанцию для хозяйственного процесса (ХП) или '
                                             'иной вид процесса (процессуальное действие):',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    type_court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'type_court', type_court)
    logger.info(f"User {user_id} has chosen the type of the court - {get_column_value(user_id, 'type_court')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_type_court[get_column_value(user_id, 'type_court')]}")
    return EC_INSTANCE


def choose_type_of_legal_proceeding_1in(update: Update, _) -> int:
    """ type_court -> instance (first) -> legal_proceeding """
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        [InlineKeyboardButton('Приказное производство', callback_data='order_proceeding')],
        [InlineKeyboardButton('По проверке законности ННПА, действий (бездействия) '
                              'государственных органов', callback_data='appeal_NNLA_proceeding')],
        [InlineKeyboardButton('Об установлении юридических фактов', callback_data='special_proceeding')],
        [InlineKeyboardButton('Об экономической несостоятельности (банкротстве)',
                              callback_data='bankrupt_proceeding')],
        [InlineKeyboardButton('По жалобам на нотариальные действия',
                              callback_data='appeal_notarial_proceeding')],
        [InlineKeyboardButton('По делам из административных и иных публичных правоотношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('По жалобам на ответы на обращения юридических лиц (ИП, граждан)',
                              callback_data='appeal_claim_proceeding')],
        [InlineKeyboardButton('По обжалованию действий (бездействия) судебного исполнителя',
                              callback_data='appeal_bailiff_proceeding')],
        [InlineKeyboardButton('По признанию и исполнению решений иностранных содов',
                              callback_data='acknowledge_proceeding')],
        [InlineKeyboardButton('По выдаче исполнительного документа на исполнение решения третейского суда,'
                              ' медиативного соглашения', callback_data='executive_doc_proceeding')],
        [InlineKeyboardButton('По обеспечению иска, рассматриваемого третейским судом, '
                              'медиативного соглашения', callback_data='securing_proceeding')],
        [InlineKeyboardButton('По отмене решений третейских, арбитражных судов',
                              callback_data='appeal_arbitration_proceeding')]
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
    return EC_PROCEEDING


def choose_type_of_legal_proceeding_app(update: Update, _) -> int:
    """ type_court -> instance (appeal) -> legal_proceeding """
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        # del order
        [InlineKeyboardButton('По проверке законности ННПА, действий (бездействия) '
                              'государственных органов', callback_data='appeal_NNLA_proceeding')],
        [InlineKeyboardButton('Об установлении юридических фактов', callback_data='special_proceeding')],
        # del bankrupt
        [InlineKeyboardButton('По жалобам на нотариальные действия',
                              callback_data='appeal_notarial_proceeding')],
        [InlineKeyboardButton('По делам из административных и иных публичных правоотношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('По жалобам на ответы на обращения юридических лиц (ИП, граждан)',
                              callback_data='appeal_claim_proceeding')],
        [InlineKeyboardButton('По обжалованию действий (бездействия) судебного исполнителя',
                              callback_data='appeal_bailiff_proceeding')],
        # del acknowledge
        [InlineKeyboardButton('По выдаче исполнительного документа на исполнение решения третейского суда,'
                              ' медиативного соглашения', callback_data='executive_doc_proceeding')],
        [InlineKeyboardButton('По обеспечению иска, рассматриваемого третейским судом, '
                              'медиативного соглашения', callback_data='securing_proceeding')],
        [InlineKeyboardButton('По отмене решений третейских, арбитражных судов',
                              callback_data='appeal_arbitration_proceeding')]
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
    return EC_PROCEEDING


def choose_type_of_legal_proceeding_cas_sup(update: Update, _) -> int:
    """ type_court -> instance (cassation, supervisory) -> legal_proceeding """
    keyboard = [
        [InlineKeyboardButton('Исковое производство', callback_data='lawsuit_proceeding')],
        # del order
        [InlineKeyboardButton('По проверке законности ННПА, действий (бездействия) '
                              'государственных органов', callback_data='appeal_NNLA_proceeding')],
        [InlineKeyboardButton('Об установлении юридических фактов', callback_data='special_proceeding')],
        # del bankrupt
        [InlineKeyboardButton('По жалобам на нотариальные действия',
                              callback_data='appeal_notarial_proceeding')],
        [InlineKeyboardButton('По делам из административных и иных публичных правоотношений',
                              callback_data='administrative_proceeding')],
        [InlineKeyboardButton('По жалобам на ответы на обращения юридических лиц (ИП, граждан)',
                              callback_data='appeal_claim_proceeding')],
        [InlineKeyboardButton('По обжалованию действий (бездействия) судебного исполнителя',
                              callback_data='appeal_bailiff_proceeding')],
        [InlineKeyboardButton('По признанию и исполнению решений иностранных содов',
                              callback_data='acknowledge_proceeding')],
        [InlineKeyboardButton('По выдаче исполнительного документа на исполнение решения третейского суда,'
                              ' медиативного соглашения', callback_data='executive_doc_proceeding')],
        [InlineKeyboardButton('По обеспечению иска, рассматриваемого третейским судом, '
                              'медиативного соглашения', callback_data='securing_proceeding')],
        [InlineKeyboardButton('По отмене решений третейских, арбитражных судов',
                              callback_data='appeal_arbitration_proceeding')]
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
    return EC_PROCEEDING


def choose_type_of_ruling_on_administrative_case(update: Update, _) -> int:
    """ type_court -> instance (administrative) -> ruling_on_ac """
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
    logger.info(f"User {user_id} has chosen instance - {get_column_value(user_id, 'instance')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return EC_ADM_CASE


def choose_type_of_another_procedural_action(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action """
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
    logger.info(f"User {user_id} has chosen instance - {get_column_value(user_id, 'instance')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_instance[get_column_value(user_id, 'instance')]}")
    return EC_OTHER


def choose_type_of_nature_of_claim(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) -> legal_proceeding (lawsuit) -> claim """
    keyboard = [
        [InlineKeyboardButton('Требование имущественного характера', callback_data='property_claim')],
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
    logger.info(f"User {user_id} has chosen legal proceeding - {get_column_value(user_id, 'proceeding')}")
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return EC_CLAIM


def choose_subject(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) ->
                    [legal_proceeding (lawsuit) -> claim (non-pecuniary_claim)] or
                     [legal_proceeding (appeal_NNLA_proceeding, administrative_proceeding, appeal_claim_proceeding,
                        appeal_bailiff_proceeding)] ->
            subject """
    keyboard = [
        [InlineKeyboardButton('Юридическое лицо', callback_data='entity')],
        [InlineKeyboardButton('Индивидуальный предприниматель',
                              callback_data='individual_entrepreneur')],
        [InlineKeyboardButton('Физическое лицо', callback_data='individual')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите юридический статус лица, подающего(-вавшего) исковое заявление '
                                             '(заявление, жалобу) для рассмотрения по существу '
                                             '(в суд первой инстанции):', reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)

    if get_column_value(user_id, 'proceeding'):
        claim = update.callback_query.data
        add_column_value(user_id, 'claim', claim)
        logger.info(f"User {user_id} has chosen nature of claim - {get_column_value(user_id, 'claim')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_claim[get_column_value(user_id, 'claim')]}")
    else:
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen legal proceeding - {get_column_value(user_id, 'proceeding')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    return EC_SUBJECT


def choose_court(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) ->
                        [[legal_proceeding (lawsuit) -> claim (non-pecuniary_claim)] or
                            [legal_proceeding (appeal_NNLA_proceeding, administrative_proceeding,
                            appeal_claim_proceeding, appeal_bailiff_proceeding)] ->  subject] or
                        [legal_proceeding (lawsuit) -> claim (contract_dispute)] or
                        [legal_proceeding (special)] ->
            court
                        """
    keyboard = [
        [InlineKeyboardButton('Верховный Суд Республики Беларусь', callback_data='supreme_court')],
        [InlineKeyboardButton('Экономические суды областей (города Минска)',
                              callback_data='regional_court')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.callback_query.message.reply_text('Выберите суд, в который подаётся(-валось) исковое заявление '
                                             '(заявление, жалоба) для рассмотрения по существу (суд первой инстанции):',
                                             reply_markup=reply_markup)
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)

    if get_column_value(user_id, 'claim'):
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {user_id} has chosen subject - {get_column_value(user_id, 'subject')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
        return EC_COURT_1
    elif get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') != 'lawsuit_proceeding':
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {user_id} has chosen subject - {get_column_value(user_id, 'subject')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
        return EC_COURT_1
    elif get_column_value(user_id, 'proceeding'):
        claim = update.callback_query.data
        add_column_value(user_id, 'claim', claim)
        logger.info(f"User {user_id} has chosen nature of claim - {get_column_value(user_id, 'claim')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_claim[get_column_value(user_id, 'claim')]}")
        return EC_COURT_1
    else:
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen proceeding - {get_column_value(user_id, 'proceeding')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
        return EC_COURT_2


def define_price_of_claim(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) -> legal_proceeding (lawsuit) ->
            claim (property, quality_of_goods) -> price_of_claim """
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen nature of claim - {get_column_value(user_id, 'claim')}")

    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    update.callback_query.message.reply_text('Укажите цену иска (оспариваемую сумму) в белорусских рублях (BYN):')
    return EC_DUTY_PROPERTY


def define_amount_for_order_proceeding(update: Update, _) -> int:
    """ type_court -> instance (first) -> legal_proceeding (order) -> amount_for_order """
    user_id = update.callback_query.from_user.id
    proceeding = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'proceeding', proceeding)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    logger.info(f"User {user_id} has chosen legal proceeding - {get_column_value(user_id, 'proceeding')}")
    update.callback_query.message.reply_text('Укажите сумму взыскания в белорусских рублях (BYN):')
    return EC_DUTY_ORDER


def define_fine(update: Update, _) -> int:
    """ type_court -> instance (administrative) -> ruling_on_ac (fine) -> fine """
    user_id = update.callback_query.from_user.id
    ruling_on_adm = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'ruling_on_adm', ruling_on_adm)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    logger.info(f"User {user_id} has chosen type of a ruling on an administrative case - "
                f"{get_column_value(user_id, 'ruling_on_adm')}")
    update.callback_query.message.reply_text(f'Укажите размер штрафа в белорусских рублях (BYN).\n\n\n'
                                             '<i>В случае, если на день расчёта государственной пошлины установлен иной'
                                             f' размер базовой величины ({BASE_VALUE} BYN), по сравнению с тем, который'
                                             f' существовал на день'
                                             ' наложения административного взыскания в виде штрафа, дополнительно '
                                             'укажите размер базовой величины, существовавшей на день наложения '
                                             'взыскания в формате:\n\n <b>штраф=базовая_величина (например, 290=29)'
                                             '</b></i>\n\n'
                                             'Если размер базовой величины не изменялся,'
                                             'достаточно указать только размер штрафа:', parse_mode='HTML')
    return EC_DUTY_ADM_CASE


def define_number_of_documents(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action (get_documents) -> number_of_documents """
    user_id = update.callback_query.from_user.id
    another_action = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'another_action', another_action)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_other[get_column_value(user_id, 'another_action')]}")
    logger.info(f"User {user_id} has chosen another procedural action - {get_column_value(user_id, 'another_action')}")
    update.callback_query.message.reply_text('Укажите количество страниц документа(ов), подлежащих изготовлению:')
    return EC_DUTY_DOCUMENTS


def determine_size_of_state_duty_for_property_claim(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) -> legal_proceeding (lawsuit) ->
                claim (property, quality_of_goods) -> price_of_claim  -> state_duty_property """
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


def determine_size_of_state_duty_for_order_claim(update: Update, _) -> float:
    """ type_court -> instance (first) -> legal_proceeding (order) -> amount_for_order -> state_duty_order """
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified amount of recovery - {update.message.text}")
    try:
        convert_amount_of_recovery = converting_user_amount(str(update.message.text))
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
        state_duty = calculating_state_duty_for_order(convert_amount_of_recovery, BASE_VALUE)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_for_administrative_case(update: Update, _) -> int:
    """ type_court -> instance (administrative) -> ruling_on_ac (fine) -> fine -> state_duty_ac"""
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} has specified the size of fine - {update.message.text}")
    convert_b_v = BASE_VALUE
    str_to_list_fine = converting_user_fine(str(update.message.text))
    if len(str_to_list_fine) == 2:
        try:
            convert_fine = converting_user_amount(str_to_list_fine[0])
            convert_b_v = converting_user_amount(str_to_list_fine[1])
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
            state_duty = calculating_state_duty_for_administrative_case(convert_fine, convert_b_v, BASE_VALUE)
            update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                      parse_mode='HTML')
            return ConversationHandler.END
    elif len(str_to_list_fine) == 1:
        try:
            convert_fine = converting_user_amount(str_to_list_fine[0])
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
            state_duty = calculating_state_duty_for_administrative_case(convert_fine, convert_b_v, BASE_VALUE)
            update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                      parse_mode='HTML')
            return ConversationHandler.END
    else:
        update.message.reply_text(raise_incorrect_value()[0])
        update.message.reply_text(raise_incorrect_value()[1])


def determine_size_of_state_duty_for_get_documents(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action (get_documents) -> number_of_documents -> state_duty_doc """
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
        state_duty = calculating_state_duty_for_get_documents(convert_pages, BASE_VALUE)
        update.message.reply_text(f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN',
                                  parse_mode='HTML')
        return ConversationHandler.END


def determine_size_of_state_duty_x05(update: Update, _) -> int:
    """ type_court -> instance (other) -> another_action (another_complaint) -> state_duty_05 """
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


def determine_size_of_state_duty_x1(update: Update, _) -> int:
    """ type_court -> instance (administrative) -> ruling_on_ac (other_penalty, non_penalty) -> state_duty_1 """
    user_id = update.callback_query.from_user.id
    ruling_on_adm = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'ruling_on_adm', ruling_on_adm)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_adm_case[get_column_value(user_id, 'ruling_on_adm')]}")
    logger.info(f"User {user_id} has chosen type of a ruling on an administrative case - "
                f"{get_column_value(user_id, 'ruling_on_adm')}")
    state_duty = round_dec(BASE_VALUE * 1)
    update.callback_query.message.reply_text(f'Размер государственной пошлины составляет:\n\n'
                                             f'<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x5(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) ->
                            [legal_proceeding (lawsuit) -> claim (non-pecuniary_claim)] or
                                [legal_proceeding (appeal_NNLA_proceeding, administrative_proceeding,
                                appeal_claim_proceeding, appeal_bailiff_proceeding) ->  subject (individual) ->
                state_duty_5 """
    user_id = update.callback_query.from_user.id
    subject = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'subject', subject)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_subject[get_column_value(user_id, 'subject')]}")
    logger.info(f"User {user_id} has chosen subject - {get_column_value(user_id, 'subject')}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 5) * coefficient['instance'])
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x10(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) ->
                              [[legal_proceeding (lawsuit) -> claim (non-pecuniary_claim)] or
                                  [legal_proceeding (appeal_NNLA_proceeding, administrative_proceeding,
                                  appeal_claim_proceeding, appeal_bailiff_proceeding) ->
                                                                                subject (individual_entrepreneur)]] or
                              [legal_proceeding (special) -> court (regional)] or
                              [legal_proceeding(appeal_notarial, appeal_arbitration, executive_doc, securing,
                                                                                                    acknowledge)] ->
                  state_duty_10 """
    user_id = update.callback_query.from_user.id
    counter = get_new_counter_value(user_id)
    if get_column_value(user_id, 'claim'):
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {user_id} has chosen subject - {get_column_value(user_id, 'subject')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
    elif get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') in {
        'appeal_NNLA_proceeding', 'administrative_proceeding', 'appeal_claim_proceeding', 'appeal_bailiff_proceeding'
    }:
        subject = update.callback_query.data
        add_column_value(user_id, 'subject', subject)
        logger.info(f"User {user_id} has chosen subject - {get_column_value(user_id, 'subject')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_subject[get_column_value(user_id, 'subject')]}")
    elif get_column_value(user_id, 'proceeding') and get_column_value(user_id, 'proceeding') == 'special_proceeding':
        court = update.callback_query.data
        add_column_value(user_id, 'court', court)
        logger.info(f"User {user_id} has chosen a court - {get_column_value(user_id, 'court')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_court[get_column_value(user_id, 'court')]}")
    else:
        proceeding = update.callback_query.data
        add_column_value(user_id, 'proceeding', proceeding)
        logger.info(f"User {user_id} has chosen legal proceeding - {get_column_value(user_id, 'proceeding')}")
        update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                     f"{dict_proceeding[get_column_value(user_id, 'proceeding')]}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 10) * coefficient['instance'])
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x15(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) -> [legal_proceeding (special) ->
                court (supreme)] -> state_duty_15 """
    user_id = update.callback_query.from_user.id
    court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'court', court)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_court[get_column_value(user_id, 'court')]}")
    logger.info(f"User {user_id} has chosen a court - {get_column_value(user_id, 'court')}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 15) * coefficient['instance'])
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x20(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) ->
                                [[legal_proceeding (lawsuit) -> claim (non-pecuniary_claim)] or
                                 [legal_proceeding (appeal_NNLA_proceeding, administrative_proceeding,
                                  appeal_claim_proceeding, appeal_bailiff_proceeding) ->
                                                                             subject (individual_entrepreneur)]] - >
                                            subject (entity) or
                                [legal_proceeding (lawsuit) -> claim (contract_dispute)] ->
             court (regional) -> state_duty_20 """
    user_id = update.callback_query.from_user.id
    court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'court', court)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_court[get_column_value(user_id, 'court')]}")
    logger.info(f"User {user_id} has chosen a court - {get_column_value(user_id, 'court')}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 20) * coefficient['instance'])
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x25(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) -> legal_proceeding (lawsuit) ->
            claim (subsidiary_liability) -> state_duty_25 """
    user_id = update.callback_query.from_user.id
    claim = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'claim', claim)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_claim[get_column_value(user_id, 'claim')]}")
    logger.info(f"User {user_id} has chosen nature of claim - {get_column_value(user_id, 'claim')}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 25) * coefficient['instance'])
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_x50(update: Update, _) -> int:
    """ type_court -> instance (first, appeal, cassation, supervisory) ->
                                    [[legal_proceeding (lawsuit) -> claim (non-pecuniary_claim)] or
                                     [legal_proceeding (appeal_NNLA_proceeding, administrative_proceeding,
                                      appeal_claim_proceeding, appeal_bailiff_proceeding) ->
                                                                                subject (individual_entrepreneur)]] ->
                                                subject (entity) or
                                    [legal_proceeding (lawsuit) -> claim (contract_dispute)] ->
                 court (supreme) -> state_duty_20 """
    user_id = update.callback_query.from_user.id
    court = update.callback_query.data
    counter = get_new_counter_value(user_id)
    add_column_value(user_id, 'court', court)
    update.callback_query.edit_message_text(text=f"{counter}. Вы выбрали:\n"
                                                 f"{dict_court[get_column_value(user_id, 'court')]}")
    logger.info(f"User {user_id} has chosen a court - {get_column_value(user_id, 'court')}")
    coefficient = calculate_coefficient(user_id)
    logger.info(f"Coefficient check. Current value of coefficient is: {coefficient}")
    state_duty = round_dec(round_dec(BASE_VALUE * 50) * coefficient['instance'])
    update.callback_query.message.reply_text(
        f'Размер государственной пошлины составляет:\n\n<b>{state_duty}</b> BYN', parse_mode='HTML')
    return ConversationHandler.END


def determine_size_of_state_duty_for_newly_facts(update: Update, _) -> int:
    """ type_court -> instance (newly_facts) -> state_duty_nf """
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
