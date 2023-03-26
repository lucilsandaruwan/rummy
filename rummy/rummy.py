
from flask import Flask, render_template, request, redirect, session, jsonify, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room
from player import Player 
# from game import Game
from models.playerModel import PlayerModel
from models.gameModel import GameModel
import sqlite3
from flask_cors import CORS, cross_origin
import time
import pickle
import json

async_mode = None
app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers='Set-Cookie')
# CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


app.secret_key = "rummy_test_app"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp'



@app.route('/fetch_user')
def fetchUser():
    return authontication(
        lambda: jsonify(getLoginUserJson())
    )

@app.route('/login', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    player = PlayerModel().login(email, password)
    if player:
        session['player'] = pickle.dumps(player)
        pJson = getLoginUserJson()
        return jsonify({'status': "success",'message': pJson})
    else:
        return jsonify({'status': "error", 'message':"Invalid username or password"})



@app.route('/load_game/')
def loadgame():
    def c():
        game = getGameJson()
        ret = {'status': 'success', 'data': game} if game else {}
        return jsonify(ret) 
    return authontication(c)

@app.route('/logout/')
def logout():
    session.clear()
    return jsonify({})

@app.route('/fetch_players')
def fetch_players():
    def x():
        player = getSesAsObj('player')
        players = PlayerModel().getPlayers(player.getId())
        return jsonify(list(map(lambda  player: {"id": player.getId(), "name": player.getName()}, players)))
    return authontication(x)

@app.route('/create_game', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def create_game():
    postRules = {
        'finish_mark': {'required': True}
        ,'players': {'requireed': True, 'type': 'list'}
    }
    def c(postData):
        postData['creator'] = getSesAsObj('player').getId()
        game = GameModel().create(postData)
        # print(game.roomId, 'game rooom id')
        if (game):
            game.sendInvitations(socketio.emit)
            return jsonify({'status': 'success', "data": postData}) 
        else:
            return jsonify({'status': 'success', "data": postData}) 
    return handlePost(postRules, None, authontication(lambda: c )) 

@app.route('/fetch_hands')
def fetch_hands():
    def f():
        return jsonify({
            'status': 'success'
            ,'data': getHandsJson()
        })
    return authontication(f)

@app.route('/accept_hand', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def accept_hand():
    postRules = {
        'id': {'required': True}
    }
    return handlePost(postRules,'accepted', authontication(lambda: updateHands )) 

@app.route('/decline_hand', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def decline_hand():
    postRules = {
        'id': {'required': True}
    }
    return handlePost(postRules,'declined', authontication(lambda: updateHands )) 

@cross_origin(supports_credentials=True)
@app.route('/start_game')
def startGameHandler(): 
    return authontication(startGame())

def startGame():
    gameModel = GameModel()
    player = getSesAsObj("player")
    gameModel.startGame(player.getId())

def updateHands(postData, status):
    gameModel = GameModel()
    player = getSesAsObj("player")
    update = gameModel.updateHandStatus(postData['id'], player.getId(), status)
    if update:
        return jsonify({
            'status': 'success'
            ,'data': getHandsJson()
        })
    else: 
        return jsonify({
            'status': 'error'
            ,'message': 'something is wrong'
        })
    
def getLoginUserJson():
    player = getSesAsObj("player")
    playerId = player.getId()
    pJson = player.getJson(playerId)
    pJson['isLogin'] = 1  
    pJson['hands'] = getHandsJson()
    return pJson

def getHandsJson():
    gameModel = GameModel()
    player = getSesAsObj("player")
    playerId = player.getId()
    hands = gameModel.getHandsByPlayer(playerId)
    for i, value in enumerate(hands):
        for key, val in value.items():
            value[key] = val.getJson(playerId) if val else None
        hands[i] = value
    return hands

def getGameJson():
    gameModel = GameModel()
    player = getSesAsObj("player")
    playerId = player.getId()
    game = gameModel.getGameByPlayer(playerId)
    return game.getJson(playerId) if game else {}
def getSesAsObj(key):
    if key in session:
        return pickle.loads(session.get(key))
    return {}

def handlePost(postRules, params, func):
    p = {}
    post = request.get_json()
    for name, value in postRules.items():
        try:
            if 'required' in value and value['required']:
                p[name] = post[name]
            else:
                p[name] = post[name] if name in post else None
        except:
            return jsonify({"status": "error", "message": "The field ? is missing or in wrong format".format(name), "code": 401})
    return func(p, params)
def authontication (func):
    player = getSesAsObj('player')
    if type(player) ==  Player:
        return func()
    return jsonify({"status": "error", "message": "User session exipired", "code": 400})

@socketio.on('connect')
def connect():
    emit('message', {'username': 'system', 'message': 'test'}, room='test_room')

@socketio.on('join')
def on_join(data):
    print(data['room'], 'room joined')
    join_room(data['room'])
    emit('message', {'username': 'system', 'message': 'test'}, room=data['room'])

@socketio.on('message')
def on_message(data):
    username = session['username']
    room = session['room']
    emit('message', {'username': username, 'message': data['message']}, room=room)



if __name__ == '__main__':
    socketio.run(app, host="localhost", port=int(8080))