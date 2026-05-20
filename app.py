import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from groq import Groq

st.title("Polynomial Examples Generator")
st.info("This app uses Groq AI to generate real-world polynomial examples.")

# Grounding: curated list of application domains injected into every prompt
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

    # Build polynomial in SymPy first, then derive numpy version from it
    # This ensures the graph and the LLM prompt use the SAME polynomial
    x = sp.Symbol('x')
    coeffs = [int(c) for c in np.random.randint(-5, 6, degree + 1)]
    coeffs[0] = int(np.random.randint(1, 6))  # positive leading coefficient
    sym_poly = sum(c * x**(degree - i) for i, c in enumerate(coeffs))

    # Convert sym_poly to a numpy-callable function for plotting
    poly_func = sp.lambdify(x, sym_poly, 'numpy')

    st.write("Generated polynomial:")
    st.latex(sp.latex(sym_poly))

    factors = sp.factor(sym_poly)
    st.write("Factored form:")
    st.latex(sp.latex(factors))

    if factorable:
        roots = sp.solve(sym_poly, x)
        distinct_roots = sorted(set(roots), key=lambda r: str(r))
        root_info = [f"${sp.latex(root)}$ (multiplicity {sp.multiplicity(root, sym_poly)})" for root in distinct_roots]
        st.markdown("**Zeros and multiplicities:**")
        for info in root_info:
            st.markdown(f"- {info}")

    # Plot using the same polynomial as the LLM prompt
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