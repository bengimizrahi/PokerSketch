class Player:

    def __init__(self):
	self.name = ''
	self.chips = 0
	self.pot = 0

    def setName(self, name):
	self.name = name

    def setChips(self, chips):
	self.chips = chips

    def setCards(self, cards):
	self.cards = cards

    def putMoney(self, amount):
	assert self.chips >= amount
	self.chips -= amount
	self.pot += amount

    def __repr__(self):
	return "Player(Name:%s, Chips:$%s, Pot:$%s)" % (self.name, self.chips, self.pot)


class Action:
    
    def __init__(self, type, amount=0):
	self.type = type
	self.amount = amount

    def __repr__(self):
	return "Action(%s, $%s)" % (self.type, self.amount)


class SidePot:
    
    def __def__(self):
	self.amount = 0
	self.players = []

    def addAmount(self, amount):
	self.amount += amount

    def addPlayer(self, player):
	self.players.append(player)


class Game:

    def __init__(self):
	self.currentPlayer = None

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
	assert index > 0 and index <= 10
	if index >= len(self.players):
	    extendAmount = index - len(self.players) + 1
	    self.players.extend([None] * extendAmount)
	if self.players[index] == None:
	    self.players[index] = Player()
	self.cursor = self.players[index]

    def setDealer(self, dealer):
	self.dealer = dealer

    def setBlinds(self, smallBlind, bigBlind):
	self.smallBlind = smallBlind
	self.bigBlind = bigBlind
    
    def setAntes(self, antes):
	self.antes = antes

    def setCommunityCards(self, communityCards):
	self.communityCards = communityCards

    def playerByName(self, name):
	for player in self.players:
	    if player:
		if player.name == name:
		    return player
	return None

    def setup(self):
	assert self.numPlayers() > 1
	assert self.dealer
	if self.numPlayers() == 2:
	    self.currentPlayer = self.dealer
	    self.currentPlayer.putMoney(self.smallBlind)
	    self.moveToNextPlayer()
	    self.currentPlayer.putMoney(self.bigBlind)
	    self.moveToNextPlayer()
	else:
	    self.currentPlayer = self.nextPlayer(self.dealer)
	    self.currentPlayer.putMoney(self.smallBlind)
	    self.moveToNextPlayer()
	    self.currentPlayer.putMoney(self.bigBlind)
	    self.moveToNextPlayer()

    def __repr__(self):
	return """Players: %s
Blinds: %s-%s
Antes: %s
Dealer: %s
Current: %s
Community Cards: %s""" % (str(self.players), self.smallBlind, self.bigBlind, self.antes, self.dealer, self.cursor, str(self.communityCards)) 
