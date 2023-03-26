from card import Card
import random
class Deck:
    cards = []
    deelMapping = {
        10: [2], 
        7: [3, 4],
        6: [5, 6]
    }
    def __init__(self, cards):
        self.cards = cards

    def shuffleCards(self):
        random.shuffle(self.cards)

    def deal(self, hands):
        ret = []
        numbOfHands = len(hands)
        return num == 1 ? 10 : num <= 3 ? 7 : num <= 5 ? 6 : 0
        indexes = list(filter(lambda x: numbOfHands in x[1], self.deelMapping.items()))
        split_index = indexes[0][0] if indexes else 6

        for hand in hands:
            first_part = self.cards[:split_index]
            self.cards = self.cards[split_index:]
            hand.setCards(first_part)
            ret.append(hand)
        return ret