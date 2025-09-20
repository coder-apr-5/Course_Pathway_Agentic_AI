# Agentic AI Course Pathway — Project Documentation (v1.0)

> **Project**: Agentic AI Course Pathway
> **Author**: Hamza Uzzaman Pritihsha Hazra Apurba Roy
> **Runtime**: Python 3.10+
> **UI**: Tkinter (desktop) + Gradio (web)
> **LLM**: Google Generative AI (Gemini 1.5)

---

# Table of Contents:

## 1) Executive Summary

**Agentic AI Course Pathway** is a lightweight guidance tool that produces a personalized learning roadmap for tech career tracks (e.g., AI/ML Engineer, Full Stack Developer, Data Scientist). It combines:

* a **quiz** to assess basic knowledge,
* a **skill-importance analyzer** powered by an LLM, and
* a generated **multi‑stage learning plan** with topics and resources.

Two user interfaces are offered:

* **Desktop (Tkinter)**: a minimal, local app with a classic GUI.
* **Web (Gradio)**: a shareable web demo for quick access in the browser.

The application integrates with **Google Generative AI (Gemini)** via API to rate user‑provided skills and to synthesize the final roadmap.

---

## 2) Goals & Non‑Goals

### 2.1 Goals

* Provide a **clear, structured roadmap** for a target career path.
* Offer a **short diagnostic quiz** and a **skill importance** breakdown.
* Keep the **code approachable**, with minimal dependencies and simple UI.
* Make it easy to **add new careers** and **extend the quiz bank**.

### 2.2 Non‑Goals

* Full student analytics, persistence, or progress tracking.
* Adaptive testing or long‑form assessments.
* Multi‑tenant deployment or complex user management.

---

## 3) High‑Level Architecture

```
+------------------+        +-------------------+        +-------------------------+
|  User Interfaces | -----> |  Core Logic       | -----> |  LLM (Gemini via API)   |
|  - Tkinter (GUI) |        |  - Quiz Scoring   |        |  - Skill rating prompt  |
|  - Gradio (Web)  |        |  - Skill Analysis |        |  - Roadmap generation   |
+------------------+        |  - Roadmap Synth  |        +-------------------------+
        |                   +-------------------+                 ^
        |                         |                                |
        v                         v                                |
   Quiz Bank (dict)    Configuration & Secrets (API key) ----------+ 
```

* **UI layer** collects inputs and displays results.
* **Core logic** orchestrates quiz scoring, skill analysis, and roadmap generation.
* **LLM service** provides numeric skill ratings and full roadmap text.
* **Quiz bank** is a simple Python dictionary; easily extended.

---

## 4) Repository & Code Layout

The current repository centers around a single Python module that contains:

* **Quiz bank** for supported careers.
* **LLM setup** for Google Generative AI (Gemini 1.5).
* **Core logic** (`generate_career_pathway`).
* **Tkinter UI** for desktop usage.
* **Gradio UI** for web usage.

> **Suggestion**: Consider the following structure as the project grows:

```
agentic_pathway/
├─ app.py                 # CLI entry or launcher (select Tkinter/Gradio)
├─ core/
│  ├─ logic.py            # generate_career_pathway, parsing helpers
│  ├─ prompts.py          # prompt templates
│  ├─ quiz_bank.py        # quiz question/answer bank
│  └─ llm.py              # model setup & wrappers
├─ ui/
│  ├─ tkinter_app.py      # Tkinter interface
│  └─ gradio_app.py       # Gradio interface
├─ tests/
│  └─ test_logic.py       # unit tests for core logic
├─ requirements.txt
├─ .env.example           # placeholder for API keys
└─ README.md
```

---

## 5) Installation & Setup

### 5.1 Requirements

* **Python** 3.10 or newer.
* Packages:

  * `google-generativeai`
  * `gradio`
  * `tkinter` (bundled with many Python builds on Windows/macOS; on Linux, install via package manager)

### 5.2 Create a Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 5.3 Install Dependencies

```bash
pip install google-generativeai gradio
```

### 5.4 Configure the API Key

* Obtain a **Google Generative AI (Gemini)** API key from your Google AI Studio account.
* Option A (GUI prompt): The Tkinter app prompts you to paste the key.
* Option B (env): Set it as an environment variable for Gradio or scripts:

```bash
# macOS/Linux
export GOOGLE_API_KEY="YOUR_KEY"
# Windows (PowerShell)
$env:GOOGLE_API_KEY="YOUR_KEY"
```

---

## 6) Running the Application

### 6.1 Desktop (Tkinter)

1. Ensure your environment is activated and dependencies installed.
2. Run the Tkinter entry point. Example:

```bash
python app.py --ui tkinter
```

* On startup, you’ll be prompted for the Google API key (if not set in env).
* Fill in **career goal**, **skills**, and **quiz answers**, then click **Generate Pathway**.

### 6.2 Web (Gradio)

1. Ensure the API key is available (textbox or environment variable).
2. Run the Gradio demo:

```bash
python app.py --ui gradio
```

* A local URL will be printed. Open it in your browser to use the web UI.

---

## 7) Core Logic Walkthrough

### 7.1 `generate_career_pathway(model, career_goal, skills, quiz_answers=None)`

**Inputs**

* `model`: an initialized `genai.GenerativeModel` (e.g., `"gemini-1.5-flash"`).
* `career_goal`: one of the supported careers (maps to quiz bank keys).
* `skills`: comma‑separated list of user skills (e.g., "Python, SQL, Pandas").
* `quiz_answers`: optional list of answers aligned to the selected quiz.

**Outputs**

* A **single formatted string** that includes:

  1. **Quiz results** and score.
  2. **Skill importance** ratings (0–10) per listed skill.
  3. A **multi‑stage roadmap** (5–7 stages) with topics, importance, and resources.

**Processing Steps**

1. **Quiz**: Looks up questions for `career_goal`, compares `quiz_answers` to correct answers, and composes a score.
2. **Skill Analysis**: For each provided skill, calls the LLM with a prompt to return a number between 0 and 10.
3. **Roadmap Generation**: Sends a larger coaching prompt to the LLM to produce the staged learning plan.

---

## 8) Prompt Design

### 8.1 Skill Importance Prompt

> *"For the career goal '{career\_goal}', how important is the skill '{skill}' on a scale of 0 to 10? Just give a number."*

**Notes**

* Keep it terse to encourage numeric‑only responses.
* Parse robustly (extract the first integer 0–10). If the model returns prose, filter digits defensively.

### 8.2 Roadmap Prompt

> *"As a career coach, help a student become a {career\_goal}. Their known skills are: {skills}. Based on these, suggest a learning roadmap in 5–7 stages with topic names, importance, and resources."*

**Enhancements** (optional):

* Ask for **time estimates** per stage.
* Request **beginner → advanced** ordering with **prerequisites**.
* Enforce **bullet format** or **JSON** for easier downstream parsing.

---

## 9) UI/UX Details

### 9.1 Tkinter

* Clean header, description, and a framed form for inputs.
* `ttk.Combobox` for **Career Goal** (read‑only list from `quiz_bank`).
* Dynamic **Quiz** rendering: labels and entries created based on selected career track.
* Styled **Generate Pathway** button with a custom `Accent.TButton` style.
* **ScrolledText** output box for results.

### 9.2 Gradio

* Single‑page layout with custom CSS.
* Inputs: API key, career goal, skills, and 3 quiz answer boxes whose labels update with the chosen career.
* Output: read‑only multiline textbox with copy support.

---

## 10) Data Model: Quiz Bank

A simple dictionary maps **career → list of (question, correct\_answer)** tuples. Example:

```python
quiz_bank = {
    "AI/ML Engineer": [
        ("What is supervised learning?", "Learning with labeled data"),
        ("What is precision?", "TP / (TP + FP)"),
        ("What is backpropagation?", "Gradient-based optimization"),
    ],
    ...
}
```

> **Tip**: Keep answers concise but unique enough to avoid accidental false mismatches during exact string comparison.

---

## 11) Error Handling & Resilience

* **API Key missing**: show a blocking dialog (Tkinter) or a visible message (Gradio) and abort.
* **Network/LLM errors**: catch exceptions and embed the error into the output instead of crashing.
* **Parsing numeric scores**: if the LLM returns text, extract the first integer; clamp to `[0, 10]`.
* **Empty inputs**: allow empty quiz answers but score them as incorrect; allow empty skills list and return a note.

---

## 12) Security & Privacy Considerations

* **Do not log API keys** or echo them to the UI.
* Prefer environment variable configuration for keys in shared environments.
* Avoid sending personally identifiable information in prompts.
* Consider **rate limiting** or back‑off on repeated API calls.

---

## 13) Performance Considerations

* Current design makes **one LLM call per skill** plus **one** for the roadmap.

  * If users enter many skills, total latency grows linearly.
  * Optimization: request a **batched rating** for all skills in one prompt and then parse a JSON list.
* UI is **synchronous**; consider threads or async tasks for better responsiveness in Tkinter.

---

## 14) Extensibility

### 14.1 Add a New Career Track

1. Add questions to `quiz_bank["New Career"] = [...]`.
2. Update any UI lists (Tkinter `Combobox`, Gradio `Dropdown`).
3. (Optional) Add tailored prompt prefixes per career.

### 14.2 Adjust Scoring Rules

* Replace exact string match with **case‑insensitive** or **keyword‑based** matching.
* Introduce **partial credit** using simple heuristics (e.g., `any(keyword in answer for keyword in ["precision", "TP", "FP"])`).

### 14.3 Output Formats

* Offer **Markdown** or **HTML** versions of the roadmap for export.
* Provide a **JSON** API for integrations.

---

## 15) Known Issues & Quick Fixes (Code Review)

Below are precise improvements for the provided code.

### 15.1 API Configuration Bug

**Problem**: `genai.configure(api_key=)` has an empty argument.  
**Fix**:

```python
genai.configure(api_key=api_key)
```

### 15.2 `__main__` Guard Typos

**Problem**: The code uses `_name_` and `_main_`.  
**Fix**:

```python
if __name__ == "__main__":
    # choose one mode; e.g., Gradio
    demo.launch()
```

For Tkinter mode:

```python
if __name__ == "__main__":
    model = setup_api_popup()
    main_tkinter_ui(model)
```

> **Only one** of these blocks should be active at a time.

### 15.3 Safer Integer Parsing for Skill Scores

**Problem**: `int(''.join(filter(str.isdigit, score_text)) or "0")` can extract multi-digit numbers or none.

**Fix** (first integer 0–10 with clamping):

```python
import re
match = re.search(r"\b(10|[0-9])\b", score_text)
score_value = int(match.group(0)) if match else 0
score_value = max(0, min(score_value, 10))
```

### 15.4 Consolidate Skill Rating Calls (Optional Optimization)

**Idea**: Rate all skills in **one** LLM request for lower latency.

```python
skills_list = [s.strip() for s in skills.split(',') if s.strip()]
prompt = (
    f"For the career goal '{career_goal}', rate these skills 0–10 and return JSON with 'skill' and 'score':\n"
    + "\n".join(f"- {s}" for s in skills_list)
)
response = model.generate_content(prompt)
# Parse JSON robustly (fallback to per-skill if parsing fails)
```

### 15.5 Threaded Generation in Tkinter (Responsiveness)

**Problem**: Long LLM calls block the UI.  
**Fix**: Run `generate_career_pathway` in a `threading.Thread` and update the text box on completion.

### 15.6 Gradio `update_quiz_labels` Safety

**Problem**: Access by index without length checks can break if you add shorter quizzes.  
**Fix**: You already guard length; also set defaults to empty strings when `qs` is empty.

### 15.7 Model Name as a Constant

Define once to avoid typos and future upgrades:

```python
MODEL_NAME = "gemini-1.5-flash"
# or consider "gemini-1.5-pro" for higher quality, if available
```

### 15.8 User Feedback & Errors

* When an exception happens during roadmap generation, surface a friendly message and suggest retry.
* In Gradio, return the **partial result** gathered so far (quiz + any rated skills) even if roadmap fails.

---

## 16) Sample User Flow

1. **Select career**: "AI/ML Engineer".
2. **Enter skills**: "Python, Linear Algebra, SQL, PyTorch".
3. **Answer quiz** (3 short questions).
4. Click **Generate Pathway**.
5. App shows:

   * Quiz responses vs correct answers and a score.
   * Skill ratings, e.g., Python 9/10, Linear Algebra 8/10…
   * A 5–7 stage roadmap (Foundations → Modeling → MLOps → Projects → Interview prep), including resources.

---

## 17) Testing Strategy

* **Unit tests** for parsing logic (quiz scoring, numeric extraction, JSON parsing fallback).
* **Mock LLM** interfaces to avoid network calls in tests.
* **UI smoke tests**: ensure Tkinter components render and Gradio callbacks run.

---

## 18) Deployment Notes

* **Local use**: Ideal for learners; distribute via `pipx` or a zipped app.
* **Web demo**: Host Gradio on Spaces/Render/Fly; store the API key as a secret.
* **Containerization** (optional):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV PORT=7860
CMD ["python", "app.py", "--ui", "gradio"]
```

Expose the port in your platform settings. Do **not** bake secrets into the image.

---

## 19) Troubleshooting

* **ImportError: google.generativeai** → `pip install google-generativeai` in the active venv.
* **KeyError (quiz labels)** → ensure each career has the expected number of questions or guard indexes.
* **NetworkError / 429** → back off and retry; reduce number of skills or batch rating.
* **No output** → check `__name__ == "__main__"` block and confirm that only one UI path is active.

---

## 20) Roadmap (Future Work)

* **Progress persistence**: save user sessions and results.  
* **Richer assessments**: multiple-choice and short answer grading with semantic matching.  
* **Export**: one-click export to **PDF/Markdown** of the roadmap and analysis.  
* **Analytics**: anonymized usage metrics to improve question design and skill importance mapping.  
* **Collaboration features**: ability for mentors or peers to suggest edits to the generated roadmap.  
* **Mobile-friendly UI**: lightweight mobile version using a responsive web app.  
* **Offline mode**: limited roadmap generation using predefined templates when no API access is available.  
* **Plugin architecture**: support for external quiz/question banks and roadmap templates.  
* **Advanced scoring**: use semantic similarity (e.g., embeddings) instead of strict string matching for answers.  
* **AI tutor mode**: interactive chat interface where users can ask questions about each roadmap stage.  

---

## 21) License

This project is licensed under the **MIT License**, granting permission to use, copy, modify, and distribute with proper attribution. See the `LICENSE` file for details.

---

## 22) Acknowledgments

* **Google Generative AI (Gemini)** for skill analysis and roadmap generation.  
* **Gradio** for the fast prototyping of the web interface.  
* **Tkinter** for the lightweight desktop GUI.  
* **Open-source community** for the datasets, tutorials, and tools that inspire quiz and roadmap design.  

---

## 23) Appendix

### 23.1 Example Quiz Flow

**Career Goal**: Data Scientist  

Questions:  
1. What is feature engineering?  
   *Correct Answer*: Creating new features from existing data.  

2. What is cross-validation?  
   *Correct Answer*: A technique to evaluate models by splitting data into folds.  

3. What is p-value in hypothesis testing?  
   *Correct Answer*: Probability of obtaining observed results under the null hypothesis.  

**User Score**: 2/3  

---

### 23.2 Example Roadmap Output (Excerpt)

**Career Goal**: Full Stack Developer  
**Skills Entered**: HTML, CSS, Python  

**Skill Ratings**:  
- HTML → 9/10  
- CSS → 8/10  
- Python → 7/10  

**Suggested Roadmap**:  

1. **Foundations** (2–3 weeks)  
   - Web basics, Git/GitHub, command line.  
   - Resources: MDN Docs, freeCodeCamp basics.  

2. **Frontend Mastery** (4–5 weeks)  
   - JavaScript, React fundamentals.  
   - Resources: React Docs, Scrimba React course.  

3. **Backend Development** (5–6 weeks)  
   - Node.js, Express, REST APIs.  
   - Resources: Node.js Docs, Express Handbook.  

4. **Databases** (2–3 weeks)  
   - SQL, NoSQL (MongoDB).  
   - Resources: PostgreSQL Tutorial, MongoDB University.  

5. **Deployment & Projects** (Ongoing)  
   - Docker, CI/CD basics, hosting on AWS/Render.  
   - Resources: Docker Docs, Render Deployment Guide.  

---

### 23.3 Environment File Example (`.env`)

```
GOOGLE_API_KEY=your_api_key_here
UI_MODE=gradio
MODEL_NAME=gemini-1.5-flash
```

---

### 23.4 Sample Command Reference

Run with Tkinter:  
```bash
python app.py --ui tkinter
```

Run with Gradio:  
```bash
python app.py --ui gradio
```

Run tests:  
```bash
pytest tests/
```

---

## 24) Version History

* **v1.0** (August 2025)  
  - Initial release with Tkinter + Gradio UI.  
  - Core logic for quiz, skill rating, roadmap generation.  
  - Documentation and repository structure defined.  

* **v1.1** (Planned)  
  - Export roadmap to PDF/Markdown.  
  - Multi-skill batch rating optimization.  
  - Improved error handling and UI responsiveness.  

---

## 25) Contact

**Author**: Hamza Uzzaman Pritisha Hazra Apurba Roy
**GitHub**: [https://github.com/YUSHEY](https://github.com/YUSHEY)  
**Email**: zaman.yushey@gmail.com  
API KEy: AIzaSyDXDf_D0_4krxHQx8wTCcrcZs_yrbIVuRY

---

✅ *End of Documentation*
