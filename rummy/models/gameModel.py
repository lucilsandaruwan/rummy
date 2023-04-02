from models.model import Model
from player import Hand, Player
from game import Game
import time
from deck import Deck, StockPile, DiscardPile
from card import Card
from round import Round
from meld import MeldRun, MeldSet
import json
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
            print(f"Error occurred: {e}")
            return None
            
    
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
                ,'handId': row['h_id']
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
            ,'handId': row['id']
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
            gameId = gameRow['id']
            game = Game(
                {
                    'id' : gameId
                    ,'finishMark' : gameRow['finish_mark']
                    ,'isCompleted': gameRow['is_completed']
                    ,'isStarted': gameRow['is_started']
                    ,'roomId' : gameRow['room_id']
                    ,'hands': self.getHandsByGameId(gameId)
                    ,'activeRound': self.getActiveRound(gameId)
                }
            )
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
        gameId = gameRow['id']
        hands = self.getHandsByGameId(gameId)
        game = Game({
            'id': gameRow['id']
            ,'hands': hands
        })
        activeHand = game.getFirstHand()
        activeHandId = activeHand.getHandId() if activeHand else None
        self.cur.execute("BEGIN")
        try:
            self.setStartGame(gameId)
            roundId = self.newRound(gameId, activeHandId, 1)
            deck = self.getCardDeck()
            deck.shuffleCards()
            hands = deck.deal(hands)
            self.setCardsInHands(hands, roundId)

            disCardPile = deck.getDiscardPile().getCards() 
            discardCard = disCardPile[0]
            self.addCardToDiscardPile(roundId, discardCard.getId())

            stockPile = deck.getStockPile().getCards()
            self.addCardsToStockPile(roundId, stockPile)
            self.con.commit()
            return True
        except Exception as e:
            self.con.rollback()
            print(f"Error occurred: {e}")
            return None

    def setStartGame(self, gameId):
        self.cur.execute('''
                UPDATE games
                SET is_started = 1
                WHERE id = ?
                ;
            ''',(gameId,))

    def addCardToDiscardPile(self, roundId, cardId):
        sql = '''
            INSERT INTO discardpile 
            (round_id, card_id) 
            VALUES (?, ?) '''
        self.cur.execute(sql, (roundId, cardId))

    def addCardsToStockPile(self, roundId, cards):
        sql = '''
            INSERT INTO stockpile 
            (round_id, card_id) 
            VALUES (?, ?) '''
        insData = []
        for card in cards:
            insData.append((roundId, card.getId()))
        self.cur.executemany(sql, insData)
    
    def setCardsInHands(self, hands, roundId):
        sql = '''
            INSERT INTO cards_in_hand 
            (hand_id, card_id, round_id) 
            VALUES (?, ?, ?) '''
        insData = []
        for hand in hands:
            cards = hand.getCards()
            if cards:
                for card in cards:
                    insData.append(
                        (hand.getHandId(), card.getId(), roundId)
                    )
        self.cur.executemany(sql, insData)
    
            
    def newRound(self, gameId, activeHandId, num):
        self.cur.execute('''
            INSERT INTO rounds 
            (game_id, round_number, active_hand) 
            VALUES (?, ?, ?)''', (gameId,num, activeHandId))
        return self.cur.lastrowid

    def getCardDeck(self):
        self.cur.execute('select * from cards')
        cardRows = self.cur.fetchall()
        if cardRows:
            return Deck(list(map(lambda row: self.getCardRow(row), cardRows))) 
    
    def getCardRow(self, row):
        return Card({
            'suit': row["suit"]
            ,'htmlCod': row['html_code']
            ,'lable': row['lable']
            ,'value': row['value']
            ,'id': row['id']
        }) 

    def getActiveRound(self, gameId):
        self.cur.execute('''
            WITH all_group AS (
                SELECT r.id AS round_id,
                    r.round_number,
                    r.active_hand,
                    r.active_hand_action,
                    h.id AS hands_id,
                    h.player_id AS player_id,
                    p.name AS player_name,
                    p.email AS player_email,
                    p.room_id AS player_room_id,
                    json_group_array(
                        json_object('cih_id', cih.id, 'id', c.id, 'suit', c.suit, 'lable', c.lable, 'value', c.value, 'html_code', c.html_code) 
                    ) AS cards
                FROM rounds AS r
                    LEFT JOIN
                    cards_in_hand AS cih ON r.id = cih.round_id
                    LEFT JOIN
                    hands AS h ON cih.hand_id = h.id
                    LEFT JOIN
                    cards AS c ON cih.card_id = c.id
                    LEFT JOIN
                    players AS p ON h.player_id = p.id
                WHERE r.game_id = ? AND 
                    r.is_complete != 1
                GROUP BY r.id, h.id
            ),
            g_rounds AS (
                SELECT round_id,
                    round_number,
                    active_hand,
                    active_hand_action,
                    json_group_array(
                        json_object(
                            'hands_id', hands_id
                            ,'player_id', player_id
                            ,'player_name', player_name
                            ,'player_email', player_email
                            ,'player_room_id', player_room_id
                            ,'cards', cards) 
                    ) AS hands
                FROM all_group
            )
            SELECT *
            FROM g_rounds
            GROUP BY round_id;
        ''', (gameId,))

        roundRow = self.cur.fetchone()

        hands = json.loads(roundRow['hands'])
        roundId = roundRow['round_id']
        sets = self.getSetsByRoundId(roundId)
        runs = self.getRunsByRoundId(roundId)
        hadsOfRounds = []
        for hand in hands:
            c = hand['cards']
            c = sorted(c, key=lambda card: card['cih_id'])
            cards = list(map(lambda row: self.getCardRow(row), c))
            handId = hand['hands_id']
            hadsOfRounds.append(
                Hand(
                    {
                        'email': hand['player_email']
                        ,'id': hand['player_id']
                        ,'name': hand['player_name']
                        ,'roomId': hand['player_room_id']
                        ,'handId': hand['hands_id']
                        ,'cards': cards
                        ,'sets': sets[handId] if handId in sets else []
                        ,'runs': runs[handId] if handId in runs else []
                    }
                )
            )
        
        round = Round({
            'hands': hadsOfRounds
            ,'activeHand': roundRow['active_hand']
            ,'roundNumber': roundRow['round_number']
            ,'activeHandAction': roundRow['active_hand_action']
            ,'id': roundId
            ,'discardPile': self.getPile(roundId, 'discardpile')
            ,'stockPile': self.getPile(roundId, 'stockpile')
        })
        return round
    
    def getSetsByRoundId(self, roundId):
        self.cur.execute('''
            WITH setl AS (
                SELECT s.round_id,
                    s.hand_id,
                    s.id AS set_id
                    ,json_group_array(
                            json_object('id', c.id, 'suit', c.suit, 'lable', c.lable, 'value', c.value, 'html_code', c.html_code) 
                        ) AS cards
                FROM sets AS s
                    LEFT JOIN
                    set_cards AS sc ON s.id = sc.set_id
                    LEFT JOIN
                    cards AS c ON sc.card_id = c.id
                WHERE round_id = ?
                group by hand_id, s.id
            )
            select round_id
            ,hand_id
            ,json_group_array(
                json_object(
                    'id', set_id
                    ,'cards', cards
                )
            ) AS sets
            from setl;
        ''', (roundId, ))
        ret = {}
        rows = self.cur.fetchall()
        if rows:
            for row in rows:
                ret[row['hand_id']] = [self.getMelds(setElement, 'set') for setElement in json.loads(row['sets'])]
        return ret
    
    def getRunsByRoundId(self, roundId):
        self.cur.execute('''
            WITH runl AS (
                SELECT r.round_id,
                    r.hand_id,
                    r.id AS run_id
                    ,json_group_array(
                            json_object('id', c.id, 'suit', c.suit, 'lable', c.lable, 'value', c.value, 'html_code', c.html_code) 
                        ) AS cards
                FROM runs AS r
                    LEFT JOIN
                    run_cards AS rc ON r.id = rc.run_id
                    LEFT JOIN
                    cards AS c ON rc.card_id = c.id
                WHERE round_id = ?
                group by hand_id, r.id
            )
            select round_id
            ,hand_id
            ,json_group_array(
                json_object(
                    'id', run_id
                    ,'cards', cards
                )
            ) AS runs
            from runl
        ''', (roundId, ))
        ret = {}
        rows = self.cur.fetchall()
        if rows:
            for row in rows:
                ret[row['hand_id']] = [self.getMelds(run, 'run') for run in json.loads(row['runs'])]
        return ret

    def getMelds(self, row, meldType):
        meldClasses = {'run': MeldRun, 'set': MeldSet}
        if meldType not in meldClasses:
            return {}
        meldClass = meldClasses[meldType]
        cards = sorted(row['cards'], key=lambda card: card['value'])
        return meldClass(
            list(map(lambda row: self.getCardRow(row), cards))
            ,row['id']
        )
    def getPile(self, roundId, tble):
        tbleObjMapping = {'discardpile': DiscardPile , 'stockpile': StockPile}
        if tble not in tbleObjMapping:
            return None

        self.cur.execute(
            ''' SELECT d.id
                ,round_id
                ,json_group_array(
                    json_object(
                        'pid', d.id, 'id', c.id, 'suit', c.suit, 'lable', c.lable, 'value', c.value, 'html_code', c.html_code
                    )
                ) AS cards
                FROM {} AS d
                left join cards as c
                on d.card_id = c.id
                WHERE d.round_id = ? '''.format(tble), (roundId,)
        )
        row = self.cur.fetchone()
        if row:
            cardRows = json.loads(row['cards'])
            cardRows = sorted(cardRows, key=lambda card: card['pid'])
            cards = list(map(lambda row: self.getCardRow(row), cardRows))
            pileObj = {
                'id': row['id']
                ,'roundId': row['round_id']
                ,'cards': cards
            }
            return tbleObjMapping[tble](pileObj)

    def draw(self, card, playerId, drawType, game):
        self.cur.execute("BEGIN")
        try:
            activeRound = game.getActiveround()
            playerHand = activeRound.getPlayerHand(playerId)
            roundId = activeRound.getId()
            handId = playerHand.getHandId()
            cardId = card.getId()

            drawTbl = 'discardpile' if drawType == 'discard' else 'stockpile'
            self.cur.execute('''
                DELETE FROM {}
                WHERE round_id = ? and card_id = ? 
            '''.format(drawTbl), (roundId, cardId))

            self.cur.execute('''
                INSERT INTO cards_in_hand 
                (hand_id, card_id, round_id) 
                VALUES (?, ?, ?)''', (handId, cardId, roundId))
            
            self.cur.execute('''
                UPDATE rounds
                SET active_hand_action = ?
                WHERE id = ?;
            ''', ("discard", roundId))
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            print(f"Error occurred: {e}")
    
    def meld(self, playerHand, cards, meldAction):
        roundId = playerHand.getRoundId()
        handId = playerHand.getHandId()
        self.cur.execute("BEGIN")
        meld = playerHand.validateNewMeldCards(cards, meldAction)
        # try:
        tble = 'runs' if meldAction == 'run' else 'sets'
        tble1 = 'run_cards' if meldAction == 'run' else 'set_cards'
        idCol = 'run_id' if meldAction == 'run' else 'set_id'
        self.cur.execute('''
            INSERT INTO {} 
            (round_id, hand_id) 
            VALUES (?, ?)'''.format(tble), (roundId, handId))
        meldId = self.cur.lastrowid
        sql = '''
            INSERT INTO {} 
            ({}, card_id) 
            VALUES (?, ?)'''.format(tble1, idCol)
        insData = []
        for card in cards:
            cardId = card['id']
            self.cur.execute('''
                DELETE FROM cards_in_hand
                WHERE round_id = ? and hand_id = ? and  card_id = ?
            ''', (roundId, handId, cardId))
            insData.append((meldId, cardId))
        self.cur.executemany(sql, insData)
        playerHand.addMeld(meld)
        self.con.commit()
        # except Exception as e:
        #     self.con.rollback()
        #     print(f"Error occurred: {e}")  
    
    def discard(self, card, hand, round):
        self.cur.execute("BEGIN")
        roundId = round.getId()
        handId = hand.getHandId()
        cardId = card.getId()
        activeHand = round.getActiveHand()
        # try:
        self.cur.execute('''
            DELETE FROM cards_in_hand
            WHERE round_id = ? and hand_id = ? and  card_id = ?
        ''', (roundId, handId, cardId))

        self.cur.execute('''
            INSERT INTO discardpile
            (round_id, card_id) 
            VALUES (?, ?)''', (roundId, cardId))

        self.cur.execute('''
            UPDATE rounds
            SET active_hand = ?, active_hand_action = ?
            WHERE id = ?;
        ''',(activeHand, 'draw', roundId))
        self.con.commit()
        # except Exception as e:
        #     self.con.rollback()
        #     print(f"Error occurred: {e}")  