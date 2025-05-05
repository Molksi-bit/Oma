import math
import re
def resolve_param(val, parameters, _rec=0, _max_rec=10):
    """
    Finds the value of 'val' recursiv, inclusive simple expressions.
    """
    val = val.strip()
    try:
        return float(val)
    except ValueError:
        pass
    if val in parameters and _rec < _max_rec:
        return resolve_param(parameters[val], parameters, _rec+1, _max_rec)
    expr = val
    pattern = r'\b[a-zA-Z_]\w*\b'
    for var in re.findall(pattern, expr):
        if var in parameters:
            repl = str(resolve_param(parameters[var], parameters, _rec+1, _max_rec))
            expr = re.sub(rf'\b{var}\b', repl, expr)
    try:
        return float(eval(expr))
    except Exception:
        return expr

def load_opa(opa_path):
    """This function reads an opa file and creates dictionary of the corresponding lattice and parameters.
    Returns: data dictionary with, used elements, lattices, parameters and the title of the file"""
    with open(opa_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    # Zeilen zusammenführen wie im alten Code (mehrzeilige Definitionen auf eine Zeile bringen)
    merged, temp_line = [], ""
    for line in lines:
        if line.endswith(","):
            temp_line += " " + line
        else:
            merged.append(temp_line + " " + line if temp_line else line)
            temp_line = ""

    # Abschnitte finden
    try:
        start_vars = merged.index("{----- variables ---------------------------------------------------}") + 1
        start_elems = merged.index("{----- table of elements ---------------------------------------------}")
        start_lattices = merged.index("{----- table of segments ---------------------------------------------}")
    except ValueError as e:
        print("OPA-File-Struktur unerwartet:", e)
        return None

    # Variablen / Parameter (grob)
    parameters = {}
    energy = merged[1].strip(";").split("=")[-1].strip()
    title = merged[0].strip("{}").rsplit("\\",1)[-1].split(".",1)[0]
    parameters["energy_GeV"] = energy
    for line in merged[start_vars:start_elems]:
        if "=" in line:
            key, val = line.replace(";", "").split("=")
            parameters[key.strip()] = val.strip()
    # Elemente
    elements = {}
    magnet_map = {
        "drift": "drift",
        "quadrupole": "quadrupole",
        "sextupole": "sextupole",
        "bending": "dipole",
        "combined": "dipole",
        "opticsmarker" : "marker"
    }

    for line in merged[start_elems+1:start_lattices]:
        if ":" not in line:
            continue
        parts = [part.strip().rstrip(";") for part in line.split(":", 1)]
        name, params = parts[0], parts[1]
        params_list = [p.strip() for p in params.split(",") if p.strip()]
        args = {}
        key_map = {
        "l": "length",
        "k": "k1",
        "t": "angle",
        "t1": "EntranceAngle",
        "t2": "ExitAngle"
        }
        for p in params_list[1:]:
            if "=" in p:
                key, val = p.split("=")
                key=key_map.get(key.strip(),key.strip())
                val=val.strip()
                val_resolved =resolve_param(val,parameters)
                args[key] = val_resolved
        elem_type = params_list[0]
        
        if elem_type in ["bending", "combined"]:
            args["angle"] = math.radians(args.get("angle", 0.0))
        typ = magnet_map.get(elem_type.lower(), elem_type.lower())
        element_dict = {"type": typ}
        element_dict.update(args)
        elements[name] = element_dict

    # Lattices/Abschnitte
    lattices = {}
    for line in merged[start_lattices+1:-1]:
        if ":" not in line:
            continue
        name, elems = map(str.strip, line.split(":", 1))
        # Trenne Kommas, entferne ;, entferne Leerzeichen
        section_elements = [e.strip() for e in elems.replace(";", "").split(",") if e.strip()]
        lattices[name] = section_elements

    # Zusammenbauen wie dein JSON
    data_dict = {
        "elements": elements,
        "lattices": lattices,
        "parameters": parameters,
        "title": title
    }
    
    return data_dict
