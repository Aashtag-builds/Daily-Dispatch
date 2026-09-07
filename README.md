# Daily Dispatch

A Python terminal productivity app for managing tasks, priorities, due dates, and progress.

Daily Dispatch stores tasks locally in JSON and provides a focused view of what needs attention today, what's coming up, and how much progress has been made. It also includes a small butler cat that reacts to the user's workload and completion progress.

## Features

* **Daily Dispatch** — View pending tasks due today, ordered by priority.
* **Upcoming Tasks** — See pending tasks due within the next 7 days.
* **Task Management** — Add, complete, and delete tasks.
* **Priority System** — Organize tasks as High, Medium, or Low priority.
* **Progress Summary** — Track completed, missed, and upcoming tasks.
* **Persistent Storage** — Tasks are saved locally using JSON.
* **Butler Cat** — A small character that reacts to workload and progress.
* **Input Validation** — Validates priorities, dates, and user input.

## How It Works

When the program starts, `main()` loads saved tasks from `data.json` and displays the main menu.

Each task is stored as a dictionary containing:

```text
id
title
priority
due_date
status
```

The program uses Python's built-in `json` module for persistent storage. Dates are entered in `DD/MM/YYYY` format and converted into Python `date` objects when comparisons or calculations are required.

A pending task is considered **missed** when its due date has passed; missed status is calculated rather than permanently stored.

## Project Structure

| File              | Purpose                                                                      |
| ----------------- | ---------------------------------------------------------------------------- |
| `project.py`      | Main application, task management, validation, dates, storage, and summaries |
| `cat.py`          | Butler cat faces, dialogue, mood logic, and display                          |
| `data.json`       | Local task storage                                                           |
| `test_project.py` | Automated tests using pytest                                                 |

## Design Decisions

The project went through several iterations before reaching its current form.

I initially planned separate structures for tasks, events, and deadlines, but realized that a task with a due date already covered most of that functionality. Removing unnecessary structures made the application simpler and easier to maintain.

I also considered a weekly summary and a larger multi-file architecture, but decided to focus on the features that directly supported the core purpose of the application.

JSON was chosen instead of a database because the project is a small local command-line application. It provides persistent, human-readable storage without introducing unnecessary infrastructure.

The cat was kept separate from the core application logic so that its personality could add character without interfering with task management or calculations.

## Testing

`test_project.py` uses `pytest` to test six core functions:

* `parse_date()`
* `get_priority_number()`
* `get_todays_tasks()`
* `get_upcoming_tasks()`
* `get_monthly_summary()`
* `get_next_id()`

The tests cover normal and edge cases including invalid dates, empty task lists, completed tasks, overdue tasks, future tasks, priority ordering, and ID generation.

Run the tests with:

```bash
pytest
```

## Running the Project

Clone the repository and run:

```bash
python project.py
```

Install the testing dependency with:

```bash
pip install -r requirements.txt
```

## What I Learned

Building Daily Dispatch taught me that good software design isn't about adding as many features as possible.

The project went through several iterations, including changes to its structure, date handling, task presentation, and feature scope. I learned to evaluate whether a feature actually solved a problem rather than adding complexity for its own sake.

The biggest shift in my approach was moving from:

> **"What else can I add?"**

to:

> **"What does the program actually need?"**

That principle shaped the final version of Daily Dispatch: smaller than the original idea, but more focused, deliberate, and testable.

## Video Demo

[Watch the Video Demo](https://youtu.be/RJRo_vbeVQE)

## Tech Stack

* Python
* JSON
* pytest
* Command-line interface
