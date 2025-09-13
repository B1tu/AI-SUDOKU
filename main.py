from function import is_valid, solve, get_counter, reset_counter, find_best_cell, solve_heuristic_MRV, solve_heuristic_MRV_LCV, solve_MRV_LCV_FC, solve_mrv_lcv_fc_ac3
from utils import read_grid_from_file, print_grid
import time
def main():
    grid = read_grid_from_file("data.txt")

    print_grid(grid)

    # reset_counter()
    # start = time.time()
    # solve(grid)
    # end = time.time()
    # print_grid(grid)
    # print("So lan goi de quy: ", get_counter())
    # print("Thời gian chạy:", end - start, "giây")

    reset_counter()
    start = time.time()
    solve_heuristic_MRV(grid)
    end = time.time()
    print_grid(grid)
    print("So lan goi de quy: ", get_counter())
    print("Thời gian chạy:", end - start, "giây")


    # reset_counter()
    # start = time.time()
    # solve_heuristic_MRV_LCV(grid)
    # end = time.time()
    # print_grid(grid)
    # print("So lan goi de quy: ", get_counter())
    # print("Thời gian chạy:", end - start, "giây")

    # reset_counter()
    # start = time.time()
    # solve_MRV_LCV_FC(grid)
    # end = time.time()
    # print_grid(grid)
    # print("So lan goi de quy: ", get_counter())
    # print("Thời gian chạy:", end - start, "giây")

    reset_counter()
    start = time.time()
    solve_mrv_lcv_fc_ac3(grid)
    end = time.time()
    print_grid(grid)
    print("So lan goi de quy: ", get_counter())
    print("Thời gian chạy:", end - start, "giây")

