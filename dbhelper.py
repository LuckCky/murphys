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
    cursor.execute("CREATE TABLE predictions ( date DATE, prediction VARCHAR(2000) ) ")
    cursor.execute("CREATE TABLE user_signs ( userID INTEGER, userSign VARCHAR(20) ) ")
    connection.commit()
except:
    pass


def set_user_sign(user_id, sign):
    # cursor.execute("INSERT INTO user_signs ( userID, userSign ) "
    #                "VALUES ( %s, %s ) ON CONFLICT (userID) "
    #                "DO UPDATE SET userSign = %s", (user_id, sign, ))
    try:
        cursor.execute("INSERT INTO user_signs ( userID, userSign ) "
                       "VALUES ( %s, %s ) ", (user_id, sign[0], ))
    except Exception as e:
        print(e)
    finally:
        connection.commit()


def set_today_prediction(date, prediction):
    date = date.strftime('%d/%m/%Y')
    cursor.execute("INSERT INTO predictions (date, prediction) VALUES ( %s, %s ) ", (date, prediction, ))
    connection.commit()


def get_today_prediction(date):
    date = date.strftime('%d/%m/%Y')
    print('DATE FROM GET PREDICTION', date)
    cursor.execute("SELECT prediction FROM predictions WHERE date = %s", (date, ))
    prediction = cursor.fetchone()
    print('PREDICTION', prediction)
    if prediction:
        return prediction
    return None


def get_user_sign(user_id):
    cursor.execute("SELECT userSign FROM user_signs WHERE userID = %s", (user_id, ))
    sign = cursor.fetchone()
    if sign:
        return sign
    return None
