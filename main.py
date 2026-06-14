import tkinter as tk
from tkinter import ttk
import random
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



def get_title(level):

    if level <= 2:
        return "🌱 Beginner"

    elif level <= 4:
        return "⚔️ Apprentice"

    elif level <= 6:
        return "🔥 Specialist"

    elif level <= 8:
        return "👑 Expert"

    else:
        return "💀 Legend"


def animate_xp(target):

    current = xp_bar["value"]

    if current < target:

        xp_bar["value"] = current + 5

        root.after(
            10,
            lambda: animate_xp(target)
        )

    elif current > target:

        xp_bar["value"] = current - 5

        root.after(
            10,
            lambda: animate_xp(target)
        )


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

    title_rank = get_title(level)

    completion = int(
        (progress / len(tree)) * 100
    )

    quests = [
        "Study for 30 minutes",
        "Learn one new concept",
        "Push code to GitHub",
        "Watch one ML tutorial",
        "Read documentation",
        "Build a small project",
        "Fix one annoying bug",
        "Learn one new Python trick",
        "Touch grass for 10 minutes 🌱",
        "Stop procrastinating (Impossible Mode)"
    ]

    daily_quest = random.choice(quests)

    animate_xp(min(xp, 1200))

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

    unlocked_skills = tree[:progress]
    achievement_output = ""

    if unlocked_skills:
        latest_skill = unlocked_skills[-1]
        achievement_banner.config(
            text=f"🏆 {ACHIEVEMENTS.get(latest_skill, latest_skill)}"
        )

        for skill in unlocked_skills:
            if skill in ACHIEVEMENTS:
                achievement_output += f"🏆 {ACHIEVEMENTS[skill]}\n"

    else:
        achievement_banner.config(text="🏆 No achievements unlocked")
        achievement_output = "No achievements unlocked yet.\n"

    classes = {
    "AI Engineer": "🧙 AI Mage",
    "Web Developer": "⚔️ Web Knight",
    "Data Scientist": "🧪 Data Alchemist"
}

    player_class = classes.get(
    goal,
    "🎮 Adventurer"
)
    result_text = (

        "══════════════════════\n\n"

        f"🧙 CLASS\n"
        f"{player_class}\n\n"

        f"🎮 LEVEL\n"
        f"{level}\n\n"

        f"👑 TITLE\n"
        f"{title_rank}\n\n"

        f"⭐ XP\n"
        f"{xp}\n\n"

        f"📈 TREE COMPLETION\n"
        f"{completion}%\n\n"

        f"🎯 CURRENT QUEST\n"
        f"{current_quest}\n\n"

        f"📜 DAILY QUEST\n"
        f"{daily_quest}\n\n"

        "══════════════════════\n\n"

        f"{tree_output}\n"

        "══════════════════════\n\n"

        "🏆 ACHIEVEMENTS\n\n"

        f"{achievement_output}"

        "\n══════════════════════"
    )

    result_text_widget.config(state="normal")
    result_text_widget.delete("1.0", "end")
    result_text_widget.insert("1.0", result_text)
    result_text_widget.config(state="disabled")

root = tk.Tk()

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Game.Horizontal.TProgressbar",
    thickness=25,
    troughcolor="#2A2A2A",
    background="#00FF88"
)

root.title("Life As A Skill Tree 🎮")
root.geometry("1000x1000")
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
    style="Game.Horizontal.TProgressbar",
    length=500,
    maximum=1200
)

xp_bar.pack(pady=10)

achievement_banner = tk.Label(
    root,
    text="🏆 No achievements unlocked",
    bg="#121212",
    fg="#FFD700",
    font=("Segoe UI", 11, "bold")
)

achievement_banner.pack(pady=10)

card_frame = tk.Frame(
    root,
    bg="#1E1E1E",
    highlightbackground="#BB86FC",
    highlightthickness=2
)

card_frame.pack(pady=20, padx=20, fill="both", expand=True)

result_text_widget = tk.Text(
    card_frame,
    bg="#1E1E1E",
    fg="white",
    font=("Consolas", 12),
    wrap="word",
    padx=20,
    pady=20,
    bd=0,
    highlightthickness=0,
    state="disabled"
)

result_text_widget.pack(fill="both", expand=True)

footer = tk.Label(
    root,
    text="Every legend starts at Level 1 ⚔️",
    bg="#121212",
    fg="gray",
    font=("Segoe UI", 9)
)

footer.pack(
    side="bottom",
    pady=15
)

root.mainloop()