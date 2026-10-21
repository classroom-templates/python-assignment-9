# Assignment 9 — Program Design

Complete this document before or during the early stages of development.

This is a **guided design worksheet**, not a formal software-engineering document.

Keep your answers concise and specific to your actual program.

Update this document if your design changes during implementation.

---

# 1. Data Representation

## One Transaction

Show how one transaction will be represented in Python.

Example format:

```python
(transaction_id, category, amount)
```

Explain what each position represents and its data type.

**Your answer:**

---

## Transaction Collection

Explain how the complete collection of transactions will be stored in memory.

**Your answer:**

---

## Category Totals

Explain how category totals will be represented.

**Your answer:**

---

# 2. Module Responsibilities

Complete one section for every application module in your program.

## `main.py`

**Responsibility:**  
Describe what `main.py` coordinates.

**Should contain:**  
List the major actions it performs.

**Should NOT contain:**  
List work that belongs in supporting modules.

---

## `data_io.py`

**Responsibility:**  
Describe what file-related work belongs here.

**Functions:**  
List the functions this module contains.

---

## Processing Module 1: `__________________.py`

**Responsibility:**  
Explain what kind of processing this module owns.

**Functions:**  
List the functions you plan to place here.

---

## Processing Module 2: `__________________.py`

Complete this section only if you use a second processing module.

**Responsibility:**  

**Functions:**  

---

# 3. Planned Functions

Complete one entry for each important function you design.

Copy this section as many times as needed.

## Function: `__________________`

**Module:**  
`__________________.py`

**Responsibility:**  
What one major job does this function perform?

**Parameters:**  
What data does it receive?

**Return Value:**  
What does it return?

**Side Effects:**  
Does it print, modify data, read a file, or write a file?

---

# 4. Data Flow

Show how data moves through your program.

Use a simple text diagram.

Example structure:

```text
transactions.txt
      ↓
read_transactions()
      ↓
transaction records
      ↓
processing functions
      ↓
calculated results
      ↓
write_report()
      ↓
transaction_report.txt
```

Replace the example with the actual data flow of your program.

**Your data-flow diagram:**

```text

```

---

# 5. Student Test Plan

Before completing `student_tests.py`, briefly plan each required test.

## Normal Case

**Function or behavior being tested:**  

**Test data:**  

**Expected result:**  

---

## Boundary or Edge State

**Function or behavior being tested:**  

**Boundary or edge state:**  

**Expected result:**  

---

## State or Invariant

**Operation being tested:**  

**What should change:**  

**What must remain true:**  

---

## Student-Selected Risk

**Risk identified:**  

**Why this could fail:**  

**Expected behavior:**  

---

# 6. Design Changes

Complete this section after implementation.

## Did your final architecture differ from your original plan?

If yes, briefly explain:

- what changed;
- why you changed it; and
- why the final design is better for this program.

If no major changes were needed, say so.

**Your answer:**
