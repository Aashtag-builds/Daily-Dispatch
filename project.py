import sys
import json
from datetime import date, datetime, timedelta
from cat import show_daily_cat, show_monthly_cat


# Converts a DD/MM/YYYY string into a date object for comparisons and calculations.
def parse_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y").date()

# Assigns a numerical value to each priority so tasks can be sorted.
def get_priority_number(t):
    if t["priority"] == "High":
        return 1
    elif t["priority"] == "Medium":
        return 2
    else:
        return 3

# Loads saved tasks from data.json, or returns an empty list if the file does not exist.
def load_tasks():
    try:
        with open("data.json", "r") as f:
            return json.load(f)["tasks"]
    except FileNotFoundError:
        return []

# Saves the current task list to data.json so it persists between program runs.
def save_tasks(tasks):
    with open("data.json", "w") as f:
        json.dump({"tasks": tasks}, f, indent=4)

# Returns pending tasks due today, sorted from highest to lowest priority.
def get_todays_tasks(tasks):
    today = date.today().strftime("%d/%m/%Y")

    today_tasks = []
    for t in tasks:
        if t["due_date"] == today and t["status"] == "pending":
            today_tasks.append(t)

    today_tasks.sort(key=get_priority_number)
    return today_tasks

# Returns pending tasks due within the next specified number of days.
def get_upcoming_tasks(tasks, days=7):
    today = date.today()
    cutoff = today + timedelta(days=days)

    upcoming = []
    for t in tasks:
        due = parse_date(t["due_date"])
        if due > today and due <= cutoff and t["status"] == "pending":
            upcoming.append(t)

    upcoming.sort(key=get_priority_number)
    return upcoming

# Counts completed and missed tasks and collects pending tasks that are not yet overdue.
def get_monthly_summary(tasks):
    today = date.today()

    completed = 0
    missed = 0
    upcoming = []

    for t in tasks:
        due = parse_date(t["due_date"])
        if t["status"] == "completed":
            completed += 1
        elif t["status"] == "pending" and due < today:
            missed += 1
        elif t["status"] == "pending" and due >= today:
            upcoming.append(t)

    return completed, missed, upcoming

# Validates a user-entered date and asks for confirmation if the date is in the past.
def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            entered = datetime.strptime(date_str, "%d/%m/%Y").date()
            if entered < date.today():
                confirm = input(
                    "That date is in the past. Add anyway? (y/n): "
                ).strip().lower()
                if confirm != "y":
                    continue
            return date_str
        except ValueError:
            print("Invalid. Use DD/MM/YYYY.")

# Validates that the user enters one of the three supported priority levels.
def get_valid_priority(prompt):
    while True:
        priority = input(prompt).strip().capitalize()
        if priority in ["High", "Medium", "Low"]:
            return priority
        print("Invalid. Enter High, Medium, or Low.")

# Displays today's pending tasks and tasks due within the next seven days.
def view_daily_dispatch(tasks):
    today_tasks = get_todays_tasks(tasks)
    upcoming = get_upcoming_tasks(tasks)
    today = date.today().strftime("%d/%m/%Y")

    print("\n╭──────────────────────────────────╮")
    print("│          ✦ DAILY DISPATCH ✦         │")
    print(f"│          {today}              │")
    print("╰──────────────────────────────────╯\n")

    show_daily_cat(len(today_tasks), len(upcoming))

    # Display today's tasks.
    print("TODAY'S TASKS")
    print("─" * 36)
    if today_tasks:
        for t in today_tasks:
            if t["priority"] == "High":
                print(f" 🌟 {t['title']}")
            elif t["priority"] == "Medium":
                print(f" 🎀 {t['title']}")
            else:
                print(f"  🧶 {t['title']}")
    else:
        print("  No tasks today.")

    # Display pending tasks due within the next seven days.
    print("\nUPCOMING")
    print("─" * 36)
    if upcoming:
        for t in upcoming:
            if t["priority"] == "High":
                print(f"  🌟 {t['title']}  (due: {t['due_date']})")
            elif t["priority"] == "Medium":
                print(f"  🎀 {t['title']}  (due: {t['due_date']})")
            else:
                print(f" 🧶 {t['title']}  (due: {t['due_date']})")
    else:
        print("  Nothing upcoming.")

    print("\n" + "═" * 36)

# Displays the number of completed, missed, and upcoming tasks.
def view_monthly_summary(tasks):
    completed, missed, upcoming = get_monthly_summary(tasks)

    print("\n╭──────────────────────────────────╮")
    print("│       ✦ MONTHLY SUMMARY ✦        │")
    print("╰──────────────────────────────────╯\n")

    show_monthly_cat(completed, missed)

    print(f"  Completed : {completed}")
    print(f"  Missed    : {missed}")
    print(f"  Upcoming  : {len(upcoming)}")
    print("\n" + "═" * 36)

# Generates a new ID by finding the highest existing ID and adding one.
def get_next_id(tasks):
    if not tasks:
        return 1

    highest = 0
    for t in tasks:
        if t["id"] > highest:
            highest = t["id"]

    return highest + 1

# Collects task information from the user and saves the new task.
def add_task(tasks):
    print("\n--- Add Task ---")
    title = input("Title: ").strip()
    priority = get_valid_priority("Priority (High/Medium/Low): ")
    due_date = get_valid_date("Due date (DD/MM/YYYY): ")

    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "status": "pending",
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added! ♡")

# Lets the user select and permanently remove a task from the list.
def delete_task(tasks):
    if not tasks:
        print("\nNo tasks to delete.")
        return

    print("\n--- Delete Task ---")
    for i, t in enumerate(tasks, 1):
        print(f"  {i}. {t['title']} (due: {t['due_date']})")

    while True:
        choice = input("Enter number (or 'cancel'): ").strip()
        if choice.lower() == "cancel":
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(tasks):
                tasks.pop(index)
                save_tasks(tasks)
                print("Deleted! ♡")
                return

            print("Invalid number.")
        except ValueError:
            print("Invalid input.")

# Lets the user select a pending task and change its status to completed.
def mark_complete(tasks):
    pending = []
    for t in tasks:
        if t["status"] == "pending":
            pending.append(t)

    if not pending:
        print("\nNo tasks to complete.")
        return

    print("\n--- Mark Complete ---")
    for i, t in enumerate(pending, 1):
        print(f"  {i}. {t['title']}")

    while True:
        choice = input("Enter number (or 'cancel'): ").strip()
        if choice.lower() == "cancel":
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(pending):
                pending[index]["status"] = "completed"
                save_tasks(tasks)
                print("Done! ♡")
                return

            print("Invalid number.")
        except ValueError:
            print("Invalid input.")

# Runs the main menu and directs the user to each feature.
def main():
    tasks = load_tasks()

    while True:
        print("\n=== Main Menu ===")
        print("1. View Daily Dispatch")
        print("2. View Monthly Summary")
        print("3. Add Task")
        print("4. Mark Task Complete")
        print("5. Delete Task")
        print("6. Quit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            view_daily_dispatch(tasks)
        elif choice == "2":
            view_monthly_summary(tasks)
        elif choice == "3":
            add_task(tasks)
        elif choice == "4":
            mark_complete(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            print("Goodbye! ♡")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
