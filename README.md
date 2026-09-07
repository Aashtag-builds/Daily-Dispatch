# Daily Dispatch

Daily Dispatch is a personal Python terminal application that helps me keep track of tasks, priorities, due dates, and progress. It stores tasks locally in a JSON file and provides a daily dispatch, an upcoming-task section, and a progress summary. It also includes a small butler cat that reacts to the user's workload and progress.

The final version is intentionally simple, but getting there involved several iterations. I changed the project structure, removed features that were adding unnecessary complexity, improved date handling, redesigned how tasks were presented, and rebuilt parts of the program before arriving at the final design.

## How It Works

When the program starts, `main()` loads the saved tasks from `data.json` and displays a menu. The user can view the Daily Dispatch, view the summary, add a task, mark a task as completed, delete a task, or quit.

Each task is stored as a dictionary containing an `id`, `title`, `priority`, `due_date`, and `status`. The status is either `pending` or `completed`.

When adding a task, the program asks for a title, priority, and due date. `get_valid_priority()` ensures that the priority is High, Medium, or Low. `get_valid_date()` checks that the date follows the `DD/MM/YYYY` format and asks for confirmation if a past date is entered. `get_next_id()` generates a new ID based on the highest existing ID.

Tasks are stored using Python's built-in `json` module. `save_tasks()` writes the current task list to `data.json`, while `load_tasks()` retrieves it when the program starts. This allows tasks to persist between program runs without requiring a database.

The Daily Dispatch uses `get_todays_tasks()` to find pending tasks due today and sorts them by priority, with High priority tasks appearing first. `get_upcoming_tasks()` looks ahead seven days so that tasks approaching their due dates remain visible instead of disappearing until the day they are due.

The summary uses each task's status and due date to calculate completed, missed, and upcoming tasks. A task does not receive a permanent `missed` status. Instead, a pending task is considered missed when its due date has already passed.

## How I Arrived at the Final Design

My original idea was considerably larger. I initially planned separate structures for tasks, events, and deadlines, along with several Python files separating different parts of the application.

At first, this seemed like good software engineering because I was trying to apply ideas such as modularity and separation of concerns. However, as I developed the project, I realized that I was creating an architecture for a much larger application than I actually needed.

For example, events and deadlines were ultimately unnecessary because a task could already have a due date. I removed them rather than maintaining separate structures and additional logic.

I also considered implementing a weekly summary, but decided that it added complexity without providing enough value for this version. Removing it allowed me to focus on the core purpose of the application: helping the user see what needs attention and keep track of progress.

At one point, I had modified the original program so many times that it was becoming difficult to understand. Instead of continuing to patch the same code, I decided to rebuild it. I first identified the functions the application actually needed and then implemented them individually before connecting them through `main()`.

The final project is therefore split into two Python files:

* **`project.py`** contains the main application, task management, data storage, validation, date handling, Daily Dispatch, upcoming tasks, and summary logic.
* **`cat.py`** contains the cat's faces, dialogue, mood logic, and display functions.

I kept `cat.py` separate because the program contains many dialogue strings. Keeping them outside `project.py` makes the main application logic easier to read without introducing unnecessary complexity.

## Important Design Decisions

One of my main design choices was using JSON instead of a database. For a command-line application of this size, a database would add unnecessary complexity. JSON provides persistent storage using Python's built-in `json` module while keeping the stored data human-readable.

I chose `DD/MM/YYYY` because it is more natural for the user to enter and read. Internally, `parse_date()` converts these strings into Python `date` objects whenever the program needs to compare dates or perform calculations.

I also separated task-processing logic from display logic. Functions such as `get_todays_tasks()` and `get_upcoming_tasks()` calculate and return information, while the display functions handle how that information is presented. This made the logic easier to test and the program easier to organize.

Another important decision was making priority central to the Daily Dispatch. Instead of displaying tasks simply in the order they were created, the program sorts them by importance so that the user can immediately see what deserves attention first.

## Giving the Program a Personality

I wanted Daily Dispatch to feel more personal than a standard command-line task manager.

My original idea was for the cat to have a dialogue box containing the daily dispatch. However, the character and the actual information were competing for the same purpose. I therefore kept the dispatch structured and readable while making the cat react to it.

The cat has different moods based on the user's workload and completion rate. A heavy workload can make it busy or worried, while completing tasks can make it happier. Multiple responses are stored for different situations, and Python's `random` module selects between them so that the program does not feel exactly the same every time.

I kept the cat's personality separate from the core task-management logic. This means the character can make the application more enjoyable without interfering with the actual task data or calculations.

## Iteration and Testing

One of the biggest changes I made was the date system. I initially used `YYYY-MM-DD`, which is convenient for programming, but eventually changed it to `DD/MM/YYYY` because it was more readable for the user. This affected validation, comparisons, and date calculations, so I had to update several parts of the program.

I also realized that showing only tasks due today was not enough. An important task due tomorrow could completely disappear from the user's view. I therefore added the **Upcoming** section, which shows pending tasks due within the next seven days.

This project includes `test_project.py`, which uses `pytest` to test six core functions: `parse_date()`, `get_priority_number()`, `get_todays_tasks()`, `get_upcoming_tasks()`, `get_monthly_summary()`, and `get_next_id()`.

The tests cover both normal and edge cases, including invalid dates, empty task lists, completed tasks, future and overdue tasks, priority ordering, and ID generation. Writing these tests also helped me think about whether the functions behaved correctly beyond the examples I had manually tried.

## What I Learned

The biggest lesson I learned from Daily Dispatch was that good software design is not about making a project as complicated as possible.

I initially thought that more features, more files, and more abstractions would automatically make the project better. Instead, I learned to ask whether each feature actually solved a problem.

I also learned how interconnected design decisions can be. Changing a date format affected multiple parts of the program, adding completion tracking changed how summaries worked, and adding the cat required thinking about how program data could influence the user experience.

Most importantly, I learned to move from **"What else can I add?"** to **"What does the program actually need?"**

The final version of Daily Dispatch is smaller than my original idea, but it is more deliberate. I built it, tested it, changed it, simplified it, rebuilt it, and learned from the process.
