import sys
import traceback
import importlib

sys.path.insert(0, r"C:\Users\Cliente\OneDrive\Documentos\Roos")

try:
    m = importlib.import_module("api.app.main")
    print("MODULE FILE:", getattr(m, "__file__", None))
    print("MODULE SPECS:", getattr(m, "__spec__", None))
    print("MODULE NAME:", getattr(m, "__name__", None))
    print("MODULE PACKAGE:", getattr(m, "__package__", None))
    print("MODULE DIR:", [n for n in dir(m) if not n.startswith("_")])
    print("HAS APP:", hasattr(m, "app"))
    print("ALL KEYS:", sorted(list(m.__dict__.keys())))
except Exception:
    traceback.print_exc()
