import pytest
from datetime import date, timedelta

from project import (
    parse_date,
    get_priority_number,
    get_todays_tasks,
    get_upcoming_tasks,
    get_monthly_summary,
    get_next_id,
)


def test_parse_date():
    # Correctly converts a date string into a date object.
    assert parse_date("21/06/2026") == date(2026, 6, 21)

    # Raises ValueError when the date format is invalid.
    with pytest.raises(ValueError):
        parse_date("banana")


def test_get_priority_number():
    # High priority should come first, followed by Medium and Low.
    assert get_priority_number({"priority": "High"}) == 1
    assert get_priority_number({"priority": "Medium"}) == 2
    assert get_priority_number({"priority": "Low"}) == 3


def test_get_todays_tasks():
    # Returns an empty list when there are no tasks.
    assert get_todays_tasks([]) == []

    today = date.today().strftime("%d/%m/%Y")

    # Includes pending tasks due today.
    tasks = [{"id": 1, "title": "Task", "priority": "High", "due_date": today, "status": "pending",}]
    assert len(get_todays_tasks(tasks)) == 1

    # Skips tasks that have already been completed.
    tasks = [{"id": 1, "title": "Done", "priority": "High", "due_date": today, "status": "completed",}]
    assert get_todays_tasks(tasks) == []

    # Skips tasks that are due in the future.
    future = (date.today() + timedelta(days=5)).strftime("%d/%m/%Y")
    tasks = [{"id": 1, "title": "Future", "priority": "High", "due_date": future, "status": "pending",}]
    assert get_todays_tasks(tasks) == []

    # Sorts today's tasks by priority, with High priority first.
    tasks = [{"id": 1,"title": "Low", "priority": "Low", "due_date": today, "status": "pending",},
             { "id": 2, "title": "High", "priority": "High", "due_date": today, "status": "pending", },]

    result = get_todays_tasks(tasks)
    assert result[0]["title"] == "High"
    assert result[1]["title"] == "Low"


def test_get_upcoming_tasks():
    # Returns an empty list when there are no tasks.
    assert get_upcoming_tasks([]) == []

    # Includes pending tasks due within the next seven days.
    future = (date.today() + timedelta(days=3)).strftime("%d/%m/%Y")
    tasks = [{ "id": 1, "title": "Soon", "priority": "High", "due_date": future, "status": "pending",}]
    assert len(get_upcoming_tasks(tasks)) == 1

    # Excludes tasks due more than seven days from today.
    far = (date.today() + timedelta(days=10)).strftime("%d/%m/%Y")
    tasks = [{"id": 1, "title": "Far", "priority": "High", "due_date": far, "status": "pending",}]
    assert get_upcoming_tasks(tasks) == []
    today = date.today().strftime("%d/%m/%Y")

    # Excludes tasks due today because they belong in the daily section.
    tasks = [{ "id": 1, "title": "Today", "priority": "High", "due_date": today, "status": "pending",}]
    assert get_upcoming_tasks(tasks) == []

    # Sorts upcoming tasks by priority.
    d1 = (date.today() + timedelta(days=2)).strftime("%d/%m/%Y")
    d2 = (date.today() + timedelta(days=3)).strftime("%d/%m/%Y")

    tasks = [{"id": 1, "title": "Low", "priority": "Low", "due_date": d1, "status": "pending",},
             {"id": 2,"title": "High", "priority": "High", "due_date": d2, "status": "pending",},]
    result = get_upcoming_tasks(tasks)
    assert result[0]["title"] == "High"


def test_get_monthly_summary():
    # An empty task list should produce zero counts.
    completed, missed, upcoming = get_monthly_summary([])

    assert completed == 0
    assert missed == 0
    assert upcoming == []

    # Counts completed tasks correctly.
    tasks = [{"id": 1,"title": "Done", "priority": "High", "due_date": "01/01/2024", "status": "completed",}]
    completed, missed, upcoming = get_monthly_summary(tasks)
    assert completed == 1

    # Counts pending tasks with past due dates as missed.
    past = (date.today() - timedelta(days=5)).strftime("%d/%m/%Y")
    tasks = [{"id": 1, "title": "Missed", "priority": "Low", "due_date": past, "status": "pending",}]
    completed, missed, upcoming = get_monthly_summary(tasks)
    assert missed == 1

    # Includes pending tasks whose due dates have not passed.
    future = (date.today() + timedelta(days=5)).strftime("%d/%m/%Y")
    tasks = [{"id": 1, "title": "Upcoming", "priority": "Medium", "due_date": future, "status": "pending",}]
    completed, missed, upcoming = get_monthly_summary(tasks)
    assert len(upcoming) == 1


def test_get_next_id():
    # Starts IDs at 1 when there are no existing tasks.
    assert get_next_id([]) == 1

    # Generates the next ID after the highest existing ID.
    tasks = [{"id": 1}, {"id": 3}]
    assert get_next_id(tasks) == 4
