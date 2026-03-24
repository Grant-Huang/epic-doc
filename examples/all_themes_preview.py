"""Generate preview documents for all 10 built-in themes.

Run from the project root:
    python examples/all_themes_preview.py

Output: previews/ directory with one .docx per theme.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from epic_doc import list_themes
from epic_doc.cli import _generate_preview

os.makedirs("previews", exist_ok=True)

for theme in list_themes():
    out = f"previews/preview_{theme.name}.docx"
    print(f"  Generating: {theme.display_name} ...", end=" ", flush=True)
    _generate_preview(theme.name, out)
    print(f"→ {out}")

print(f"\n✓ {len(list_themes())} theme previews saved in previews/")
