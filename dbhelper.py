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
    cursor.execute("DROP TABLE predictions")
    cursor.execute("DROP TABLE user_signs")

    cursor.execute("CREATE TABLE predictions ( date DATE, sign VARCHAR(20), prediction INTEGER ) ")
    cursor.execute("CREATE TABLE user_signs ( userID INTEGER, userSign VARCHAR(20) ) ")
    connection.commit()
except:
    pass


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
        print('set user sign EXCEPTION', e)
    finally:
        connection.commit()


def set_today_prediction(date, sign, prediction):
    date = date.strftime('%Y-%m-%d')
    print('DATE FROM SET PREDICTION', date)
    try:
        cursor.execute("INSERT INTO predictions (date, sign, prediction) "
                       "VALUES ( %s, %s, %s ) ", (date, sign, prediction, ))
    except Exception as e:
        print('set today prediction EXCEPTION', e)
    connection.commit()


def get_today_prediction(date):
    # date = date.strftime('%d-%m-%Y')
    date = date.strftime('%Y-%m-%d')
    print('DATE FROM GET PREDICTION', date)
    try:
        cursor.execute("SELECT * FROM predictions WHERE date = %s", (date, ))
    except Exception as e:
        print('get today prediction EXCEPTION: ', e)
    prediction = cursor.fetchone()
    print('PREDICTION', prediction)
    if prediction:
        return prediction
    return None


def get_user_sign(user_id):
    try:
        cursor.execute("SELECT userSign FROM user_signs WHERE userID = %s", (user_id, ))
    except Exception as e:
        print('get user sign EXCEPTION', e)
    sign = cursor.fetchone()
    print('get user sign SIGN', sign)
    if sign:
        return sign
    return None
