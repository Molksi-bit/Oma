import re

def load_pyat(path):
    structure_elements = r"(\w+)\s*=\s*at\.(\w+)\("
    structure_section = r"(\w+) ?s*=\s* at\.ring(\w+)\("
    structure_varables = r"(\w+)\s*=\s*(\w+)\("
    with open(path, "r") as file:
        lines = file.read()
    matches = re.findall(structure_elements, lines)
    sections = {}
    metadata = {}
    elements = {}
    for match in matches:
        print(match)

    
    


    return sections, metadata, elements

<<<<<<< HEAD
#load_pyat("testing/test_lattices/full_types/full_type.py")
=======
#load_pyat("testing/test_lattices/full_types/full_type.py")
>>>>>>> e8b1c1e7eda2b9327c3eaadf2f647164046ec816
