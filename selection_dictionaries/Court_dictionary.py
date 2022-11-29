"""
This module contains the responses (text messages) that are returned to the user when they select a court type
when using the Bot.
The value of the response is determined based on the data of the table status log in the database
"""

dict_type_court = {
    'economic_court': 'Суд, рассматривающий экономические дела',
    'ordinary_court': 'Суд общей юрисдикции',
    'intellectual_property_court': 'Судебная коллегия по делам интеллектуальной собственности '
                                   'Верховного Суда Республики Беларусь',
    'international_arbitration_court': 'Международный арбитражный суд при Белорусской торгово-промышленной палате'
}
