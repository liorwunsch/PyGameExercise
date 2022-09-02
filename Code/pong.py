import pygame, sys, random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x; ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height: ball_speed_y *= -1
    if ball.left <= 0: score_time = pygame.time.get_ticks(); player_score += 1
    if ball.right >= screen_width: score_time = pygame.time.get_ticks(); opponent_score += 1
    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0: player.top = 0
    if player.bottom >= screen_height: player.bottom = screen_height

def opponent_animation():
    if opponent.top < ball.y: opponent.top += opponent_speed
    if opponent.bottom > ball.y: opponent.bottom -= opponent_speed
    if opponent.top <= 0: opponent.top = 0
    if opponent.bottom >= screen_height: opponent.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y, score_time
    ball.topleft = start_pos
    curr_time = pygame.time.get_ticks()

    if score_time is None:
        return
    if curr_time - score_time < 700:
        number_three = score_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < curr_time - score_time < 1400:
        number_two = score_font.render("2", False, light_grey)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < curr_time - score_time < 2100:
        number_one = score_font.render("1", False, light_grey)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if curr_time - score_time < 2100:
        ball_speed_y,ball_speed_x = 0,0
    else:
        ball_speed_x = 7 * random.choice((1,-1))
        ball_speed_y = 7 * random.choice((1,-1))
        score_time = None

def draw_player_score():
    score_text = str(player_score)
    score_surface = score_font.render(score_text, True, (255, 255, 255))
    score_x = int(screen_width - 20); score_y = int(screen_height - 20)
    score_rect = score_surface.get_rect(center=(score_x,score_y))
    screen.blit(score_surface, score_rect)

def draw_opponent_score():
    score_text = str(opponent_score)
    score_surface = score_font.render(score_text, True, (255, 255, 255))
    score_x = int(10); score_y = int(screen_height - 20)
    score_rect = score_surface.get_rect(center=(score_x,score_y))
    screen.blit(score_surface, score_rect)

def game_over():
    pygame.quit(); sys.exit()

# General setup
pygame.init()
clock = pygame.time.Clock(); fps = 120

# Main Window
screen_width = 1280; screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Colors
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

# Game Rectangles
start_pos = (screen_width / 2 - 15, screen_height / 2 - 15)
ball = pygame.Rect(start_pos[0], start_pos[1], 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0; opponent_speed = 7
score_time = True

# Score Text
player_score = 0; opponent_score = 0
score_font = pygame.font.Font('Snake/Font/PoetsenOne-Regular.ttf', 25)

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_over()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: player_speed += 6
            if event.key == pygame.K_UP: player_speed -= 6
            if event.key == pygame.K_ESCAPE: game_over()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN: player_speed -= 6
            if event.key == pygame.K_UP: player_speed += 6

    # Game Logic
    ball_animation()
    player_animation()
    opponent_animation()

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    if score_time: ball_start()
    draw_player_score()
    draw_opponent_score()

    # Window Update
    pygame.display.flip()
    clock.tick(fps)
