def read_grid_from_file(filename):
    grid = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            row = [int(x) for x in line.split()]
            grid.append(row)
    return grid

def print_grid(grid):
    print("--------Bảng SUDOKU--------")
    for row in grid:
    #    print(" ".join(str(x) for x in row))
        print(row)
    print("---------------------------")