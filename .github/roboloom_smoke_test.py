"""Checks an installed pysurvive wheel without tracking hardware.

Run by the roboloom-wheels workflow (cibuildwheel's test step) and usable by hand:
`python .github/roboloom_smoke_test.py`. It imports the package, checks that the
native library and the device plugins (driver_vive, ...) are in the wheel and load, and
opens and drops a SimpleContext in a child process (no device is expected to be found).
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pysurvive

package = Path(pysurvive.__file__).parent
plugins = sorted(p.name for p in (package / "libsurvive" / "plugins").glob("*.so"))
print("package:", package)
print("plugins:", ", ".join(plugins))
assert any(name.startswith("driver_vive") for name in plugins), "driver_vive missing"
assert any(name.startswith("poser_") for name in plugins), "no poser plugin"
assert importlib.util.find_spec("gooey") is None or "--gui" in sys.argv, (
    "gooey must not be installed by default"
)

libs = sorted(p.name for p in (package.parent / "pysurvive.libs").glob("*.so*"))
print("bundled:", ", ".join(libs))
assert any(name.startswith("libusb") for name in libs), "libusb is not bundled"
assert not any(name.startswith("libudev") for name in libs), "libudev must not be bundled"

pysurvive.init_plugins()  # dlopen()s every plugin: fails on a missing shared library
items = list(pysurvive.config_items())
print("config items:", len(items))
assert items, "no configuration items after loading the plugins"

child = (
    "import os, pysurvive\n"
    "ctx = pysurvive.SimpleContext(['smoke'])\n"
    "print('objects:', [o.Name() for o in ctx.Objects()], 'running:', ctx.Running(), flush=True)\n"
    "os._exit(0)\n"
)
result = subprocess.run(
    [sys.executable, "-c", child], timeout=60, capture_output=True, text=True
)
print(result.stdout + result.stderr)
assert result.returncode == 0, f"SimpleContext failed ({result.returncode})"
print("ok", os.environ.get("PYSURVIVE_VERSION", ""))
