from typing import List, Dict, Any, Optional, Iterable
from venv import logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")



class Validator:
    REQUIRED = ["order_id", "timestamp", "item", "quantity", "price", "payment_status", "total"]

    def __init__(self,
                 order_id: str,
                 timestamp,
                 item: str,
                 quantity: int,
                 price: float,
                 payment_status: str,
                 total: float):
        self.order_id = order_id
        self.timestamp = timestamp
        self.item = item
        self.quantity = quantity
        self.price = price
        self.payment_status = payment_status
        self.total = total

    def validate_rows(self):
        if self.total and self.price and self.quantity is None:
            return None

    def validate_int(self, a: int):
        if a is None or a == "":
            return None
        pass

    def validate_float(self, a: Any):
        if a is None or a == "":
            return None
        if isinstance(a, (int, float)) and not isinstance(a, bool):
            return float(a)
        pass

    def validate_str(self, a: Any):
        pass

        # for field in self.REQUIRED:
        #     if field not in row:
        #         logger.debug("Missing field %s in %s", field, row)
        #     return None
        # quantity = self.validate_int(row.get ("quantity"))
        # price = self.validate_float(row.get ("price"))
        # total = validate_float(row.get ("total"))
#checks

        if self.quantity is None or self.quantity < 0:
            logger.debug("Quantity cannot be None or negative")
            return None
        if self.price < 0:
            logger.debug("Price cannot be Negative")