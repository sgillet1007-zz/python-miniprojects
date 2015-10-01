# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False #used to indicate hand is in play
outcome = ""
score = 0

#initialize global variabes for player hand, dealer hand, and the game deck
player_hand = []
dealer_hand = []
blackjack_deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            #print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand_cards = []	## hand_cards field is created and assigned an empty list     
        
    def __str__(self):
        # return a string representation of a hand
        hand_string = "Hand contains: "
        for c in self.hand_cards:
           hand_string += str(c) + ' '
        return hand_string

    def add_card(self, card):
        # add a card object to a hand
        self.added_card = self.hand_cards.append(card) ## appends new card to the hand_cards list
        return self.added_card

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0     ##initializes hand value to 0
        ace_in_hand = False ## boolean flag for aces in hand
        for card in self.hand_cards:     ##logic for scoring hand based on dealer's logic (i.e. never count 2 aces as having value = 11)
            card_value = VALUES[card.get_rank()]
            hand_value += card_value
            if card.get_rank() == 'A':
                ace_in_hand = True
        if ace_in_hand == False: # if no aces in hand just return the hand value
                return hand_value
        else:
            if hand_value + 10 > 21: #else if counting one ace as 11 busts the hand also just return the hand value
                    return hand_value
            else: #otherwise add 10 to the value of the hand
                    return hand_value + 10
        if hand_value == 0: #returns a value for the hand when no cards are in hand
                    return hand_value
                   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand_cards:
            card.draw(canvas,[pos[0]+ self.hand_cards.index(card)*90 ,pos[1]]) ##uses pos coords and increments x coord by 90 pixels for each succesive cards in hand
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.card_deck = []	#card_deck field is created and assigned empty list
        for s in SUITS:
            for r in RANKS:
                self.card_deck.append(Card(s,r))
        return self.card_deck
            
    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.card_deck) # use random.shuffle()
      
    def deal_card(self):
        # deal a card object from the deck
        self.dealt_card = self.card_deck[-1] #deals last card in deck
        self.card_deck.pop() #removes last card from deck after it has been dealt
        return self.dealt_card
        
    def __str__(self):
        # return a string representing the deck
        deck_string = "Deck contains "
        for c in self.card_deck:
            deck_string += str(c)+ ' '
        return deck_string

#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, blackjack_deck, score
    # your code goes here
    blackjack_deck = Deck() #makes blackjack_deck a Deck() instance
    blackjack_deck.shuffle() #shuffles blackjack_deck
        
    if in_play == True: #player loses if deal button is pressed during play
        score -= 1
        
    outcome = 'Hit or Stand?'
    #print outcome
    
    player_hand = Hand() #makes player_hand a Hand() instance
    player_hand.add_card(blackjack_deck.deal_card()) #adds first card to player's hand using Hand object method
    player_hand.add_card(blackjack_deck.deal_card()) #adds second card to player's hand using Hand object method
    #print 'Player Hand. ' + str(player_hand) 
        
    dealer_hand = Hand() #makes dealer_hand a Hand() instance
    dealer_hand.add_card(blackjack_deck.deal_card()) #adds first card to player's hand
    dealer_hand.add_card(blackjack_deck.deal_card()) #adds second card to player's hand
    #print 'Dealer Hand. ' + str(dealer_hand) 

    in_play = True
    
def hit():
    global outcome, in_play, score
 
    if in_play == True: # if the hand is in play, hit the player
        if player_hand.get_value() <= 21: #only hit player if hand is <= 21
            player_hand.add_card(blackjack_deck.deal_card())
            #print 'Player hits.'
            #print 'Player Hand. ' + str(player_hand)
            if player_hand.get_value() > 21: # if busted, assign a message to outcome, update in_play and score
                outcome = "You busted. Dealer wins. New Deal?"
                #print outcome
                score -= 1
                in_play = False
   
def stand():
    global outcome, in_play, score
    
    if in_play == True:# if current game is in play,... 
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(blackjack_deck.deal_card()) #repeatedly hit dealer until his hand has value 17 or more
            #print 'Dealer hits.'
            #print 'Dealer Hand. ' + str(dealer_hand)
            if dealer_hand.get_value() > 21:
                outcome = "Dealer busted. You win! New Deal?"
                #print outcome
                score += 1
                in_play = False
        if player_hand.get_value() > dealer_hand.get_value():
            outcome = "You win! Hooray! New Deal?"
            #print outcome
            score += 1
            in_play = False
        elif dealer_hand.get_value() <= 21: 
            outcome = "Dealer wins. New Deal?"
            #print outcome
            score -= 1
            in_play = False
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global score, outcome, in_play, card_back, CARD_SIZE
    # test to make sure that card.draw works, replace with your code below
    score_string = 'Score: ' + str(score)
    canvas.draw_text('Blackjack', (30, 70), 56, 'orange')
    canvas.draw_text(score_string, (420, 70), 36, 'gold') #draws score text
    canvas.draw_text('Dealer', (40, 160), 36, 'black')
    canvas.draw_text('Player', (40, 410), 36, 'black')
    
    canvas.draw_text(outcome, (220,410),22, 'gold') #draws outcome message that also prompts player.   
        
    #Draw dealer's hand on canvas
    dealer_hand.draw(canvas,[25,180])
    if in_play == True: # if hand is in play draw the back of the hole card
        canvas.draw_image(card_back, (108,48), CARD_SIZE, [151,228], CARD_SIZE)

    #Draw player's hand on canvas
    player_hand.draw(canvas,[25,430])
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
