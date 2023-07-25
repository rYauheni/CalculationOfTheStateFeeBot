from telegram.ext import (MessageHandler, Filters)

from configs.Feedback_config import *

from CSDB_index import FEEDBACK

feedback_conv_handler_dict = {
    FEEDBACK: [MessageHandler(Filters.text & ~Filters.command, save_feedback)]
}
