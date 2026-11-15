# 🛠️ Fine Tuner

**Welcome to Fine Tuner!** 

If you've ever asked an AI a question and got a terrible, generic answer, it's usually because the prompt was weak. Fine Tuner is a simple, zero-dependency Python project designed to fix that. It grades your raw prompts and automatically rewrites them into structured, highly detailed formats that AIs actually understand.

This project was built from scratch by a 3rd-year B.Tech student working alongside an "AI Solutions Architect." We stripped away all the complicated external libraries and built this using purely Python's standard library (plus Gradio for the web UI).

---

## ✨ What does it actually do?

Fine Tuner works in three simple steps:
1. **Lints your prompt:** It uses a custom scoring system to grade your prompt from **A to F**. It checks if you're being too vague or missing important details.
2. **Optimizes your prompt:** If your prompt is weak (like "write a python function"), it wraps your idea in a structured "Chain-of-Thought" template. It adds a role, clear objectives, and formatting rules.
3. **Estimates Tokens:** It tells you roughly how many "tokens" (pieces of words) your prompt is, so you don't accidentally crash the AI's memory limit.

---

---

## 🏭 Here is the simplest way to understand what every file does.

### ⚙️ The "Brain" Files (The Logic)
These files do the actual work behind the scenes. They don't have buttons or screens; they just do the math.

token_estimator.py (The Calculator)

What it does: Counts the words and characters to guess how many "tokens" (AI word pieces) your prompt is. It prevents you from sending a message so big that the AI crashes.

Uses: Basic Python math (math).

linter.py (The English Teacher)

What it does: Reads your prompt and grades it from A to F. If your prompt is too short or missing keywords like "context" or "role," it deducts points and gives you feedback.

Uses: Regex (re) – which is just a way for Python to search for specific patterns in words.

optimizer.py (The Editor)

What it does: Takes your bad prompt and fixes it. It wraps your prompt in a fancy "XML" template (adding a role, goal, and formatting rules) so the AI gives you a much better answer.

Uses: Just pure Python logic.

### 🎮 The "Control" Files (The Interfaces)
These files are how you (the human) interact with the brain.

app.py (The Showroom / Front Door)

What it does: This creates the beautiful web page you see in your browser. It has the split-screen, the text boxes, and the buttons. When you click a button, it asks linter.py and optimizer.py for the answers.

Uses: Gradio (a magical library that builds web pages using Python).

cli.py (The Remote Control)

What it does: This is for hardcore users. It lets you use the tool by typing commands into the black terminal screen (like python cli.py lint "my prompt") instead of clicking buttons on a website.

Uses: argparse (Python's built-in tool for reading terminal commands).

### 🛠️ The "Maintenance" Files (The Setup)
These files make sure the app runs smoothly when you share it with the world.

test_engine.py (The Quality Inspector)

What it does: This is a robot that tests the app for you. It automatically throws bad prompts at your code to make sure it doesn't crash. If you break something, this file will yell at you.

Uses: unittest (Python's built-in testing tool).

setup.py (The Installation Manual)

What it does: If you wanted to install this app on your computer like a real program (so you could just type finetuner anywhere in your terminal), this file tells the computer how to do it.

Uses: setuptools.

requirements.txt (The Shopping List)

What it does: When you put your app on the internet (like Render), the server reads this list to know what to download. In our case, it literally just says gradio.

Uses: Plain text.



---

## 🚀 How to use it (For Non-Techies)

You can use Fine Tuner in two ways: the beautiful Web UI, or the hardcore Terminal CLI.

### Option 1: The Web UI (Recommended)
1. Make sure you have Python installed.
2. Open your terminal (Command Prompt) in the project folder.
3. Install Gradio by typing: `pip install -r requirements.txt`
4. Start the app by typing: `python app.py`
5. Open your web browser and go to `http://localhost:7860`. Paste your prompt and watch the magic happen!

### Option 2: The Terminal (CLI)
If you prefer the terminal, you can use these commands:
*   `python cli.py lint "your weak prompt here"` (Grades it)
*   `python cli.py optimize "your weak prompt here"` (Rewrites it)
*   `python cli.py diff "prompt A" "prompt B"` (Compares token sizes)
*   `python cli.py history` (Shows your past prompts)

---

## 🧠 The "Behind the Scenes" Prompts (How we built this)

To build this project perfectly without messy code, we used the **Self-Refine technique**. We gave the AI strict instructions to draft the code, critique its own work like a QA tester, fix the bugs, and *then* output the final file.

If you want to rebuild or expand this project, here are the exact 5 Meta-Prompts we used:

### Window 1: Core Engine (`token_estimator.py`)

<System_Context>
You are an expert Python developer building the "Fine Tuner" application. 
Project Root Path: D:\projects\FineTuner
</System_Context>
<Strict_Rules>
1. Use ONLY Python standard libraries. NO external dependencies.
2. Do NOT hardcode values; use config dictionaries.
3. Add casual, easy-to-understand comments.
4. Target code quality: 9/10 or higher.
</Strict_Rules>
<Task>
Create the file `token_estimator.py`. It must contain a function to estimate token count from a string, a dictionary of model context limits, and a function to check if a prompt exceeds the limit.
</Task>
<Self_Refine_Protocol>
Act as the Programmer, then the QC Tester. Draft, critique, refactor, and output ONLY the final code.
</Self_Refine_Protocol>
```

### Window 2: The Brain (`linter.py` & `optimizer.py`)

<System_Context>
You are an expert Python developer building the "Fine Tuner" application.
</System_Context>
<Task>
Create two files:
1. `linter.py`: Contains a function `grade_prompt(prompt)`. It uses regex to check for vagueness and grade the prompt A-F.
2. `optimizer.py`: Contains a function `optimize_prompt(prompt)`. It wraps raw user input into an XML/Chain-of-Thought structure.
</Task>
<Self_Refine_Protocol>
Act as the Programmer, then the QC Tester. Draft, critique (look for regex edge cases), refactor, and output ONLY the final code.
</Self_Refine_Protocol>
```

### Window 3: Command Line Interface (`cli.py`)
```text
<System_Context>
You are an expert Python developer building the "Fine Tuner" application.
</System_Context>
<Task>
Create `cli.py` using `argparse`. It must import your previous modules. It must support these commands: `lint`, `optimize`, `diff` (show token differences), and `history` (save/retrieve prompts to a local JSON file).
</Task>
<Self_Refine_Protocol>
Act as the Programmer, then the QC Tester. Draft, critique (does it handle JSON file errors?), refactor, and output ONLY the final code.
</Self_Refine_Protocol>
```

### Window 4: Web UI (`app.py`)
*(Note: We pivoted from standard HTTP to Gradio for a better UI).*
```text
<System_Context>
You are an expert Python developer building the "Fine Tuner" application.
</System_Context>
<Task>
Create `app.py` using Gradio. Build a dual-pane UI (left: raw prompt, right: optimized). Connect the "Process" button to the linter and optimizer functions. Use a custom Gradio theme to make it look professional.
</Task>
<Self_Refine_Protocol>
Act as the Programmer, then the QC Tester. Draft, critique (are the outputs mapped correctly?), refactor, and output ONLY the final code.
</Self_Refine_Protocol>
```

### Window 5: Testing & Packaging

<System_Context>
You are an expert Python developer finalizing the "Fine Tuner" application.
</System_Context>
<Task>
Create `test_engine.py` using `unittest` to test the linter and optimizer. Test edge cases like empty strings. Create `setup.py` so the app can be installed locally.
</Task>
<Self_Refine_Protocol>
Act as the Programmer, then the QC Tester. Draft, critique (are edge cases covered?), refactor, and output ONLY the final code.
</Self_Refine_Protocol>
```

---

## 🌐 Deployment
This app is deployed using **Render**. Because it uses Gradio, Render automatically detects the Python environment, installs Gradio, and launches `app.py` as a web service. 

*(https://fine-tuner.onrender.com it's live!)*

---
*Built with 🧠 and ☕ by almostpm.*
```
