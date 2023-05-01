"""Version 2: Integrate Main Menu and instruction screen into main program
as well as button class
Jack Andrews
01/5/23"""
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


def render_main_menu():
    win.fill("white")
    draw_text("Street Surfers", "black", (WIDTH // 2, 100))
    # Greatly simplified rendering function, making it easier to understand
    start.draw()
    how_to.draw()
    finish.draw()


def render_instructions():
    # Passing in menu button as parameter instead of creating it each frame
    win.fill("white")
    draw_text("Instructions", "black", (WIDTH // 2, 100))
    draw_text("Controls:", "black", (40, 160), align="left")
    draw_text("Left arrow/A:  Move left", "black", (40, 185), align="left")
    draw_text("Right arrow/D: Move right", "black", (40, 210), align="left")
    draw_text("Escape:        Pause", "black", (40, 235), align="left")

    draw_text("Rules:", "black", (40, 310), align="left")
    draw_text("Avoid the oncoming cars", "black", (40, 335), align="left")
    draw_text("by switching lanes. If you", "black", (40, 360), align="left")
    draw_text("hit a car, you lose.", "black", (40, 385), align="left")
    # Rendering all the text for the instructions

    menu.draw()


def render_menu(menu_key):
    menus[menu_key]()

def switch_menu(new_key):
    global menu_key
    menu_key = new_key


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
clock = pygame.time.Clock()
menus = {0: render_main_menu, 1: render_instructions}
start = Button(
    WIDTH // 2 - 125, HEIGHT // 2, 250, 50, "Start",
    lambda: print("Start Game"))

how_to = Button(
    WIDTH // 2 - 125, HEIGHT // 2 + 100, 250, 50, "Instructions",
    lambda: switch_menu(1))

finish = Button(
    WIDTH // 2 - 125, HEIGHT // 2 + 200, 250, 50, "Quit", exit)
menu_key = 0

menu = Button(WIDTH // 2 - 125, HEIGHT // 2 + 150, 250, 50,
              "Back To Menu", lambda: switch_menu(0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    render_menu(menu_key)
    pygame.display.update()
    clock.tick(FPS)
