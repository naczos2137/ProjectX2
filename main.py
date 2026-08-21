from flask import Flask, render_template, jsonify, request, session, redirect, abort
from game import Game
import time
import uuid

app = Flask(__name__)

game: Game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lobby')
def lobby():
    return render_template('lobby.html')

@app.route('/fake_ai')
def minigame_fake_ai():
    return render_template('minigames/fake_ai.html')

@app.route('/not_one_vote')
def minigame_not_one_vote():
    return render_template('minigames/not_one_vote.html')

@app.route('/blind_auction')
def minigame_blind_auction():
    return render_template('minigames/blind_auction.html')

@app.route('/be_closer')
def minigame_be_closer():
    return render_template('minigames/be_closer.html')

@app.route("/get_id")
def get_id():
    return jsonify({
        "client_id": str(uuid.uuid4())
    })

@app.get("/get_status")
def get_state():
    global game
    client_id = request.args.get("client_id")
    return jsonify(game.get_state(client_id))

@app.route("/set_info", methods=["POST"])
def set_info():
    global game
    data = request.get_json()
    client_id = data["client_id"]
    game_info = data["game_info"]
    game.set_info(client_id, game_info)

    return jsonify({"status": "ok"})

@app.route("/buy", methods=["POST"])
def buy():
    global game
    data = request.get_json()
    client_id = data["client_id"]
    item = data["item"]
    target_id = data.get("target_id", None)
    game.buy(client_id, item, target_id)
    return jsonify({"status": "ok"})

@app.route("/join", methods=["POST"])
def join():
    global game
    data = request.get_json()

    client_id = data["client_id"]
    name = data["name"]
    avatar = data["avatar"]

    if client_id not in game.players:
        game.add_player(client_id, name, avatar)
    else:
        game.update_player(client_id, name, avatar)

    return jsonify({"status": "ok"})

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/reset", methods=["POST"])
def admin_reset():
    global game
    game = Game()

    return jsonify({"status": "ok"})

@app.route("/admin/new_round", methods=["POST"])
def admin_new_round():
    global game
    game.new_round()

    return jsonify({"status": "ok"})

@app.route("/admin/lobby", methods=["POST"])
def admin_lobby():
    global game
    game.finish_round()

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
