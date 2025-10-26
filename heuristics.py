"""
heuristics.py
Purpose: Heuristiken für A*.
Input:  state = 9er Tuple
Output: hamming(state), manhattan(state)
"""

from __future__ import annotations
from typing import Tuple
from puzzle import GOAL

# Zielpositionen vorberechnen (für Manhattan)
_GOAL_POS = {tile: (i // 3, i % 3) for i, tile in enumerate(GOAL)}

def hamming(state: Tuple[int, ...]) -> int:
    """Anzahl falsch platzierter Steine (0 ignoriert)."""
    return sum(1 for i, t in enumerate(state) if t != 0 and t != GOAL[i])

def manhattan(state: Tuple[int, ...]) -> int:
    """Summe der |dx|+|dy| Abstände zur Zielposition (0 ignoriert)."""
    d = 0
    for idx, tile in enumerate(state):
        if tile == 0:
            continue
        r, c = divmod(idx, 3)
        gr, gc = _GOAL_POS[tile]
        d += abs(r - gr) + abs(c - gc)
    return d
