def generate_gcc_matrices(archs, versions):
    gcc_matrix = {}
    gcc_matrix["config"] = []
    for v in versions:
        if v == "4.9":
            gcc_matrix["config"].extend(__generate_gcc4_9_matrix(archs))
        if v == "5":
            gcc_matrix["config"].extend(__generate_gcc5_matrix(archs))
        if v == "6":
            gcc_matrix["config"].extend(__generate_gcc6_matrix(archs))
        if v == "7":
            gcc_matrix["config"].extend(__generate_gcc7_matrix(archs))
        if v == "8":
            gcc_matrix["config"].extend(__generate_gcc8_matrix(archs))
        if v == "9":
            gcc_matrix["config"].extend(__generate_gcc9_matrix(archs))
        if v == "10":
            gcc_matrix["config"].extend(__generate_gcc10_matrix(archs))
    return gcc_matrix["config"]

def __generate_gcc_matrix(archs, version, valid_gcc_archs):
    gcc_matrix = []
    gcc_archs = [x for x in archs if x in valid_gcc_archs]
    for arch in gcc_archs:
        gcc_matrix.append(
            {"name": "GCC "+ version + " " + arch, "compiler": "GCC",
                "version": version, "os": "ubuntu-18.04", "arch": arch}
        )
    return gcc_matrix

def __generate_gcc4_9_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "x86", "x86_64"])
    matrix = __generate_gcc_matrix(archs,"4.9",valid_gcc_archs)
    return matrix

def __generate_gcc5_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = __generate_gcc_matrix(archs,"5",valid_gcc_archs)
    return matrix

def __generate_gcc6_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = __generate_gcc_matrix(archs,"6",valid_gcc_archs)
    return matrix

def __generate_gcc7_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = __generate_gcc_matrix(archs,"7",valid_gcc_archs)
    return matrix

def __generate_gcc8_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = __generate_gcc_matrix(archs,"8",valid_gcc_archs)
    return matrix

def __generate_gcc9_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "armv8", "x86", "x86_64"])
    matrix = __generate_gcc_matrix(archs,"9",valid_gcc_archs)
    return matrix

def __generate_gcc10_matrix(archs):
    valid_gcc_archs = set(["armv7", "armv7hf", "x86_64"])
    matrix = __generate_gcc_matrix(archs,"10",valid_gcc_archs)
    return matrix