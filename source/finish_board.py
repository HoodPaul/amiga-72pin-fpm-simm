#!/usr/bin/env python3
"""Reapply A7 artwork without replacing the user's custom silkscreen layout."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('apply_a7_artwork.py')),run_name='__main__')
