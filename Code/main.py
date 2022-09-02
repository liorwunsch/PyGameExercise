import snake
import pygame

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    clock = pygame.time.Clock()
    fps = 120

    main_game = snake.GAME()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snake.game_over()
            if event.type == pygame.USEREVENT:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                main_game.snake.change_direction(event.key)
                if event.key == pygame.K_ESCAPE:
                    snake.game_over()

        # draw all our elements
        main_game.screen.fill(main_game.screen_color)
        main_game.draw_elements()

        pygame.display.update()
        clock.tick(fps)

main()
