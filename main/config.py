ICONS_PATH = "main/images/"
ICONS = {
    "dashboard": ICONS_PATH + "dashboard.svg",
    "health": ICONS_PATH + "health.svg",
    "challenges": ICONS_PATH + "challenges.svg",
    "assignments": ICONS_PATH + "assignments.svg",
    "quizzes": ICONS_PATH + "quizzes.svg",
    "progress": ICONS_PATH + "progress.svg",
}

SIDEBAR_ITEMS = {
    "student": [
        {"name": "dashboard", "icon": ICONS["dashboard"]},
        {"name": "health", "icon": ICONS["health"]},
        {"name": "challenges", "icon": ICONS["challenges"]},
        {"name": "assignments", "icon": ICONS["assignments"]},
        {"name": "quizzes", "icon": ICONS["quizzes"]},
    ],
    "teacher": [
        {"name": "dashboard", "icon": ICONS["dashboard"]},
        {"name": "health", "icon": ICONS["health"]},
        {"name": "progress", "icon": ICONS["progress"]},
        {"name": "assignments", "icon": ICONS["assignments"]},
    ],
    "parent": [
        {"name": "dashboard", "icon": ICONS["dashboard"]},
        {"name": "health", "icon": ICONS["health"]},
        {"name": "progress", "icon": ICONS["progress"]},
    ],
}