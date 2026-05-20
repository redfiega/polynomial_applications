# Evaluation Log — Polynomial Examples Generator VERSION 1

## What I'm measuring
The LLM is asked to connect a randomly generated polynomial to a real-world scenario. 
The core risk is that it produces a scenario that is implausible, mathematically 
inconsistent, or too vague to be useful in a classroom. 

**Definition of "good":** A good output (score 3) names a specific, recognizable 
real-world scenario, correctly interprets at least one feature of the polynomial 
(degree, sign of leading coefficient, a zero, or the general shape), and poses a 
question a student could actually answer.

## Scoring rubric
- **3 — Plausible and useful:** Scenario is realistic. At least one mathematical 
  feature of the polynomial is correctly interpreted. Discussion question is answerable.
- **2 — Plausible but shallow:** Scenario is realistic but the interpretation is 
  generic (could apply to any polynomial of that degree). Discussion question is vague.
- **1 — Implausible or inconsistent:** Scenario contradicts the polynomial's 
  mathematical behavior, or the numbers used don't match the actual expression.

---

## Results

| # | Degree | Context | Polynomial | Output summary | Score | Notes |
|---|--------|---------|------------|----------------|-------|-------|
| 1 | 2 | Business | 4x^2-4x+2 | The revenue from selling x-shirts is given by the polynomial. | 1/3 |  Wants to maximize revenue but gives a cocave up polynomial.|
| 2 | 3 | General | 4x^3+32x^2+2x+3 | The cost of producing x units of each product is given by the polynomial.| 2/3 | No need to have mention of three products. Potential analysis includes calculus instead of college algebra.|
| 3 | 4 | Healthcare |x^4-x^3-x^2+5x+5 |The dosage is related to the patient's weight (x) by the polynomial. | 2/3 | The polynomial changes in the description of the scenario. Analysis includes calculus.|
| 4 | 2 | Geometric | 3x^2-x+5 | The length and width of a rectangle are given in terms of x, the number of weeks since planting. | 1/3 | Scenario makes no sense. Garden dimensions do not depend on number of weeks. The polynomial is completely different in the worked application.|
| 5 | 3 | Business | 4x^3-2x^2-x+3 | Generated same business example as general example in line 2. | 1/3 | The polynomial changed in the explanation. No need for three products. Application is calculus.|
| 6 | 5 | General | 2x^5-2x^4-x^3-x^2-2x+4 | Total cost of producing x units of product per day. | 2/3 | The polynomial changed in the explanation. The analysis is calculus.|
| 7 | 2 | Healthcare | | | /3 | |
| 8 | 3 | Geometric | | | /3 | |
| 9 | 4 | Business | | | /3 | |
| 10 | 2 | General | | | /3 | |
| 11 | 3 | Healthcare | | | /3 | |
| 12 | 5 | Business | | | /3 | |
| 13 | 2 | Geometric | | | /3 | |
| 14 | 4 | General | | | /3 | |
| 15 | 3 | Business | | | /3 | |

**Total: 9 / 18**

---

## Summary

The application is very inconsistent. It is successful at staying within the specified domain (i.e. selecting "Healthcare" will result in a healthcare application example. However, the real-world example it generates will use a completely different polynomial than what it displays initially. The system also does not seem to recognize the difference between college algebra topics (such discussing end-behavior, zeros and their multiplicity, or solving when possible) from calculus topics (like taking derivatives and finding critical points).

---

## What I learned
The app is functioning on a mechanical level, but it is not serving the purpose it was designed for. I stopped generating examples after the initial 6 generated examples all failed to meet expectations. Further refining is needed.