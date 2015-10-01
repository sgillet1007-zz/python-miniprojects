# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


ball_pos = [WIDTH / 2, HEIGHT / 2] #list for ball position initialized to middle of canvas
ball_vel = [1, 2]  #list for ball velocity in pixels per tick

paddle1_pos = [PAD_WIDTH/2,HEIGHT/2]
paddle2_pos = [WIDTH-(PAD_WIDTH/2),HEIGHT/2]

paddle1_vel = [0]
paddle2_vel = [0]

SCORE_P1 = 0
SCORE_P2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_vel[0] =  random.randrange(2,5) #local variable for random horizontal velocity
    ball_vel[1] =  random.randrange(2,5)#local variable for random vertical velocity
    
    ball_pos = [WIDTH / 2, HEIGHT / 2] #re-initializes ball position to middle of canvas
    
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
        ball_vel[1] = -ball_vel[1]
    else:
        ball_vel[1] = -ball_vel[1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global SCORE_P1, SCORE_P2  # these are ints
    
    SCORE_P1 = 0
    SCORE_P2 = 0
    spawn_ball(random.choice([LEFT,RIGHT])) #starts new game with a random direction
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, SCORE_P1, SCORE_P2
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 0.5, "white")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "white")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "white")
        
    # update ball
    ball_pos[0] += ball_vel[0] #updates ball's x position
    ball_pos[1] += ball_vel[1] #updates ball's y position
    
    #collide and reflect off bottom wall
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    #collide and reflect off top wall
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    #Tests for right side paddle strike. If no strike then spawn ball to left.
    if ball_pos[0] >= (WIDTH - PAD_WIDTH) - BALL_RADIUS:
        if abs(paddle2_pos[1] - ball_pos[1]) <= (PAD_HEIGHT/2):
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            SCORE_P1 += 1
            spawn_ball(LEFT)
    
    #tests for left side paddle strike. If no strike then spawn ball to right.
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if abs(paddle1_pos[1] - ball_pos[1]) <= (PAD_HEIGHT/2):
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            SCORE_P2 += 1
            spawn_ball(RIGHT)
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "yellow", "yellow")
    
    # update paddle's vertical position, keep paddle on the screen
     #paddle1
    if (paddle1_pos[1] + paddle1_vel[0] >= PAD_HEIGHT/2) and (paddle1_pos[1] + paddle1_vel[0] <= (HEIGHT - PAD_HEIGHT/2)):
            paddle1_pos[1] += paddle1_vel[0]
      
     #paddle2
    if (paddle2_pos[1] + paddle2_vel[0] >= PAD_HEIGHT/2) and (paddle2_pos[1] + paddle2_vel[0] <= (HEIGHT - PAD_HEIGHT/2)):
        paddle2_pos[1] += paddle2_vel[0]
    
    # draw paddles
     #draw paddle1
    canvas.draw_polygon([[paddle1_pos[0]+(PAD_WIDTH/2),paddle1_pos[1]-(PAD_HEIGHT/2)],[paddle1_pos[0]+(PAD_WIDTH/2),paddle1_pos[1]+(PAD_HEIGHT/2)],[paddle1_pos[0]-(PAD_WIDTH/2),paddle1_pos[1]+(PAD_HEIGHT/2)],[paddle1_pos[0]-(PAD_WIDTH/2),paddle1_pos[1]-(PAD_HEIGHT/2)]],2,"orange","orange")
     #draw paddle2
    canvas.draw_polygon([[paddle2_pos[0]+(PAD_WIDTH/2),paddle2_pos[1]-(PAD_HEIGHT/2)],[paddle2_pos[0]+(PAD_WIDTH/2),paddle2_pos[1]+(PAD_HEIGHT/2)],[paddle2_pos[0]-(PAD_WIDTH/2),paddle2_pos[1]+(PAD_HEIGHT/2)],[paddle2_pos[0]-(PAD_WIDTH/2),paddle2_pos[1]-(PAD_HEIGHT/2)]],2,"orange","orange")
    # draw scores
    canvas.draw_text(str(SCORE_P1), [240,30], 36, "Green")
    canvas.draw_text(str(SCORE_P2), [343, 30], 36, "Green")

def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[0] = -7
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[0]= 7
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[0] = -7
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[0]= 7
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[0] = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[0] = 0
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[0] = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[0] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("RESET",new_game)

# start frame
new_game()
frame.start()
