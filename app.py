from flask import Flask, render_template, request
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    expenses = []
    total = 0
    average = 0
    highest_category = ""
    insight = ""

    pie_chart = None
    bar_chart = None

    if request.method == "POST":

        categories = request.form.getlist("category")
        amounts = request.form.getlist("amount")

        data = []

        for category, amount in zip(categories, amounts):

            if category.strip() and amount.strip():

                data.append({
                    "Category": category,
                    "Amount": float(amount)
                })

        if data:

            df = pd.DataFrame(data)

            expenses = data

            total = round(df["Amount"].sum(), 2)

            average = round(df["Amount"].mean(), 2)

            highest_category = df.loc[
                df["Amount"].idxmax(),
                "Category"
            ]

            highest_amount = df["Amount"].max()

            percentage = round(
                (highest_amount / total) * 100,
                2
            )

            insight = (
                f"{highest_category} accounts for "
                f"{percentage}% of total spending."
            )

            # Pie Chart
            plt.figure(figsize=(5, 5))

            plt.pie(
                df["Amount"],
                labels=df["Category"],
                autopct="%1.1f%%"
            )

            plt.title("Expense Distribution")

            buffer = io.BytesIO()

            plt.savefig(
                buffer,
                format="png",
                bbox_inches="tight"
            )

            buffer.seek(0)

            pie_chart = base64.b64encode(
                buffer.getvalue()
            ).decode()

            plt.close()

            # Bar Chart
            plt.figure(figsize=(6, 4))

            plt.bar(
                df["Category"],
                df["Amount"]
            )

            plt.title("Expense Comparison")
            plt.ylabel("Amount")

            buffer = io.BytesIO()

            plt.savefig(
                buffer,
                format="png",
                bbox_inches="tight"
            )

            buffer.seek(0)

            bar_chart = base64.b64encode(
                buffer.getvalue()
            ).decode()

            plt.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        average=average,
        highest_category=highest_category,
        insight=insight,
        pie_chart=pie_chart,
        bar_chart=bar_chart
    )


if __name__ == "__main__":
    app.run(debug=True)
