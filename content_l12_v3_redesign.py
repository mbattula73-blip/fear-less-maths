"""
Fear Less Maths — LEVEL 12 (Algebra — Equations) v3 worksheet architecture
(2026-08-04)

Same pattern as Levels 10/11: already has 100% SVG diagram coverage, so
this reorganizes existing content rather than authoring new diagrams,
and audits every diagram type for answer leaks (all 7 types used here
-- balance_scale, two_line_graph, inverse_machine, linear_equation_
graph, solve_equation_ladder, substitution_steps, consecutive_bar --
were already correctly designed; no leaks found this time).

  Q1-6   The sheet's own existing diagram questions, diagram-DEPENDENT
         ones prioritized (12CUM1/12G/12CUM3 have some -- "graph both
         equations, where do they meet?" can't be answered without the
         picture).
  Q7-12  6 more of the sheet's own questions, self-contained text,
         diagram stripped.
  Q13-15 "Quick Review" -- toughened beyond Level 11's tier: 3-digit x
         3-digit multiplication (Level 4), 4-digit / 3-digit division
         (Level 5), simplifying an algebraic expression harder than
         Level 11's own range (Level 11 -- solving an equation starts
         with simplifying the expressions on each side).
  Q16-20 "Speed Calculation" -- BODMAS (order of operations) questions,
         moderate to tough, per direct request. Brackets + mixed
         operations at sheet 1, escalating to multiple brackets/
         exponents by sheet 4 -- genuinely tests order of operations,
         not just raw arithmetic speed.
"""
import random
import content as _C


_DEP_KEYWORDS = ("graph", "diagram", "shown", "pictured", "picture",
                  "table shows", "bar shows", "chart", "the model",
                  "the tiles", "the scale", "the machine", "the ladder",
                  "plot both")


def _is_dependent(text):
    t = (text or "").lower()
    return any(k in t for k in _DEP_KEYWORDS)


def _item_key(item):
    return (item.get("text", ""), repr(item.get("diagram_params")))


_SOURCE_DISPATCH = {code: dict(_C._DISPATCH[code]) for code in (
    "12A", "12B", "12C", "12CUM1", "12D", "12E", "12F", "12CUM2",
    "12G", "12H", "12I", "12CUM3", "12J", "12REV",
)}


def _build_block1(code, sheet):
    items = _SOURCE_DISPATCH[code][sheet]()
    concept_items = [x for x in items if x.get("type") in ("concept_box", "tips_box")]
    qs = [x for x in items if x.get("type") not in ("concept_box", "tips_box")]
    diag_qs = [x for x in qs if x.get("diagram_type")]
    dependent = [x for x in diag_qs if _is_dependent(x.get("text", ""))]
    independent = [x for x in diag_qs if not _is_dependent(x.get("text", ""))]

    block1a_src = list(dependent[:6])
    if len(block1a_src) < 6:
        block1a_src += independent[:6 - len(block1a_src)]
    block1a = []
    for i, x in enumerate(block1a_src):
        y = dict(x)
        params = dict(y.get("diagram_params") or {})
        params["blank"] = (i >= 2)
        y["diagram_params"] = params
        block1a.append(y)
    used_keys = {_item_key(x) for x in block1a_src}

    pool = [x for x in independent if _item_key(x) not in used_keys]
    pool_sorted = sorted(range(len(pool)), key=lambda i: len(pool[i].get("text", "")))
    block1b_src = [pool[i] for i in pool_sorted[:6]]
    block1b = []
    for x in block1b_src:
        y = dict(x)
        y["type"] = "fill"
        y["diagram_type"] = None
        y["diagram_params"] = None
        block1b.append(y)
    idx = 0
    while len(block1b) < 6:
        n = random.randint(2, 15) + idx
        block1b.append(_C.q(f"True or False: x = {n} satisfies x + {n} = {2*n}.", "fill", "____ (True/False)"))
        idx += 1

    return concept_items, block1a, block1b


# ───────────────────────── Quick Review (toughened beyond Level 11) ─────────────────────────

def _l12v3_quick_review(sheet):
    """3 questions, toughened beyond Level 11's tier: 3-digit x 3-digit
    multiplication (Level 4), 4-digit / 3-digit division (Level 5), and
    simplifying an expression harder than Level 11's own range (Level
    11 -- solving an equation starts with simplifying each side)."""
    tiers = {
        1: {"mlo": 200, "mhi": 500, "dlo": 150, "dhi": 400, "dbig": 9500, "elo": 3, "ehi": 12},
        2: {"mlo": 250, "mhi": 600, "dlo": 180, "dhi": 450, "dbig": 9700, "elo": 4, "ehi": 15},
        3: {"mlo": 300, "mhi": 700, "dlo": 200, "dhi": 500, "dbig": 9800, "elo": 5, "ehi": 18},
        4: {"mlo": 350, "mhi": 800, "dlo": 220, "dhi": 550, "dbig": 9900, "elo": 6, "ehi": 22},
    }
    t = tiers[sheet]
    items = []

    a = random.randint(t["mlo"], t["mhi"])
    b = random.randint(t["mlo"], t["mhi"])
    items.append(_C.q(f"Quick Review (Level 4): {a} x {b} = ____", "fill", "Answer = ____"))

    d = random.randint(t["dlo"], t["dhi"])
    k_lo = t["dlo"] // 10
    k_hi = min(t["dhi"] // 10, t["dbig"] // d)
    if k_hi < k_lo:
        k_hi = k_lo
    k = random.randint(k_lo, k_hi)
    k = max(k, 2)
    n = d * k
    items.append(_C.q(f"Quick Review (Level 5): {n} / {d} = ____", "fill", "Answer = ____"))

    c1 = random.randint(t["elo"], t["ehi"])
    c2 = random.randint(t["elo"], t["ehi"])
    c3 = random.randint(t["elo"], t["ehi"])
    items.append(_C.q(f"Quick Review (Level 11): Simplify {c1}x + {c2}y - {c3}x + {c2}y", "fill", "Answer = ____"))

    return items


# ───────────────────────── Speed Calculation: BODMAS ─────────────────────────

def _l12v3_bodmas_calc(sheet):
    """5 BODMAS (order of operations) questions, moderate to tough,
    escalating across sheets -- brackets + mixed operations at sheet 1,
    multiple brackets and a simple exponent by sheet 4. This is
    deliberately an order-of-operations test, not just raw arithmetic:
    each template is only correct if brackets/multiplication/division
    are evaluated before addition/subtraction. Every expression is
    constructed (or retried) to guarantee a clean non-negative integer
    result -- a BODMAS fluency drill with a negative or decimal answer
    is the wrong kind of hard for this level."""
    tiers = {
        1: {"lo": 2, "hi": 12},
        2: {"lo": 3, "hi": 15},
        3: {"lo": 4, "hi": 18},
        4: {"lo": 5, "hi": 22},
    }
    t = tiers[sheet]
    lo, hi = t["lo"], t["hi"]

    def r():
        return random.randint(lo, hi)

    def ordered_pair():
        """Two values, larger first, so a-b style subtraction stays >= 0."""
        a, b = r(), r()
        return (a, b) if a >= b else (b, a)

    def clean_div(min_q=2, max_q=None):
        """A (dividend, divisor) pair that divides exactly."""
        max_q = max_q or hi
        divisor = random.randint(2, max(2, hi // 2))
        quotient = random.randint(min_q, max_q)
        return divisor * quotient, divisor

    templates_by_tier = {
        1: [
            lambda: f"{r()} + {r()} x {r()}",
            lambda: f"({r()} + {r()}) x {r()}",
            lambda: (lambda a, b, c: f"{a} x {c} - {b}")(*ordered_pair(), r()),
            lambda: (lambda b, c: f"{r()} x ({b} - {c})")(*ordered_pair()),
            lambda: (lambda a, b: f"{a} - {b} + {r()} x 2")(*ordered_pair()),
        ],
        2: [
            lambda: (lambda a, b: f"{a} + {r()} x {r()} - {b}")(*ordered_pair()),
            lambda: (lambda a, b: f"({r()} + {r()}) x {a} - {b}")(*ordered_pair()),
            lambda: (lambda p, q: f"{r()} x {r()} - {p} x {q}")(*ordered_pair()),
            lambda: f"({r()} - {min(r(),hi-1)}) x ({r()} + {r()})",
            lambda: (lambda n, d: f"{r()} x {r()} + {n} / {d}")(*clean_div()),
        ],
        3: [
            lambda: (lambda p, q: f"({r()} + {r()}) x {r()} - {p} x {q}")(*ordered_pair()),
            lambda: (lambda a, b: f"{a} x {r()} - ({b} + {r()}) x {r()%4+2}")(*ordered_pair()),
            lambda: f"({max(r(),lo+1)} - {lo}) x {r()} + {r()} x {r()%5+2}",
            lambda: (lambda p, q: f"{r()}^2 - {p} x {q}")(*ordered_pair()),
            lambda: (lambda n, d: f"({r()} + {n} / {d}) - {min(r(),hi-1)}")(*clean_div()),
        ],
        4: [
            lambda: f"({r()} + {r()}) x ({max(r(),lo+2)} - {lo})",
            lambda: (lambda p, q: f"{r()}^2 + {p} x {q} - {min(r(),hi-1)}")(*ordered_pair()),
            lambda: (lambda n, d: f"({n} - {min(d,n-1)}) / {d}")(*clean_div(min_q=3)),
            lambda: (lambda a, b: f"{r()} x ({r()} + {r()}) - {a} x {b}")(*ordered_pair()),
            lambda: (lambda n, d: f"({r()} + {r()})^2 / {d} - {min(n//d, hi-1)}")(*clean_div(min_q=2, max_q=6)),
        ],
    }
    templates = templates_by_tier[sheet]
    chosen = random.sample(templates, 5)
    items = []
    for tmpl in chosen:
        expr = None
        for _ in range(60):
            try:
                candidate = tmpl()
                py_expr = candidate.replace("x", "*").replace("^", "**")
                val = eval(py_expr)
            except Exception:
                continue
            if isinstance(val, float) and not float(val).is_integer():
                continue
            if val < 0:
                continue
            expr = candidate
            break
        if expr is None:
            expr = f"{r()} + {r()} x {r()}"
        items.append(_C.q(f"Speed Calculation (BODMAS): {expr} = ____", "fill", "Answer = ____"))
    return items


# ───────────────────────── Assembly ─────────────────────────

def build_v3_sheet(code, sheet):
    random.seed(12000 + hash(code) % 5000 + sheet * 31)
    concept_items, block1a, block1b = _build_block1(code, sheet)
    out = list(concept_items)
    out += block1a
    out += block1b
    out += _l12v3_quick_review(sheet)
    out += _l12v3_bodmas_calc(sheet)
    return out


LEVEL12_V3_DISPATCH = {
    code: {s: (lambda c=code, s=s: build_v3_sheet(c, s)) for s in (1, 2, 3, 4)}
    for code in _SOURCE_DISPATCH
}
