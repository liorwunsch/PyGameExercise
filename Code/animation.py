import pygame, sys

class Frog(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('Animation/attack_1.png'))
        self.sprites.append(pygame.image.load('Animation/attack_2.png'))
        self.sprites.append(pygame.image.load('Animation/attack_3.png'))
        self.sprites.append(pygame.image.load('Animation/attack_4.png'))
        self.sprites.append(pygame.image.load('Animation/attack_5.png'))
        self.sprites.append(pygame.image.load('Animation/attack_6.png'))
        self.sprites.append(pygame.image.load('Animation/attack_7.png'))
        self.sprites.append(pygame.image.load('Animation/attack_8.png'))
        self.sprites.append(pygame.image.load('Animation/attack_9.png'))
        self.sprites.append(pygame.image.load('Animation/attack_10.png'))

        self.current_sprite = 0
        self.update_image()

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
        self.is_animating = False

    def update_image(self):
        self.image = pygame.transform.scale(self.sprites[int(self.current_sprite)], (512, 256))

    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if not self.is_animating:
            return
        self.current_sprite += speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            self.is_animating = False
        self.update_image()

def game_over():
    pygame.quit()
    sys.exit()

# General Setup
pygame.init()
clock = pygame.time.Clock()
fps = 120

# Game Screen
screen_width = 400; screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
frog = Frog(10, 10)
moving_sprites.add(frog)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        if event.type == pygame.KEYDOWN:
            frog.animate()
            if event.key == pygame.K_ESCAPE:
                game_over()

    # Drawing
    screen.fill((0,0,0))
    moving_sprites.draw(screen)
    moving_sprites.update(0.25)
    pygame.display.update()
    clock.tick(fps)
