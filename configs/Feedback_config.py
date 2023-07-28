import logging

from telegram import Update
from telegram.ext import ConversationHandler

from status_log_db.bot_status_log_db import add_column_value


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def save_feedback(update: Update, _) -> int:

    user_id = update.message.from_user.id
    feedback = update.message.text
    logger.info(f"User {user_id} has left the feedback - {feedback}")
    add_column_value(user_id, 'feedback', feedback, 'feedback')
    update.message.reply_text(f'Команда разработчиков благодарит за оставленный отзыв.\n\n'
                              f'Чтобы продолжить работу с ботом, нажмите /start')
    return ConversationHandler.END
