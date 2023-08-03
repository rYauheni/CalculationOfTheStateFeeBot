"""
This module contains the responses (text messages) that are returned to the user when a certain option is selected
when using the Bot in the InternationalArbitrationCourt branch.
The value of the response is determined based on the data of the table status log in the database.
"""

dict_subject = {
    'resident': 'Спор между субъектами, местонахождение или местожительство каждого из которых находится '
                'в Республике Беларусь',
    'non-resident': 'Спор между субъектами, местонахождение или местожительство хотя бы одного из них находится '
                    'за границей Республики Беларусь'
}

dict_proceeding = {
    'ordinary': 'Обычная процедура рассмотрения споров',
    'simplified': 'Упрощённая процедура рассмотрения споров'
}

dict_instance = {
    'one': 'Разрешение спора единоличным арбитром',
    'collegial': 'Разрешение спора тремя арбитрами (коллегиальное)'
}

dict_claim = {
    'property_claim': 'Требование имущественного характера',
    'non-pecuniary_claim': 'Требование неимущественного характера (или иск не имеет цены)'
}

dict_limit_sp = {
    'limit_sp': 'Упрощенная процедура применяется для рассмотрения споров между субъектами Республики Беларусь, '
                'сумма требований по которым <b>не превышает 10 000 базовых величин</b>.\n'
                '(п. 2 статьи 62 Регламента МАС пр БелТПП)'
}
