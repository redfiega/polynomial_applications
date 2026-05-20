import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from groq import Groq

st.title("Polynomial Examples Generator")
st.info("This app uses Groq AI to generate real-world polynomial examples.")

APPLICATION_DOMAINS = {
    "Business": [
        "total revenue as a function of units sold (evaluate for specific quantities)",
        "total cost modeled as a polynomial — find break-even points by solving for zeros",
        "profit over time — discuss end behavior to reason about long-run trends",
    ],
    "Healthcare": [
        "drug concentration in the bloodstream over time — evaluate at specific hours",
        "patient recovery score as a function of days — find when it returns to baseline using zeros",
        "modeled health metric over time — describe end behavior and what it means clinically",
    ],
    "General": [
        "height of a projectile as a function of time — find when it hits the ground using zeros (degree 2 only)",
        "distance traveled as a polynomial function of time — evaluate at specific times",
        "a quantity that rises and falls — describe end behavior and zeros",
    ],
    "Geometric": [
        "area of a shape as a function of a side length — evaluate for specific dimensions",
        "volume as a polynomial function of a dimension — find zeros to interpret physical constraints",
        "perimeter or surface area model — discuss end behavior as the dimension grows",
    ],
}

SYSTEM_PROMPT = """You are an experienced college algebra instructor creating 
real-world examples to help students connect abstract polynomial functions to 
practical applications.

IMPORTANT CONSTRAINTS — read carefully:
- This is a COLLEGE ALGEBRA course, not calculus. Never mention derivatives, 
  critical points, or any optimization technique that requires calculus.
- The only maximizing or minimizing allowed is for degree 2 polynomials using 
  the vertex formula (-b/2a). Do not discuss maxima or minima for degree 3 or higher.
- Algebra topics you may use: evaluating the polynomial at specific values, 
  solving for zeros, interpreting zeros and their multiplicities, describing 
  end behavior (what happens as x → ∞ or x → -∞).

Your output must follow this structure exactly:
1. Context (1–2 sentences): Name the real-world scenario and state what x and y represent, including units.
2. Interpretation (2–3 sentences): Explain what the end behavior and/or zeros mean in this context. Use plain language a college algebra student would understand.
3. Discussion question (1 sentence): Pose one question a student could answer using only algebra — evaluating, solving, or interpreting end behavior.

Keep the total response under 150 words."""

degree = st.selectbox("Select polynomial degree", [2, 3, 4, 5])
context = st.selectbox("Select real-world context", ["Business", "Healthcare", "General", "Geometric"])
factorable = st.checkbox("Include factorable polynomials with zeros analysis")

if st.button("Generate Example"):

    x = sp.Symbol('x')
    coeffs = [int(c) for c in np.random.randint(-5, 6, degree + 1)]
    coeffs[0] = int(np.random.randint(1, 6))
    sym_poly = sum(c * x**(degree - i) for i, c in enumerate(coeffs))

    poly_func = sp.lambdify(x, sym_poly, 'numpy')

    st.write("Generated polynomial:")
    st.latex(sp.latex(sym_poly))

    factors = sp.factor(sym_poly)
    st.write("Factored form:")
    st.latex(sp.latex(factors))

    if factorable:
        roots = sp.solve(sym_poly, x)
        real_roots = [r for r in roots if sp.im(r) == 0]

        if real_roots:
            distinct_roots = sorted(set(real_roots), key=lambda r: float(r.evalf()))
            st.markdown("**Zeros and multiplicities:**")
            for root in distinct_roots:
                try:
                    mult = sp.multiplicity(root, sym_poly)
                    st.markdown(f"- $x = {sp.latex(root)}$ (multiplicity {mult})")
                except (ValueError, TypeError):
                    st.markdown(f"- $x = {sp.latex(root)}$")
        else:
            st.info("This polynomial has no real zeros.")

    x_vals = np.linspace(-10, 10, 400)
    y_vals = poly_func(x_vals)
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True)
    st.pyplot(fig)

    st.write("Generating real-world example...")

    domain_examples = "\n".join(f"- {d}" for d in APPLICATION_DOMAINS[context])

    user_prompt = f"""The polynomial is: {sp.expand(sym_poly)}
Degree: {degree}
Context category: {context}

Real-world scenarios appropriate for college algebra in this category:
{domain_examples}

Using one of these scenarios, generate a real-world example for this exact polynomial 
following the required output structure. The polynomial expression in your response 
must exactly match: {sp.expand(sym_poly)}"""

    try:
        client = Groq(api_key=st.secrets["groq"]["api_key"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        st.write("Real-world example:")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}")