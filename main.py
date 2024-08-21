import pygame, sys, random

# General Setup 
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock() # Makes sure game runs at a constant speed

# Setting up the main window 
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Defining colors 
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# Game Rectangles 
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 16, 16)
# Right side of screen
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 100)
# Left side of screen
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 100)

# Variables 
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

player_score = 0
opponent_score = 0
score_font = pygame.font.Font('freesansbold.ttf', 24)

score_time = True

pong_sound = pygame.mixer.Sound('Hit_3.wav')
score_sound = pygame.mixer.Sound('score.wav')

# Functions 
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time # Global Variables 
    # Ball Animations 
    ball.x += ball_speed_x  
    ball.y += ball_speed_y    

    # Vertical or y axis (bouncing ball)
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    # Horizontal or x axis (Player Score)
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
    # Opponent Score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    
    # Collisions 
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 10:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
      

# Player Animation 
def player_animation(): 
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height: 
        player.bottom = screen_height

# Opponent AI Animation 
def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height: 
        opponent.bottom = screen_height

# Ball Restart 
def ball_restart(): 
    global ball_speed_x, ball_speed_y, score_time, number_three, number_two, number_one # Global Variables

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = score_font.render('3', False, light_grey)
        screen.blit(number_three, (screen_width/2 - 8, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = score_font.render('2', False, light_grey)
        screen.blit(number_two, (screen_width/2 - 8, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = score_font.render('1', False, light_grey)
        screen.blit(number_one, (screen_width/2 - 8, screen_height/2 + 20))

    # Time until ball is released from center after scoring 
    
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else: 
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None

    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


# In-game while loop
while True:
    # Handling input
     
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Keyboard Functions 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # Game Logic - Functions 
    ball_animation()
    player_animation()
    opponent_ai()
  
# Visuals - in order (surface)
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2,0), (screen_width/2,screen_height))

    if score_time: 
        ball_restart()

# Text Visuals (text surface)
    player_text = score_font.render(f'{player_score}',False, light_grey) 
    screen.blit(player_text, (330, 227))

    opponent_text = score_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (297, 227))
    # second argument is if the text is anti aliased or not 

# Updating the window 
    pygame.display.flip() # Draws everything that came before it 
    clock.tick(60) # Frame Rate 
    


