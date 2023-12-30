from flask import Flask, request, render_template, redirect, url_for
from scripts import ioLayer as IO
import openpyxl

app = Flask(__name__)

# Config

IO.init()


# Routing
@app.route("/", methods=("GET", "POST"))
def base_redirect():
    return redirect(url_for("bar_render"))


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "GET":
        return render_template("login.html")
    loginData = request.form.to_dict()
    if IO.auth(loginData["password"]):
        return redirect(url_for("dreix_render"))
    return redirect(url_for("bar_render"))


@app.route("/bar", methods=("GET", "POST"))
def bar_render():
    if request.method == "GET":
        users = IO.get_user_list()
        return render_template("bar.html", users=users)


@app.route("/order/<username>", methods=("GET", "POST"))
def order(username: str):
    if request.method == "GET":
        card = IO.get_card()
        user = IO.get_user(username)
        return render_template("order.html", user=user, card=card)


@app.route("/place_order/<drink>/<price>/<username>", methods=("GET", "POST"))
def place_order(drink: str, price: str, username: str):
    IO.place_order(username, drink, price)
    return redirect(url_for("order", username=username))


@app.route("/user_tab/<username>", methods=("GET", "POST"))
def user_tab(username: str):
    if not request.method == "GET":
        return redirect(url_for("bar_render"))
    user = IO.get_user(username)
    tab = IO.get_tab_list(username)
    return render_template("user.html", user=user, tabs=tab)


@app.route("/card", methods=("GET", "POST"))
def card_render():
    if request.method == "GET":
        card = IO.get_card()
        return render_template("card.html", card=card)
    newDrink = request.form.to_dict()
    isSuccess = IO.add_drink_to_card(newDrink)
    return redirect(url_for("card_render"))


@app.route("/card_delete/<item>")
def card_delete(item: str):
    isSuccess = IO.delete_drink_from_card(item)
    return redirect(url_for("card_render"))


@app.route("/user", methods=("GET", "POST"))
def user_render():
    if request.method == "GET":
        return render_template("user.html")


@app.route("/xxx", methods=("GET", "POST"))
def dreix_render():
    if request.method == "GET":
        users = IO.get_user_list()
        return render_template("xxx.html", users=users)
    return redirect(url_for("bar_render"))


@app.route("/delete_user/<username>", methods=("GET", "POST"))
def delete_user(username: str):
    IO.delete_user(username)
    return redirect(url_for("dreix_render"))


@app.route("/add_user", methods=("GET", "POST"))
def add_user():
    if request.method == "GET":
        return redirect(url_for("bar_render"))
    newUser = request.form.to_dict()
    IO.add_user(newUser)
    return redirect(url_for("dreix_render"))


@app.route("/billing", methods=("GET", "POST"))
def billing():
    IO.billing()
    return redirect(url_for("bar_render"))


if __name__ == "__main__":
    app.run(debug=False)
