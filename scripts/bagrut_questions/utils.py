from dataclasses import dataclass, field
import os
import re
from typing import List, Tuple

# Supported media extensions for Bagrut questions (in priority order when deduplicating stems)
SUPPORTED_EXTENSIONS: Tuple[str, ...] = ("pdf", "png", "jpg", "jpeg")

_EXTENSIONS_PATTERN = "|".join(SUPPORTED_EXTENSIONS)
PATTERN = re.compile(
    rf"^(.+?)_(\d{{4}}[a-z]?)_(\d+[a-z]?)_(\d+[a-z]?)\.({_EXTENSIONS_PATTERN})$",
    re.IGNORECASE,
)


def parse_filename(filename: str) -> Tuple[str, str, str, str, str]:
    """
    Parse a question filename of the form:
        <topic_name>_<year>_<model>_<question_number>.<ext>

    Preserves original casing for `year`, `model`, and `qnum` (e.g. '899271B'),
    while normalizing `topic` and `extension` to lowercase.
    Returns ("UNKNOWN", ...) if the filename does not match.
    """
    match = PATTERN.match(os.path.basename(filename))
    if not match:
        return ("UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN")

    topic, year, model, qnum, extension = match.groups()
    return topic.lower(), year, model, qnum, extension.lower()


def natural_sort_key(value: str) -> Tuple:
    """
    Produce a tuple key for natural (human) sorting of alphanumeric strings
    so that '2' < '10' and '899271' < '899271B'.
    """
    parts = re.split(r"(\d+)", str(value))
    return tuple(int(p) if p.isdigit() else p.lower() for p in parts)


@dataclass
class QuestionRecord:
    """Structured representation of a single Bagrut question asset."""

    folder: str
    topic: str
    model: str
    year: str
    qnum: str
    has_sol: bool
    has_tex: bool
    file_path: str
    ext: str
    used_in: List[str] = field(default_factory=list)

    @property
    def is_used(self) -> bool:
        return len(self.used_in) > 0

    @property
    def stem(self) -> str:
        return os.path.splitext(os.path.basename(self.file_path))[0]

    @property
    def tex_path(self) -> str:
        return f"{os.path.splitext(self.file_path)[0]}.tex"

    @property
    def effective_topic(self) -> str:
        return "loops" if self.topic.startswith("loops_") else self.topic

    @property
    def latex_input(self) -> str:
        return f"\\input{{../../../bagrut_questions/{self.folder}/{self.stem}.tex}}"

    @property
    def repo_relative_path(self) -> str:
        return os.path.normpath(self.file_path).replace("\\", "/")
