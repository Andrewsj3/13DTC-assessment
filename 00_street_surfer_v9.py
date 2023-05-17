"""Version 9: Integrate car customization into main game + Add 'New Best'
text when user beats their highscore
Jack Andrews
17/5/23"""
import pygame
import random
WIDTH = 600
HEIGHT = 700
FPS = 60
START_X = 241
LANE_DIST = 118
IMG_WIDTH = 80
IMG_HEIGHT = 135


class Car:
    CAR_Y = 600
    LEFT_BOUND = 121
    RIGHT_BOUND = 481
    cars = {
        "red": 1,
        "green": 2,
        "light blue": 3,
        "copper": 4,
        "purple": 5,
        "cyan": 6
    }
    # This maps the colours to the actual cars, e.g. car_1.png is red,
    # car_2.png is green, etc.

    def __init__(self, img, x):
        self.img_f = img
        self.img_l = pygame.transform.rotate(img, 30)
        self.img_r = pygame.transform.rotate(img, -30)
        # Need separate images for when the car is rotating
        self.mask_f = pygame.mask.from_surface(self.img_f)
        self.mask_l = pygame.mask.from_surface(self.img_l)
        self.mask_r = pygame.mask.from_surface(self.img_r)
        self.col = "red"
        self.stripe = 'n'
        self.car = self.cars[self.col]
        self.x = x
        self.dir = "forward"

    def draw(self):
        imgs = {"forward": self.img_f, "left": self.img_l, "right": self.img_r}
        Game.win.blit(imgs[self.dir], imgs[self.dir].get_rect(
            center=[self.x, self.CAR_Y]))

    def move(self, direction):
        if direction == "left":
            if self.x - 10 >= self.LEFT_BOUND:
                # Bounds checking
                self.x -= 10
                self.dir = direction
            else:
                self.dir = "forward"
        elif direction == "right":
            if self.x + 10 <= self.RIGHT_BOUND:
                self.x += 10
                self.dir = direction
            else:
                self.dir = "forward"

    def collide(self):
        masks = {
            "forward": self.mask_f,
            "left": self.mask_l,
            "right": self.mask_r}
        p_car = masks[self.dir]
        for enemy in Game.car_queue:
            e_car = enemy.mask
            y_offset = IMG_HEIGHT // 2
            x_offset = 28 if p_car != self.mask_f else 0
            # Needed because the y positions are measured differently for
            # player and enemy cars
            # Due to size differences in the masks, x_offset is also needed
            offset = (enemy.x - self.x + x_offset, enemy.y + y_offset -
                      self.CAR_Y)
            if p_car.overlap(e_car, offset):
                return True

    def change_img(self):
        if self.stripe == 'n':
            cars = Game.cars_normal
        elif self.stripe == 'w':
            cars = Game.cars_stripew
        elif self.stripe == 'b':
            cars = Game.cars_stripeb
        self.img_f = cars[self.car]
        self.img_l = pygame.transform.rotate(self.img_f, 30)
        self.img_r = pygame.transform.rotate(self.img_f, -30)
        # After changing the colour/stripe, the images need to be updated

    def change_colour(self, col):
        self.col = col
        self.car = self.cars[self.col]
        self.change_img()


class EnemyCar:
    # Enemy cars need to behave differently to the player car
    # Opposing cars will not have a fixed y position

    def __init__(self, img, x):
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.x = x
        self.y = -140
        # Drawing car off screen so it doesn't pop into view suddenly
        self.speed = random.randint(6, 9)
        self._ignore = False

    def draw(self):
        Game.win.blit(self.img, self.img.get_rect(midtop=[self.x, self.y]))

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT and not self._ignore:
            # _ignore makes it so it will only be activated once
            Game.score += 1
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
        self.len = len(self)
        return self

    def __next__(self):
        # Allows us to do for ... in queue:
        if self.i < self.len:
            self.i += 1
            return self._queue[self.i - 1]
        else:
            raise StopIteration


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
        "white": {
            "normal": "white",
            "hover": "#C7B9B9"
        }
    }
    # Garage component required a lot of colours, hence this dictionary being
    # so big

    def __init__(self, x, y, width, height, text, fn, txt_col="white",
                 btn_col="blue"):
        # Now allows button colour to be passed as a parameter
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fn = fn
        self.state = "normal"
        self.btn_col = btn_col
        self.txt_col = txt_col
        self.btn = pygame.Rect((x, y), (width, height))
        self.is_clicked = False

    @property
    def col(self):
        # Need to make this a property because state changes often
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
    MAIN_MENU_ID = 0
    INSTRUCTIONS_ID = 1
    GAME_ID = 2
    GARAGE_ID = 3
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
    cars = {i: pygame.transform.flip(
            pygame.transform.smoothscale(
                pygame.image.load(f"./assets/car_{i}.png"),
                [IMG_WIDTH, IMG_HEIGHT]), False, True) for i in range(1, 7)}
    # This is for the ai cars
    cars_normal = {i: pygame.transform.smoothscale(pygame.image.load(
        f"./assets/car_{i}.png"), [IMG_WIDTH, IMG_HEIGHT])
        for i in range(1, 7)}
    cars_stripew = {i: pygame.transform.smoothscale(pygame.image.load(
        f"./assets/car_{i}_striped_w.png"), [IMG_WIDTH, IMG_HEIGHT])
        for i in range(1, 7)}
    cars_stripeb = {i: pygame.transform.smoothscale(pygame.image.load(
        f"./assets/car_{i}_striped_b.png"), [IMG_WIDTH, IMG_HEIGHT])
        for i in range(1, 7)}
    # Loading all the images needed for the player

    car = Car(cars_normal[1], START_X)
    car_queue = Queue([], 4)

    transparent_screen = pygame.Surface((WIDTH, HEIGHT))
    transparent_screen.set_alpha(100)
    transparent_screen.fill("white")
    # Setting up a transparent screen so the user can still see what
    # is going on as opposed to making the pause screen completely opaque
    is_paused = is_dead = False
    prev_lane = -1
    ms_elapsed = 0
    score = 0
    is_focused = True

    @staticmethod
    def start_game():
        # Resetting the game state, and saving/loading highscore if necessary
        Game.save_high_score("highscore.txt", Game.score)
        Game.high_score = load_high_score("highscore.txt")
        Game.screen_id = Game.GAME_ID
        Game.car.x = START_X
        Game.is_paused = Game.is_dead = False
        Game.car_queue._queue.clear()
        Game.score = 0

    @staticmethod
    def save_high_score(fpath, score, stop=False):
        # These functions would normally be defined after the variables, but
        # that won't work in this case as the buttons need to have a reference
        # to these functions
        if Game.is_new_best():
            with open(fpath, 'w') as f:
                f.write(str(score))
        if stop:
            pygame.quit()
            exit()

    start_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2 - 100, 250, 50, "Start",
        start_game)

    how_to_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2, 250, 50, "Instructions",
        lambda: setattr(Game, "screen_id", Game.INSTRUCTIONS_ID))

    quit_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 + 200, 250, 50, "Quit",
                      lambda: Game.save_high_score(
                          "highscore.txt", Game.score, stop=True))

    menu_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50,
                      "Back To Menu",
                      lambda: setattr(Game, "screen_id", Game.MAIN_MENU_ID))

    resume_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 - 50, 250, 50,
                        "Resume", lambda: setattr(Game, "is_paused", False))

    restart_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 - 50, 250, 50,
                         "Restart", start_game)
    garage_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50,
                        'Garage', lambda: setattr(Game, "screen_id", 3))

    garage_menu_btn = Button(WIDTH // 2 - 125, HEIGHT - 100, 250, 50,
                             "Back To Menu",
                             lambda: setattr(Game, "screen_id", 0))
    # Need a different menu button as the other one is too high up

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
                              or Game.car.change_img(), "black",
                              "white")
    black_stripe_btn = Button(WIDTH - 170, HEIGHT // 2 + 100, 150, 50,
                              "Black",
                              lambda: setattr(Game.car, "stripe", 'b')
                              or Game.car.change_img(),
                              "black", "white")
    no_stripe_btn = Button(WIDTH - 170, HEIGHT // 2 + 170, 150, 50, "None",
                           lambda: setattr(Game.car, "stripe", 'n')
                           or Game.car.change_img(), "black", "white")
    # These buttons control what kind of stripes the car has
    high_score = "\n\n\n"

    @classmethod
    def render_main_menu(cls):
        cls.win.fill("white")
        cls.draw_text("Street Surfers", "black", (WIDTH // 2, 100))
        cls.start_btn.draw()
        cls.how_to_btn.draw()
        cls.garage_btn.draw()
        cls.quit_btn.draw()

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
        if cls.screen_id == cls.MAIN_MENU_ID:
            cls.render_main_menu()
        elif cls.screen_id == cls.INSTRUCTIONS_ID:
            cls.render_instructions()
        elif cls.screen_id == cls.GAME_ID:
            cls.render_game()
        elif cls.screen_id == cls.GARAGE_ID:
            cls.render_garage()

    @classmethod
    def render_pause(cls):
        cls.win.blit(cls.transparent_screen, [0, 0])
        cls.draw_text("Paused", "black", (WIDTH // 2, 100))
        cls.menu_btn.draw()
        cls.resume_btn.draw()

    @classmethod
    def render_game(cls, counter=[0]):
        cls.win.fill("white")
        img = cls.backgrounds[counter[0]]
        cls.win.blit(img, [0, 0])
        cls.is_dead = cls.car.collide()
        cls.car_queue.apply(EnemyCar.draw)
        cls.car.draw()
        is_new_best = cls.is_new_best()
        cls.draw_text(
            f"Score: {cls.score}", "black", [
                WIDTH - 80, 50], align="right")
        cls.draw_text(
            f"Best: {cls.high_score}", "black", [
                80, 50], align="left")
        if is_new_best:
            cls.draw_text("New Best!", "black", [WIDTH // 2, 80])
            # Lets the user know they have a new high score

        if not (cls.is_paused or cls.is_dead):
            cls.car_queue.apply(EnemyCar.update)
            counter[0] += 1
            # We don't want the background 'moving' after we've paused
        elif cls.is_paused:
            cls.render_pause()
        elif cls.is_dead:
            cls.render_death()
        counter[0] %= 60

    @classmethod
    def render_death(cls):
        cls.win.blit(cls.transparent_screen, [0, 0])
        cls.draw_text("You died!", "black", (WIDTH // 2, 100))
        cls.menu_btn.draw()
        cls.restart_btn.draw()

    @classmethod
    def render_garage(cls):
        width, height = Game.car.img_f.get_width(), Game.car.img_f.get_height()
        preview_window = pygame.transform.smoothscale(
            Game.car.img_f, [width * 1.3, height * 1.3])
        # This 'window' is simply what the user's car looks like with their
        # current settings. Any changes made in this menu are immediately
        # reflected
        stripes = {'n': "No", 'b': "Black", 'w': "White"}
        # Controls how the different stripes are represented, e.g. n means no
        # stripe, w means white stripe, etc.
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
        # Letting the user know what paint and what stripes they have on their
        # car
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
        cls.win.blit(preview_window, preview_window.get_rect(center=[
            WIDTH // 2, 250]))

    @classmethod
    def spawn_cars(cls):
        lane = cls.prev_lane
        if cls.ms_elapsed // 100 >= 6 and not (cls.is_dead or cls.is_paused):
            # Now we don't have to check the length of our queue manually
            # But we do have to check if the game is paused or if we have
            # crashed
            while lane == cls.prev_lane:
                # Prevents this car from being in the same lane as the previous
                # one
                lane = random.randint(0, 3)
            choices = [i for i in range(1, 7) if i != Car.cars[Game.car.col]]
            # Preventing ai from having the same colour as the player in order
            # to help differentiate the ai cars from the player
            cls.prev_lane = lane
            cls.car_queue.queue(
                EnemyCar(cls.cars[random.choice(choices)],
                         123 + LANE_DIST * lane))
            cls.ms_elapsed = 0

    @classmethod
    def is_new_best(cls):
        # Logic that checks if we should save the current score as the
        # highscore
        if cls.high_score != "\n\n\n":
            if cls.score > cls.high_score:
                return True
        elif cls.score > 0:
            return True
        return False


def load_high_score(fpath):
    try:
        with open(fpath) as f:
            return int(f.read())
    except (ValueError, FileNotFoundError):
        return '\n\n\n'
        # Pygame will render these as question marks, which signifies that
        # there is no value for the highscore


def main():
    while True:
        Game.ms_elapsed += 1 / FPS * 1000 * (Game.is_paused ^ True)
        # Time only increases if game is not paused
        Game.spawn_cars()
        keys = pygame.key.get_pressed()
        # Gets all keys currently being pressed, as opposed to pygame.KEYDOWN
        # which does not get keys that are held down
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.save_high_score("highscore.txt", Game.score, stop=True)
            elif event.type == pygame.WINDOWFOCUSLOST and not Game.is_dead:
                # Fixed bug where pause screen would be drawn on top of death
                # screen
                Game.is_paused = True
            elif event.type == pygame.WINDOWFOCUSGAINED:
                for button in (Game.resume_btn, Game.menu_btn):
                    if button.btn.collidepoint(pygame.mouse.get_pos()):
                        button.fn()
                        # Fixes bug where buttons would have to be clicked
                        # twice to work after window had lost focus, although
                        # this is slightly hacky
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if Game.screen_id == Game.GAME_ID and not Game.is_dead:
                        # Checking that we are not in a menu
                        Game.is_paused = Game.is_paused ^ True
                        # Can also unpause by pressing escape again
                if event.key == pygame.K_SPACE:
                    if Game.screen_id == Game.GAME_ID and Game.is_dead:
                        Game.start_game()
        if not (Game.is_paused or Game.is_dead):
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                Game.car.move("right")
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                Game.car.move("left")
            else:
                Game.car.dir = "forward"

        Game.render_screen()
        pygame.display.update()
        Game.clock.tick(FPS)


if __name__ == "__main__":
    main()
