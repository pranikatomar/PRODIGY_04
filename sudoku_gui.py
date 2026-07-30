"""
==============================================================
 Sudoku Solver -- Graphical Interface (Tkinter)
==============================================================
 ProDigy InfoTech | Software Development Internship
 Task 04 : Implement a Sudoku Solver
 Author  : Comillas Negras
==============================================================

A small desktop GUI wrapped around the backtracking engine in
sudoku_solver.py. Load a sample puzzle (or type your own numbers
into the grid), press "Solve", and watch the completed grid
appear -- solved digits are shown in blue, original clues stay
bold black so you can always tell them apart.

Run:
    python sudoku_gui.py

Requires: Python's standard `tkinter` module.
  * Windows / macOS: included with the official python.org installer.
  * Linux: if missing, install it with  sudo apt install python3-tk
"""

import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

from sudoku_solver import SudokuSolver, PUZZLES

# ---------------------------------------------------------------
# Palette
# ---------------------------------------------------------------
BG_COLOR = "#f4f5fb"
BOARD_BG = "#1a1a2e"
CELL_BG = "#ffffff"
GIVEN_COLOR = "#1a1a2e"
SOLVED_COLOR = "#1565c0"
ERROR_COLOR = "#c0392b"
ACCENT = "#4361ee"
ACCENT_DARK = "#3651d4"
MUTED = "#6b7280"


class SudokuGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sudoku Solver \u2014 ProDigy InfoTech Task 04")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.cells: list[list[tk.Entry]] = [[None] * 9 for _ in range(9)]  # type: ignore
        self.given_mask = [[False] * 9 for _ in range(9)]
        self.label_to_key = {v[0]: k for k, v in PUZZLES.items()}

        self._build_header()
        self._build_board()
        self._build_controls()
        self._build_status()

        self.load_puzzle("1")

    # ---------------------------------------------------------------
    # UI construction
    # ---------------------------------------------------------------
    def _build_header(self):
        tk.Label(
            self.root, text="SUDOKU SOLVER", font=("Helvetica", 24, "bold"),
            bg=BG_COLOR, fg=BOARD_BG,
        ).pack(pady=(20, 2))
        tk.Label(
            self.root, text="Backtracking Algorithm  \u2022  ProDigy InfoTech \u2014 Task 04",
            font=("Helvetica", 10), bg=BG_COLOR, fg=MUTED,
        ).pack(pady=(0, 16))

    def _build_board(self):
        outer = tk.Frame(self.root, bg=BOARD_BG, bd=0)
        outer.pack(padx=24)
        self.num_font_given = tkfont.Font(family="Helvetica", size=17, weight="bold")
        self.num_font_solved = tkfont.Font(family="Helvetica", size=17, weight="normal")

        for br in range(3):
            for bc in range(3):
                box = tk.Frame(outer, bg=BOARD_BG)
                box.grid(
                    row=br, column=bc,
                    padx=(3, 3), pady=(3, 3),
                )
                for r in range(3):
                    for c in range(3):
                        R, C = br * 3 + r, bc * 3 + c
                        e = tk.Entry(
                            box, width=2, font=self.num_font_given, justify="center",
                            relief="flat", bd=0, bg=CELL_BG, fg=GIVEN_COLOR,
                            highlightthickness=1, highlightbackground="#e2e4f0",
                            highlightcolor=ACCENT, disabledbackground=CELL_BG,
                        )
                        e.grid(row=r, column=c, padx=1, pady=1, ipady=8)
                        e.bind("<KeyRelease>", lambda ev, row=R, col=C: self._on_key(row, col))
                        self.cells[R][C] = e

    def _on_key(self, row, col):
        e = self.cells[row][col]
        val = e.get()
        if val and (not val[-1].isdigit() or val[-1] == "0"):
            e.delete(0, tk.END)
        elif len(val) > 1:
            e.delete(0, tk.END)
            e.insert(0, val[-1])
        self.given_mask[row][col] = bool(e.get())
        e.config(fg=GIVEN_COLOR, font=self.num_font_given)

    def _build_controls(self):
        bar = tk.Frame(self.root, bg=BG_COLOR)
        bar.pack(pady=16)

        tk.Label(bar, text="Load example:", bg=BG_COLOR, fg=BOARD_BG,
                 font=("Helvetica", 10)).grid(row=0, column=0, padx=(0, 8))

        self.puzzle_var = tk.StringVar(value=PUZZLES["1"][0])
        display_labels = [v[0] for v in PUZZLES.values()]
        menu = tk.OptionMenu(bar, self.puzzle_var, *display_labels, command=self._on_menu_select)
        menu.config(width=20, relief="flat", bg="#e5e7eb", highlightthickness=0, cursor="hand2")
        menu.grid(row=0, column=1, padx=(0, 14))

        solve_btn = tk.Button(
            bar, text="Solve", command=self.solve, bg=ACCENT, fg="white",
            font=("Helvetica", 11, "bold"), relief="flat", padx=18, pady=7,
            activebackground=ACCENT_DARK, activeforeground="white", cursor="hand2",
        )
        solve_btn.grid(row=0, column=2, padx=6)

        clear_btn = tk.Button(
            bar, text="Clear", command=self.clear, bg="#e5e7eb", fg=BOARD_BG,
            font=("Helvetica", 11), relief="flat", padx=18, pady=7, cursor="hand2",
        )
        clear_btn.grid(row=0, column=3, padx=6)

    def _build_status(self):
        self.status = tk.Label(
            self.root, text="Ready.", font=("Helvetica", 10, "bold"),
            bg=BG_COLOR, fg=MUTED, wraplength=360, justify="center",
        )
        self.status.pack(pady=(0, 20))

    # ---------------------------------------------------------------
    # Grid <-> UI helpers
    # ---------------------------------------------------------------
    def _read_grid(self):
        grid = []
        for r in range(9):
            row = []
            for c in range(9):
                v = self.cells[r][c].get().strip()
                row.append(int(v) if v.isdigit() and v != "0" else 0)
            grid.append(row)
        return grid

    def _write_grid(self, grid):
        for r in range(9):
            for c in range(9):
                e = self.cells[r][c]
                e.delete(0, tk.END)
                if grid[r][c] != 0:
                    e.insert(0, str(grid[r][c]))
                is_given = self.given_mask[r][c]
                e.config(
                    fg=GIVEN_COLOR if is_given else SOLVED_COLOR,
                    font=self.num_font_given if is_given else self.num_font_solved,
                )

    # ---------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------
    def _on_menu_select(self, label):
        self.load_puzzle(self.label_to_key[label])

    def load_puzzle(self, key):
        label, grid = PUZZLES[key]
        self.puzzle_var.set(label)
        self.given_mask = [[grid[r][c] != 0 for c in range(9)] for r in range(9)]
        self._write_grid(grid)
        self.status.config(text=f"Loaded: {label} puzzle. Press Solve.", fg=MUTED)

    def clear(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].config(fg=GIVEN_COLOR, font=self.num_font_given)
        self.given_mask = [[False] * 9 for _ in range(9)]
        self.status.config(text="Grid cleared. Type your own puzzle or load an example.", fg=MUTED)

    def solve(self):
        grid = self._read_grid()
        self.given_mask = [[grid[r][c] != 0 for c in range(9)] for r in range(9)]

        try:
            solver = SudokuSolver(grid)
        except ValueError as exc:
            messagebox.showerror("Invalid grid", str(exc))
            return

        if not solver.is_valid_puzzle():
            self.status.config(
                text="Invalid puzzle: a digit repeats in a row, column, or box.",
                fg=ERROR_COLOR,
            )
            return

        self.status.config(text="Solving...", fg=MUTED)
        self.root.update_idletasks()

        start = time.perf_counter()
        solved = solver.solve()
        elapsed = time.perf_counter() - start

        if solved:
            self._write_grid(solver.grid)
            self.status.config(
                text=f"Solved in {elapsed:.4f}s  ({solver.attempts:,} placements attempted).",
                fg=SOLVED_COLOR,
            )
        else:
            self.status.config(text="No solution exists for this puzzle.", fg=ERROR_COLOR)


def main():
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
