"""v1: A mirror of the original button design in 01_main_menu_v3_t1.py
Jack Andrews
10/5/23"""
import pygame
WIDTH = 600
HEIGHT = 700
FPS = 10


def draw_text(text, text_col, coords, bg_col=None):
    # Helper function that draws text onto the screen at a given location
    txt = font.render(text, True, text_col, bg_col)
    text_box = txt.get_rect(center=coords)
    win.blit(txt, text_box)


def check_clicked(btn: pygame.Rect, func):
    # Checks if the button was hovered over or clicked
    mouse_coords = pygame.mouse.get_pos()
    hovered = False
    if btn.collidepoint(mouse_coords):
        hovered = True
        if pygame.mouse.get_pressed()[0]:
            func()
    return hovered


pygame.init()
icon = pygame.image.load("./assets/game_icon.png")
font = pygame.font.Font("./assets/PressStart.ttf", 18)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Surfers")
pygame.display.set_icon(icon)
win.fill("white")
hello_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2), (250, 50))
clock = pygame.time.Clock()
colours = {
    "normal": "blue",
    "hover": "#6E6EEA",
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if check_clicked(hello_btn, lambda: print("Hello World")):
        hello_btn_col = colours["hover"]
        # Change colour so user knows button was pressed
    else:
        hello_btn_col = colours["normal"]
    pygame.draw.rect(win, hello_btn_col, hello_btn)
    draw_text("Hello", "white", (hello_btn.centerx, hello_btn.centery))
    # Obtaining button coords so we can place text in the centre
    pygame.display.update()
    clock.tick(FPS)
