"""Load many plain-text Ulauncher snippets from one phrases.json file.

The optional file lives alongside existing .j2 snippets. No additional Python
packages or background process are required.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

PHRASES_FILENAME = "phrases.json"
ICON_PATH = str(Path(__file__).resolve().parent.parent / "images" / "icon.png")


class PhraseSnippet:
    """Adapts a plain-text phrase to the existing Snippet UI contract."""

    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.description = content.replace("\n", " ")[:40]
        self.icon = ICON_PATH
        self.variables = {}
        self.file_path_template = None

    def next_variable(self):
        return None

    def render(self, args=None, copy_mode="gtk"):
        # Phrase text is literal, never interpreted as Jinja/HTML/commands.
        return ("text/plain", self.content)


@lru_cache(maxsize=8)
def _read_phrases(path, mtime_ns, size):
    """Cache parsed JSON until file metadata changes, avoiding per-keypress IO."""
    try:
        with open(path, encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, UnicodeError, ValueError) as exc:
        logger.warning("Cannot load phrases from %s: %s", path, exc)
        return ()

    if not isinstance(data, dict):
        logger.warning("Phrases file %s must contain a JSON object", path)
        return ()

    valid = []
    for name, content in data.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(content, str):
            logger.warning("Skipping invalid phrase %r in %s", name, path)
            continue
        valid.append((name, content))
    return tuple(valid)


def get_phrases(snippets_directory):
    """Return optional phrases; invalid/missing JSON never crashes extension."""
    path = Path(snippets_directory).expanduser() / PHRASES_FILENAME
    try:
        stat = path.stat()
    except (OSError, ValueError):
        return []
    return [PhraseSnippet(name, content)
            for name, content in _read_phrases(str(path), stat.st_mtime_ns, stat.st_size)]
