INVISIBLE, ALWAYS_VISIBLE, VISIBLE_ON_HOVER = range(3)
NONE = 0
CALL, BET, RAISE, FOLD, GO_ALL_IN = range(5)
PRE_FLOP, FLOP, TURN, RIVER = range(4)

class Player:

    def __init__(self):
	self.name = ''
	self.chips = 0
	self.betOrRaise = 0
	self.cardVisibility = INVISIBLE 
	self.action = NONE

    def setName(self, name):
	self.name = name

    def setChips(self, chips):
	self.chips = chips

    def setCards(self, cards):
	self.cards = cards
	return True

    def putMoney(self, amount):
	if self.chips >= amount:
	    self.lastError = "Player %s has got only $%s worth of chips at this state"
	    return False
	self.chips -= amount
	self.pot += amount
	return True

    def __repr__(self):
	return "Player(Name:%s, Chips:$%s, Bet/Raise:$%s)" % (self.name, self.chips, self.betOrRaise)


class Game:

    def __init__(self):
	self.currentPlayer = None
	self.started = False
	self.stage = NONE

    def setNumSeats(self, numSeats):
	self.players = [None] * numSeats

    def numPlayers(self):
	return len(filter(lambda x: x != None, self.players))

    def nextPlayer(self, player):
	index = 0
	while self.players[index] != player:
	    index += 1
	index += 1
	while self.players[index % len(self.players)] != player:
	    nextPlayer = self.players[index % len(self.players)]
	    if nextPlayer:
		return nextPlayer
	    else:
		index += 1
	return None
    
    def moveToNextPlayer(self):
	currentPlayer = self.nextPlayer(self.currentPlayer)
	assert currentPlayer
	self.currentPlayer = currentPlayer

    def insertPlayerAtIndex(self, index):
	if index < 1:
	    self.lastError = "Index number cannot be smaller than 1"
	    return False
	if index > len(self.players):
	    self.lastError = "Index number cannot be greater than the number of players in table"
	    return False
	if self.players[index] == None:
	    self.players[index] = Player()
	self.currentPlayer = self.players[index]
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

    def start(self):
	if self.numPlayers() <= 1:
	    self.lastError = "There should be more than one player to start the game"
	    self.started = False
	    return False
	if not self.dealer:
	    self.lastError = "Cannot start the game without a dealer"
	    self.started = False
	    return False
	if self.numPlayers() == 2:
	    self.currentPlayer = self.dealer
	    self.currentPlayer.putMoney(self.smallBlind)
	    self.moveToNextPlayer()
	    self.currentPlayer.putMoney(self.bigBlind)
	    self.lastBetterOrRaiser = self.currentPlayer
	    self.moveToNextPlayer()
	else:
	    self.currentPlayer = self.nextPlayer(self.dealer)
	    self.currentPlayer.putMoney(self.smallBlind)
	    self.moveToNextPlayer()
	    self.currentPlayer.putMoney(self.bigBlind)
	    self.lastBetterOrRaiser = self.currentPlayer
	    self.moveToNextPlayer()
	self.started = True
	return True

    def maxBetOrRaise(self):
	return max(map(self.players, lambda x: x.betOrRaise))

    def addAction(self, action, amount=0):
	if not self.started:
	    if not self.start():
		self.lastError = "Could not start the game, the following error occurred:\n\t%s" % (self.lastError)
		return False
	if action == FOLD:
	    self.currentPlayer.action = FOLD
	    return True
	elif action == CALL:
	    return True
	elif action == BET:
	    if not self.currentPlayer.putMoney(amount):
		self.lastError = self.currentPlayer.lastError
		return False
	    else:
		return True
	elif action == RAISE:
	    if self.currentPlayer.putMoney(amount):
		self.lastError = self.currentPlayer.lastError
		return False
	    else:
		return True
	elif action == GO_ALL_IN:
	    # TODO
	    return True
	else:
	    self.lastError = "Unknown action: %s" % (action)
	    return False
    def __repr__(self):
	return """Players: %s
Blinds: %s-%s
Antes: %s
Dealer: %s
Current: %s
Community Cards: %s""" % (str(self.players), self.smallBlind, self.bigBlind, self.antes, self.dealer, self.currentPlayer, str(self.communityCards)) 
