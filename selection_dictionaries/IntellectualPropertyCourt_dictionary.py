"""
This module contains the responses (text messages) that are returned to the user when a certain option is selected
when using the Bot in the IntellectualPropertyCourt branch.
The value of the response is determined based on the data of the table status log in the database.
"""

dict_instance = {
    'first_instance': 'Производство в суде первой инстанции',
    'supervisory': 'Производство дел в порядке надзора',
    'newly_facts': 'Производство по пересмотру судебных постановлений вновь открывшимся обстоятельствам',
    'other': 'Иные процессуальные действия'
}

dict_proceeding = {
    'lawsuit_proceeding': 'Исковое производство',
    'appealing_decision_on_ipi': 'Рассмотрение жалобы на решение Апелляционного совета при государственном учреждении '
                                 '«Национальный центр интеллектуальной собственности», а также на решение иного органа '
                                 'по вопросам, связанным с объектами интеллектуальной собственности'
}

dict_other = {
    'another_complaint': 'Рассмотрение иной жалобы, не указанной в иных опциях',
    'get_copy_of_court_order': 'Повторная выдача копии судебного постановления судебной коллегии по делам '
                               'интеллектуальной собственности Верховного Суда Республики Беларусь'
}

dict_claim = {
    'property_claim': 'Требование имущественного характера',
    'non-pecuniary_claim': 'Требование неимущественного характера (или не подлежащее оценке)'
}

dict_subject = {
    'entity': 'Юридическое лицо или организация, не являющаяся юридическим лицом',
    'individual': 'Физическое лицо'
}
