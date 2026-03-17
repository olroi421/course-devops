from decimal import Decimal


def apply_promo_code(total: Decimal, promo: str) -> Decimal:
    """
    Застосовує промокод до суми замовлення.

    SAVE10  → знижка 10 грн
    HALF    → знижка 50%
    FREE    → безкоштовно (0 грн)
    інший   → без знижки
    """
    if promo == "SAVE10":
        return total - Decimal("10")

    if promo == "HALF":
        return total * Decimal("0.5")

    if promo == "FREE":
        return Decimal("0.00")

    return total                           # невідомий промокод — без знижки


def calculate_shipping(total: Decimal) -> Decimal:
    """
    Розраховує вартість доставки.
    При сумі від 500 грн — безкоштовна доставка.
    """
    if total >= Decimal("500"):
        return Decimal("0.00")
    return Decimal("59.00")
