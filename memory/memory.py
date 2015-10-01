# implementation of card game - Memory
import simplegui
import random
deck_1 = range(0,8) #list for first deck
deck_2 = range(0,8) #list for second deck
card_list = deck_1 + deck_2 #concatenates two deck lists
card_chosen0 = 3 #global for first card choice
card_chosen1 = 3 #global for second card choice
card_width = 50 #global variable for width of card
card_height = 100 #global variable for height of card
exposed = [] #empty list for cards with exposed values
for i in range(16): #loop for initializing cards as exposed equals false
        exposed.append(False)
turns = 0 #global variable for turns taken
state = 0 #global variable for tracking game state

# helper function to initialize globals
def new_game():
    global card_list, exposed, turns, state, card_chosen0, card_chosen1
    random.shuffle(card_list)
    exposed = [False]*16
    card_chosen0 = 3
    card_chosen1 = 3
    label.set_text('Turns = ' + str(turns))
    turns = 0
    state = 0
    
# define event handlers
def mouseclick(pos):
    global exposed, card_chosen0, card_chosen1, state
    index = int(pos[0]//50) #returns the index of the chosen card Note:replaces helper function card_clicked()
    print index

# add game state logic here    
    if state == 0:
        if exposed[index] == False:
            if(card_list[card_chosen0] != card_list[card_chosen1]):
                exposed[card_chosen0] = False
                #print card_chosen0
                #print type(card_chosen0)
                exposed[card_chosen1] = False  
            card_chosen0 = index
            exposed[index] = True
            state = 1            
            
    elif state == 1: #logic for game state 1
        global turns
        if exposed[index] == False:
            exposed[index] = True
            card_chosen1 = index
            turns += 1
            label.set_text('Turns = ' + str(turns))
            state = 0 

# cards are logically 50x100 pixels in size
def draw(canvas):
    for i in range(0,16):
        if exposed[i] == False:
            canvas.draw_polygon([(card_width*i,(card_height-card_height)),
                                 (card_width*(i+1),(card_height-card_height)),                        
                                 (card_width*(i+1),card_height),
                                 (card_width*i,card_height)],1,'black','green')
        else:
            canvas.draw_text(str(card_list[i]),
                             [card_width*i+10,card_height-25],55,'Red','serif')

# create frame and add a button and labels
frame = simplegui.create_frame('Memory', 800, 100)
frame.add_button('Restart', new_game)
label=frame.add_label('Turns = 0')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
