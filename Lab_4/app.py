from flask import Flask, render_template, request
from cur_conv import *
import psycopg2

conn = psycopg2.connect(dbname='d35ghu4nho8g46', user='noglraoqozczqg',
                        password='c3e7c74e860567d660bf4b365f5b400e9f7611d023fbc051d4b7a2cbef695833', host='ec2-54-247-122-209.eu-west-1.compute.amazonaws.com')
print("Database opened successfully")
cur = conn.cursor()
#cur.execute("CREATE TABLE forlab4 (id SERIAL PRIMARY KEY, " +
#    "from_ VARCHAR(4), value_ VARCHAR(20), to_ VARCHAR(4))")
#conn.commit()



app = Flask(__name__)


@app.route('/')
def index():
    values = [check_currency(DOLLAR_RUB), check_currency(EURO_RUB), check_currency(JPY_RUB)]
    for value in values:
        print(value)
    return render_template("index.html", cur_value=values)

@app.route("/submit", methods=["POST"])
def submit():
    values = [check_currency(DOLLAR_RUB), check_currency(EURO_RUB), check_currency(JPY_RUB)]
    if request.method == "POST":
        from_cur = request.form["from"]
        amount = request.form["cash"]
        to_cur = request.form["to"]
        cur.execute("INSERT INTO forlab4 (from_, value_, to_) VALUES (%s, %s, %s)", (from_cur, amount, to_cur))
        conn.commit()

    return render_template("index.html", cur_value=values)



if __name__ == "__main__":
    app.run()
    cur.close()
    conn.close()
