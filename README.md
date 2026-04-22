# 🧮 CalcQuest – Calculus Learning Game

An interactive Python quiz game to help students learn and practise **differentiation** and **integration** through randomised questions, hints, and streak-based scoring.

---

## 🎮 Features

- **3 difficulty levels** — Easy (polynomials), Medium (multi-term), Hard (trig & exponentials)
- **3 modes** — Differentiation only, Integration only, or Mixed
- **SymPy-powered answer checking** — accepts any mathematically equivalent form, not just exact matches
- **Hints** — type `hint` at any question to see a full step-by-step solution
- **Streak bonuses** — get a +5 bonus for 3 correct answers in a row 🔥
- **Session tracking** — saves your total score, best streak, and last played date

---

## 🚀 How to Run

**1. Install Python** (3.8 or above) from [python.org](https://python.org)

**2. Install the required library:**
```bash
pip install sympy
```

**3. Run the game:**
```bash
python calcquest.py
```

---

## 🕹️ How to Play

- Choose a topic: Differentiation / Integration / Mixed
- Choose a difficulty level: 1 (Easy) → 3 (Hard)
- Answer 7 questions per round
- Type answers using standard Python math notation:

| Math | Type this |
|------|-----------|
| x²   | `x**2`    |
| 3x   | `3*x`     |
| sin(x) | `sin(x)` |
| eˣ   | `exp(x)`  |

- Type `hint` instead of an answer to see the full solution (costs your attempt)
- You don't need to add `+ C` for integration answers

---

## 📁 Files

```
calcquest.py          # Main game file
calcquest_save.json   # Auto-generated — stores your progress
```

---

## 🛠️ Built With

- Python 3
- [SymPy](https://www.sympy.org/) — symbolic mathematics library

---

## 👩‍💻 Author

**Ananya J** — 2nd Year B.Tech CSE, Anurag University  
[GitHub](https://github.com/nyanya0) · [LinkedIn](https://linkedin.com/in/ananya-j-748265357)
