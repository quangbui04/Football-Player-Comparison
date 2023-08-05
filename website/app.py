from flask import Flask, render_template, request
import plotly.express as px
import plotly.offline as opy
from helper_function import plot_players_right, plot_players_left, df_players, plot_radar, player_to_text, compare_stats_between_examples, df_radar, get_info, general_info, all_players, color_ranking, forward_features, midfielder_features, defender_features, forward_category, midfield_category, defend_category, similar_players, playing_time

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    player1 = str(request.form.get("player1-input"))
    player2 = str(request.form.get("player2-input"))
    position_submitted = str(request.form.get("position"))
    attributes = []
    category = []
    position_category = ""
    if position_submitted == "forward":
        attributes = forward_features
        category = forward_category
        position_category = "FW"
    elif position_submitted == "midfield":
        attributes = midfielder_features
        category = midfield_category
        position_category = "MF"
    elif position_submitted == "defend":
        attributes = defender_features
        category = defend_category
        position_category = "DF"
    
    if position_category !=  list(get_info(player1, ["Position Category"], df_players)[0].values[0])[0]:
        return render_template("notsamepos.html", player=player1, pos=position_submitted)
    elif position_category !=  list(get_info(player2, ["Position Category"], df_players)[0].values[0])[0]:
        return render_template("notsamepos.html", player=player2, pos=position_submitted)
    
    general_info1 = list(get_info(player1, general_info, df_players)[0].values[0])
    general_info2 = list(get_info(player2, general_info, df_players)[0].values[0])
    pos1 = general_info1[2]
    pos2 = general_info2[2]
    fig1 = plot_players_right(player1, attributes, df_players)
    fig2 = plot_players_right(player2, attributes, df_players)
    radar1 = plot_radar(player1, df_radar)
    radar2 = plot_radar(player2, df_radar)
    color1 = color_ranking[get_info(player1, general_info, df_players)[1]]
    color2 = color_ranking[get_info(player2, general_info, df_players)[1]]
    squad1 = general_info1[3]
    squad2 = general_info2[3]
    age1 = general_info1[4]
    age2 = general_info2[4]
    year1 = general_info1[5]
    year2 = general_info2[5]

    plot_div1 = opy.plot(fig1, auto_open=True, output_type='div')
    plot_div2 = opy.plot(fig2, auto_open=True, output_type='div')
    plot_radar1 = opy.plot(radar1, auto_open=True, output_type='div')
    plot_radar2 = opy.plot(radar2, auto_open=True, output_type='div')

    player_input = player_to_text(player1, player2, attributes)
    analysis = compare_stats_between_examples(player_input[0], player_input[1])["choices"][0]["text"]
    similar_player1 = similar_players(player1, playing_time + forward_features + midfielder_features + defender_features, df_radar)[1:11]
    similar_player2 = similar_players(player2, playing_time + forward_features + midfielder_features + defender_features, df_radar)[1:11]

    return render_template("results.html", plot_div1=plot_div1, plot_div2=plot_div2, 
                           player1=player1, player2=player2, radar1=plot_radar1, radar2=plot_radar2,
                           pos1=pos1, pos2=pos2, squad1=squad1, squad2=squad2, age1=age1, 
                           age2=age2, year1=year1, year2=year2, analysis=analysis, color1=color1, color2=color2, steelblue=category[0], green=category[1], gold=category[2], red=category[3], similar_player1=similar_player1, 
                           similar_player2=similar_player2)


if __name__ == "__main__":
    app.run(debug=True)