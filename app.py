from flask import Flask, render_template, request
import pandas as pd
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    pie_chart = None
    bar_chart = None

    total = 0
    average = 0
    highest_category = ""

    if request.method == "POST":

        food = float(request.form["food"])
        travel = float(request.form["travel"])
        shopping = float(request.form["shopping"])
        others = float(request.form["others"])

        data = {
            "Category": ["Food", "Travel", "Shopping", "others"],
            "Amount": [food, travel, shopping, others]
        }

        df = pd.DataFrame(data)

        total = df["Amount"].sum()
        average = round(df["Amount"].mean(), 2)

        highest_category = df.loc[
            df["Amount"].idxmax(),
            "Category"
        ]

        # PIE CHART
        plt.figure(figsize=(5, 5))

        plt.pie(
            df["Amount"],
            labels=df["Category"],
            autopct="%1.1f%%"
        )

        plt.title("Expense Distribution")

        buffer = io.BytesIO()

        plt.savefig(buffer, format="png")
        buffer.seek(0)

        pie_chart = base64.b64encode(
            buffer.getvalue()
        ).decode()

        plt.close()

        # BAR CHART
        plt.figure(figsize=(6, 4))

        plt.bar(
            df["Category"],
            df["Amount"]
        )

        plt.title("Expense Comparison")
        plt.ylabel("Amount")

        buffer = io.BytesIO()

        plt.savefig(buffer, format="png")
        buffer.seek(0)

        bar_chart = base64.b64encode(
            buffer.getvalue()
        ).decode()

        plt.close()

    return render_template(
        "index.html",
        pie_chart=pie_chart,
        bar_chart=bar_chart,
        total=total,
        average=average,
        highest_category=highest_category
    )

if __name__ == "__main__":
    app.run(debug=True)