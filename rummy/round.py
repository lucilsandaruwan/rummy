class Round:
    hands = []
    activeHand = ""
    roundNumber = 0 
    winner = ""
    marks = 0
    id = ""
    discardPile = None
    stockPile = None
    activeHandAction = 'draw'

    def __init__(self, params):
        for key, value in params.items():
            setattr(self, key, value)

    def  getJson(self, playerId):
        return {
            'hands': list(map(lambda hand: hand.getJson(playerId), self.hands))
            ,'activeHand':  self.activeHand
            ,'roundNumber': self.roundNumber
            ,'discardPile': self.discardPile.getJson()
            ,'stockPile': self.stockPile.getJson()
            ,'activeHandAction': self.activeHandAction
        }

    def draw(self, playerId,  type):
        playerHand = self.getPlayerHand(playerId)
        playerHandId = playerHand.getHandId()
        validDraw = playerHandId == self.activeHand and self.activeHandAction == 'draw'
        if not validDraw:
            raise ValueError("Invalid request please refresh the game and send request")
        card = self.discardPile.draw() if type == 'discard' else self.stockPile.draw()
        playerHand.pushCard(card)
        self.activeHandAction = 'discard'
        return card

    def getPlayerHand(self, playerId):
        print(self.hands, "self.hands self.hands")
        playerHands = list(filter(lambda x: x.isPlayerHand(playerId), self.hands))
        return playerHands[0] if playerHands else None

    def getId(self):
        return self.id
    
    def getActiveHandAction(self):
        return self.activeHandAction

    def meldValidate(self, playerHand):
        playerHandId = playerHand.getHandId()
        validDraw = playerHandId == self.activeHand and self.activeHandAction == 'discard'
        if not validDraw:
            raise ValueError("Invalid request please refresh the game and send request")

    def discard(self, playerId, card, gameModel):
        playerHand = self.getPlayerHand(playerId)
        playerHandId = playerHand.getHandId()
        validReq = playerHandId == self.activeHand and self.activeHandAction == 'discard'
        if not validReq:
            raise ValueError("Invalid request please refresh the game and send request")
        cardObj = playerHand.discard(card)
        self.discardPile.addCard(cardObj)
        self.setNextHand()
        gameModel.discard(cardObj, playerHand, self)

    def setNextHand(self):
        active = self.activeHand
        hands = self.hands
        nextHands = list(filter(lambda hand: hand.getHandId() > active, self.hands))
        
        if nextHands:
            nextHand = min(nextHands, key=lambda h: h.getId())
        else:
            nextHand = min(hands, key=lambda h: h.getId())
        self.activeHand = nextHand.getHandId()
        self.activeHandAction = "draw"
    
    def getActiveHand(self):
        return self.activeHand