import pickle
import time
# from dbConnector import DBConnector
from flask import session, jsonify
class Player:
    email = ""
    id = ""
    name = ""
    roomId = ""
    def __init__(self, email, id, name, roomId):
        self.email = email
        self.id = id
        self.roomId = roomId
        self.name = name

    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getEmail(self):
        return self.email
    def getRoomId(self):
        return self.roomId
    def getJson(self, id):
        return {
            'email': self.email
            ,'id': self.id
            ,'name': self.name
            ,'roomId': self.roomId
        } if id == self.id else {'name': self.name}

class Hand(Player):
    is_creator = 0
    is_accepted = -1
    handId = 0
    cards = []
    def __init__(self, params):
        super().__init__(params['email'], params['id'], params['name'], params['roomId'])
        self.is_creator = params['is_creator']
        self.is_accepted = params['is_accepted']
        self.handId = params['hand_id']

    def getHandId(self):
        return self.handId

    def __getattr__(self, name):
        if name == 'is_creator':
            return self.is_creator
    
    def sendGameInvitation(self, creator, emit):
        if self.is_accepted == 'pending' and self.is_creator != 1:
            print('emit game_invitation', {'hand_id': self.handId, 'creator': creator.getName()})
            emit('game_invitation', {'hand_id': self.handId, 'creator': creator.getName()}, room = self.roomId)

    def getJson(self, id):
        jsonR = super().getJson(id)
        jsonR['is_creator'] = self.is_creator
        jsonR['is_accepted'] = self.is_accepted
        if id == self.id:
            jsonR['hand_id'] = self.handId
        return jsonR
    
    def setCards(self, cards):
        self.cards = cards
    
    def getCards(self):
        return self.cards