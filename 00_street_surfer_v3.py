"""Version 3: Add Game class which takes care of images,
buttons, and rendering functions
Jack Andrews
02/5/23"""
import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60


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
    pygame.init()
    icon = pygame.image.load("./assets/game_icon.png")
    font = pygame.font.Font("./assets/PressStart.ttf", 18)
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Street Surfers")
    pygame.display.set_icon(icon)
    win.fill("white")
    clock = pygame.time.Clock()
    menu_key = 0

    start_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2, 250, 50, "Start",
        lambda: print("Start Game"))

    how_to_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50, "Instructions",
        lambda: setattr(Game, "menu_key", 1))

    quit_btn = Button(
        WIDTH // 2 - 125, HEIGHT // 2 + 200, 250, 50, "Quit", exit)

    menu_btn = Button(WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50,
                      "Back To Menu", lambda: setattr(Game, "menu_key", 0))

    @classmethod
    def render_main_menu(cls):
        cls.win.fill("white")
        cls.draw_text("Street Surfers", "black", (WIDTH // 2, 100))
        # Greatly simplified rendering function, making it easier to understand
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
    def render_menu(cls, menu_key):
        # This function determines which screen will be drawn
        if menu_key == 0:
            cls.render_main_menu()
        elif menu_key == 1:
            cls.render_instructions()


def main():
    # Abstracting our program into functions makes main routine quite small
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        Game.render_menu(Game.menu_key)
        pygame.display.update()
        Game.clock.tick(FPS)


if __name__ == "__main__":
    main()
