from enum import StrEnum


class Column(StrEnum):
    TRANSACTION_ID = "Transaction ID"
    DATE = "Date"
    VENDOR = "Vendor"
    CATEGORY = "Category"
    PRICE = "Price"
    IS_FOOD = "Is Food"
    CONTROLLABLE = "Controllable"
