import random
import sympy as sp
import json
import os
from datetime import date

# ── Symbols ──────────────────────────────────────────────────────────────────
x = sp.Symbol('x')

# ── Colour helpers (works on most terminals) ──────────────────────────────────
def col(text, code): return f"\033[{code}m{text}\033[0m"
def green(t):  return col(t, "92")
def red(t):    return col(t, "91")
def cyan(t):   return col(t, "96")
def yellow(t): return col(t, "93")
def bold(t):   return col(t, "1")

SAVE_FILE = "calcquest_save.json"

# ── Save / Load ───────────────────────────────────────────────────────────────
def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            return json.load(f)
    return {"total_score": 0, "sessions": 0, "best_streak": 0, "last_played": ""}

def write_save(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Question generators ───────────────────────────────────────────────────────
def make_differentiation(level):
    """Return (question_str, answer_expr, steps_str)"""
    if level == 1:
        # Simple polynomials: ax^n
        a = random.randint(1, 8)
        n = random.randint(1, 5)
        expr = a * x**n
        q = f"d/dx [ {sp.latex(expr)} ]"
        ans = sp.diff(expr, x)
        steps = (f"  Rule: d/dx [ax^n] = n·ax^(n-1)\n"
                 f"  = {n} × {a} · x^({n}-1)\n"
                 f"  = {sp.latex(ans)}")
    elif level == 2:
        # Sum of two terms
        a, b = random.randint(1, 6), random.randint(1, 6)
        m, n_ = random.randint(2, 5), random.randint(1, 4)
        expr = a * x**m + b * x**n_
        q = f"d/dx [ {sp.latex(expr)} ]"
        ans = sp.diff(expr, x)
        steps = (f"  Differentiate term by term:\n"
                 f"  d/dx[{sp.latex(a*x**m)}] = {sp.latex(sp.diff(a*x**m,x))}\n"
                 f"  d/dx[{sp.latex(b*x**n_)}] = {sp.latex(sp.diff(b*x**n_,x))}\n"
                 f"  Answer = {sp.latex(ans)}")
    else:
        # Trig / exp
        choices = [sp.sin(x), sp.cos(x), sp.exp(x), sp.log(x)]
        a = random.randint(1, 5)
        base = random.choice(choices)
        expr = a * base
        q = f"d/dx [ {sp.latex(expr)} ]"
        ans = sp.diff(expr, x)
        steps = (f"  Standard rule applied to {sp.latex(base)}:\n"
                 f"  d/dx[{sp.latex(expr)}] = {sp.latex(ans)}")
    return q, ans, steps


def make_integration(level):
    """Return (question_str, answer_expr, steps_str)"""
    if level == 1:
        a = random.randint(1, 8)
        n = random.randint(0, 4)
        expr = a * x**n
        q = f"∫ {sp.latex(expr)} dx"
        ans = sp.integrate(expr, x)
        steps = (f"  Rule: ∫ax^n dx = ax^(n+1)/(n+1) + C\n"
                 f"  = {a}·x^({n}+1)/({n}+1) + C\n"
                 f"  = {sp.latex(ans)} + C")
    elif level == 2:
        a, b = random.randint(1, 6), random.randint(1, 6)
        m, n_ = random.randint(1, 4), random.randint(0, 3)
        expr = a * x**m + b * x**n_
        q = f"∫ {sp.latex(expr)} dx"
        ans = sp.integrate(expr, x)
        steps = (f"  Integrate term by term:\n"
                 f"  ∫{sp.latex(a*x**m)} dx = {sp.latex(sp.integrate(a*x**m,x))}\n"
                 f"  ∫{sp.latex(b*x**n_)} dx = {sp.latex(sp.integrate(b*x**n_,x))}\n"
                 f"  Answer = {sp.latex(ans)} + C")
    else:
        choices = [sp.sin(x), sp.cos(x), sp.exp(x)]
        a = random.randint(1, 5)
        base = random.choice(choices)
        expr = a * base
        q = f"∫ {sp.latex(expr)} dx"
        ans = sp.integrate(expr, x)
        steps = (f"  Standard integral of {sp.latex(base)}:\n"
                 f"  ∫{sp.latex(expr)} dx = {sp.latex(ans)} + C")
    return q, ans, steps


def parse_answer(user_input):
    """Try to parse user's answer as a sympy expression."""
    try:
        return sp.sympify(user_input.replace("^", "**"), locals={"x": x, "e": sp.E})
    except Exception:
        return None


def answers_match(user_expr, correct_expr):
    """Check equivalence by simplifying the difference."""
    try:
        diff = sp.simplify(user_expr - correct_expr)
        return diff == 0
    except Exception:
        return False


# ── UI helpers ────────────────────────────────────────────────────────────────
def banner():
    print(cyan(bold("""
 ██████╗ █████╗ ██╗      ██████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗
██╔════╝██╔══██╗██║     ██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
██║     ███████║██║     ██║     ██║   ██║██║   ██║█████╗  ███████╗   ██║   
██║     ██╔══██║██║     ██║     ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
╚██████╗██║  ██║███████╗╚██████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║   
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
""")))
    print(cyan("         Learn Calculus Through Play — Integration & Differentiation\n"))


def show_stats(save):
    print(yellow(f"\n  📊  All-time Score : {save['total_score']}  |  "
                 f"Sessions Played : {save['sessions']}  |  "
                 f"Best Streak : {save['best_streak']}"))
    if save["last_played"]:
        print(yellow(f"       Last Played   : {save['last_played']}\n"))


def choose_level():
    print("\n  Choose difficulty:")
    print("   1 → Easy    (simple polynomials)")
    print("   2 → Medium  (multi-term polynomials)")
    print("   3 → Hard    (trig & exponentials)\n")
    while True:
        choice = input("  Enter 1 / 2 / 3: ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print(red("  Please enter 1, 2, or 3."))


def choose_topic():
    print("\n  Choose topic:")
    print("   1 → Differentiation")
    print("   2 → Integration")
    print("   3 → Mixed (random)\n")
    while True:
        choice = input("  Enter 1 / 2 / 3: ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print(red("  Please enter 1, 2, or 3."))


# ── Main game loop ────────────────────────────────────────────────────────────
def play_round(topic, level, num_questions=7):
    score = 0
    streak = 0
    best_streak = 0

    print(cyan(f"\n  ── Starting round: {num_questions} questions ──\n"))

    for q_num in range(1, num_questions + 1):
        # Pick question type
        if topic == "3":
            q_type = random.choice(["diff", "integ"])
        elif topic == "1":
            q_type = "diff"
        else:
            q_type = "integ"

        if q_type == "diff":
            question, correct, steps = make_differentiation(level)
            type_label = "Differentiate"
        else:
            question, correct, steps = make_integration(level)
            type_label = "Integrate"

        points = level * 10
        print(bold(f"  Q{q_num}/{num_questions}  [{type_label}]  (+{points} pts if correct)"))
        print(f"  {yellow(question)}\n")
        print("  Tips: use ** for powers (x**2), * for multiply (3*x)")
        print("        sin(x), cos(x), exp(x), log(x) are supported\n")

        attempts = 0
        answered = False
        while attempts < 2:
            raw = input("  Your answer: ").strip()
            if raw.lower() == "hint":
                print(cyan(f"\n  Hint — step-by-step:\n{steps}\n"))
                attempts += 2  # hint costs the attempt
                break

            user_expr = parse_answer(raw)
            if user_expr is None:
                print(red("  Couldn't parse that. Try again (e.g. 3*x**2 + 2*x)"))
                attempts += 1
                continue

            if answers_match(user_expr, correct):
                streak += 1
                best_streak = max(best_streak, streak)
                bonus = 5 if streak >= 3 else 0
                earned = points + bonus
                score += earned
                msg = f"  ✅  Correct! +{earned} pts"
                if bonus:
                    msg += f"  (🔥 streak bonus +{bonus}!)"
                print(green(bold(msg)))
                answered = True
                break
            else:
                attempts += 1
                streak = 0
                if attempts < 2:
                    print(red("  ✗  Not quite. One more try!\n"))

        if not answered:
            print(red(f"  ✗  The answer was: {sp.latex(correct)}"
                      + (" + C" if q_type == "integ" else "")))
            print(cyan(f"\n  Step-by-step:\n{steps}"))

        print()

    return score, best_streak


def main():
    banner()
    save = load_save()
    show_stats(save)

    while True:
        print("\n  ── Main Menu ──")
        print("   1 → Play")
        print("   2 → View my stats")
        print("   3 → How to enter answers (help)")
        print("   4 → Quit\n")
        choice = input("  Choose: ").strip()

        if choice == "1":
            topic = choose_topic()
            level = choose_level()
            score, best_streak = play_round(topic, level)

            # Update save
            save["total_score"] += score
            save["sessions"] += 1
            save["best_streak"] = max(save["best_streak"], best_streak)
            save["last_played"] = str(date.today())
            write_save(save)

            lvl_names = {1: "Easy", 2: "Medium", 3: "Hard"}
            print(yellow(bold(f"\n  ── Round Over ──")))
            print(yellow(f"  Score this round : {score}"))
            print(yellow(f"  Best streak      : {best_streak}"))
            print(yellow(f"  Total all-time   : {save['total_score']}\n"))

        elif choice == "2":
            show_stats(save)

        elif choice == "3":
            print(cyan("""
  ── How to type answers ──────────────────────────────
  Use standard Python/math notation:

  Powers     →  x**2  (not x^2)
  Multiply   →  3*x   (not 3x)
  Constants  →  sin(x), cos(x), exp(x), log(x)
  Fractions  →  x**3/3  or  Rational(1,3)*x**3

  Examples:
    3*x**2 + 2*x         ✓
    -cos(x)              ✓  (for ∫sin(x) dx)
    exp(x)               ✓  (for d/dx[e^x])

  You don't need to add + C for integrals.
  Type  hint  at any answer prompt for full steps.
  ─────────────────────────────────────────────────────
"""))

        elif choice == "4":
            print(cyan("\n  Thanks for playing CalcQuest! Keep practising 🚀\n"))
            break
        else:
            print(red("  Please enter 1–4."))


if __name__ == "__main__":
    main()
