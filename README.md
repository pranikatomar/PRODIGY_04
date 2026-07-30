# PRODIGY_04
# 🧩 Sudoku Solver

**A Python Sudoku solver that uses backtracking to fill in any valid 9×9 puzzle — complete with a command-line interface and a graphical (Tkinter) front end.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> **ProDigy InfoTech — Software Development Internship**
> **Task 04 — Implement a Sudoku Solver**
> Author: **Pranika Tomar**

![Sudoku Solver banner](screenshots/banner_before_after.png)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How the Algorithm Works](#how-the-algorithm-works)
- [Demo Screenshots](#demo-screenshots)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Example Input / Output](#example-input--output)
- [Performance Notes](#performance-notes)
- [Possible Improvements](#possible-improvements)
- [Author](#author)
- [License](#license)

## Overview

This project takes an unsolved 9×9 Sudoku grid (empty cells written as `0`) and
fills it in completely, using a **recursive backtracking algorithm** — trying
digits one at a time, undoing any choice that leads to a dead end, until every
row, column, and 3×3 box legally contains the digits 1-9 exactly once.

The repository includes three ways to use it:

| Script | What it is |
|---|---|
| `sudoku_solver.py` | The core solving engine + an interactive command-line menu |
| `sudoku_gui.py` | A point-and-click Tkinter desktop app built on the same engine |
| `visualize.py` | A bonus utility that renders a "before / after" PNG image of any puzzle |

## Features

- ✅ Classic recursive **backtracking** solver, written from scratch
- ✅ Validates the starting grid so it never tries to "solve" a broken puzzle
- ✅ Four bundled sample puzzles — **Easy, Medium, Hard**, and the famous
  **"World's Hardest Sudoku"** (Arto Inkala, 2012)
- ✅ Type in your own puzzle at the CLI menu, or type numbers directly into the GUI grid
- ✅ Clean, boxed grid printing in the console (Unicode, with an ASCII-safe fallback)
- ✅ GUI clearly distinguishes original clues (bold black) from solved digits (blue)
- ✅ Reports solve time and number of placements attempted
- ✅ Fully documented, type-hinted, dependency-free core (pure standard library)

## How the Algorithm Works

Backtracking explores the grid one empty cell at a time:

```
1. Find the next empty cell.
2. Try digits 1–9 in it, one at a time.
3. For each digit, check it doesn't already appear in that
   row, column, or 3x3 box.
4. If it's legal, place it and recurse into the rest of the grid.
5. If the recursion succeeds, the puzzle is solved -- done.
6. If the recursion fails (dead end), undo the digit
   ("backtrack") and try the next one.
7. If no digit works, backtrack to the previous cell.
```

Because every possibility is tried systematically, backtracking is guaranteed
to find a solution if one exists (or correctly report that none does). It's
not the fastest technique on the market (compared to constraint-propagation
solvers), but it is simple, reliable, and easy to follow — which is exactly
why it's the standard teaching example for this problem.

## Demo Screenshots

**Command-line interface**, solving the "World's Hardest Sudoku":

![CLI demo](screenshots/cli_demo.png)

**Graphical interface** — load an example, then press *Solve*:

| Before | After |
|---|---|
| ![GUI before solving](screenshots/gui_before_solving.png) | ![GUI after solving](screenshots/gui_after_solving.png) |

Original clues stay **bold black**; every digit the algorithm placed itself is shown in **blue**.

## Getting Started

### Prerequisites
- Python 3.8 or later
- Tkinter, for the GUI only (already included with Python on Windows/macOS;
  on Linux install it with `sudo apt install python3-tk` if it's missing)
- matplotlib, for the bonus `visualize.py` script only

### Installation
```bash
git clone https://github.com/<your-username>/PRODIGY_SD_04.git
cd PRODIGY_SD_04
pip install -r requirements.txt   # only needed for visualize.py
```

### Usage

**Command line** — interactive menu:
```bash
python sudoku_solver.py
```
```
Choose a puzzle to solve:
  1. Easy
  2. Medium
  3. Hard
  4. Expert (World's Hardest*)
  5. Enter your own puzzle
  0. Exit
```

**Command line** — non-interactive demo (solves the Expert puzzle and exits):
```bash
python sudoku_solver.py --demo
```

**Graphical app**:
```bash
python sudoku_gui.py
```

**Bonus — generate your own before/after image**:
```bash
python visualize.py --puzzle 3 --out hard_puzzle.png
```

## Project Structure

```
PRODIGY_SD_04/
├── sudoku_solver.py     # Core backtracking engine + CLI menu (run this first)
├── sudoku_gui.py        # Tkinter GUI front-end
├── visualize.py         # Bonus: renders before/after PNG images
├── requirements.txt     # Only matplotlib, and only for visualize.py
├── LICENSE              # MIT
├── .gitignore
├── README.md
└── screenshots/
    ├── banner_before_after.png
    ├── cli_demo.png
    ├── gui_before_solving.png
    └── gui_after_solving.png
```

## Example Input / Output

**Input** (0 = empty cell):
```
5 3 0 | 0 7 0 | 0 0 0
6 0 0 | 1 9 5 | 0 0 0
0 9 8 | 0 0 0 | 0 6 0
------+-------+------
8 0 0 | 0 6 0 | 0 0 3
4 0 0 | 8 0 3 | 0 0 1
7 0 0 | 0 2 0 | 0 0 6
------+-------+------
0 6 0 | 0 0 0 | 2 8 0
0 0 0 | 4 1 9 | 0 0 5
0 0 0 | 0 8 0 | 0 7 9
```

**Output**:
```
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
------+-------+------
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
------+-------+------
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

## Performance Notes

Plain backtracking with no extra heuristics is intentionally simple — it
picks the first empty cell it finds (left-to-right, top-to-bottom) rather
than the "smartest" one. Measured on the sample puzzles bundled with this
project:

| Puzzle | Clues given | Placements attempted | Typical solve time |
|---|---|---|---|
| Easy | 30 | ~37,600 | ~0.02 s |
| Medium | 36 | ~300 | < 0.01 s |
| Hard | 19 | ~705,600 | ~0.3 – 0.6 s |
| Expert (World's Hardest) | 21 | ~445,800 | ~0.3 – 1.1 s |

(The attempt counts are deterministic and will match on any machine; only
the elapsed *time* depends on your hardware.) Interestingly, **Hard** ends
up needing more brute-force attempts than **Expert** here — a good reminder
that "hardest for a human" and "slowest for a naive backtracker" aren't
always the same thing. Which empty cell you search next matters more to
plain backtracking's speed than the raw clue count does.

## Possible Improvements

Ideas for extending this project further:
- Minimum-Remaining-Values (MRV) heuristic to pick the most constrained cell first
- A Sudoku **puzzle generator**, not just a solver
- Step-by-step visualization of the backtracking process (animated)
- OCR input: read a puzzle from a photo of a newspaper grid
- Web version using the same engine behind a Flask/FastAPI backend

## Author

**Pranika Tomar**
Submitted as Task 04 of the ProDigy InfoTech Software Development internship.

## License

This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and share it.
