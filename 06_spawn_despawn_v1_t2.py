"""v2: First version of spawning and despawning cars
Now uses a custom-defined Queue class to keep track of cars
Jack Andrews
7/05/2023
"""
import pygame
import random
WIDTH = 600
HEIGHT = 700
FPS = 60
LANE_DIST = 118
# Distance the car will move when switching lanes


class EnemyCar:
    # Enemy cars need to behave differently to the player car
    #    CAR_Y = 600
    # Opposing cars will not have a fixed y position

    def __init__(self, img, x):
        self.img = img
        self.x = x
        self.y = -140
        # Drawing car off screen so it doesn't pop into view suddenly
        self.speed = random.randint(6, 9)

    def draw(self):
        win.blit(self.img, self.img.get_rect(midtop=[self.x, self.y]))

    def update(self):
        self.y += self.speed


class Queue:
    # Data structure to keep track of cars
    def __init__(self, queue, max_size):
        self._queue: list = queue
        self._max_size = max_size
        # Allows us to specify a max size for our queue, which you can't do
        # with a list

    def queue(self, item, force=True):
        if len(self) < self._max_size:
            self._queue.append(item)
        elif force:
            # Gets rid of the first item to make room
            self.dequeue()
            self.queue(item)

    def dequeue(self):
        if len(self):
            # Avoiding IndexError
            self._queue.pop(0)

    def apply(self, fn):
        # Used to call the cars' `update` and `draw` methods
        for item in self:
            fn(item)

    def __len__(self):
        # So we can use len(self)
        return len(self._queue)

    def __iter__(self):
        self.i = 0
        self.len = len(self)
        return self

    def __next__(self):
        # Allows us to do for ... in queue:
        if self.i < self.len:
            self.i += 1
            return self._queue[self.i - 1]
        else:
            raise StopIteration


def draw_game(counter=[0]):
    # Keeping an internalised counter so there is no need for global variable
    global car_queue
    win.fill("white")
    img = backgrounds[counter[0]]
    win.blit(img, img.get_rect())
    car_queue.apply(EnemyCar.update)
    car_queue.apply(EnemyCar.draw)
    counter[0] += 1
    counter[0] %= 60


def spawn_cars():
    global ms_elapsed, prev_lane
    lane = prev_lane
    if ms_elapsed // 100 >= 6:
        # Now we don't have to check the length of our queue manually
        while lane == prev_lane:
            # Prevents this car from being in the same lane as the previous one
            lane = random.randint(0, 3)
        prev_lane = lane
        car_queue.queue(
            EnemyCar(cars[random.randint(0, 5)],
                     123 + LANE_DIST * lane))
        ms_elapsed = 0


pygame.init()
car_queue = Queue([], 4)
prev_lane = -1
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
cars = {i - 1:
        pygame.transform.flip(
            pygame.transform.smoothscale(
                pygame.image.load(f"./assets/car_{i}.png"),
                [80, 135]), False, True) for i in range(1, 7)}
backgrounds = {i: pygame.image.load(
    f"./assets/backgrounds/bg{i}.png") for i in range(60)}
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
clock = pygame.time.Clock()
ms_elapsed = -1 / FPS * 1000
# Timer used to determine when cars should spawn
while True:
    spawn_cars()
    ms_elapsed += 1 / FPS * 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    draw_game()
    pygame.display.update()
    clock.tick(FPS)
