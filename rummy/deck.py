import random
class DeckBase():
    cards = []
    def __init__(self, params):
        for key, value in params.items():
            setattr(self, key, value)

    def shuffleCards(self):
        random.shuffle(self.cards)
    
    def getCards(self):
        return self.cards

class Deck(DeckBase):
    def __init__(self, cards):
        super().__init__({'cards': cards})
    deelMapping = {
        10: [2], 
        7: [3, 4],
        6: [5, 6]
    }

    def deal(self, hands):
        ret = []
        numbOfHands = len(hands)
        indexes = list(filter(lambda x: numbOfHands in x[1], self.deelMapping.items()))
        split_index = indexes[0][0] if indexes else 6

        for hand in hands:
            first_part = self.cards[:split_index]
            self.setCards(self.cards[split_index:])
            hand.setCards(first_part)
            ret.append(hand)
        return ret
    
    def setCards(self, cards):
        self.cards = cards

    def getDiscardPile(self):
        card = self.cards.pop()
        cards = {'cards': [card]}
        return DeckBase(cards)

    def getStockPile(self):
        cardObj = { 'cards':  self.cards.copy()} 
        return DeckBase(cardObj)

    

class Pile(DeckBase):
    id = ""
    roundId = ""
    def __init__(self, params):
        super().__init__(params)
        
    def draw(self):
        return self.cards.pop()

    def addCard(self, card):
        self.cards.append(card)
    
class DiscardPile(Pile):
    def __init__(self, params):
        super().__init__(params)

    def getJson(self):
        return {
            'count': len(self.cards) - 1
            ,'lastCard': self.cards[-1].getJson() if self.cards[-1] else {}
        } if self.cards else {}

class StockPile(Pile):
    def __init__(self, params):
        super().__init__(params)

    def getJson(self):
        return {
            'count': len(self.cards) - 1
            ,'lastCard': {}
        }