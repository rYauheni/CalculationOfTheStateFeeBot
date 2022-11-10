from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters)

from EconomicCourt_config import *

from CSDB_index import (EC_INSTANCE, EC_PROCEEDING, EC_OTHER, EC_CLAIM, EC_DUTY_PROPERTY, EC_DUTY_ORDER, EC_SUBJECT,
                        EC_COURT_1, EC_COURT_2, EC_ADM_CASE, EC_DUTY_ADM_CASE, EC_DUTY_DOCUMENTS)

ec_conv_handler_dict = {
    EC_INSTANCE: [
        CallbackQueryHandler(choose_type_of_legal_proceeding_1in, pattern="^" + 'first_instance' + "$"),
        CallbackQueryHandler(choose_type_of_legal_proceeding_app, pattern="^" + 'appeal' + "$"),
        CallbackQueryHandler(choose_type_of_legal_proceeding_cas_sup, pattern="^" + 'cassation' + "$"),
        CallbackQueryHandler(choose_type_of_legal_proceeding_cas_sup, pattern="^" + 'supervisory' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_for_newly_facts,
                             pattern="^" + 'newly_facts' + "$"),
        CallbackQueryHandler(choose_type_of_ruling_on_administrative_case,
                             pattern="^" + 'administrative_appeal' + "$"),
        CallbackQueryHandler(choose_type_of_another_procedural_action, pattern="^" + 'other' + "$")
    ],
    EC_PROCEEDING: [
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
    EC_ADM_CASE: [
        CallbackQueryHandler(define_fine, pattern="^" + 'fine' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'other_penalty' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'non_penalty' + "$")
    ],
    EC_OTHER: [
        CallbackQueryHandler(determine_size_of_state_duty_x05, pattern="^" + 'another_complaint' + "$"),
        CallbackQueryHandler(define_number_of_documents, pattern="^" + 'get_documents' + "$"),
    ],
    EC_CLAIM: [
        CallbackQueryHandler(define_price_of_claim, pattern="^" + 'property_claim' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x25,
                             pattern="^" + 'subsidiary_liability_claim' + "$"),
        CallbackQueryHandler(define_price_of_claim, pattern="^" + 'quality_of_goods_claim' + "$"),
        CallbackQueryHandler(choose_subject, pattern="^" + 'non-pecuniary_claim' + "$"),
        CallbackQueryHandler(choose_court, pattern="^" + 'contract_dispute_claim' + "$")
    ],
    EC_SUBJECT: [
        CallbackQueryHandler(choose_court, pattern="^" + 'entity' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x10,
                             pattern="^" + 'individual_entrepreneur' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x5, pattern="^" + 'individual' + "$")
    ],
    EC_COURT_1: [
        CallbackQueryHandler(determine_size_of_state_duty_x50, pattern="^" + 'supreme_court' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x20, pattern="^" + 'regional_court' + "$"),
    ],
    EC_COURT_2: [
        CallbackQueryHandler(determine_size_of_state_duty_x15, pattern="^" + 'supreme_court' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x10, pattern="^" + 'regional_court' + "$"),
    ],
    EC_DUTY_PROPERTY: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_property_claim)],
    EC_DUTY_ORDER: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_order_claim)],
    EC_DUTY_ADM_CASE: [
        MessageHandler(Filters.text & ~Filters.command,
                       determine_size_of_state_duty_for_administrative_case)],
    EC_DUTY_DOCUMENTS: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_get_documents)]
}
