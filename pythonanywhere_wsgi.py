# pythonanywhere_wsgi.py
# ─────────────────────────────────────────────────────────────────
# On PythonAnywhere, go to:
#   Web tab → WSGI configuration file
# Replace the entire file content with this file's contents,
# then update the path below to match your home directory.
# ─────────────────────────────────────────────────────────────────

import sys
import os

# ✏️  Change this to your actual PythonAnywhere project path
PROJECT_PATH = "/home/YOUR_USERNAME/url_shortener"

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

os.chdir(PROJECT_PATH)

from app import app as application  # noqa: F401
