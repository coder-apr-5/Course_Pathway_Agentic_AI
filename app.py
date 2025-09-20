




import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, scrolledtext
import google.generativeai as genai

# ---- Quiz Bank ----
quiz_bank = {
    "AI/ML Engineer": [
        ("What is supervised learning?", "Learning with labeled data"),
        ("What is precision?", "TP / (TP + FP)"),
        ("What is backpropagation?", "Gradient-based optimization"),
    ],
    "Full Stack Developer": [
        ("What is HTML used for?", "Structure"),
        ("Which is a JavaScript framework?", "React"),
        ("What is server-side rendering?", "Rendering on server"),
    ],
    "Data Scientist": [
        ("What is a DataFrame?", "Pandas object"),
        ("Which plot is used for distributions?", "Histogram"),
        ("What is PCA?", "Dimensionality reduction"),
    ]
}

# ---- Model Setup ----
def setup_api_popup():
    api_key = simpledialog.askstring("Google Gemini API", "Enter your Google Generative AI API Key:")
    if not api_key:
        messagebox.showerror("Key Required", "You must enter an API key to proceed.")
        exit()
    genai.configure(api_key=)
    return genai.GenerativeModel("gemini-1.5-flash")

# ---- Core Logic ----
def generate_career_pathway(model, career_goal, skills, quiz_answers=None):
    user_skills = [s.strip() for s in skills.split(',') if s.strip()]
    result = ""
    # Quiz Section
    quiz_section_content = "\n--- Quiz Results ---\n"
    qs_with_answers = quiz_bank.get(career_goal, [])
    score = 0
    if not qs_with_answers:
        quiz_section_content += "No quiz questions available for the selected career goal.\n\n"
    else:
        for i, (question, correct_answer) in enumerate(qs_with_answers):
            user_ans = quiz_answers[i].strip() if quiz_answers and i < len(quiz_answers) else ""
            quiz_section_content += f"{i+1}. {question}\n   Your answer: {user_ans}\n   Correct answer: {correct_answer}\n"
            if user_ans.lower() == correct_answer.lower():
                score += 1
        quiz_section_content += f"\nScore: {score}/{len(qs_with_answers)}\n"
    result += quiz_section_content

    # Skill Analysis
    result += "\nAnalyzing skill importance...\n"
    skill_scores = {}
    for skill in user_skills:
        prompt = f"For the career goal '{career_goal}', how important is the skill '{skill}' on a scale of 0 to 10? Just give a number."
        try:
            response = model.generate_content(prompt)
            score_text = response.text.strip()
            score_value = int(''.join(filter(str.isdigit, score_text)) or "0")
            skill_scores[skill] = min(score_value, 10)
        except Exception as e:
            skill_scores[skill] = 0
    for skill, val in skill_scores.items():
        result += f"- {skill}: {val}/10\n"

    # Roadmap
    roadmap_prompt = (
        f"As a career coach, help a student become a {career_goal}. Their known skills are: {', '.join(user_skills)}. "
        f"Based on these, suggest a learning roadmap in 5–7 stages with topic names, importance, and resources."
    )
    result += "\nGenerating roadmap...\n"
    try:
        roadmap_response = model.generate_content(roadmap_prompt)
        result += f"\n{roadmap_response.text}\n"
    except Exception as e:
        result += f"\nError: {e}\n"
    return result

# ---- Tkinter UI ----
def main_tkinter_ui(model):
    root = tk.Tk()
    root.title("Agentic AI Course Pathway")
    root.geometry("780x680")
    root.configure(bg="#F8F9FB")
    root.resizable(False, False)

    header = tk.Label(root, text="🎓 Agentic AI Course Pathway", font=("Helvetica", 18, "bold"), bg="#F8F9FB", fg="#162447")
    header.pack(pady=(18, 2))
    desc = tk.Label(root, text="Get a personalized roadmap, quiz, and skill analysis for your chosen tech career.",
                    font=("Helvetica", 11), bg="#F8F9FB", fg="#364F6B")
    desc.pack(pady=(0, 10))

    frame = tk.Frame(root, bg="#fff", bd=1, relief=tk.RIDGE)
    frame.pack(padx=30, pady=5, fill="x")

    tk.Label(frame, text="Choose Career Goal:", font=("Helvetica", 12), anchor="w", bg="#fff").grid(row=0, column=0, sticky="w", padx=14, pady=(15, 0))
    combo_goal = ttk.Combobox(frame, values=list(quiz_bank.keys()),
                              font=("Helvetica", 12), state="readonly", width=32)
    combo_goal.grid(row=1, column=0, padx=14, pady=(5, 8), sticky="ew")
    combo_goal.current(0)

    tk.Label(frame, text="Enter Your Skills (comma-separated):", font=("Helvetica", 12), anchor="w", bg="#fff").grid(row=2, column=0, sticky="w", padx=14)
    skill_entry = tk.Entry(frame, width=44, font=("Helvetica", 12))
    skill_entry.grid(row=3, column=0, padx=14, pady=(5, 10), sticky="ew")

    quiz_labels = []
    quiz_entries = []

    def render_questions():
        for lab in quiz_labels:
            lab.destroy()
        for ent in quiz_entries:
            ent.destroy()
        quiz_labels.clear()
        quiz_entries.clear()
        goal = combo_goal.get()
        qs = quiz_bank.get(goal, [])
        if qs:
            quiz_header = tk.Label(frame, text="Quiz:", font=("Helvetica", 12, "bold"), anchor="w", bg="#fff", fg="#0077B6")
            quiz_header.grid(row=4, column=0, sticky="w", padx=14, pady=(6, 3))
            quiz_labels.append(quiz_header)
            start_row = 5
            for i, (question, _) in enumerate(qs):
                lab = tk.Label(frame, text=f"{i+1}. {question}", font=("Helvetica", 11), anchor="w", bg="#fff", wraplength=510, justify="left")
                ent = tk.Entry(frame, width=48, font=("Helvetica", 11))
                lab.grid(row=start_row + i, column=0, sticky="w", padx=38, pady=(0, 2))
                ent.grid(row=start_row + i, column=0, sticky="e", padx=38, pady=(0, 2))
                quiz_labels.append(lab)
                quiz_entries.append(ent)

    combo_goal.bind("<<ComboboxSelected>>", lambda e: render_questions())

    style = ttk.Style()
    style.theme_use('default')
    style.configure(
        'Accent.TButton',
        font=('Helvetica', 12, 'bold'),
        foreground='#fff',
        background='#0077B6',
        borderwidth=1,
        focusthickness=3,
        focuscolor='none'
    )
    style.map(
        'Accent.TButton',
        background=[('active', '#005f99'), ('!active', '#0077B6')],
        foreground=[('active', '#fff'), ('!active', '#fff')]
    )

    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=14, font=("Consolas", 11), padx=10, pady=7, bg="#fff")
    output_box.pack(fill="both", expand=True, padx=30, pady=(10, 15))
    output_box.config(state="disabled")

    def on_submit():
        career_goal = combo_goal.get()
        skills = skill_entry.get()
        user_answers = [ent.get() for ent in quiz_entries]
        output_box.config(state="normal")
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "⏳ Generating your personalized results, please wait...\n")
        output_box.config(state="disabled")
        root.update()
        result = generate_career_pathway(model, career_goal, skills, user_answers)
        output_box.config(state="normal")
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, result)
        output_box.config(state="disabled")

    button_frame = tk.Frame(frame, bg="#fff")
    button_frame.grid(row=30, column=0, pady=(12, 10), padx=14, sticky="e")
    generate_btn = ttk.Button(
        button_frame,
        text="Generate Pathway",
        style="Accent.TButton",
        command=on_submit
    )
    generate_btn.pack(ipadx=18, ipady=3)

    render_questions()
    root.mainloop()

# ---- Gradio Web UI ----
import gradio as gr

gr_model = None

def gr_setup_model(api_key):
    global gr_model
    try:
        genai.configure(api_key=api_key)
        gr_model = genai.GenerativeModel("gemini-1.5-flash")
        return True, "API key configured. You may proceed."
    except Exception as e:
        gr_model = None
        return False, f"Failed to configure API: {e}"

def gr_generate_all(api_key_val, career_goal_val, skills_val, a1, a2, a3):
    ok, msg = gr_setup_model(api_key_val)
    if not ok:
        return msg
    quiz_answers = [a1, a2, a3]
    return generate_career_pathway(gr_model, career_goal_val, skills_val, quiz_answers)

def update_quiz_labels(goal):
    qs = quiz_bank.get(goal, [])
    return (
        gr.Textbox.update(label=qs[0][0] if len(qs) > 0 else ""),
        gr.Textbox.update(label=qs[1][0] if len(qs) > 1 else ""),
        gr.Textbox.update(label=qs[2][0] if len(qs) > 2 else ""),
    )

custom_css = """
body {background: #f0f6fc;}
.gradio-container {background: #f0f6fc !important;}
#main-card {background: #fff;border-radius:18px;max-width:670px;margin:20px auto;padding:32px 30px;box-shadow:0 5px 18px rgba(74,110,166,0.08);}
#quiz-sec {margin-top:24px;}
#generate-btn {background:#246ce0;color:white;font-weight:bold;font-size:18px;border-radius:12px;border:none;padding:14px 12px;}
#generate-btn:hover {background:#193f73}
.output-box {background:#f6fbff;border-radius:10px;}
.header-main {font-size:2.4em;font-weight:900;color:#24529a;margin-bottom:4px;}
.desc {color:#3f608b;font-size:1.16em;margin-bottom:28px;}
@media (max-width: 780px){
    #main-card {padding:16px 6px;}
}
"""

with gr.Blocks(css=custom_css) as demo:
    with gr.Column(elem_id="main-card"):
        gr.HTML("<div class='header-main'>🎓 Agentic AI Course Pathway</div>")
        gr.Markdown("<div class='desc'>Get a personalized roadmap, quiz, and skill analysis for your chosen tech career. <br><b>You'll need a Google Gemini API key.</b></div>")
        with gr.Row():
            api_key = gr.Textbox(label="🔑 Google Gemini API Key", type="password", elem_id="api-key-in", show_label=True, scale=1, min_width=170)
        with gr.Row():
            career_goal = gr.Dropdown(list(quiz_bank.keys()), label="🎯 Career Goal", value="AI/ML Engineer", interactive=True, scale=1)
            skills = gr.Textbox(label="💡 Your Skills (comma-separated)", placeholder="e.g. Python, SQL, Pandas", scale=2)

        with gr.Column(elem_id="quiz-sec"):
            gr.HTML("<div style='font-weight:600;color:#2451ba;font-size:1.15em;margin:10px 0 8px 3px;'>Quiz</div>")
            quiz_q1 = gr.Textbox(label=quiz_bank["AI/ML Engineer"][0][0], interactive=True)
            quiz_q2 = gr.Textbox(label=quiz_bank["AI/ML Engineer"][1][0], interactive=True)
            quiz_q3 = gr.Textbox(label=quiz_bank["AI/ML Engineer"][2][0], interactive=True)

        submit_btn = gr.Button("✨ Generate Pathway", elem_id="generate-btn")
        output = gr.Textbox(label="Personalized Pathway, Quiz & Skill Analysis", lines=18, elem_classes="output-box", interactive=False, show_copy_button=True)

    career_goal.change(
        fn=update_quiz_labels,
        inputs=career_goal,
        outputs=[quiz_q1, quiz_q2, quiz_q3]
    )

    submit_btn.click(
        gr_generate_all,
        inputs=[api_key, career_goal, skills, quiz_q1, quiz_q2, quiz_q3],
        outputs=output
    )

# ---- MAIN ----
# Uncomment ONE of the following blocks to run either Tkinter or Gradio

# --- Tkinter mode ---
# if _name_ == "_main_":
#     model = setup_api_popup()
#     main_tkinter_ui(model)

# --- Gradio mode ---
if __name__ == "_main_":
    demo.launch()
