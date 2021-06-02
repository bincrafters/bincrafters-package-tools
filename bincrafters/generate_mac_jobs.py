def generate_mac_matrices(archs, versions):
    clang_matrix = {}
    clang_matrix["config"] = []
    for v in versions:
        if v == "10":
            clang_matrix["config"].extend(__generate_clang10_matrix(archs))
        if v == "11":
            clang_matrix["config"].extend(__generate_clang11_matrix(archs))
        if v == "12":
            clang_matrix["config"].extend(__generate_clang12_matrix(archs))

    return clang_matrix["config"]

def __generate_clang10_matrix(archs):
    valid_clang_archs = set(["x86", "x86_64", "armv7", "armv7hf", "armv8"])
    matrix = __generate_clang_matrix(archs,"10.0",valid_clang_archs)
    return matrix

def __generate_clang11_matrix(archs):
    valid_clang_archs = set(["x86", "x86_64", "armv7", "armv7hf", "armv8"])
    matrix = __generate_clang_matrix(archs,"11.0",valid_clang_archs)
    return matrix

def __generate_clang12_matrix(archs):
    valid_clang_archs = set(["x86", "x86_64", "armv7", "armv7hf", "armv8"])
    matrix = __generate_clang_matrix(archs,"12.0",valid_clang_archs)
    return matrix

def __generate_clang_matrix(archs, version, valid_clang_archs):
    clang_matrix = []
    clang_archs = [x for x in archs if x in valid_clang_archs]
    for arch in clang_archs:
        {"name": "macOS Apple-Clang "+ version+ " " + arch, "compiler": "APPLE_CLANG", 
        "version": version, "os": "macOS-10.15", "arch": arch}
    return clang_matrix