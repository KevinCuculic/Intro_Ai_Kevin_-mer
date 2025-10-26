"""
search.py
Purpose: A* Suche über 8-Puzzle.
Input:  start: Tuple[int,...], h: Heuristik(state)->int, name: str
Output: SearchResult (path, cost, expanded_nodes, runtime_s, found, heuristic_name)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple
import heapq, time
from puzzle import neighbors, is_goal

State = Tuple[int, ...]
Heuristic = Callable[[State], int]

@dataclass
class SearchResult:
    path: List[State]
    cost: int
    expanded_nodes: int
    runtime_s: float
    found: bool
    heuristic_name: str

def _reconstruct(came_from: Dict[State, State], current: State) -> List[State]:
    """Pfad rückwärts aufrollen."""
    p = [current]
    while current in came_from:
        current = came_from[current]
        p.append(current)
    return list(reversed(p))

def a_star(start: State, h: Heuristic, name: str) -> SearchResult:
    """Standard A*: f = g + h, open als Min-Heap, closed via best_seen g."""
    t0 = time.perf_counter()
    came_from: Dict[State, State] = {}
    best_seen: Dict[State, int] = {start: 0}
    # Heap-Eintrag: (f, g, tie, state) — tie für stabile Ordnung
    open_heap = [(h(start), 0, 0, start)]
    expanded = 0
    tie = 0

    while open_heap:
        f, g, _, s = heapq.heappop(open_heap)
        if is_goal(s):
            t1 = time.perf_counter()
            return SearchResult(_reconstruct(came_from, s), g, expanded, t1 - t0, True, name)

        expanded += 1
        for nxt, step in neighbors(s):
            ng = g + step
            if nxt not in best_seen or ng < best_seen[nxt]:
                best_seen[nxt] = ng
                came_from[nxt] = s
                tie += 1
                heapq.heappush(open_heap, (ng + h(nxt), ng, tie, nxt))

    t1 = time.perf_counter()
    return SearchResult([], 0, expanded, t1 - t0, False, name)
