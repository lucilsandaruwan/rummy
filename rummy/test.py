from models.gameModel import GameModel

gameModel = GameModel()
game = gameModel.getGameByPlayer(2)
# print(game.getJson(1))
activeRound = game.getActiveround()
playerHand = activeRound.getPlayerHand(2)
# round = gameModel.getActiveRound(41).getJson(2)

# print(playerHand)

print(playerHand)