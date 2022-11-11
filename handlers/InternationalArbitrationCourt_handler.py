from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters)

from configs.InternationalArbitrationCourt_config import *

from CSDB_index import (IAC_SUBJECT, IAC_PROCEEDING, IAC_INSTANCE, IAC_CLAIM, IAC_A_FEE_PROPERTY)

iac_conv_handler_dict = {
    IAC_SUBJECT: [
        CallbackQueryHandler(choose_type_of_legal_proceeding, pattern="^" + 'resident' + "$"),
        CallbackQueryHandler(choose_instance, pattern="^" + 'non-resident' + "$")
    ],
    IAC_PROCEEDING: [
        CallbackQueryHandler(choose_instance, pattern="^" + 'ordinary' + "$"),
        CallbackQueryHandler(choose_type_of_nature_of_claim, pattern="^" + 'simplified' + "$")
    ],
    IAC_INSTANCE: [
        CallbackQueryHandler(choose_type_of_nature_of_claim, pattern="^" + 'one' + "$"),
        CallbackQueryHandler(choose_type_of_nature_of_claim, pattern="^" + 'collegial' + "$")
    ],
    IAC_CLAIM: [
        CallbackQueryHandler(define_amount, pattern="^" + 'property_claim' + "$"),
        CallbackQueryHandler(determine_size_of_arbitration_fee_for_non_pecuniary_claim,
                             pattern="^" + 'non-pecuniary_claim' + "$")
    ],
    IAC_A_FEE_PROPERTY: [
        MessageHandler(Filters.text & ~Filters.command, determine_size_of_arbitration_fee_for_property_claim)
    ]
}
