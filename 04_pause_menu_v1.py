import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60


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


def render_pause(*buttons):
    win.fill("white")
    draw_text("Paused", "black", (WIDTH // 2, 100))
    for button in buttons:
        button.draw()


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
clock = pygame.time.Clock()
menu = Button(WIDTH // 2 - 125, HEIGHT // 2 + 50, 250, 50,
              "Back To Menu", lambda: print("Main Menu"))
resume = Button(WIDTH // 2 - 125, HEIGHT // 2 - 50, 250, 50,
                "Resume", lambda: print("Resume"))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    render_pause(menu, resume)
    pygame.display.update()
    clock.tick(FPS)
