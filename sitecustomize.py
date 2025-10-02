import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("PYTHONFAULTHANDLER", "1")
os.environ.setdefault("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
