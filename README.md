# ⚡ Async Calculator 🧮  
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white&style=flat-square)
![AsyncIO](https://img.shields.io/badge/Async-Enabled-44CC11?style=flat-square&logo=python)
![Rich TUI](https://img.shields.io/badge/TUI-Rich-CC0066?style=flat-square&logo=console)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

---

<div align="center">

### 🧠 **Full-Fledged Asynchronous CLI Calculator**  
A modern, non-blocking **Python 3.9+** calculator powered by `asyncio`, `classes`, and `Rich` TUI styling.  
Supports advanced math, memory ops, concurrent evaluations — all in a beautiful command line experience 🎨  

<img src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="480" alt="Python Animated GIF" />

</div>

---

## ✨ Features

✅ **Async & Non-Blocking** (uses `asyncio`)  
✅ **Safe Expression Evaluation** via `ast` (no `eval()` 🚫)  
✅ Handles **multiple operators & parentheses**  
✅ Advanced Math: `sin`, `cos`, `tan`, `sqrt`, `log`, `fact`, `abs`, etc.  
✅ **Memory Support:** store, recall, clear  
✅ **Batch & Concurrent Modes** for large computations  
✅ **Rich TUI** — colorful panels, prompts, tables 💅  
✅ Fully **offline & cross-platform**

---

## 🎥 Demo Preview

> Try it yourself!  
>  
> ![Async Calculator Demo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWdpbHB4Y3FwN2Fmb3ZmbnpwdHRldThzdmh3MWtxYzkwODJwOWp2ZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26u4nJPf0JtQPdStq/giphy.gif)

---

## 🛠️ Installation

```bash
# 1️⃣ Clone the repo
git clone https://github.com/<your-username>/async-calculator.git
cd async-calculator

# 2️⃣ (Optional) create virtual environment
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# 3️⃣ Install dependency
pip install rich

# 4️⃣ Run
python async_calculator.py
````

---

## 🧩 Usage

```bash
# 🧮 Single Expression
> 3 * (4 + 5)
Result: 27

# 🧠 Advanced Math
> sin(90) + cos(0)
Result: 2.0

# 🗃️ Batch Mode
> 2 + 2
> sqrt(81)
> fact(5)
> [press Enter on empty line to run all]

# 🚀 Concurrent Mode
Evaluate multiple expressions simultaneously!
```

---

## 🧮 Supported Syntax

| Category          | Supported Examples                                   |
| ----------------- | ---------------------------------------------------- |
| **Arithmetic**    | `+`, `-`, `*`, `/`, `%`, `**`, parentheses `( )`     |
| **Power (Alt)**   | `^` auto-converted to `**`                           |
| **Trigonometry**  | `sin(x)`, `cos(x)`, `tan(x)` *(degrees)*             |
| **Advanced Math** | `sqrt(x)`, `log(x)`, `log10(x)`, `fact(n)`, `abs(x)` |
| **Constants**     | `pi`, `e`                                            |
| **Memory**        | `mem()`, store, recall, clear                        |

---

## ⚙️ Architecture Overview

```
async_calculator.py
├── Calculator class (async)
├── SafeEvaluator (AST-based parser)
├── Rich-based TUI
└── Batch & Concurrent async execution
```

---

## 🌈 Example Screenshot

![Calculator Screenshot](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2R2aHYzYjM5MHFpMmJoemppZWpsZm9kbWxzMmd4M2pvN2x1dmJ5dyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/tXL4FHPSnVJ0A/giphy.gif)

---

## 💻 Tech Stack

| Component | Description                      |
| --------- | -------------------------------- |
| 🐍 Python | Core language                    |
| ⚡ asyncio | Async event loop for concurrency |
| 🎨 Rich   | Beautiful TUI elements           |
| 🔒 ast    | Safe expression parsing          |

---

## 🪄 Future Roadmap

* [ ] Add **Textual GUI** with live layout
* [ ] Add **History Recall** (↑ key)
* [ ] Add **Degree/Radian switch**
* [ ] Add **Export results to file**

---

## 🧑‍💻 Author

**Pinaka**
🌐 [GitHub](https://github.com/raxku2) 
Made with 🤖 using Python & Rich ⚡

---

## 📜 License

Licensed under the [MIT License](LICENSE)

---

<div align="center">

![Footer Banner](https://capsule-render.vercel.app/api?type=waving\&color=0:000000,100:444444\&height=80\&section=footer\&text=Async%20Calculator%20🧮\&fontColor=ffffff\&fontSize=24)

</div>
