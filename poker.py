class Player:

    def setName(self, name):
	self.name = name

    def setChips(self, chips):
	self.chips = chips

    def setCards(self, cards):
	self.cards = cards

    def isValid(self):
	return hasAttr(self, name) and hasAttr(self, chips)

    def __repr__(self):
	return "Player: %s ($%s)" % (self.name, self.chips)

class Action:
    
    def __init__(self, type, amount=0):
	self.type = type
	self.amount = amount

    def __repr__(self):
	return "Action(%s, %s)" % (self.type, self.amount)

class SidePot:
    
    def __def__(self):
	self.amount = 0
	self.players = []

    def addAmount(self, amount):
	self.amount += amount

    def addPlayer(self, player):
	self.players.append(player)


class Game:

    def __init__(self, table):
	self.table = table
	self.actions = []

    def __repr__(self):
	pass
	

class Table:

    def __init__(self):
	self.cursor = None
	self.game = Game(self)

    def setNumPlayers(self, numPlayers):
	self.players = [None] * numPlayers

    def setCursor(self, index):
	assert index > 0 and index <= 10
	if index >= len(self.players):
	    extendAmount = index - len(self.players) + 1
	    self.players.extend([None] * extendAmount)
	if self.players[index] == None:
	    self.players[index] = Player()
	self.cursor = self.players[index]

    def setBlinds(self, smallBlind, bigBlind):
	self.smallBlind = smallBlind
	self.bigBlind = bigBlind
    
    def setAntes(self, antes):
	self.antes = antes

    def setCommunityCards(self, communityCards):
	self.communityCards = communityCards

    def setDealer(self, dealer):
	self.dealer = dealer

    def playerByName(self, name):
	for player in self.players:
	    if player:
		if player.name == name:
		    return player
	return None

    def isValid(self):
	pass

    def start(self):
	pass

    def __repr__(self):
	return """Players: %s
Blinds: %s-%s
Antes: %s
Dealer: %s
Cursor: %s
Community Cards: %s""" % (str(self.players), self.smallBlind, self.bigBlind, self.antes, self.dealer, self.cursor, str(self.communityCards)) 
