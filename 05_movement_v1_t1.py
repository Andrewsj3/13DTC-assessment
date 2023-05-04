"""v1: First version of movement component that lets the car move
between the four lanes
Jack Andrews
5/05/2023
"""
import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60
LANE_DIST = 118
# Distance the car will move when switching lanes
CAR_Y = 575
LEFT_BOUND = 123
RIGHT_BOUND = 477


def draw_game(backgrounds, counter=[0]):
    # Keeping an internalised counter so there is no need for global variable
    win.fill("white")
    img = backgrounds[counter[0] % 30]
    win.blit(img, img.get_rect())
    win.blit(car, car.get_rect(center=[car_x, CAR_Y]))
    counter[0] += 1
    counter[0] %= 30


def move_car(direction):
    global car_x
    if direction == "left":
        if car_x - LANE_DIST < LEFT_BOUND:
            return
        car_x -= LANE_DIST
    elif direction == "right":
        if car_x + LANE_DIST > RIGHT_BOUND:
            return
        car_x += LANE_DIST


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
car = pygame.image.load("./assets/car_1.png")
car = pygame.transform.smoothscale(car, [80, 135])
backgrounds = {i: pygame.image.load(
    f"./assets/backgrounds/bg{i}.png") for i in range(30)}
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
clock = pygame.time.Clock()
car_x = 123 + LANE_DIST
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                move_car("right")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                move_car("left")
    draw_game(backgrounds)
    pygame.display.update()
    clock.tick(FPS)
