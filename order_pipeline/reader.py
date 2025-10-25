from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Iterable
import csv
import json
import logging
import math
from pathlib import Path
from collections import OrderedDict


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

@dataclass
class ShoplinkOrder:
    """ Dataclass for Shoplink order record. """

    order_id: str
    timestamp: str
    item: str
    payment_status: str
    quantity: float
    price: float
    total: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class Reader:
    """Read orders from CSV or JSON files"""
    def __init__(self, path: Path, file_format: str = "csv"):       #Initialization function
        self.path = path
        self.file_format = file_format

    def read_file(self):        #Read file function
        if self.file_format == "csv":       #CSV reader
            with open(self.path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                     yield dict(row)        #print rows as a generator

        if self.file_format == "json":      #JSON reader
            with open(self.path, newline="", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    yield dict(item)        #print items as a generator

        else:
            raise ValueError("format not supported; import csv or json" + self.file_format)