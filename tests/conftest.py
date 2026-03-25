import sys
from pathlib import Path

# Ensure `import epic_doc` works when running tests from repo root
# without installing the package.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

