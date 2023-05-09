"""v2: Add saving and loading of high_score
Jack Andrews
9/05/2023
"""
import pygame
import random
WIDTH = 600
HEIGHT = 700
FPS = 60
LANE_DIST = 118


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
        elif direction == "right":
            if self.x + LANE_DIST <= self.RIGHT_BOUND:
                cur_lane = self.x // LANE_DIST
                self.x += LANE_DIST
                new_lane = self.x // LANE_DIST

    def collide(self):
        possible_contacts = [car for car in car_queue if car.x == self.x]
        # Only getting the cars that are in the same lane as the player
        p_car = self.img.get_rect(center=[self.x, self.CAR_Y])
        for enemy in possible_contacts:
            e_car = enemy.img.get_rect(midtop=[enemy.x, enemy.y])
            if p_car.colliderect(e_car):
                return True


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
        self._ignore = False

    def draw(self):
        win.blit(self.img, self.img.get_rect(midtop=[self.x, self.y]))

    def update(self):
        global score
        self.y += self.speed
        if self.y > HEIGHT and not self._ignore:
            score += 1
            # Makes sure the score only increases once instead of every frame
            self._ignore = True


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
        return self

    def __next__(self):
        # Allows us to do for ... in queue:
        self.len = len(self)
        if self.i < self.len:
            self.i += 1
            return self._queue[self.i - 1]
        else:
            raise StopIteration


class Button:
    # Copying button class from main menu component
    colours = {
        "normal": "blue",
        "hover": "#6E6EEA",
    }
    # This controls the colour of the buttons

    def __init__(self, x, y, width, height, text, fn):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fn = fn
        self.btn = pygame.Rect((x, y), (width, height))
        self.col = self.colours["normal"]
        self.is_clicked = False

    def check_clicked(self):
        mouse_coords = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        focused = pygame.mouse.get_focused()
        if self.btn.collidepoint(mouse_coords) and focused:
            # Button is being hovered over
            self.col = self.colours["hover"]
            if pressed:
                if not self.is_clicked:
                    # Makes it so the function can only be executed once per
                    # click
                    self.fn()
                    self.is_clicked = True
            else:
                self.is_clicked = False
        else:
            self.is_clicked = True
            # Fixes bug where user can activate button by holding and
            # navigating to button instead of clicking it directly
            self.col = self.colours["normal"]

    def draw(self):
        pygame.draw.rect(win, self.col, self.btn)
        draw_text(self.text, "white", (self.btn.centerx, self.btn.centery))
        self.check_clicked()


def draw_text(text, text_col, coords, bg_col=None, align="center"):
    # Helper function that draws text onto the screen at a given location
    # Added align parameter to align text easier
    txt = font.render(text, True, text_col, bg_col)
    if align == "left":
        text_box = txt.get_rect(midleft=coords)
    elif align == "right":
        text_box = txt.get_rect(midright=coords)
    else:
        text_box = txt.get_rect(center=coords)
    win.blit(txt, text_box)


def render_pause():
    win.blit(transparent_screen, [0, 0])
    draw_text("Paused", "black", (WIDTH // 2, 100))
    menu.draw()
    resume.draw()


def render_death():
    win.blit(transparent_screen, [0, 0])
    draw_text("You died!", "black", (WIDTH // 2, 100))
    menu.draw()
    restart.draw()


def render_game(counter=[0], is_paused=False):
    global is_dead
    # Keeping an internalised counter so there is no need for global variable
    win.fill("white")
    img = backgrounds[counter[0]]
    win.blit(img, [0, 0])
    if car.collide():
        is_dead = True
    car.draw()
    car_queue.apply(EnemyCar.draw)
    draw_text(f"Score: {score}", "black", [WIDTH - 80, 50], align="right")
    draw_text(f"Best: {highscore}", "black", [80, 50], align="left")
    # Right align to ensure the text never goes offscreen
    if not (is_paused | is_dead):
        car_queue.apply(EnemyCar.update)
        counter[0] += 1
        # We don't want the background 'moving' after we've paused
    elif is_paused:
        render_pause()
    elif is_dead:
        render_death()
    counter[0] %= 60


def unpause():
    global is_paused
    is_paused = False


def restart_game():
    global car_queue, car, is_dead, score, highscore
    if score != 0 and highscore == "\n\n\n":
        save_high_score("highscore.txt")
    elif score > highscore:
        save_high_score("highscore.txt")
    car.x = 123 + LANE_DIST
    car_queue = Queue([], 4)
    is_dead = False
    score = 0
    highscore = load_high_score("highscore.txt")


def spawn_cars():
    global ms_elapsed, prev_lane
    lane = prev_lane
    if ms_elapsed // 100 >= 6 and not (is_dead | is_paused):
        # Now we don't have to check the length of our queue manually
        # But we do have to check if the game is paused or if we have crashed
        while lane == prev_lane:
            # Prevents this car from being in the same lane as the previous one
            lane = random.randint(0, 3)
        prev_lane = lane
        car_queue.queue(
            EnemyCar(cars[random.randint(1, 5)],
                     123 + LANE_DIST * lane))
        ms_elapsed = 0


def save_high_score(fpath):
    with open(fpath, 'w') as f:
        f.write(str(score))


def load_high_score(fpath):
    try:
        with open(fpath) as f:
            return int(f.read())
    except (ValueError, FileNotFoundError):
        return '\n\n\n'
        # Pygame will render these as question marks, which signifies that
        # there is no value for the highscore


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
car_img = pygame.image.load("./assets/car_1.png")
car_img = pygame.transform.smoothscale(car_img, [80, 135])
backgrounds = {i: pygame.image.load(
    f"./assets/backgrounds/bg{i}.png") for i in range(60)}
cars = {i - 1:
        pygame.transform.flip(
            pygame.transform.smoothscale(
                pygame.image.load(f"./assets/car_{i}.png"),
                [80, 135]), False, True) for i in range(2, 7)}
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
car = Car(car_img, 123 + LANE_DIST)
transparent_screen = pygame.Surface((WIDTH, HEIGHT))
transparent_screen.set_alpha(100)
transparent_screen.fill("white")
# Setting up a transparent screen so the user can still see what is going on
# as opposed to making the pause screen completely opaque
is_paused = is_dead = False
clock = pygame.time.Clock()
car_queue = Queue([], 4)
prev_lane = -1
menu = Button(WIDTH // 2 - 125, HEIGHT // 2 + 50, 250, 50,
              "Back To Menu", lambda: print("Main Menu"))
resume = Button(WIDTH // 2 - 125, HEIGHT // 2 - 50, 250, 50,
                "Resume", unpause)
restart = Button(WIDTH // 2 - 125, HEIGHT // 2 - 50, 250, 50,
                 "Restart", restart_game)
ms_elapsed = 0
score = 0
highscore = load_high_score("highscore.txt")
while True:
    ms_elapsed += 1 / FPS * 1000 * (is_paused ^ True)
    # Prevents counter from going up if game is paused
    spawn_cars()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score != 0 and highscore == "\n\n\n":
                save_high_score("highscore.txt")
            elif score > highscore:
                save_high_score("highscore.txt")
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not is_dead:
                is_paused = True
            if is_paused | is_dead:
                continue
            # We don't want the car moving
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                car.move("right")
                break
            # Fix exploit where you could move two lanes in a single frame
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                car.move("left")
                break
    render_game(is_paused=is_paused)
    pygame.display.update()
    clock.tick(FPS)
