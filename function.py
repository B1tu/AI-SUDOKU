import time
import pygame
def is_valid(board, row, col, value):
    for c in range(9):
        if c != col:
            if value == board[row][c]:
                return False

    for r in range(9):
        if r != row:
            if value == board[r][col]:
                return False

    start_r = (row // 3) * 3
    start_c = (col // 3) * 3
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if (r, c) != (row, col) and value == board[r][c]:
                return False
    return True

dem = 0

def reset_counter():
    global dem
    dem = 0

def get_counter():
    return dem

def solve(board, visualize=False, draw_fn=None, delay=0.05):
    global dem
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for k in range(1, 10):
                    if is_valid(board, i, j, k):
                        board[i][j] = k
                        if visualize and draw_fn:
                            draw_fn(board, highlight=(i, j, (50, 50, 255)))
                            pygame.display.flip()
                            time.sleep(delay)

                        if solve(board, visualize, draw_fn, delay):
                            return True
                        board[i][j] = 0
                        dem += 1

                        if visualize and draw_fn:
                            draw_fn(board, highlight=(i, j, (200, 50, 50)))
                            pygame.display.flip()
                            time.sleep(delay)
                return False
    return True

def find_best_cell(board):
    best_cell = None
    min_options = 10
    has_empty = False
    for i in range(9):
        for j in range(9):
            if(board[i][j]==0):
                has_empty = True
                count = 0
                for k in range(1, 10):
                    if(is_valid(board, i, j, k)):
                        count+=1
                if count == 0:
                    return None
                if (count < min_options):
                    best_cell = (i, j)
                    min_options = count
    if not has_empty:
        return (-1,-1)
    return best_cell

def solve_heuristic_MRV(board, visualize=False, draw_fn=None, delay=0.05):
    global dem
    cell = find_best_cell(board)
    if cell is None:
        return False
    if cell == (-1, -1):
        return True

    row, col = cell
    for k in range(1, 10):
        if is_valid(board, row, col, k):
            board[row][col] = k

            if visualize and draw_fn:
                draw_fn(board, highlight=(row, col, (50, 50, 255)))
                time.sleep(delay)

            if solve_heuristic_MRV(board, visualize, draw_fn, delay):
                return True

            board[row][col] = 0
            if visualize and draw_fn:
                draw_fn(board, highlight=(row, col, (200, 50, 50)))
                time.sleep(delay)

            dem += 1
    return False

def count_constraints(board, row, col, val):
    board[row][col] = val
    impact = 0
    neighbors = set()
    for j in range(9):
        if board[row][j] == 0:
            neighbors.add((row, j))

    for i in range(9):
        if board[i][col] == 0:
            neighbors.add((i, col))

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == 0:
                neighbors.add((i, j))

    for (i, j) in neighbors:
        count = 0
        for k in range(1, 10):
            if is_valid(board, i, j, k):
                count += 1
        impact += count

    board[row][col] = 0
    return impact

def solve_heuristic_MRV_LCV(board, visualize=False, draw_fn=None, delay=0.05):
    global dem
    cell = find_best_cell(board)
    if cell is None:
        return False
    row, col = cell
    if row == -1 and col == -1:
        return True

    candidates = [k for k in range(1,10) if is_valid(board, row, col, k)]
    candidates.sort(key=lambda val: count_constraints(board, row, col, val), reverse = True)

    for val in candidates:
        board[row][col] = val
        if visualize and draw_fn:
            draw_fn(board, highlight=(row, col, (50, 50, 255)))
            time.sleep(delay)

        if solve_heuristic_MRV_LCV(board, visualize, draw_fn, delay):
            return True

        board[row][col] = 0
        if visualize and draw_fn:
            draw_fn(board, highlight=(row, col, (200, 50, 50)))
            time.sleep(delay)

        dem += 1
    return False

def init_domain(board):
    domains = [[set() for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                domains[i][j] = {board[i][j]}
            else:
                S = set(range(1, 10))

                for x in range(9):
                    if board[i][x] in S:
                        S.remove(board[i][x])

                for y in range(9):
                    if board[y][j] in S:
                        S.remove(board[y][j])

                bi, bj = (i // 3) * 3, (j // 3) * 3
                for r in range(bi, bi + 3):
                    for c in range(bj, bj + 3):
                        if board[r][c] in S:
                            S.remove(board[r][c])
                domains[i][j] = S
    return domains

def get_neighbors(row, col):
    neighbors = set()
    for i in range(9):
        if i != col:
            neighbors.add((row, i))
        if i != row:
            neighbors.add((i, col))

    start_r, start_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if (r, c) != (row, col):
                neighbors.add((r, c))
    return neighbors

def solve_MRV_LCV_FC(board, visualize=False, draw_fn=None, delay=0.05):
    global dem
    domains = init_domain(board)

    def backtrack():
        global dem
        min_len, cell = 10, None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if len(domains[i][j]) < min_len:
                        min_len = len(domains[i][j])
                        cell = (i, j)

        if not cell:
            return True

        row, col = cell
        candidates = list(domains[row][col])
        candidates.sort(key=lambda val: sum(val in domains[r][c]
                                            for r, c in get_neighbors(row, col)))

        for val in candidates:
            board[row][col] = val

            if visualize and draw_fn:
                draw_fn(board, highlight=(row, col, (50, 50, 255)))
                time.sleep(delay)

            removed = {}
            fail = False
            for r, c in get_neighbors(row, col):
                if board[r][c] == 0 and val in domains[r][c]:
                    domains[r][c].remove(val)
                    removed[(r, c)] = val
                    if not domains[r][c]:
                        fail = True
                        break

            if not fail:
                if backtrack():
                    return True

            board[row][col] = 0
            if visualize and draw_fn:
                draw_fn(board, highlight=(row, col, (200, 50, 50)))
                time.sleep(delay)

            for (r, c), v in removed.items():
                domains[r][c].add(v)

            dem += 1
        return False

    return backtrack()