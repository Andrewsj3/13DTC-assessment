"""v1: Continuously cycle through background images, 
creating an infinite scrolling effect
Jack Andrews
4/05/2023
"""
import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60


def draw_game(backgrounds, counter=[0]):
    # Keeping an internalised counter so there is no need for global variable
    win.fill("white")
    img = backgrounds[counter[0] % 30]
    print(f"Loaded background {counter[0]}")
    win.blit(img, img.get_rect())
    counter[0] += 1
    counter[0] %= 30


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
backgrounds = {i: pygame.image.load(
    f"./assets/backgrounds/bg{i}.png") for i in range(30)}
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    draw_game(backgrounds)
    pygame.display.update()
    clock.tick(FPS)
