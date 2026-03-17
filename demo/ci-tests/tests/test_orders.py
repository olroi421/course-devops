"""
Тести для модуля обробки замовлень.

Запуск: pytest tests/test_orders.py -v
"""

import pytest
from decimal import Decimal
from src.orders import apply_promo_code, calculate_shipping


class TestApplyPromoCode:

    def test_save10_reduces_total(self):
        result = apply_promo_code(Decimal("100.00"), "SAVE10")
        assert result == Decimal("90.00")

    def test_half_gives_fifty_percent(self):
        result = apply_promo_code(Decimal("200.00"), "HALF")
        assert result == Decimal("100.00")

    def test_free_gives_zero(self):
        result = apply_promo_code(Decimal("300.00"), "FREE")
        assert result == Decimal("0.00")

    def test_unknown_promo_no_discount(self):
        result = apply_promo_code(Decimal("150.00"), "INVALID")
        assert result == Decimal("150.00")

    # -------------------------------------------------------
    # Цей тест виявляє прихований баг:
    # SAVE10 на суму 5 грн → результат -5 грн (від'ємна сума!)
    # -------------------------------------------------------
    def test_save10_cannot_make_total_negative(self):
        result = apply_promo_code(Decimal("5.00"), "SAVE10")
        assert result >= Decimal("0.00"), (
            f"Сума замовлення не може бути від'ємною, отримано: {result}"
        )


class TestCalculateShipping:

    def test_free_shipping_above_500(self):
        result = calculate_shipping(Decimal("500.00"))
        assert result == Decimal("0.00")

    def test_free_shipping_well_above_500(self):
        result = calculate_shipping(Decimal("1000.00"))
        assert result == Decimal("0.00")

    def test_paid_shipping_below_500(self):
        result = calculate_shipping(Decimal("499.99"))
        assert result == Decimal("59.00")

    def test_paid_shipping_small_order(self):
        result = calculate_shipping(Decimal("50.00"))
        assert result == Decimal("59.00")
