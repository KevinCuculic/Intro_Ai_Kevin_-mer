"""
puzzle.py
Purpose: 8-Puzzle Zustände + Moves + Solvability.
Input:  state = 9er Tuple (row-major), 0 = Leerfeld
Output: GOAL, is_solvable, neighbors, format_board, initial_random
"""

from __future__ import annotations
from typing import Iterator, Tuple
import random

# Zielzustand (1..8, 0 als Leerfeld)
GOAL: Tuple[int, ...] = (1,2,3,4,5,6,7,8,0)

def initial_random(solvable: bool = True, seed: int | None = None) -> Tuple[int, ...]:
    """Erzeugt zufälligen Startzustand; bei solvable=True so lange mischen bis lösbar."""
    rng = random.Random(seed)
    while True:
        tiles = list(range(9))
        rng.shuffle(tiles)
        state = tuple(tiles)
        if not solvable or is_solvable(state):
            return state

def is_solvable(state: Tuple[int, ...]) -> bool:
    """3x3-Regel: Gerade Anzahl Inversionen ⇒ lösbar (0 ignorieren)."""
    tiles = [t for t in state if t != 0]
    inv = sum(1 for i in range(len(tiles)) for j in range(i+1, len(tiles)) if tiles[i] > tiles[j])
    return inv % 2 == 0

def neighbors(state: Tuple[int, ...]) -> Iterator[Tuple[Tuple[int, ...], int]]:
    """Alle legalen Züge erzeugen, indem 0 mit Nachbar getauscht wird (Kosten=1)."""
    z = state.index(0)
    r, c = divmod(z, 3)
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            s = list(state)
            j = nr*3 + nc
            s[z], s[j] = s[j], s[z]
            yield tuple(s), 1

def is_goal(state: Tuple[int, ...]) -> bool:
    return state == GOAL

def format_board(state: Tuple[int, ...]) -> str:
    """Kleine Textdarstellung 3x3 (.) für das Leerfeld)."""
    rows = []
    for r in range(3):
        row = state[r*3:(r+1)*3]
        rows.append(" ".join(" ." if t==0 else f"{t:2d}" for t in row))
    return "\n".join(rows)
