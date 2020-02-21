import random
import time

#instance variables
myCards = []
splitCards = []
myCardValue = 0
dealersCards = []
dealerTopCard = []
dealerTopCardValue = 0
dealerCardValue = 0
splitCardValue = 0
deck = []
myMoney = 1000
myBet = 0
secondaryBet = 0
lost = False
won = False
pushed = False
insuranceTaken = False
doubleDownTaken = False
splitTaken = False


def blackjack():
	'''makes a game of blackjack'''

	global myCards
	global splitCards
	global dealersCards
	global myMoney
	global myBet
	global dealerTopCardValue
	global dealerTopCard
	global myCardValue
	global dealerCardValue
	global splitCardValue
	global lost
	global won
	global pushed
	global secondaryBet
	global insuranceTaken
	global doubleDownTaken
	global splitTaken
		
	lost = False
	won = False
	push = False
	myCards = []
	dealersCards = []
	splitCards = []
	dealerTopCard = []
	dealerTopCardValue = 0
	myCardValue = 0
	dealerCardValue = 0
	secondaryBet = 0
	insuranceTaken = False
	doubleDownTaken = False
	splitTaken = False
	splitCardValue = 0
	

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
	elif pushed:
		push()
		return
	elif splitTaken:
		splitMove()
		return
	playerMove()
	dealerHit()
	checkWin()
	if lost:
		loseMessage()
		return
	elif won:
		winMessage()
		return
	elif pushed:
		push()
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
	if myMoney <= 100:
		print("\nYou need more funds! Please wait 15 seconds to replenish your funds!\n")
		time.sleep(15)
		myMoney += 500
		print("$500 has been added to your funds!")
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

def sayCardsSplit():
	'''List the cards you have in a split deck'''
	print("The dealer's top card is the", deckToString(dealerTopCard)[0])
	print("You have the", " and the ".join(deckToString(splitCards)))

def sayCardValues():
	'''Say the value of the cards'''
	global myCardValue
	global dealerCardValue
	global dealerTopCardValue
	getCardValues()
	print("\nThe value of the dealer's",
		deckToString(dealerTopCard)[0], "is", dealerTopCardValue)
	print("The value of your cards in your main deck is", myCardValue)
	if splitTaken:
		print("The value of your cards in your secondary deck is", splitCardValue)


def getCardValues():
	'''gets the values of all decks'''
	global myCardValue
	global dealerCardValue
	global dealerTopCardValue
	global splitCardValue
	mySum = 0
	for i in myCards:
		mySum += i[2]
	myCardValue = mySum
	dealerSum = 0
	for i in dealersCards:
		dealerSum += i[2]
	dealerCardValue = dealerSum
	dealerTopCardValue = dealerTopCard[0][2]
	splitSum = 0
	for i in splitCards:
		splitSum += i[2]
	splitCardValue = splitSum
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
	print("\nIf you want to play again, type in blackjack()!\n")

def loseMessage():
	'''Displayed when the player loses'''
	global myMoney
	myMoney -= myBet
	print("\nDarn, you lost. D: Better luck next time! You have lost $%.2f. You have $%.2f remaining.\n"
		% (myBet, myMoney))
	print("\nIf you want to play again, type in blackjack()!\n")
		
def push():
	'''Displayed when there is a tie'''
	print("\nPush! You two have the same card value! You get back your bet. You have $%.2f remaining.\n" % (myMoney))
	print("\nIf you want to play again, type in blackjack()!\n")

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

		if dealerTopCardValue == 11:
			print("\nThe dealer has an ace. Do you want to take a separate insurance bet that pays double which is half your original bet?\n")
			insuranceCheck = False
			responseCheck = input("Do you want to bet insurance? (Y/N) ").upper()
			while insuranceCheck == False:
				if responseCheck == "Y":
					insurance()
					return
				elif responseCheck == "N":
					insuranceCheck = True
				else:
					print("\nInvalid input. Please try again.")
					responseCheck = input("Do you want to bet insurance? (Y/N) ").upper()

		if myCards[0][2] == myCards[1][2]:
			print("\nSince your two cards have the same value, you have the opportunity to split and play a separate game.\n")
			splitCheck = False
			responseCheck = input("Do you want to split? (Y/N) ").upper()
			while splitCheck == False:
				if responseCheck == "Y":
					split()
					return
				elif responseCheck == "N":
					splitCheck = True
				else:
					print("\nInvalid input. Please try again.")
					responseCheck = input("Do you want to split? (Y/N) ").upper()
	return

def surrender():
	'''causes the player to surrender'''
	global lost
	global myBet
	print("\nYou have decided to surrender.\n")
	lost = True
	myBet /= 2
	return

def split():
	global secondaryBet
	print("\nYou have now split your deck and bet the same as your original bet for the new deck.")
	splitCards.append(myCards.pop())
	secondaryBet = myBet
	pass


def doubleDown():
	global myBet
	global doubleDownTaken
	
	doubleDownTaken = True
	myBet *= 2
	print("\nYour bet has been doubled, making it now $%.2f." % (myBet))
	playerHit()
	dealerHit()
	checkWin()
	return


def insurance():
	global insuranceTaken
	global secondaryBet

	insuranceTaken = True
	secondaryBet = .5 * myBet
	print("\nYou have decided to take the insurance bet for $%.2f" % (secondaryBet))
	pass

def playerMove():
	playerTurn = True
	moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
	while playerTurn or myCardValue < 21:
		if moveCheck == "hit":
			playerHit()
			moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
		elif moveCheck == "stand":
			playerTurn = False
		else:
			print("\nInvalid input. Please try again.")
			moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
	return

def playerHit():
	myCards.append(deck.pop(random.randrange(len(deck))))
	sayCards()
	sayCardValues()
	return

def dealerHit():
	global lost
	global myBet
	global secondaryBet
	global myMoney
	print("The dealer has the", " and the ".join(deckToString(dealersCards)))
	print("The value of the dealer's cards is", dealerCardValue)
	if dealerCardValue == 21:
		print("\nThe dealer got blackjack! You lost 1.5 times your bet amount.\n")
		myBet *=1.5
		if splitTaken:
			secondaryBet *=1.5
		if insuranceTaken:
			print("\nHowever, you won the insurance bet! You get $%.2f back.\n" % 2*secondaryBet)
			myMoney += (2*secondaryBet)
		lost = True
		return
	elif insuranceTaken:
		print("\nHowever, you lost the insurance bet! You lost $%.2f.\n" % secondaryBet)
		myMoney -= secondaryBet
	while dealerCardValue < 17:	
		print("\nDealer is drawing.\n")
		time.sleep(1)
		dealersCards.append(deck.pop(random.randrange(len(deck))))
		sayCards()
		print("The dealer has the", " and the ".join(deckToString(dealersCards)))
		sayCardValues()
		print("The value of the dealer's cards is", dealerCardValue)
	return

def splitMove():
	'''Plays if you have a split'''
	global myMoney
	print("\nPlaying first deck\n")
	playerTurn = True
	moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
	while playerTurn or myCardValue < 21:
		if moveCheck == "hit":
			playerHit()
			moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
		elif moveCheck == "stand":
			playerTurn = False
		else:
			print("\nInvalid input. Please try again.")
			moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
	print("\nPlay second deck.\n")
	playerTurn = True
	moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
	while playerTurn or splitCardValue < 21:
		if moveCheck == "hit":
			splitCards.append(deck.pop(random.randrange(len(deck))))
			sayCardsSplit()
			sayCardValues()
			moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
		elif moveCheck == "stand":
			playerTurn = False
		else:
			print("\nInvalid input. Please try again.")
			moveCheck = input("Do you want to hit or stand? (hit/stand) ").lower()
	dealerHit()
	print("Checking deck 1")
	if myCardValue > 21:
		print("\nBust! You went over 21!\n")
		print("\nDarn, you lost for deck 1. D: Better luck next time! You have lost $%.2f. You have $%.2f remaining.\n"
		% (myBet, myMoney))
		myMoney -= myBet
	elif dealerCardValue > 21:
		print("\nBust! The dealer went over 21!\n")
		print("\nCongratulations! You win for deck 1! $%.2f has been added to your money amount! You currently have $%.2f.\n"
		% (myBet, myMoney))
		myMoney += myBet
	elif myCardValue == dealerCardValue:
		print("\nPush! You two have the same card value for deck 1! You get back your bet. You have $%.2f remaining.\n" % (myMoney))
	elif myCardValue < dealerCardValue:
		print("\nDarn, you lost for deck 1. D: Better luck next time! You have lost $%.2f. You have $%.2f remaining.\n"
		% (myBet, myMoney))
		myMoney -= myBet
	elif myCardValue > dealerCardValue:
		print("\nCongratulations! You win for deck 1! $%.2f has been added to your money amount! You currently have $%.2f.\n"
		% (myBet, myMoney))
		myMoney += myBet
	print("Checking deck 2")
	if myCardValue > 21:
		print("\nBust! You went over 21!\n")
		print("\nDarn, you lost for deck 2. D: Better luck next time! You have lost $%.2f. You have $%.2f remaining.\n"
		% (secondaryBet, myMoney))
		myMoney -= secondaryBet
	elif dealerCardValue > 21:
		print("\nBust! The dealer went over 21!\n")
		print("\nCongratulations! You win for deck 2! $%.2f has been added to your money amount! You currently have $%.2f.\n"
		% (secondaryBet, myMoney))
		myMoney += secondaryBet
	elif myCardValue == dealerCardValue:
		print("\nPush! You two have the same card value for deck 2! You get back your bet. You have $%.2f remaining.\n" % (myMoney))
	elif myCardValue < dealerCardValue:
		print("\nDarn, you lost for deck 2. D: Better luck next time! You have lost $%.2f. You have $%.2f remaining.\n"
		% (secondaryBet, myMoney))
		myMoney -= secondaryBet
	elif myCardValue > dealerCardValue:
		print("\nCongratulations! You win for deck 1! $%.2f has been added to your money amount! You currently have $%.2f.\n"
		% (secondaryBet, myMoney))
		myMoney += secondaryBet
	return


def checkWin():
	global won
	global lost
	global pushed
	global myBet

	if myCardValue > 21:
		print("\nBust! You went over 21!\n")
		lost = True
	elif dealerCardValue > 21:
		print("\nBust! The dealer went over 21!\n")
		won = True
	elif myCardValue == dealerCardValue:
		pushed = True
	elif myCardValue < dealerCardValue:
		lost = True
	elif myCardValue > dealerCardValue:
		won = True
	return

welcome()
blackjack()