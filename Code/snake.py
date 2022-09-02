import pygame, sys, random
from pygame.math import Vector2

cell_size = 40; num_of_cells = 20

class FRUIT:
    def __init__(self, screen_):
        self.screen = screen_
        self.pos = Vector2(0,0)
        self.randomize()
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()

    def draw_fruit(self):
        rect_pos = [value * cell_size for value in self.pos]
        rect_size = cell_size
        rect_color = (126,166,114)
        fruit_rect = pygame.Rect(int(rect_pos[0]), int(rect_pos[1]), rect_size, rect_size)
        self.screen.blit(self.apple, fruit_rect)
        #pygame.draw.rect(screen, rect_color, fruit_rect)

    def randomize(self):
        x = random.randint(0, num_of_cells - 1); y = random.randint(0, num_of_cells - 1)
        self.pos = Vector2(x, y)

class SNAKE:
    def __init__(self, screen_):
        self.screen = screen_
        self.init_body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.body = self.init_body
        self.init_direction = Vector2(1,0)
        self.direction = self.init_direction
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.head_img = self.head_right

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.tail_img = self.tail_left

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        rect_size = cell_size
        # rect_color = (183, 111, 122)
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            rect_pos = [value * cell_size for value in block]
            block_rect = pygame.Rect(int(rect_pos[0]), int(rect_pos[1]), rect_size, rect_size)
            if index == 0:
                self.screen.blit(self.head_img, block_rect)
            elif index == len(self.body) - 1:
                self.screen.blit(self.tail_img, block_rect)
            else:
                body_img = self.body_horizontal
                previous_block_relation = self.body[index + 1] - block
                next_block_relation = self.body[index - 1] - block
                if previous_block_relation.x == next_block_relation.x:
                    body_img = self.body_vertical
                elif previous_block_relation.y == next_block_relation.y:
                    body_img = self.body_horizontal
                else:
                    if previous_block_relation.x == -1 and next_block_relation.y == -1 or previous_block_relation.y == -1 and next_block_relation.x == -1:
                        body_img = self.body_tl
                    elif previous_block_relation.x == -1 and next_block_relation.y == 1 or previous_block_relation.y == 1 and next_block_relation.x == -1:
                        body_img = self.body_bl
                    elif previous_block_relation.x == 1 and next_block_relation.y == -1 or previous_block_relation.y == -1 and next_block_relation.x == 1:
                        body_img = self.body_tr
                    elif previous_block_relation.x == 1 and next_block_relation.y == 1 or previous_block_relation.y == 1 and next_block_relation.x == 1:
                        body_img = self.body_br

                self.screen.blit(body_img, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(0,1): self.head_img = self.head_up
        if head_relation == Vector2(-1,0): self.head_img = self.head_right
        if head_relation == Vector2(0,-1): self.head_img = self.head_down
        if head_relation == Vector2(1,0): self.head_img = self.head_left

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(0,1): self.tail_img = self.tail_up
        if tail_relation == Vector2(-1,0): self.tail_img = self.tail_right
        if tail_relation == Vector2(0,-1): self.tail_img = self.tail_down
        if tail_relation == Vector2(1,0): self.tail_img = self.tail_left

    def move_snake(self):  # from head = body[0]
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def change_direction(self, event_key):
        if event_key == pygame.K_UP:
            if self.direction.y != 1:
                self.direction = Vector2(0,-1)
        if event_key == pygame.K_RIGHT:
            if self.direction.x != -1:
                self.direction = Vector2(1,0)
        if event_key == pygame.K_DOWN:
            if self.direction.y != -1:
                self.direction = Vector2(0,1)
        if event_key == pygame.K_LEFT:
            if self.direction.x != 1:
                self.direction = Vector2(-1,0)

    def reset(self):
        self.body = self.init_body
        self.direction = self.init_direction

class GAME:
    def __init__(self):
        self.interval_ms = 150
        pygame.time.set_timer(pygame.USEREVENT, self.interval_ms)
        self.screen_size = cell_size * num_of_cells
        self.screen_color = (175, 215, 70)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))

        self.snake = SNAKE(self.screen)
        self.fruit = FRUIT(self.screen)
        self.game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

    def update(self):
        self.snake.move_snake()
        if self.check_collision():
            self.interval_ms -= 2
            pygame.time.set_timer(pygame.USEREVENT, self.interval_ms)
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            print('snack')
            self.snake.add_block()
            # self.snake.crunch_sound.play()
            self.fruit_randomize()
            return True
        return False

    def fruit_randomize(self):
        b_old_fruit = True
        while b_old_fruit:
            self.fruit.randomize()
            b_old_fruit = False
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    b_old_fruit = True
                    break

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < num_of_cells or not 0 <= self.snake.body[0].y < num_of_cells:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        rect_size = cell_size
        rect_color = (167,209,61)
        for row in range(num_of_cells):
            if row % 2 == 0:
                for col in range(num_of_cells):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * rect_size, row * cell_size, rect_size, rect_size)
                        pygame.draw.rect(self.screen, rect_color, grass_rect)
            else:
                for col in range(num_of_cells):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * rect_size, row * cell_size, rect_size, rect_size)
                        pygame.draw.rect(self.screen, rect_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * num_of_cells - 60)
        score_y = int(cell_size * num_of_cells - 40)

        score_rect = score_surface.get_rect(center=(score_x,score_y))
        apple_rect = self.fruit.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(self.screen, (167, 209, 61), bg_rect)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(self.fruit.apple, apple_rect)
        pygame.draw.rect(self.screen, (56,74,12), bg_rect, 2)

    def game_over(self):
        self.snake.reset()
        self.fruit_randomize()

def game_over():
    pygame.quit()
    sys.exit()

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    clock = pygame.time.Clock()
    framerate = 90

    main_game = GAME()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            if event.type == pygame.USEREVENT:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                main_game.snake.change_direction(event.key)
                if event.key == pygame.K_ESCAPE:
                    game_over()

        # draw all our elements
        main_game.screen.fill(main_game.screen_color)
        main_game.draw_elements()

        pygame.display.update()
        clock.tick(framerate)
