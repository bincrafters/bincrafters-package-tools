def generate_clang_matrices(archs, versions):
    clang_matrix = {}
    clang_matrix["config"] = []
    for v in versions:
        if v == "3.9":
            clang_matrix["config"].extend(__generate_clang3_9_matrix(archs))
        if v == "4":
            clang_matrix["config"].extend(__generate_clang4_matrix(archs))
        if v == "5":
            clang_matrix["config"].extend(__generate_clang5_matrix(archs))
        if v == "6":
            clang_matrix["config"].extend(__generate_clang6_matrix(archs))
        if v == "7":
            clang_matrix["config"].extend(__generate_clang7_matrix(archs))
        if v == "8":
            clang_matrix["config"].extend(__generate_clang8_matrix(archs))
        if v == "9":
            clang_matrix["config"].extend(__generate_clang9_matrix(archs))
        if v == "10":
            clang_matrix["config"].extend(__generate_clang10_matrix(archs))
        if v == "11":
            clang_matrix["config"].extend(__generate_clang11_matrix(archs))

    return clang_matrix["config"]

def __generate_clang3_9_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"3.9",valid_clang_archs)
    return matrix

def __generate_clang4_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"4.0",valid_clang_archs)
    return matrix

def __generate_clang5_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"5.0",valid_clang_archs)
    return matrix

def __generate_clang6_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"6.0",valid_clang_archs)
    return matrix

def __generate_clang7_matrix(archs):
    valid_clang_archs = set(["x86", "x86_64"])
    matrix = __generate_clang_matrix(archs,"7.0",valid_clang_archs)
    return matrix

def __generate_clang8_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"8",valid_clang_archs)
    return matrix

def __generate_clang9_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"9",valid_clang_archs)
    return matrix

def __generate_clang10_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"10",valid_clang_archs)
    return matrix

def __generate_clang11_matrix(archs):
    valid_clang_archs = set(["x86_64"])
    matrix = __generate_clang_matrix(archs,"11",valid_clang_archs)
    return matrix

def __generate_clang_matrix(archs, version, valid_clang_archs):
    clang_matrix = []
    clang_archs = [x for x in archs if x in valid_clang_archs]
    for arch in clang_archs:
        clang_matrix.append(
            {"name": "CLANG "+ version + " " + arch, "compiler": "CLANG", "version": version, "os": "ubuntu-18.04", "arch": arch}
        )
    return clang_matrix