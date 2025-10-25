import re
from datetime import datetime
from typing import  Dict, Any, Optional
from reader import ShoplinkOrder
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")



class Validator:
    REQUIRED = ["order_id", "timestamp", "item", "payment_status"]
    OTHERS = ["quantity", "price", "total"]
    def __init__(self,
                 min_quantity: int = 1,
                 min_price: float = 0.1,
                 min_total: float = 0.1):

        self.min_quantity = min_quantity
        self.min_price = min_price
        self.min_total = min_total

    def validate_datatype(self, item: Dict[str, Any]):
        """Check data type and inspects quality, price and total fields."""

        if not isinstance(item, dict):
            logger.warning("Row is not a dictionary: %s", item)
            return None

    def validate_fields(self, item):
        for field in self.REQUIRED:
            if field not in item:
                logger.debug("Missing field %s in %s", field, item)
            return None
        present = [col for col in self.OTHERS if col in item]
        if len(present) < 2:
            logger.warning("Insufficient numeric fields in row: %s", item)
            return None

        return item
    def validate_nums(self, a: any):
        """Remove text and convert to float."""
        if isinstance(a, (int, float)) and not isinstance(a, bool):
            return float(a)
        if isinstance(a, str):
            cleaned = re.sub(r"[^\d.]", "", a)
            try:
                return float(cleaned)
            except ValueError:
                logger.debug("Failed to convert string to float: '%s'", a)
                return None
        logger.debug("Unsupported type for numeric cleaning: %s", type(a))
        return None

    def validate_timestamp(self, ts: str):
        """Normalize timestamp format: YYYY-MM-DDTHH:MM:00Z"""
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %I:%M %p",
            "%Y/%m/%dT%H:%MZ"
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(ts, fmt) # If "ts" matches "fmt", it returns a datetime.datetime object "dt"
                return dt.strftime("%Y-%m-%dT%H:%M:00Z")
            except ValueError:
                continue
        logger.warning("Unrecognized timestamp format: '%s'", ts)
        return None

    def validate_record(self, record: Dict[str, Any]):
        order_id = record.get("order_id")
        if not re.fullmatch(r"ORD\d+", str(order_id)):
            logger.warning("Invalid order_id format: '%s'", order_id)
            return None

        timestamp = self.validate_timestamp(record.get("timestamp", ""))
        if not timestamp:
            logger.warning("Invalid timestamp in record: %s", record)
            return None

        raw_item = record.get("item", "")
        item = raw_item.strip().lower() if isinstance(raw_item, str) else None
        if not item:
            logger.warning("Missing or invalid item field: '%s'", raw_item)
            return None

        quantity = self.validate_nums(record.get("quantity"))
        price = self.validate_nums(record.get("price"))
        total = self.validate_nums(record.get("total"))

        if any([
            quantity is not None and quantity < self.min_qty,
            price is not None and price < self.min_price,
            total is not None and total < self.min_total
        ]):
            logger.info("Record rejected due to values below thresholds: %s", record)
            return None

        values = {"quantity": quantity, "price": price, "total": total}         # If two values are present, calculate the third
        present = [key for key, value in values.items() if value is not None]

        if len(present) < 2:
            logger.warning("Not enough numeric values to compute missing field: %s", record)
            return None

        try:
            if quantity is None:
                quantity = total / price
                logger.debug("Computed missing quantity: %.2f", quantity)
            elif price is None:
                price = total / quantity
                logger.debug("Computed missing price: %.2f", price)
            elif total is None:
                total = quantity * price
                logger.debug("Computed missing total: %.2f", total)
        except Exception as e:
            logger.error("Error computing missing value: %s", e)
            return None

            raw_status = record.get("payment_status", "")            # check payment_status
            status = raw_status.strip().lower() if isinstance(raw_status, str) else None
            if status not in {"paid", "refunded", "pending"}:
                logger.warning("Invalid payment_status: '%s'", status)
                return None

            data_row = {
                "order_id": order_id,
                "timestamp": timestamp,
                "item": item,
                "quantity": round(quantity, 2),
                "price": round(price, 2),
                "total": round(total, 2),
                "payment_status": status
            }

            logger.info("Validated record: %s", data_row)

            cleaned_data = ShoplinkOrder(order_id=data_row["order_id"],
                                         timestamp=data_row["timestamp"],
                                         item=data_row["item"],
                                         payment_status=data_row["payment_status"],
                                         quantity=data_row["quantity"],
                                         price=data_row["price"],
                                         total=data_row["total"])

            return cleaned_data
