from random import randint


def randomize_hash_id(name: str) -> str:
    """
    Generate a random hash for div id for a component.

    Parameters
    ----------
    name : str
        The name of the component. E.g. 'BarChart'.

    Returns
    -------
    str
        The generated hash ID.
    """
    random_hex_id = hex(randint(10**8, 10**9))[2:]
    hashed_div_id = f"{name}-{random_hex_id}"
    return hashed_div_id
