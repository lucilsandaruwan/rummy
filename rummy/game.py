
import random
# from models.gameModel import GameModel
class Game:
    id = 0
    finishMark = 100
    isCompleted = 0
    isStarted = 0
    roomId = 0
    hands = []
    activeRound = None
    def __init__(self, params):
        for key, value in params.items():
            setattr(self, key, value)
        

    def sendInvitations(self, emit):
        creator = [hand for hand in self.hands if hand.is_creator == 1].pop()
        for hand in self.hands:
            hand.sendGameInvitation(creator, emit)
    
    def getId(self):
        return self.id
    def getHands(self):
        return self.hands

    def setHands(self, hands):
        self.hands = hands

    def getJson(self, playerId):
        return {
            'finish_mark': self.finishMark
            ,'is_completed': self.isCompleted
            ,'is_started': self.isStarted
            ,'room_id': self.roomId
            ,'hands': list(map(lambda hand: hand.getJson(playerId), self.hands))
            ,'active_round': self.activeRound.getJson(playerId) if self.activeRound else {}
        }
    
    def getFirstHand(self):
        if not self.hands:
            return None
        suffHands = self.hands.copy()
        random.shuffle(suffHands)
        return suffHands[0]
    
    def getActiveround(self):
        return self.activeRound
