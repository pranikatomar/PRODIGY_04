"""
==============================================================
 Sudoku Solver -- Backtracking Algorithm
==============================================================
 ProDigy InfoTech | Software Development Internship
 Task 04 : Implement a Sudoku Solver
 Author  : Comillas Negras
==============================================================

WHAT THIS PROGRAM DOES
-----------------------
Given an unsolved 9x9 Sudoku grid (0 represents an empty cell),
this program fills in every empty cell so that:

  * Each row contains the digits 1-9 exactly once.
  * Each column contains the digits 1-9 exactly once.
  * Each of the nine 3x3 boxes contains the digits 1-9 exactly once.

HOW IT WORKS (Backtracking)
----------------------------
1. Find the next empty cell.
2. Try placing digits 1-9 in it, one at a time.
3. For each digit, check whether it is legal (not already used in
   the same row, column, or 3x3 box).
4. If legal, place it and recursively try to solve the rest of the
   grid the same way.
5. If the recursive call succeeds, the puzzle is solved.
6. If it fails (a dead end is reached), undo ("backtrack") the last
   digit placed, and try the next possible digit instead.
7. If no digit 1-9 works for a cell, backtrack further to the
   previous cell and try a different digit there.

This guarantees that every possibility is explored systematically
until a valid solution is found (or every possibility is exhausted,
meaning the puzzle has no solution).

USAGE
-----
    python sudoku_solver.py            -> interactive menu
    python sudoku_solver.py --demo     -> auto-solves a sample puzzle
"""

from __future__ import annotations

import copy
import sys
import time
from typing import List, Optional, Tuple

Grid = List[List[int]]

# Make Unicode box-drawing characters safe to print on every platform
# (falls back to '?' instead of crashing on very old Windows consoles).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ------------------------------------------------------------------
# Sample puzzles (0 = empty cell). Feel free to add your own!
# ------------------------------------------------------------------
PUZZLES: dict[str, Tuple[str, Grid]] = {
    "1": ("Easy", [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]),
    "2": ("Medium", [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ]),
    "3": ("Hard", [
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 3],
        [0, 7, 4, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 0, 2],
        [0, 8, 0, 0, 4, 0, 0, 1, 0],
        [6, 0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 7, 8, 0],
        [5, 0, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 4, 0],
    ]),
    "4": ("Expert (World's Hardest, Arto Inkala 2012)", [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]),
}


class SudokuSolver:
    """Wraps a 9x9 grid and solves it in-place using backtracking."""

    SIZE = 9
    BOX = 3

    def __init__(self, grid: Grid):
        self._validate_shape(grid)
        self.original: Grid = copy.deepcopy(grid)
        self.grid: Grid = copy.deepcopy(grid)
        self.attempts = 0  # number of digit placements tried (for stats)

    # ---------------------------------------------------------------
    # Validation
    # ---------------------------------------------------------------
    @staticmethod
    def _validate_shape(grid: Grid) -> None:
        if len(grid) != 9 or any(len(row) != 9 for row in grid):
            raise ValueError("Grid must be 9x9.")
        for row in grid:
            for val in row:
                if not isinstance(val, int) or not (0 <= val <= 9):
                    raise ValueError("Grid values must be integers 0-9 (0 = empty).")

    def is_valid_puzzle(self) -> bool:
        """Check that the *given* clues don't already break Sudoku's rules."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                val = self.grid[r][c]
                if val != 0:
                    self.grid[r][c] = 0
                    ok = self._is_valid_placement(r, c, val)
                    self.grid[r][c] = val
                    if not ok:
                        return False
        return True

    # ---------------------------------------------------------------
    # Backtracking engine
    # ---------------------------------------------------------------
    def _is_valid_placement(self, row: int, col: int, num: int) -> bool:
        if num in self.grid[row]:
            return False
        if num in (self.grid[r][col] for r in range(self.SIZE)):
            return False
        box_r, box_c = (row // self.BOX) * self.BOX, (col // self.BOX) * self.BOX
        for r in range(box_r, box_r + self.BOX):
            for c in range(box_c, box_c + self.BOX):
                if self.grid[r][c] == num:
                    return False
        return True

    def _find_empty(self) -> Optional[Tuple[int, int]]:
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] == 0:
                    return r, c
        return None

    def solve(self) -> bool:
        """Recursively solve the puzzle in place. Returns True if solved."""
        empty = self._find_empty()
        if empty is None:
            return True  # no empty cells left -> solved
        row, col = empty
        for num in range(1, 10):
            self.attempts += 1
            if self._is_valid_placement(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0  # backtrack
        return False

    def count_clues(self) -> int:
        return sum(1 for row in self.original for v in row if v != 0)


# ------------------------------------------------------------------
# Display helpers
# ------------------------------------------------------------------
def format_grid(grid: Grid) -> str:
    """Return the grid as a nicely boxed string."""
    top, mid, bottom = (
        "\u2554" + "\u2550" * 7 + "\u2566" + "\u2550" * 7 + "\u2566" + "\u2550" * 7 + "\u2557",
        "\u2560" + "\u2550" * 7 + "\u256c" + "\u2550" * 7 + "\u256c" + "\u2550" * 7 + "\u2563",
        "\u255a" + "\u2550" * 7 + "\u2569" + "\u2550" * 7 + "\u2569" + "\u2550" * 7 + "\u255d",
    )
    lines = [top]
    for r in range(9):
        cells = [str(v) if v != 0 else "\u00b7" for v in grid[r]]
        row_str = (
            "\u2551 " + " ".join(cells[0:3]) +
            " \u2551 " + " ".join(cells[3:6]) +
            " \u2551 " + " ".join(cells[6:9]) + " \u2551"
        )
        lines.append(row_str)
        if r in (2, 5):
            lines.append(mid)
    lines.append(bottom)
    return "\n".join(lines)


BANNER = """
============================================================
   SUDOKU SOLVER  --  Backtracking Algorithm
   ProDigy InfoTech | Task 04 | by Comillas Negras
============================================================
"""


def read_custom_grid() -> Grid:
    print("\nEnter your puzzle, one row at a time.")
    print("Type 9 digits per row, using 0 for empty cells (e.g. 530070000).\n")
    grid = []
    for i in range(9):
        while True:
            raw = input(f"Row {i + 1}: ").strip().replace(" ", "")
            if len(raw) == 9 and raw.isdigit():
                grid.append([int(ch) for ch in raw])
                break
            print("  Invalid row -- please enter exactly 9 digits (0-9).")
    return grid


def solve_and_report(grid: Grid, label: str) -> None:
    solver = SudokuSolver(grid)
    print(f"\nPuzzle ({label}) -- {solver.count_clues()} clues given:")
    print(format_grid(solver.grid))

    if not solver.is_valid_puzzle():
        print("\n[INVALID] This puzzle breaks Sudoku's rules "
              "(a digit repeats in a row, column, or box).")
        return

    print("\nSolving...")
    start = time.perf_counter()
    solved = solver.solve()
    elapsed = time.perf_counter() - start

    if solved:
        print(f"\n[SOLVED] in {elapsed:.4f} seconds "
              f"({solver.attempts:,} placements attempted).\n")
        print(format_grid(solver.grid))
    else:
        print("\n[UNSOLVABLE] No solution exists for this puzzle.")


def main() -> None:
    if "--demo" in sys.argv:
        print(BANNER)
        label, grid = PUZZLES["4"]
        solve_and_report(grid, label)
        return

    print(BANNER)
    while True:
        print("Choose a puzzle to solve:")
        print("  1. Easy")
        print("  2. Medium")
        print("  3. Hard")
        print("  4. Expert (World's Hardest*)")
        print("  5. Enter your own puzzle")
        print("  0. Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice in PUZZLES:
            label, grid = PUZZLES[choice]
            solve_and_report(grid, label)
        elif choice == "5":
            grid = read_custom_grid()
            solve_and_report(grid, "Custom")
        else:
            print("Invalid choice, please try again.\n")
            continue

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
