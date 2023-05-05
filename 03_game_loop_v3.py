"""v3: Integrate car movement with game loop
Jack Andrews
6/05/2023
"""
import pygame
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


def draw_game(backgrounds, counter=[0], is_paused=False):
    # Keeping an internalised counter so there is no need for global variable
    win.fill("white")
    img = backgrounds[counter[0]]
    win.blit(img, [0, 0])
    car.draw()
    if not is_paused:
        counter[0] += 1
        # We don't want the background 'moving' after we've paused
    else:
        render_pause()
    counter[0] %= 30


def unpause():
    global is_paused
    is_paused = False


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
car = Car(car_img, 123 + LANE_DIST)
transparent_screen = pygame.Surface((WIDTH, HEIGHT))
transparent_screen.set_alpha(100)
transparent_screen.fill("white")
# Setting up a transparent screen so the user can still see what is going on
# as opposed to making the pause screen completely opaque
is_paused = False
clock = pygame.time.Clock()
menu = Button(WIDTH // 2 - 125, HEIGHT // 2 + 50, 250, 50,
              "Back To Menu", lambda: print("Main Menu"))
resume = Button(WIDTH // 2 - 125, HEIGHT // 2 - 50, 250, 50,
                "Resume", unpause)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = True
            if is_paused:
                continue
            # We don't want the car moving
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                car.move("right")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                car.move("left")
    draw_game(backgrounds, is_paused=is_paused)
    pygame.display.update()
    clock.tick(FPS)
