"""
Модуль розрахунку знижок — ПІСЛЯ рефакторингу.
"""

from enum import Enum
from decimal import Decimal

class CustomerType(Enum):
    REGULAR = "regular"
    PREMIUM = "premium"
    VIP = "vip"


DISCOUNT_RATES = {
    CustomerType.REGULAR: Decimal("0.00"),
    CustomerType.PREMIUM: Decimal("0.10"),
    CustomerType.VIP:     Decimal("0.15"),
}

def calculate_discount(amount: Decimal, customer_type: CustomerType) -> Decimal:
    """Розраховує знижку залежно від типу клієнта."""
    if amount < 0:
        raise ValueError("Сума не може бути від'ємною")
    return (amount * DISCOUNT_RATES[customer_type]).quantize(Decimal("0.01"))

def apply_discount(amount: Decimal, customer_type: CustomerType) -> Decimal:
    """Повертає суму після застосування знижки."""
    discount = calculate_discount(amount, customer_type)
    return amount - discount
