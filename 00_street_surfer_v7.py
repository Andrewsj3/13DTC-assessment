"""Version 7: Integrate scoring into main program + Qol improvements
First version of complete game
Jack Andrews
13/5/23"""
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
        Game.win.blit(self.img, self.img.get_rect(center=[self.x, self.CAR_Y]))

    def move(self, direction):
        if direction == "left":
            if self.x - LANE_DIST >= self.LEFT_BOUND:
                # Bounds checking
                self.x -= LANE_DIST
        elif direction == "right":
            if self.x + LANE_DIST <= self.RIGHT_BOUND:
                self.x += LANE_DIST

    def collide(self):
        possible_contacts = [car for car in Game.car_queue if car.x == self.x]
        # Only getting the cars that are in the same lane as the player
        p_car = self.img.get_rect(center=[self.x, self.CAR_Y])
        for enemy in possible_contacts:
            e_car = enemy.img.get_rect(midtop=[enemy.x, enemy.y])
            return p_car.colliderect(e_car)


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
        "normal": "blue",
        "hover": "#6E6EEA",
    }
    # This controls the colour of the buttons

    def __init__(self, x, y, width, height, text, fn, txt_col="white"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fn = fn
        self.txt_col = txt_col
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
        pygame.draw.rect(Game.win, self.col, self.btn)
        Game.draw_text(self.text, self.txt_col, (self.btn.centerx,
                                                 self.btn.centery))
        self.check_clicked()


class Game:
    MAIN_MENU_ID = 0
    INSTRUCTIONS_ID = 1
    GAME_ID = 2
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
    cars = {i - 1:
            pygame.transform.flip(
                pygame.transform.smoothscale(
                    pygame.image.load(f"./assets/car_{i}.png"),
                    [80, 135]), False, True) for i in range(2, 7)}

    car_img = pygame.image.load("./assets/car_1.png")
    car_img = pygame.transform.smoothscale(car_img, [80, 135])
    car = Car(car_img, 123 + LANE_DIST)
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
        # Resetting the game state
        Game.save_high_score("highscore.txt", Game.score)
        Game.high_score = load_high_score("highscore.txt")
        Game.screen_id = Game.GAME_ID
        Game.car.x = 123 + LANE_DIST
        Game.is_paused = Game.is_dead = False
        Game.car_queue._queue.clear()
        Game.score = 0

    @staticmethod
    def save_high_score(fpath, score, stop=False):
        # These functions would normally be defined after the variables, but
        # that won't work in this case
        if Game.high_score != "\n\n\n":
            if Game.score > Game.high_score:
                with open(fpath, 'w') as f:
                    f.write(str(score))
        elif Game.score > 0:
            with open(fpath, 'w') as f:
                f.write(str(score))
        if stop:
            pygame.quit()
            exit()

    start_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2, 250, 50, "Start",
        start_game)

    how_to_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50, "Instructions",
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
    high_score = "\n\n\n"

    @classmethod
    def render_main_menu(cls):
        cls.win.fill("white")
        cls.draw_text("Street Surfers", "black", (WIDTH // 2, 100))
        cls.start_btn.draw()
        cls.how_to_btn.draw()
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
        if cls.car.collide():
            cls.is_dead = True
        cls.car_queue.apply(EnemyCar.draw)
        cls.car.draw()
        cls.draw_text(
            f"Score: {cls.score}", "black", [
                WIDTH - 80, 50], align="right")
        cls.draw_text(
            f"Best: {cls.high_score}", "black", [
                80, 50], align="left")
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
            cls.prev_lane = lane
            cls.car_queue.queue(
                EnemyCar(cls.cars[random.randint(1, 5)],
                         123 + LANE_DIST * lane))
            cls.ms_elapsed = 0


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.save_high_score("highscore.txt", Game.score, stop=True)
            elif event.type == pygame.WINDOWFOCUSLOST:
                Game.is_paused = True
            elif event.type == pygame.WINDOWFOCUSGAINED:
                for button in (Game.resume_btn, Game.menu_btn):
                    if button.btn.collidepoint(pygame.mouse.get_pos()):
                        button.fn()
                        # Fixes bug where buttons would have to be clicked
                        # twice to work after window had lost focus
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if Game.screen_id == 2 and not Game.is_dead:
                        # Checking that we are not in a menu
                        Game.is_paused = Game.is_paused ^ True
                        # Can also unpause by pressing escape again
                if Game.is_paused or Game.is_dead:
                    continue
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    Game.car.move("right")
                    break
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    Game.car.move("left")
                    break

        Game.render_screen()
        pygame.display.update()
        Game.clock.tick(FPS)


if __name__ == "__main__":
    main()
