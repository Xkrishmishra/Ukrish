import glob
import os

def __list_all_modules():
    work_dir = os.path.dirname(__file__)
    mod_paths = glob.glob(work_dir + "/**/*.py")
    all_modules = [
        ((f.replace(work_dir, "")).replace("/", "."))[:-3]
        for f in mod_paths
        if os.path.isfile(f) and f.endswith(".py") and not f.endswith("__(link unavailable)")
    ]
    return all_modules

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
