import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import ollama

st.title("Polynomial Examples Generator")
st.info("Make sure Ollama is running locally on your computer before generating examples.")

# User inputs
degree = st.selectbox("Select polynomial degree", [2, 3, 4, 5])
context = st.selectbox("Select real-world context", ["Business", "Healthcare", "General", "Geometric"])
factorable = st.checkbox("Include factorable polynomials with zeros analysis")

if st.button("Generate Example"):
    # Generate random polynomial
    coeffs = np.random.randint(-5, 6, degree + 1)
    coeffs[-1] = np.random.randint(1, 6)  # Ensure leading coeff positive
    poly = np.poly1d(coeffs)
    
    # Convert to SymPy for math rendering
    x = sp.Symbol('x')
    sym_poly = sum(c * x**i for i, c in enumerate(coeffs))
    st.write("Generated polynomial:")
    st.latex(sp.latex(sym_poly))
    
    # Analyze if factorable
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
    
    # Plot
    x_vals = np.linspace(-10, 10, 400)
    y_vals = poly(x_vals)
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True)
    st.pyplot(fig)
    
    # AI-generated example using Ollama
    st.write("Generating real-world example...")
    prompt = f"Generate a real-world example for the polynomial {poly} in {context.lower()} context, suitable for college algebra students. Explain its application and how to analyze it. Keep the explanation clear and concise."
    try:
        response = ollama.chat(
            model='tinyllama',
            messages=[{'role': 'user', 'content': prompt}]
        )
        st.write("Real-world example:")
        st.write(response['message']['content'])
    except Exception as e:
        st.error(f"Error: {e}. Make sure Ollama is running and the llama2:latest model is installed.")