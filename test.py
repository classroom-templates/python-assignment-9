#!/usr/bin/env python3

"""
Assignment 9 — Supplied Tests

Run this test module from the project directory with:

    python test.py

or:

    python3 test.py

These instructor-supplied tests verify the major Assignment 9 acceptance
requirements while intentionally leaving some of the student's internal
architecture and testing responsibilities open.

DO NOT MODIFY THIS FILE.

Unlike earlier assignments, these tests do not attempt to verify every
student-designed analysis function independently. Assignment 9 requires you
to make some architectural decisions yourself and to write additional tests
for your own design.

The supplied tests focus on:

- required project structure;
- the required file-I/O boundary;
- safe imports and the standard run guard;
- parsing alternate transaction data;
- report writing;
- complete-program behavior with the supplied data;
- complete-program behavior with alternate data;
- missing-file handling;
- separation of file I/O from processing modules; and
- normal course control-flow standards.

Passing these tests is necessary, but it is not the same as earning a perfect
assignment grade. The tests do not evaluate every architecture decision,
student-written test, documentation requirement, DESIGN.md explanation,
Git-history requirement, or ESSAY response.

The goal is not merely to make the supplied tests pass.

The goal is to design, implement, test, and explain a coherent program.
"""

import ast
import importlib
import io
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "main.py",
    "data_io.py",
    "transactions.txt",
]

DATA_IO_FUNCTIONS = {
    "read_transactions": ["filename"],
    "write_report": [
        "filename",
        "transactions",
        "total_spending",
        "average_transaction",
        "largest_transaction",
        "category_totals",
        "highest_category",
        "classification",
    ],
}


def normalize_output(text):
    """
    Normalize line endings and trailing whitespace for reliable comparison.

    :param: text - Output or file-content string to normalize.
    :raises: none
    :return: Normalized string.
    :note: Makes comparisons consistent across operating systems.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    result = "\n".join(
        line.rstrip() for line in text.strip().splitlines()
    )

    return result


def load_tree(filename):
    """
    Read and parse one Python source file for structural testing.

    :param: filename - Python source filename located in the project directory.
    :raises: AssertionError if the file is missing or contains a syntax error.
    :return: Tuple containing the source text and parsed abstract syntax tree.
    :note: none
    """
    path = PROJECT_DIR / filename

    if not path.exists():
        raise AssertionError(f"{filename} was not found.")

    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise AssertionError(
            f"{filename} has a syntax error on line "
            f"{exc.lineno}: {exc.msg}"
        ) from exc

    return source, tree


def get_function_nodes(tree):
    """
    Collect the top-level function definitions from a parsed Python module.

    :param: tree - Parsed Python abstract syntax tree.
    :raises: none
    :return: Dictionary mapping function names to their AST nodes.
    :note: Only top-level function definitions are collected.
    """
    functions = {}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = node

    return functions


def import_module_safely(module_name):
    """
    Import a project module while capturing unexpected output during import.

    :param: module_name - Importable project-module name without the .py suffix.
    :raises: AssertionError if the module cannot be imported.
    :return: Tuple containing the imported module and captured standard output.
    :note: none
    """
    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))

    if module_name in sys.modules:
        del sys.modules[module_name]

    captured = io.StringIO()

    try:
        with redirect_stdout(captured):
            module = importlib.import_module(module_name)
    except Exception as exc:
        raise AssertionError(
            f"{module_name}.py could not be imported: "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    return module, captured.getvalue()


def has_standard_run_guard(tree):
    """
    Check whether main.py contains the standard course run guard.

    :param: tree - Parsed abstract syntax tree for main.py.
    :raises: none
    :return: True if the standard run guard calls main(); otherwise False.
    :note: The expected form is if __name__ == "__main__": main().
    """
    result = False

    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test

            correct_test = (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            )

            if correct_test and len(node.body) == 1:
                statement = node.body[0]

                correct_call = (
                    isinstance(statement, ast.Expr)
                    and isinstance(statement.value, ast.Call)
                    and isinstance(statement.value.func, ast.Name)
                    and statement.value.func.id == "main"
                    and not statement.value.args
                    and not statement.value.keywords
                )

                if correct_call:
                    result = True

    return result


def count_returns(function_node):
    """
    Count return statements contained in one top-level function.

    :param: function_node - AST node representing a function definition.
    :raises: none
    :return: Integer number of return statements found.
    :note: Used to verify the course single-return rule.
    """
    count = 0

    for node in ast.walk(function_node):
        if isinstance(node, ast.Return):
            count += 1

    return count


def contains_break_continue_or_while_true(function_node):
    """
    Detect prohibited course control-flow structures in a function.

    :param: function_node - AST node representing a function definition.
    :raises: none
    :return: True if break, continue, or while True appears; otherwise False.
    :note: none
    """
    result = False

    for node in ast.walk(function_node):
        if isinstance(node, (ast.Break, ast.Continue)):
            result = True

        if isinstance(node, ast.While):
            if (
                isinstance(node.test, ast.Constant)
                and node.test.value is True
            ):
                result = True

    return result


def called_simple_names(tree_or_node):
    """
    Collect simple function-call names from an AST node.

    :param: tree_or_node - AST module or function node to inspect.
    :raises: none
    :return: Set containing directly called simple function names.
    :note: Attribute calls such as module.function() are not included.
    """
    names = set()

    for node in ast.walk(tree_or_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.add(node.func.id)

    return names


def discover_processing_modules(directory):
    """
    Discover student-created processing modules without requiring exact names.

    :param: directory - Project directory to inspect.
    :raises: none
    :return: Sorted list of application-module filenames beyond main.py and data_io.py.
    :note: test.py and student_tests.py are excluded from application modules.
    """
    excluded = {
        "main.py",
        "data_io.py",
        "test.py",
        "student_tests.py",
    }

    modules = []

    for path in Path(directory).glob("*.py"):
        if path.name not in excluded:
            modules.append(path.name)

    modules.sort()

    return modules


def run_project_copy(input_text=None, remove_input=False):
    """
    Run main.py in an isolated temporary copy of the project.

    :param: input_text - Optional replacement transactions.txt contents;
            remove_input - whether to delete transactions.txt before execution.
    :raises: AssertionError if the temporary project cannot be prepared.
    :return: Tuple containing the completed subprocess and generated report text.
    :note: The original student project is not modified by the run.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for path in PROJECT_DIR.iterdir():
            if path.name == "__pycache__":
                continue

            if path.is_file():
                shutil.copy2(path, temp_path / path.name)

        input_path = temp_path / "transactions.txt"
        report_path = temp_path / "transaction_report.txt"

        # Never allow a previously generated report to affect this test run.
        if report_path.exists():
            report_path.unlink()

        if input_text is not None:
            input_path.write_text(
                input_text,
                encoding="utf-8",
            )

        if remove_input and input_path.exists():
            input_path.unlink()

        completed = subprocess.run(
            [sys.executable, "main.py"],
            cwd=temp_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        report_text = ""

        if report_path.exists():
            report_text = report_path.read_text(
                encoding="utf-8"
            )

    return completed, report_text


def test_01_required_project_structure():
    """
    Verify required files and the expected small application-module count.

    :param: none
    :raises: AssertionError if required files are missing or the application architecture is outside the required size.
    :return: None
    :note: Students choose the names of one or two processing modules.
    """
    for filename in REQUIRED_FILES:
        assert (PROJECT_DIR / filename).exists(), (
            f"Missing required file: {filename}"
        )

    processing_modules = discover_processing_modules(
        PROJECT_DIR
    )

    assert 1 <= len(processing_modules) <= 2, (
        "Create one or two processing/analysis modules in addition "
        "to main.py and data_io.py."
    )


def test_02_data_io_functions_and_signatures():
    """
    Verify the required data_io.py functions and exact interfaces.

    :param: none
    :raises: AssertionError if a required file-I/O function or signature is incorrect.
    :return: None
    :note: Internal processing-function names are intentionally not prescribed.
    """
    _, tree = load_tree("data_io.py")
    nodes = get_function_nodes(tree)

    for name, expected_parameters in DATA_IO_FUNCTIONS.items():
        assert name in nodes, (
            f"Missing required function: data_io.{name}()"
        )

        actual_parameters = [
            argument.arg
            for argument in nodes[name].args.args
        ]

        assert actual_parameters == expected_parameters, (
            f"data_io.{name}() must use parameters "
            f"({', '.join(expected_parameters)})."
        )


def test_03_run_guard_and_safe_imports():
    """
    Verify the main.py run guard and safe importing of application modules.

    :param: none
    :raises: AssertionError if the run guard is incorrect or importing an application module produces output.
    :return: None
    :note: Processing modules are discovered dynamically.
    """
    _, main_tree = load_tree("main.py")

    assert has_standard_run_guard(main_tree), (
        'Expected the standard run guard in main.py:\n'
        'if __name__ == "__main__":\n'
        '    main()'
    )

    module_names = [
        "data_io",
        "main",
    ]

    for filename in discover_processing_modules(
        PROJECT_DIR
    ):
        module_names.append(
            Path(filename).stem
        )

    for module_name in module_names:
        _, output = import_module_safely(module_name)

        assert normalize_output(output) == "", (
            f"Importing {module_name}.py produced output."
        )


def test_04_read_transactions_alternate_data():
    """
    Verify parsing of alternate transaction data and required field types.

    :param: none
    :raises: AssertionError if read_transactions() parses values or types incorrectly.
    :return: None
    :note: Alternate data prevents a solution that hardcodes the supplied file.
    """
    data_io, _ = import_module_safely("data_io")

    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "alternate.txt"

        path.write_text(
            "2001,Food,10.50\n"
            "2002,Utilities,22.25\n"
            "2003,Travel,30.00\n",
            encoding="utf-8",
        )

        transactions = data_io.read_transactions(
            path
        )

    expected = [
        (2001, "Food", 10.50),
        (2002, "Utilities", 22.25),
        (2003, "Travel", 30.00),
    ]

    assert transactions == expected, (
        "read_transactions() did not parse alternate data correctly."
    )

    for transaction in transactions:
        assert isinstance(transaction, tuple)
        assert isinstance(transaction[0], int)
        assert isinstance(transaction[1], str)
        assert isinstance(transaction[2], float)


def test_05_write_report_alternate_results():
    """
    Verify report writing independently using alternate supplied results.

    :param: none
    :raises: AssertionError if write_report() creates incorrect report contents or returns a value.
    :return: None
    :note: Analysis calculations are supplied directly so this test isolates file output.
    """
    data_io, _ = import_module_safely("data_io")

    transactions = [
        (2001, "Food", 10.00),
        (2002, "Utilities", 20.00),
        (2003, "Food", 30.00),
        (2004, "Entertainment", 50.00),
    ]

    category_totals = {
        "Food": 40.00,
        "Utilities": 20.00,
        "Entertainment": 50.00,
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "report.txt"

        result = data_io.write_report(
            path,
            transactions,
            110.00,
            27.50,
            (2004, "Entertainment", 50.00),
            category_totals,
            ("Entertainment", 50.00),
            "Low",
        )

        contents = path.read_text(
            encoding="utf-8"
        )

    expected = """Transaction Analysis Report

Transactions Processed: 4
Total Spending: $110.00
Average Transaction: $27.50
Largest Transaction: 2004 - Entertainment - $50.00

Category Totals
Food: $40.00
Utilities: $20.00
Entertainment: $50.00

Highest-Spending Category: Entertainment - $50.00
Overall Spending Classification: Low"""

    assert normalize_output(contents) == normalize_output(expected), (
        "write_report() did not produce the required report."
    )

    assert result is None, (
        "write_report() should write the report rather than return data."
    )


def test_06_complete_program_supplied_data():
    """
    Verify complete application behavior with the supplied transaction file.

    :param: none
    :raises: AssertionError if the program fails or produces incorrect console/report output.
    :return: None
    :note: This is an end-to-end acceptance test.
    """
    completed, report = run_project_copy()

    assert completed.returncode == 0, (
        "main.py did not complete normally.\n"
        f"{completed.stderr}"
    )

    assert normalize_output(completed.stdout) == (
        "Report written to transaction_report.txt."
    ), (
        "main.py should display exactly:\n"
        "Report written to transaction_report.txt."
    )

    expected = """Transaction Analysis Report

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
Overall Spending Classification: Moderate"""

    assert normalize_output(report) == normalize_output(expected), (
        "transaction_report.txt does not match the required report."
    )


def test_07_complete_program_alternate_data():
    """
    Verify the complete architecture with alternate transaction data.

    :param: none
    :raises: AssertionError if the program hardcodes results or integrates its components incorrectly.
    :return: None
    :note: Exercises the full read-process-write sequence with different data.
    """
    alternate = (
        "2001,Food,10.00\n"
        "2002,Utilities,20.00\n"
        "2003,Food,30.00\n"
        "2004,Entertainment,50.00\n"
    )

    completed, report = run_project_copy(
        input_text=alternate
    )

    assert completed.returncode == 0, (
        "main.py failed with alternate valid data.\n"
        f"{completed.stderr}"
    )

    expected_lines = [
        "Transactions Processed: 4",
        "Total Spending: $110.00",
        "Average Transaction: $27.50",
        "Largest Transaction: 2004 - Entertainment - $50.00",
        "Food: $40.00",
        "Utilities: $20.00",
        "Entertainment: $50.00",
        "Highest-Spending Category: Entertainment - $50.00",
        "Overall Spending Classification: Low",
    ]

    for line in expected_lines:
        assert line in report, (
            f"Alternate-data report is missing: {line}"
        )


def test_08_missing_input_file():
    """
    Verify the required application-level missing-file behavior.

    :param: none
    :raises: AssertionError if the missing input file is not handled as required.
    :return: None
    :note: No report should be created when the source file is unavailable.
    """
    completed, report = run_project_copy(
        remove_input=True
    )

    assert completed.returncode == 0, (
        "main.py should handle a missing input file without crashing."
    )

    assert normalize_output(completed.stdout) == (
        "Error: transactions.txt was not found."
    ), (
        "Missing-file message must be:\n"
        "Error: transactions.txt was not found."
    )

    assert report == "", (
        "The program should not create transaction_report.txt "
        "when transactions.txt is missing."
    )


def test_09_architecture_separates_file_io():
    """
    Verify that file I/O stays in data_io.py rather than processing modules.

    :param: none
    :raises: AssertionError if processing modules or main.py directly open files, or if processing modules print output.
    :return: None
    :note: Students remain free to choose processing-module and function names.
    """
    _, data_tree = load_tree("data_io.py")
    data_calls = called_simple_names(data_tree)

    assert "open" in data_calls, (
        "data_io.py should own the application's file opening."
    )

    _, main_tree = load_tree("main.py")
    main_calls = called_simple_names(main_tree)

    assert "open" not in main_calls, (
        "main.py should coordinate file I/O through data_io.py, "
        "not open files directly."
    )

    for filename in discover_processing_modules(
        PROJECT_DIR
    ):
        _, tree = load_tree(filename)
        calls = called_simple_names(tree)

        assert "open" not in calls, (
            f"{filename} should not perform file I/O."
        )

        assert "print" not in calls, (
            f"{filename} should return results rather than print output."
        )


def test_10_course_function_standards():
    """
    Verify single-return and loop-control standards across application functions.

    :param: none
    :raises: AssertionError if a function contains multiple returns, break, continue, or while True.
    :return: None
    :note: Checks all application modules while preserving freedom over processing-function names.
    """
    filenames = [
        "main.py",
        "data_io.py",
    ]

    filenames.extend(
        discover_processing_modules(PROJECT_DIR)
    )

    for filename in filenames:
        _, tree = load_tree(filename)
        functions = get_function_nodes(tree)

        for name, node in functions.items():
            count = count_returns(node)

            assert count <= 1, (
                f"{filename}:{name}() contains "
                f"{count} return statements."
            )

            assert not contains_break_continue_or_while_true(node), (
                f"{filename}:{name}() uses prohibited loop control."
            )


TESTS = [
    ("Required project structure",
     test_01_required_project_structure),
    ("Required data_io.py interfaces",
     test_02_data_io_functions_and_signatures),
    ("Run guard and safe imports",
     test_03_run_guard_and_safe_imports),
    ("read_transactions() with alternate data",
     test_04_read_transactions_alternate_data),
    ("write_report() with alternate results",
     test_05_write_report_alternate_results),
    ("Complete program with supplied data",
     test_06_complete_program_supplied_data),
    ("Complete program with alternate data",
     test_07_complete_program_alternate_data),
    ("Missing input-file handling",
     test_08_missing_input_file),
    ("Architecture separates file I/O",
     test_09_architecture_separates_file_io),
    ("Course function standards",
     test_10_course_function_standards),
]


def main():
    """
    Run all instructor-supplied Assignment 9 acceptance tests.

    :param: none
    :raises: none
    :return: Integer status code 0 after the test run completes.
    :note: Student-written tests are separate from this supplied suite.
    """
    print("Assignment 9 Supplied Tests")
    print()

    passed = 0

    for number, (name, test_function) in enumerate(
        TESTS,
        start=1,
    ):
        try:
            test_function()
            status = "PASS"
            passed += 1
            detail = ""
        except AssertionError as exc:
            status = "FAIL"
            detail = str(exc)
        except Exception as exc:
            status = "FAIL"
            detail = (
                f"{type(exc).__name__}: {exc}"
            )

        print(
            f"{number:02d}. "
            f"{name:<46} "
            f"{status}"
        )

        if detail:
            for line in detail.splitlines():
                print(f"    {line}")

    print()
    print(f"{passed}/{len(TESTS)} tests passed")

    if passed == len(TESTS):
        print("All supplied acceptance tests passed.")
    else:
        print(
            "Review the failed tests and continue developing."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
