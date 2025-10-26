"""
benchmark.py
Usage:
  python benchmark.py --n 100
Output:
  results.csv (Rohdaten) + Konsolen-Summary (Mean/Std)
"""

import argparse, csv, statistics, time
from puzzle import initial_random
from heuristics import hamming, manhattan
from search import a_star

HEURISTICS = {"Hamming": hamming, "Manhattan": manhattan}

def run_benchmark(n: int, seed_base: int = 42):
    rows = []
    for i in range(n):
        state = initial_random(True, seed=seed_base + i)  # reproduzierbar
        for name, h in HEURISTICS.items():
            r = a_star(state, h, name)
            rows.append({
                "run": i,
                "heuristic": name,
                "cost": r.cost,
                "expanded_nodes": r.expanded_nodes,
                "runtime_s": r.runtime_s,
            })
    return rows

def summarize(rows):
    def stats_of(key, filt):
        vals = [r[key] for r in rows if r["heuristic"] == filt]
        m = statistics.mean(vals)
        sd = statistics.pstdev(vals) if len(vals) > 1 else 0.0
        return m, sd
    for name in HEURISTICS:
        m_exp, sd_exp = stats_of("expanded_nodes", name)
        m_t, sd_t   = stats_of("runtime_s", name)
        m_c, sd_c   = stats_of("cost", name)
        print(f"{name:10s} | expanded {m_exp:.1f}±{sd_exp:.1f} | time {m_t*1000:.2f}±{sd_t*1000:.2f} ms | cost {m_c:.1f}±{sd_c:.1f}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--out", type=str, default="results.csv")
    args = ap.parse_args()

    t0 = time.perf_counter()
    rows = run_benchmark(args.n)
    t1 = time.perf_counter()

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["run","heuristic","cost","expanded_nodes","runtime_s"])
        w.writeheader(); w.writerows(rows)

    summarize(rows)
    print(f"\nTotal wall time: {t1 - t0:.2f}s")

if __name__ == "__main__":
    main()
