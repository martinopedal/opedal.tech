#!/usr/bin/env python3
"""
CV build script — architect variant.

Reads cv/data/architect.yml, renders cv/templates/architect.tex.j2 for both
1-page and multi-page modes, compiles each via latexmk, and copies the resulting
PDFs to public/cv/architect-{1page,multipage}.pdf.

Runs in CI via .github/workflows/cv.yml. Can be run locally if latexmk is on PATH.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

# Repository root (two levels up from this script)
REPO_ROOT = Path(__file__).resolve().parent.parent
CV_ROOT = REPO_ROOT / "cv"
DATA_FILE = CV_ROOT / "data" / "architect.yml"
TEMPLATES_DIR = CV_ROOT / "templates"
BUILD_DIR = CV_ROOT / "architect" / "build"
LATEX_DIR = CV_ROOT / "architect"
PUBLIC_DIR = REPO_ROOT / "public" / "cv"

MODES = ["1page", "multipage"]


def main():
    """Main build orchestration."""
    print("[build.py] Starting CV build for architect variant")

    # 1. Load YAML data
    if not DATA_FILE.exists():
        print(f"[ERROR] Data file not found: {DATA_FILE}", file=sys.stderr)
        sys.exit(1)

    with open(DATA_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    print(f"[build.py] Loaded data from {DATA_FILE}")

    # 2. Set up Jinja2 with custom delimiters (to avoid LaTeX clash)
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        block_start_string="((*",
        block_end_string="*))",
        variable_start_string="(((",
        variable_end_string=")))",
        comment_start_string="((=",
        comment_end_string="=))",
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("architect.tex.j2")
    print(f"[build.py] Loaded template from {TEMPLATES_DIR / 'architect.tex.j2'}")

    # 3. Prepare build directory
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Render and compile each mode
    for mode in MODES:
        print(f"\n[build.py] Rendering mode: {mode}")
        rendered = template.render(mode=mode, **data)

        tex_file = BUILD_DIR / f"architect-{mode}.tex"
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"[build.py] Wrote {tex_file} ({len(rendered)} chars)")

        # Compile with latexmk from the LATEX_DIR so photo.jpg resolves
        print(f"[build.py] Compiling {tex_file.name} with latexmk...")
        try:
            subprocess.run(
                [
                    "latexmk",
                    "-pdf",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-output-directory={BUILD_DIR}",
                    tex_file,
                ],
                cwd=LATEX_DIR,
                check=True,
                capture_output=False,
            )
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] latexmk failed for {mode}", file=sys.stderr)
            sys.exit(1)

        pdf_file = BUILD_DIR / f"architect-{mode}.pdf"
        if not pdf_file.exists():
            print(f"[ERROR] Expected PDF not found: {pdf_file}", file=sys.stderr)
            sys.exit(1)

        # 5. Copy PDF to public/cv/
        PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
        dest = PUBLIC_DIR / f"architect-{mode}.pdf"
        shutil.copy(pdf_file, dest)
        print(f"[build.py] Copied {pdf_file} → {dest}")

    # 6. Clean up build artifacts (keep PDFs, remove .aux, .log, .fls, etc.)
    print(f"\n[build.py] Cleaning build directory {BUILD_DIR}")
    for ext in [".aux", ".fdb_latexmk", ".fls", ".log", ".out", ".synctex.gz"]:
        for artifact in BUILD_DIR.glob(f"*{ext}"):
            artifact.unlink()
            print(f"[build.py] Removed {artifact.name}")

    print("\n[build.py] ✓ Build complete. PDFs at:")
    for mode in MODES:
        print(f"  - {PUBLIC_DIR / f'architect-{mode}.pdf'}")

    sys.exit(0)


if __name__ == "__main__":
    main()
