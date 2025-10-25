from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

class Transformer:
    """Transformer class used to transform Shoplink order records."""
    def __init__(self, index_cols=("order_id", "timestamp")):
        self.index_cols = index_cols
