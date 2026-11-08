"""The cultivation game (paper, section 9): N institutions choose to cultivate (contribute) or harvest.

Payoffs, with k contributors including oneself:
  cultivate:  R + s + r - (c - f) + nb*k + B*[k >= k*]
  harvest:    R + nb*k + B*[k >= k*]
s private benefit, r recognition, c cost, f funding, nb benefit each contribution gives everyone,
B the benefit a maintained commons gives everyone once k* contributors sustain it.

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import math
DEFAULTS = {"players": 8, "R": 10.0, "s": 2.0, "r": 0.0, "c": 6.0, "f": 0.0, "nb": 1.0, "B": 8.0, "k_star": 3}

def _g(g):
    d = dict(DEFAULTS); d.update(g or {}); return d
def _bonus(k, g):
    return g["B"] if k >= g["k_star"] else 0.0
def pay_c(k, g):
    return g["R"] + g["s"] + g["r"] - (g["c"] - g["f"]) + g["nb"] * k + _bonus(k, g)
def pay_h(k, g):
    return g["R"] + g["nb"] * k + _bonus(k, g)
def equilibria(g=None):
    g = _g(g); N = int(g["players"]); out = []
    for k in range(N + 1):
        ok = True
        if k > 0 and pay_c(k, g) < pay_h(k - 1, g): ok = False
        if k < N and pay_h(k, g) < pay_c(k + 1, g): ok = False
        if ok: out.append(k)
    return out
def welfare(k, g=None):
    g = _g(g); N = int(g["players"])
    return N * g["R"] + k * (g["s"] + g["r"] - g["c"]) + N * g["nb"] * k + N * _bonus(k, g)
def optimum(g=None):
    g = _g(g); N = int(g["players"]); best = 0
    for k in range(1, N + 1):
        if welfare(k, g) > welfare(best, g): best = k
    return best
def pmf(n, k, x):
    if k < 0 or k > n: return 0.0
    return math.comb(n, k) * math.pow(x, k) * math.pow(1.0 - x, n - k)
def gain(x, g=None):
    """Expected payoff advantage of cultivating when a share x of the others cultivate."""
    g = _g(g); N = int(g["players"]); ks = int(g["k_star"])
    return g["s"] + g["r"] - g["c"] + g["f"] + g["nb"] + g["B"] * pmf(N - 1, ks - 1, x)
def replicator(x0, g=None, steps=60, rate=0.05):
    g = _g(g); xs = [x0]; x = x0
    for _ in range(steps):
        x = x + rate * x * (1.0 - x) * gain(x, g)
        x = 1.0 if x > 1.0 else (0.0 if x < 0.0 else x)
        xs.append(x)
    return xs
