#!/usr/bin/env python3
"""
Canonical entrypoint for Lexicon Locksmith.

Runs the accessibility v5 solver (ranking + accessibility modes) from the
lexicon_locksmith package. Prefer this over digging into accessibility/v5/.
"""

from lexicon_locksmith.solver import main

if __name__ == "__main__":
    main()
