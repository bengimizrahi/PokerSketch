from poker import *
from common import *

import sys


class InputParser:
    
    def __init__(self, inputFile, game):

	self.game = game
	self.inputFile = inputFile
	self.errors = []
	self.warnings = []


    def parse(self):

	input = open(self.inputFile, 'r')
	for (i, line) in enumerate(input.xreadlines()):
	    self.lineNumber = i + 1
	    line = line.strip()

	    print "----------- Line %d ---- %s ----------" % (self.lineNumber, line)

	    if len(line) == 0 or line.startswith('#'): continue

	    text_line = line
	    text_before = "BEFORE: %s\n\n%s" % (text_line, str(game))

	    line = line.lower()
	    args = line.split(' ')
	    cmd = args.pop(0)

	    if self.readLine(cmd, args):
		text_after = "AFTER: %s\n\n%s" % (text_line, str(game))
		print sideBySideText([text_before, text_after], 150)
	    else:
		print text_before
		input.close()
		return False

	input.close()
	return True


    def isNumber(self, str):

	tokens = str.split(".")
	for t in tokens:
	    if not t.isdigit():	
		return False
	return True


    def readLine(self, cmd, args):

	if cmd == "num-seats":
	    if not self.isNumber(args[0]):
		self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
		return False
	    numSeats = int(args.pop(0))
	    if numSeats < 2 or numSeats > 10:
		self.errors.append((self.lineNumber, "Number of seats cannot be less than 2 or greater than 10"))
		return False
	    else:
		self.game.setNumSeats(numSeats)
		return True

	elif cmd == "blinds":
	    if len(args) != 2:
		self.errors.append((self.lineNumber, "You should put two entries, one for small blind and one for big blind"))
		return False
	    if not self.isNumber(args[0]):
		self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
	    if not self.isNumber(args[1]):
		self.errors.append((self.lineNumber, "%s is not a valid number" % (args[1])))
	    smallBlind = int(args.pop(0))
	    bigBlind = int(args.pop(0))
	    if smallBlind > bigBlind:
		self.errors.append((self.lineNumber, "Small blind should be less than big blind"))
		return False
	    self.game.setBlinds(smallBlind, bigBlind)
	    return True

	elif cmd == "antes":
	    if len(args) != 1:
		self.warnings.append((self.lineNumber, "There must be only one entry for antes"))
	    if not self.isNumber(args[0]):
		self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
	    antes = int(args.pop(0))
	    self.game.setAntes(antes)
	    return True

	elif cmd == "player":
	    if not self.isNumber(args[0]):
		self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
	    if not self.isNumber(args[0]):
		self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
	    playerIndex = int(args.pop(0))
	    if self.game.insertPlayerAtIndex(playerIndex):
		return True
	    else:
		self.errors.append((self.lineNumber, "Failed to select player with index %s" % (playerIndex)))
		return False

	elif cmd == "name":
	    player = self.game.currentPlayer
	    if player:
		if len(args) == 0:
		    self.warnings.append((self.lineNumber, "No name has been entered here"))
		    name = "?"
		elif len(args) > 1:
		    self.warnings.append((self.lineNumber, "Only one name is allowed here"))
		name = args.pop(0)
		player.setName(name)
		return True
	    else:
		self.errors.append((self.lineNumber, "You should first select a player before naming"))
		return False

	elif cmd == "chips":
	    player = self.game.currentPlayer
	    if player:
		if len(args) == 0:
		    self.errors.append((self.lineNumber, "No amount of chips have been entered here"))
		    return False
		elif len(args) > 1:
		    self.warnings.append((self.lineNumber, "Only one entry is allowed here"))
		if not self.isNumber(args[0]):
		    self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
		stack = int(args.pop(0))
		player.setStack(stack)
		return True
	    else:
		self.errors.append((self.lineNumber, "You should first select a player before giving chips"))
		return False

	elif cmd == "cards" or cmd == "hold" or cmd == "holds":
	    player = self.game.currentPlayer
	    if player:
		player.setCards(args)
		return True
	    else:
		self.errors.append((self.lineNumber, "You should first select a player before selecting cards"))
		return False

	elif cmd == "dealer":
	    if len(args) == 0:
		player = self.game.currentPlayer
		if player:
		    self.game.setDealer(player)
		    return True
		else:
		    self.errors.append((self.lineNumber, "Either select a player first, or append the player name here"))
		    return False
	    
	    elif len(args) == 1:
		name = args.pop(0)
		if name == "player":
		    self.errors.append((self.lineNumber, "Player number has not been specified"))
		    return False
		player = self.game.playerByName(name)
		if player:
		    self.game.setDealer(player)
		    return True
		else:
		    self.errors.append((self.lineNumber, "Player %s cannot be found in the current list of players" % (name)))
		    return False

	    elif len(args) == 2:
		param = args.pop(0)
		if param != "player":
		    self.errors.append((self.lineNumber, "Syntax Error"))
		    return False
		number = args.pop(0)
		if not self.isNumber(number):
		    self.errors.append((self.lineNumber, "%s is not a valid number" % (number)))
		    return False
		index = int(number)
		if self.game.playerAtIndex(index) == None:
		    self.game.insertPlayerAtIndex(index)
		self.game.dealer = self.game.playerAtIndex(index) 
		return True

	elif cmd == "community":
	    if args[0] == "cards":
		communityCards = args[1:]
	    else:
		communityCards = args
	    if self.game.setCommunityCards(communityCards):
		return True
	    else:
		self.errors.append((self.lineNumber, self.game.lastError))
		return False

	else:
	    name = cmd
	    player = self.game.playerByName(name)

	    if player:
		if len(args) == 0:
		    self.errors.append((lineNumber, "No actions has been entered here"))
		    return False

		action = args.pop(0)
		if action == "hold" or action == "holds":
		    lastArg = args[len(args)-1]

		    if lastArg == "visible" or lastArg == "(visible)" or lastArg == "always-visible" or lastArg == "(always-visible)" or lastArg == "visible-always" or lastArg == "(visible-always)":
			player.cardVisibility = ALWAYS_VISIBLE
			args.pop()

		    elif lastArg == "invisible" or lastArg == "(invisible)":
			args.pop()

		    elif lastArg == "visible-on-hover" or lastArg == "(visible-on-hover)":
			player.cardVisibility = VISIBLE_ON_HOVER

		    if player.setCards(args):
			return True
		    else:
			self.errors.append((self.lineNumber, player.lastError))
			return False
		
		elif action == "fold" or action == "folds":
		    if self.game.addAction(player, FOLD):
			return True
		    else:
			self.errors.append((self.lineNumber, self.game.lastError))
			return False

		elif action == "check" or action == "checks":
		    if self.game.addAction(player, CHECK):
			return True
		    else:
			self.errors.append((self.lineNumber, self.game.lastError))
			return False

		elif action == "bet" or action == "bets":
		    if len(args) == 0:
			self.errors.append((self.lineNumber, "No amount of bet has been entered here"))
			return False
		    if not self.isNumber(args[0]):
			self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
		    amount = int(args.pop(0))
		    if self.game.addAction(player, BET, amount):
			return True
		    else:
			self.errors.append((self.lineNumber, self.game.lastError))
			return False

		elif action == "call" or action == "calls":
		    if self.game.addAction(player, CALL):
			return True
		    else:
			self.errors.append((self.lineNumber, self.game.lastError))
			return False

		elif action == "raise" or action == "raises":
		    nextWord = args[0]
		    if nextWord == "to":
			args.pop(0)
		    if len(args) == 0:
			self.errors.append((self.lineNumber, "No amount of raise has been entered here"))
			return False
		    if len(args) > 1:
			self.warnings.append((self.lineNumber, "Too many numbers have been entered; only the first one will be used"))
			return False
		    if not self.isNumber(args[0]):
			self.errors.append((self.lineNumber, "%s is not a valid number" % (args[0])))
			return False
		    amount = int(args.pop(0))
		    if self.game.addAction(player, RAISE, amount):
			return True
		    else:
			self.errors.append((self.lineNumber, "Error while processing action 'raise':\n\t%s" % (self.game.lastError)))
			return False

		elif action == "go" or action == "goes":
		    if args[0] == "all-in" or (args[0] == "all" and args[1] == "in"):
			if self.game.addAction(player, GO_ALL_IN):
			    return True
			else:
			    self.errors.append((self.lineNumber, self.game.lastError))
			    return False
		    else:
			self.errors.append((self.lineNumber, "Unknown command 'go'; did you mean 'go all-in'?"))
			return False
		else:
		    self.errors.append((self.lineNumber, "Unknown action '%s'" % (action)))
		    return False
	    else:
		self.warnings.append((self.lineNumber, "Unknown command or player '%s'" % (cmd)))
		return True


if __name__ == "__main__":

    if len(sys.argv) != 2:
	print "Usage: python %s <input file>" % (sys.argv[0])
	exit(1)

    game = Game()
    parser = InputParser(sys.argv[1], game)
    if not parser.parse():
	print "There were some errors in the text:"
	if len(parser.errors) > 0:
	    print "Errors:"
	for (lineNumber, error) in parser.errors:
	    print "On line %s: %s" % (lineNumber, error)
	print
	if len(parser.warnings) > 0:
	    print "Warnings:"
	for (lineNumber, warning) in parser.warnings:
	    print "On line %s: %s" % (lineNumber, warning)

