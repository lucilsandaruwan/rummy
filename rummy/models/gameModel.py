from models.model import Model
from player import Hand
from player import Player
from game import Game
import time
from deck import Deck
from card import Card

class GameModel(Model):
    def create(self, data):
        game = None
        try:
            self.cur.execute("BEGIN")
            gameRoomId = "r{}".format(int(time.time()))
            self.cur.execute('''
                INSERT INTO games 
                (finish_mark, is_completed, room_id) 
                VALUES (?, ?, ?)''', (data['finish_mark'], 0, gameRoomId))
            gameId = self.cur.lastrowid

            sql = '''
                    INSERT INTO hands 
                    (game_id, player_id, is_creator, is_accepted ) 
                    VALUES (?, ?, ?, ?) '''
            insData = [(gameId, data['creator'], 1, 'accepted')]

            for player in data['players']:
                insData.append((
                    gameId
                    ,player['id']
                    ,0
                    ,'pending'
                ))
            self.cur.executemany(sql, insData)
            
            self.con.commit()

            hands = self.getHands(gameId)
            gameParams = {
                    'id': gameId
                    ,'finishMark': data['finish_mark']
                    ,'isCompleted': 0
                    ,'roomId': gameRoomId
                    ,'hands': hands
                }
            game = Game(gameParams)
            return game
        except Exception as e:
            # Rollback changes if an error occurs
            self.con.rollback()
            return None
            print(f"Error occurred: {e}")

        # finally:
        #     # Close cursor and connection
        #     # self.con.close()
    
    def getHands(self, gameId):
        self.cur.execute('''
            SELECT h.id AS h_id
            , room_id
            , is_accepted
            , is_creator
            , p.id AS player_id
            , p.name
            , p.email
            , p.room_id
            FROM hands AS h 
            LEFT JOIN players AS P
            ON h.player_id = p.id
            WHERE h.game_id = ?
            ''', (gameId,))
        players = self.cur.fetchall()
        # self.close_db()
        return list(map(lambda row: Hand(
            {
                'is_creator': row['is_creator']
                ,'is_accepted': row['is_accepted']
                ,'hand_id': row['h_id']
                ,'id': row['player_id']
                ,'name': row['name']
                ,'email': row['email']
                ,'roomId': row['room_id']
            }
        ), players))

    def getHandsByPlayer(self, playerId):
            self.cur.execute('''
                WITH player_d AS (
                    SELECT ? AS player_id
                ),
                tble AS (
                    SELECT h.*,
                    p.name,
                    p.email,
                    p.room_id,
                    CASE WHEN h.player_id != (SELECT player_id FROM player_d) THEN 1 ELSE 0 END AS acceptor
                    FROM games AS g
                    LEFT JOIN hands AS h ON g.id = h.game_id
                    LEFT JOIN players AS p ON h.player_id = p.id
                    WHERE g.id IN (
                        SELECT game_id
                        FROM hands
                        WHERE player_id = (
                            SELECT player_id
                            FROM player_d
                        )
                        AND is_accepted != 'declined'
                    )
                    AND g.is_completed != 1 
                    AND (h.player_id = (SELECT player_id FROM player_d) OR h.is_creator = 1) 
                ),
                p AS (
                    SELECT *
                    FROM tble
                    WHERE player_id = (SELECT player_id FROM player_d)
                ),
                c AS (
                    SELECT *
                    FROM tble
                    WHERE player_id != (SELECT player_id FROM player_d)
                )
                SELECT p.*,
                c.player_id AS creator_id,
                c.name AS creator_name,
                c.email AS creator_email,
                c.room_id AS creator_room_id
                FROM p
                LEFT JOIN c 
                ON p.game_id = c.game_id;
            ''', (playerId,))
            players = self.cur.fetchall()
            # self.close_db()
            accepted = list(filter(lambda x: (x['is_accepted'] == 'accepted'), players)) 
            if accepted:
                players = accepted
            return list(map(lambda row: self.getHandRow(row, withCreator = True), players))

    def getHandRow(self, row, withCreator):
        creator = None
        hand = Hand({
            'is_creator': row['is_creator']
            ,'is_accepted': row['is_accepted']
            ,'hand_id': row['id']
            ,'id': row['player_id']
            ,'name': row['name']
            ,'email': row['email']
            ,'roomId': row['room_id']
        })
        if 'creator_id' in row and row['creator_id']:
            creator = Player(row['creator_email'], row['creator_id'], row['creator_name'], row['creator_room_id'])
        return {
            'hand': hand
            ,'creator': creator
        } if withCreator else hand

    def updateHandStatus(self, handId, playerId, status):
        try:
            self.cur.execute('''
                UPDATE hands
                SET is_accepted = ?
                WHERE id IN (
                    SELECT h.id
                    FROM hands AS h
                    JOIN games AS g 
                    ON g.is_started != 1 
                    AND h.player_id = ? 
                    AND h.id = ?
                );
            ''',(status, playerId, handId))
            self.con.commit()
            return True
        except Exception as e:
            # Rollback changes if an error occurs
            return None

    def getGameByPlayer(self, playerId):
        game = None
        self.cur.execute('''
            SELECT *
            FROM games
            WHERE id IN (
                SELECT game_id
                FROM hands
                WHERE player_id = ? AND 
                    is_accepted = 'accepted'
            )
        ''', (playerId,))
        gameRow = self.cur.fetchone()
        if gameRow:
            game = Game(
                {
                    'id' : gameRow['id']
                    ,'finishMark' : gameRow['id']
                    ,'isCompleted': gameRow['is_completed']
                    ,'isStarted': gameRow['is_started']
                    ,'roomId' : gameRow['room_id']
                }
            )
            game.setHands(self.getHandsByGameId(game.getId())) 
        return game

    def getHandsByGameId(self, gameId):
        self.cur.execute('''
            SELECT h.* 
            ,p.name
            ,p.email
            ,p.room_id
            FROM hands as h 
            LEFT JOIN players AS p
            ON h.player_id = p.id
            WHERE h.game_id = ? AND h.is_accepted != 'declined'
        ''', (gameId,))
        players = self.cur.fetchall()
        return list(map(lambda row: self.getHandRow(row, withCreator = False), players))
    
    def startGame(self, playerId):
        self.cur.execute('''SELECT *
            FROM games
            WHERE id IN (
            SELECT game_id
            FROM hands
            WHERE player_id = ? AND 
            is_creator = 1
            );''', (playerId,)
        )
        gameRow = self.cur.fetchone()
        if not gameRow:
            return False
        game = Game(
            {
                'id' : gameRow['id']
                ,'finishMark' : gameRow['id']
                ,'isCompleted': gameRow['is_completed']
                ,'isStarted': gameRow['is_started']
                ,'roomId' : gameRow['room_id']
            }
        )
        gameId = game.getId()
        hands = self.getHandsByGameId(gameId)
        game.setHands(hands)
        try:
            roundId = self.newRound(gameId, 1)
            deck = self.getCardDeck()
            deck.shuffleCards()
            hands = deck.deel(hands)
            self.setCardsInHands(hands, roundId)

            # TODO: need top implement stockpile and descardpile

        except Exception as e:
            self.con.rollback()
            return None
            print(f"Error occurred: {e}")
    
    def setCardsInHands(self, hands, roundId):
        cards = hands.getCards()
        sql = '''
            INSERT INTO cards_in_hand 
            (hand_id, card_id, round_id) 
            VALUES (?, ?, ?) '''
        insData = []
        for hand in hands:
            if cards:
                for card in cards:
                    insData.append(
                        (hand.getHandId(), card.getId(), roundId)
                    )
        self.cur.executemany(sql, insData)
    
    def setHandsInFirstRounds(self, roundId, game):
        firstHand = game.getFirstHand()
        hands = game.getHands()
        gameId = game.getId()
        if not hands:
            return None
        for hand in hands:
            playing = 0
            if hand.getHandId() == firstHand.getHandId():
                playing = 1
            self.cur.execute('''
                INSERT INTO hands_in_rounds 
                (hand_id, round_id, playing) 
                VALUES (?, ?, ?)''', (gameId,roundId, playing))
            id = self.cur.lastrowid
            
    def newRound(self, gameId, num):
        self.cur.execute('''
            INSERT INTO rounds 
            (game_id, round_number) 
            VALUES (?, ?)''', (gameId,num))
        return self.cur.lastrowid

    def getCardDeck(self):
        self.cur.execute('select * from cards')
        cardRows = self.cur.fetchall()
        if cardRows:
            return Deck(list(map(lambda row: self.getCardRow(row), cardRows))) 
    
    def getCardRow(self, row):
        return Card({
            'suit': row['suit']
            ,'htmlCod': row['html_code']
            ,'lable': row['lable']
            ,'value': row['value']
            ,'id': row['id']
        }) 

