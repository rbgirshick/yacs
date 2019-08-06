import io
import sys

# Flag for py2 and py3 compatibility to use when separate code paths are necessary
# When _PY2 is False, we assume Python 3 is in use
_PY2 = sys.version_info.major == 2

# Filename extensions for loading configs from files
_YAML_EXTS = {"", ".yaml", ".yml"}
_PY_EXTS = {".py"}

# py2 and py3 compatibility for checking file object type
# We simply use this to infer py2 vs py3
if _PY2:
    _FILE_TYPES = (file, io.IOBase)
else:
    _FILE_TYPES = (io.IOBase,)

# CfgNodes can only contain a limited set of valid types
_VALID_TYPES = {tuple, list, str, int, float, bool}
# py2 allow for str and unicode
if _PY2:
    _VALID_TYPES = _VALID_TYPES.union({unicode})  # noqa: F821
