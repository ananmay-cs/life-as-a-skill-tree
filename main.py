import tkinter as tk
from tkinter import ttk
from skill_trees import SKILL_TREES


ACHIEVEMENTS = {
    "Python": "🐍 Python Survivor",
    "Git": "🌳 Git Explorer",
    "Machine Learning": "🧠 AI Apprentice",
    "Deep Learning": "🤖 Neural Warrior",
    "Model Deployment": "🚀 Production Ready",
    "AI Engineer": "👑 AI Master",

    "HTML": "🌐 First Web Page",
    "CSS": "🎨 Style Wizard",
    "JavaScript": "⚡ Browser Tamer",
    "React": "⚛ React Rookie",
    "Backend": "🛠 Backend Builder",
    "Full Stack Developer": "🏆 Full Stack Hero",

    "Statistics": "📊 Number Cruncher",
    "Pandas": "🐼 Data Wrangler",
    "Data Visualization": "📈 Chart Master",
    "Data Scientist": "🧪 Data Scientist"
}


def generate_tree():
    goal = goal_var.get()

    user_skills = [
        skill.strip()
        for skill in skills_entry.get().split(",")
        if skill.strip()
    ]

    tree = SKILL_TREES[goal]

    progress = 0

    for skill in tree:
        if skill in user_skills:
            progress += 1
        else:
            break

    xp = progress * 200
    level = (xp // 300) + 1

    xp_bar["value"] = min(xp, 1200)

    if progress < len(tree):
        current_quest = tree[progress]
    else:
        current_quest = "🏆 Skill Tree Completed"

    tree_output = ""

    for i, skill in enumerate(tree):

        if i < progress:
            symbol = "✔"

        elif i == progress:
            symbol = "⚡"

        else:
            symbol = "🔒"

        tree_output += f"{symbol} {skill}\n"

        if i < len(tree) - 1:
            tree_output += "    │\n"
            tree_output += "    ▼\n"

    achievement_output = ""

    unlocked_skills = tree[:progress]

    if unlocked_skills:

        for skill in unlocked_skills:

            if skill in ACHIEVEMENTS:
                achievement_output += (
                    f"🏆 {ACHIEVEMENTS[skill]}\n"
                )

    else:
        achievement_output = (
            "No achievements unlocked yet.\n"
        )

    player_class = goal.replace(
        "Engineer",
        "Aspirant"
    )

    result_text = (
        "══════════════════════\n\n"

        f"🧙 CLASS\n"
        f"{player_class}\n\n"

        f"🎮 LEVEL\n"
        f"{level}\n\n"

        f"⭐ XP\n"
        f"{xp}\n\n"

        f"🎯 CURRENT QUEST\n"
        f"{current_quest}\n\n"

        "══════════════════════\n\n"

        f"{tree_output}\n"

        "══════════════════════\n\n"

        "🏆 ACHIEVEMENTS\n\n"

        f"{achievement_output}"

        "\n══════════════════════"
    )

    result_label.config(
        text=result_text
    )


root = tk.Tk()

root.title("Life As A Skill Tree 🎮")
root.geometry("800x850")
root.configure(bg="#121212")

title = tk.Label(
    root,
    text="LIFE AS A SKILL TREE 🎮",
    font=("Segoe UI", 24, "bold"),
    bg="#121212",
    fg="white"
)

title.pack(pady=20)

goal_label = tk.Label(
    root,
    text="Choose Your Goal",
    font=("Segoe UI", 12),
    bg="#121212",
    fg="white"
)

goal_label.pack()

goal_var = tk.StringVar()
goal_var.set("AI Engineer")

goal_menu = ttk.Combobox(
    root,
    textvariable=goal_var,
    values=list(SKILL_TREES.keys()),
    state="readonly",
    width=30
)

goal_menu.pack(pady=10)

skills_label = tk.Label(
    root,
    text="Your Current Skills (comma separated)",
    font=("Segoe UI", 12),
    bg="#121212",
    fg="white"
)

skills_label.pack()

skills_entry = tk.Entry(
    root,
    width=45,
    font=("Segoe UI", 11)
)

skills_entry.pack(pady=10)

generate_button = tk.Button(
    root,
    text="Generate Skill Tree ⚔️",
    command=generate_tree,
    bg="#1E88E5",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    padx=20,
    pady=10,
    borderwidth=0
)

generate_button.pack(pady=20)

xp_title = tk.Label(
    root,
    text="XP Progress ⭐",
    bg="#121212",
    fg="white",
    font=("Segoe UI", 12, "bold")
)

xp_title.pack()

xp_bar = ttk.Progressbar(
    root,
    length=500,
    maximum=1200
)

xp_bar.pack(pady=10)

result_label = tk.Label(
    root,
    text="Choose a goal and begin your journey.",
    bg="#121212",
    fg="white",
    font=("Consolas", 12),
    justify="left"
)

result_label.pack(pady=20)

footer = tk.Label(
    root,
    text="Every legend starts at Level 1 ⚔️",
    bg="#121212",
    fg="gray",
    font=("Segoe UI", 9)
)

footer.pack(side="bottom", pady=15)

root.mainloop()