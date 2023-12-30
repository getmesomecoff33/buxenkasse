import os
import json
import pandas
import hashlib
from datetime import datetime

from . import ioHandling as handle

with open(os.path.join(os.getcwd(), "static", "config.json")) as file:
    CONFIG = json.load(file)

BILLFOLDER = CONFIG["bill"]
if BILLFOLDER == "":
    BILLFOLDER = os.getcwd()


def init():
    handle.init_db()


def auth(pw: str) -> bool:
    if hashlib.sha256(pw.encode("utf-8")).hexdigest() == CONFIG["pw"]:
        return True
    return False


def get_card() -> list:
    return handle.card_get()


def add_drink_to_card(drink: dict):
    try:
        return handle.card_add(drink["dname"], drink["dprice"])
    except Exception as exe:
        return exe


def delete_drink_from_card(drink: str):
    try:
        return handle.card_delete(drink)
    except Exception as exe:
        return exe


def get_user(username: str) -> tuple:
    try:
        return handle.user_get(username)
    except Exception as exe:
        return exe


def get_user_list() -> list:
    try:
        users = []
        users = handle.user_get_list()
        return users
    except Exception as exe:
        return []


def get_tab_list(username: str) -> list:
    tabList = []
    tabList = handle.tab_get(username)
    return tabList


def place_order(username: str, drink: str, price: str, amount=1):
    price = int(price)
    total = str(int(amount) * price)
    day = str(datetime.now())
    order = {"date": day, "amount": drink, "price": str(price), "total": total}
    handle.tab_add(username, order)
    metaUser = handle.user_get(username)
    metaAmount = str(int(metaUser[1]) + int(total))
    handle.user_update(username, metaAmount)


def delete_user(username: str) -> bool:
    try:
        handle.tab_void(username)
        return handle.user_delete(username)
    except Exception as exe:
        return exe


def add_user(user: dict) -> bool:
    try:
        return handle.user_add(
            user["username"], user["full"], user["contact"], user["orga"]
        )
    except Exception as exe:
        return exe


def billing():
    today = datetime.today().strftime("%Y_%m_%d")
    billFile = os.path.join(BILLFOLDER, "Bill_" + today + ".xlsx")
    with pandas.ExcelWriter(billFile) as writer:
        users = handle.user_get_list()
        overview = pandas.DataFrame(users)
        overview.to_excel(writer, sheet_name="overview", index=False)
        for user in users:
            userTab = pandas.DataFrame(get_tab_list(user[0]))
            userTab.to_excel(writer, sheet_name=user[0], index=False)
            handle.tab_void(user[0])
            handle.user_update(user[0], 0)


if __name__ == "__main__":
    print(get_user_list())
