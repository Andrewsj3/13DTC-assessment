"""Trial 2: Use car class and move the 'move' function into the car class
Jack Andrews
5/05/2023
"""
import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60
LANE_DIST = 118
# Distance the car will move when switching lanes


class Car:
    CAR_Y = 600
    LEFT_BOUND = 123
    RIGHT_BOUND = 477

    def __init__(self, img, x):
        self.img = img
        self.x = x

    def draw(self):
        win.blit(self.img, self.img.get_rect(center=[self.x, self.CAR_Y]))

    def move(self, direction):
        if direction == "left":
            if self.x - LANE_DIST >= self.LEFT_BOUND:
                # Bounds checking
                cur_lane = self.x // LANE_DIST
                self.x -= LANE_DIST
                new_lane = self.x // LANE_DIST
#                print(f"Lane {cur_lane} < Lane {new_lane}")
#            else:
                #                print("Can't move left")
        elif direction == "right":
            if self.x + LANE_DIST <= self.RIGHT_BOUND:
                cur_lane = self.x // LANE_DIST
                self.x += LANE_DIST
                new_lane = self.x // LANE_DIST
#                print(f"Lane {cur_lane} > Lane {new_lane}")
#            else:
                #                print("Can't move right")


def draw_game(backgrounds, counter=[0]):
    # Keeping an internalised counter so there is no need for global variable
    win.fill("white")
    img = backgrounds[counter[0] % 30]
    win.blit(img, img.get_rect())
    car.draw()
    counter[0] += 1
    counter[0] %= 30


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
car_img = pygame.image.load("./assets/car_1.png")
car_img = pygame.transform.smoothscale(car_img, [80, 135])
backgrounds = {i: pygame.image.load(
    f"./assets/backgrounds/bg{i}.png") for i in range(30)}
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
clock = pygame.time.Clock()
car = Car(car_img, 123 + LANE_DIST)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                car.move("right")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                car.move("left")
    draw_game(backgrounds)
    pygame.display.update()
    clock.tick(FPS)
