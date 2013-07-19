from poker import *

class InputParser:
    
    def __init__(self, inputFile, game):
	self.game = game
	self.inputFile = inputFile

    def parse(self):
	input = open(self.inputFile, 'r')
	for line in input.readlines():
	    line = line.strip()
	    if len(line) == 0 or line.startswith('#'): continue
	    line = line.lower()
	    args = line.split(' ')
	    cmd = args.pop(0)
	    self.readLine(cmd, args)
	input.close()

    def readLine(self, cmd, args):
	if cmd == "num-seats":
	    numSeats = int(args.pop(0))
	    game.setNumSeats(numSeats)
	    return True
	elif cmd == "blinds":
	    smallBlind = int(args.pop(0))
	    bigBlind = int(args.pop(0))
	    game.setBlinds(smallBlind, bigBlind)
	    return True
	elif cmd == "antes":
	    antes = int(args.pop(0))
	    game.setAntes(antes)
	    return True
	elif cmd == "player":
	    playerIndex = int(args.pop(0))
	    return game.insertPlayerAtIndex(playerIndex)
	elif cmd == "name":
	    player = game.cursor
	    if player:
		name = args.pop(0)
		player.setName(name)
		return True
	    else:
		return False
	elif cmd == "chips":
	    player = game.cursor
	    if player:
		chips = int(args.pop(0))
		player.setChips(chips)
		return True
	    else:
		return False
	elif cmd == "cards" or cmd == "hold" or cmd == "holds":
	    player = game.cursor
	    if player:
		player.setCards(args)
		return True
	    else:
		return False
	elif cmd == "dealer":
	    if len(args) == 0:
		player = game.cursor
		if player:
		    game.setDealer(player)
		    return True
		else:
		    return False
	    elif len(args) == 1:
		name = args.pop(0)
		player = game.playerByName(name)
		if player:
		    game.setDealer(player)
		    return True
		else:
		    return False
	elif cmd == "community":
	    if args[0] == "cards":
		communityCards = args[1:]
	    else:
		communityCards = args
	    return game.setCommunityCards(communityCards)
	else:
	    name = cmd
	    player = game.playerByName(name)
	    if player:
		action = args.pop(0)
		if action == "hold" or action == "holds":
		    player.setCards(args)
		    return True
		elif action == "bet" or action == "bets":
		    # ACTION: bet
		    return True
		elif action == "call" or action == "calls":
		    # ACTION: call
		    return True
		elif action == "raise" or action == "raises":
		    # ACTION: raise
		    return True
		elif action == "go" or action == "goes":
		    if args[0] == "all-in" or (args[0] == "all" and args[1] == "in"):
			# ACTION: all-in
			return True
		    else:
			return False
	    else:
		return False


if __name__ == "__main__":
    game = Game()
    parser = InputParser("input.txt", game)
    parser.parse()
    game.setup()
    print game

