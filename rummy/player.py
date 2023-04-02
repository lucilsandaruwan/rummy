import pickle
import time
from meld import MeldRun, MeldSet
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
    sets = []
    runs = []
    roundId = ""
    def __init__(self, params):
        for key, value in params.items():
            setattr(self, key, value)

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
        jsonR['sets'] = list(map(lambda sete: sete.getJson(), self.sets))
        jsonR['runs'] = list(map(lambda run: run.getJson(), self.runs))
        jsonR['hand_id'] = self.handId
        if id == self.id:
            jsonR['cards'] = list(map(lambda card: card.getJson(), self.cards))
        else:
            jsonR['cards'] = []
            jsonR['cardCount'] = len(self.cards)
            
        return jsonR
    
    def setCards(self, cards):
        self.cards = cards
    
    def getCards(self):
        return self.cards

    def isPlayerHand(self, playerId):
        return True if self.id == playerId else False
    
    def pushCard(self, card):
        self.cards.append(card)

    def validateNewMeldCards(self, cards, meldAction):
        meldCards = []
        cards = sorted(cards, key=lambda card: card['value'])
        cardIds = []
        for card in cards:
            cId = card['id']
            cs = list(filter(lambda c: c.getId() == cId, self.cards))
            if not cs:
                raise ValueError("There is a card which is not in hand")
            meldCards.append(cs[0])
            cardIds.append(cId)
        meld = MeldRun(meldCards, None) if meldAction == 'run' else MeldSet(meldCards, None)
        if meld:
            self.cards = list(filter(lambda c: c.getId() not in cardIds, self.cards))
        return meld

    def setRoundId(self, roundId):
        self.roundId = roundId
    
    def getRoundId(self):
        return self.roundId
    
    def addMeld(self, meld):
        if isinstance(meld, MeldRun):
            self.runs.append(meld)
        else:
            self.sets.append(meld)
    def discard(self, card):
        cardId = card['id']
        c = next(filter(lambda c: c.getId() == cardId, self.cards), None)
        if not c:
            return ValueError("Invalid card")
        self.cards = [elem for elem in self.cards if elem.getId() != cardId]
        return c