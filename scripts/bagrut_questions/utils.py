import re
import os

# Supported extensions for parsing
SUPPORTED_EXTENSIONS = ["pdf", "png", "jpg", "jpeg"]

# Build Regex pattern
supported_extensions_pattern = "|".join(SUPPORTED_EXTENSIONS)
PATTERN = re.compile(rf"(.+?)_(\d{{4}}[A-Z]?)_(\d+[A-Z]?)_(\d+[A-Z]?)\.({supported_extensions_pattern})$")

def parse_filename(filename):
    """
    Parse filename like: <topic_name>_<year>_<model>_<question_number>.<ext>
    Returns: topic, year, model, qnum, extension
    """
    match = PATTERN.match(filename)
    if not match:
        return ("UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN")

    prefixes, year, model, number, extension = match.groups()
    return prefixes, year, model, number, extension
