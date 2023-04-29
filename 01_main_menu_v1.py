import pygame
WIDTH = 600
HEIGHT = 700
FPS = 60


def draw_text(text, text_col, coords, bg_col=None):
    # Helper function that draws text onto the screen at a given location
    txt = font.render(text, True, text_col, bg_col)
    text_box = txt.get_rect(center=coords)
    win.blit(txt, text_box)


def render_main_menu():
    win.fill("white")
    draw_text("Street Surfers", "black", (WIDTH // 2, 100))

    start_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2), (250, 50))
    pygame.draw.rect(win, "blue", start_btn)
    draw_text("Start", "white", (start_btn.centerx, start_btn.centery))
    # Obtaining button coords so we can place text in the centre

    help_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2 + 100), (250, 50))
    pygame.draw.rect(win, "blue", help_btn)
    draw_text("Instructions", "white", (help_btn.centerx, help_btn.centery))

    quit_btn = pygame.Rect((WIDTH // 2 - 125, HEIGHT // 2 + 200), (250, 50))
    pygame.draw.rect(win, "blue", quit_btn)
    draw_text("Quit", "white", (quit_btn.centerx, quit_btn.centery))


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
    render_main_menu()
    pygame.display.update()
    clock.tick(FPS)
