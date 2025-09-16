import time
import pygame
from function import (
    solve, solve_heuristic_MRV,
    solve_heuristic_MRV_LCV, solve_MRV_LCV_FC,
    get_counter, reset_counter
)

from visualize import draw_board

from utils import read_grid_from_file

def main():
    board = read_grid_from_file("data.txt")
    solver_name, elapsed_time, elapsed_real_time, backtracks = "", 0, 0, 0
    delay = 0.01
    dragging = False

    buttons, slider_rect = draw_board(board, solver_name, elapsed_time, elapsed_real_time, backtracks, delay=delay)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if slider_rect.collidepoint(pos):
                    dragging = True

                if buttons["load"].collidepoint(pos):
                    board = read_grid_from_file("data.txt")

                else:
                    reset_counter()
                    solver_name = ""
                    elapsed_time = elapsed_real_time = backtracks = 0

                    if buttons["basic"].collidepoint(pos):
                        solver_name = "Backtracking co ban"
                        start_real = time.time()
                        solve([row[:] for row in board], visualize=False, draw_fn=None, delay=0)
                        elapsed_real_time = time.time() - start_real

                        start_total = time.time()
                        solve(board, visualize=True,
                              draw_fn=lambda b, highlight=None: draw_board(b, solver_name,
                                                                            time.time() - start_total,
                                                                            elapsed_real_time,
                                                                            get_counter(),
                                                                            highlight, delay),
                              delay=delay)
                        elapsed_time = time.time() - start_total
                        backtracks = get_counter()

                    elif buttons["mrv"].collidepoint(pos):
                        solver_name = "Backtracking + MRV"
                        start_real = time.time()
                        solve_heuristic_MRV([row[:] for row in board], visualize=False, draw_fn=None, delay=0)
                        elapsed_real_time = time.time() - start_real

                        start_total = time.time()
                        solve_heuristic_MRV(board, visualize=True,
                                            draw_fn=lambda b, highlight=None: draw_board(b, solver_name,
                                                                                          time.time() - start_total,
                                                                                          elapsed_real_time,
                                                                                          get_counter(),
                                                                                          highlight, delay),
                                            delay=delay)
                        elapsed_time = time.time() - start_total
                        backtracks = get_counter()

                    elif buttons["mrv_lcv"].collidepoint(pos):
                        solver_name = "Backtracking + MRV + LCV"
                        start_real = time.time()
                        solve_heuristic_MRV_LCV([row[:] for row in board], visualize=False, draw_fn=None, delay=0)
                        elapsed_real_time = time.time() - start_real

                        start_total = time.time()
                        solve_heuristic_MRV_LCV(board, visualize=True,
                                                draw_fn=lambda b, highlight=None: draw_board(b, solver_name,
                                                                                              time.time() - start_total,
                                                                                              elapsed_real_time,
                                                                                              get_counter(),
                                                                                              highlight, delay),
                                                delay=delay)
                        elapsed_time = time.time() - start_total
                        backtracks = get_counter()

                    elif buttons["fc"].collidepoint(pos):
                        solver_name = "Backtracking + MRV + LCV + FC"
                        start_real = time.time()
                        solve_MRV_LCV_FC([row[:] for row in board], visualize=False, draw_fn=None, delay=0)
                        elapsed_real_time = time.time() - start_real

                        start_total = time.time()
                        solve_MRV_LCV_FC(board, visualize=True,
                                         draw_fn=lambda b, highlight=None: draw_board(b, solver_name,
                                                                                       time.time() - start_total,
                                                                                       elapsed_real_time,
                                                                                       get_counter(),
                                                                                       highlight, delay),
                                         delay=delay)
                        elapsed_time = time.time() - start_total
                        backtracks = get_counter()

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                x = max(150, min(450, event.pos[0]))
                delay = ((x - 150) / 300) * 0.5

        buttons, slider_rect = draw_board(board, solver_name, elapsed_time, elapsed_real_time, backtracks, delay=delay)

    pygame.quit()


if __name__ == "__main__":
    main()