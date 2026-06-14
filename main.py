import tkinter as tk
from tkinter import ttk
from skill_trees import SKILL_TREES


def generate_tree():
    goal = goal_var.get()

    user_skills = [
        skill.strip()
        for skill in skills_entry.get().split(",")
        if skill.strip()
    ]

    tree = SKILL_TREES[goal]

    output = ""

    unlocked = 0

    for skill in tree:
        if skill in user_skills:
            output += f"✔ {skill}\n"
            unlocked += 1

        elif unlocked == len([
            s for s in tree
            if s in user_skills
        ]):
            output += f"⚡ {skill}\n"

            unlocked += 999999

        else:
            output += f"🔒 {skill}\n"

    xp = len(user_skills) * 200
    level = (xp // 300) + 1

    result_label.config(
        text=(
            f"🎮 LEVEL {level}\n"
            f"⭐ XP: {xp}\n\n"
            f"{output}"
        )
    )

    xp_bar["value"] = min(xp, 1000)


root = tk.Tk()

root.title("Life As A Skill Tree 🎮")
root.geometry("700x650")
root.configure(bg="#121212")

title = tk.Label(
    root,
    text="LIFE AS A SKILL TREE 🎮",
    font=("Segoe UI", 22, "bold"),
    bg="#121212",
    fg="white"
)

title.pack(pady=20)

goal_label = tk.Label(
    root,
    text="Choose Your Goal",
    font=("Segoe UI", 11),
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
    width=25
)

goal_menu.pack(pady=10)

skills_label = tk.Label(
    root,
    text="Your Current Skills (comma separated)",
    font=("Segoe UI", 11),
    bg="#121212",
    fg="white"
)

skills_label.pack()

skills_entry = tk.Entry(
    root,
    width=40,
    font=("Segoe UI", 11)
)

skills_entry.pack(pady=10)

generate_button = tk.Button(
    root,
    text="Generate Skill Tree ⚔️",
    command=generate_tree,
    bg="#1E88E5",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    padx=20,
    pady=10
)

generate_button.pack(pady=15)

xp_title = tk.Label(
    root,
    text="XP Progress ⭐",
    bg="#121212",
    fg="white",
    font=("Segoe UI", 11, "bold")
)

xp_title.pack()

xp_bar = ttk.Progressbar(
    root,
    length=450,
    maximum=1000
)

xp_bar.pack(pady=10)

result_label = tk.Label(
    root,
    text="Choose a goal and generate your journey.",
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
    fg="gray"
)

footer.pack(side="bottom", pady=15)

root.mainloop()