from flask import Flask, render_template, request
import plotly.express as px
import plotly.offline as opy
from helper_function import plot_players_right, df_players, forward_features

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    player1 = str(request.form.get("player1-input"))
    player2 = str(request.form.get("player2-input"))
    fig1 = plot_players_right(player1, forward_features, df_players)
    plot_div = opy.plot(fig1, auto_open=True, output_type='div')

    return render_template("results.html", plot_div=plot_div)

if __name__ == "__main__":
    app.run(debug=True)