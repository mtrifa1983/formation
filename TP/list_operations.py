"""
Module for list operations with PEP8 compliance and type annotations.

This module provides functions to perform common operations on lists,
including summing elements and calculating squares.
"""

from typing import List


def sum_list(nums: List[int]) -> int:
    """
    Calculate the sum of all elements in a list.

    Args:
        nums: A list of integers to sum.

    Returns:
        The sum of all elements in the list.

    Examples:
        >>> sum_list([1, 2, 3])
        6
        >>> sum_list([10, 20, 30])
        60
        >>> sum_list([])
        0
    """
    total: int = 0
    for num in nums:
        total += num
    return total


def squares(nums: List[int]) -> List[int]:
    """
    Calculate the square of each element in a list.

    Args:
        nums: A list of integers to square.

    Returns:
        A list containing the square of each element.

    Examples:
        >>> squares([1, 2, 3, 4])
        [1, 4, 9, 16]
        >>> squares([2, 3, 5])
        [4, 9, 25]
        >>> squares([])
        []
    """
    return [num * num for num in nums]


def average(nums: List[int]) -> float:
    """
    Calculate the average of all elements in a list.

    Args:
        nums: A list of integers.

    Returns:
        The average value of the list.

    Raises:
        ValueError: If the list is empty.

    Examples:
        >>> average([1, 2, 3, 4, 5])
        3.0
        >>> average([10, 20])
        15.0
    """
    if not nums:
        raise ValueError("Cannot calculate average of an empty list")
    return sum(nums) / len(nums)


def main() -> None:
    """Run test cases for all functions."""
    print("=" * 50)
    print("TEST RESULTS")
    print("=" * 50)

    # Test sum_list
    print("\nTest 1: sum_list([1, 2, 3])")
    result_1: int = sum_list([1, 2, 3])
    expected_1: int = 6
    print(f"Result: {result_1}")
    print(f"Expected: {expected_1}")
    print(f"Status: {'PASS' if result_1 == expected_1 else 'FAIL'}")

    # Test squares
    print("\nTest 2: squares([1, 2, 3, 4])")
    result_2: List[int] = squares([1, 2, 3, 4])
    expected_2: List[int] = [1, 4, 9, 16]
    print(f"Result: {result_2}")
    print(f"Expected: {expected_2}")
    print(f"Status: {'PASS' if result_2 == expected_2 else 'FAIL'}")

    # Test average
    print("\nTest 3: average([1, 2, 3, 4, 5])")
    result_3: float = average([1, 2, 3, 4, 5])
    expected_3: float = 3.0
    print(f"Result: {result_3}")
    print(f"Expected: {expected_3}")
    print(f"Status: {'PASS' if result_3 == expected_3 else 'FAIL'}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
