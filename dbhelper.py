# -*- coding: utf-8 -*-

import urllib.parse
import os
import psycopg2

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

connection = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port)
cursor = connection.cursor()

try:
    # cursor.execute("DROP TABLE predictions")
    # cursor.execute("DROP TABLE user_signs")

    cursor.execute("CREATE TABLE predictions ( date DATE, sign VARCHAR(20), prediction INTEGER ) ")
    cursor.execute("CREATE TABLE user_signs ( userID INTEGER, userSign VARCHAR(20) ) ")
    connection.commit()
except:
    connection.rollback()


def set_user_sign(user_id, sign):
    try:
        cursor.execute("SELECT userSign FROM user_signs WHERE userID = %s", (user_id, ))
        if cursor.fetchone():
            cursor.execute("UPDATE user_signs SET userSign = %(sign)s "
                           "WHERE userID = %(id)s", {'id': user_id, 'sign': sign[0]})
        else:
            cursor.execute("INSERT INTO user_signs ( userID, userSign ) "
                           "VALUES ( %s, %s ) ", (user_id, sign[0], ))
    except Exception as e:
        # print('set user sign EXCEPTION', e)
        pass
    finally:
        connection.commit()


def set_today_prediction(date, sign, prediction):
    date = date.strftime('%Y-%m-%d')
    try:
        cursor.execute("INSERT INTO predictions (date, sign, prediction) "
                       "VALUES ( %s, %s, %s ) ", (date, sign, prediction, ))
    except Exception as e:
        pass
        # print('set today prediction EXCEPTION', e)
    connection.commit()


def get_today_prediction(date, sign):
    date = date.strftime('%Y-%m-%d')
    try:
        cursor.execute("SELECT prediction FROM predictions WHERE date = %s AND sign = %s", (date, sign, ))
    except Exception as e:
        pass
        # print('get today prediction EXCEPTION: ', e)
    prediction = cursor.fetchone()
    if prediction:
        return prediction[0]
    return None


def get_user_sign(user_id):
    try:
        cursor.execute("SELECT userSign FROM user_signs WHERE userID = %s", (user_id, ))
    except Exception as e:
        pass
        # print('get user sign EXCEPTION', e)
    sign = cursor.fetchone()
    print(sign)
    if sign:
        return sign[0]
    return None
