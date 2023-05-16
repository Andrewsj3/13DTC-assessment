"""Version 2: Allow the user to change the stripes on their car
Jack Andrews
16/5/23"""
import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60
LANE_DIST = 118


class Car:
    CAR_Y = 600
    LEFT_BOUND = 123
    RIGHT_BOUND = 477
    cars = {
        "red": 1,
        "green": 2,
        "light blue": 3,
        "copper": 4,
        "purple": 5,
        "cyan": 6
    }

    def __init__(self, img, x):
        self.x = x
        self.stripe = 'n'
        self.col = "red"
        self.car = self.cars[self.col]
        self.img = img

    def draw(self):
        Game.win.blit(self.img, self.img.get_rect(center=[self.x, self.CAR_Y]))

    def move(self, direction):
        if direction == "left":
            if self.x - LANE_DIST >= self.LEFT_BOUND:
                # Bounds checking
                self.x -= LANE_DIST
        elif direction == "right":
            if self.x + LANE_DIST <= self.RIGHT_BOUND:
                self.x += LANE_DIST

    def change_img(self):
        if self.stripe == 'n':
            cars = Game.cars_normal
        elif self.stripe == 'w':
            cars = Game.cars_stripew
        elif self.stripe == 'b':
            cars = Game.cars_stripeb
        self.img = cars[self.car]

    def change_colour(self, col):
        self.col = col
        self.car = self.cars[self.col]
        self.change_img()


class Button:
    colours = {
        "blue": {
            "normal": "blue",
            "hover": "#6E6EEA"
        },
        "red": {
            "normal": "#C90000",
            "hover": "#C74848"
        },
        "green": {
            "normal": "#328632",
            "hover": "#609660"
        },
        "light blue": {
            "normal": "#0068B4",
            "hover": "#367EB3"
        },
        "copper": {
            "normal": "#B66500",
            "hover": "#AD7B39"
        },
        "purple": {
            "normal": "#724E81",
            "hover": "#81668C"
        },
        "cyan": {
            "normal": "#00C8C9",
            "hover": "#59E3E3"
        },
        "black": {
            "normal": "#000000",
            "hover": "#5A5A5A"
        },
        "white": {
            "normal": "white",
            "hover": "#C7B9B9"
        }
    }
    # Many more colours needed for garage menu

    def __init__(self, x, y, width, height, text, fn, txt_col="white",
                 btn_col="blue"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fn = fn
        self.txt_col = txt_col
        self.btn = pygame.Rect((x, y), (width, height))
        self.state = "normal"
        self.btn_col = btn_col
        self._col = self.colours[btn_col][self.state]
        self.is_clicked = False
        # Slight alterations to how Button class works, allowing for button
        # colour to be passed as an argument

    @property
    def col(self):
        return self.colours[self.btn_col][self.state]

    def check_clicked(self):
        mouse_coords = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        focused = pygame.mouse.get_focused()
        if self.btn.collidepoint(mouse_coords) and focused:
            # Button is being hovered over
            self.state = "hover"
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
            self.state = "normal"

    def draw(self):
        pygame.draw.rect(Game.win, self.col, self.btn)
        Game.draw_text(self.text, self.txt_col, (self.btn.centerx,
                                                 self.btn.centery))
        self.check_clicked()


class Game:
    pygame.init()
    icon = pygame.image.load("./assets/game_icon.png")
    font = pygame.font.Font("./assets/PressStart.ttf", 18)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Street Surfers")
    pygame.display.set_icon(icon)
    win.fill("white")
    clock = pygame.time.Clock()

    screen_id = 0
    backgrounds = {i: pygame.image.load(
        f"./assets/backgrounds/bg{i}.png") for i in range(60)}
    cars_normal = {i: pygame.transform.smoothscale(pygame.image.load(
        f"./assets/car_{i}.png"), [80, 135]) for i in range(1, 7)}
    cars_stripew = {i: pygame.transform.smoothscale(pygame.image.load(
        f"./assets/car_{i}_striped_w.png"), [80, 135]) for i in range(1, 7)}
    cars_stripeb = {i: pygame.transform.smoothscale(pygame.image.load(
        f"./assets/car_{i}_striped_b.png"), [80, 135]) for i in range(1, 7)}
    # Loading all the images needed
    car = Car(cars_normal[1], 123 + LANE_DIST)
    transparent_screen = pygame.Surface((WIDTH, HEIGHT))
    transparent_screen.set_alpha(100)
    transparent_screen.fill("white")
    # Setting up a transparent screen so the user can still see what
    # is going on as opposed to making the pause screen completely opaque
    is_paused = False

    def start_game():
        # Resetting the game state
        Game.screen_id = 2
        Game.car.x = 123 + LANE_DIST
        Game.is_paused = False

    start_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2 - 100, 250, 50, "Start",
        start_game)

    how_to_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2, 250, 50, "Instructions",
        lambda: setattr(Game, "screen_id", 1))

    quit_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2 + 200, 250, 50, "Quit", exit)

    menu_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50,
                      "Back To Menu", lambda: setattr(Game, "screen_id", 0))

    resume_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 - 50, 250, 50,
                        "Resume", lambda: setattr(Game, "is_paused", False))

    garage_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50,
                        'Garage', lambda: setattr(Game, "screen_id", 3))

    garage_menu_btn = Button(WIDTH // 2 - 125, HEIGHT - 100, 250, 50,
                             "Back To Menu",
                             lambda: setattr(Game, "screen_id", 0))

    red_btn = Button(30, HEIGHT // 2 + 30, 50, 50, '',
                     lambda: Game.car.change_colour("red"), btn_col="red")
    light_blue_btn = Button(100, HEIGHT // 2 + 30, 50, 50, '',
                            lambda: Game.car.change_colour("light blue"),
                            btn_col="light blue")
    green_btn = Button(30, HEIGHT // 2 + 100, 50, 50, '',
                       lambda: Game.car.change_colour("green"),
                       btn_col="green")
    purple_btn = Button(100, HEIGHT // 2 + 100, 50, 50, '',
                        lambda: Game.car.change_colour("purple"),
                        btn_col="purple")
    copper_btn = Button(30, HEIGHT // 2 + 170, 50, 50, '',
                        lambda: Game.car.change_colour("copper"),
                        btn_col="copper")
    cyan_btn = Button(100, HEIGHT // 2 + 170, 50, 50, '',
                      lambda: Game.car.change_colour("cyan"), btn_col="cyan")
    # These buttons correspond to the colour of the car ingame
    white_stripe_btn = Button(WIDTH - 170, HEIGHT // 2 + 30, 150, 50,
                              "White",
                              lambda: setattr(Game.car, "stripe", 'w')
                              or Game.car.change_img(),
                              btn_col="black")
    black_stripe_btn = Button(WIDTH - 170, HEIGHT // 2 + 100, 150, 50,
                              "Black",
                              lambda: setattr(Game.car, "stripe", 'b')
                              or Game.car.change_img(),
                              "black", "white")
    no_stripe_btn = Button(WIDTH - 170, HEIGHT // 2 + 170, 150, 50, "None",
                           lambda: setattr(Game.car, "stripe", 'n')
                           or Game.car.change_img())

    @classmethod
    def render_main_menu(cls):
        cls.win.fill("white")
        cls.draw_text("Street Surfers", "black", (WIDTH // 2, 100))
        # Greatly simplified rendering function, making it easier to understand
        cls.start_btn.draw()
        cls.how_to_btn.draw()
        cls.quit_btn.draw()
        cls.garage_btn.draw()

    @classmethod
    def render_instructions(cls):
        cls.win.fill("white")
        cls.draw_text("Instructions", "black", (WIDTH // 2, 100))
        cls.draw_text("Controls:", "black", (40, 160), align="left")
        cls.draw_text("Left arrow/A:  Move left",
                      "black", (40, 185), align="left")
        cls.draw_text("Right arrow/D: Move right",
                      "black", (40, 210), align="left")
        cls.draw_text("Escape:        Pause", "black", (40, 235), align="left")
        cls.draw_text("Rules:", "black", (40, 310), align="left")
        cls.draw_text("Avoid the oncoming cars",
                      "black", (40, 335), align="left")
        cls.draw_text("by switching lanes. If you",
                      "black", (40, 360), align="left")
        cls.draw_text("hit a car, you lose.", "black", (40, 385), align="left")
        # Rendering all the text for the instructions

        cls.menu_btn.draw()

    @classmethod
    def draw_text(cls, text, text_col, coords, bg_col=None, align="center"):
        # Helper function that draws text onto the screen at a given location
        # Added align parameter to align text easier
        txt = cls.font.render(text, True, text_col, bg_col)
        if align == "left":
            text_box = txt.get_rect(midleft=coords)
        elif align == "right":
            text_box = txt.get_rect(midright=coords)
        else:
            text_box = txt.get_rect(center=coords)
        cls.win.blit(txt, text_box)

    @classmethod
    def render_screen(cls):
        # This function determines which screen will be drawn
        if cls.screen_id == 0:
            cls.render_main_menu()
        elif cls.screen_id == 1:
            cls.render_instructions()
        elif cls.screen_id == 2:
            cls.render_game()
        elif cls.screen_id == 3:
            cls.render_garage()

    @classmethod
    def render_pause(cls):
        cls.win.blit(cls.transparent_screen, [0, 0])
        cls.draw_text("Paused", "black", (WIDTH // 2, 100))
        cls.menu_btn.draw()
        cls.resume_btn.draw()

    @classmethod
    def render_game(cls, counter=[0]):
        # Keeping an internalised counter so there is no need for global
        # variable
        cls.win.fill("white")
        img = cls.backgrounds[counter[0]]
        cls.win.blit(img, [0, 0])
        cls.car.draw()
        if not cls.is_paused:
            counter[0] += 1
            # We don't want the background 'moving' after we've paused
        else:
            cls.render_pause()
        counter[0] %= 60

    @classmethod
    def render_garage(cls):
        stripes = {'n': "None", 'b': "Black", 'w': "White"}
        cls.win.fill("white")
        cls.draw_text("Car Customization", "black", [WIDTH // 2, 100])
        cls.draw_text("Paint", "black", [30, HEIGHT // 2], align="left")
        cls.draw_text(
            "Stripes", "black", [
                WIDTH - 30, HEIGHT // 2], align="right")
        cls.draw_text(
            f"{Game.car.col.capitalize()}", "black", [
                30, HEIGHT // 2 - 50], align="left")
        cls.draw_text(f"{stripes[Game.car.stripe]}", "black", [
                      WIDTH - 30, HEIGHT // 2 - 50], align="right")
        cls.red_btn.draw()
        cls.light_blue_btn.draw()
        cls.green_btn.draw()
        cls.purple_btn.draw()
        cls.copper_btn.draw()
        cls.cyan_btn.draw()
        cls.white_stripe_btn.draw()
        cls.black_stripe_btn.draw()
        cls.no_stripe_btn.draw()
        cls.garage_menu_btn.draw()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if Game.screen_id == 2:
                        # Checking that we are not in a menu
                        Game.is_paused = Game.is_paused ^ True
                        # Can also unpause by pressing escape again
                if Game.is_paused:
                    continue
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    Game.car.move("right")
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    Game.car.move("left")

        Game.render_screen()
        pygame.display.update()
        Game.clock.tick(FPS)


if __name__ == "__main__":
    main()
