#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# TODO fix form styling in Create Experiments
# TODO make My Experiments and Home Page experiments cards clickable to detail
# view
# TODO Change to add Workspace option on Nav, where the workspace is the most
# recent experiment with the My Experiments view as the sidebar


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )

    current_path = Path(__file__).resolve().parent
    sys.path.append(str(current_path / "backend"))
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
