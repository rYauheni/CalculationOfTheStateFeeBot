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
    values_101 = (101, 'test_user_101', 'economic_court', 'first_instance', 'lawsuit_proceeding', None,
                  'property_claim', None, None, None, None, None, 4)
    add_values(101, values_101)

    add_new_row(102)  # EC: first instance + quality of goods claim
    values_102 = (102, 'test_user_102', 'economic_court', 'first_instance', 'lawsuit_proceeding', None,
                  'quality_of_goods_claim', None, None, None, None, None, 4)
    add_values(102, values_102)

    add_new_row(103)  # EC: appeal instance + property claim
    values_103 = (103, 'test_user_103', 'economic_court', 'appeal', 'lawsuit_proceeding', None,
                  'property_claim', None, None, None, None, None, 4)
    add_values(103, values_103)

    add_new_row(104)  # EC: cassation instance + quality of goods claim
    values_104 = (104, 'test_user_104', 'economic_court', 'cassation', 'lawsuit_proceeding', None,
                  'quality_of_goods_claim', None, None, None, None, None, 4)
    add_values(104, values_104)

    # ORDINARY COURT
    add_new_row(201)  # OC: first instance
    values_201 = (201, 'test_user_201', 'ordinary_court', 'first_instance', 'lawsuit_proceeding', None,
                  'property_claim', None, None, None, None, None, 4)
    add_values(201, values_201)

    add_new_row(202)  # OC: appeal instance
    values_202 = (202, 'test_user_202', 'ordinary_court', 'appeal', 'lawsuit_proceeding', None,
                  'property_claim', None, None, None, None, None, 4)
    add_values(202, values_202)

    add_new_row(203)  # OC: criminal + in part of civil lawsuit
    values_203 = (203, 'test_user_203', 'ordinary_court', 'criminal', None, 'in_part_of_civil_lawsuit',
                  'property_claim', None, None, None, None, None, 4)
    add_values(203, values_203)

    # INTELLECTUAL PROPERTY COURT
    add_new_row(301)  # IPC: first instance
    values_301 = (301, 'test_user_301', 'intellectual_property_court', 'first_instance', 'lawsuit_proceeding', None,
                  'property_claim', None, None, None, None, None, 4)
    add_values(301, values_301)

    add_new_row(302)  # IPC: supervisory instance
    values_302 = (302, 'test_user_302', 'intellectual_property_court', 'supervisory', 'lawsuit_proceeding', None,
                  'property_claim', None, None, None, None, None, 4)
    add_values(302, values_302)


def main():
    create_table('status_log')
    add_test_users()


main()
