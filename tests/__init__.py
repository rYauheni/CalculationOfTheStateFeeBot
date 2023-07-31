"""
When unittest has run, records are created in the database, the data from which is necessary for test functions.
"""

from orm.orm_functions import (create_table, add_new_row, add_column_value)

table_content = ('user_id', 'user_name', 'type_court', 'instance', 'proceeding', 'criminal', 'claim', 'criminal_order',
                 'subject', 'court', 'ruling_on_adm', 'another_action', 'counter')


def add_values(user_id, values):
    for i in range(len(values)):
        add_column_value(user_id, table_content[i], values[i])


def add_test_users():
    # ECONOMIC COURT
    add_new_row(101)  # EC: first instance + property_claim
    values_101 = (101, 'test_user_101', 'economic_court', 'first_instance', 'lawsuit_proceeding', 'NULL',
                  'property_claim', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 4)
    add_values(101, values_101)

    add_new_row(102)  # EC: first instance + quality of goods claim
    values_102 = (102, 'test_user_102', 'economic_court', 'first_instance', 'lawsuit_proceeding', 'NULL',
                  'quality_of_goods_claim', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 4)
    add_values(102, values_102)

    add_new_row(103)  # EC: appeal instance + property claim
    values_103 = (103, 'test_user_103', 'economic_court', 'appeal', 'lawsuit_proceeding', 'NULL',
                  'property_claim', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 4)
    add_values(103, values_103)

    add_new_row(104)  # EC: cassation instance + quality of goods claim
    values_104 = (104, 'test_user_104', 'economic_court', 'cassation', 'lawsuit_proceeding', 'NULL',
                  'quality_of_goods_claim', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 4)
    add_values(104, values_104)


def main():
    create_table('status_log')
    add_test_users()


main()
