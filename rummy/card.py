class Card:
    suit = ""
    htmlCod = ""
    lable = ""
    value = ""
    id = ""
    def __init__(self, params):
        for key, value in params.items():
            setattr(self, key, value)
            
    def getId(self):
        return self.id
    
    def getSuit(self):
        return self.suit
    def getValue(self):
        return self.value

    def getJson(self):
        return {
            'suit': self.suit
            ,'htmlCod': self.htmlCod
            ,'lable': self.lable
            ,'value': self.value
            ,'id': self.id
        }