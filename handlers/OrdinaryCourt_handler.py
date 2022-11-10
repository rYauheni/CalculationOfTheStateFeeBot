from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters)

from OrdinaryCourt_config import *

from CSDB_index import (OC_INSTANCE, OC_PROCEEDING, OC_ADM_CASE, OC_CRIMINAL, OC_OTHER, OC_CLAIM, OC_TYPE_CRIMINAL_SUP,
                        OC_DUTY_PROPERTY_ORDER, OC_DUTY_ADM_CASE, OC_DUTY_COURT_ORDER, OC_DUTY_O_DOCUMENTS)

oc_conv_handler_dict = {
    OC_INSTANCE: [
        CallbackQueryHandler(choose_type_of_legal_proceeding_1in, pattern="^" + 'first_instance' + "$"),
        CallbackQueryHandler(choose_type_of_legal_proceeding_app_sup, pattern="^" + 'appeal' + "$"),
        CallbackQueryHandler(choose_type_of_legal_proceeding_app_sup, pattern="^" + 'supervisory' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_for_newly_facts,
                             pattern="^" + 'newly_facts' + "$"),
        CallbackQueryHandler(choose_type_of_criminal_complaint, pattern="^" + 'criminal' + "$"),
        CallbackQueryHandler(choose_type_of_ruling_on_administrative_case,
                             pattern="^" + 'administrative_appeal' + "$"),
        CallbackQueryHandler(choose_type_of_another_procedural_action, pattern="^" + 'other' + "$")
    ],
    OC_PROCEEDING: [
        CallbackQueryHandler(choose_type_of_nature_of_claim, pattern="^" + 'lawsuit_proceeding' + "$"),
        CallbackQueryHandler(choose_type_of_nature_of_claim_for_order, pattern="^" + 'order_proceeding' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'administrative_proceeding' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x2, pattern="^" + 'special_proceeding' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x2,
                             pattern="^" + 'appeal_arbitration_proceeding' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x2,
                             pattern="^" + 'executive_doc_proceeding' + "$")
    ],
    OC_ADM_CASE: [
        CallbackQueryHandler(define_fine, pattern="^" + 'fine' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'other_penalty' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'non_penalty' + "$")
    ],
    OC_CRIMINAL: [
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'appeal_non_court_order' + "$"),
        CallbackQueryHandler(choose_type_of_appeal_court_criminal_order, pattern="^" + 'appeal_court_order' + "$"),
        CallbackQueryHandler(choose_type_of_nature_of_claim_for_civil_in_criminal,
                             pattern="^" + 'in_part_of_civil_lawsuit' + "$")
    ],
    OC_OTHER: [
        CallbackQueryHandler(determine_size_of_state_duty_x01, pattern="^" + 'another_complaint' + "$"),
        CallbackQueryHandler(define_number_of_pages_court_order, pattern="^" + 'get_copy_of_court_order' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x2, pattern="^" + 'get_first_divorce_order' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x3, pattern="^" + 'get_repeat_divorce_order' + "$"),
        CallbackQueryHandler(define_number_of_other_documents, pattern="^" + 'get_documents' + "$")
    ],
    OC_CLAIM: [
        CallbackQueryHandler(define_amount, pattern="^" + 'property_claim' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'expenses_for_children' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x4, pattern="^" + 'first_divorce' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x8, pattern="^" + 'repeat_divorce' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'special_divorce' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x5, pattern="^" + 'contract_dispute_claim' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x3, pattern="^" + 'non-pecuniary_claim' + "$")
    ],
    OC_TYPE_CRIMINAL_SUP: [
        CallbackQueryHandler(determine_size_of_state_duty_x2, pattern="^" + 'repeat_supreme_sup_criminal' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x1, pattern="^" + 'other_sup_criminal' + "$")
    ],
    OC_DUTY_PROPERTY_ORDER: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_property_and_order_claim)
    ],
    OC_DUTY_ADM_CASE: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_administrative_case)
    ],
    OC_DUTY_COURT_ORDER: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_get_copy_of_court_order)
    ],
    OC_DUTY_O_DOCUMENTS: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_get_documents)
    ]
}
