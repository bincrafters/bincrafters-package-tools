def generate_win_matrices(archs, versions):
    gcc_matrix = {}
    gcc_matrix["config"] = []
    for v in versions:
        if v == "2017":
            gcc_matrix["config"].extend(__generate_vs2017_matrix(archs))
        if v == "2019":
            gcc_matrix["config"].extend(__generate_vs2019_matrix(archs))
    return gcc_matrix["config"]


def __generate_vs2017_matrix(archs):
    valid_vs2017_archs = set(["x86", "x86_64", "armv7", "armv7hf", "armv8"])
    
    vs2017_matrix = {}
    vs2017_matrix["config"] = []
    
    vs2017_archs = [x for x in archs if x in valid_vs2017_archs]

    for arch in vs2017_archs:
        vs2017_matrix["config"].append(
            {"name": "Windows VS 2017 "+ arch, "compiler": "VISUAL", 
            "version": "15", "os": "vs2017-win2016", "arch": arch},
        )
    return vs2017_matrix["config"]

def __generate_vs2019_matrix(archs):
    valid_vs2019_archs = set(["x86", "x86_64", "armv7", "armv7hf", "armv8"])
    
    vs2019_matrix = {}
    vs2019_matrix["config"] = []
    
    vs2019_archs = [x for x in archs if x in valid_vs2019_archs]

    for arch in vs2019_archs:
        vs2019_matrix["config"].append(
            {"name": "Windows VS 2019 " + arch, "compiler": "VISUAL", 
            "version": "16", "os": "windows-2019", "arch": arch},
        )
    return vs2019_matrix["config"]