#!/usr/bin/env python3
"""launch the CAS502 measles simulation GUI


Usage::

    python scripts/run_model.py
"""

import sys
from pathlib import Path

# make sure thatthe project root is on sys.path so that `cas502` can be imported
#no matter where the script is invoked from
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cas502.gui import MeaslesGUI


def main():
    app = MeaslesGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
