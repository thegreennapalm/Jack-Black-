import random

#instance variables
myCards = []
myCardValue = 0
dealersCards = []
dealerTopCard = []
dealerTopCardValue = 0
dealerCardValue = 0
deck = []
myMoney = 1000
myBet = 0
secondaryBet = 0
lost = False
won = False
insuranceTaken = False
doubleDownTaken = False


def blackjack():
	'''makes a game of blackjack'''

	global myCards
	global dealersCards
	global myMoney
	global myBet
	global dealerTopCardValue
	global dealerTopCard
	global myCardValue
	global dealerCardValue
	global lost
	global won
		
	lost = False
	myCards = []
	dealersCards = []
	dealerTopCard = []
	if len(deck) < 60:
		print("\nShuffling deck.\n")
		generateDeck()
	myBet = wager()
	initialDraw()
	if isFirstRoundBlackjack():
		firstRoundBlackjack()
		return
	specialBetCheck()
	if lost:
		loseMessage()
		return
	elif won:
		winMessage()
		return

def firstRoundBlackjack():
	global myBet
	if dealerTopCardValue != 11:
			myBet *= 1.5
			print("\nYou got blackjack! You win 1.5 times your bet amount!\n")
			winMessage()
	else:
		print("\nThe dealer has an ace. Do you want to take even money to prevent a push and get back your original bet?\n")
		evenMoneyCheck = False
		responseCheck = input("Do you want to take even money? (Y/N) ").upper()
		while evenMoneyCheck == False:
			if responseCheck == "Y":
				evenMoneyCheck = True
				print("\nYou have decided to take even money.\n")
				winMessage()
				return
			elif responseCheck == "N":
				evenMoneyCheck = True
				if dealerCardValue == 21:
					push()
				else:
					myBet *= 1.5
					print("\nYou got blackjack! You win 1.5 times your bet amount!\n")
					winMessage()
			else:
				print("\nInvalid input. Please try again.")
				responseCheck = input("Do you want to take even money? (Y/N) ").upper()

def welcome():
	'''greets player'''
	print("Welcome to blackjack! Play at your own risk!\n")


def generateDeck():
	'''Makes a new deck'''
	global deck
	deck = []
	for numCards in range(52):
		card = [setNumber(numCards + 1), setSuit(numCards)]
		card.append(setValue(card))
		deck.append(card)
	deck *= 6


def setSuit(position):
	'''sets the suit of a card'''
	if position % 4 == 0:
		return "Spades"
	elif position % 4 == 1:
		return "Clubs"
	elif position % 4 == 2:
		return "Hearts"
	elif position % 4 == 3:
		return "Diamonds"


def setNumber(position):
	'''sets the number of the cards'''
	numArray = [2, 3, 4, 5, 6, 7, 8, 9, 10]
	if position % 13 in numArray:
		return str(position % 13)
	elif position % 13 == 1:
		return "Ace"
	elif position % 13 == 11:
		return "Jack"
	elif position % 13 == 12:
		return "Queen"
	elif position % 13 == 0:
		return "King"


def setValue(card):
	'''sets the blackjack value of a card'''
	try:
		return int(card[0])
	except:
		if card[0] == "Ace":
			return 11
		else:
			return 10


def deckToString(deck):
	'''turns each card into a string'''
	stringDeck = []
	for i in range(len(deck)):
		stringDeck.append(" of ".join([deck[i][0], deck[i][1]]))
	return stringDeck


def wager():
	'''makes a bet'''
	global myMoney
	wager = makeWager()
	invalidBet = True
	while invalidBet:
		if wager < 2:
			print("\nWager too low. Please wager again.")
			wager = makeWager()
		elif wager > myMoney:
			print("\nInsufficient funds! Please wager again.")
			wager = makeWager()
		elif wager > 500:
			print("\nWager too high. Please wager again.")
			wager = makeWager()
		else:
			invalidBet = False
	print("\nYou have wagered $%.2f.\n" % (wager))
	return wager


def makeWager():
	'''asks for a bet'''
	print(
		"\nYou currently have $%.2f. How much do you want to wager (between $2 and $500)?\n"
		% (myMoney))
	try:
		return int(input("Enter amount to wager: "))
	except:
		makeWager()


def initialDraw():
	'''first draw'''
	for i in range(2):
		myCards.append(deck.pop(random.randrange(len(deck))))
		dealersCards.append(deck.pop(random.randrange(len(deck))))
	dealerTopCard.append(dealersCards[0])
	sayCards()
	sayCardValues()


def sayCards():
	'''List the cards you have'''
	print("The dealer's top card is the", deckToString(dealerTopCard)[0])
	print("You have the", " and the ".join(deckToString(myCards)))


def sayCardValues():
	'''Say the value of the cards'''
	global myCardValue
	global dealerCardValue
	global dealerTopCardValue
	getCardValues()
	print("\nThe value of the dealer's",
		deckToString(dealerTopCard)[0], "is", dealerTopCardValue)
	print("The value of your cards is", myCardValue)


def getCardValues():
	'''gets the values of all decks'''
	global myCardValue
	global dealerCardValue
	global dealerTopCardValue
	mySum = 0
	for i in myCards:
		mySum += i[2]
	myCardValue = mySum
	dealerSum = 0
	for i in dealersCards:
		dealerSum += i[2]
	dealerCardValue = dealerSum
	dealerTopCardValue = dealerTopCard[0][2]
	return


def isFirstRoundBlackjack():
	'''Was the player handed a blackjack?'''
	return myCardValue == 21


def winMessage():
	'''Displayed when the player wins'''
	global myMoney
	myMoney += myBet
	print("\nCongratulations! You win! $%.2f has been added to your money amount! You currently have $%.2f.\n"
		% (myBet, myMoney))

def loseMessage():
	'''Displayed when the player loses'''
	global myMoney
	myMoney -= myBet
	print("\nDarn, you lost. D: Better luck next time! You have lost $%.2f. You have $%.2f remaining.\n"
		% (myBet, myMoney))
		
def push():
	'''Displayed when there is a tie'''
	print("\nPush! You two have the same card value! You get back your bet. You have $%.2f remaining.\n" % (myMoney))

def specialBetCheck():
	'''checks for split, double, insurance, surrender'''
	
	print("\nHave a bad hand? You have the option to surrender and get half your bet back!\n")
	surrenderCheck = False
	responseCheck = input("Do you want to surrender? (Y/N) ").upper()
	while surrenderCheck == False:
		if responseCheck == "Y":
			surrender()
			return
		elif responseCheck == "N":
			surrenderCheck = True
		else:
			print("\nInvalid input. Please try again.")
			responseCheck = input("Do you want to surrender? (Y/N) ").upper()
	
	print("\nThink you can beat the dealer? Double your bet and see if you can win with only one more card!\n")
	doubleDownCheck = False
	responseCheck = input("Do you want to double down? (Y/N) ").upper()
	while doubleDownCheck == False:
		if responseCheck == "Y":
			doubleDown()
			return
		elif responseCheck == "N":
			doubleDownCheck = True
		else:
			print("\nInvalid input. Please try again.")
			responseCheck = input("Do you want to double down? (Y/N) ").upper()
	pass

def surrender():
	'''causes the player to surrender'''
	global lost
	global myBet
	lost = True
	myBet /= 2
	return

def split():
	pass


def doubleDown():
	global myBet
	global doubleDownTaken

	doubleDownTaken = True
	myBet *= 2
	playerHit()
	dealerTurn()
	return


def insurance():
	pass


def playerHit():
	myCards.append(deck.pop(random.randrange(len(deck))))
	pass


def playerStand():
	pass


def dealerTurn():
	pass


def dealerHit():
	pass


def dealerStand():
	pass

def checkWin():
	pass

welcome()
blackjack()
