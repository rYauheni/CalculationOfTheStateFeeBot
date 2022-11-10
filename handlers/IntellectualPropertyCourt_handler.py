from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters)

from IntellectualPropertyCourt_config import *

from CSDB_index import (IPC_INSTANCE, IPC_PROCEEDING, IPC_OTHER, IPC_CLAIM, IPC_SUBJECT_1, IPC_SUBJECT_2,
                        IPC_DUTY_PROPERTY, IPC_DUTY_COURT_ORDER)

ipc_conv_handler_dict = {
    IPC_INSTANCE: [
        CallbackQueryHandler(choose_type_of_legal_proceeding, pattern="^" + 'first_instance' + "$"),
        CallbackQueryHandler(choose_type_of_legal_proceeding, pattern="^" + 'supervisory' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_for_newly_facts,
                             pattern="^" + 'newly_facts' + "$"),
        CallbackQueryHandler(choose_type_of_another_procedural_action, pattern="^" + 'other' + "$")
    ],
    IPC_PROCEEDING: [
        CallbackQueryHandler(choose_type_of_nature_of_claim, pattern="^" + 'lawsuit_proceeding' + "$"),
        CallbackQueryHandler(choose_subject, pattern="^" + 'appealing_decision_on_ipi' + "$")
    ],
    IPC_OTHER: [
        CallbackQueryHandler(determine_size_of_state_duty_x05, pattern="^" + 'another_complaint' + "$"),
        CallbackQueryHandler(choose_subject, pattern="^" + 'get_copy_of_court_order' + "$")
    ],
    IPC_CLAIM: [
        CallbackQueryHandler(define_amount, pattern="^" + 'property_claim' + "$"),
        CallbackQueryHandler(choose_subject, pattern="^" + 'non-pecuniary_claim' + "$")
    ],
    IPC_SUBJECT_1: [
        CallbackQueryHandler(determine_size_of_state_duty_x50, pattern="^" + 'entity' + "$"),
        CallbackQueryHandler(determine_size_of_state_duty_x20, pattern="^" + 'individual' + "$")
    ],
    IPC_SUBJECT_2: [
        CallbackQueryHandler(define_number_of_pages_court_order, pattern="^" + 'entity' + "$"),
        CallbackQueryHandler(define_number_of_pages_court_order, pattern="^" + 'individual' + "$")
    ],
    IPC_DUTY_PROPERTY: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_property_claim)
    ],
    IPC_DUTY_COURT_ORDER: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_state_duty_for_get_copy_of_court_order)
    ]
}
