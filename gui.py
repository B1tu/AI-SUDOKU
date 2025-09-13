import tkinter as tk
from tkinter import messagebox, ttk
import time

from function import (
    solve, solve_heuristic_MRV, solve_heuristic_MRV_LCV,
    solve_MRV_LCV_FC, solve_mrv_lcv_fc_ac3,
    get_counter, reset_counter
)
from utils import read_grid_from_file

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        # Tạo bảng Sudoku
        frame = tk.Frame(root)
        frame.pack(pady=10)
        for i in range(9):
            for j in range(9):

                e = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                e.grid(row=i, column=j, padx=1, pady=1, ipadx=10, ipady=10)
                self.entries[i][j] = e

        # Menu chọn solver
        self.solver_choice = tk.StringVar()
        solvers = ["BACKTRACK THUẦN", "MRV", "MRV+LCV", "MRV+LCV+FC", "MRV+LCV+FC+AC3"]
        self.solver_choice.set(solvers[0])
        tk.Label(root, text="Chọn Solver:").pack()
        self.solver_menu = ttk.Combobox(root, textvariable=self.solver_choice, values=solvers, state="readonly")
        self.solver_menu.pack(pady=5)

        # Nút điều khiển
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Load từ file", command=self.load_from_file).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Solve", command=self.solve).grid(row=0, column=1, padx=10)

        # Label kết quả
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def load_from_file(self):
        try:
            grid = read_grid_from_file("data.txt")
            for i in range(9):
                for j in range(9):
                    val = grid[i][j]
                    self.entries[i][j].delete(0, tk.END)
                    if val != 0:
                        self.entries[i][j].insert(0, str(val))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")

    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            grid.append(row)
        return grid

    def set_grid(self, grid):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(grid[i][j]))

    def solve(self):
        grid = self.get_grid()
        solver = self.solver_choice.get()

        reset_counter()
        start = time.time()

        if solver == "BACKTRACK THUẦN":
            solve(grid)
        elif solver == "MRV":
            solve_heuristic_MRV(grid)
        elif solver == "MRV+LCV":
            solve_heuristic_MRV_LCV(grid)
        elif solver == "MRV+LCV+FC":
            solve_MRV_LCV_FC(grid)
        elif solver == "MRV+LCV+FC+AC3":
            solve_mrv_lcv_fc_ac3(grid)

        end = time.time()

        self.set_grid(grid)
        self.result_label.config(
            text=f"Số lần gọi đệ quy: {get_counter()} | Thời gian: {end - start:.4f} giây"
        )

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
