# file for testfunctions 

import traceback
import time

def test_lattices_with_functions(lattices, functions, section_name="RING"):
    """
    Tests multiple lattice configurations against a set of analysis functions.
    
    Args:
        lattices (dict): Dictionary of {name: lattice_data} where each value should be a dict containing 'elements'.
        functions (list): List of tuples like (func_name, callable_function).
        section_name (str): The section to use in each lattice for testing.

    Returns:
        dict: Results including runtime and errors for each lattice-function pair.
    """
    results = {}

    for lat_name, lattice_data in lattices.items():
        results[lat_name] = {}
        section = lattice_data.get("elements", {}).get(section_name)
        if not section:
            results[lat_name]["error"] = f"Section '{section_name}' not found in lattice."
            continue

        for func_name, func in functions:
            result = {"runtime": None, "error": None}
            try:
                start = time.perf_counter()
                _ = func(section)  # run function on lattice section
                end = time.perf_counter()
                result["runtime"] = round(end - start, 6)
            except Exception as e:
                result["error"] = traceback.format_exc(limit=1)
            results[lat_name][func_name] = result

    return results
