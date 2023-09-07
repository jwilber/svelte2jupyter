import pytest

from svelte2jupyter import randomize_hash_id


def test_randomize_hash_id_format():
    """
    Test if the randomize_hash_id function provides the expected formatted output.
    """
    name = "BarChart"
    result = randomize_hash_id(name)

    # Check if the result has the correct prefix and the correct format with a hyphen.
    assert result.startswith(name)
    assert len(result.split("-")) == 2
    assert all(character in "0123456789abcdef" for character in result.split("-")[1])


def test_randomize_hash_id_uniqueness():
    """
    Test if the randomize_hash_id function provides unique values on multiple invocations.
    """
    name = "BarChart"

    # Generate a set of IDs.
    ids = {randomize_hash_id(name) for _ in range(1000)}

    # Check if the count of unique IDs matches the expected count.
    assert len(ids) == 1000


# If you want to run the tests from the command line, use:
# pytest your_test_file_name.py  # Replace 'your_test_file_name' with the actual name of this test file.
