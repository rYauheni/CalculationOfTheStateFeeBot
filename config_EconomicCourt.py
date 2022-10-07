import telebot
from telebot import types

token = '5675091266:AAHbP-X6DxIrQ5FqXwkn9Nt03ayzA74CP1Y'
bot = telebot.TeleBot(token, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Настоящий <i><b>бот</b></i> представляет собой калькулятор государственной '
                                      'пошлины при обращениии в суды.\n\n'
                                      'Расчёт государственной пошлины является примерным.\n\n'
                                      'Сведения, полученные в результате работы настоящего бота, '
                                      'не могут быть использованы в качестве доказательства в суде.')


@bot.message_handler(commands=['instance'])
def choose_instance(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Производство в суде первой инстанции', callback_data='first_instance')
    item2 = types.InlineKeyboardButton('Производство в суде апелляционной инстанции', callback_data='appeal')
    item3 = types.InlineKeyboardButton('Производство в суде кассационной инстанции', callback_data='cassation')
    item4 = types.InlineKeyboardButton('Производство по пересмотру судебных постановлений в порядке надзора',
                                       callback_data='supervisory')
    item5 = types.InlineKeyboardButton('Производство по вновь открывшимся обстоятельствам', callback_data='newly_facts')
    item6 = types.InlineKeyboardButton('Иные процессуальные действия', callback_data='other')
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, 'Выберите судебную инстанцию', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def choose_instance_callback(call):
    if call.data == 'first_instance':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Первая инстанция')  # удаляется предыдущее сообщение, чтобы было красиво
#         bot.register_next_step_handler(call, choose_type_of_legal_proceeding_first_instance)
#
#
# # @bot.message_handler(commands=['proceeding'])
# def choose_type_of_legal_proceeding_first_instance(message):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     item1 = types.InlineKeyboardButton('Исковое производство', callback_data='isk')
#     item2 = types.InlineKeyboardButton('Приказное производство', callback_data='prikaz')
#     markup.add(item1, item2)
#     bot.send_message(message.chat.id, 'Выберите вид судопроизводства', reply_markup=markup)


bot.infinity_polling()
