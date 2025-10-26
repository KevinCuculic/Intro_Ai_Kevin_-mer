"""
main.py
Usage:
  python main.py --demo   # eine zufällige, lösbare Instanz mit Hamming & Manhattan
"""

import argparse
from puzzle import initial_random, format_board
from heuristics import hamming, manhattan
from search import a_star

def run_one(state):
    print("Start:\n", format_board(state), sep="")
    for name, h in [("Hamming", hamming), ("Manhattan", manhattan)]:
        r = a_star(state, h, name)
        print(f"\n{name}: found={r.found} cost={r.cost} expanded={r.expanded_nodes} time={r.runtime_s:.4f}s")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        st = initial_random(solvable=True)
        run_one(st)
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
