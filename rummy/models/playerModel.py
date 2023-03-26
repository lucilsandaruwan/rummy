# Import necessary modules
from models.model import Model
from player import Player
from typing import List
# Create a PlayerModel class that inherits from the Model class
class PlayerModel(Model):
    
    # method for player login that takes the following parameters:
    # - email (str): The email of the player trying to login
    # - password (str): The password of the player trying to login
    # Returns a Player object if the login is successful, None otherwise
    def login(self, email: str, password: str) -> Player:
        
        # Execute a SELECT query to check if player exists with the given email and password
        self.cur.execute('SELECT * FROM players where email = ? AND password = ?', (email, password))
        
        # Fetch the result of the query
        row = self.cur.fetchone()
        
        # Close the database connection
        # self.close_db()
        
        # Check if a player with the given email and password was found
        if row and 'id' in row:
            # If a player was found, return a Player object
            return Player(row['email'], row['id'], row['name'], row['room_id'])
        
        # If no player was found, return None
        return None
    
    # method to get all players except the one with the given id
    # Takes the following parameter:
    # - id (int): The id of the player to exclude from the result
    # Returns a list of Player objects
    def getPlayers(self, id: int) -> List[Player]:
        
        # Execute a SELECT query to get all players except the one with the given id
        self.cur.execute('SELECT id, name, email, room_id FROM players where id != ?', (id,))
        
        # Fetch all results of the query
        players = self.cur.fetchall()
        
        # Close the database connection
        # self.close_db()
        
        # Map the results to a list of Player objects and return the list
        return list(map(lambda row: Player(row['email'], row['id'], row['name'], row['room_id']), players))
