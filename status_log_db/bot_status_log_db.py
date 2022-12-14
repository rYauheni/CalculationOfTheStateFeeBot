"""
The module contains a set of functions that describe the SQL requests needed to keep a log of user actions
when working with the Bot
"""

import sqlite3

table = 'status_log'
data_base = 'status_log.db'


def create_table():
    """
    Creates a table in the database to status log user actions (only if no table has been created)
    :return: None
    """
    with sqlite3.connect(f'{data_base}') as db:
        cursor = db.cursor()
        query = f""" CREATE TABLE IF NOT EXISTS '{table}'(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            user_name TEXT,
            type_court TEXT,
            instance TEXT,
            proceeding TEXT,
            criminal TEXT,
            claim TEXT,
            criminal_order TEXT,
            subject TEXT,
            court TEXT,
            ruling_on_adm TEXT,
            another_action TEXT,
            counter INT); """
        cursor.execute(query)
        db.commit()


def get_column_value(user_id: int, column_name: str) -> list[tuple[str]]:
    """
    Returns the field value of the user status log table based on the user id and column name as a list
    (if the field value is NULL, an empty list is returned)
    :param user_id: int
    :param column_name: str
    :return: list
    """
    with sqlite3.connect(f'{data_base}') as db:
        cursor = db.cursor()
        query = f"SELECT {column_name} FROM '{table}' WHERE user_id = {user_id};"
        cursor.execute(query)
        data = cursor.fetchall()
        db.commit()
        if data:
            return data[0][0]
        return []


def add_new_row(user_id: int):
    """
    Creates a status log table row for a new user based on user id if the user has not previously used the Bot.
    Otherwise, calls the cleanup function, which clears (passes NULL) all fields of the row except the id and user_id
    :param user_id:
    :return: None
    """
    with sqlite3.connect(f'{data_base}') as db:
        cursor = db.cursor()
        data = get_column_value(user_id, 'user_id')
        if not data:
            query = f"INSERT INTO '{table}' (user_id) VALUES ({user_id});"
            cursor.execute(query)
            db.commit()
        else:
            clear_values(user_id)


def add_column_value(user_id: int, column_name: str, value: str):
    """
    Fills the corresponding log table field based on the user id, column name, and the value passed.
    Raise an exception if a row with the corresponding user id does not exist
    :param user_id: int
    :param column_name: str
    :param value: str
    :return: None
    """
    with sqlite3.connect(f'{data_base}') as db:
        cursor = db.cursor()
        data = get_column_value(user_id, 'user_id')
        if data:
            query = f"UPDATE '{table}' SET {column_name} = '{value}' WHERE user_id = {user_id};"
            cursor.execute(query)
            db.commit()
        else:
            raise ValueError(f'Row (User) with user_id = {user_id} does not exist')


def get_new_counter_value(user_id):
    """
    Increments the value of the user action counter on each function call based on the user ID
    and returns new counter value.
    Necessary for numbering user actions when displaying to the user his sequence of actions.
    Raise an exception if a row with the corresponding user id does not exist
    :param user_id: int
    :return: int
    """
    with sqlite3.connect(f'{data_base}') as db:
        cursor = db.cursor()
        data = get_column_value(user_id, 'counter')
        if str(data):
            query = f"UPDATE '{table}' SET counter = counter + 1 WHERE user_id = {user_id};"
            cursor.execute(query)
            db.commit()
            return get_column_value(user_id, 'counter')
        else:
            raise ValueError(f'Field counter in row (User) with user_id = {user_id} is not filled')


def clear_values(user_id: int):
    """
    Clears (passes NULL) the value of all status log table fields except id and user_id based on user id
    :param user_id: int
    :return: None
    """
    with sqlite3.connect(f'{data_base}') as db:
        cursor = db.cursor()
        query = f""" UPDATE '{table}'
                    SET user_name = NULL,
                            type_court = NULL,
                            instance = NULL,
                            proceeding = NULL,
                            criminal = NULL,
                            claim = NULL,
                            criminal_order = NULL,
                            subject = NULL,
                            court = NULL,
                            ruling_on_adm = NULL,
                            another_action = NULL,
                            counter = NULL
                    WHERE user_id = {user_id}; """
        cursor.execute(query)
        db.commit()


def delete_row(user_id: int):
    """
    Deletes a table row of status log table corresponding to the user id
    :param user_id: int
    :return: None
    """
    with sqlite3.connect(f'{data_base}') as db:
        cursor = db.cursor()
        query = f"DELETE FROM '{table}' WHERE user_id = {user_id};"
        cursor.execute(query)
        db.commit()
