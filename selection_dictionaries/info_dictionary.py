from settings.settings import ACTUALITY_CHECK_DATE, BASE_VALUE

dict_info = {
    'info': 'Данный бот позволяет рассчитывать государственную пошлину, подлежащую уплате при обращении в суды '
            'Республики Беларусь, а также арбитражный сбор для Международного арбитражного суда при БелТПП.\n'
            'Государственная пошлина определяется:\n'
            '- для всех судов (судебных юрисдикций);\n'
            '- для всех видов судебных процессов;\n'
            '- для всех судебных инстанций;\n'
            '- для всех видов судопроизводства;\n'
            '- по всем видам требований.\n\n'
            'Порядок исчисления государственной пошлины (арбитражного сбора) определяется на основании'
            'Налогового кодекса Республики Беларусь, Гражданского процессуального кодекса Республики Беларусь, '
            'Хозяйственного процессуального кодекса Республики Беларусь, '
            'Регламента Международного арбитражного суда при '
            'БелТПП, постановления Совета Министров Республики Беларусь об установлении размера базовой величины.\n\n'
            'Указанные нормативные правовые акты применяются по состоянию (в редакциях, с изменениями и дополнениями) '
            f'на <b>{ACTUALITY_CHECK_DATE}</b>.\n'
            f'Текущий размер базовой величины: <b>{BASE_VALUE} BYN</b>.\n\n'
            'Расчет государственной пошлины (арбитражного сбора) является ориентировочным.\n'
            'Расчет, произведенный данным ботом, <b>НЕ МОЖЕТ</b> быть использован в качестве доказательства в суде,'
            ' <b>НЕ ИМЕЕТ</b> юридической силы.\n\n'
            'Чтобы продолжить работу с ботом, нажмите /start'
}
