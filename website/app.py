from flask import Flask, render_template, request
import plotly.express as px
import plotly.offline as opy
from helper_function import plot_players_right, plot_players_left, df_players, forward_features, plot_radar, df_radar

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    player1 = str(request.form.get("player1-input"))
    player2 = str(request.form.get("player2-input"))
    fig1 = plot_players_right(player1, forward_features, df_players)
    fig2 = plot_players_left(player2, forward_features, df_players)
    radar1 = plot_radar(player1, df_radar)
    radar2 = plot_radar(player2, df_radar)

    plot_div1 = opy.plot(fig1, auto_open=True, output_type='div')
    plot_div2 = opy.plot(fig2, auto_open=True, output_type='div')
    plot_radar1 = opy.plot(radar1, auto_open=True, output_type='div')
    plot_radar2 = opy.plot(radar2, auto_open=True, output_type='div')

    return render_template("results.html", plot_div1=plot_div1, plot_div2=plot_div2, 
                           player1=player1, player2=player2, radar1=plot_radar1, radar2=plot_radar2)

if __name__ == "__main__":
    app.run(debug=True)