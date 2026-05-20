# Build Log — Polynomial Examples Generator

## Who built this
I am a college algebra instructor with no prior coding experience. 
This project was built entirely with AI assistance (GitHub Copilot in VS Code, 
then Claude) as part of an introductory generative AI course.

## What the app does
Generates a random polynomial of a chosen degree, computes its factored form and 
zeros using SymPy, plots it, then uses an LLM to produce a real-world example 
connecting the polynomial to a practical context (business, healthcare, etc.).

---

## Session 1 — Initial build

**Goal:** Get a working local prototype.

**Stack decision:** Started with Ollama running a local model. Chose this because 
it required no API key and I could run it offline. Used Streamlit for UI because 
it generates a working web interface from plain Python with minimal setup.

**What worked:** The SymPy integration for factoring and zeros worked well. 
Streamlit made it easy to add interactive widgets (dropdowns, checkbox, button).

**Problem encountered:** Ollama was too slow for classroom use — each generation 
took 30–60 seconds. Also couldn't share the app with students because it only 
ran on my laptop.

---

## Session 2 — Model swap and deployment

**Decision:** Switched from Ollama/tinyllama to Groq API with llama-3.3-70b-versatile.

**Why Groq:** Free tier, fast inference, no local hardware dependency. 
The speed difference was dramatic — responses went from ~45 seconds to ~2 seconds.

**Deployment:** Moved to Streamlit Cloud. Storing the API key in st.secrets so 
it never appears in the code or GitHub repo.

**Problem encountered:** Had to learn how .gitignore works to make sure 
secrets.toml was excluded from version control.

---

## Session 3 (P2 revision) — Prompt engineering, system prompt, grounding, evaluation

**Problem identified by reviewer:** The original app sent only a user message with 
no system prompt, no role framing, no output structure, and no grounding for what 
"real-world" means.

**Change 1 — System prompt added:**
Wrote a dedicated system prompt that gives the model a role (college algebra instructor), 
specifies a required output structure (Context / Interpretation / Discussion question), 
sets a word limit (150 words), and prohibits jargon. This is now sent as the `system` 
role message in every API call.

**Change 2 — Prompt engineering:**
Restructured the user prompt to explicitly label each input (polynomial expression, 
degree, context category), inject the grounding list, and ask for the output structure 
by name. Earlier version was a single run-on sentence.

**Change 3 — Grounding:**
Added `APPLICATION_DOMAINS` dictionary — a small curated list of plausible real-world 
scenarios per context category. These are injected into every user prompt so the model 
draws from known-good scenarios rather than inventing implausible ones.

**Change 4 — Typo fix:**
Fixed "polnomial" → "polynomial" in st.info() copy.

---

## Prompts tried during P2 revision

**Attempt 1 (original):**
> "Generate a real-world example for the polynomial {poly} in {context} context, 
> suitable for college algebra students. Explain its application and how to analyze it. 
> Keep the explanation clear and concise."

Problem: No role. No structure. "Clear and concise" is not a measurable constraint. 
Model sometimes produced responses over 400 words, or invented contexts with no 
connection to the actual polynomial coefficients.

**Attempt 2:**
Added role framing ("You are a math educator...") to the user prompt. 
Better tone, but output structure was still inconsistent — sometimes bullet points, 
sometimes paragraphs, sometimes included LaTeX.

**Attempt 3 (final):**
Moved role framing to system prompt. Added explicit 3-part output structure 
(Context / Interpretation / Discussion question). Added word limit. 
Added grounded domain list. Results became consistent and classroom-appropriate
(after a few adjustments). Fixed zeros analysis error.

---

## Known limitations

- Polynomials with large or irrational coefficients sometimes produce examples 
  where the numbers don't make physical sense (e.g., a negative leading coefficient 
  in a "height of a projectile" example implying the object starts underground).
- The app does not validate whether the LLM's interpretation is mathematically 
  consistent with the actual polynomial — that check is still done by the instructor.
- Random coefficient generation occasionally produces polynomials with no real zeros, 
  which makes the "zeros analysis" section less useful for classroom demonstration.