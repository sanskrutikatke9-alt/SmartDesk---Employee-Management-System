
# first

# import mysql.connector
# conn = mysql.connector.connect(
#     host="localhost" ,
#     user="root" ,
#     password="sanskruti@123" ,
#     database="smartdesk" 
# )
# cursor = conn.cursor(dictionary=True)

# first end





# second 
# ==============================
# SMARTDESK DATABASE CONNECTION
# db.py
# ==============================

import mysql.connector
from mysql.connector import Error


def create_connection():

    try:

        conn = mysql.connector.connect(

            host="localhost",

            user="root",

            password="sanskruti@123",

            database="smartdesk"

        )

        if conn.is_connected():

            print("SmartDesk Database Connected Successfully")

            return conn


    except Error as e:

        print("Database Connection Error :", e)

        return None



# Main Database Connection

conn = create_connection()


# Dictionary Cursor

if conn:

    cursor = conn.cursor(dictionary=True)

else:

    cursor = None



# ==============================
# Reconnect Function
# ==============================

def get_connection():

    global conn, cursor


    if conn is None or not conn.is_connected():

        conn = create_connection()

        if conn:

            cursor = conn.cursor(dictionary=True)


    return conn