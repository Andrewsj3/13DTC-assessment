import pygame
WIDTH = 600
HEIGHT = 800
pygame.init()
icon = pygame.image.load("./assets/game_icon.png")

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfer")
pygame.display.set_icon(icon)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
