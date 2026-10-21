# Assignment 9 — Transaction Analysis System

## Description

**Read this entire assignment before you begin.**

Assignment 9 is your first **guided architecture assignment**.

In earlier assignments, most of the program architecture was supplied to you:

- module names;
- function names;
- parameter lists;
- major data flow; and
- much of the overall decomposition.

In this assignment, some of those decisions become yours.

You will build a multifile transaction-analysis program that:

- reads transaction records from a text file;
- converts the file data into an internal Python representation;
- performs several calculations and classifications;
- writes a formatted report;
- handles a missing input file;
- uses a small procedural architecture with clear responsibilities;
- uses instructor-supplied acceptance tests; and
- includes student-designed tests for your own processing functions.

The primary learning goal is not a new Python feature.

The primary goal is to begin making **reasonable architectural decisions** about how a larger procedural program should be organized.

---

# Learning Objectives

By completing this assignment, you should be able to:

- identify the major responsibilities in a program specification;
- represent structured data appropriately;
- separate file I/O from processing logic;
- design one or two processing modules with coherent responsibilities;
- design functions with clear parameters, return values, and side effects;
- use `main()` as an application driver rather than as the location of all implementation logic;
- keep dependencies visible through parameters and return values;
- implement a program incrementally rather than all at once;
- integrate multiple modules through explicit data flow;
- use supplied acceptance tests to verify major program requirements;
- design several meaningful tests for your own functions;
- distinguish normal cases, boundaries, state/invariant tests, and identified risks;
- handle a missing input file with a narrow exception handler;
- document architectural decisions in a lightweight design document;
- maintain meaningful incremental Git history; and
- use generative AI as a design and development partner while retaining responsibility for the final architecture and implementation.

---

# Background

Before beginning this assignment, complete and review:

- **Systematic Testing and Verification Part I** lecture and notes;
- **Systematic Testing and Verification Part II** lecture and notes;
- **Integrated Procedural Design Part I** lecture and notes;
- **Integrated Procedural Design Part II** lecture and notes;
- **File I/O Part I and Part II** lecture and notes;
- **Modularity and Multifile Programs Part I and Part II** lecture and notes;
- the course [Best Practices for Procedural Programming](https://katrompas.accprofessors.com/best-practice-procedural-programming);
- the course [Testing Guidelines](https://katrompas.accprofessors.com/testing);
- the course [Commenting Guidelines](https://katrompas.accprofessors.com/commenting);
- the [.gitignore Guidelines](https://katrompas.accprofessors.com/gitignore-guidelines);
- the [README Guidelines](https://katrompas.accprofessors.com/readme-guidelines); and
- the course [Commit Guidelines](https://katrompas.accprofessors.com/committing).

This assignment assumes that you already understand:

- functions and function contracts;
- `main()` as the application driver;
- modules and imports;
- lists, tuples, and dictionaries;
- file input/output;
- exception handling;
- testing with `assert`;
- state, transitions, and invariants;
- and the course rule of no more than one `return` statement per function.

---

# Starter Repository

Your starter repository will contain:

```text
ASSIGNMENT.md
ESSAY.md
DESIGN.md
README.md
.gitignore
main.py
data_io.py
transactions.txt
test.py
student_tests.py
```

You will create **one or two additional processing/analysis modules** as part of your design.

Examples of reasonable module names might include:

```text
analysis.py
processing.py
summary.py
classification.py
```

You are not required to use those names.

Your completed application must contain:

```text
main.py
data_io.py
one or two student-designed processing modules
```

Therefore your application should use **three or four Python application modules total**.

Do not create a large collection of tiny modules.

Do not modify:

```text
transactions.txt
test.py
```

You **will** complete and modify:

```text
student_tests.py
DESIGN.md
README.md
ESSAY.md
```

`DESIGN.md` is already structured for you as a guided worksheet. Complete the
provided sections rather than inventing a design-document format.

---

# Part I — Required Transaction Data

The supplied file:

```text
transactions.txt
```

contains:

```text
1001,Groceries,84.27
1002,Utilities,142.80
1003,Entertainment,38.50
1004,Groceries,63.19
1005,Transportation,51.25
1006,Utilities,96.40
1007,Entertainment,120.00
1008,Groceries,107.65
```

Each line represents one transaction in this format:

```text
transaction_id,category,amount
```

For example:

```text
1001,Groceries,84.27
```

must become:

```python
(1001, "Groceries", 84.27)
```

with these data types:

```text
int, str, float
```

The complete transaction collection should be represented as a list of transaction tuples.

The supplied transaction file is guaranteed to contain valid records in the required format.

You are **not** required to validate malformed transaction records.

The program **is** required to handle the case in which `transactions.txt` cannot be found.

---

# Part II — Required Architecture

This assignment gives you some architectural freedom, but it also defines several required boundaries.

## Required `main.py`

`main.py` is the application driver.

It should coordinate the major program steps.

It should **not** contain the implementation of the calculations or file-processing logic.

`main.py` must:

- use the standard run guard;
- coordinate the read → process → report sequence;
- handle a missing `transactions.txt` file;
- call functions in the supporting modules; and
- display the required final console message.

`main.py` must not call `open()` directly.

File access belongs in `data_io.py`.

---

## Required `data_io.py`

`data_io.py` owns the application's external text-file boundary.

It must contain these exact required functions:

```python
read_transactions(filename)
```

and:

```python
write_report(
    filename,
    transactions,
    total_spending,
    average_transaction,
    largest_transaction,
    category_totals,
    highest_category,
    classification,
)
```

The supplied tests depend on these exact interfaces.

You may add another small file-I/O helper only if it is genuinely useful and remains appropriate to the assignment.

---

## Student-Designed Processing Module(s)

You must create **one or two** additional modules that own the program's processing responsibilities.

These modules must:

- perform calculations and classifications;
- receive required data through parameters;
- return calculated results;
- not call `open()`;
- not write files;
- not print program output; and
- not depend on hidden global program state.

You decide:

- the module name or names;
- the processing function names;
- the parameter lists;
- the return values; and
- how the required processing responsibilities are divided between functions.

Keep the architecture small and understandable.

> More modules and more abstractions do not automatically create a better design.

---

# Part III — Required File-I/O Functions

## `read_transactions(filename)`

This function must:

- open the supplied filename for reading;
- read records line by line;
- remove the line ending;
- split each record using the comma delimiter;
- convert the transaction ID to `int`;
- keep the category as `str`;
- convert the amount to `float`;
- create tuples in this form:

  ```python
  (transaction_id, category, amount)
  ```

- append the tuples to a list;
- return the completed transaction list;
- contain no more than one `return` statement; and
- not print anything.

Use the normal course file pattern:

```python
with open(filename, "r") as file:
```

Do not hardcode the supplied transaction data.

The function must work with alternate valid transaction files.

---

## `write_report(...)`

The exact interface is:

```python
write_report(
    filename,
    transactions,
    total_spending,
    average_transaction,
    largest_transaction,
    category_totals,
    highest_category,
    classification,
)
```

This function must:

- open the supplied output filename using write mode;
- create or replace the report file;
- use the completed results supplied through its parameters;
- write the required report format;
- format monetary values with exactly two digits after the decimal point;
- return no calculated result;
- contain no more than one `return` statement; and
- not repeat calculations that belong in a processing module.

Use:

```python
with open(filename, "w") as file:
```

The report is generated output, so overwriting the previous report is the correct behavior.

---

# Part IV — Required Processing Capabilities

Your processing module or modules must provide functions that collectively perform all of the following responsibilities.

You decide the exact function names and interfaces.

## 1. Calculate total spending

For the supplied transaction file:

```text
$704.06
```

Do not hardcode the result.

---

## 2. Calculate average transaction amount

For the supplied transaction file:

```text
$88.01
```

when formatted to two decimal places.

Do not hardcode the result.

---

## 3. Calculate totals by category

For the supplied transaction file:

```text
Groceries: $255.11
Utilities: $239.20
Entertainment: $158.50
Transportation: $51.25
```

A dictionary is an appropriate representation for category totals.

For example:

```python
{
    "Groceries": 255.11,
    "Utilities": 239.20,
}
```

Categories should remain in the order in which they are first encountered in the transaction data.

---

## 4. Find the largest transaction

For the supplied data:

```text
1002 - Utilities - $142.80
```

The processing function should return the complete transaction record or another clear representation that allows the report to be produced correctly.

If equal maximum amounts occur, preserving the first maximum encountered is acceptable.

---

## 5. Find the highest-spending category

Using the category totals, determine which category has the greatest total spending.

For the supplied data:

```text
Groceries - $255.11
```

Return a useful representation such as:

```python
("Groceries", 255.11)
```

If equal maximum category totals occur, preserving the first maximum encountered is acceptable.

---

## 6. Classify overall spending

Use these exact thresholds:

```text
$750.00 or more       High
$500.00–$749.99       Moderate
below $500.00         Low
```

For the supplied data:

```text
Moderate
```

The threshold values are important test boundaries.

---

# Part V — Application Driver Behavior

The required filenames are:

```python
input_filename = "transactions.txt"
output_filename = "transaction_report.txt"
```

Your `main()` must coordinate the program so that it:

1. attempts to read `transactions.txt`;
2. handles `FileNotFoundError` at the application level;
3. performs the required analysis using your processing module(s);
4. sends the completed results to `data_io.write_report()`;
5. creates `transaction_report.txt`; and
6. displays the required completion message.

Use a narrow exception handler around the file-reading operation.

A reasonable structure is conceptually:

```text
attempt to read the file
    ↓
if the file is missing:
    display the required error message

otherwise:
    perform analysis
    write report
    display completion message
```

Do not put the entire application inside one large `try` block.

---

# Part VI — Missing Input File Behavior

If:

```text
transactions.txt
```

does not exist, the program must not crash.

It must display exactly:

```text
Error: transactions.txt was not found.
```

The program must not create:

```text
transaction_report.txt
```

when the source file is unavailable.

---

# Part VII — Required Program Output

Running:

```bash
python main.py
```

with the supplied `transactions.txt` must display exactly:

```text
Report written to transaction_report.txt.
```

The generated:

```text
transaction_report.txt
```

must contain:

```text
Transaction Analysis Report

Transactions Processed: 8
Total Spending: $704.06
Average Transaction: $88.01
Largest Transaction: 1002 - Utilities - $142.80

Category Totals
Groceries: $255.11
Utilities: $239.20
Entertainment: $158.50
Transportation: $51.25

Highest-Spending Category: Groceries - $255.11
Overall Spending Classification: Moderate
```

Do not hardcode the report.

The report must be generated from:

- the records read from the file; and
- the results returned by your processing functions.

---

# Part VIII — `DESIGN.md`

The starter repository includes a **guided `DESIGN.md` worksheet**.

You are **not** expected to invent the format of a formal software-design document.

Instead, complete the supplied sections using the actual design decisions for your program.

The purpose of `DESIGN.md` is to make you think through the program's architecture before and during implementation.

Complete it **before or during the early stages of development**, then update it if your design changes.

The supplied worksheet asks you to document:

- how your transaction data is represented;
- the responsibility of each application module;
- the important functions you plan to create;
- the parameters, return values, and side effects of those functions;
- how data moves through the complete program;
- the four required student-designed test categories; and
- any important design changes made during implementation.

Keep your answers concise and specific.

This is not a formal software-engineering document and does not need to be long.

Your final `DESIGN.md` must accurately describe the architecture of your completed program.

---

# Part IX — Instructor-Supplied Tests

The repository contains:

```text
test.py
```

Do not modify it.

Run:

```bash
python test.py
```

or:

```bash
python3 test.py
```

depending on your system.

The supplied tests intentionally verify the **major acceptance contract** without prescribing every detail of your student-designed processing architecture.

They verify:

- required project structure;
- one or two student-designed processing modules;
- exact `data_io.py` interfaces;
- safe imports;
- the standard `main.py` run guard;
- transaction parsing with alternate data;
- report writing with alternate supplied results;
- complete behavior with the supplied transaction file;
- complete behavior with alternate transaction data;
- missing-file handling;
- separation of file I/O from processing logic; and
- normal course function/control-flow standards.

Your completed program should report:

```text
10/10 tests passed
All supplied acceptance tests passed.
```

Passing the supplied tests is necessary, but it is not the complete assignment grade.

The supplied tests deliberately do **not** verify every function you design.

That is part of your responsibility in this assignment.

There is **no Classroom 50 autograding** for this assignment.

---

# Part X — Student-Designed Tests

The repository also contains:

```text
student_tests.py
```

You must complete it.

Do not replace the supplied runner.

You must complete the four required student-designed test functions.

## 1. Normal-case test

Test one student-designed processing capability using ordinary valid data.

The test must:

- construct its own test data;
- call one of your processing functions; and
- use one or more assertions with a known expected result.

---

## 2. Boundary or edge-state test

Test a meaningful boundary or unusual valid state.

The spending-classification thresholds are one natural possibility:

```text
499.99
500.00
749.99
750.00
```

You may choose another meaningful boundary or edge state if appropriate to your design.

---

## 3. State or invariant test

Verify an important state relationship or invariant.

For example, you might verify that:

- a processing function produces the correct result; and
- the supplied transaction collection remains unchanged.

Your test should make clear what is expected to change and/or what must remain true.

---

## 4. Student-selected risk test

Identify one behavior that you believe could reasonably fail.

Construct a test for that risk.

In the test docstring `:note:` field, explain:

- what risk you identified;
- why you chose it; and
- what requirement or assumption the test verifies.

---

## Student-Test Rules

Each test must:

- be independent of the other student tests;
- create the state or data it needs;
- have a known expected result;
- use one or more `assert` statements;
- verify actual application behavior;
- follow normal course documentation standards; and
- not simply copy an instructor-supplied test.

A single test may contain multiple assertions when those assertions all verify one coherent requirement, boundary, state, or invariant.

Run:

```bash
python student_tests.py
```

Your completed test file should report:

```text
4/4 student tests passed
All student-designed tests passed.
```

A student-written test that always passes without actually verifying meaningful behavior does not satisfy the requirement.

---

# Part XI — Programming and Architecture Standards

The normal course programming standards apply.

In particular:

- every source file must contain required file-header documentation;
- every function must contain a course-standard function docstring;
- each function may contain no more than one `return` statement;
- computational functions return results rather than print;
- processing modules do not perform file I/O;
- processing modules do not print program output;
- `data_io.py` owns file access;
- `main.py` coordinates the application;
- application modules must be safe to import;
- dependencies should be explicit through parameters and return values;
- avoid global program state;
- keep the architecture small and understandable.

Do not use:

- `while True`;
- `break`;
- `continue`;
- recursion;
- classes;
- lambda expressions;
- additional third-party libraries; or
- architecture that is unnecessarily complex for this problem.

This is still a procedural-programming assignment.

Object-oriented design will be introduced later.

---

# Part XII — Documentation Requirements

Complete all source-file and function documentation according to the course Commenting Guidelines.

Function docstrings must begin with a short description and then use exactly the course-standard fields:

```python
"""
Short description of what the function does.

:param: ...
:raises: ...
:return: ...
:note: ...
"""
```

Use wording appropriate to the actual function.

For example, do not write:

```text
:param: data
```

if you can clearly explain what the parameter represents.

Documentation should describe the real contract of the function you designed.

---

# Part XIII — Development Process and Git

This assignment should be developed incrementally.

Do not design the entire architecture, write the entire program, and then create one final code commit.

Your repository must contain **at least ten meaningful development commits**.

Ten is the minimum, not the target.

Because architecture is part of this assignment, meaningful `DESIGN.md` work may count when it reflects real design progress.

Natural development milestones may include:

- initial architecture/design plan;
- transaction parsing;
- one completed processing capability;
- category-total processing;
- largest/highest calculations;
- spending classification;
- report generation;
- missing-file handling;
- integration through `main.py`;
- one completed student-designed test category;
- correction of a real integration failure;
- refinement of module/function organization; or
- another coherent program improvement.

Changes only to:

```text
README.md
ESSAY.md
```

do not count toward the required development commits.

Do not manufacture meaningless commits merely to reach the minimum.

The normal workflow is:

```text
make a coherent change
test it
run the relevant test suite
commit
push
```

---

# Part XIV — Generative AI

Use of generative AI is required.

AI may assist with:

- identifying responsibilities;
- proposing module structures;
- designing function interfaces;
- reviewing data flow;
- explaining file-I/O or dictionary logic;
- designing test cases;
- identifying boundaries and invariants;
- debugging integration failures;
- reviewing architecture; and
- improving documentation.

You remain responsible for the final design.

In particular, you must be able to explain:

- why your modules exist;
- why each major function belongs where you placed it;
- how data moves through the application;
- why your student-written tests are meaningful;
- and why your final architecture is appropriate to the problem.

AI may suggest architecture that is far more complicated than this assignment requires.

For example, AI may suggest:

- classes;
- many tiny modules;
- factories;
- configuration layers;
- service layers;
- generic utilities;
- design patterns; or
- other abstractions that are not appropriate here.

Do not accept additional architecture merely because it sounds sophisticated.

> The goal is the simplest reasonable architecture that clearly organizes the required responsibilities.

---

# Part XV — `README.md`

Complete the supplied README according to the course [README Guidelines](https://katrompas.accprofessors.com/readme-guidelines).

Your README should accurately describe:

- what the application does;
- your module structure;
- the responsibility of each application module;
- the input file;
- the output file;
- how to run the program;
- how to run `test.py`;
- how to run `student_tests.py`; and
- any other information required by the course README standard.

---

# Part XVI — `ESSAY.md`

Complete all supplied reflection questions.

The reflection will focus on:

- your architectural decisions;
- your function decomposition;
- data flow;
- student-designed testing; and
- your use of AI as an architectural and development partner.

Your responses must refer to your actual completed project.

---

# Final Review and Submission

Before submitting:

## 1. Review `DESIGN.md`

Confirm that it accurately describes the completed program.

---

## 2. Run the complete program

```bash
python main.py
```

Verify:

```text
Report written to transaction_report.txt.
```

---

## 3. Inspect the generated report

Open:

```text
transaction_report.txt
```

and verify the required calculations, category order, classification, and formatting.

---

## 4. Verify missing-file behavior

Temporarily rename or move:

```text
transactions.txt
```

and verify that the program displays:

```text
Error: transactions.txt was not found.
```

Restore the file immediately afterward.

Do not submit with the input file missing or renamed.

---

## 5. Run the supplied acceptance tests

```bash
python test.py
```

Verify:

```text
10/10 tests passed
All supplied acceptance tests passed.
```

---

## 6. Run your student-designed tests

```bash
python student_tests.py
```

Verify:

```text
4/4 student tests passed
All student-designed tests passed.
```

---

## 7. Check Git status

```bash
git status
```

Your working tree should be clean.

---

## 8. Review development history

```bash
git log --oneline
```

Verify that the history shows meaningful incremental design, implementation, testing, and integration.

---

## 9. Review the repository

Confirm that the repository contains:

```text
ASSIGNMENT.md
ESSAY.md
DESIGN.md
README.md
.gitignore
main.py
data_io.py
transactions.txt
test.py
student_tests.py
your processing module(s)
```

The generated:

```text
transaction_report.txt
```

may also be present in the completed repository if required by your instructor.

---

## 10. Review documentation

Verify that:

- every source file has complete file-header documentation;
- every function uses the course-standard docstring format;
- `DESIGN.md` reflects the completed architecture;
- `README.md` is complete;
- `ESSAY.md` is complete;
- `student_tests.py` contains four meaningful completed tests; and
- temporary debugging code has been removed.

---

## 11. Submit through Blackboard

Submit the normal HTTPS URL of the completed GitHub repository in Blackboard.
