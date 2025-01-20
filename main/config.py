ICONS_PATH = "main/images/"
ICON_PATH = {
    "dashboard": ICONS_PATH + "dashboard.svg",
    "health": ICONS_PATH + "health.svg",
    "challenges": ICONS_PATH + "challenges.svg",
    "assignments": ICONS_PATH + "assignments.svg",
    "quizzes": ICONS_PATH + "quizzes.svg",
    "progress": ICONS_PATH + "progress.svg",
    "settings": ICONS_PATH + "settings.svg",
}

SIDEBAR_ITEMS = {
    "student": [
        {"name": "dashboard", "icon": ICON_PATH["dashboard"]},
        {"name": "health", "icon": ICON_PATH["health"]},
        {"name": "challenges", "icon": ICON_PATH["challenges"]},
        {"name": "settings", "icon": ICON_PATH["settings"]},
    ],
    "teacher": [
        {"name": "dashboard", "icon": ICON_PATH["dashboard"]},
        {"name": "health", "icon": ICON_PATH["health"]},
        {"name": "challenges", "icon": ICON_PATH["challenges"]},
        # {"name": "progress", "icon": ICON_PATH["progress"]},
        # {"name": "assignments", "icon": ICON_PATH["assignments"]},
        {"name": "settings", "icon": ICON_PATH["settings"]},
    ],
    "parent": [
        {"name": "dashboard", "icon": ICON_PATH["dashboard"]},
        {"name": "health", "icon": ICON_PATH["health"]},
        {"name": "progress", "icon": ICON_PATH["progress"]},
        {"name": "settings", "icon": ICON_PATH["settings"]},
    ],
}

BMI_ICONS = {
    "underweight": ICONS_PATH + "body-underweight.svg",
    "normal": ICONS_PATH + "body-normal.svg",
    "overweight": ICONS_PATH + "body-overweight.svg",
    "obese": ICONS_PATH + "body-obese.svg",
}