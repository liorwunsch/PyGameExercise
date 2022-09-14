import pygame, sys, enum, random
from pygame.math import Vector2

class Suit(enum.Enum):
    Hearts = 1
    Clubs = 2
    Diamonds = 3
    Spades = 4

    def __str__(self):
        return str(self.name)

class Value(enum.IntEnum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

    def __str__(self):
        return str(self.name)

class Card(object):
    def __init__(self, suit: Suit, value: Value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

def game_over():
    pygame.quit()
    sys.exit()

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    clock = pygame.time.Clock()
    fps = 120

    main_game = "GAME()"

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
        clock.tick(fps)

card = Card(Suit.Hearts, Value.Jack)
print(card)
