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
    # Helper function that checks whether user has clicked on button, but
    # could be integrated into a potential Button class
    mouse_coords = pygame.mouse.get_pos()
    hovered = False
    if btn.collidepoint(mouse_coords):
        hovered = True
        if pygame.mouse.get_pressed()[0]: 
            func()
    return hovered

def render_main_menu():
    win.fill("white")
    draw_text("Street Surfers", "black", (WIDTH // 2, 100))

    start_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2), (250, 50))
    if check_clicked(start_btn, lambda: print("Start Game")):
        start_btn_col = colours["hover"]
        # Change colour so user knows button was pressed
    else:
        start_btn_col = colours["normal"]
    pygame.draw.rect(win, start_btn_col, start_btn)
    draw_text("Start", "white", (start_btn.centerx, start_btn.centery))
    # Obtaining button coords so we can place text in the centre

    help_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2 + 100), (250, 50))
    if check_clicked(help_btn, lambda: print("Start Game")):
        help_btn_col = colours["hover"]
    else:
        help_btn_col = colours["normal"]
    pygame.draw.rect(win, help_btn_col, help_btn)
    draw_text("Instructions", "white", (help_btn.centerx, help_btn.centery))
    check_clicked(help_btn, lambda: print("Instructions"))

    quit_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2 + 200), (250, 50))
    if check_clicked(quit_btn, lambda: print("Start Game")):
        quit_btn_col = colours["hover"]
    else:
        quit_btn_col = colours["normal"]
    pygame.draw.rect(win, quit_btn_col, quit_btn)
    draw_text("Quit", "white", (quit_btn.centerx, quit_btn.centery))
    check_clicked(quit_btn, lambda: print("Goodbye!"))
    # These eight lines get repeated a lot, something that could be improved


pygame.init()
colours = {
        "normal": "blue",
        "hover": "#6E6EEA",
        }
# This controls the colour of the buttons
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
    render_main_menu()
    pygame.display.update()
    clock.tick(FPS)
