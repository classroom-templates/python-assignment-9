# Assignment 9 — Reflection

Answer each question clearly, specifically, and in your own words.

This reflection is **not** a second version of `DESIGN.md`.

`DESIGN.md` documents the architecture you planned and ultimately implemented.

`ESSAY.md` asks you to reflect on the decisions you made, what changed during development, how you verified the program, and how you used generative AI.

Your responses must demonstrate actual engagement with your completed project.

Short, vague, or generic answers will not receive full credit.

Whenever possible, refer to specific modules, functions, tests, failures, or design decisions from your own program.

Each question is worth **2.5 points**, for a total of **10 points**.

---

## 1. Architectural Decision

Choose **one architectural decision** you made in this assignment.

Examples include:

- how you divided processing responsibilities between modules;
- why a particular function belongs in one module rather than another;
- how you decided what `main()` should coordinate;
- how you represented transaction or category data.

Explain:

- what decision you made;
- what reasonable alternative you considered;
- why you chose your final approach; and
- how that choice affected the clarity or organization of the program.

Do not simply repeat the contents of `DESIGN.md`.

The purpose of this question is to explain the reasoning behind one of your design choices.

---

## 2. Design Change During Development

Compare your original plan in `DESIGN.md` with your completed program.

Identify **one thing that changed** during implementation.

This might involve:

- a function interface;
- a module responsibility;
- the number of functions;
- the way data moved through the program;
- a test you added after discovering a risk; or
- another meaningful design decision.

Explain:

- what changed;
- what caused you to reconsider the original design;
- why the final version is better or more appropriate; and
- what this taught you about designing before coding.

If your architecture changed very little, identify one design decision that you reconsidered and explain why you kept the original approach.

---

## 3. Testing and Verification

Choose **one of the tests you designed in `student_tests.py`**.

Explain:

- what requirement, state, boundary, invariant, or risk the test verifies;
- why you selected the test data;
- how you determined the expected result;
- what kind of defect the test could expose; and
- why simply running the program once would provide weaker evidence.

Your answer should demonstrate the testing ideas from the Systematic Testing and Verification lectures.

Do not merely restate the test code.

---

## 4. Generative AI and Engineering Judgment

Describe **one meaningful suggestion from generative AI** that you:

- accepted;
- rejected; or
- modified substantially.

The suggestion may involve:

- architecture;
- function decomposition;
- testing;
- debugging;
- file handling;
- documentation; or
- another important part of the assignment.

Explain:

- what AI suggested;
- how you evaluated the suggestion;
- what decision you ultimately made; and
- why that decision was appropriate for this assignment.

Your answer should show that you used AI as a development partner while retaining responsibility for the final program.

##  5. Integration and Architecture
Describe one place where two parts of your program had to agree about data, state, or an interface. Explain what could have gone wrong if those assumptions did not match, and how you verified the integration worked correctly.
