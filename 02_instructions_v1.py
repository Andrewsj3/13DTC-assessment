import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60


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


def render_instructions():
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

    menu_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2 + 150), (250, 50))
    pygame.draw.rect(win, "blue", menu_btn)
    draw_text("Back to Menu", "white", (menu_btn.centerx, menu_btn.centery))


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    render_instructions()
    pygame.display.update()
    clock.tick(FPS)
