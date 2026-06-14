import json
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk
from skill_trees import SKILL_TREES

SAVE_FILE = os.path.join(os.path.dirname(__file__), "character_save.json")

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

CLASS_NAMES = {
    "AI Engineer": "🧙 AI Mage",
    "Web Developer": "⚔️ Web Knight",
    "Data Scientist": "🧪 Data Alchemist"
}

INVENTORY_ITEMS = [
    (1, "📖 Beginner's Handbook"),
    (2, "⚔️ Coding Sword"),
    (3, "🛡️ Debug Shield"),
    (4, "🔥 ML Spellbook"),
    (5, "👑 Crown of Consistency")
]

DAILY_QUESTS = [
    "Study for 30 minutes",
    "Learn one new concept",
    "Push code to GitHub",
    "Watch one ML tutorial",
    "Read documentation",
    "Build a small project",
    "Fix one annoying bug",
    "Learn one new Python trick",
    "Touch grass for 10 minutes 🌱",
    "Practice a new algorithm"
]

BUTTON_BG = "#1E88E5"
BUTTON_HOVER = "#3EA0FF"
BUTTON_ACTIVE = "#579CFF"

loaded_state = {}
skill_map_window = None
current_state = {}


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


def get_stats(progress, completion):
    strength = min(15, 4 + progress * 2)
    intelligence = min(15, 3 + progress * 2)
    focus = min(15, 2 + completion // 10)
    creativity = min(15, 2 + (progress + completion // 20))
    return {
        "strength": strength,
        "intelligence": intelligence,
        "focus": focus,
        "creativity": creativity
    }


def get_inventory(level):
    return [item for threshold, item in INVENTORY_ITEMS if level >= threshold]


def animate_xp(target):
    current = xp_bar["value"]
    if current < target:
        xp_bar["value"] = min(target, current + 10)
        root.after(10, lambda: animate_xp(target))
    elif current > target:
        xp_bar["value"] = max(target, current - 10)
        root.after(10, lambda: animate_xp(target))


def apply_button_hover(button):
    button.bind("<Enter>", lambda e: button.config(bg=BUTTON_HOVER))
    button.bind("<Leave>", lambda e: button.config(bg=BUTTON_BG))
    button.bind("<ButtonPress>", lambda e: button.config(bg=BUTTON_ACTIVE))
    button.bind("<ButtonRelease>", lambda e: button.config(bg=BUTTON_HOVER))


def build_tree_output(tree, progress):
    output = ""
    for i, skill in enumerate(tree):
        if i < progress:
            symbol = "✔"
        elif i == progress:
            symbol = "⚡"
        else:
            symbol = "🔒"
        output += f"{symbol} {skill}\n"
        if i < len(tree) - 1:
            output += "    │\n"
            output += "    ▼\n"
    return output


def update_profile(player_class, level, xp, title_rank, completion, stats):
    profile_class_value.config(text=player_class)
    profile_level_value.config(text=str(level))
    profile_xp_value.config(text=f"{xp} XP")
    profile_title_value.config(text=title_rank)
    profile_completion_value.config(text=f"{completion}%")
    profile_strength_value.config(text=str(stats["strength"]))
    profile_intelligence_value.config(text=str(stats["intelligence"]))
    profile_focus_value.config(text=str(stats["focus"]))
    profile_creativity_value.config(text=str(stats["creativity"]))


def update_inventory(level):
    items = get_inventory(level)
    inventory_text = "\n".join(items) if items else "No items unlocked yet."
    inventory_value.config(text=inventory_text)


def update_quest_log(main_quest, daily_quest, main_reward, daily_reward):
    main_quest_label.config(text=f"Main Quest: {main_quest}")
    main_quest_reward.config(text=f"Reward: {main_reward} XP")
    daily_quest_label.config(text=f"Daily Quest: {daily_quest}")
    daily_quest_reward.config(text=f"Reward: {daily_reward} XP")


def save_character():
    goal = goal_var.get()
    skills = skills_entry.get().strip()
    if not goal:
        messagebox.showwarning("Save Failed", "Choose a goal before saving.")
        return
    state = {
        "goal": goal,
        "skills": skills,
        "xp": current_state.get("xp", 0),
        "level": current_state.get("level", 1),
        "completion": current_state.get("completion", 0),
        "achievements": current_state.get("achievements", []),
        "daily_quest": current_state.get("daily_quest", ""),
        "main_quest": current_state.get("main_quest", "")
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as save_file:
            json.dump(state, save_file, indent=2, ensure_ascii=False)
        messagebox.showinfo("Saved", "Character saved successfully.")
    except Exception as exc:
        messagebox.showerror("Save Error", f"Unable to save character:\n{exc}")


def load_character():
    global loaded_state
    if not os.path.exists(SAVE_FILE):
        messagebox.showwarning("Load Failed", "No saved character found.")
        return
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as save_file:
            loaded_state = json.load(save_file)
        goal_var.set(loaded_state.get("goal", "AI Engineer"))
        skills_entry.delete(0, tk.END)
        skills_entry.insert(0, loaded_state.get("skills", ""))
        generate_tree(from_save=True)
        messagebox.showinfo("Loaded", "Character loaded successfully.")
    except Exception as exc:
        messagebox.showerror("Load Error", f"Unable to load character:\n{exc}")


def open_skill_map():
    global skill_map_window
    if skill_map_window and skill_map_window.winfo_exists():
        skill_map_window.lift()
        return
    skill_map_window = tk.Toplevel(root)
    skill_map_window.configure(bg="#121212")
    skill_map_window.title("Skill Map")
    skill_map_window.geometry("760x420")
    skill_map_window.resizable(True, True)
    canvas = tk.Canvas(skill_map_window, bg="#121212", highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=20, pady=20)
    goal = goal_var.get()
    tree = SKILL_TREES.get(goal, [])
    progress = current_state.get("progress", 0)
    draw_skill_map(canvas, tree, progress)
    canvas.bind("<Configure>", lambda event: draw_skill_map(canvas, tree, progress))


def draw_skill_map(canvas, tree, progress):
    canvas.delete("all")
    width = int(canvas.winfo_width() or 700)
    height = int(canvas.winfo_height() or 400)
    radius = 28
    spacing = max(120, (width - 160) // max(1, len(tree) - 1))
    start_x = 80
    y = height // 2
    node_positions = []
    for i, skill in enumerate(tree):
        x = start_x + i * spacing
        node_positions.append((x, y))
        if i < progress:
            fill = "#00FF88"
        elif i == progress:
            fill = "#FFD700"
        else:
            fill = "#FF4D4D"
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill, outline="#BBBBBB", width=2)
        canvas.create_text(x, y, text=str(i + 1), fill="#121212", font=("Segoe UI", 10, "bold"))
        canvas.create_text(x, y + radius + 18, text=skill, fill="white", font=("Segoe UI", 9), anchor="n")
    for i in range(len(node_positions) - 1):
        x1, y1 = node_positions[i]
        x2, y2 = node_positions[i + 1]
        canvas.create_line(x1 + radius, y1, x2 - radius, y2, fill="#BB86FC", width=3, dash=(4, 2))


def generate_tree(from_save=False):
    goal = goal_var.get()
    user_skills = [
        skill.strip()
        for skill in skills_entry.get().split(",")
        if skill.strip()
    ]
    tree = SKILL_TREES.get(goal, [])
    progress = 0
    for skill in tree:
        if skill in user_skills:
            progress += 1
        else:
            break
    xp = progress * 200
    level = (xp // 300) + 1
    title_rank = get_title(level)
    completion = int((progress / len(tree)) * 100) if tree else 0
    if from_save and loaded_state.get("daily_quest"):
        daily_quest = loaded_state["daily_quest"]
    else:
        daily_quest = random.choice(DAILY_QUESTS)
    if from_save and loaded_state.get("main_quest"):
        main_quest = loaded_state["main_quest"]
    else:
        main_quest = f"Unlock {tree[-1]}" if progress < len(tree) else "Master your path"
    current_quest = tree[progress] if progress < len(tree) else "🏆 Skill Tree Completed"
    tree_output = build_tree_output(tree, progress)
    unlocked_skills = tree[:progress]
    achievement_output = ""
    achievements = []
    if unlocked_skills:
        latest_skill = unlocked_skills[-1]
        achievement_banner.config(text=f"🏆 {ACHIEVEMENTS.get(latest_skill, latest_skill)}")
        for skill in unlocked_skills:
            if skill in ACHIEVEMENTS:
                achievement_output += f"🏆 {ACHIEVEMENTS[skill]}\n"
                achievements.append(ACHIEVEMENTS[skill])
    else:
        achievement_banner.config(text="🏆 No achievements unlocked")
        achievement_output = "No achievements unlocked yet.\n"
    player_class = CLASS_NAMES.get(goal, "🎮 Adventurer")
    stats = get_stats(progress, completion)
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
    update_profile(player_class, level, xp, title_rank, completion, stats)
    update_inventory(level)
    update_quest_log(main_quest, daily_quest, 300, 150)
    xp_bar.config(maximum=max(1200, xp, 1200))
    animate_xp(min(xp, 1200))
    current_state.update({
        "goal": goal,
        "skills": ", ".join(user_skills),
        "progress": progress,
        "xp": xp,
        "level": level,
        "completion": completion,
        "achievements": achievements,
        "daily_quest": daily_quest,
        "main_quest": main_quest,
        "current_quest": current_quest
    })
    if skill_map_window and skill_map_window.winfo_exists():
        skill_map_window.destroy()
        open_skill_map()

root = tk.Tk()
root.title("Life As A Skill Tree 🎮")
root.geometry("1040x980")
root.configure(bg="#121212")
root.resizable(False, False)

header = tk.Label(
    root,
    text="LIFE AS A SKILL TREE 🎮",
    font=("Segoe UI", 28, "bold"),
    bg="#121212",
    fg="white"
)
header.pack(pady=(20, 10))

input_panel = tk.Frame(root, bg="#121212")
input_panel.pack(pady=(0, 15), fill="x")

goal_frame = tk.Frame(input_panel, bg="#121212")
goal_frame.pack(side="left", padx=20, fill="y")

goal_label = tk.Label(
    goal_frame,
    text="Choose Your Goal",
    font=("Segoe UI", 12),
    bg="#121212",
    fg="white"
)

goal_label.pack(anchor="w")

goal_var = tk.StringVar(value="AI Engineer")

goal_menu = ttk.Combobox(
    goal_frame,
    textvariable=goal_var,
    values=list(SKILL_TREES.keys()),
    state="readonly",
    width=30
)

goal_menu.pack(pady=6)

skills_frame = tk.Frame(input_panel, bg="#121212")
skills_frame.pack(side="left", padx=20, fill="y")

skills_label = tk.Label(
    skills_frame,
    text="Your Current Skills (comma separated)",
    font=("Segoe UI", 12),
    bg="#121212",
    fg="white"
)

skills_label.pack(anchor="w")

skills_entry = tk.Entry(
    skills_frame,
    width=44,
    font=("Segoe UI", 11)
)

skills_entry.pack(pady=6)

button_frame = tk.Frame(input_panel, bg="#121212")
button_frame.pack(side="left", padx=20, fill="y")

generate_button = tk.Button(
    button_frame,
    text="Generate Skill Tree ⚔️",
    command=generate_tree,
    bg=BUTTON_BG,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    padx=18,
    pady=10,
    borderwidth=0
)

save_button = tk.Button(
    button_frame,
    text="Save Character 💾",
    command=save_character,
    bg=BUTTON_BG,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    padx=18,
    pady=10,
    borderwidth=0
)

load_button = tk.Button(
    button_frame,
    text="Load Character 📂",
    command=load_character,
    bg=BUTTON_BG,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    padx=18,
    pady=10,
    borderwidth=0
)

map_button = tk.Button(
    button_frame,
    text="Open Skill Map 🗺️",
    command=open_skill_map,
    bg=BUTTON_BG,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    padx=18,
    pady=10,
    borderwidth=0
)

for btn in (generate_button, save_button, load_button, map_button):
    btn.pack(pady=5, fill="x")
    apply_button_hover(btn)

progress_frame = tk.Frame(root, bg="#121212")
progress_frame.pack(pady=(0, 20), fill="x")

xp_title = tk.Label(
    progress_frame,
    text="XP Progress ⭐",
    bg="#121212",
    fg="white",
    font=("Segoe UI", 12, "bold")
)

xp_title.pack()

xp_bar = ttk.Progressbar(
    progress_frame,
    style="Game.Horizontal.TProgressbar",
    length=660,
    maximum=1200
)

xp_bar.pack(pady=10)

achievement_banner = tk.Label(
    progress_frame,
    text="🏆 No achievements unlocked",
    bg="#121212",
    fg="#FFD700",
    font=("Segoe UI", 11, "bold")
)

achievement_banner.pack()

content_frame = tk.Frame(root, bg="#121212")
content_frame.pack(fill="both", expand=True)

result_card = tk.Frame(
    content_frame,
    bg="#1E1E1E",
    bd=0,
    highlightbackground="#BB86FC",
    highlightthickness=2
)

result_card.pack(side="left", padx=(20, 10), pady=10, fill="both", expand=True)

result_header = tk.Label(
    result_card,
    text="Skill Journey Overview",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 14, "bold")
)

result_header.pack(pady=(20, 6))

result_text_widget = tk.Text(
    result_card,
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

result_text_widget.pack(fill="both", expand=True, padx=10, pady=(0, 20))

side_panel = tk.Frame(content_frame, bg="#121212")
side_panel.pack(side="right", padx=(10, 20), pady=10, fill="y")

profile_card = tk.Frame(
    side_panel,
    bg="#1E1E1E",
    bd=0,
    highlightbackground="#BB86FC",
    highlightthickness=2
)

profile_card.pack(fill="x", pady=(0, 10))

profile_header = tk.Label(
    profile_card,
    text="RPG Profile",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 14, "bold")
)

profile_header.pack(pady=(16, 6))

profile_class_label = tk.Label(
    profile_card,
    text="Class:",
    bg="#1E1E1E",
    fg="#BBBBBB",
    font=("Segoe UI", 11)
)

profile_class_label.pack(anchor="w", padx=16)

profile_class_value = tk.Label(
    profile_card,
    text="🎮 Adventurer",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 12, "bold")
)

profile_class_value.pack(anchor="w", padx=16, pady=(0, 10))

profile_level_label = tk.Label(
    profile_card,
    text="Level:",
    bg="#1E1E1E",
    fg="#BBBBBB",
    font=("Segoe UI", 11)
)

profile_level_label.pack(anchor="w", padx=16)

profile_level_value = tk.Label(
    profile_card,
    text="1",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 12, "bold")
)

profile_level_value.pack(anchor="w", padx=16, pady=(0, 10))

profile_xp_label = tk.Label(
    profile_card,
    text="XP:",
    bg="#1E1E1E",
    fg="#BBBBBB",
    font=("Segoe UI", 11)
)

profile_xp_label.pack(anchor="w", padx=16)

profile_xp_value = tk.Label(
    profile_card,
    text="0 XP",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 12, "bold")
)

profile_xp_value.pack(anchor="w", padx=16, pady=(0, 10))

profile_title_label = tk.Label(
    profile_card,
    text="Title:",
    bg="#1E1E1E",
    fg="#BBBBBB",
    font=("Segoe UI", 11)
)

profile_title_label.pack(anchor="w", padx=16)

profile_title_value = tk.Label(
    profile_card,
    text="🌱 Beginner",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 12, "bold")
)

profile_title_value.pack(anchor="w", padx=16, pady=(0, 10))

profile_completion_label = tk.Label(
    profile_card,
    text="Completion:",
    bg="#1E1E1E",
    fg="#BBBBBB",
    font=("Segoe UI", 11)
)

profile_completion_label.pack(anchor="w", padx=16)

profile_completion_value = tk.Label(
    profile_card,
    text="0%",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 12, "bold")
)

profile_completion_value.pack(anchor="w", padx=16, pady=(0, 16))

stats_frame = tk.Frame(profile_card, bg="#1E1E1E")
stats_frame.pack(fill="x", padx=16, pady=(0, 16))

profile_strength_value = tk.Label(stats_frame, text="0", bg="#1E1E1E", fg="white", font=("Segoe UI", 11, "bold"))
profile_intelligence_value = tk.Label(stats_frame, text="0", bg="#1E1E1E", fg="white", font=("Segoe UI", 11, "bold"))
profile_focus_value = tk.Label(stats_frame, text="0", bg="#1E1E1E", fg="white", font=("Segoe UI", 11, "bold"))
profile_creativity_value = tk.Label(stats_frame, text="0", bg="#1E1E1E", fg="white", font=("Segoe UI", 11, "bold"))

for text, value_widget in [
    ("💪 Strength", profile_strength_value),
    ("🧠 Intelligence", profile_intelligence_value),
    ("⚡ Focus", profile_focus_value),
    ("🎨 Creativity", profile_creativity_value)
]:
    row_frame = tk.Frame(stats_frame, bg="#1E1E1E")
    row_frame.pack(fill="x", pady=2)
    label = tk.Label(row_frame, text=text, bg="#1E1E1E", fg="#BBBBBB", font=("Segoe UI", 10))
    label.pack(side="left")
    value_widget.pack(side="right")

inventory_card = tk.Frame(
    side_panel,
    bg="#1E1E1E",
    bd=0,
    highlightbackground="#BB86FC",
    highlightthickness=2
)

inventory_card.pack(fill="x", pady=(0, 10))

inventory_header = tk.Label(
    inventory_card,
    text="Inventory",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 14, "bold")
)

inventory_header.pack(pady=(16, 10))

inventory_value = tk.Label(
    inventory_card,
    text="No items unlocked yet.",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 11),
    justify="left",
    wraplength=280
)

inventory_value.pack(anchor="w", padx=16, pady=(0, 16))

quest_card = tk.Frame(
    side_panel,
    bg="#1E1E1E",
    bd=0,
    highlightbackground="#BB86FC",
    highlightthickness=2
)

quest_card.pack(fill="x")

quest_header = tk.Label(
    quest_card,
    text="Quest Log",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 14, "bold")
)

quest_header.pack(pady=(16, 10))

main_quest_label = tk.Label(
    quest_card,
    text="Main Quest: Unlock your path",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 11),
    justify="left",
    wraplength=280
)

main_quest_label.pack(anchor="w", padx=16)

main_quest_reward = tk.Label(
    quest_card,
    text="Reward: 300 XP",
    bg="#1E1E1E",
    fg="#BBBBBB",
    font=("Segoe UI", 10)
)

main_quest_reward.pack(anchor="w", padx=16, pady=(4, 10))

daily_quest_label = tk.Label(
    quest_card,
    text="Daily Quest: Stay disciplined",
    bg="#1E1E1E",
    fg="white",
    font=("Segoe UI", 11),
    justify="left",
    wraplength=280
)

daily_quest_label.pack(anchor="w", padx=16)

daily_quest_reward = tk.Label(
    quest_card,
    text="Reward: 150 XP",
    bg="#1E1E1E",
    fg="#BBBBBB",
    font=("Segoe UI", 10)
)

daily_quest_reward.pack(anchor="w", padx=16, pady=(4, 16))

style = ttk.Style()
style.theme_use("default")
style.configure(
    "Game.Horizontal.TProgressbar",
    thickness=25,
    troughcolor="#2A2A2A",
    background="#00FF88"
)

if __name__ == "__main__":
    generate_tree()
    root.mainloop()
