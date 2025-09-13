from collections import deque

def is_valid(board, row, col, value):
    # Kiểm tra hàng
    for c in range(9):
        if c != col:
            if value == board[row][c]:
                return False
    # Kiểm tra cột
    for r in range(9):
        if r != row:
            if value == board[r][col]:
                return False

    start_r = (row // 3) * 3
    start_c = (col // 3) * 3

    # kiểm tra ô trống trong Block
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

def solve(board):
    global dem

    for i in range(9):
        for j in range(9):
            if(board[i][j]==0):
                for k in range(1,10):
                    if(is_valid(board, i, j, k)):
                        board[i][j] = k
                        if solve(board):                                # đệ quy
                            return True
                        board[i][j]=0
                        dem += 1
                return False
    return True
#MRV
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

def solve_heuristic_MRV(board):
    global dem
    cell = find_best_cell(board)
    if cell is None:
        return False
    if cell == (-1,-1):
        return True
    row, col = cell
    for k in range(1, 10):
        if (is_valid(board, row, col, k)):
            board[row][col] = k
            if solve_heuristic_MRV(board):  # đệ quy
                return True
            board[row][col] = 0
            dem += 1
    return False

#MRV+LCV
def count_constraints(board, row, col, val):
    # tạm gán
    # board[row][col] = val
    # impact = 0
    # for i in range(9):
    #     for j in range(9):
    #         if board[i][j] == 0:
    #             count = 0
    #             for k in range(1, 10):
    #                 if is_valid(board, i, j, k):
    #                     count += 1
    #             impact += count
    # board[row][col] = 0  # reset lại
    # return impact
    # gán thử giá trị
    board[row][col] = val
    impact = 0

    neighbors = set()

    # cùng hàng
    for j in range(9):
        if board[row][j] == 0:
            neighbors.add((row, j))

    # cùng cột
    for i in range(9):
        if board[i][col] == 0:
            neighbors.add((i, col))

    # cùng block 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == 0:
                neighbors.add((i, j))

    # đếm số lựa chọn hợp lệ cho mỗi neighbor
    for (i, j) in neighbors:
        count = 0
        for k in range(1, 10):
            if is_valid(board, i, j, k):
                count += 1
        impact += count

    # reset lại
    board[row][col] = 0
    return impact

def solve_heuristic_MRV_LCV(board):
    global dem

    cell = find_best_cell(board)
    if cell is None:  # ngõ cụt
        return False
    row, col = cell
    if row == -1 and col == -1:  # hết ô trống -> thành công
        return True

    candidates = [k for k in range(1,10)
                  if is_valid(board, row, col, k)]

    # Áp dụng LCV: sắp xếp theo sự hạn chế
    candidates.sort(key=lambda val: count_constraints(board, row, col, val), reverse=True)

    for val in candidates:
        board[row][col] = val
        if solve_heuristic_MRV_LCV(board):  # đệ quy
            return True
        board[row][col] = 0
        dem += 1
    return False

# Forward Checking

def init_domain(board):
    domains = [[set() for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                domains[i][j] = {board[i][j]}
            else:
                S = set(range(1, 10))
                # loại số trong hàng
                for x in range(9):
                    if board[i][x] in S:
                        S.remove(board[i][x])
                # loại số trong cột
                for y in range(9):
                    if board[y][j] in S:
                        S.remove(board[y][j])
                # loại số trong block
                bi, bj = (i // 3) * 3, (j // 3) * 3
                for r in range(bi, bi + 3):
                    for c in range(bj, bj + 3):
                        if board[r][c] in S:
                            S.remove(board[r][c])
                domains[i][j] = S
    return domains

def get_neighbors(row, col):
    """Lấy các ô láng giềng của (row, col) chưa gán."""
    neighbors = set()
    for i in range(9):
        if i != col:
            neighbors.add((row, i))
        if i != row:
            neighbors.add((i, col))
    # block 3x3
    start_r, start_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if (r, c) != (row, col):
                neighbors.add((r, c))
    return neighbors

def solve_MRV_LCV_FC(board):
    global dem
    domains = init_domain(board)

    def backtrack():
        global dem
        # MRV: chọn ô còn ít giá trị khả thi nhất
        min_len = 10
        cell = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if len(domains[i][j]) < min_len:
                        min_len = len(domains[i][j])
                        cell = (i, j)

        if not cell:
            return True  # hết ô trống

        row, col = cell

        # LCV: sắp xếp các giá trị theo mức ảnh hưởng
        candidates = list(domains[row][col])
        candidates.sort(key=lambda val: sum(val in domains[r][c]
                                             for r, c in get_neighbors(row, col)))

        for val in candidates:
            # thử gán
            board[row][col] = val
            # lưu lại các miền bị loại
            removed = {}
            fail = False
            for r, c in get_neighbors(row, col):
                if board[r][c] == 0 and val in domains[r][c]:
                    domains[r][c].remove(val)
                    removed[(r, c)] = val
                    if not domains[r][c]:  # dead-end
                        fail = True
                        break
            if not fail:
                if backtrack():
                    return True
            # quay lui
            board[row][col] = 0
            for (r, c), v in removed.items():
                domains[r][c].add(v)
            dem += 1
        return False

    return backtrack()

#AC3

def revise(domains, xi, xj):
    """
    xi, xj are tuples (r,c).
    Remove any value x in domains[xi] that has NO supporting value y in domains[xj]
    (for Sudoku constraint x != y, support exists if any y in domains[xj] with y != x).
    Return True if domains[xi] was reduced.
    """
    i, j = xi
    p, q = xj
    revised = False
    xi_dom = domains[i][j]
    xj_dom = domains[p][q]

    # make a snapshot to iterate (avoid modifying set during iteration)
    to_remove = set()
    for x in list(xi_dom):
        # there must exist y in xj_dom such that y != x
        if not any(y != x for y in xj_dom):
            # no supporting y => remove x
            to_remove.add(x)

    if to_remove:
        xi_dom -= to_remove
        revised = True
    return revised

def ac3(domains, get_neighbors):
    """
    domains: 9x9 list of sets (domains[r][c])
    get_neighbors: function (r,c) -> set of neighbor positions
    Returns True if arc consistency achieved (no empty domain), False if some domain became empty.
    """
    # Build initial queue of all arcs (Xi, Xj) where Xj is neighbor of Xi
    queue = deque()
    for r in range(9):
        for c in range(9):
            # only variables with non-empty domains matter
            if domains[r][c]:
                for n in get_neighbors(r, c):
                    queue.append(((r, c), n))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi[0]][xi[1]]:
                return False
            # enqueue all neighbors Xk of Xi except Xj
            for xk in get_neighbors(xi[0], xi[1]):
                if xk != xj:
                    queue.append((xk, xi))
    return True

def deep_copy_domains(domains):
    return [[set(domains[r][c]) for c in range(9)] for r in range(9)]

def select_unassigned_variable(domains, board):
    best = None
    min_len = 10
    has_empty = False
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                has_empty = True
                l = len(domains[r][c])
                if l < min_len:
                    min_len = l
                    best = (r, c)
                if l == 0:
                    # dead end: we can return special signal None to indicate fail
                    return None
    if not has_empty:
        return (-1, -1)  # solved
    return best

def lcv_order(domains, row, col, get_neighbors):
    """Return list of candidate values sorted by LCV (least constraining first)."""
    candidates = list(domains[row][col])
    def impact(val):
        # đếm có bao nhiêu láng giềng sẽ mất val khỏi domain
        cnt = 0
        for (r,c) in get_neighbors(row, col):
            if val in domains[r][c]:
                cnt += 1
        return cnt
    candidates.sort(key=impact)  # tăng dần -> ít ảnh hưởng trước
    return candidates

def solve_mrv_lcv_fc_ac3(board):
    domains = init_domain(board)  # trả về domains as 2D list of sets
    if domains is None:
        return False

    def backtrack():
        global dem
        dem += 1

        cell = select_unassigned_variable(domains, board)
        if cell == (-1, -1):
            return True
        if cell is None:  # dead-end
            return False

        row, col = cell
        # LCV ordering
        candidates = lcv_order(domains, row, col, get_neighbors)

        for val in candidates:
            # save domains snapshot (deep copy)
            saved_domains = deep_copy_domains(domains)

            # assign
            board[row][col] = val
            domains[row][col] = {val}

            # forward checking: remove val from neighbors' domains
            fail = False
            for (r, c) in get_neighbors(row, col):
                if board[r][c] == 0 and val in domains[r][c]:
                    domains[r][c].remove(val)
                    if not domains[r][c]:
                        fail = True
                        break

            # if not fail, run AC-3 to further prune
            if not fail:
                if ac3(domains, get_neighbors):
                    if backtrack():
                        return True
                else:
                    fail = True

            # restore (undo)
            board[row][col] = 0
            # restore domains from snapshot
            for r in range(9):
                for c in range(9):
                    domains[r][c] = set(saved_domains[r][c])

            dem += 1

        return False

    return backtrack()

