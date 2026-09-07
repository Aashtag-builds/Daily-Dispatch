import random

# Different cat faces used to represent the user's current workload or progress.
CAT_FACES = {
    "normal": "( =^.^= )",
    "busy": "( ;.; )",
    "worried": "( o.o )",
    "done": "( ^.^ )~♡",
    "excellent": "( ^.^ )~♡",
    "good": "( =^.^= )",
    "okay": "( -.- )",
    "bad": "( ;.; )",
    }

# Randomized responses for the daily brief based on workload and upcoming tasks.
DAILY_QUOTES = {
    "busy": [
        "Oh my. {n} tasks, my lady. I've already started stress-brewing tea.",
        "Milady, {n} tasks. May I inquire what happened to the royal calendar?",
        "Your schedule is... ambitious today, your highness. very well. 💅",
        "{n} tasks. I've seen lighter days at the palace, my queen.",
        "My queen, your day is STACKED. I recommend we lock in immediately. ☕",
        "I do hate to alarm you, milady, but your to-do list is giving... chaos.",],
    "normal": [
        "A manageable day, my lady. just the way I like it.",
        "{n} tasks. Quite manageable, my queen. Shall we proceed?",
        "Light duties today, your highness. how very civilized.",
        "Not too bad, milady. {n} tasks. I believe we can handle this. ♡",
        "{n} tasks. I shall prepare the tea, milady.",
        "A rather pleasant task list, your grace. I am pleased with the current outlook.",],
    "worried": [
        "A word of caution, my lady — a deadline approaches rather quickly.",
        "Milady. I regret to inform you that there is a deadline approaching. Like... VERY soon.",
        "I noticed a deadline looming, milady. I've already panic-organized your desk.",
        "Your highness, we appear to have a PROBLEM. Deadline incoming. 🚨",
        "Your highness, I do hate to alarm you, but time is... not on our side.",
        "Milady, I would like to formally flag an increasingly imminent deadline. 😭",],
    "done": [
        "Absolutely nothing on the list, milady. shall I run you a bath?",
        "NO TASKS?? My queen, you have successfully conquered the royal schedule. absolutely magnificent.",
        "The schedule is clear, your highness. how lovely for you.",
        "You finished everything?? My lady, I am genuinely impressed. ✨",
        "No tasks? I... don't know what to do with my paws, your highness.",
        "The list is completely clear, milady. Productivity levels are exemplary. 💅",],
    "upcoming": [
        "A word of caution, my lady — {n} future tasks await.",
        "Milady, please be advised — {n} tasks are approaching.",
        "I've noted {n} upcoming tasks, milady. I do hope you're pacing yourself.",
        "Your highness, {n} tasks are currently awaiting your attention. Consider this your formal notice.",
        "{n} tasks loom in your near future, your highness. I've stocked extra tea.",
        "Milady, {n} future tasks have been identified. I recommend strategic preparation. 💅",],}

# Randomized responses for the monthly summary based on task completion.
MONTHLY_QUOTES = {
    "excellent": [
        "ALL tasks completed?? milady, you are simply... magnificent. 💅",
        "My queen. You have successfully completed EVERYTHING. I am SPEECHLESS. 👑",
        "100% completion rate. Your highness, the palace is PROUD. ✨",
        "You have exceeded operational expectations, my lady. Absolutely stellar. ♡",
        "Every. Single. Task. Done. Milady, you're making me emotional. 😭💅",
    ],

    "good": [
        "Most tasks completed, my lady. a commendable month indeed.",
        "A very satisfactory performance, milady. I believe we are making excellent progress. ♡",
        "My queen, the majority of your tasks have been successfully completed. I am pleased. 💅",
        "Your highness, the numbers look good. very good. i'm pleased.",
        "A solid month, queen. The palace salutes you. 👑",
    ],

    "okay": [
        "Some tasks got away from us, milady. but we move.",
        "Your Grace, this month's performance was... adequate. There is room for improvement.",
        "Your highness, half the tasks done. Shall we aim higher next month?",
        "Milady, we have completed a respectable portion of the workload. Further optimization may be required.",
        "A mixed month, queen. But you showed up. That counts. ♡",
    ],

    "bad": [
        "My lady... most tasks were missed. shall we... discuss this??",
        "Milady. I believe we need to review this month's performance. 😭",
        "Your Grace, a significant number of tasks remain pending. I shall refrain from commenting further. 💅",
        "Your highness, the monthly report is... concerning. Shall I reschedule everything?",
        "Milady, we missed quite a few tasks. But you know what? New month, new you. ✨",
    ],

    "missed_zero": [
        "NOTHING missed?? milady, you're absolutely flawless. 💅",
        "Zero missed tasks. My queen, you are officially undefeated. 👑",
        "Milady, not a single task missed. An exemplary performance. ✨",
        "Your highness, perfect record. I am literally bowing right now. 🙇",
    ],
}
def get_cat_art(mood):
    face = CAT_FACES.get(mood, "( =^.^= )")
    return (
        f"    /\\_/\\\n"
        f"   {face}\n"
        f"    > ♡ <\n"
        f"   /|   |\\\n"
        f"  (_|   |_)"
    )

# Determines the cat's daily mood from today's task count and upcoming tasks.
def get_daily_mood(today_count, upcoming_count):
    if today_count == 0 and upcoming_count == 0:
        return "done"
    elif today_count >= 5:
        return "busy"
    elif upcoming_count >= 3:
        return "worried"
    else:
        return "normal"


def show_daily_cat(today_count, upcoming_count):
    mood = get_daily_mood(today_count, upcoming_count)
    print(get_cat_art(mood))

    # Upcoming warning first if tasks exist
    if upcoming_count > 0:
        quotes = DAILY_QUOTES.get("upcoming", ["You've got tasks coming."])
        quote = random.choice(quotes).format(n=upcoming_count)
        print(f'\n  "{quote}"')

    # Then today's mood quote
    if today_count == 0 and upcoming_count == 0:
        quotes = DAILY_QUOTES.get("done", ["All clear!"])
        quote = random.choice(quotes)
        print(f'\n  "{quote}"\n')
    elif today_count >= 5:
        quotes = DAILY_QUOTES.get("busy", ["Busy day!"])
        quote = random.choice(quotes).format(n=today_count)
        print(f'\n  "{quote}"\n')
    else:
        quotes = DAILY_QUOTES.get("normal", ["Let's go!"])
        quote = random.choice(quotes).format(n=today_count)
        print(f'\n  "{quote}"\n')


def get_monthly_mood(completed, missed):
    total = completed + missed
    if total == 0:
        return "good"
    ratio = completed / total

    if ratio == 1.0:
        return "excellent"
    elif ratio >= 0.7:
        return "good"
    elif ratio >= 0.4:
        return "okay"
    else:
        return "bad"


def show_monthly_cat(completed, missed):
    mood = get_monthly_mood(completed, missed)
    print(get_cat_art(mood))

    if missed == 0 and completed > 0:
        quotes = MONTHLY_QUOTES.get("missed_zero", ["Perfect!"])
        quote = random.choice(quotes)
    else:
        quotes = MONTHLY_QUOTES.get(mood, ["Keep going!"])
        quote = random.choice(quotes)

    print(f'\n  "{quote}"\n')
