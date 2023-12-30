import os
import json
import sqlite3

with open(os.path.join(os.getcwd(), "static", "config.json")) as file:
    CONFIG = json.load(file)

DBFOLDER = CONFIG["dbFolder"]
DBNAME = CONFIG["dbName"]
DBPATH = os.path.join(os.getcwd(), DBFOLDER, DBNAME)


# DB Management
def init_db() -> bool:
    if os.path.exists(DBPATH):
        return True
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE card (item VARCHAR, price VARCHAR)")
    cursor.execute(
        "CREATE TABLE user (username VARCHAR, open VARCHAR, name VARCHAR, contact VARCHAR, orga VARCHAR)"
    )
    cursor.execute(
        "CREATE TABLE tabs (user VARCHAR, date VARCHAR, amount VARCHAR, price VARCHAR, total VARCHAR)"
    )
    connection.commit()
    connection.close
    return True


# User management
def user_add(username: str, name: str, contact: str, orga: str) -> bool:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM user WHERE username='{}'".format(username))
    if cursor.fetchone() is not None:
        connection.close()
        return False
    cursor.execute(
        "INSERT INTO user (username,open,name,contact,orga) VALUES('{}','0','{}','{}','{}')".format(
            username, name, contact, orga
        )
    )
    connection.commit()
    connection.close()
    return True


def user_update(username, openTab) -> bool:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM user WHERE username='{}'".format(username))
    if cursor.fetchone is None:
        return False
    cursor.execute(
        "UPDATE user SET open = '{}' WHERE username='{}'".format(openTab, username)
    )
    connection.commit()
    connection.close()
    return True


def user_delete(username) -> bool:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM user WHERE username='{}'".format(username))
    if cursor.fetchone() is None:
        connection.close()
        return False
    cursor.execute("DELETE FROM user WHERE username='{}'".format(username))
    connection.commit()
    connection.close()
    return True


def user_get(username) -> tuple:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username='{}'".format(username))
    user = cursor.fetchone()
    connection.close()
    return user


def user_get_list() -> list:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT username, open,name,contact,orga FROM user ORDER BY USERNAME DESC"
    )
    users = cursor.fetchall()
    connection.close()
    return users


def tab_add(username: str, order: dict) -> bool:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tabs (user, date, amount, price, total) VALUES ('{}','{}','{}','{}','{}')".format(
            username, order["date"], order["amount"], order["price"], order["total"]
        )
    )
    connection.commit()
    connection.close()
    return True


def tab_void(username: str) -> bool:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tabs WHERE user='{}'".format(username))
    connection.commit()
    connection.close()
    return True


def tab_get(username: str) -> list:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT user FROM tabs WHERE user='{}'".format(username))
    if cursor.fetchone() is None:
        connection.close()
        return []
    cursor.execute("SELECT * from tabs WHERE user='{}'".format(username))
    userTab = cursor.fetchall()
    connection.commit()
    connection.close()
    return userTab


# Card management
def card_add(item: str, price: str) -> bool:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT item FROM card WHERE item='{}'".format(item))
    if cursor.fetchone() is not None:
        connection.close()
        return False
    cursor.execute("INSERT INTO card (item, price) VALUES (?,?)", (item, price))
    connection.commit()
    connection.close()
    return True


def card_delete(item: str) -> bool:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT item FROM card WHERE item='{}'".format(item))
    if cursor.fetchone() is None:
        connection.close()
        return False
    cursor.execute("DELETE FROM card WHERE item='{}'".format(item))
    connection.commit()
    connection.close()
    return True


def card_get() -> list:
    connection = sqlite3.connect(DBPATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM card")
    card = cursor.fetchall()
    connection.close()
    return card


if __name__ == "__main__":
    testOrder = {"date": "01.03.23", "amount": "3", "price": "1", "total": "3"}
    init_db()
    user_add("zuse")
    print(card_add("beer", "0.5"))
    card_add("appler", "3")
    print(card_delete("beer"))
    print(card_get())
    tab_add("zuse", testOrder)
    print(tab_get("zuse"))
    tab_void("zuse")
    print(tab_get("zuse"))
    user_add("zuse")
    print(user_get("zuse"))
    user_update("zuse", "3")
    print(user_get("zuse"))
    print(user_add("zuse"))
    user_add("Maddin")
    user_delete("zuse")
    print(user_get("zuse"))
    print(user_get_list())
