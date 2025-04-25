import math

def load_opa(opa_path):
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
        elem_type = params_list[0]
        key_map = {
        "l": "length",
        "k": "k1",
        "t": "angle",
        "t1": "EntranceAngle",
        "t2": "ExitAngle"
        }
        args = {
            key_map.get(p.split("=")[0].strip(), p.split("=")[0].strip()): float(p.split("=")[1])
            for p in params_list[1:] if "=" in p
        }
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
    print(data_dict["elements"])
    return data_dict
