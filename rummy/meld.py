class Meld:
    id = ""
    cards = []
    def __init__(self, cards, id):
        if (len(cards) < 3):
                raise ValueError("Number of cards should be more than 3")
        self.id = id
    def getJson(self):
        return {
            'id': self.id
            ,'cards': list(map(lambda card: card.getJson(), self.cards))
        }
    
class MeldRun(Meld):
    def __init__(self, cards, id):
        super().__init__(cards, id)
        suit = set(card.getSuit() for card in cards)
        if len(suit) != 1:
            raise ValueError("Cards should be in the same suit")
        values = [card.getValue() for card in cards]
        if max(values) - min(values) != len(values) - 1:
            raise ValueError("Cards should be in sequance")
        self.cards = cards

class MeldSet(Meld):
    def __init__(self, cards, id):
        super().__init__(cards, id)
        values = set(card.getValue() for card in cards)
        print (values)
        if len(values) != 1:
            raise ValueError("Cards should be having same rank")
        self.cards = cards