import pdb
import logging

INVISIBLE, ALWAYS_VISIBLE, VISIBLE_ON_HOVER = range(3)

NONE, CHECK, CALL, BET, RAISE, FOLD, GO_ALL_IN = range(7)
NONE, PRE_FLOP, FLOP, TURN, RIVER, SHOW_DOWN = range(6)
NONE, GAME_IN_PROGRESS, GAME_ENDED = range(3)


class SidePot:

    def __init__(self):

	self.players = None
	self.pot = 0

    
    def prepare(self, players):
	
	self.players = players
	minimumToSubtract = min(map(lambda player: player.bet, players))
	for player in self.players:
	    player.bet = player.bet - minimumToSubstract


    def __repr__(self):

        strs = []
	strs.append("SidePot:")
	strs.append("$%s" % (self.pot))
	for player in self.players:
	    strs.append("\t%s" % (player.name))

	
class Player:

    def __init__(self):

	self.name = ''
	self.stack = 0
	self.bet = 0
	self.cardVisibility = INVISIBLE 
	self.action = NONE
	self.state = NONE


    def setCards(self, cards):

	self.cards = cards
	return True


    def putMoney(self, amount):

	amountAvailable = min(self.stack, amount)
	self.stack -= amountAvailable
	self.bet += amountAvailable


    def __repr__(self):
	return "Player(Name:%s, Stack:$%s, Bet/Raise:$%s)" % (self.name, self.stack, self.bet)


class Game:

    def __init__(self):

	self.currentPlayer = None
	self.lastBetter = None
	self.state = NONE
	self.stage = NONE


    def setNumSeats(self, numSeats):

	self.players = [None] * numSeats


    def numOfPlayers(self):

	return len(filter(lambda player: player != None, self.players))


    def nextPlayer(self, player):

	return self.__nextPlayer__(player, False)


    def nextPlayerInGame(self, player):

	return self.__nextPlayer__(player, True)


    def __nextPlayer__(self, player, skipFolds):

	index = 0
	while self.players[index] != player:
	    index += 1
	index += 1
	while self.players[index % len(self.players)] != player:
	    nextPlayer = self.players[index % len(self.players)]
	    if nextPlayer:
		if skipFolds and nextPlayer.action == FOLD:
		    index += 1
		else:
		    return nextPlayer
	    else:
		index += 1
	return None
    

    def moveToNextPlayer(self):

	player = self.nextPlayer(self.currentPlayer)
	assert player
	self.currentPlayer = player


    def moveToNextPlayerInGame(self):

	player = self.nextPlayerInGame(self.currentPlayer)
	assert player
	self.currentPlayer = player


    def collectPots(self):

	claimingPlayers = filter(lambda player: player != None, self.players)
	assert all(map(lambda player: player.bet > 0, claimingPlayers))
	assert all(map(lambda player: player.bet == 0, claimingPlayers))

	while len(claimingPlayers) > 0:
	    sidePot = SidePot()
	    sidePot.prepare(claimingPlayers)
	    self.sidePots.append(sidePot)
	    map(lambda player: claimingPlayers.remove(player), filter(lambda player: player.bet == 0, claimingPlayers))


    def moveToNextStage(self):

	assert self.stage
	playersInGame = filter(lambda player: player != None and player.action != FOLD, self.players)
	if len(playersInGame) == 1:
	    self.state = GAME_ENDED
	    return True

	if self.stage == PRE_FLOP:
	    self.stage = FLOP
	    self.lastBetter = None
	    self.currentPlayer = self.nextPlayerInGame(self.dealer)
	    return True
	
	elif self.stage == FLOP:
	    self.stage = TURN
	    self.lastBetter = None
	    self.currentPlayer = self.nextPlayerInGame(self.dealer)
	    return True

	elif self.stage == TURN:
	    self.stage = RIVER
	    self.lastBetter = None
	    self.currentPlayer = self.nextPlayerInGame(self.dealer)
	    return True

	elif self.stage == RIVER:
	    self.stage = SHOW_DOWN
	    self.state = GAME_ENDED
	    # TODO
	    return True


    def insertPlayerAtIndex(self, index):

	arrayIndex = index - 1
	if index < 1:
	    self.lastError = "Index number cannot be smaller than 1"
	    return False
	if index > len(self.players):
	    self.lastError = "Index number cannot be greater than the number of players in table"
	    return False
	if self.players[arrayIndex] == None:
	    self.players[arrayIndex] = Player()
	self.currentPlayer = self.players[arrayIndex]
	return True


    def setDealer(self, dealer):

	self.dealer = dealer


    def setBlinds(self, smallBlind, bigBlind):

	self.smallBlind = smallBlind
	self.bigBlind = bigBlind
    

    def setAntes(self, antes):

	self.antes = antes


    def setCommunityCards(self, communityCards):

	self.communityCards = communityCards
	return True


    def playerByName(self, name):

	for player in self.players:
	    if player:
		if player.name == name:
		    return player
	return None


    def playerAtIndex(self, index):

	assert index >= 1 and index <= 9
	return self.players[index - 1]


    def start(self):

	if self.numOfPlayers() <= 1:
	    self.lastError = "There should be more than one player to start the game"
	    self.state = NONE
	    return False

	if not hasattr(self, "dealer") or not self.dealer:
	    self.lastError = "Cannot start the game without a dealer"
	    self.state = NONE
	    return False

	if self.smallBlind == 0 or self.bigBlind == 0:
	    self.lastError = "Blinds cannot be 0"
	    return False
	    
	self.stage = PRE_FLOP
	if hasattr(self, "antes") and self.antes > 0:
	    for player in filter(lambda player: player != None, self.players):
		if player.stack == 0:
		    self.lastError = "%s is out of chips"
		    return False

	if self.numOfPlayers() == 2:
	    self.currentPlayer = self.dealer
	    self.smallBlindPlayer = self.currentPlayer
	    self.smallBlindPlayer.putMoney(self.smallBlind)
	    self.moveToNextPlayerInGame()
	    self.bigBlindPlayer = self.currentPlayer
	    self.bigBlindPlayer.putMoney(self.bigBlind)
	    self.lastBetter = self.currentPlayer
	    self.moveToNextPlayerInGame()
	else:
	    self.currentPlayer = self.nextPlayer(self.dealer)
	    self.smallBlindPlayer = self.currentPlayer
	    self.currentPlayer.putMoney(self.smallBlind)
	    self.moveToNextPlayerInGame()
	    self.bigBlindPlayer = self.currentPlayer
	    self.bigBlindPlayer.putMoney(self.bigBlind)
	    self.lastBetter = self.currentPlayer
	    self.moveToNextPlayerInGame()

	self.state = GAME_IN_PROGRESS
	self.sidePots = []
	return True


    def addAction(self, player, action, amount=0):

	if self.state == NONE:
	    if not self.start():
		self.lastError = "Could not start the game, the following error occurred:\n\t%s" % (self.lastError)
		return False

	if player != self.currentPlayer:
	    self.lastError = "It's %s's turn." % (self.currentPlayer.name)
	    return False

	if action == FOLD:
	    self.currentPlayer.action = FOLD

	elif action == CHECK:
	    if self.lastBetter:
		self.lastError = "%s raised/bet, %s cannot check" % (self.lastBetter, self.currentPlayer)
		return False
	    else:
		self.currentPlayer.action = CHECK

	elif action == CALL:
	    diff = self.lastBetter.bet - self.currentPlayer.bet
	    self.currentPlayer.putMoney(diff)
	    self.currentPlayer.action = CALL

	elif action == BET:
	    if self.lastBetter:
		self.lastError = "%s can only raise here" % (self.currentPlayer.name)
		return False
	    self.currentPlayer.putMoney(amount)
	    self.lastBetter = self.currentPlayer

	elif action == RAISE:
	    if not self.lastBetter:
		self.lastError = "No one has bet yet, %s should bet here instead." % (self.currentPlayer.name)
		return False
	    if amount == self.lastBetter.bet:
		self.lastError = "This is not a raise, it is a call"
		return False
	    if amount < self.lastBetter.bet:
		self.lastError = "%s can only call with $%s here" % (self.currentPlayer, self.currentPlayer.stack + self.currentPlayer.bet)
		return False
	    diff = amount - self.currentPlayer.bet
	    if self.currentPlayer.stack < diff:
		self.lastError = "%s cannot put $%s, he/she only has $%s" % (self.currentPlayer, diff, self.currentPlayer.stack)
		return False
	    self.currentPlayer.putMoney(diff)
	    self.lastBetter = self.currentPlayer

	elif action == GO_ALL_IN:
	    self.currentPlayer.putMoney(self.currentPlayer.stack)
	    if self.currentPlayer.bet > self.lastBetter.bet:
		self.lastBetter = self.currentPlayer

	else:
	    self.lastError = "Unknown action: %s" % (action)
	    return False

	self.moveToNextPlayerInGame()
	if self.currentPlayer == self.lastBetter:
	    self.collectPot()
	    self.moveToNextStage()
	return True


    def __repr__(self):

	strs = []
	if self.state == NONE:
	    strs.append("Game: not started")
	    if hasattr(self, "numOfSeats"):
		 strs.append("Number of seats: %s\n" % (self.numOfSeats))
	    if hasattr(self, "players"):
		strs.append("Number of players: %s\n" % (self.numOfPlayers()))
		for (index, player) in enumerate(self.players):
		    substrs = []
		    substrs.append("%s." % (index + 1))
		    if hasattr(self, "dealer") and self.dealer == player:
			substrs.append("D")
		    elif hasattr(self, "smallBlindPlayer") and self.smallBlindPlayer == player:
			substrs.append("S")
		    elif hasattr(self, "bigBlindPlayer") and self.bigBlindPlayer == player:
			substrs.append("B")
		    else:
			substrs.append(" ")
		    if player:
			if player.name:
			    substrs.append("Name: %s" % (player.name))
			else:
			    substrs.append("Name: N/A")
		    else:
			substrs.append("<Empty Seat>")
		    if player:
			substrs.append("Stack: $%s" % (player.stack))
			if player.action != NONE:
			    substrs.append(["NONE", "CHECK", "CALL", "BET", "RAISE", "FOLD", "GO_ALL_IN"][player.action])
			if player.bet > 0:
			    substrs.append("-> $%s" % (player.bet))
		    if self.currentPlayer == player:
			substrs.append("<-- current player")
		    strs.append(" ".join(substrs))
	    if hasattr(self, "antes") and self.antes > 0:
		strs.append("Antes: %s" % (self.antes))
	    if hasattr(self, "smallBlind"):
		strs.append("Small Blind: %s" % (self.smallBlind))
	    if hasattr(self, "bigBlind"):
		strs.append("Big Blind: %s" % (self.bigBlind))
	    if hasattr(self, "communityCards"):
		strs.append("Community Cards: %s" % (self.communityCards))

	elif self.state == GAME_IN_PROGRESS:
	    strs.append("Game: in progress")
	    strs.append("Game stage: %s" % (["NONE", "PRE_FLOP", "FLOP", "TURN", "RIVER", "SHOW_DOWN"][self.stage]))
	    for (index, player) in enumerate(self.players):
		substrs = []
		substrs.append("%s." % (index + 1))
		if self.dealer == player:
		    substrs.append("D")
		elif self.smallBlindPlayer == player:
		    substrs.append("S")
		elif self.bigBlindPlayer == player:
		    substrs.append("B")
		else:
		    substrs.append(" ")
		if player:
		    substrs.append(player.name)
		else:
		    substrs.append("<Empty Seat>")
		if player:
		    substrs.append("Stack: $%s" % (player.stack))
		    if player.action != NONE:
			substrs.append(["NONE", "CHECK", "CALL", "BET", "RAISE", "FOLD", "GO_ALL_IN"][player.action])
		    if player.bet > 0:
			substrs.append("-> $%s" % (player.bet))
		    if self.currentPlayer == player:
			substrs.append("<-- current player")
		strs.append(" ".join(substrs))

	return "\n".join(strs)
