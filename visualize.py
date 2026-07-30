"""
==============================================================
 Sudoku Visualizer -- bonus utility
==============================================================
 ProDigy InfoTech | Task 04
 Author: Comillas Negras
==============================================================

Generates a clean "before / after" PNG image of any sample puzzle,
showing the unsolved grid next to the grid solved by the
backtracking engine in sudoku_solver.py. Handy for README banners,
LinkedIn posts, or just admiring the algorithm's work.

Usage:
    python visualize.py                    -> renders the Medium example
    python visualize.py --puzzle 4         -> renders the Expert example
    python visualize.py --out mine.png     -> custom output filename

Requires: matplotlib  (pip install matplotlib)
"""

import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sudoku_solver import SudokuSolver, PUZZLES

GIVEN_COLOR = "#1a1a2e"
SOLVED_COLOR = "#1565c0"
SHADE = "#eef1fb"
LINE_THIN = "#c7cbdb"
LINE_THICK = "#1a1a2e"


def draw_board(ax, grid, original=None):
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")

    for br in range(3):
        for bc in range(3):
            if (br + bc) % 2 == 1:
                ax.add_patch(plt.Rectangle((bc * 3, br * 3), 3, 3,
                                            facecolor=SHADE, edgecolor="none", zorder=0))

    for i in range(10):
        lw = 2.6 if i % 3 == 0 else 0.9
        color = LINE_THICK if i % 3 == 0 else LINE_THIN
        ax.plot([0, 9], [i, i], color=color, linewidth=lw, zorder=2)
        ax.plot([i, i], [0, 9], color=color, linewidth=lw, zorder=2)

    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v == 0:
                continue
            is_given = original is None or original[r][c] != 0
            ax.text(c + 0.5, r + 0.5, str(v), ha="center", va="center", fontsize=17,
                    color=GIVEN_COLOR if is_given else SOLVED_COLOR,
                    fontweight="bold" if is_given else "normal", zorder=3)


def render(puzzle_key: str, out_path: str) -> None:
    label, grid = PUZZLES[puzzle_key]
    solver = SudokuSolver(grid)
    if not solver.is_valid_puzzle():
        raise SystemExit("Puzzle is invalid, cannot visualize.")
    solver.solve()

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.1))
    draw_board(axes[0], grid)
    draw_board(axes[1], solver.grid, original=grid)
    axes[0].set_title("INPUT \u2014 Unsolved", fontsize=14, fontweight="bold",
                       color=GIVEN_COLOR, pad=14)
    axes[1].set_title("OUTPUT \u2014 Solved", fontsize=14, fontweight="bold",
                       color=SOLVED_COLOR, pad=14)
    fig.suptitle(f"Sudoku Solver \u2014 {label}", fontsize=18, fontweight="bold",
                 color=GIVEN_COLOR, y=1.02)
    fig.text(0.5, 0.5, "\u2192", fontsize=36, ha="center", va="center",
              color=SOLVED_COLOR, fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(out_path, dpi=170, bbox_inches="tight", facecolor="white")
    print(f"Saved {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a before/after Sudoku image.")
    parser.add_argument("--puzzle", default="2", choices=list(PUZZLES.keys()),
                         help="Which sample puzzle to render (1=Easy .. 4=Expert). Default: 2")
    parser.add_argument("--out", default="sudoku_before_after.png", help="Output PNG filename")
    args = parser.parse_args()
    render(args.puzzle, args.out)
