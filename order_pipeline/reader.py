from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Iterable
import csv
import json
import logging
import math
from collections import OrderedDict

class Reader:
    def __init__(self, path, file_format: str = "csv"):
        self.path = path
        self.file_format = file_format

    def read(self):
        if self.file_format == "csv":
            with open(self.path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                     yield dict(row)

        if self.file_format == "json":
            with open(self.path, newline="", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    yield dict(row)

        else:
            raise ValueError("format not supported; import csv or json" + self.format)