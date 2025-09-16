import pygame
pygame.init()

WIDTH, HEIGHT = 600, 900
CELL_SIZE = 60
MARGIN = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Visualizer")

FONT = pygame.font.SysFont("Arial", 32, bold=True)
BTN_FONT = pygame.font.SysFont("Arial", 20, bold=True)
INFO_FONT = pygame.font.SysFont("Arial", 18)

def draw_button(rect, text, mouse_pos, base_color=(100, 149, 237), hover_color=(65, 105, 225)):
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = BTN_FONT.render(text, True, (255, 255, 255))
    screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

def draw_board(board, solver_name="", elapsed_time=0, real_time=0, backtracks=0, highlight=None, delay=0.0):
    screen.fill((245, 245, 245))
    mouse_pos = pygame.mouse.get_pos()

    for i in range(9):
        for j in range(9):
            x = MARGIN + j * CELL_SIZE
            y = MARGIN + i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), True, (0, 0, 0))
                screen.blit(text, (x + 20, y + 10))

    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0),
                         (MARGIN, MARGIN + i * CELL_SIZE),
                         (MARGIN + 9 * CELL_SIZE, MARGIN + i * CELL_SIZE),
                         line_width)
        pygame.draw.line(screen, (0, 0, 0),
                         (MARGIN + i * CELL_SIZE, MARGIN),
                         (MARGIN + i * CELL_SIZE, MARGIN + 9 * CELL_SIZE),
                         line_width)

    if highlight:
        if len(highlight) == 2:
            (r, c) = highlight
            color = (0, 255, 0)  # mặc định xanh lá
        else:
            (r, c, color) = highlight
        x = MARGIN + c * CELL_SIZE
        y = MARGIN + r * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect, 3)

    btns = {
        "load": pygame.Rect(50, 600, 100, 50),
        "basic": pygame.Rect(200, 600, 150, 40),
        "mrv": pygame.Rect(200, 650, 150, 40),
        "mrv_lcv": pygame.Rect(370, 600, 180, 40),
        "fc": pygame.Rect(370, 650, 180, 40),
    }

    draw_button(btns["load"], "LOAD", mouse_pos)
    draw_button(btns["basic"], "Backtracking", mouse_pos)
    draw_button(btns["mrv"], "BT+MRV", mouse_pos)
    draw_button(btns["mrv_lcv"], "BT+MRV+LCV", mouse_pos)
    draw_button(btns["fc"], "BT+MRV+LCV+FC", mouse_pos)

    slider_x, slider_y = 150, 740
    slider_w, slider_h = 300, 8
    handle_x = slider_x + int((delay / 0.5) * slider_w)

    pygame.draw.rect(screen, (180, 180, 180), (slider_x, slider_y, slider_w, slider_h))
    pygame.draw.circle(screen, (70, 130, 180), (handle_x, slider_y + slider_h // 2), 10)

    slider_label = INFO_FONT.render(f"Delay: {delay:.2f}s", True, (0, 0, 0))
    screen.blit(slider_label, (WIDTH // 2 - slider_label.get_width() // 2, slider_y - 25))

    slider_rect = pygame.Rect(slider_x, slider_y, slider_w, slider_h)

    info_rect = pygame.Rect(0, 780, WIDTH, 120)
    pygame.draw.rect(screen, (220, 220, 220), info_rect)

    line1 = f"Solver: {solver_name}"
    line2 = f"Thoi gian chay: {elapsed_time:.3f}s   |   Thoi gian thuc: {real_time:.6f}s   |   So lan backtrack: {backtracks}"

    line1_surface = INFO_FONT.render(line1, True, (0, 0, 0))
    line2_surface = INFO_FONT.render(line2, True, (0, 0, 0))

    screen.blit(line1_surface, (WIDTH // 2 - line1_surface.get_width() // 2, 800))
    screen.blit(line2_surface, (WIDTH // 2 - line2_surface.get_width() // 2, 830))

    pygame.display.update()
    return btns, slider_rect
