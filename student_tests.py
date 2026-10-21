#!/usr/bin/env python3

"""
Assignment 9 — Student-Designed Tests

Complete the four required test functions in this file.

These tests are separate from the instructor-supplied test.py. The supplied
tests verify major acceptance requirements. Your tests should verify meaningful
behavior in the architecture and functions that you designed.

You may add imports, local test data, and small test-support helpers if needed.

Requirements:

- Complete all four required test functions.
- Each test must be independent of the other tests.
- Each test must construct the state or data it needs.
- Each test must use one or more assert statements.
- Each test must have a known expected result.
- Do not copy tests from the instructor-supplied test.py.
- A test may contain multiple assertions when they verify one coherent
  requirement, boundary, state, or invariant.
- Complete each docstring note so it explains what the test verifies and why
  the test matters.
- Follow normal course programming and documentation standards.

The four required categories are:

1. a normal-case test;
2. a boundary or edge-state test;
3. a state or invariant test; and
4. a student-selected risk test.

The goal is not merely to make four tests pass. The goal is to demonstrate that
you can choose meaningful states and expected results based on the requirements
and architecture of your own program.
"""


# Add the imports required to test your student-designed processing module(s)
# below. For example:
#
# import analysis
#
# Use the actual module name(s) from your design.


def test_normal_case():
    """
    Test one normal case for a student-designed program capability.

    :param: none
    :raises: AssertionError if the tested behavior is incorrect.
    :return: None
    :note: Replace this note with the requirement this test verifies and why
           the selected data represents a meaningful normal case.
    """

    # Arrange:
    # Create ordinary valid data for one capability you designed.

    # Act:
    # Call the function being tested.

    # Assert:
    # Compare the actual result with a known expected result.

    raise AssertionError(
        "Complete test_normal_case()."
    )


def test_boundary_or_edge_case():
    """
    Test one meaningful boundary or edge state.

    :param: none
    :raises: AssertionError if the tested behavior is incorrect.
    :return: None
    :note: Replace this note with the boundary or edge state being tested and
           explain why that state is important.
    """

    # Arrange:
    # Choose data at or around a meaningful boundary, or another unusual but
    # valid state.

    # Act:
    # Call the function being tested.

    # Assert:
    # Verify the required behavior at that boundary or edge state.

    raise AssertionError(
        "Complete test_boundary_or_edge_case()."
    )


def test_state_or_invariant():
    """
    Test a meaningful state transition or invariant in the program.

    :param: none
    :raises: AssertionError if the tested behavior or invariant is incorrect.
    :return: None
    :note: Replace this note with what should change and/or what must remain
           true after the operation being tested.
    """

    # Arrange:
    # Create the starting state and preserve any values needed for comparison.

    # Act:
    # Perform the operation or sequence being tested.

    # Assert:
    # Verify the expected result and/or an invariant that must remain true.

    raise AssertionError(
        "Complete test_state_or_invariant()."
    )


def test_student_selected_risk():
    """
    Test one additional behavior selected because it presents a meaningful risk.

    :param: none
    :raises: AssertionError if the tested behavior is incorrect.
    :return: None
    :note: Replace this note with the risk you identified, why you selected it,
           and what requirement or assumption the test verifies.
    """

    # Arrange:
    # Construct data or state that exercises the risk you identified.

    # Act:
    # Perform the relevant operation.

    # Assert:
    # Verify the expected behavior.

    raise AssertionError(
        "Complete test_student_selected_risk()."
    )


TESTS = [
    ("Normal case", test_normal_case),
    ("Boundary or edge state", test_boundary_or_edge_case),
    ("State or invariant", test_state_or_invariant),
    ("Student-selected risk", test_student_selected_risk),
]


def main():
    """
    Run all required student-designed Assignment 9 tests.

    :param: none
    :raises: none
    :return: Integer status code 0 after the test run completes.
    :note: A failing test is reported but does not stop the remaining tests.
    """
    print("Assignment 9 Student Tests")
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
            f"{name:<28} "
            f"{status}"
        )

        if detail:
            for line in detail.splitlines():
                print(f"    {line}")

    print()
    print(f"{passed}/{len(TESTS)} student tests passed")

    if passed == len(TESTS):
        print("All student-designed tests passed.")
    else:
        print(
            "Complete or correct the failed student tests."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
